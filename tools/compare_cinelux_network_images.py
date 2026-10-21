#!/usr/bin/env python3
"""Classify Ethernet/Wi-Fi evidence from three independently verified RUIOS images."""
import collections,json
from pathlib import Path
directory=Path("/tmp/net-audit")
data={label:json.loads((directory/(label+".json")).read_text()) for label in ("8052-factory","8052-ota","8054-factory")}
output=Path("analysis/Network_8052_Regression_20261021")
output.mkdir(exist_ok=True,parents=True)
rows=[]
for v,d in data.items():
    for category in ("wifi_modules","ethernet_modules"):
        for row in d[category]:
            rows.append({"variant":v,"kind":category,"name":Path(row["path"]).name,
                         "path":row["path"],"sha":row["sha256"],"text":row["sections"].get(".text"),
                         "rodata":row["sections"].get(".rodata"),"modinfo":row["modinfo"]})
names=sorted(set(r["name"] for r in rows))
matrix={}
for name in names:
    observed={x["variant"]:x for x in rows if x["name"]==name}
    matrix[name]={"versions":observed}
    for a,b in (("8052-factory","8052-ota"),("8052-ota","8054-factory")):
        x=observed.get(a);y=observed.get(b)
        matrix[name][a+"__"+b]={
            "both_present":bool(x and y),
            "same_full":x["sha"]==y["sha"] if x and y else None,
            "same_code":x["text"]==y["text"] if x and y and x["text"] and y["text"] else None,
            "same_rodata":x["rodata"]==y["rodata"] if x and y and x["rodata"] and y["rodata"] else None,
            "same_modinfo":x["modinfo"]==y["modinfo"] if x and y else None}
firmware={}
for variant,d in data.items():
    for f in d["firmware_candidates"]:
        firmware.setdefault(f["path"],{})[variant]={"sha256":f["sha256"],"size":f["size"]}
report={"sources":{k:{"stats":v["stats"]} for k,v in data.items()},
        "kernel_modules":matrix,"firmware":firmware,
        "network_runtime_config":{v:d["init_refs"][:100] for v,d in data.items()},
        "network_feature_xml":{v:d["network_features"] for v,d in data.items()},
        "module_load_lists":{v:d["modules_index"] for v,d in data.items()},
        "note":"Static image evidence. Ethernet drivers may be built into boot kernel; PHY may be disabled by DT even if source files exist."}
(output/"network_image_comparison.json").write_text(json.dumps(report,indent=2,ensure_ascii=False)+"\n")
lines=["# Wi-Fi and Ethernet: RUIOS 8052 factory vs OTA, and factory 8054","",
"Sources are three original SHA256-verified images. No network access on a projector, no configuration changes.",
"Variants: August 2026 factory 8052, October 2026 OTA 8052.1.0.4, September 2026 factory 8054.1.0.1.",
"",
"## Is an updated 8052 driver a plausible regression cause?","",
"| Module | Factory 8052 → OTA 8052 .text identical? | OTA 8052 ↔ factory 8054 .text identical? | Versions in .modinfo |",
"|---|---|---|---|"]
for name,item in matrix.items():
    if not any(t in name.lower() for t in ("wlan","wifi","ether","eth","phy","mdio","gmac","stmmac","r81")):continue
    a=item["8052-factory__8052-ota"];b=item["8052-ota__8054-factory"]
    vermag={}
    for v,o in item["versions"].items():
        vermag[v]=next((val[8:] for val in o["modinfo"] if val.startswith("vermagic=")),"unknown")
    lines.append("| "+name+" | "+str(a["same_code"])+" | "+str(b["same_code"])+" | "+(" / ".join(k+":"+val.split(" SMP")[0] for k,val in vermag.items()))+" |")
lines+=["","## Firmware files with Wi-Fi/BT-related filename","",
"| File | Original 8052 | OTA 8052 | Original 8054 |", "|---|---|---|---|"]
for path,entry in sorted(firmware.items()):
    names=[]
    for v in ("8052-factory","8052-ota","8054-factory"):
        z=entry.get(v)
        names.append(z["sha256"][:14] if z else "absent")
    lines.append("| "+path+" | "+" | ".join(names)+" |")
lines+=["","## Network init and configuration file references","",
"Only selected network-related lines are retained; sensitive identifiers, NVRAM, per-device calibration and passwords are excluded."]
for v,d in data.items():
    lines+=["","### "+v]
    for f in d["init_refs"][:45]:
        lines+=["","**"+f["path"]+"**"]
        for m in f["matches"][:14]:lines.append("- "+str(m["line"])+": "+m["text"].replace("|","/"))
    if not d["init_refs"]:lines.append("- No matching references in scanned init/build.prop files.")
lines+=["","## Distinguishing LAN problems","",
"- **No link**: router port LED off, kernel sysfs carrier 0/operstate down even when eth0 UP; investigate PHY power, device-tree enablement, board wiring, speed negotiation, cable, vendor Ethernet driver.",
"- **Link but no IP**: carrier 1, speed negotiated, no IPv4; investigate Android EthernetManager/netd, DHCP, static IP and network priority.",
"- **No eth0 interface**: verify /sys/class/net and loaded/built-in driver, DT/PHY and init services. A physical RJ45 port does not ensure enabled Ethernet in the current SKU.",
"- **Wi-Fi slow but linked**: distinguish RSSI, link PHY rate, channel/band, iperf3 LAN test vs public speedtest, Bluetooth coexistence and kernel/firmware driver logs.",
"- **Regression after OTA**: determine if link/speed changed after upgrade; static hashes alone cannot prove actual cause.",
"",
"## What this offline scan cannot establish","",
"- Ethernet MAC might be built directly into the kernel; no external .ko does not prove missing Ethernet support.",
"- DTBO blobs and factory TV service may configure PHY/MAC independently of Android vendor init files.",
"- Kernel module with any name may remain unused; report cannot identify physical Wi-Fi chip without live interface/driver details.",
"- Do not mix kernel modules across versions while vermagic / CONFIG_MODVERSIONS differs.",
"- No firmware replacement proposed until actual chipset, chip bus and reference performance are verified.",
""]
(output/"NETWORK_REGRESSION_RU.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
print("NETWORK COMPARISON modules",len(matrix),"firmware",len(firmware))
for name,v in matrix.items():
    if "wlan_mt" in name.lower() or "eth" in name.lower():
        print(name,"8052old/latest",v["8052-factory__8052-ota"])
