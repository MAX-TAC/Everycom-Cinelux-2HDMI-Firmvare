#!/usr/bin/env python3
"""Focused, reproducible static 8052 OTA audit of settings entry points, dispatch and signing.
Output only app metadata and short contextual markers, not proprietary decompiled code.
No Android device, firmware or data is changed.
"""
import collections,hashlib,json,re,subprocess,shutil
from pathlib import Path

ROOT=Path("/tmp/erofs")
OUT=Path("analysis/Global_Firmware_Map_20261021")
OUT.mkdir(parents=True,exist_ok=True)
APKS={
 "TvSettingsPlus":"system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk",
 "KuSettings":"system/system/app/KuSettings/KuSettings.apk",
 "trdservice":"system/system/app/trdservice/trdservice.apk",
 "zxlauncher":"system/system/app/zxlauncher/zxlauncher.apk",
 "RuiAutoFocus":"system/system/app/RuiAutoFocus/RuiAutoFocus.apk",
 "KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk",
 "KeystoneCorrection":"system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk",
 "KuSourceRJ":"system/system/app/KuSourceRJ/KuSourceRJ.apk",
 "RuiYunOta":"system/system/priv-app/RuiYunOta/RuiYunOta.apk",
 "SystemUI":"system_ext/priv-app/SystemUI/SystemUI.apk",
 "SettingsProvider":"system/system/priv-app/SettingsProvider/SettingsProvider.apk"}
# Sources may have one or two nested system directories depending on how OTA was unpacked.
REGEX=re.compile(r'com\.android\.tv\.settings|com\.my\.settings|com\.trd\.projector\.settings|android\.settings\.SETTINGS|ACTION_SETTINGS|KEYCODE_TRD_POPMENU|TRD_POPMENU|KEYCODE_MENU|KEYCODE_SETTINGS|android\.intent\.category\.LAUNCHER|LEANBACK_LAUNCHER|GlobalKeyEventProcess|com\.zeasn\.whale\.saas',re.I)
SOURCES={
 "TvSettingsPlus":("com/android/tv/settings/MainSettings.java",
                   "com/android/tv/settings/uicustom/MainActivity.java",
                   "com/android/tv/settings/uicustom/fragment/general/GeneralFragment.java"),
 "KuSettings":("com/my/settings/SettingActivity.java","com/my/utils/IntentUtils.java"),
 "trdservice":("com/trd/service/communication/GlobalKeyEventProcess.java",),
 "zxlauncher":("com/zeasn/utils/TvSetting.java","com/zeasn/utils/AppUtil.java",
               "com/zeasn/launcher/CustomApplication.java"),
 "RuiAutoFocus":("com/hysd/client/VAF2S.java",)
}
report={"source":"verified 8052 2026-10 OTA; no 8054.1.0.4 dump",
        "apps":{},"dispatch":{},"keylayout":{},"limitations":[]}
def cmd(args,timeout=120):
 return subprocess.run(args,capture_output=True,text=True,errors="replace",timeout=timeout)
def sha(data):return hashlib.sha256(data).hexdigest()
def find_package(aapt):
 m=re.search(r"package: name='([^']+)'",aapt)
 return m.group(1) if m else None
