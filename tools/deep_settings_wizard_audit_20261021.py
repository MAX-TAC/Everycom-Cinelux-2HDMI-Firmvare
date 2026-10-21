#!/usr/bin/env python3
"""Audit provisioning responsibilities, OEM settings equivalence, TvSettingsPlus paths,
and static code risk markers from SHA-verified 8052.1.0.4 APKs.
Read-only; publish derived locations and identifiers, not decompiled proprietary source.
"""
import json, hashlib, re, subprocess, shutil, collections, zipfile
from pathlib import Path

BASE=Path("/tmp/erofs")
OUT=Path("analysis/Settings_Wizard_Debloat_20261021")
OUT.mkdir(parents=True,exist_ok=True)
INPUT={
 "KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk",
 "KuSettings":"system/system/app/KuSettings/KuSettings.apk",
 "TvSettingsPlus":"system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk"
}
# Indicator names, not proof of an active Android lifecycle path.
SIGNALS={
 "provision_flag":r"DEVICE_PROVISIONED|USER_SETUP_COMPLETE|device_provisioned|user_setup_complete|setup_wizard|SETUP_WIZARD",
 "boot_setup":r"BOOT_COMPLETED|LOCKED_BOOT_COMPLETED|onBootCompleted|BootupReceiver|ProvisionWifiActivity|DEVICE_PROVISIONED",
 "provision_components":r"DevicePolicyManager|setUserProvisioningState|setUserSetupComplete|setProvisioned|Settings[.](?:Global|Secure)[.]putInt|Settings[.](?:Global|Secure)[.]putString",
 "package_dependencies":r"com[.]my[.]settings|com[.]coolux[.]source|com[.]hysd[.]screen|com[.]android[.]tv[.]settings|com[.]android[.]provision",
 "hardware":r"MotorJNI|IProjectorCtrl|ITofCtrl|TrdSystemManager|I2CDevice|writeRegister|readRegister|setBootSource|TofCtrl|ProjectorManager",
 "persistence":r"Settings[.](?:Secure|System|Global)[.](?:put|get)|SystemProperties[.](?:set|get)|SharedPreferences|PreferenceManager|persist[.]",
 "launch":r"startActivity|startService|sendBroadcast|setComponent|setClassName|setPackage|Intent[.]ACTION|android[.]settings[.]SETTINGS",
 "lifecycle":r"registerReceiver|unregisterReceiver|bindService|unbindService|onStartCommand|onDestroy|onStop|onResume|onPause",
 "risk_candidates":r"printStackTrace|catch[ ]*[(][ ]*(?:Exception|Throwable)|Thread[.]sleep|System[.]exit|Runtime[.]getRuntime[(][)][.]exec|ProcessBuilder|catch[ ]*[(][^)]*[)][ ]*[{][ ]*[}]|getSystemService[(]|open[(]|writeRegister[(]",
 "remote":r"KeyEvent|dispatchKeyEvent|onKeyDown|HOME|LEANBACK_SETTINGS|TRD_POPMENU|SOURCE"
}
RX={k:re.compile(v,re.I) for k,v in SIGNALS.items()}
TARGET_PREFIXES={
 "KuSetupWizard":("com/my/","com/android/provision/"),
 "KuSettings":("com/my/","com/android/provision/"),
 "TvSettingsPlus":("com/android/tv/settings/","com/mediatek/wwtv/","com/google/android/tv/settings/")
}
FOCUS_FILES={
 "KuSetupWizard":r"(ProvisionWifiActivity|ProvisionBluetoothActivity|SettingActivity|IntentUtils|Provision|BootupReceiver|SetupWizard|MyWifiActivity)[.]java$",
 "KuSettings":r"(BootupReceiver|ScreenServices|SettingActivity|IntentUtils|ProjectionActivity|MyWifiActivity|MyBluetoothActivity|TimeService)[.]java$",
 "TvSettingsPlus":r"(MainSettings|MainFragment|MainActivity|ProjectorFragment|FocusSettingsFragment|KeystoneCalibrationActivity|ProjectorSubMenuController|SourceSubMenuController|PictureModeFragment|PictureModeValueFragment|GammaFragment|BrightnessModeSettingsFragment|AudioOutputFragment|TvBootupReceiver|WirelessSpeakerServices|SoundEARCReceiver|BootReceiver)[.]java$"
}
FUNCTION_RX=re.compile(r"(?m)^\s*(?:(?:public|private|protected|static|final|synchronized|native|override)\s+){1,5}[\w\s<>\[\],.?$]+\s+([A-Za-z_]\w*)\s*\([^;{}]*\)\s*(?:throws\s+[\w., ]+)?(?:\{|;)")
SAFETY=re.compile(r"(?i)(?:password|passphrase|secret|token|private.?key|ssid|device.?id|serial.?number|advertising.?id|mac.?address)")
def cmd(args,seconds=90):
 return subprocess.run(args,capture_output=True,text=True,errors="replace",timeout=seconds)
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as fh:
  for block in iter(lambda:fh.read(1048576),b""):h.update(block)
 return h.hexdigest()
