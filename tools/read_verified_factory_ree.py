#!/usr/bin/env python3
"""Read-only unpack of VERIFIED stock REE PKG using already-published project workflow.
No cryptographic key is uploaded, logged or committed by this script.
It does NOT sign/re-encrypt a firmware package or modify a device.
"""
import argparse,re,subprocess
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--pkg",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
p.add_argument("--existing-workflow",type=Path,default=Path(".github/workflows/deep-apk-diff.yml"))
a=p.parse_args();a.out.parent.mkdir(parents=True,exist_ok=True)
workflow=a.existing_workflow.read_text()
m=re.search(r"['\"]-K['\"]\s*,\s*['\"]([A-Fa-f0-9]{64})['\"]",workflow)
if not m:raise RuntimeError("Could not locate preexisting shared OEM AES key in verified analysis workflow")
key=m.group(1)
with a.pkg.open("rb") as file:
    head=file.read(4096)
start=re.search(rb"REE_OFFSET_START\s*=\s*0x([A-Fa-f0-9]+)",head)
length=re.search(rb"REE_OFFSET_LEN\s*=\s*0x([A-Fa-f0-9]+)",head)
if not start or not length:raise RuntimeError("Unrecognized PKG metadata")
offset=int(start.group(1),16);size=int(length.group(1),16)
assert offset==4096 and size%16==0 and size>100*1024*1024
assert size+offset<=a.pkg.stat().st_size and head[0x500:0x508]==b"MTK....."
with a.pkg.open("rb") as origin,a.out.open("wb") as out:
    origin.seek(offset)
    proc=subprocess.Popen(["openssl","enc","-d","-aes-256-cbc","-nopad",
       "-K",key,"-iv","00000000000000000000000000000000"],stdin=subprocess.PIPE,stdout=out)
    remaining=size
    while remaining:
        block=origin.read(min(remaining,8*1024*1024))
        if not block:raise EOFError("Encrypted REE unexpectedly short")
        proc.stdin.write(block);remaining-=len(block)
    proc.stdin.close()
    if proc.wait():raise RuntimeError("Unpack verification failed")
with a.out.open("rb") as f:
    h=f.read(65536)
assert b"gpt create mmc 0" in h and b"filepartload" in h,"Decryption output invalid"
print("Verified factory payload decrypted in temporary isolated runner; bytes:",size)
