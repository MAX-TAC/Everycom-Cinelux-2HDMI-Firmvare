#!/usr/bin/env python3
"""Compare OEM launcher/store/setup Java method bodies: latest 8052 OTA vs original stock 8054.
Read-only JADX hashes, no original source distributed. Code differences are not automatically defects.
"""
import collections,hashlib,json,re,subprocess,shutil,zipfile
from pathlib import Path
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

a=json.loads(Path("/tmp/deep-8054/deep-apks.json").read_text())["apps"]
targets={
    "zxlauncher":"system/system/app/zxlauncher/zxlauncher.apk",
    "zxstore":"system/system/app/zxstore/zxstore.apk",
    "KuSetupWizard":"system/system/app/KuSetupWizard/KuSetupWizard.apk",
}
owned={
"zxlauncher":("com/zeasn/launcher/","com/zeasn/utils/"),
"zxstore":("zeasn/open/technical/tv/store/","com/zeasn/utils/"),
"KuSetupWizard":("com/android/provision/","com/my/settings/")
}
out=Path("analysis/Deep_Stock_Audit_20261021")
out.mkdir(parents=True,exist_ok=True)
overall={"sources":["8052 OTA 2026-10-12","8054 factory 2026-09-30"],"apps":{}}
for name,rel in targets.items():
    apk=Path("/tmp/erofs")/rel
    assert apk.is_file(),str(apk)
    old=a[name]
    assert old.get("methods"),name+" stock method hashes not available"
    work=Path("/tmp/jadx-compare-"+name)
    p=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3",
       "-d",str(work),str(apk)],capture_output=True,text=True,errors="replace",timeout=750)
    root=work/"sources"
    assert root.exists(),"JADX failed for "+name+" "+p.stderr[-250:]
    latest={}
    for f in root.rglob("*.java"):
        path=f.relative_to(root).as_posix()
        latest[path]=signatures(f.read_text(errors="replace"))
    shutil.rmtree(work,ignore_errors=True)
    stats=collections.Counter()
    changes=[]
    for cls in sorted(set(old["methods"])|set(latest)):
        oldmethods=old["methods"].get(cls,{})
        newmethods=latest.get(cls,{})
        for signature in sorted(set(oldmethods)|set(newmethods)):
            if signature not in oldmethods:status="only_new_8052"
            elif signature not in newmethods:status="only_old_8054"
            elif oldmethods[signature]["digest"]==newmethods[signature]["digest"]:status="same"
            else:status="changed_body"
            stats[status]+=1
            if status!="same":
                changes.append({"class":cls,"method":signature,"status":status})
    ours=[x for x in changes if x["class"].startswith(owned[name])]
    interested=re.compile(r"(?i)(install|package|launch|home|boot|ota|service|setting|permission|broadcast|auth|network|updat|focus|hdmi)")
    risk=[x for x in ours if interested.search(x["class"]+" "+x["method"])]
    newhash=hashlib.sha256(apk.read_bytes()).hexdigest()
    overall["apps"][name]={"apk_sha_8052":newhash,"apk_sha_8054":old.get("sha256"),
                            "identical_apk":newhash==old.get("sha256"),
                            "counts":dict(stats),"own_changed":len(ours),"risk_named_own_changed":len(risk),
                            "own_changes":ours[:400],"risk_own_changes":risk[:180],
                            "other_changes_sample":[x for x in changes if x not in ours][:75],
                            "jadx_exit":p.returncode}
    print("APP",name,"same APK",overall["apps"][name]["identical_apk"],
          "changed methods",dict(stats),"own",len(ours),"risk",len(risk),flush=True)
(out/"latest_8052_vs_8054_launcher_store_setup_methods.json").write_text(json.dumps(overall,indent=2,ensure_ascii=False)+"\n")
md=["# Latest OTA 8052 vs stock 8054: launcher, store and setup wizard method changes",
"",
"Original sources verified by SHA256. Decompiled Java normalized with the same hashing rules for both sides.",
"Changed method digest is a code fingerprint, not a confirmed bug nor proof that this method is used on the device.",
"",
"## Summary","",
"| APK | Exact APK SHA match | Same methods | Changed body | Added/removed | Own methods changed |",
"|---|---|---:|---:|---:|---:|"]
for name,row in overall["apps"].items():
    counts=row["counts"]
    md.append("| "+name+" | "+str(row["identical_apk"])+
       " | "+str(counts.get("same",0))+" | "+str(counts.get("changed_body",0))+
       " | "+str(counts.get("only_new_8052",0)+counts.get("only_old_8054",0))+
       " | "+str(row["own_changed"])+" |")
for name,row in overall["apps"].items():
    md+=["","## "+name,"",
        "- APK byte-identical: "+str(row["identical_apk"]),
        "- OEM-owned changed methods: "+str(row["own_changed"]),
        "- Changes matched to important feature keywords: "+str(row["risk_named_own_changed"]),
        "","### Candidate changed OEM methods"]
    for c in row["risk_own_changes"][:65]:
        md.append("- "+c["status"]+" — "+c["class"]+" :: "+c["method"])
    if not row["risk_own_changes"]:md.append("- No changed OEM method matched filter. Check full JSON.")
md+=["","## Interpretation","",
"- Most changes in support-library code may be build or decompiler noise; concentrate on app-owned method changes.",
"- Distinguish executable behavior from manifest/resources, because dex hashes alone cannot capture exported components.",
"- Before removing launcher/store, test shared install broadcasts, package install flow, HOME fallback and system settings writes.",
"- Setup wizard package can duplicate settings Java code but still have distinct provisioning manifest and lifecycle.",
"- No APKs were modified or installed.",
""]
(out/"LAUNCHER_STORE_SETUP_METHODS_RU.md").write_text("\n".join(md)+"\n")
print("DONE",list(overall["apps"]),flush=True)