result={"sources":{"board8052":"RUIOS.8052.1.0.4 Oct OTA",
                    "board8054":"RUIOS.8054.1.0.1 Sep factory (identical related APKs, not current 8054 OTA)"},
        "apps":{},"limitations":[]}
for name,rel in INPUT.items():
 path=BASE/rel
 assert path.is_file(),str(path)
 work=Path("/tmp/settings-audit-"+name)
 p=cmd(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3",
        "-d",str(work),str(path)],seconds=960)
 source=work/"sources"
 assert source.is_dir(),"No JADX sources for "+name+": "+p.stderr[-500:]
 files=list(source.rglob("*.java"))
 owned=[f for f in files if f.relative_to(source).as_posix().startswith(TARGET_PREFIXES[name])]
 prefixes=collections.Counter()
 selected=[]
 hits=collections.defaultdict(list)
 counts=collections.Counter()
 method_classes=[]
 external_refs=collections.Counter()
 for f in owned:
  r=f.relative_to(source).as_posix()
  # TvSettingsPlus partitions of code
  parts=r.split("/")
  if name=="TvSettingsPlus":
   subgroup=parts[4] if len(parts)>4 and r.startswith("com/android/tv/settings/") else "other"
  else:
   subgroup=parts[2] if len(parts)>2 else "root"
  prefixes[subgroup]+=1
  txt=f.read_text(errors="replace")
  lines=txt.splitlines()
  file_signals=collections.Counter()
  matched_methods=[]
  if name=="TvSettingsPlus" and re.search(r"(?i)(?:projector|focus|keystone|trapezoid|tof|source|bright|audio|picture|hdmi|settings|gamma|power|mode)",r):
   matched_methods=[m.group(1) for m in FUNCTION_RX.finditer(txt)][:45]
   if matched_methods and len(method_classes)<160:
    method_classes.append({"file":r,"methods":matched_methods,"signals":[]})
  important=bool(re.search(FOCUS_FILES[name],r,re.I))
  for n,line in enumerate(lines,1):
   if SAFETY.search(line):continue
   for tag,pattern in RX.items():
    match=pattern.search(line)
    if not match:continue
    counts[tag]+=1
    file_signals[tag]+=1
    if important and len(hits[tag])<130:
     # publish only matched public API/symbol identifiers, no source lines
     toks=sorted(set(m.group(0) for m in pattern.finditer(line)))
     hits[tag].append({"file":r,"line":n,"identifiers":toks[:4]})
   for pkg in re.findall(r"com\.(?:my\.settings|coolux\.source|android\.tv\.settings|android\.provision|trd\.service|hysd\.screen)",line):
    external_refs[pkg]+=1
  if important:
   selected.append({"file":r,"lines":len(lines),"signals":dict(file_signals),
                    "methods":[m.group(1) for m in FUNCTION_RX.finditer(txt)][:55]})
 apk_data={"source_apk":rel,"sha256":sha(path),"jadx_exit":p.returncode,
    "total_java_files":len(files),"owned_java_files":len(owned),"code_groups":dict(prefixes),
    "api_counts":dict(counts),"selected_classes":selected[:90],
    "interesting_classes":method_classes[:160],"api_call_sites":dict(hits),
    "reference_counts":dict(external_refs)}
 # Avoid over-interpreting zero matches. Also inspect APK namespaces, app metadata.
 manifest=cmd(["aapt","dump","xmltree",str(path),"AndroidManifest.xml"],seconds=50)
 aapt=manifest.stdout
 apk_data["manifest_component_counts"]=dict(collections.Counter(re.findall(r"E: (activity|activity-alias|service|receiver|provider)\b",aapt)))
 apk_data["manifest_setup_flags"]=sorted(set(re.findall(r"android\.intent\.(?:category\.)?(?:SETUP_WIZARD|HOME)|BOOT_COMPLETED|DEVICE_PROVISIONED|android\.settings\.\w+",aapt)))
 badging=cmd(["aapt","dump","badging",str(path)],seconds=50)
 apk_data["requested_permissions"]=sorted(set(re.findall(r"uses-permission: name='([^']+)'",badging.stdout)))
 result["apps"][name]=apk_data
 shutil.rmtree(work,ignore_errors=True)
 print("APP",name,"classes",len(owned),"groups",dict(prefixes),"APIs",dict(counts),flush=True)
