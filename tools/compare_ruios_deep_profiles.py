#!/usr/bin/env python3
"""Compare two original RUIOS OTA builds with direct DTS/config diffs; no firmware writes."""
import collections,difflib,json,re
from pathlib import Path

src=Path("/tmp/deep-ota-data")
one=json.loads((src/"8052.json").read_text())
two=json.loads((src/"8053.json").read_text())
root=Path("analysis/RUIOS_8052_vs_8053_Deep")
root.mkdir(parents=True,exist_ok=True)

def lines_diff(x,y,n=3):
    a=x.splitlines();b=y.splitlines()
    u=list(difflib.unified_diff(a,b,fromfile="8052",tofile="8053",n=n,lineterm=""))
    return u[:160],len(u),difflib.SequenceMatcher(None,a,b,autojunk=False).ratio()

# Both DTBO images contain 207 entries; the unique 2+2 blobs are pre-identified by SHA256.
x=one["two_unique_dtbo"]; y=two["two_unique_dtbo"]
candidate=[]
for i,p in enumerate(x):
    for j,q in enumerate(y):
        diff,total,ratio=lines_diff(p["dts"],q["dts"])
        candidate.append((ratio,i,j,diff,total))
candidate.sort(reverse=True)
used_a=set();used_b=set();pairs=[]
for ratio,i,j,diff,total in candidate:
    if i in used_a or j in used_b:continue
    used_a.add(i);used_b.add(j)
    pairs.append({"8052":{k:x[i][k] for k in ("index","id","size","sha256")},
                  "8053":{k:y[j][k] for k in ("index","id","size","sha256")},
                  "line_similarity":round(ratio,5),
                  "different_dts_lines_total":total,
                  "diff_lines":diff})
assert len(pairs)==2
pairs.sort(key=lambda p:p["8052"]["size"],reverse=True)
cfgs={}
for key in one["configs"]:
    a=one["configs"][key];b=two["configs"][key]
    same=a.get("sha256")==b.get("sha256") and a.get("sha256") is not None
    d,nd,sim=lines_diff(a.get("text",""),b.get("text",""),n=1)
    cfgs[key]={"same_sha":same,"sha_8052":a.get("sha256"),"sha_8053":b.get("sha256"),
              "sizes":[a.get("size"),b.get("size")],"diff_lines_total":nd,
              "diff_lines_preview":d,"similarity":round(sim,5),
              "error_8052":a.get("error"),"error_8053":b.get("error")}
# Existing independent inventory of the actual full Android OTA payloads.
original=[]
for code in ("8052","8053"):
    original.append(json.loads(Path("analysis/RUIOS_OTA_Comparison/"+code+"/inventory.json").read_text()))
builds=dict(zip(("8052","8053"),original))
comp=json.loads(Path("analysis/RUIOS_OTA_Comparison/comparison.json").read_text())
apps=[]
for app in comp["apps"]:
    path=app["path"]
    if any(k in path.lower() for k in ("rui","source","setting","focus","keystone","trd","factory","launcher","provision","setupwizard")):
        apps.append(app)
