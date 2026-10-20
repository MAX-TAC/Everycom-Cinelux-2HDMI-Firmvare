#!/usr/bin/env python3
"""Read-only OEM Android projector interface investigation (metadata only, no proprietary source).
Input: reconstructed and extracted genuine 8054 stock EROFS at /tmp/erofs.
"""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument("--root",type=Path,required=True)
ap.add_argument("--out",type=Path,required=True)
ap.add_argument("--variant",default="8054-stock")
args=ap.parse_args()
args.out.mkdir(parents=True,exist_ok=True)

APPS={
"TvSettingsPlus":"system_ext_a/priv-app/TvSettingsPlus/TvSettingsPlus.apk",
"Factory":"system_ext_a/app/Factory/Factory.apk",
"RuiAutoFocus":"system_a/system/app/RuiAutoFocus/RuiAutoFocus.apk",
"KeystoneCorrection":"system_a/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk",
"KuSourceRJ":"system_a/system/app/KuSourceRJ/KuSourceRJ.apk",
"trdmiddle":"vendor_a/priv-app/trdmiddle/trdmiddle.apk",
"trdservice":"system_a/system/app/trdservice/trdservice.apk",
"KuSettings":"system_a/system/app/KuSettings/KuSettings.apk",
}
FOCUS=re.compile(r"(?i)(projector|trapezoid|keystone|focus|motor|tof|hdmi|inputsource|source|i2c|cameraapi|trdsystem|ITrd|IProjector|ITof|mirrormode|i2cdevice|brightness|picturemode|gamma|bluetooth|audiodevice|audiooutput)")
CALLS=re.compile(r"\b(?:i2c|setProjectorMirrorMode|setFocus|autoFocus|MotorFront(?:Step|TofStep)?|MotorBack(?:Step|TofStep)?|MotorStop|startTof|stopTof|getMotorCtrl|getTofCtrl|setBootSource|resetTrapezoid|writeParcelToFlinger|switchSource|setInputSource|setTofAutofocus|getProjectorCtrl)\s*\(")
SENSITIVE=re.compile(r"(?i)(password|secret|passwords|serialnumber|macaddress|widevine|hdcp|privatekey|access_token|apikey)")
METHOD=re.compile(r"(?m)^[ \t]*(?:(?:public|protected|private|static|final|synchronized|native|abstract|transient|strictfp)\s+){0,7}[\w$<>, ?.\[\]]{2,160}\s+([a-zA-Z_$][\w$]*)\s*\([^;{}]{0,260}\)\s*(?:throws\s+[\w., ]+)?(?:;|\{)")
reports={}
results={"variant":args.variant,"apps":{},"native":{},"bluetooth_audio":{},"note":"Static method signatures/call references only; decompiled OEM source is not redistributed."}
for name,relative in APPS.items():
    apk=args.root/relative
    if not apk.is_file():
        results["apps"][name]={"missing":True,"path":relative}
        print("MISSING",name,relative,flush=True)
        continue
    row={"path":relative,"size":apk.stat().st_size,"sha256":hashlib.sha256(apk.read_bytes()).hexdigest(),
         "package":None,"version":None,"permissions":[],"jni_loads":[],"selected_classes":[],
         "declarations":[],"call_sites":[],"related_actions":[],"errors":[]}
    pp=subprocess.run(["aapt","dump","badging",str(apk)],capture_output=True,text=True,timeout=45,errors="replace")
    match=re.search(r"package: name='([^']+)' versionCode='([^']*)' versionName='([^']*)'",pp.stdout)
    if match:row["package"],row["version_code"],row["version"]=match.groups()
    row["permissions"]=sorted(set(re.findall(r"uses-permission: name='([^']+)'",pp.stdout)))
    dest=args.out/("jadx-temp-"+name)
    cmd=["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3","-d",str(dest),str(apk)]
    p=subprocess.run(cmd,capture_output=True,text=True,timeout=650,errors="replace")
    row["jadx_exit_code"]=p.returncode
    if p.returncode:row["errors"].append(p.stderr[-250:])
    sources=dest/"sources"
    code_files=list(sources.rglob("*.java")) if sources.exists() else []
    row["decompiled_class_count"]=len(code_files)
    decls=[];references=[];loads=set();actions=set()
    for source in code_files:
        rel=source.relative_to(sources).as_posix()
        contents=source.read_text(encoding="utf-8",errors="replace")
        if (not FOCUS.search(rel)) and (not (CALLS.search(contents) or "loadLibrary" in contents)):
            continue
        for lib in re.findall(r'(?:System\.)?loadLibrary\s*\(\s*"([^"]{2,90})"',contents):
            loads.add(lib)
        relevant=bool(FOCUS.search(rel))
        if relevant:
            if len(row["selected_classes"])<130:row["selected_classes"].append(rel)
            for m in METHOD.finditer(contents):
                signature=" ".join(m.group(0).split()).rstrip("{; ")
                if (FOCUS.search(signature) or " native " in " "+signature+" " or "i2c" in rel.lower()):
                    if not SENSITIVE.search(signature) and len(decls)<650:
                        decls.append({"class":rel,"signature":signature[:350],
                                      "jni":bool(re.search(r"\bnative\b",signature))})
        # Record only identifiers and location metadata, not proprietary statements.
        lines=contents.splitlines()
        for k,line in enumerate(lines,1):
            names=sorted(set(m.group().split("(")[0].strip() for m in CALLS.finditer(line)))
            if names and not SENSITIVE.search(line) and len(references)<280:
                references.append({"class":rel,"line":k,"calls":names})
        if relevant:
            for action in re.findall(r'(?:new Intent\s*\(|setAction\s*\()\s*"([^"]{4,120})"',contents):
                if not SENSITIVE.search(action):actions.add(action)
    # safe cleanup of intermediate proprietary Java sources
    import shutil
    shutil.rmtree(dest,ignore_errors=True)
    row["selected_classes"].sort()
    row["declarations"]=sorted(decls,key=lambda e:(e["class"],e["signature"]))
    row["call_sites"]=references
    row["related_actions"]=sorted(actions)[:70]
    row["jni_loads"]=sorted(loads)
    results["apps"][name]=row
    print("APP",name,"classes",len(code_files),"decl",len(decls),"calls",len(references),"jni",sorted(loads),flush=True)

