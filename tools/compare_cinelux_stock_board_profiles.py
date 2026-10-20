#!/usr/bin/env python3
"""Compare original 8052/8054 board configs, GPIO and DTBO mappings."""
import collections,difflib,json,re
from pathlib import Path
base=Path("/tmp/stock-board-input")
one=json.loads((base/"8052.json").read_text())
two=json.loads((base/"8054.json").read_text())
out=Path("analysis/Stock_8052_vs_8054_Board")
out.mkdir(parents=True,exist_ok=True)
tick=chr(96)

def kv(s):
    section="global"; result={}
    for line in s.splitlines():
        t=line.strip()
        if not t or t.startswith(("#",";","//")):continue
        if t.startswith("[") and "]" in t:
            section=t.split("]",1)[0][1:]
        elif "=" in t:
            key,value=t.split("=",1)
            key=key.strip()
            if re.match(r"^[a-zA-Z_][\w.:/-]*$",key):
                result[(section,key)]=value.split(";",1)[0].split("#",1)[0].strip()
    return result

files={}
for name,x in one["files"].items():
    y=two["files"][name]
    record={"same_sha":x["sha256"]==y["sha256"],
            "sha8052":x["sha256"],"sha8054":y["sha256"],
            "bytes":[x["size"],y["size"]]}
    if "text" in x and "text" in y:
        left,right=kv(x["text"]),kv(y["text"])
        record["changed"]=[dict(section=k[0],name=k[1],v8052=left[k],v8054=right[k])
                          for k in sorted(left.keys()&right.keys()) if left[k]!=right[k]]
        record["added"]=[dict(section=k[0],name=k[1],value=right[k]) for k in sorted(right.keys()-left.keys())]
        record["removed"]=[dict(section=k[0],name=k[1],value=left[k]) for k in sorted(left.keys()-right.keys())]
        dif=list(difflib.unified_diff(x["text"].splitlines(),y["text"].splitlines(),
                                     fromfile="8052",tofile="8054",n=2,lineterm=""))
        record["diff_line_count"]=len(dif)
        record["diff_excerpt"]=dif[:140]
        record["key_count"]=[len(left),len(right)]
    files[name]=record

A=one["dtbo"]["entries"];B=two["dtbo"]["entries"]
counter1=collections.Counter(x["sha256"] for x in A)
counter2=collections.Counter(x["sha256"] for x in B)
bysha=collections.defaultdict(list)
for x in B:bysha[x["sha256"]].append(x["index"])
same_positions=sum(x["sha256"]==B[i]["sha256"] for i,x in enumerate(A))
dtbo={"entry_counts":[len(A),len(B)],"matching_contents":sum((counter1&counter2).values()),
      "same_index":same_positions,"changed_index":len(A)-same_positions,
      "moved_examples":[dict(id=x["id"],from_index=x["index"],to_index=bysha[x["sha256"]][0])
                        for x in A if x["sha256"] in bysha and x["index"]!=bysha[x["sha256"]][0]][:30]}

previous=json.loads(Path("analysis/HDMI_Comparison/comparison.json").read_text())
props={}
for p in previous["build_prop_comparison"]:
    key=p["name"].split(":")[-1]
    if key.startswith("ro.rjpj.") and (not p["identical"] or re.search("hdmi|tof|focus|machine|keystone",key)):
        if not re.search("serial|mac|password|token|secret|private",key,re.I):
            props[key]={"8052":p["one"],"8054":p["two"]}

result={"sources":["Stock Everycom 8052 (2026-08-13, 1 HDMI)",
                   "Stock Everycom 8054 (2026-09-30, 2 HDMI)"],
        "oem_properties":props,"files":files,"dtbo":dtbo,
        "android_apps":previous["apps"],
        "limitations":["These are factory images, not board-specific live calibration.",
                       "Matching content across DTBO tables does not confirm live overlay selection.",
                       "Different file SHA may indicate build metadata changes, not altered function.",
                       "Cross-flashing and swapping hardware-specific partitions are not established as safe."]}
(out/"comparison.json").write_text(json.dumps(result,ensure_ascii=False,indent=2)+"\n")
md=["# Stock Everycom 8052 versus 8054 — board configuration comparison","",
    "Read-only analysis of SHA256-verified original factory archives, decrypted PKGs, ext4 config files and DTBO.",
    "8052 is the 1-HDMI profile; 8054 is the 2-HDMI/ToF profile used in two-port CineLux OEM firmware.",
    "A two-HDMI FlixTone also displays 8054; this does not prove that its PCB matches the CineLux PCB.","",
    "## Android OEM settings","",
    "| Property | 8052 | 8054 |","|---|---|---|"]
