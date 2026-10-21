#!/usr/bin/env python3
"""Compare latest 8052 OEM autofocus method digests to verified factory 8054 JADX digests.
Do not publish reconstructed OEM Java. This is only heuristic static code evidence.
"""
import collections,hashlib,json,re,subprocess
from pathlib import Path

app=Path("/tmp/erofs/system/system/app/RuiAutoFocus/RuiAutoFocus.apk")
factory=Path("/tmp/deep-8054/deep-apks.json")
assert app.is_file() and factory.is_file(),(app,factory)
old=json.loads(factory.read_text())["apps"]["RuiAutoFocus"]
assert old.get("methods"),"Stock 8054 method hashes missing"
work=Path("/tmp/jadx-focus")
p=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3",
                 "-d",str(work),str(app)],capture_output=True,text=True,errors="replace",timeout=620)
assert (work/"sources").is_dir(),"JADX produced no sources; "+p.stderr[-600:]
def norm(s):
    s=re.sub(r"(?s)/\*.*?\*/","",s)
    s=re.sub(r"(?m)^\s*//.*$","",s)
    return re.sub(r"\s+"," ",s).strip()
def signatures(s):
    found={}
    rx=re.compile(r"(?m)^[ \t]*(?:@Override[ \t]+)?(?:(?:public|private|protected|static|final|synchronized|native|abstract|volatile)\s+){0,6}[A-Za-z_$\w<>\[\].?, ]+\s+([A-Za-z_$][\w$]*)\s*\([^;{}]*?\)\s*(?:throws\s+[\w., ]+)?\{")
    for match in rx.finditer(s):
        head=s[match.start():match.end()].strip()
        name=match.group(1)
        if name in ("if","while","for","switch","catch","synchronized"):continue
        depth=1;i=match.end()
        while i<len(s) and depth:
            if s[i]=="{":depth+=1
            elif s[i]=="}":depth-=1
            i+=1
        if depth:continue
        canonical=norm(s[match.start():i])
        sig=re.sub(r"\s+"," ",head)
        key=name+"("+re.sub(r"^(.*?)\(","",sig).split(")",1)[0][:150]+")"
        found[key]={"digest":hashlib.sha256(canonical.encode()).hexdigest(),"tokens":len(canonical.split()),"name":name}
    return found
latest={}
for path in (work/"sources").rglob("*.java"):
    r=path.relative_to(work/"sources").as_posix()
    latest[r]=signatures(path.read_text(errors="replace"))
stats=collections.Counter()
changes=[]
for classname in sorted(set(old["methods"])|set(latest)):
    x=old["methods"].get(classname,{})
    y=latest.get(classname,{})
    for sig in sorted(set(x)|set(y)):
        if sig not in x:status="added_in_8052_ota"
        elif sig not in y:status="only_8054_factory"
        elif x[sig]["digest"]==y[sig]["digest"]:status="same"
        else:status="changed"
        stats[status]+=1
        if status!="same":
            changes.append({"class":classname,"method":sig,"status":status})
important=re.compile(r"(?i)(motor|focus|camera|tof|keystone|angle|sensor|step|zoom|trapezoid|hysd)")
priority=[x for x in changes if important.search(x["class"]+" "+x["method"])]
result={"source_8052":"RUIOS.8052.1.0.4 OTA",
        "source_8054":"RUIOS.8054.1.0.1 stock, verified deep-app artifact run 39421706994",
        "jadx_exit_code":p.returncode,
        "counts":dict(stats),
        "modified_or_added_sample":changes[:250],
        "hardware_relevant_sample":priority[:150],
        "note":"Digests derived from JADX output; changes may include compiler/decompiler artifacts. No source is published."}
out=Path("analysis/Latest_8052_OTA_vs_8054_Stock")
out.mkdir(exist_ok=True,parents=True)
(out/"autofocus_method_diff.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
lines=["# Autofocus API differences: October 8052 OTA versus September 8054 stock","",
"Read-only comparison of normalized JADX 1.5.6 method digests; proprietary Java code not published.",
"Identical method digests indicate identical normalized decompiled bodies; differences need semantic validation.",
"",
"## Method comparison",""]
for k,v in stats.items():lines.append("- "+k+": "+str(v))
lines+=["","## Hardware-related changed methods",""]
for x in priority[:85]:lines.append("- "+x["status"]+" — "+x["class"]+" :: "+x["method"])
if not priority:lines.append("- No hardware-named method changes detected by this normalization; inspect all changes in JSON.")
lines+=["","## Limitations","",
"- These are implementation-level indications, not evidence of different physical motor drivers.",
"- Method hashes can differ with compiler optimization, library packaging and decompiler changes.",
"- Never call unknown motor/ToF methods on real hardware without limits and stop/recovery controls.",
""]
(out/"autofocus_method_diff.md").write_text("\n".join(lines)+"\n")
print("FOCUS COMPARISON",dict(stats),"hardware relevant",len(priority),flush=True)
print("\n".join(lines[:55]),flush=True)
