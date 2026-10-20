#!/usr/bin/env python3
"""Read-only extract selected board configuration from verified decrypted OEM PKG."""
import argparse, hashlib, json, re, struct, subprocess
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--plain",type=Path,required=True)
p.add_argument("--script",type=Path,required=True)
p.add_argument("--variant",required=True,choices=("8052","8054"))
p.add_argument("--work",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
a.work.mkdir(parents=True,exist_ok=True)
a.out.mkdir(parents=True,exist_ok=True)
wanted=("tvconfig_a","bootdata_a","dtbo_a")
lines=a.script.read_text(encoding="utf-8").splitlines()
segments={}
for i,line in enumerate(lines):
    if not line.startswith("filepartload "): continue
    cols=line.split()
    following=[]
    for ln in lines[i+1:]:
        if ln.startswith("filepartload "):break
        following.append(ln)
    match=None
    for partition in wanted:
        if any(re.search(r"\bpartition write mmc 0 "+partition+r"\b",ln) for ln in following):
            match=partition
            break
    if match and match not in segments:
        segments[match]={"offset":int(cols[4],16),"bytes":int(cols[3],16)}
assert set(segments)==set(wanted),segments

images={}
for name,meta in segments.items():
    zipped=a.work/(name+".lz4")
    with a.plain.open("rb") as src,zipped.open("wb") as output:
        src.seek(meta["offset"]-4096)
        remaining=meta["bytes"]
        while remaining:
            chunk=src.read(min(4*1024*1024,remaining))
            if not chunk:raise EOFError((name,remaining))
            output.write(chunk);remaining-=len(chunk)
    img=a.work/(name+".img")
    subprocess.run(["lz4","-q","-d","-f",str(zipped),str(img)],check=True,timeout=120)
    zipped.unlink()
    images[name]=img
    print("DECODED",a.variant,name,img.stat().st_size,flush=True)

FILES={
"board.ini":("tvconfig_a","bsp/board/BD_MT5873_H1V1_B6_S/board.ini"),
"tvconfig/dtbo_mapping.ini":("tvconfig_a","config/dtbo_mapping.ini"),
"bootdata/dtbo_mapping.ini":("bootdata_a","config/dtbo_mapping.ini"),
"BasicSound_HDMI.ini":("tvconfig_a","bsp/chip/aq/InputSrc/BasicSound_HDMI.ini"),
"BasicSound_DTV.ini":("tvconfig_a","bsp/chip/aq/InputSrc/BasicSound_DTV.ini"),
"BasicSound_MM.ini":("tvconfig_a","bsp/chip/aq/InputSrc/BasicSound_MM.ini"),
"ConfigDefaultValue.ini":("tvconfig_a","platform/data/misc/ConfigDefaultValue.ini"),
"gammatable_1.ini":("tvconfig_a","bsp/common/PQ_general/gammatable_1.ini"),
"pmu_mcs51_sign.bin":("bootdata_a","pmu/pmu_mcs51_sign.bin")
}
data={"variant":a.variant,"source":"stock PKG decrypted locally, read-only","segments":segments,"files":{}}
for key,(partition,filepath) in FILES.items():
    exe=subprocess.run(["debugfs","-R","cat /"+filepath,str(images[partition])],
                       capture_output=True,timeout=45)
    if exe.returncode or not exe.stdout:
        raise RuntimeError("debugfs failed for "+key+" "+exe.stderr.decode("utf-8","replace")[-260:])
    raw=exe.stdout
    entry={"size":len(raw),"sha256":hashlib.sha256(raw).hexdigest()}
    if key.endswith(".ini") and key not in ("gammatable_1.ini",):
        if len(raw)>400000:raise ValueError("unexpectedly large config "+key)
        txt=raw.decode("utf-8","replace")
        # Only factory default source files, no device-specific NVRAM/calibration.
        forbidden=re.compile(r"(?i)(serial[_ ]?number|mac[_ ]?address|password|private.?key|widevine|hdcp.?key|imei|api[_-]?token)")
        lines_out=[line if not forbidden.search(line) else "# [redacted]" for line in txt.splitlines()]
        entry["text"]="\n".join(lines_out)
    data["files"][key]=entry
    print("READ",a.variant,key,len(raw),entry["sha256"][:15],flush=True)

raw=images["dtbo_a"].read_bytes()
magic,total,header_len,entry_len,count,offset,page,version=struct.unpack(">8I",raw[:32])
assert magic==0xd7b7ab1e and count==207 and entry_len==32
entries=[]
for i in range(count):
    start=offset+i*entry_len
    size,pos,id,rev,c0,c1,c2,c3=struct.unpack(">8I",raw[start:start+32])
    assert pos+size<=len(raw)
    blob=raw[pos:pos+size]
    assert blob[:4]==bytes.fromhex("d00dfeed")
    entries.append({"index":i,"id":id,"rev":rev,"size":size,"sha256":hashlib.sha256(blob).hexdigest()})
data["dtbo"]={"entry_count":count,"entries":entries,"image_sha256":hashlib.sha256(raw).hexdigest()}
(a.out/(a.variant+".json")).write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
print("DONE",a.variant,"profile complete",flush=True)
