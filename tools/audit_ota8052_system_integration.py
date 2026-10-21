#!/usr/bin/env python3
"""Read-only current OTA integration inventory: init service, privilege grants, TV inputs, key layouts.
No APK, firmware, keys, serials or proprietary configuration data published.
"""
import collections,hashlib,json,re,subprocess,xml.etree.ElementTree as ET
from pathlib import Path

base=Path("/tmp/erofs")
out=Path("analysis/Global_Firmware_Map_20261021")
out.mkdir(exist_ok=True,parents=True)
partitions=[p for p in base.iterdir() if p.is_dir()]
data={"source":"SHA256 verified original RUIOS.8052.1.0.4 October OTA",
      "apk_paths":[],"boot_services":[],"key_layouts":[],"privileged_grants":[],"overlays":[],
      "errors":[],"counts":{}}
focus=re.compile(r"trd|rjpj|hysd|keystone|projector|tof|motor|tv|mtk|wifi|wlan|bluetooth|ota|hdmi|cec|audio|input|ether|network|boot|factory|thermal|power|auto.?pair",re.I)
for part in partitions:
    apks=list(part.rglob("*.apk"))
    for p in apks:
        r=p.relative_to(base).as_posix()
        data["apk_paths"].append(r)
        if "/overlay/" in r or r.split("/")[0]=="overlay":data["overlays"].append(r)
    rcfiles=[p for p in part.rglob("*.rc") if "/etc/init/" in p.as_posix() or p.name.startswith("init.")]
    for rc in rcfiles:
        rel=rc.relative_to(base).as_posix()
        text=rc.read_text(errors="replace")
        for line_no,line in enumerate(text.splitlines(),1):
            m=re.match(r"^\s*service\s+([A-Za-z0-9_.:-]+)\s+([^\s#]+)",line)
            if m and focus.search(m.group(1)+" "+m.group(2)):
                data["boot_services"].append({"rc":rel,"line":line_no,"service":m.group(1),"executable":m.group(2)[:220]})
    for kl in part.rglob("*.kl"):
        rel=kl.relative_to(base).as_posix()
        lines=kl.read_text(errors="replace").splitlines()
        keep=[]
        for l in lines:
            m=re.match(r"^\s*key\s+([^\s#]+)\s+([A-Z0-9_]+)",l)
            if m and any(x in m.group(2) for x in ["HOME","SETTINGS","MENU","SOURCE","TV_INPUT","INPUT","FOCUS","BACK","VOLUME","POWER","DPAD"]):
                keep.append({"keycode":m.group(1),"action":m.group(2)})
        data["key_layouts"].append({"path":rel,"sha256":hashlib.sha256(kl.read_bytes()).hexdigest(),"relevant_keys":keep[:70],"relevant_key_count":len(keep)})
    for xmlfile in part.rglob("*.xml"):
        rel=xmlfile.relative_to(base).as_posix()
        if "/etc/permissions/" not in rel and "/etc/sysconfig/" not in rel:continue
        try:
            tree=ET.parse(xmlfile)
        except Exception:
            continue
        for tag in tree.iter():
            if tag.tag in ("privapp-permissions","permissions"):
                package=tag.attrib.get("package")
                if not package or not re.search(r"(?i)tv\.settings|trd|rjpj|hysd|coolux|mediatek|zeasn|my\.settings|android\.provision",package):
                    continue
                granted=sorted(set(c.attrib.get("name","") for c in tag.iter() if c.tag in ("permission","allow-permission") and c.attrib.get("name")))
                denied=sorted(set(c.attrib.get("name","") for c in tag.iter() if c.tag in ("deny-permission","deny") and c.attrib.get("name")))
                data["privileged_grants"].append({"source":rel,"package":package,"requested_or_granted":granted,"denied":denied})
    print("SCANNED",part.name,"APK",len(apks),"boot-services",len(data["boot_services"]),"layouts",len(data["key_layouts"]),flush=True)
data["apk_paths"].sort()
data["boot_services"].sort(key=lambda x:(x["service"],x["rc"]))
data["key_layouts"].sort(key=lambda x:x["path"])
data["counts"]={
    "apk_paths":len(data["apk_paths"]),"init_service_entries_matching_oem_or_hardware":len(data["boot_services"]),
    "key_layout_files":len(data["key_layouts"]),"privilege_xml_declarations":len(data["privileged_grants"]),
    "overlay_apks":len(data["overlays"])}
(out/"ota8052_init_permissions_keylayout.json").write_text(json.dumps(data,ensure_ascii=False,indent=2)+"\n")
tick=chr(96)
lines=["# Оригинальная OTA 8052.1.0.4: init, разрешения, раскладки пульта и системные APK","",
"Сканирование только оригинальных распакованных readonly partitions Android; не заменяет реальные PackageManager и сервисы в памяти.",
"",
"## Количество найденных компонентов",""]
lines+=["- "+k+": "+str(v) for k,v in data["counts"].items()]
lines+=["","## Аппаратные/OEM init services","",
"| Service | Executable | .rc source |","|---|---|---|"]
for row in data["boot_services"][:140]:
    lines.append("| "+row["service"]+" | "+tick+row["executable"].replace(tick,"")+tick+" | "+row["rc"]+" |")
lines+=["","## Android privilege XML for OEM and TV Settings",""]
for grant in data["privileged_grants"][:90]:
    lines+=["### "+grant["package"],
            "From "+tick+grant["source"]+tick,
            "Permissions: "+(", ".join(grant["requested_or_granted"]) if grant["requested_or_granted"] else "none listed"),""]
lines+=["","## KeyLayout files relevant to HOME/SETTINGS/INPUT",""]
for kl in data["key_layouts"]:
    if kl["relevant_keys"] and (focus.search(kl["path"]) or any(t in kl["path"].lower() for t in ("remote","vendor_"))):
        lines+=["### "+kl["path"],"",
                "- SHA256: "+kl["sha256"],
                "- Mapped relevant keys: "+", ".join(x["keycode"]+"→"+x["action"] for x in kl["relevant_keys"][:45]),""]
lines+=["","## APK and overlay coverage","",
"All APK paths (including APEX-bundled APK) listed in JSON. APK on disk does not prove installed for user 0 or actively started.",
"Overlay list: "+(", ".join(data["overlays"][:70]) if data["overlays"] else "none found in scanned partitions."),
"",
"## Current unknowns and release implications","",
"- Android Settings may be redirected by launchers, GlobalKeyEventProcess, default intents and overlay definitions; a .kl mapping alone cannot prove target Activity.",
"- OEM privileged permissions can depend on platform signature, shared UID, SELinux and execution context. Copying an APK to priv-app does not automatically restore those rights.",
"- Compare this latest 8052 index with a **verified 8054 of the same release generation** before removing OEM binaries.",
"- Boot service presence is a configuration fact, not proof of an active driver/daemon at runtime.",
"- No OEM binaries, keys, firmware or personal identifiers were exported.",
""]
(out/"OTA8052_INIT_PERMISSIONS_KEYLAYOUT_RU.md").write_text("\n".join(lines)+"\n")
print("DONE",data["counts"],flush=True)
