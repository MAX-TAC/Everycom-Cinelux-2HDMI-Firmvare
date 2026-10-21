#!/usr/bin/env python3
"""Correct exported flags in existing OEM manifest report using exact binary Boolean values."""
import collections,json,re,subprocess
from pathlib import Path
root=Path("/tmp/erofs")
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
"KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk"}
out=Path("analysis/Deep_Stock_Audit_20261021")
info=json.loads((out/"oem_intent_call_chains.json").read_text())
counts={};review=[]
for name,rel in paths.items():
    apk=root/rel
    assert apk.is_file(),str(apk)
    p=subprocess.run(["aapt","dump","xmltree",str(apk),"AndroidManifest.xml"],
                     capture_output=True,text=True,errors="replace",timeout=65)
    assert p.returncode==0,(name,p.stderr[-200:])
    nodes=[];depth=None
    for line in p.stdout.splitlines():
        event=re.match(r"^(\s*)E: (activity|activity-alias|service|receiver|provider)\b",line)
        if event:
            depth=len(event.group(1))
            nodes.append({"kind":event.group(2),"name":None,"exported":None,"permissions":[]})
            continue
        if depth is None:continue
        a=re.match(r"^(\s*)A: android:(name|exported|permission)\b",line)
        if not a or len(a.group(1))!=depth+2:continue
        value=re.search(r'="([^"]*)"',line)
        if a.group(2)=="name" and value:nodes[-1]["name"]=value.group(1)
        elif a.group(2)=="permission" and value:nodes[-1]["permissions"].append(value.group(1))
        elif a.group(2)=="exported":
            v=re.search(r"\(type 0x12\)0x([0-9a-fA-F]+)",line)
            if v:nodes[-1]["exported"]=int(v.group(1),16)!=0
            elif value and value.group(1).lower() in ("true","false"):
                nodes[-1]["exported"]=value.group(1).lower()=="true"
    originals=info["components"].get(name,[])
    refs={(x["kind"],x["name"]):x for x in nodes if x["name"]}
    for obj in originals:
        row=refs.get((obj["kind"],obj["name"]))
        if row:
            obj["exported"]=row["exported"]
            obj["permissions"]=row["permissions"]
    c=collections.Counter(x["exported"] for x in nodes)
    counts[name]={"total":len(nodes),"true":c[True],"false":c[False],"absent":c[None]}
    for x in nodes:
        if x["exported"] is True and not x["permissions"] and x["kind"] in ("service","receiver","provider"):
            review.append({"app":name,"kind":x["kind"],"name":x["name"],
                           "status":"Requires caller permission and runtime behavior audit; not a vulnerability finding"})
    print("MANIFEST",name,counts[name],flush=True)
info["corrected_manifest_bool_parser"]=True
info["manifest_review_candidates"]=review
(out/"oem_intent_call_chains.json").write_text(json.dumps(info,ensure_ascii=False,indent=2)+"\n")
lines=["# Corrected AndroidManifest component exported flags","",
"Source: verified RUIOS 8052 OTA. A previous static parser mistook the Boolean TYPE marker for the value true. This report reads the value AFTER the marker.",
"",
"| App | Components | Explicit exported=true | Explicit exported=false | Not specified |",
"|---|---:|---:|---:|---:|"]
for name,v in counts.items():
    lines.append("| "+name+" | "+str(v["total"])+" | "+str(v["true"])+" | "+str(v["false"])+" | "+str(v["absent"])+" |")
lines+=["","## Review candidates (not confirmed security defects)","",
"Listed services/providers/receivers are explicitly exported without a direct per-component permission. App-level checks, inherited privileges, SELinux and runtime restrictions may still apply.",""]
for x in review[:75]:
    lines.append("- "+x["app"]+": "+x["kind"]+" "+str(x["name"]))
lines+=["","## Interpretation","",
"- Unspecified exported flag does not mean false; Android defaults depend on component kind and intent filters.",
"- A listed candidate does not establish untrusted-app reachability or privilege escalation.",
"- Do not send test intents to safety-sensitive functions on another person's projector.",
""]
(out/"MANIFEST_EXPORTED_VERIFIED_RU.md").write_text("\n".join(lines)+"\n")
original=(out/"OEM_INTENT_CALL_CHAINS_RU.md").read_text()
assert "## OEM cross-app call candidates" in original
pref=original.split("## Exported and internal component inventory",1)[0]
tail=original.split("## OEM cross-app call candidates",1)[1]
summary=pref+"## Exported and internal component inventory (corrected)\n\n"
summary+="| App | Components | True | False | Unspecified |\n|---|---:|---:|---:|---:|\n"
for name,v in counts.items():
    summary+="| "+name+" | "+str(v["total"])+" | "+str(v["true"])+" | "+str(v["false"])+" | "+str(v["absent"])+" |\n"
summary+="\nSee corrected verification: [MANIFEST_EXPORTED_VERIFIED_RU.md](MANIFEST_EXPORTED_VERIFIED_RU.md).\n\n"
summary+="## OEM cross-app call candidates"+tail
(out/"OEM_INTENT_CALL_CHAINS_RU.md").write_text(summary)
print("DONE",len(review),"review candidates; these are not confirmed vulnerabilities",flush=True)
