#!/usr/bin/env python3
"""Read-only triage of extracted projector firmware contents. No payloads published."""
from pathlib import Path
import argparse,collections,datetime,hashlib,json,re,shutil,subprocess

a=argparse.ArgumentParser()
a.add_argument("--root",required=True)
a.add_argument("--archive",required=True)
a.add_argument("--output",default="analysis/Original_Firmware")
v=a.parse_args()
root,out,archive=Path(v.root),Path(v.output),Path(v.archive)
out.mkdir(parents=True,exist_ok=True)
MAGICS={"MStar-firmware":b"# MSTAR FIRMWARE","android-boot":b"ANDROID!","android-sparse":b"\x3a\xff\x26\xed","erofs":b"\xe2\xe1\xf5\xe0","squashfs":b"hsqs","ubi":b"UBI#","avb":b"AVB0","android-payload":b"CrAU","zip":b"PK\x03\x04","fdt":b"\xd0\x0d\xfe\xed","elf":b"\x7fELF"}
PROPS=re.compile(rb"(?:ro\.(?:build|product|vendor|board|boot|hardware|treble|vndk|soc|mediatek|mstar|mtk)[\w.\-]{0,75}|androidboot\.[\w.\-]{1,65})[= ][ -~]{0,160}")
SENSITIVE=re.compile(rb"(serial|password|passwd|secret|token|mac|imei|widevine|private|attestation|api.?key)",re.I)
def hm(n):return f"{n/1048576:.1f} MiB"
def digest(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(8*1024*1024),b""):h.update(b)
    return h.hexdigest()
def run(cmd,timeout=120):
    try:
        p=subprocess.run(cmd,capture_output=True,text=True,errors="replace",timeout=timeout)
        return p.returncode,p.stdout[:120000],p.stderr[-3000:]
    except Exception as e:return -1,"",str(e)
def scan(path):
    start=path.open("rb").read(1024)
    mags=collections.defaultdict(list)
    props=set()
    with path.open("rb") as f:
        prev=b""
        offset=0
        while 1:
            chunk=f.read(16*1024*1024)
            if not chunk:break
            data=prev+chunk
            base=offset-len(prev)
            for key,magic in MAGICS.items():
                pos=0
                while len(mags[key])<20:
                    pos=data.find(magic,pos)
                    if pos<0:break
                    n=base+pos
                    if n>=0 and n not in mags[key]:mags[key].append(n)
                    pos+=1
            if len(props)<90:
                for m in PROPS.finditer(data):
                    b=m.group(0)
                    if not SENSITIVE.search(b):
                        text=b.decode("latin1").split("\x00")[0].strip()
                        if 8<len(text)<220:props.add(text)
                        if len(props)>100:break
            offset+=len(chunk)
            prev=data[-256:]
    return start,{k:v for k,v in mags.items() if v},sorted(props)
files=sorted((p for p in root.rglob("*") if p.is_file() and not p.is_symlink()),key=lambda p:-p.stat().st_size)
result={"archive":{"name":archive.name,"size":archive.stat().st_size,"sha256":digest(archive)},"files":[]}
lines=["# Everycom CineLux 2-HDMI firmware: read-only inspection","",
       "Static observations only. NOT tested on D11 Master. Do NOT flash across board revisions.","",
       "Archive: "+archive.name+"; "+hm(archive.stat().st_size)+"; sha256="+result["archive"]["sha256"],
       "Extracted file count: "+str(len(files)),"","## Archive members"]
for i,p in enumerate(files):
    rel=str(p.relative_to(root))
    size=p.stat().st_size
    rc,ft,_=run(["file","-b",str(p)],20)
    item={"path":rel,"size":size,"file_type":ft.strip()[:200],"sha256":digest(p)}
    lines+=["",f"### {rel}","Size: "+hm(size),"Detected type: "+item["file_type"],"SHA256: "+item["sha256"]]
    if size>4096 and i<35:
        head,matches,props=scan(p)
        item["header_text"]="".join(chr(c) if 32<=c<127 else "." for c in head[:450])
        item["header_hex"]=head[:120].hex(" ")
        item["magic_offsets"]=matches
        item["public_props"]=props
        lines += ["Header preview: "+item["header_text"],"Magic signatures: "+json.dumps(matches)]
        if props:lines+=["Properties and string matches:",*props[:70]]
        if size>4*1024*1024 and i<4 and shutil.which("binwalk"):
            rc,so,se=run(["binwalk","-B",str(p)],300)
            item["binwalk_exit"]=rc
            item["binwalk_head"]=so.splitlines()[:100]
            lines+=["Binwalk results:",*item["binwalk_head"][:55]]
    result["files"].append(item)
(out/"triage.json").write_text(json.dumps(result,indent=2,ensure_ascii=False),encoding="utf8")
(out/"README.md").write_text("\n".join(lines)+"\n",encoding="utf8")
print("\n".join(lines)[:18000],flush=True)
