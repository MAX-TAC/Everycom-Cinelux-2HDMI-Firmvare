#!/usr/bin/env python3
"""Compare actual stock OEM TvSettingsPlus Decompiled Java class/method surfaces against
ONE clearly named AOSP Android 13 tag, not a claim about OEM's actual fork point.
No AOSP or OEM source copied to report.
"""
import collections,hashlib,json,re
from pathlib import Path
UP=Path("/tmp/aosp-tv/Settings/src/com/android/tv/settings")
OEM=Path("/tmp/tv-jadx/sources/com/android/tv/settings")
OUT=Path("analysis/Settings_Wizard_Debloat_20261021")
assert UP.is_dir(), "AOSP TvSettings Settings/src absent"
assert OEM.is_dir(), "OEM TvSettingsPlus JADX sources absent"
A={x.relative_to(UP).as_posix():x for x in UP.rglob("*.java")}
B={x.relative_to(OEM).as_posix():x for x in OEM.rglob("*.java")}
a,b=set(A),set(B)
same=sorted(a&b)
def method_names(p):
 s=p.read_text(errors="replace")
 # Source methods in actual AOSP and OEM JADX may differ in signature
 hits=re.findall(r"(?m)^\s*(?:(?:public|private|protected|final|static|synchronized|native)\s+){1,5}[\w<>[\].?, ]+\s+([A-Za-z_$]\w*)\s*\([^;{}]*?\)\s*(?:throws\s+[\w., ]+)?(?:\{|;)",s)
 return set(x for x in hits if x not in ("if","for","switch","while","catch"))
areas=lambda items:dict(collections.Counter(x.split("/")[0] if "/" in x else "top-level" for x in items))
detail=[]
for key in same:
 oa=method_names(A[key]);ob=method_names(B[key])
 if not oa and not ob:continue
 added=sorted(ob-oa);lost=sorted(oa-ob)
 if not added and not lost:continue
 if key.startswith(("partnercustomizer/","uicustom/")):continue
 detail.append({"class":key,"shared_methods":len(oa&ob),"aosp_only":lost[:20],"oem_only":added[:20],
               "aosp_total":len(oa),"oem_total":len(ob)})
detail.sort(key=lambda o:len(o["aosp_only"])+len(o["oem_only"]),reverse=True)
result={"baseline":"AOSP TvSettings android-13.0.0_r56 (reference ONLY; not proven OEM parent)",
        "aosp_java_classes":len(a),"oem_java_classes":len(b),
        "both_paths":len(same),"aosp_only":len(a-b),"oem_only":len(b-a),
        "oem_path_group_counts":areas(b-a),"aosp_path_group_counts":areas(a-b),
        "method_surface_changes":detail[:160],
        "unique_oem_examples":sorted(b-a)[:220],
        "aosp_missing_examples":sorted(a-b)[:100],
        "limits":["JADX is not original source; nested classes and synthetic constructs differ.",
                  "Tag 13_r56 is a known open upstream reference but not established OEM fork commit.",
                  "Method name differences do not prove bugs or behavior changes.",
                  "Only com/android/tv/settings class namespace is compared; OEM MediaTek copied classes outside it are excluded."]}
(OUT/"aosp_tvsettings_13_reference_diff.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n")
lines=["# Проверка TV Settings по официальному исходнику AOSP Android 13","",
"Comparison: original SHA-verified RUIOS 8052.1.0.4 TvSettingsPlus APK (JADX class names/method surfaces) **versus** public AOSP TvSettings tag \`android-13.0.0_r56\`.",
"",
"**Внимание:** это НЕ доказательство, что OEM использовал именно r56. Исходный commit производителя неизвестен, а результат JADX не равен исходному Java. Здесь выявляем OEM namespace/classes и потенциальные различия API, но не объявляем баги.",
"",
"| Показатель | Количество |","|---|---:|",
" | AOSP Java классы | "+str(result["aosp_java_classes"])+" |",
" | OEM JADX Java классы | "+str(result["oem_java_classes"])+" |",
" | Путь класса найден с обеих сторон | "+str(result["both_paths"])+" |",
" | Пути только в OEM | "+str(result["oem_only"])+" |",
" | Пути только в AOSP | "+str(result["aosp_only"])+" |","",
"## OEM-only namespace names",""]
for group,n in sorted(result["oem_path_group_counts"].items(),key=lambda x:-x[1]):lines.append("- "+group+": "+str(n)+" Java classes")
lines+=["","## Differing method names in shared class paths (bounded sample)","",
"Method names, not machine-code semantics. Differences also include changes from the exact upstream tag chosen as reference.",""]
for z in detail[:65]:
 lines.append("- "+z["class"]+": AOSP-only "+", ".join(z["aosp_only"][:8])+"; OEM-only "+", ".join(z["oem_only"][:8]))
lines+=["","## Correct bug-review procedure","",
"1. Focus only on project-owned \`uicustom\`, \`partnercustomizer\`, fork-specific extensions, and changes to common entrypoints.",
"2. For a candidate with direct hardware or settings writes: analyze branch conditions, exception handling, permissions, and persistence.",
"3. Compare exact methods only after establishing OEM's real AOSP fork point; a single Android 13 release tag is NOT sufficient to attribute a fault.",
"4. Confirm any crash/regression with real-device logcat and reproducible conditions; never call harmless-looking factory calibration methods on another user's projector.",
"","Source reference: https://android.googlesource.com/platform/packages/apps/TvSettings/+/refs/tags/android-13.0.0_r56",""]
(OUT/"AOSP_TVSETTINGS_13_REFERENCE_RU.md").write_text("\n".join(lines)+"\n")
print("RESULT",result["aosp_java_classes"],result["oem_java_classes"],result["both_paths"],result["oem_only"],result["aosp_only"],flush=True)
