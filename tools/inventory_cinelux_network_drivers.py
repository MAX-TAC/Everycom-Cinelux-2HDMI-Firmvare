#!/usr/bin/env python3
"""Read-only WLAN/LAN provenance scan for original verified CineLux RUIOS images.
No net scans, credentials, calibration values, firmware replacement or writes to projector.
"""
import argparse,collections,hashlib,json,re,subprocess
from pathlib import Path
from elftools.elf.elffile import ELFFile

p=argparse.ArgumentParser()
p.add_argument("--root",type=Path,required=True)
p.add_argument("--variant",required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
a.out.parent.mkdir(parents=True,exist_ok=True)
root=a.root
summary={"variant":a.variant,"wifi_modules":[],"ethernet_modules":[],"firmware_candidates":[],
         "init_refs":[],"network_features":[],"network_properties":[],
         "board_support_files":[],"modules_index":[],"stats":{}}
wifi=re.compile(r"(wlan_mt|wlan\.ko|mt7663|mt7902|mt7961|mt76|wifi.*\.ko|btmtk|bluetooth.*\.ko)",re.I)
eth=re.compile(r"(ethernet|(^|[/_-])eth([_.-]|$)|gmac|r815[236]|r816[89]|stmmac|dwmac|mdio|(^|/)phy[_a-z0-9-]*\.ko|mtk_net|mstar[_-]?eth)",re.I)
firmware=re.compile(r"(mt7663|mt7902|mt7961|wlan|wifi|btmtk|bluetooth|ethernet|gmac|mdio)",re.I)
secret=re.compile(r"(?:nvram|nvcfg|calibrat|ssid|passw|passwd|psk|secret|private|user.?data|macaddr|mac_addr|key|cert|widevine|hdcp|serial)",re.I)
interesting_line=re.compile(r"(?i)(?:\b(?:eth0|eth1|wlan0|wlan1|ethernet|wlan|wifi|btmtk|bluetooth|mdio|gmac|stmmac|r8169|r8152|mt7663|mt7902|mt7961)\b|(?:^|[/_\s])(?:eth|lan)[_\s./-])")
def sha_file(f):
    h=hashlib.sha256()
    with f.open("rb") as s:
        for chunk in iter(lambda:s.read(8*1024*1024),b""):h.update(chunk)
    return h.hexdigest()
files_seen=0
for part in sorted(root.iterdir()):
    if not part.is_dir() or not part.name.endswith("_a"):continue
    for f in part.rglob("*"):
        if not f.is_file():continue
        files_seen+=1
        rel=f.relative_to(root).as_posix()
        # Never inspect or disclose unique NVRAM/SSID/private certificates.
        if secret.search(f.name):continue
        if f.name.endswith(".ko"):
            category="wifi" if wifi.search(rel) else ("ethernet" if eth.search(rel) else None)
            if category:
                meta={"path":rel,"sha256":sha_file(f),"bytes":f.stat().st_size,"sections":{},
                      "modinfo":[],"needed_modules":[]}
                try:
                    with f.open("rb") as s:
                        elf=ELFFile(s)
                        for sec in (".text",".rodata",".modinfo"):
                            obj=elf.get_section_by_name(sec)
                            meta["sections"][sec]=hashlib.sha256(obj.data()).hexdigest() if obj else None
                            if sec==".modinfo" and obj:
                                info=[x.decode(errors="replace") for x in obj.data().split(b"\x00")]
                                meta["modinfo"]=sorted(x for x in info if x.startswith(("vermagic=","depends=","version=","srcversion=")))[:15]
                except Exception as exc:
                    meta["elf_error"]=type(exc).__name__
                summary[category+"_modules"].append(meta)
        if ("/firmware/" in rel or "/wifi/" in rel or "/bluetooth/" in rel) and firmware.search(f.name):
            summary["firmware_candidates"].append({"path":rel,"size":f.stat().st_size,"sha256":sha_file(f)})
        if ("/etc/permissions/" in rel or "/etc/vintf/" in rel) and f.suffix==".xml" and ("ethernet" in f.name.lower() or "wifi" in f.name.lower()):
            summary["network_features"].append({"path":rel,"sha256":sha_file(f)})
        if f.name in ("modules.load","modules.load.recovery","modules.dep","modules.order","modules.alias"):
            if len(summary["modules_index"])<35:
                lines=f.read_text(errors="replace").splitlines()
                chosen=[line.strip()[:240] for line in lines if interesting_line.search(line) and not secret.search(line)]
                summary["modules_index"].append({"path":rel,"matched_lines":chosen[:80]})
        if re.search(r"(^|/)init[^/]*\.rc$|/etc/init/[^/]+\.rc$",rel) or (f.name in ("build.prop","vendor.prop")):
            if f.stat().st_size>2*1024*1024:continue
            selected=[]
            for number,line in enumerate(f.read_text(errors="replace").splitlines(),1):
                if secret.search(line) or not interesting_line.search(line):continue
                if "http" in line or "@" in line:continue
                selected.append({"line":number,"text":line.strip()[:240]})
                if len(selected)>=35:break
            if selected:
                summary["init_refs"].append({"path":rel,"sha256":sha_file(f),"matches":selected})
summary["stats"]={"files_examined":files_seen,"wifi_modules":len(summary["wifi_modules"]),
                  "eth_modules":len(summary["ethernet_modules"]),
                  "firmware_candidates":len(summary["firmware_candidates"]),
                  "init_config_files_with_refs":len(summary["init_refs"])}
a.out.write_text(json.dumps(summary,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
print("NETWORK INVENTORY",a.variant,summary["stats"],flush=True)
for category in ("wifi_modules","ethernet_modules"):
    for item in summary[category]:
        print(category,item["path"],item["modinfo"][:3],flush=True)
