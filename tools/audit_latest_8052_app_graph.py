#!/usr/bin/env python3
"""OEM read-only app dependency and possible defect candidate survey."""
import collections,hashlib,json,re,subprocess,shutil
from pathlib import Path
root=Path("/tmp/erofs")
targets={
"zxlauncher":"system/system/app/zxlauncher/zxlauncher.apk",
"zxstore":"system/system/app/zxstore/zxstore.apk",
"KuSettings":"system/system/app/KuSettings/KuSettings.apk",
"TvSettingsPlus":"system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk",
"RuiYunOta":"system/system/priv-app/RuiYunOta/RuiYunOta.apk",
"KuSourceRJ":"system/system/app/KuSourceRJ/KuSourceRJ.apk",
"RuiAutoFocus":"system/system/app/RuiAutoFocus/RuiAutoFocus.apk",
"KeystoneCorrection":"system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk",
"trdservice":"system/system/app/trdservice/trdservice.apk",
"trdmiddle":"vendor/priv-app/trdmiddle/trdmiddle.apk",
"Factory":"system_ext/app/Factory/Factory.apk",
"TvServices":"system_ext/priv-app/TvServices/TvServices.apk",
"LiveTV":"system_ext/priv-app/LiveTV/LiveTV.apk",
"KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk"
}
signals={
"binder":r"ServiceManager.getService|ITrdSystemService|TrdSystemManager|getProjectorCtrl|getTofCtrl",
"motor_tof":r"MotorJNI|MotorFront|MotorBack|MotorStop|startTof|ITofCtrl",
"i2c":r"I2CDevice|readRegister|writeRegister|/dev/i2c-",
"hdmi":r"HdmiControlManager|HDMI_CEC|setBootSource|selectInput|switchSource",
"ota":r"UpdateEngine|OTACheckService|RuiYunOta|OTASystemNetworkUpdateActivity",
"installer":r"INSTALL_SUCCESS|PackageInstaller|ACTION_INSTALL_PACKAGE|REQUEST_INSTALL_PACKAGES",
"settings":r"WRITE_SECURE_SETTINGS|Settings.Secure.put|Settings.Global.put|SystemProperties.set",
"review":r"Runtime.getRuntime().exec|System.exit|ProcessBuilder"
}
pattern=re.compile("|".join("(?P<"+k+">"+v+")" for k,v in signals.items()),re.I)
untrusted=re.compile(r"serial|macaddress|ssid|password|secret|privatekey|token|hdcp|widevine",re.I)
data={"source":"Latest SHA256-verified 8052 OTA 2026-10-12","apps":{}}
for name,rel in targets.items():
    apk=root/rel
    if not apk.is_file():
        data["apps"][name]={"missing":True};print("MISSING",name,flush=True);continue
    info={"sha256":hashlib.sha256(apk.read_bytes()).hexdigest(),"package":None,"permissions":[],"launcher":[],
          "manifest_component_counts":{},"has_boot_completed":False,"home_hint":False,
          "classes":0,"match_counts":{},"samples":{},"decompile_exit":None}
    cmd=subprocess.run(["aapt","dump","badging",str(apk)],capture_output=True,text=True,errors="replace",timeout=60)
    m=re.search(r"package: name='([^']+)'",cmd.stdout)
    if m:info["package"]=m.group(1)
    info["permissions"]=sorted(set(re.findall(r"uses-permission: name='([^']+)'",cmd.stdout)))
    info["launcher"]=re.findall(r"launchable-activity: name='([^']+)'",cmd.stdout)
    tree=subprocess.run(["aapt","dump","xmltree",str(apk),"AndroidManifest.xml"],
                        capture_output=True,text=True,errors="replace",timeout=60)
    info["manifest_component_counts"]=dict(collections.Counter(re.findall(r"E: (activity|service|receiver|provider)\b",tree.stdout)))
    info["has_boot_completed"]="BOOT_COMPLETED" in tree.stdout
    info["home_hint"]="android.intent.category.HOME" in tree.stdout or "android.intent.category.LAUNCHER" in tree.stdout
    dest=Path("/tmp/oemaudit-"+name)
    jadx=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3","-d",str(dest),str(apk)],
                        capture_output=True,text=True,errors="replace",timeout=650)
    info["decompile_exit"]=jadx.returncode
    sources=dest/"sources";java=list(sources.rglob("*.java")) if sources.exists() else []
    info["classes"]=len(java)
    counts=collections.Counter();samples=collections.defaultdict(list)
    for f in java:
        rel=f.relative_to(sources).as_posix()
        for num,line in enumerate(f.read_text(errors="replace").splitlines(),1):
            if untrusted.search(line):continue
            for m in pattern.finditer(line):
                k=m.lastgroup
                counts[k]+=1
                if len(samples[k])<25:
                    samples[k].append({"class":rel,"line":num,"identifier":m.group(0)[:90]})
    info["match_counts"]=dict(counts);info["samples"]=dict(samples)
    data["apps"][name]=info
    shutil.rmtree(dest,ignore_errors=True)
    print("SCANNED",name,"classes",len(java),"patterns",dict(counts),flush=True)
out=Path("analysis/Deep_Stock_Audit_20261021")
out.mkdir(exist_ok=True,parents=True)
(out/"latest_8052_app_graph.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
lines=["# Latest 8052 stock APK dependency and code review index","",
"Read-only AAPT/JADX scan of verified October OTA. Only code reference identifiers and locations are retained.",
"Presence of a token in decompiled output **does not prove invocation, dependency or bug**.",
"",
"| App | Package | Decompiled Java files | BOOT_COMPLETED | Manifest HOME/LAUNCHER hint | OEM hardware references |",
"|---|---|---:|---|---|---:|"]
for name,v in data["apps"].items():
    if v.get("missing"):
        lines.append("| "+name+" | missing | - | - | - | - |");continue
    important=sum(v["match_counts"].get(x,0) for x in ("binder","motor_tof","i2c","hdmi"))
    lines.append("| "+name+" | "+str(v["package"])+" | "+str(v["classes"])+
                 " | "+str(v["has_boot_completed"])+" | "+str(v["home_hint"])+" | "+str(important)+" |")
for name,v in data["apps"].items():
    if v.get("missing"):continue
    lines+=["","## "+name,"",
            "- APK SHA256: "+v["sha256"],
            "- Component counts: "+str(v["manifest_component_counts"]),
            "- Launcher activities: "+str(v["launcher"]),
            "- Permissions: "+", ".join(v["permissions"]),
            "- Signal occurrences: "+str(v["match_counts"]),
            "","### Candidate review locations"]
    for k,vals in v["samples"].items():
        for item in vals[:8]:
            lines.append("- "+k+": "+item["class"]+":"+str(item["line"])+" ("+item["identifier"]+")")
lines+=["","## Interpretation and next checks","",
"- First trace actual outgoing/incoming intents, Binder calls, listener lifecycles and system permissions.",
"- Check launcher fallback and early-boot hooks before considering any app replacement.",
"- Verify OTA, HDMI selection, focus/ToF, keystone and hardware recovery on real devices.",
"- Never label method-pattern occurrences as confirmed defects until control flow and triggers are verified.",
"- No packages were disabled, removed, executed, or modified.",
""]
(out/"LATEST_8052_APP_GRAPH_RU.md").write_text("\n".join(lines)+"\n")
print("DONE",len(data["apps"]),flush=True)
