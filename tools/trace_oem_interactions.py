#!/usr/bin/env python3
"""Trace candidate cross-app Intent/Binder interactions in original RUIOS OTA.
Only classify explicit identifiers found in OEM-owned Java classes and manifests;
do not publish decompiled Java source or claim these as runtime-verified edges.
"""
import collections,json,re,subprocess,shutil
from pathlib import Path

src=Path("analysis/Deep_Stock_Audit_20261021/latest_8052_app_graph.json")
previous=json.loads(src.read_text())["apps"]
paths={
"zxlauncher":"system/system/app/zxlauncher/zxlauncher.apk",
"zxstore":"system/system/app/zxstore/zxstore.apk",
"KuSettings":"system/system/app/KuSettings/KuSettings.apk",
"TvSettingsPlus":"system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk",
"RuiYunOta":"system/system/priv-app/RuiYunOta/RuiYunOta.apk",
"KuSourceRJ":"system/system/app/KuSourceRJ/KuSourceRJ.apk",
"RuiAutoFocus":"system/system/app/RuiAutoFocus/RuiAutoFocus.apk",
"trdservice":"system/system/app/trdservice/trdservice.apk",
"trdmiddle":"vendor/priv-app/trdmiddle/trdmiddle.apk",
"KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk"
}
own_prefix={
"zxlauncher":("com/zeasn/launcher/","com/zeasn/utils/"),
"zxstore":("zeasn/open/technical/tv/store/","com/zeasn/utils/"),
"KuSettings":("com/my/",),
"TvSettingsPlus":("com/android/tv/settings/",),
"RuiYunOta":("com/rjpj/yunota/",),
"KuSourceRJ":("com/coolux/source/",),
"RuiAutoFocus":("com/hysd/","com/rui/cameraapi/"),
"trdservice":("com/trd/service/",),
"trdmiddle":("com/trd/framework/",),
"KuSetupWizard":("com/android/provision/","com/my/")
}
pkgs={name:v.get("package") for name,v in previous.items() if v.get("package") and name in paths}
# Literal targets only; these require tracing actual control flow before naming a proven dependency.
targets={v:n for n,v in pkgs.items()}
targetstrings=list(targets)+[
"com.rjpj.yunota.OTACheckService",
"com.rjpj.yunota.OTASystemNetworkUpdateActivity",
"com.zeasn.launcher.INSTALL_SUCCESS",
"com.trd.projector.settings.MainSettingsActivity",
"com.trd.factory.SplashActivity",
"android.settings.SETTINGS"]
verbs=re.compile(r"\b(startActivity|startService|startForegroundService|bindService|sendBroadcast|sendOrderedBroadcast|setClassName|setComponent|setPackage|setAction|new ComponentName|new Intent)\s*\(",re.I)
source_root=Path("/tmp/erofs")
records={"packages":pkgs,"components":{},"candidate_edges":[],"notes":[]}
for name,rel in paths.items():
    apk=source_root/rel
    if not apk.exists():continue
    m=subprocess.run(["aapt","dump","xmltree",str(apk),"AndroidManifest.xml"],
                     capture_output=True,text=True,errors="replace",timeout=60)
    nodes=[];cur=None;depth=0
    for line in m.stdout.splitlines():
        event=re.match(r"^(\s*)E: (activity|activity-alias|service|receiver|provider|intent-filter)\b",line)
        if event:
            level=len(event.group(1));what=event.group(2)
            if what in ("activity","activity-alias","service","receiver","provider"):
                cur={"kind":what,"name":None,"exported":None,"actions":[],"permissions":[]}
                nodes.append(cur);depth=level
            continue
        if cur is None:continue
        attr=re.match(r"^(\s*)A: android:(name|exported|permission)\b.*",line)
        if not attr:continue
        level=len(attr.group(1))
        value=re.search(r'="([^"]+)"',line)
        if attr.group(2)=="name" and level==depth+2 and value:cur["name"]=value.group(1)
        elif attr.group(2)=="exported" and level==depth+2:
            cur["exported"]="0xffffffff" in line or "0x1" in line or "true" in line.lower()
        elif attr.group(2)=="permission" and level==depth+2 and value:cur["permissions"].append(value.group(1))
        elif attr.group(2)=="name" and value and "action" in line.lower():cur["actions"].append(value.group(1))
    records["components"][name]=nodes
    dst=Path("/tmp/trace-oem-"+name)
    r=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3",
                      "-d",str(dst),str(apk)],capture_output=True,text=True,errors="replace",timeout=650)
    root=dst/"sources"
    if not root.exists():
        records["notes"].append(name+": no decompiled Java sources")
        continue
    edges=[]
    for f in root.rglob("*.java"):
        relpath=f.relative_to(root).as_posix()
        if not relpath.startswith(own_prefix[name]):continue
        lines=f.read_text(errors="replace").splitlines()
        for i,line in enumerate(lines):
            # Exclude URLs / obvious auth material and only preserve named references.
            if not any(t in line for t in targetstrings):continue
            if len(line)>1200:continue
            hits=[t for t in targetstrings if t in line]
            if not hits:continue
            lo=max(0,i-12);hi=min(len(lines),i+18)
            kinds=sorted(set(m.group(1) for fragment in lines[lo:hi] for m in verbs.finditer(fragment)))
            if not kinds: continue
            for dest in hits[:5]:
                edge={"from":name,"target_literal":dest,"target_known_package":targets.get(dest),
                      "class":relpath,"line":i+1,"nearby_dispatch_operations":kinds,
                      "evidence":"string literal and dispatch API occur within a bounded source window, not proven invocation"}
                edges.append(edge)
    # Cap repeated references due copied libraries or shared classes.
    seen=set()
    for edge in edges:
        key=(edge["target_literal"],edge["class"],tuple(edge["nearby_dispatch_operations"]))
        if key in seen:continue
        seen.add(key)
        if len(records["candidate_edges"])<950:records["candidate_edges"].append(edge)
    shutil.rmtree(dst,ignore_errors=True)
    print("TRACED",name,"candidates",len(edges),"components",len(nodes),flush=True)
