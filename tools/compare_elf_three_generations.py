#!/usr/bin/env python3
"""Three-generation .text and byte SHA chronology: Aug 8052 -> Sep 8054 -> Oct 8052.
Input only verified native ELF metadata from archived stock actions and latest successful OTA audit.
No binaries/decompiled sources and no runtime operations.
"""
import argparse,collections,json,re
from pathlib import Path
p=argparse.ArgumentParser()
p.add_argument("--aug8052",type=Path,required=True)
p.add_argument("--sep8054",type=Path,required=True)
p.add_argument("--oct8052",type=Path,required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args();a.out.mkdir(parents=True,exist_ok=True)
def canon(path):return re.sub(r"^(system|vendor|product|system_ext)(_a)?/",lambda x:x.group(1)+"/",path)
def inventory(path):
    d=json.loads(path.read_text())["native"]
    return {canon(k):v for k,v in d.items()}
x=inventory(a.aug8052);y=inventory(a.sep8054)
octdiff=json.loads(a.oct8052.read_text())
delta={v["path"]:v for v in octdiff["elf_changes"]}
assert octdiff["summary"]["total_ota_elf"]==len(y)==1335
assert octdiff["summary"]["matched"]==len(y)
assert not octdiff["only_ota"] and not octdiff["only_factory"]
def trihash(left,middle,right):
    if not left or not middle or not right:return "missing_digest"
    if left==middle==right:return "all_three_same"
    if left!=middle and middle==right:return "changed_between_aug_and_sep_then_converged"
    if left==right and right!=middle:return "sep_8054_unique_against_both_8052"
    if left==middle and middle!=right:return "oct_8052_only_changed"
    return "all_three_distinct"
stats=collections.Counter();byte_stats=collections.Counter();changed=[]
for path in sorted(y):
    p1=x.get(path);p2=y[path]
    if not p1:continue
    t1=p1.get("sections",{}).get(".text",{}).get("sha256")
    t2=p2.get("sections",{}).get(".text",{}).get("sha256")
    ot=delta.get(path)
    # Already-verified exact byte match to Sept factory allows reuse of its .text digest.
    t3=ot.get("ota_text_sha") if ot else t2
    b1=p1.get("sha256")
    b2=p2.get("sha256")
    b3=ot.get("ota_sha") if ot else b2
    tstat=trihash(t1,t2,t3)
    bstat=trihash(b1,b2,b3)
    stats[tstat]+=1;byte_stats[bstat]+=1
    if tstat!="all_three_same":
        changed.append({"path":path,"classification":tstat,"byte_classification":bstat,
                        "text_sha":{"aug8052":t1,"sep8054":t2,"oct8052":t3},
                        "file_sha":{"aug8052":b1,"sep8054":b2,"oct8052":b3},
                        "original_code_bytes":[p1.get("sections",{}).get(".text",{}).get("size"),
                                               p2.get("sections",{}).get(".text",{}).get("size")],
                        "needed_additions_aug_to_sep":sorted(set(p2.get("needed",[]))-set(p1.get("needed",[])))[:20],
                        "needed_removals_aug_to_sep":sorted(set(p1.get("needed",[]))-set(p2.get("needed",[])))[:20]})
summary={"paths_compared":len(y),"text_classifications":dict(stats),
         "whole_file_classifications":dict(byte_stats),
         "changed_executable_paths":len(changed),
         "interpretation":"Convergence to the same machine code on two hardware profiles after the 8052 OTA strongly suggests a shared manufacturer software revision, but cannot alone prove the reason for the original change."}
report={"source":{"aug8052":"SHA-verified factory 8052 Aug 13 2026",
                  "sep8054":"SHA-verified factory 8054 Sep 30 2026",
                  "oct8052":"SHA-verified OTA 8052 Oct 12 2026"},
        "summary":summary,"changed_code":changed,
        "limitations":[".text equality does not establish identical runtime behavior when data and board properties differ.",
           "Classification is version history based on three known builds, not commit-history or source-level attribution.",
           "Runtimes and device revisions are not tested by this script."]}
(a.out/"three_generation_elf.json").write_text(json.dumps(report,ensure_ascii=False,indent=2)+"\n")
md=["# Three-generation native ELF code chronology: August 8052 → September 8054 → October 8052","",
"Machine-code hash comparison across **three original, SHA-verified vendor builds**; no firmware images redistributed or flashed.",
"","## .text hash evolution","",
"| Pattern | ELF count | Meaning / interpretation |","|---|---:|---|"]
desc={
"all_three_same":"The executable section stayed identical in all 3 images.",
"changed_between_aug_and_sep_then_converged":"The code in Sep-8054 first differs from Aug-8052 and Oct-8052 later adopted exactly Sep-8054 bytes; common update is plausible.",
"sep_8054_unique_against_both_8052":"8054 code remains different while Aug and Oct 8052 match; board-specific code is plausible, not proven.",
"oct_8052_only_changed":"Aug-8052 equals Sep-8054 but Oct-8052 changes; later correction possible, exact motive unverified.",
"all_three_distinct":"All three versions differ; further binary/source disassembly required.",
"missing_digest":"Insufficient digest data for classification."}
for k,v in sorted(stats.items()):md.append("| "+k+" | "+str(v)+" | "+desc.get(k,"—")+" |")
md+=["","## Complete ELF file hashes (including data and packaging)",""]
for k,v in sorted(byte_stats.items()):md.append("- "+k+": "+str(v))
md+=["","## All changed executable sections","",
"| Path | Version history class | .text bytes (Aug / Sep) | Linked dependencies changed? |","|---|---|---|---|"]
for f in changed:
    md.append("| "+f["path"]+" | "+f["classification"]+" | "+str(f["original_code_bytes"])+" | "+
              str(len(f["needed_additions_aug_to_sep"])+len(f["needed_removals_aug_to_sep"]))+" |")
md+=["","## Engineering verdict constraints","",
"- All-three-equal .text means no detected machine-code change in the section, even if signatures, data or filesystem metadata differ.",
"- Aug-to-Sep code change adopted by October 8052 is evidence of common software evolution, not proof of physical-board identity.",
"- Persistent 8054-unique code suggests board specialization but must be checked against version-related features.",
"- Identical code can still behave differently when ToF/HDMI build.props, Device Tree, PMU and runtime hardware differ.",
"- This method does **not** identify specific repaired bugs; function-level disassembly, vendor source or live reproduction is needed.",
""]
(a.out/"three_generation_elf.md").write_text("\n".join(md)+"\n")
print("THREE-GENERATION COMPARISON",summary,flush=True)
for f in changed:print("CHANGED",f["classification"],f["path"],flush=True)