# Relevant partition image sizes and hash matches from previous SHA inventory.
partitions=comp["partition_comparison"]
out={
 "scope":"Verified OTA 8052 2026-10-12 vs OTA 8053 2026-06-12; static examination",
 "dtbo_changed_pairs":pairs,
 "configs":cfgs,
 "file_comparison":{k:comp[k] for k in ("shared_paths","identical_files","changed_files","only_8052","only_8053")},
 "apps":apps,
 "partition_comparison":partitions,
 "known_limitations":[
   "Matching DTS text does not certify the active overlay or physical panel.",
   "Two differing DTBO blobs are paired by maximum textual similarity; their entry IDs differ.",
   "The OTA build timestamps differ by four months, so source-code changes are not solely hardware changes.",
   "Missing ro.rjpj.hdmi.ports in 8053 does not mean HDMI is absent.",
   "Different whole-binary hashes can reflect metadata or build dates rather than altered executable code.",
   "Cross-flashing is unsafe without verified board profile, backups and recovery path."
 ]
}
(root/"comparison.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n")
fmt=lambda v: str(v) if v is not None else "not recorded"
md=[
 "# Deep comparison of public RUIOS 8052 and 8053 OTA builds",
 "",
 "Static audit only: verified ZIPs, two differing DTBO blobs, manufacturer TV configuration, Android image inventory.",
 "",
 "## Versions and device identity","",
 "| | RUIOS 8052 | RUIOS 8053 |","|---|---|---|",
 "| Public OTA | RUIOS.8052.1.0.4 | RUIOS.8053.1.0.0 |",
 "| Android build | eng.suhaix.20261012.025220 | eng.luzhih.20260612.083454 |",
 "| Android / pre-device | 13 / mt5873 | 13 / mt5873 |",
 "| Hardware model | Everycom 1 HDMI (photographic confirmation) | Unknown OEM product |",
 "| OTA machine ID | 8052 | 8053 |",
 "| Configured HDMI ports | 1 | not specified in vendor build.prop |",
 "| ToF function | 0 | not specified in vendor build.prop |",
 "| Autokeystone power on | 0 | 0 |",
 "",
 "## DTBO overview","",
 "Both DTBO images contain 207 entries, of which **205 exact DTB contents** are common as a multiset.",
 "These two unmatched blob pairs are matched by DTS line similarity, NOT by entry index.",
 ""
]
for n,p in enumerate(pairs,1):
    a=p["8052"];b=p["8053"]
    md += [
        f"### Changed DTBO profile {n}: {a['size']} → {b['size']} bytes",
        "",
        f"- 8052 entry index/ID: {a['index']}/{a['id']}; SHA256: {a['sha256']}",
        f"- 8053 entry index/ID: {b['index']}/{b['id']}; SHA256: {b['sha256']}",
        f"- DTS line similarity: {p['line_similarity']:.3%}; unified-diff lines: {p['different_dts_lines_total']}",
        "",
        "~~~diff",*p["diff_lines"],"~~~",""
    ]
md+=["## TV configuration differences",""]
for key,c in cfgs.items():
    md += [f"### {key}","",f"- Equal SHA256: **{c['same_sha']}**. Sizes: {c['sizes']}.",
            f"- Total diff lines: {c['diff_lines_total']}; text similarity: {c['similarity']:.2%}."]
    if c["error_8052"] or c["error_8053"]:
        md+=[f"- Extraction errors: 8052={c['error_8052']} 8053={c['error_8053']}"]
    else:
        md+=["","~~~diff",*c["diff_lines_preview"],"~~~"]
    md.append("")
md+=["## Android file comparison","",
     f"- Common file paths: **{comp['shared_paths']}**",
     f"- Identical full SHA256: **{comp['identical_files']}**",
     f"- Different SHA256: **{comp['changed_files']}**",
     f"- Only 8052: **{len(comp['only_8052'])}**; only 8053: **{len(comp['only_8053'])}**.",
     "",
     "### Files unique to OTA 8052","",*[f"- {s}" for s in comp["only_8052"]],
     "","### Files unique to OTA 8053","",*[f"- {s}" for s in comp["only_8053"]],
     "","### Selected manufacturer apps","",
     "| App path | 8052 version | 8053 version | Identical SHA? |",
     "|---|---|---|---|"]
for p in apps:
    md.append(f"| {p['path']} | {fmt(p['one_version'])} | {fmt(p['two_version'])} | {p['same_sha']} |")
md+=["","## Image partitions","",
     "| Partition | 8052 bytes | 8053 bytes | Exact SHA match? |",
     "|---|---:|---:|---|"]
for p in partitions:
    md.append(f"| {p['name']} | {fmt(p['one_bytes'])} | {fmt(p['two_bytes'])} | {p['same_sha']} |")
md+=["","## Interpretation and limitations","",
     "The two OTA channels are siblings on the same Android/MediaTek platform, but different OEM profiles and notably different build dates.",
     "Two DTBO contents vary, and board/DTBO mapping is not identical. This is evidence against considering the binaries interchangeable.",
     "Presence of hardware module names is evidence about software packaging, not proof of a physical sensor.",
     "OTA 8053 is NOT identified as a one-HDMI or two-HDMI projector without device-side confirmation.",
     "No projector was flashed; all steps used static read-only tools.",""]
(root/"README.md").write_text("\n".join(md)+"\n")
print("\n".join(md[:60]),flush=True)
