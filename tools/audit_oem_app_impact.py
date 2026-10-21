#!/usr/bin/env python3
"""Offline OEM APK replacement-impact audit: manifest components, method SHA deltas,
JNI, and code-risk indicators. NO code is called and NO app is disabled."""
import argparse,collections,json,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser()
for n in ("ota","factory","erofs","out"):p.add_argument("--"+n,type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
new=json.loads(a.ota.read_text())["apps"]
old=json.loads(a.factory.read_text())["apps"]
RISK={
"zxlauncher":("candidate_replacement","HOME role, key routing, boot startup, callbacks, TV/source actions"),
"zxstore":("candidate_later_disable","APK install/update dependencies, intents, package events, download provider"),
"KuSettings":("UI_replacement_only_after_proof","OEM settings, privileged permissions and TRD control"),
"TvSettingsPlus":("privileged_core_until_adapter","Android-TV system settings, HDMI and I2C JNI"),
"trdmiddle":("keep_hardware_core","TRD Binder/HIDL ToF and projector middleware"),
"trdservice":("keep_hardware_core","motor, key and boot event service"),
"RuiAutoFocus":("keep_hardware_core","motor, ToF, camera and optical calibration"),
"KeystoneCorrection":("keep_hardware_core","projector trapezoid and display functions"),
"KuSourceRJ":("keep_until_adapter_tested","input source switching and HDMI boot selection"),
"Factory":("keep_for_recovery_diagnostics","factory test and native I2C"),
"RuiYunOta":("keep_until_rollback_ready","OEM OTA client and update permission chain"),
"KuSetupWizard":("keep_for_first_boot","first boot and provisioning"),
"TvServices":("keep_until_tv_regression_test","Android TV service lifecycle"),
"LiveTV":("keep_until_input_regression_test","TV input framework and HDMI handling"),
}
def manifest(apk):
    if not apk.is_file():return []
    p=subprocess.run(["aapt","dump","xmltree",str(apk),"AndroidManifest.xml"],
                     capture_output=True,text=True,errors="replace",timeout=60)
    if p.returncode:return []
    components=[];cur=None;level=0;action_level=-1
    for line in p.stdout.splitlines():
        m=re.match(r"^(\s*)E: ([\w.-]+)",line)
        if m:
            n=len(m.group(1));tag=m.group(2)
            if cur and n<=level:cur=None
            if tag in ("activity","activity-alias","receiver","service","provider"):
                cur={"type":tag,"name":"","exported":None,"permission":None,"actions":[]}
                components.append(cur);level=n;action_level=-1
            elif cur and tag=="action":action_level=n
            continue
        if not cur:continue
        k=re.match(r"^\s*A: android:(name|exported|permission|authorities)(?:\([^)]+\))?=(.*)",line)
        if not k:continue
        key,raw=k.groups()
        string=re.search(r'"([^"]*)"',raw)
        v=string.group(1) if string else raw[:130]
        if key=="name":
            if action_level>=0 and len(line)-len(line.lstrip())>action_level:cur["actions"].append(v[:140])
            elif not cur["name"]:cur["name"]=v[:160]
        elif key=="exported":
            cur["exported"]=bool("0xffffffff" in raw or "0x1" in raw or "true" in raw)
        else:cur[key]=v[:160]
    return components
def methods(x,y):
    xs=x.get("methods",{});ys=y.get("methods",{})
    counts=collections.Counter();changes=[]
    for cls in sorted(set(xs)|set(ys)):
        aa=xs.get(cls,{});bb=ys.get(cls,{})
        for sig in set(aa)|set(bb):
            if sig not in aa:status="stock_only"
            elif sig not in bb:status="ota_only"
            elif aa[sig]["digest"]==bb[sig]["digest"]:status="same"
            else:status="changed"
            counts[status]+=1
            if status!="same" and len(changes)<200 and re.search(r"(?i)(motor|focus|tof|hdmi|source|service|settings|key|projector|image|trapezoid|boot|bluetooth|audio|init)",cls+" "+sig):
                changes.append({"class":cls,"method":sig,"difference":status})
    return dict(counts),sorted(changes,key=lambda t:(t["class"],t["method"]))
rows={}
for name in sorted(set(new)|set(old)):
    x,y=new.get(name,{}),old.get(name,{})
    c,d=methods(x,y)
    manifest_entries=manifest(a.erofs/x["path"]) if x.get("path") else []
    exported=[e for e in manifest_entries if e["exported"]]
    classification,notes=RISK.get(name,("unclassified_keep_until_review","Additional analysis needed"))
    refs=x.get("referenced_oem_java_symbols",[])
    rows[name]={
      "ota_present":bool(x.get("sha256")) and not x.get("missing",False),"stock_present":bool(y.get("sha256")) and not y.get("missing",False),
      "apk_identical":x.get("sha256")==y.get("sha256") if x.get("sha256") and y.get("sha256") else None,
      "dex_identical":x.get("dex")==y.get("dex") if x.get("dex") and y.get("dex") else None,
      "method_deltas_are_decompiler_noise_if_dex_identical":bool(x.get("dex") and y.get("dex") and x.get("dex")==y.get("dex")),
      "package":x.get("package"),"apk_path":x.get("path"),
      "component_counts":dict(collections.Counter(e["type"] for e in manifest_entries)),
      "exported_components":exported[:150],
      "shared_user_id":x.get("manifest_extract",{}).get("sharedUserId"),
      "permission_count":len(x.get("permissions",[])),
      "critical_permissions":[p for p in x.get("permissions",[]) if re.search("WRITE_SECURE|INJECT_EVENTS|REBOOT|MANAGE_|BLUETOOTH_PRIVILEGED|TV_INPUT",p)],
      "jni":x.get("native_libraries",[]),"method_deltas":c,"hardware_related_deltas":d[:140],
      "static_risk_counts":x.get("risk_indicator_counts",{}),
      "static_risk_examples":x.get("risk_indicator_examples",[])[:100],
      "referenced_oem_symbols":refs[:100],
      "classification":classification,"required_review":notes}
    print("APP",name,"method_diff",c,"exported",len(exported),"classified",classification,flush=True)
result={"subject":"RUIOS Oct-8052 OTA vs Sep-8054 OEM app code and removal impact",
        "apps":rows,
        "caveats":["No app disabled and no Android setting changed.",
         "When APK and DEX hashes match, individual JADX method-hash differences are decompiler artifacts, NOT changes to original code.",
         "Package and permission parsing from aapt may be incomplete because upstream audit trims stdout; do not infer absence from an empty field.",
         "Static Java reference is not proof of Binder IPC or runtime dependency.",
         "Exported component presence is not proof it can be called without signature permissions.",
         "Risk indicators are candidates for manual defect review; zero confirmed bugs by this tool."]}
(a.out/"app_impact.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
md=["# OEM application deep audit — latest 8052 OTA vs factory 8054","",
"Verified factory stock-method hash artifact + latest OTA APK decompilation and AndroidManifest trees.",
"NO app removed, no signed APK recreated, no OEM code or private data redistributed.",
"",
"## Replacement and removal risk","",
"| App | Risk and plan | APK same? | JADX deltas* | Exported components |",
"|---|---|---|---:|---:|"]
for name,x in rows.items():
    md.append("| "+name+" | "+x["classification"]+" | "+str(x["apk_identical"])+" | "+
      str(x["method_deltas"].get("changed",0))+" | "+str(len(x["exported_components"]))+" |")
md+=["","* A nonzero JADX delta with identical DEX is a decompiler artifact, not a change of firmware code.","",
"## App-by-app evidence and required runtime validation",""]
for name,x in rows.items():
    md+=["### "+name,"",
       "- Recommendation: "+x["classification"]+"; inspect "+x["required_review"]+".",
       "- Package: "+str(x["package"])+"; privileges: "+str(x["critical_permissions"][:10])+".",
       "- Dynamic libraries: "+str(x["jni"])+".",
       "- Android components: "+str(x["component_counts"])+".",
       "- Method digest comparison: "+str(x["method_deltas"])+".",
       "- Code review indicators (not proven bugs): "+str(x["static_risk_counts"])+".",""]
    if x["exported_components"]:
        md+=["Selected exported components (not confirmed accessible):",""]
        for e in x["exported_components"][:16]:
            md.append("- "+e["type"]+" "+str(e.get("name"))+
               (", permission="+str(e.get("permission")) if e.get("permission") else "")+
               (", actions="+", ".join(e.get("actions",[])[:5]) if e.get("actions") else ""))
        md.append("")
    if x["hardware_related_deltas"]:
        md+=["Relevant modified method signatures:"]
        for e in x["hardware_related_deltas"][:20]:md.append("- "+e["difference"]+": "+e["class"]+" :: "+e["method"])
        md.append("")
md+=["## Critical uninstall/replacement test gates","",
"- Replace the stock launcher only after HOME selection, reboot, remote inputs, suspend/resume and HDMI return are tested.",
"- Do not remove proprietary TRD/ToF/motor/keystone/TV input services until a tested replacement exists.",
"- OEM store is only a candidate for disable; verify any installed-package callback, provider authority and firmware-linked download activity.",
"- Replace settings UI behind a verified adapter that preserves Binder, system permissions and essential JNI paths.",
"- Keep OEM OTA service and wizard until update/recovery and first-boot behavior are tested.",
"- Do not report code-heuristic indicators as confirmed defects without manual control-flow review and reproduced behavior.",
"- Watch both 8052 and 8054 test results; the same Java APK can act differently due to native HAL and build.prop.",
""]
(a.out/"app_impact.md").write_text("\n".join(md)+"\n")
print("APP AUDIT complete",len(rows),"packages, reports in",a.out,flush=True)