def safe_xml_manifest(apk):
 p=cmd(["aapt","dump","xmltree",str(apk),"AndroidManifest.xml"],timeout=80)
 if p.returncode:return {"error":"aapt returned "+str(p.returncode)}
 # Preserve flags for each activity, alias and their action/category-filter strings, no code.
 items=[];cur=None;depth=-1;actdepth=-1;activefilter=False
 for line in p.stdout.splitlines():
  m=re.match(r"^(\s*)E: ([\w-]+)",line)
  if m:
   indent=len(m.group(1));tag=m.group(2)
   if tag in ("activity","activity-alias","service","receiver","provider"):
    cur={"kind":tag,"name":None,"exported":None,"actions":[],"categories":[],"target":None}
    items.append(cur);depth=indent;actdepth=indent
   elif cur and indent<=actdepth:
    cur=None
   elif cur and tag=="intent-filter":activefilter=True
   continue
  if not cur:continue
  attr=re.match(r"^(\s*)A: android:([a-zA-Z]+)(?:[^=]*)=(.*)$",line)
  if not attr:continue
  indent=len(attr.group(1));kind=attr.group(2);raw=attr.group(3)
  value=re.search(r'"([^"]+)"',raw)
  val=value.group(1) if value else None
  if indent==depth+2 and kind=="name" and val:cur["name"]=val
  elif indent==depth+2 and kind=="targetActivity" and val:cur["target"]=val
  elif indent==depth+2 and kind=="exported":
   b=re.search(r"\(type 0x12\)0x([0-9A-Fa-f]+)",raw)
   cur["exported"]=bool(int(b.group(1),16)) if b else val=="true" if val in ("true","false") else None
  elif kind=="name" and val and indent>=depth+4:
   if val.startswith("android.intent.action.") or val.startswith("android.settings.") or ".action." in val:
    if val not in cur["actions"]:cur["actions"].append(val)
   elif val.startswith("android.intent.category.") or "LAUNCHER" in val:
    if val not in cur["categories"]:cur["categories"].append(val)
 return {"components_total":len(items),"entrypoint_candidates":[x for x in items if x["kind"] in ("activity","activity-alias") and (x["exported"] is True or x["actions"] or x["categories"] or any(k in str(x["name"]) for k in ("Settings","Setting","MainActivity","MainSettings")))],
         "boot_receivers":[x for x in items if x["kind"]=="receiver" and any("BOOT" in a or "PACKAGE_" in a for a in x["actions"])]}
for name,path in APKS.items():
 apk=ROOT/path
 if not apk.is_file():
  report["limitations"].append("Unavailable "+name+" "+path)
  continue
 badging=cmd(["aapt","dump","badging",str(apk)],timeout=80)
 info={"path":path,"sha256":sha(apk.read_bytes()),"package":find_package(badging.stdout)}
 info["manifest"]=safe_xml_manifest(apk)
 signer=cmd(["apksigner","verify","--print-certs",str(apk)],timeout=80) if shutil.which("apksigner") else None
 if signer and (signer.returncode==0 or "Signer #1 certificate SHA-256 digest" in signer.stdout):
  digests=re.findall(r"Signer #\d+ certificate SHA-256 digest:\s*([0-9a-fA-F:]+)",signer.stdout)
  info["signer_cert_sha256"]=digests
  info["apksigner_verified"]=signer.returncode==0
 else:info["signer_cert_sha256"]=[];info["signer_error"]="apksigner missing or unable to verify original APK"
 report["apps"][name]=info
 print("APP",name,info["package"],len(info["manifest"].get("entrypoint_candidates",[])),info["signer_cert_sha256"],flush=True)

for name,requested in SOURCES.items():
 apk=ROOT/APKS[name]
 if not apk.exists():continue
 work=Path("/tmp/jadx-settings-"+name)
 args=["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3",
       "--show-bad-code","-d",str(work),str(apk)]
 r=cmd(args,timeout=850)
 sources=work/"sources"
 if not sources.exists():
  report["limitations"].append("JADX no sources: "+name)
  continue
 matched=[]
 for wanted in requested:
  candidate=sources/wanted
  if not candidate.exists():
   # Package obfuscation or no source for file; search by last basename
   hits=list(sources.rglob(Path(wanted).name))
   if len(hits)==1:candidate=hits[0]
   else:
    report["limitations"].append("No unique source: "+name+"/"+wanted)
    continue
  text=candidate.read_text(errors="replace")
  lines=text.splitlines()
  entries=[]
  for k,line in enumerate(lines):
   hits=REGEX.findall(line)
   if not hits:continue
   # avoid full source publishing; only named API identifiers and dispatch indicator within 12-line window
   lo=max(0,k-8);hi=min(len(lines),k+10)
   nearby="\n".join(lines[lo:hi])
   ops=sorted(set(re.findall(r"\b(?:startActivity|startService|sendBroadcast|setAction|setClassName|setComponent|setPackage|getKeyCode|onKeyDown|onKeyUp|dispatchKeyEvent|getLaunchIntentForPackage|resolveActivity|startActivityAsUser|isPackageInstalled)\b",nearby)))
   near_constants=sorted(set(re.findall(r'\b(?:KEYCODE_[A-Z_]+|TRD_POPMENU|(?:android|com)\.[A-Za-z0-9_.]{6,120})\b',line)))[:12]
   # Mask urls/tokens by only displaying identifiers, never whole quoted strings
   entries.append({"line":k+1,"match":sorted(set(hits)),"calls_nearby":ops,"symbols":near_constants})
  if entries:matched.append({"file":candidate.relative_to(sources).as_posix(),"entries":entries[:140]})
 report["dispatch"][name]={"files":matched,"jadx_exit":r.returncode}
 shutil.rmtree(work,ignore_errors=True)
 print("JADX",name,"sourcefiles",len(matched),"references",sum(len(x["entries"]) for x in matched),flush=True)

