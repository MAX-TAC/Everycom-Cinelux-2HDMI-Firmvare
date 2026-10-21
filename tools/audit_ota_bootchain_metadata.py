#!/usr/bin/env python3
"""Read-only AVB metadata/bootloader signature inventory from original RUIOS 8052 OTA.
No secrets, private data, binary dumps, signing or flashing.
"""
import argparse,collections,hashlib,json,re,struct
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--images",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args();a.out.mkdir(exist_ok=True,parents=True)
STOCK_PUB_SHA="dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe"
def be32(v,i):return struct.unpack_from(">I",v,i)[0]
def be64(v,i):return struct.unpack_from(">Q",v,i)[0]
def hashfile(p):
    h=hashlib.sha256()
    with p.open("rb") as f:
        for data in iter(lambda:f.read(8*1024*1024),b""):h.update(data)
    return h.hexdigest()
def avb(p):
    header=p.read_bytes()[:256]
    if len(header)<256 or header[:4]!=b"AVB0":return {"valid_avb_header":False}
    auth=be64(header,12);aux=be64(header,20)
    keyoff=be64(header,64);keysize=be64(header,72)
    descoff=be64(header,96);descsize=be64(header,104)
    data=p.read_bytes()
    assert 256+auth+aux<=len(data)
    assert keyoff+keysize<=aux
    assert descoff+descsize<=aux
    key=data[256+auth+keyoff:256+auth+keyoff+keysize]
    alltags=[];b=data[256+auth+descoff:256+auth+descoff+descsize]
    cursor=0
    while cursor+16<=len(b):
        tag,size=struct.unpack_from(">QQ",b,cursor)
        if cursor+16+size>len(b):break
        alltags.append(tag);cursor+=16+size
    pubsha=hashlib.sha256(key).hexdigest()
    release=header[128:176].split(b"\x00")[0].decode("ascii","replace")[:80]
    return {"valid_avb_header":True,"version":str(be32(header,4))+"."+str(be32(header,8)),
            "alg_id":be32(header,28),"auth_bytes":auth,"aux_bytes":aux,
            "signature_size":be64(header,56),"public_key_size":keysize,
            "public_key_sha256":pubsha,"equals_factory_8054_public_key_sha256":pubsha==STOCK_PUB_SHA,
            "rollback_index":be64(header,112),"flags":be32(header,120),
            "rollback_index_location":be32(header,124),
            "release_info":release,
            "descriptor_types":dict(collections.Counter(str(t) for t in alltags)),
            "NOTE":"Metadata parsed offline. These fields do not prove live bootloader verification policy."}
parts={}
for name in ("boot","mboot","optee","vbmeta","vbmeta_system","dtbo","armfw"):
    f=a.images/(name+".img")
    if not f.exists():parts[name]={"missing":True};continue
    with f.open("rb") as fd:head=fd.read(128)
    rec={"size":f.stat().st_size,"sha256":hashfile(f),
         "header_magic_ascii":head[:16].decode("ascii","backslashreplace")}
    if name.startswith("vbmeta"):rec["avb"]=avb(f)
    if name=="boot":rec["is_android_boot_image"]=head.startswith(b"ANDROID!")
    if name=="dtbo" and head.startswith(bytes.fromhex("d7b7ab1e")):
        rec["dtbo_entries"]=be32(head,16)
    if name in ("mboot","optee"):
        # A keyword hit is an indication of embedded diagnostics only,
        # not proof that a command or feature can be invoked on real hardware.
        hints=collections.Counter()
        data=f.read_bytes()
        for token in (b"fastboot",b"vbmeta",b"verity",b"rollback",b"secureboot",
                      b"androidboot",b"bootargs",b"recovery",b"unlock",b"dtbo",
                      b"optee",b"usb",b"avb",b"verify"):
            hints[token.decode()]=len(re.findall(re.escape(token),data,re.I))
        rec["string_keyword_counts"]=dict(hints)
    parts[name]=rec
result={"source":"SHA256-verified original RUIOS 8052 OTA (2026-10-12)",
        "factory_comparison":"Stock 8054 AVB key hash from analysis/HDMI_Comparison/AVB.md",
        "parts":parts,
        "limitations":["No stock 8054 bootloader body inspected by this tool; see physical inventory comparison.",
                       "No secure boot fuse, active trust policy, fastboot support or rollback behavior can be established from static string searches.",
                       "No partitions were modified, signed or flashed."]}
(a.out/"bootchain_ota_metadata.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
lines=["# Bootchain and AVB: original October OTA 8052","",
"All metadata obtained by read-only inspection of the original OTA payload. No device was accessed.",
"",
"## Image headers, cryptographic fields and software provenance","",
"| Partition | Bytes | SHA-256 prefix | Key checks |",
"|---|---:|---|---|"]
for n,v in parts.items():
    checks=[]
    if "avb" in v:
        av=v["avb"]
        checks=[("AVB="+str(av.get("valid_avb_header"))),
                ("key_equal_factory8054="+str(av.get("equals_factory_8054_public_key_sha256"))),
                ("flags="+str(av.get("flags"))),("rollback_index="+str(av.get("rollback_index"))),
                ("algo="+str(av.get("alg_id")))]
    if "is_android_boot_image" in v:checks+=["Android boot header="+str(v["is_android_boot_image"])]
    if "dtbo_entries" in v:checks+=["DTBO entries="+str(v["dtbo_entries"])]
    lines.append("| "+n+" | "+str(v.get("size","—"))+" | "+v.get("sha256","—")[:18]+" | "+", ".join(checks)+" |")
lines+=["","## Bootloader and OP-TEE static string hints (counts are NOT capabilities)",""]
for n in ("mboot","optee"):
    lines+=["- "+n+": "+str(parts.get(n,{}).get("string_keyword_counts",{}))]
lines+=["","## Hardware-only unknowns and release blockers","",
"- Cannot conclude the bootloader trusts a user-signed PKG or vbmeta. A matching public key only identifies the stock signing key.",
"- Cannot conclude that a live device allows fastboot/fastbootd, OEM unlock, root or a downgrade.",
"- Need actual slot/SELinux/verifiedbootstate/flash.locked/avb rollback values from a real device.",
"- Device-specific unique partitions and calibration require a private backup and verified restoration path BEFORE any update.",
"- Never use factory updater commands containing erase/wipe as the custom installer.",
""]
(a.out/"bootchain_ota_metadata.md").write_text("\n".join(lines)+"\n")
print("BOOT META",[(k,v.get("avb",{}).get("equals_factory_8054_public_key_sha256")) for k,v in parts.items()],flush=True)
