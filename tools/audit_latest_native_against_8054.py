#!/usr/bin/env python3
"""Compare verified October 8052 OTA native/physical inventories with September 8054 factory.
All input data are original system images or manifests from completed pinned GitHub Actions.
No OEM binaries, keys, calibration data or proprietary source is published.
"""
import argparse,collections,json,re
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--ota-native",type=Path,required=True)
p.add_argument("--stock-native",type=Path,required=True)
p.add_argument("--ota-images",type=Path,required=True)
p.add_argument("--stock-manifest",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
a.out.mkdir(parents=True,exist_ok=True)
ota=json.loads(a.ota_native.read_text())
stock=json.loads(a.stock_native.read_text())
stock_parts=json.loads(a.stock_manifest.read_text())["partitions"]
def normalize(path):
    return re.sub(r"^(system|vendor|system_ext|product)(_a)?/",lambda m:m.group(1)+"/",path)
N={normalize(k):v for k,v in ota["native"].items()}
S={normalize(k):v for k,v in stock["native"].items()}
common=sorted(N.keys()&S.keys())
changed=[];stats=collections.Counter()
for name in common:
    x,y=N[name],S[name]
    if "error" in x or "error" in y:
        stats["parse_error"]+=1
        continue
    tx=x.get("sections",{}).get(".text",{}).get("sha256")
    ty=y.get("sections",{}).get(".text",{}).get("sha256")
    fullx=x.get("sha256");fully=y.get("sha256")
    textstatus="same" if tx and tx==ty else ("different" if tx and ty else "unknown")
    if fullx and fully and fullx==fully:stat="byte_identical"
    elif textstatus=="same":stat="same_executable_text_but_other_bytes_differ"
    elif textstatus=="different":stat="executable_text_differs"
    else:stat="inconclusive_or_metadata_only"
    stats[stat]+=1
    if stat=="byte_identical":continue
    depsx=set(x.get("needed",[]));depsy=set(y.get("needed",[]))
    exx=set(x.get("hardware_exports",[]));exy=set(y.get("hardware_exports",[]))
    changed.append({"path":name,"classification":stat,"text":textstatus,
        "ota_text_sha":tx,"stock_text_sha":ty,"ota_bytes":x.get("bytes"),"stock_bytes":y.get("bytes"),
        "ota_sha":fullx,"stock_sha":fully,
        "deps_only_ota":sorted(depsx-depsy)[:35],"deps_only_stock":sorted(depsy-depsx)[:35],
        "exports_only_ota":sorted(exx-exy)[:35],"exports_only_stock":sorted(exy-exx)[:35]})
only_ota=sorted(N.keys()-S.keys());only_stock=sorted(S.keys()-N.keys())
CHUNKS=["boot","mboot","optee","dtbo","vbmeta","vbmeta_system","linux_rootfs","tvservice","tvconfig","bootdata","factory","persist","super","armfw","project_id","3rd"]
def parkey(stem):
    return stem[:-2] if stem.endswith("_a") else stem
SP={parkey(k):v for k,v in stock_parts.items() if isinstance(v,dict)}
images={}
import hashlib
for img in sorted(a.ota_images.glob("*.img")):
    name=parkey(img.stem)
    if name in SP and name in CHUNKS:
        hasher=hashlib.sha256()
        with img.open("rb") as f:
            for b in iter(lambda:f.read(8*1024*1024),b""):hasher.update(b)
        x=SP[name]
        images[name]={"ota_sha":hasher.hexdigest(),"stock8054_sha":x["sha256"],"same":hasher.hexdigest()==x["sha256"],
            "ota_bytes":img.stat().st_size,"factory8054_bytes":x["size"]}
    elif name in CHUNKS:
        images[name]={"ota_present":True,"factory_comparable":False}
core=r"(tof|motor|camera|focus|hdmi|cec|audio|mi_|mstar|mtk|display|tvservice|trd|project|drm|boot|keystone|pmu|panel|source)"
high=[r for r in changed if re.search(core,r["path"],re.I)]
critical_code=[x for x in high if x["classification"]=="executable_text_differs"]
summary={"total_ota_elf":len(N),"total_factory_elf":len(S),"matched":len(common),"only_ota":len(only_ota),
         "only_factory":len(only_stock),"by_classification":dict(stats),
         "critical_code_changes":len(critical_code),
         "note":"section .text SHA equality is byte identity of code section; code changes may be bug fixes or board adaptations, not automatically attributable."}
report={"summary":summary,"partitions":images,"elf_changes":changed,"only_ota":only_ota,
        "only_factory":only_stock,"critical_code_changes":critical_code,
        "limits":["No actual device executed any code.","Static code-section SHA alone cannot determine intent or functional change.",
                  "Module runtime selection, SoC fuses, HDMI routing, AVB enforcement require actual hardware.","Stock manifest and OTA naming conventions were normalized, no crossflashing done."]}
(a.out/"native_diff.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
md=["# Latest 8052 OTA vs factory 8054: native executable code and boot partition audit","",
"Source 1: verified RUIOS.8052.1.0.4 official A/B OTA payload (October 2026).",
"Source 2: SHA-verified RUIOS.8054.1.0.1 original September factory archive, *previous run native and physical inventories*.",
"Scripts only read trusted source images, never execute binaries or flash the device.",
"",
"## Native ELF comparison","",
"| Classification | Number |","|---|---:|"]
for k,v in sorted(stats.items()):md.append("| "+k+" | "+str(v)+" |")
md+=["","- Matched native ELF paths: "+str(len(common)),
     "- ELF paths only in OTA/factory: "+str(len(only_ota))+"/"+str(len(only_stock)),
     "- Relevant ELF with changed .text: "+str(len(critical_code))+".",
"","## Changed .text in likely hardware code","",
"| Path | Bytes OTA / factory | Added dependencies | Removed dependencies |",
"|---|---|---|---|"]
for x in critical_code[:100]:
    md.append("| "+x["path"]+" | "+str(x["ota_bytes"])+" / "+str(x["stock_bytes"])+" | "+
              ", ".join(x["deps_only_ota"][:5])+" | "+", ".join(x["deps_only_stock"][:5])+" |")
if not critical_code:md.append("| No differing code-section SHA in selected paths | — | — | — |")
md+=["","## Full original physical boot / TV partitions","",
"| Partition | SHA identical? | OTA bytes | 8054 factory bytes |","|---|---|---:|---:|"]
for k,v in sorted(images.items()):
    md.append("| "+k+" | "+str(v.get("same","not comparable"))+" | "+str(v.get("ota_bytes","—"))+" | "+str(v.get("factory8054_bytes","—"))+" |")
md+=["","## Code vs metadata vs hardware inference","",
"- **Byte-identical** indicates same full ELF bytes.",
"- **Same executable .text** indicates the same .text bytecode but differences may remain in data, relocations or dynamic symbols.",
"- **Different executable .text** confirms machine-code changes, but does not tell whether a bug fix, OEM enhancement or a board-dependent change.",
"- Firmware image SHA differences can reflect embedded build dates and signatures as well as functional changes.",
"- No conclusions about compatibility or actual fuse/locked boot state follow from images alone.",
"- Do not swap any boot, OP-TEE, PMU, ToF, panel or TVservice component until there is a proven recovery path and live board identification.",
"",
"## Prioritized follow-up","",
"1. For each changed ELF .text identify matching source-service/ABI and symbol changes; disassembly and targeted manual review required to classify intent.",
"2. Compare bootloader bootargs and AVB policies via header inspection on stock images, not just SHA.",
"3. On a real 8052 and 8054 confirm boot state, running services and relevant hardware instances.",
"4. Keep this as reference metadata for future test builds; no modification until safe restoration verified.",
""]
(a.out/"native_diff.md").write_text("\n".join(md)+"\n")
print(json.dumps(summary,ensure_ascii=False),flush=True)
print("Physical partitions:",{k:v.get("same") for k,v in images.items()},flush=True)
print("Core code delta:",[x["path"] for x in critical_code[:25]],flush=True)