out=Path("analysis/Deep_Stock_Audit_20261021")
(out/"oem_intent_call_chains.json").write_text(json.dumps(records,ensure_ascii=False,indent=2)+"\n")
tick=chr(96)
lines=["# OEM Intent/receiver/service call-site candidates — RUIOS 8052.1.0.4","",
"Static AndroidManifest and JADX source-code reference scan. This is not live execution proof.",
"A target literal and dispatch function in the same source window is a candidate edge, not a proven dependency.",
"",
"## Exported and internal component inventory","",
"| APK | Components | Exported=true | Exported=false | Unresolved flags |",
"|---|---:|---:|---:|---:|"]
for name,nodes in records["components"].items():
    c=collections.Counter(x["exported"] for x in nodes)
    lines.append("| "+name+" | "+str(len(nodes))+" | "+str(c[True])+" | "+str(c[False])+" | "+str(c[None])+" |")
lines+=["","## OEM cross-app call candidates",""]
group=collections.defaultdict(list)
for e in records["candidate_edges"]:
    if e["target_known_package"] and e["target_known_package"]==e["from"]:continue
    group[(e["from"],e["target_literal"])].append(e)
for (source,target),items in sorted(group.items()):
    lines+=["","### "+source+" → "+target,""]
    for x in items[:12]:
        lines.append("- "+tick+x["class"]+":"+str(x["line"])+tick+" — "+", ".join(x["nearby_dispatch_operations"]))
lines+=["","## Runtime validation requirements","",
"- Verify exported flags and actual package manager visibility on both real hardware profiles.",
"- For each candidate, inspect exact data flow from intent creation to dispatch and receiver/action handler.",
"- Confirm shared UID / signature permissions, service availability and boot-time ordering.",
"- If disabling app later, test OTA, Home, remote key events, HDMI, focus, keystone and provisioning with rollback.",
"- A class reference to an OEM package may be dead code or a copied SDK. Do not treat it as a confirmed dependency.",
""]
(out/"OEM_INTENT_CALL_CHAINS_RU.md").write_text("\n".join(lines)+"\n")
print("DONE OEM candidates",len(records["candidate_edges"]),flush=True)
