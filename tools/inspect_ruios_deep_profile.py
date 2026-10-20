#!/usr/bin/env python3
"""Read-only, bounded extraction of hardware-related text and selected DTBO blobs from genuine OTA images."""
import argparse, hashlib, json, re, struct, subprocess
from pathlib import Path

p=argparse.ArgumentParser()
p.add_argument("--code",required=True,choices=["8052","8053"])
p.add_argument("--images",required=True,type=Path)
p.add_argument("--out",required=True,type=Path)
args=p.parse_args()
args.out.mkdir(parents=True,exist_ok=True)

TARGETS={
 "8052":["ce500de3b701285f471ad473cc1c7c0e32119e2a5dba28a676335b3167a20c15","e1242cf41e005a442146439184f36e119526231c0550a378bc2518e5585fbead"],
 "8053":["9727bc37fa26fab29a11d326804906c6e51ae50e697fd6082974adf97b8e7dd9","bb87edc8b839f2ebac6bd38aec7a058f1fc1d14eb0c3420d4b2f2ef7f694ab99"]
}
raw=(args.images/"dtbo.img").read_bytes()
head=struct.unpack(">8I",raw[:32])
magic,total,header_size,entry_size,count,entries_offset,page_size,version=head
assert magic==0xD7B7AB1E and count==207 and entry_size==32
target_records=[]
for i in range(count):
    length,offset,bid,rev,c0,c1,c2,c3=struct.unpack(">8I",raw[entries_offset+i*entry_size:entries_offset+(i+1)*entry_size])
    assert 0<length<600000 and 0<offset<len(raw)-length+1
    blob=raw[offset:offset+length]
    sha=hashlib.sha256(blob).hexdigest()
    if sha not in TARGETS[args.code]:continue
    cmd=subprocess.run(["dtc","-q","-I","dtb","-O","dts","-o","-"],input=blob,
                       stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=30)
    if cmd.returncode:raise RuntimeError(f"dtc failed on {args.code} index {i}: {cmd.stderr[:150]}")
    dts=cmd.stdout.decode("utf-8","replace")
    target_records.append(dict(index=i,id=bid,revision=rev,size=length,sha256=sha,
                               dts=dts[:180000],dtc_warnings=cmd.stderr.decode("utf-8","replace")[:180]))
assert len(target_records)==2,(args.code,len(target_records))

names={
 "board_ini":("tvconfig","bsp/board/BD_MT5873_H1V1_B6_S/board.ini"),
 "dtbo_mapping_tv":("tvconfig","config/dtbo_mapping.ini"),
 "dtbo_mapping_boot":("bootdata","config/dtbo_mapping.ini"),
 "tv_defaults":("tvconfig","platform/data/misc/ConfigDefaultValue.ini"),
 "hdmi_audio":("tvconfig","bsp/chip/aq/InputSrc/BasicSound_HDMI.ini")
}
files={}
for name,(partition,path) in names.items():
    img=args.images/(partition+".img")
    assert img.is_file(),img
    proc=subprocess.run(["debugfs","-R","cat /"+path,str(img)],capture_output=True,timeout=35)
    if proc.returncode or not proc.stdout:
        files[name]={"error":proc.stderr.decode("utf-8","replace")[:300]}
        continue
    content=proc.stdout
    sha=hashlib.sha256(content).hexdigest()
    if len(content)>350000:
        files[name]={"size":len(content),"sha256":sha,"error":"too_large_to_include"}
        continue
    val=content.decode("utf-8","replace")
    safe=[]
    for line in val.splitlines():
        if re.search(r"(?i)(passw|secret|private.?key|serial.?number|mac.?address|uuid|token|imei|widevine|hdcp.?key)",line):
            safe.append("[redacted nonhardware value]")
        else:
            safe.append(line[:400])
    files[name]={"size":len(content),"sha256":sha,"text":"\n".join(safe)[:350000]}

result={"code":args.code,"dtbo_table":dict(total_entries=count,entry_size=entry_size,
               table_version=version,header_size=header_size),
        "two_unique_dtbo":target_records,"configs":files}
(args.out/(args.code+".json")).write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
print(args.code,[(x["index"],x["id"],x["size"]) for x in target_records],flush=True)
print("config hashes",{k:v.get("sha256") for k,v in files.items()},flush=True)