native_names={"libsettingsi2c_jni.so","libfactoryi2c_jni.so","libi2c_jni.so",
              "libtof_jni.so","libtrd_jni.so","librjpj_private_function.so",
              "libruicameraapi_jni.so","libfocusvahysd.so","libtrdmiddle.so"}
for root in args.root.iterdir():
    if not root.is_dir():continue
    for path in root.rglob("*.so"):
        if path.name not in native_names:continue
        rel=path.relative_to(args.root).as_posix()
        try:
            symbols=subprocess.run(["readelf","-Ws",str(path)],capture_output=True,text=True,timeout=30)
            sym=[l.split()[-1] for l in symbols.stdout.splitlines() if l.strip() and
                 (("Java_" in l or FOCUS.search(l.split()[-1])) and not SENSITIVE.search(l))]
            needed=subprocess.run(["readelf","-d",str(path)],capture_output=True,text=True,timeout=30)
            deps=sorted(set(re.findall(r"Shared library: \[([^\]]+)\]",needed.stdout)))
            results["native"][rel]={"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                                      "candidate_export_symbols":sorted(set(sym))[:130],"deps":deps}
        except Exception as e:results["native"][rel]={"error":str(e)[:200]}
    print("NATIVE SCAN",root.name,flush=True)
for subdir in ("vendor_a/etc","system_a/system/etc"):
    directory=args.root/subdir
    if not directory.exists():continue
    for p in directory.rglob("*audio*policy*.xml"):
        if not p.is_file() or p.stat().st_size>120000:continue
        content=p.read_text(errors="replace")
        selected=[line.strip()[:200] for line in content.splitlines()
                  if re.search(r"(?i)(a2dp|bluetooth|le.audio|sco|mixPort|devicePort|route)",line)]
        results["bluetooth_audio"][p.relative_to(args.root).as_posix()]={"hits":selected[:65],
                        "a2dp_mentions":len(re.findall("a2dp",content,re.I)),
                        "le_audio_mentions":len(re.findall("le_audio|le audio",content,re.I))}
report=args.out/(args.variant+".json")
report.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
print("SUCCESS",report,report.stat().st_size,flush=True)
