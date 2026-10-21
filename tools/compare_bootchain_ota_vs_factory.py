#!/usr/bin/env python3
"""Compare verified stock OTA boot header inventory to original factory 8054 partition SHA.
Metadata only. No firmware writes.
"""
import argparse,json
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--ota",type=Path,required=True)
p.add_argument("--stock",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args()
ota=json.loads(a.ota.read_text())["parts"]
stock=json.loads(a.stock.read_text())["partitions"]
def canon(x):
    while x.endswith("_a"):x=x[:-2]
    return x
normalized={canon(k):v for k,v in stock.items() if isinstance(v,dict)}
rows={}
for k,rec in ota.items():
    baseline=normalized.get(k)
    rows[k]={"ota_sha256":rec.get("sha256"),"stock_8054_sha256":baseline.get("sha256") if baseline else None,
             "ota_size":rec.get("size"),"stock_8054_size":baseline.get("size") if baseline else None,
             "same":rec.get("sha256")==baseline.get("sha256") if baseline else None}
result={"base":"October 12 8052 OTA versus factory Sep 30 8054","partitions":rows,
        "limitations":["Whole image SHA differences do not prove bootloader code change.",
                       "Physical GPT and OTA partition naming normalized; no hardware trusted states measured.",
                       "For code attribution use disassembly, ELF .text comparison and live tests."]}
a.out.mkdir(parents=True,exist_ok=True)
(a.out/"bootchain_8052_vs_8054.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
lines=["# Bootchain partitions: latest 8052 OTA versus original factory 8054","",
"SHA from SHA256-verified release artifacts. No bootloader code executed or firmware flashed.","",
"| Partition | Same bytes? | OTA bytes | Factory 8054 bytes |","|---|---|---:|---:|"]
for k,v in rows.items():
    lines.append("| "+k+" | "+str(v["same"])+" | "+str(v["ota_size"])+" | "+str(v["stock_8054_size"])+" |")
lines+=["",
"Interpretation: byte differences are not yet classified as changed executable code, bug fixes, signatures, dates or board-specific constants.",
"Do not combine images from different revisions until live boot trust and recovery are understood.",""]
(a.out/"bootchain_8052_vs_8054.md").write_text("\n".join(lines)+"\n")
print("Boot chain factory comparison",[(k,v["same"]) for k,v in rows.items()],flush=True)
