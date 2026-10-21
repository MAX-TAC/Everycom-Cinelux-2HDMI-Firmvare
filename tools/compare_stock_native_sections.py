#!/usr/bin/env python3
"""Compare verified ELF section and named-function digests without publishing code."""
import argparse,collections,json,re
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--ota",type=Path,required=True)
p.add_argument("--stock",type=Path,required=True)
p.add_argument("--out",type=Path,default=Path("analysis/Deep_Stock_Audit_20261021"))
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
ota=json.loads(a.ota.read_text());stock=json.loads(a.stock.read_text())
L,R=ota["files"],stock["files"]
common=sorted(set(L)&set(R))
hardware=re.compile(r"vendor_a/.+(?:tv|hdmi|cec|factory|i2c|motor|tof|audio|display|camera|mtk|trd|source)|system_a/system/lib/(?:libsettings|libfactory|librjpj|libtof|libtrd|libcom_mediatek|libruicamera|libfocus)",re.I)
result={"sources":[ota["variant"],stock["variant"]],"totals":{},"changed":[],"missing_or_added":{},"errors":ota["failed"]+stock["failed"]}
cats=collections.Counter()
for name in common:
    x,y=L[name],R[name]
    if x["sha256"]==y["sha256"]:
        cats["identical_file"]+=1
        continue
    def equal_section(sec):
        c=x["sections"].get(sec,{}).get("sha256")
        d=y["sections"].get(sec,{}).get("sha256")
        return c==d if c and d else None
    tx=equal_section(".text");rd=equal_section(".rodata");dt=equal_section(".data")
    case=("code_changed" if tx is False else "text_same_rodata_changed" if tx is True and rd is False
          else "text_same_data_changed" if tx is True and dt is False
          else "text_same_other_changed" if tx is True else "unclassified")
    cats[case]+=1
    sx,sy=x.get("functions",{}),y.get("functions",{})
    symnames=set(sx)&set(sy)
    changed=[k for k in sorted(symnames) if sx[k]["sha256"]!=sy[k]["sha256"]]
    opcode_changed=[k for k in changed if sx[k].get("opcode_only_sha256") and
                    sy[k].get("opcode_only_sha256") and
                    sx[k]["opcode_only_sha256"]!=sy[k]["opcode_only_sha256"]]
    opcode_same=[k for k in changed if sx[k].get("opcode_only_sha256") and
                    sy[k].get("opcode_only_sha256") and
                    sx[k]["opcode_only_sha256"]==sy[k]["opcode_only_sha256"]]
    record={"path":name,"kind":case,"section_status":{
        sec:{"ota_size":x["sections"].get(sec,{}).get("bytes"),"stock_size":y["sections"].get(sec,{}).get("bytes"),
             "same_hash":equal_section(sec)}
        for sec in (".text",".rodata",".data",".data.rel.ro",".rel.dyn",".rela.dyn")},
        "abi":{"ota_class":x["class"],"stock_class":y["class"],"machine":x["machine"],
               "needed_only_stock":sorted(set(y["deps"])-set(x["deps"])),
               "needed_only_ota":sorted(set(x["deps"])-set(y["deps"]))},
        "functions":{"common_named":len(symnames),"changed_named_count":len(changed),
                     "changed_named_sample":changed[:140],
                     "opcode_changed_count":len(opcode_changed),
                     "opcode_same_but_bytes_changed_count":len(opcode_same),
                     "opcode_changed_sample":opcode_changed[:120],
                     "opcode_same_sample":opcode_same[:100],
                     "only_stock":sorted(set(sy)-set(sx))[:80],
                     "only_ota":sorted(set(sx)-set(sy))[:80]},
        "hardware_relevant":bool(hardware.search(name))}
    result["changed"].append(record)
result["totals"]={"ota_all":len(L),"stock_all":len(R),"shared":len(common),
                  "only_in_ota":len(set(L)-set(R)),"only_in_stock":len(set(R)-set(L)),
                  "cases":dict(cats)}
result["missing_or_added"]={"only_ota":[n for n in sorted(set(L)-set(R)) if hardware.search(n)][:150],
                             "only_stock":[n for n in sorted(set(R)-set(L)) if hardware.search(n)][:150]}
(a.out/"native_ota8052_vs_stock8054.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
tick=chr(96)
lines=["# Native machine-code comparison: latest 8052 OTA vs stock 8054","",
"Original SHA256-verified 8052.1.0.4 OTA vs 8054.1.0.1 factory PKG. ELF sections and named function bytes compared by SHA.",
"Different .text SHA means different machine-code bytes, not necessarily a bug fix or board-specific functionality.",
"",
"## ELF totals",""]
lines+=["- "+k+": "+str(v) for k,v in result["totals"].items() if k!="cases"]
lines+=["- "+k+": "+str(v) for k,v in sorted(cats.items())]
lines+=["","## Projector hardware-relevant native ELF changes","",
"| File | Category | Same .text? | Same .rodata? | Changed named functions |",
"|---|---|---|---|---:|"]
focus=[c for c in result["changed"] if c["hardware_relevant"]]
focus.sort(key=lambda x:(0 if x["kind"]=="code_changed" else 1,x["path"]))
for c in focus[:220]:
    lines.append("| "+c["path"]+" | "+c["kind"]+" | "+str(c["section_status"][".text"]["same_hash"])+
                 " | "+str(c["section_status"][".rodata"]["same_hash"])+" | "+str(c["functions"]["changed_named_count"])+" |")
lines+=["","## Changes in executable machine code",""]
for c in focus:
    if c["kind"]!="code_changed":continue
    lines+=["","### "+c["path"],"",
            "- .text sizes OTA / stock: "+str(c["section_status"][".text"]["ota_size"])+"/"+str(c["section_status"][".text"]["stock_size"]),
            "- Named functions common / changed: "+str(c["functions"]["common_named"])+"/"+str(c["functions"]["changed_named_count"]),
            "- Dynamic dependency set changed: "+str(bool(c["abi"]["needed_only_stock"] or c["abi"]["needed_only_ota"])),
            "- Changed exported function examples:",
            "- Different disassembled mnemonic sequences: "+str(c["functions"]["opcode_changed_count"]),
            "- Identical mnemonic sequence despite code byte changes: "+str(c["functions"]["opcode_same_but_bytes_changed_count"])]
    lines.extend("- "+tick+z.replace(tick,"")+tick for z in c["functions"]["changed_named_sample"][:30])
    if not c["functions"]["changed_named_sample"]:lines.append("- Not available, possibly stripped binary.")
lines+=["","## Confidence and next steps","",
"Confirmed: differences in .text, read-only constant data, function SHA and dynamic symbol names.",
"Unconfirmed: why code changed, intended hardware, fault fixes, runtime ABI behavior and safe backports.",
"Prioritize ARM disassembly and control-flow diff for affected functions, then check real 8052 and 8054.",
"Analysis excludes most non-ELF boot firmware, OP-TEE/PMU, DTBO and embedded TV Linux userspace.",
"The actual 8054.1.0.4 firmware is not available for the binary comparison yet.",
""]
(a.out/"NATIVE_8052_OTA_VS_8054_RU.md").write_text("\n".join(lines)+"\n")
print("TOTAL",result["totals"],"hardware changes",len(focus),flush=True)
for c in focus:
    if c["kind"]=="code_changed":print("CODE",c["path"],c["functions"]["changed_named_count"],flush=True)
