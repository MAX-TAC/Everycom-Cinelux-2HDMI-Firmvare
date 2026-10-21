#!/usr/bin/env python3
"""Determine whether OEM setup wizard and settings reuse the same Java implementation.
Reports normalized class digests and manifest component names, never source contents.
"""
import hashlib,json,re,subprocess,shutil
from pathlib import Path
pairs={
"KuSettings":Path("/tmp/erofs/system/system/app/KuSettings/KuSettings.apk"),
"KuSetupWizard":Path("/tmp/erofs/system/system/app/KuSetupWizard/KuSetupWizard.apk")
}
data={"apps":{},"shared_java":{}}
def sha(data):return hashlib.sha256(data).hexdigest()
for name,apk in pairs.items():
    assert apk.is_file(),str(apk)
    work=Path("/tmp/cmp-oem-"+name)
    p=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3","-d",str(work),str(apk)],
                     capture_output=True,text=True,errors="replace",timeout=660)
    root=work/"sources"
    assert root.is_dir(),p.stderr[-350:]
    names={}
    for f in root.rglob("*.java"):
        rel=f.relative_to(root).as_posix()
        text=f.read_text(errors="replace")
        text=re.sub(r"(?s)/\*.*?\*/","",text)
        text=re.sub(r"(?m)^\s*//.*$","",text)
        text=re.sub(r"\s+"," ",text).strip()
        names[rel]=sha(text.encode())
    b=subprocess.run(["aapt","dump","badging",str(apk)],capture_output=True,text=True,errors="replace",timeout=50)
    package=re.search(r"package: name='([^']+)'",b.stdout)
    xml=subprocess.run(["aapt","dump","xmltree",str(apk),"AndroidManifest.xml"],capture_output=True,text=True,errors="replace",timeout=50)
    tokens=re.findall(r'E: (activity|receiver|provider|service)\b',xml.stdout)
    data["apps"][name]={"package":package.group(1) if package else None,
         "apk_sha256":sha(apk.read_bytes()),
         "class_count":len(names),
         "components":{k:tokens.count(k) for k in sorted(set(tokens))},
         "classes":names}
    shutil.rmtree(work,ignore_errors=True)
    print("APP",name,len(names),data["apps"][name]["package"],flush=True)
a=data["apps"]["KuSettings"]["classes"]
b=data["apps"]["KuSetupWizard"]["classes"]
inter=set(a)&set(b)
same=[x for x in sorted(inter) if a[x]==b[x]]
modified=[x for x in sorted(inter) if a[x]!=b[x]]
data["shared_java"]={"common_paths":len(inter),"bytecode_decompiled_class_same":len(same),
                     "changed":len(modified),"only_settings":len(set(a)-set(b)),
                     "only_wizard":len(set(b)-set(a)),
                     "identical_fraction_common":round(len(same)/len(inter),4) if inter else None,
                     "changed_paths":modified[:100],
                     "only_settings_paths":sorted(set(a)-set(b))[:100],
                     "only_wizard_paths":sorted(set(b)-set(a))[:100]}
# To avoid inflating metadata repository, do not commit 6000 class hashes.
for obj in data["apps"].values():obj.pop("classes")
out=Path("analysis/Deep_Stock_Audit_20261021")
out.mkdir(parents=True,exist_ok=True)
(out/"setup_settings_overlap.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
stats=data["shared_java"]
lines=["# OEM KuSetupWizard versus KuSettings — source clone analysis","",
"Source: SHA256-verified OTA RUIOS.8052.1.0.4. Reconstructed Java code was not published.",
"Identical normalized JADX classes are a strong similarity signal, not permission to remove either package.",
"",
"## Packages and installed components",""]
for name,v in data["apps"].items():
    lines+=["- "+name+": "+str(v["package"])+"; Java classes "+str(v["class_count"])+"; components "+str(v["components"])]
lines+=["","## Exact class-path overlap","",
"- Common class paths: "+str(stats["common_paths"]),
"- Identical normalized Java classes: "+str(stats["bytecode_decompiled_class_same"]),
"- Modified normalized classes: "+str(stats["changed"]),
"- Unique to Settings: "+str(stats["only_settings"]),
"- Unique to Wizard: "+str(stats["only_wizard"]),
"- Shared-class identity rate: "+str(stats["identical_fraction_common"]),
"",
"### Classes with changed bodies"]
lines.extend("- "+x for x in stats["changed_paths"][:35])
lines+=["","### Classes unique to Setup Wizard"]
lines.extend("- "+x for x in stats["only_wizard_paths"][:30])
lines+=["","## Consequences","",
"- A setup APK may contain a copy of the settings code but still have unique provisioning manifest, package UID, signatures and receivers.",
"- Inspect actual setup intent and DEVICE_PROVISIONED/USER_SETUP_COMPLETE handling before treating either APK as redundant.",
"- No app was removed, executed or modified.",
""]
(out/"SETUP_VS_SETTINGS_RU.md").write_text("\n".join(lines)+"\n")
print("CLONE",stats,flush=True)