for key,p in sorted(props.items()):
    if re.search("machine.id|hdmi|tof|auto|keystone|focus|yunota.version|yunota.url",key):
        md.append("| "+key+" | "+str(p["8052"]).replace("|","/")+" | "+str(p["8054"]).replace("|","/")+" |")
md+=["","## Board pins and GPIO from board.ini",""]
board=files["board.ini"]
md += ["- Full SHA identical: "+str(board["same_sha"]),
       "- Modified config values: "+str(len(board["changed"]))+
       ", added: "+str(len(board["added"]))+
       ", removed: "+str(len(board["removed"]))+".",
       "- Text diff lines: "+str(board["diff_line_count"])+".","",
       "| Group | Property | 8052 | 8054 |","|---|---|---|---|"]
for item in board["changed"]:
    md.append("| "+" | ".join(str(item[k]).replace("|","/") for k in ("section","name","v8052","v8054"))+" |")
for label,key in (("Added in 8054","added"),("Removed in 8054","removed")):
    md += ["","### "+label,""]
    md += ["- "+tick+x["section"]+"/"+x["name"]+"="+x["value"]+tick for x in board[key][:100]]
md += ["","### Board.ini text diff","", "~~~diff",*board["diff_excerpt"],"~~~",
       "","## DTBO content and indexes","",
       "- DTBO entries: "+str(dtbo["entry_counts"])+".",
       "- Identical blobs regardless of order: "+str(dtbo["matching_contents"])+".",
       "- Matching at same index: "+str(dtbo["same_index"])+".",
       "- Different position: "+str(dtbo["changed_index"])+".",
       "","### Representative moves","",
       "| ID | 8052 position | 8054 position |","|---|---:|---:|"]
md += ["| "+str(p["id"])+" | "+str(p["from_index"])+" | "+str(p["to_index"])+" |" for p in dtbo["moved_examples"][:18]]
md+=["","## Vendor TV configuration files","",
     "| File | Byte-identical? | Sizes (8052 / 8054) | Changed keys | Added / removed keys |",
     "|---|---|---|---:|---|"]
for name,p in files.items():
    md.append("| "+name+" | "+str(p["same_sha"])+" | "+str(p["bytes"][0])+" / "+str(p["bytes"][1])+
              " | "+str(len(p.get("changed",[])))+" | "+str(len(p.get("added",[])))+
              " / "+str(len(p.get("removed",[])))+" |")
for name in ("tvconfig/dtbo_mapping.ini","bootdata/dtbo_mapping.ini",
             "ConfigDefaultValue.ini","BasicSound_HDMI.ini","BasicSound_DTV.ini","BasicSound_MM.ini"):
    p=files[name]
    md+=["","### "+name,"",
         "Same SHA256: "+str(p["same_sha"])+
         "; modified config keys: "+str(len(p.get("changed",[])))+
         "; added: "+str(len(p.get("added",[])))+
         "; removed: "+str(len(p.get("removed",[])))+
         "; text diff lines: "+str(p.get("diff_line_count",0))+".",
         "","~~~diff",*p.get("diff_excerpt",[])[:90],"~~~"]
md+=["","## Software differences relevant to porting","",
     "### Applications added in the 8054 factory image",""]
md += ["- "+tick+p+tick for p in previous["apps"]["two_only"]]
md += ["","### Applications present only in 8052",""]
md += ["- "+tick+p+tick for p in previous["apps"]["one_only"]]
md += ["","### Different manufacturer packages",""]
md += ["- "+tick+p+tick for p in previous["apps"]["changed"]
       if re.search("KuSettings|KuSource|AutoFocus|Keystone|TvSettings|trdservice|Factory|zxlauncher",p,re.I)]
md+=["","## Engineering conclusions","",
     "- Keep one shared Android codebase with separate board profiles 8052 and 8054.",
     "- A DTBO with the same blobs but different entry order requires its matching DTBO mapping.",
     "- Preserve board GPIO, PMU, HDMI audio, focus/ToF and panel defaults per variant.",
     "- Do not assume identical physical PCBs from a common hardware machine ID.",
     "- OTA 8053 is excluded as a supported hardware profile; consider its APKs only for optional software features.",
     "- No image was installed and no device state or calibration was modified.",""]
(out/"README.md").write_text("\n".join(md)+"\n")
print("DONE board changed",len(board["changed"]),"added",len(board["added"]),
      "removed",len(board["removed"]),"same DTBO",dtbo["matching_contents"],flush=True)
print("\n".join(md[:56]),flush=True)