# Enumerate known hardware key codes from actual OTA, not assumptions about physical device.
kl=ROOT/"vendor/usr/keylayout/Vendor_3697_Product_0001.kl"
if kl.exists():
 report["keylayout"]={"path":kl.relative_to(ROOT).as_posix(),"keys":[
   {"scan":m.group(1),"android":m.group(2)} for line in kl.read_text().splitlines()
   if (m:=re.match(r"^\s*key\s+(\w+)\s+(\w+)",line)) and m.group(2) in
   ("TRD_POPMENU","MENU","FOCUS","FOCUS_RESET","FOCUS_PLUS","FOCUS_MINUS","SOURCE","HOME","TV_INPUT")]}
(OUT/"SETTINGS_DISPATCH_8052_EVIDENCE.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
lines=["# TvSettingsPlus versus KuSettings versus Zeasn launcher: where Settings opens",
"",
"Source: Oct 8052.1.0.4 verified OTA. Important: TvSettingsPlus, KuSettings, trdservice APKs are **byte-identical** to the only available Sep stock 8054.1.0.1. That does not guarantee same runtime components or settings launch policy.",
"",
"## APK certificates, package and exported activity candidates","",
"| App | Package | Cert SHA256 | Entry candidates |",
"|---|---|---|---:|"]
for name,a in report["apps"].items():
 lines.append("| "+name+" | "+str(a["package"])+" | "+(", ".join(a["signer_cert_sha256"][:1]) if a["signer_cert_sha256"] else "unverified")+" | "+str(len(a["manifest"].get("entrypoint_candidates",[])))+" |")
for name,a in report["apps"].items():
 entries=a["manifest"].get("entrypoint_candidates",[])
 if name not in ("TvSettingsPlus","KuSettings","trdservice","zxlauncher","RuiAutoFocus","KuSetupWizard"):continue
 lines+=["","## "+name+" declared activity entrypoints",""]
 for x in entries[:100]:
  lines.append("- "+str(x["name"])+", exported="+str(x["exported"])+", actions="+str(x["actions"][:4])+", categories="+str(x["categories"][:4]))
for name,p in report["dispatch"].items():
 lines+=["","## "+name+" key code / settings dispatch evidence",""]
 for f in p["files"]:
  lines+=["### "+f["file"],""]
  for x in f["entries"][:95]:
   lines.append("- line "+str(x["line"])+": "+", ".join(x["match"])+"; dispatch APIs nearby: "+", ".join(x["calls_nearby"])+"; symbols: "+", ".join(x["symbols"][:6]))
lines+=["","## Physical remote caveat","",
"Hardware key layout maps TRD_POPMENU but does not prove which button sends it or which target Activity ultimately launches. Photo of remote alone cannot establish dispatch.",
"",
"## Signing distinction","",
"- Any modified APK must be signed with a key. OEM platform signature may be required for signature-level permissions; a new key is **not** equivalent.",
"- privapp-permissions XML can allow privileged permissions, but not change APK signer identity, existing package upgrade checks or all signature-only permissions.",
"- System partitions may separately be verified by AVB; signing APK alone cannot make a modified system image bootable.",
"- Do not ship re-signed TvSettingsPlus before checking cert relations with SystemUI/SettingsProvider and whether sharedUserId/signature checks exist.",
"",
"## Runtime unverified","",
"- ACTION_SETTINGS/Settings intent resolution, getComponentEnabledSettings, privileged grants, keyboard dispatch and installed updated apps need actual device evidence.",
"- Current binary comparison of two board profiles has 8052 Oct 1.0.4 vs **8054 Sep 1.0.1**, not latest 8054 1.0.4.",
""]
(OUT/"SETTINGS_DISPATCH_8052_RU.md").write_text("\n".join(lines)+"\n")
print("DONE","APKs",len(report["apps"]),"JADX",len(report["dispatch"]),flush=True)