(OUT/"deep_settings_wizard_analysis.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
# Structured MD; no ungrounded claim of bug or unique operation.
md=["# Deep static audit of KuSetupWizard, KuSettings and TvSettingsPlus",
"",
"Based on verified RUIOS 8052.1.0.4 source APKs. TvSettingsPlus and KuSettings are byte-identical in the archived original Sep 8054.1.0.1, while original updated 8054.1.0.4 is unavailable.",
"",
"**JADX API occurrences are search signals only. They do not prove a reachable code path, a crash, or firmware incompatibility.**",
"",
"## Java classes and manifest coverage","",
"| APK | Decompiled Java files | OEM-owned files | Manifest components |",
"|---|---:|---:|---|"]
for n,d in result["apps"].items():
 md.append("| "+n+" | "+str(d["total_java_files"])+" | "+str(d["owned_java_files"])+" | "+str(d["manifest_component_counts"])+" |")
for n,d in result["apps"].items():
 md+=["","## "+n,"",
      "**Namespace-group file counts:** "+", ".join(k+"="+str(v) for k,v in d["code_groups"].items()),"",
      "**Observed code API families:** "+", ".join(k+"="+str(v) for k,v in d["api_counts"].items()),"",
      "### Important concrete Java classes and method names",""]
 for f in d["selected_classes"][:80]:
  md.append("- "+f["file"]+": "+", ".join(f["methods"][:24])+"; evidence "+str(f["signals"]))
 md+=["","### High-risk or migration-relevant API call sites",""]
 for tag in ("provision_flag","boot_setup","provision_components","hardware","persistence","lifecycle","risk_candidates"):
  if tag not in d["api_call_sites"]:continue
  md.append("**"+tag+"**")
  for hit in d["api_call_sites"][tag][:42]:
   md.append("- "+hit["file"]+":"+str(hit["line"])+": "+", ".join(hit["identifiers"]))
md+=["","## Decision discipline","",
"- \`KuSetupWizard\` cannot be removed just because its Java library copies \`KuSettings\`; its package \`com.android.provision\` has different setup lifecycle and intent filters.",
"- \`TvSettingsPlus\` is a modified Android TV Settings; existing \`uicustom\` and \`partnercustomizer\` should be reused where tested; AOSP baseline source comparison is required to assign a defect to an OEM change.",
"- FLauncher must explicitly open \`com.android.tv.settings/.MainSettings\`; \`android.settings.SETTINGS\` resolves to OEM \`KuSettings\` on stock manifests.",
"- For any apparent bug candidate, read the full method and inbound call chain, check error handling and show a reproducible device scenario before calling it a confirmed defect.",
"- No APK code or binaries were altered, no device was accessed.",
""]
(OUT/"DEEP_SETTINGS_WIZARD_RU.md").write_text("\n".join(md)+"\n")
