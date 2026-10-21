#!/usr/bin/env python3
"""Compare 8052 OTA vs 8054 factory Wi-Fi modules from previously verified ELF metadata.
Does not touch devices and does not assume module presence == active hardware.
"""
import json,collections
from pathlib import Path
p=Path("/tmp/native-versions")
a=json.loads((p/"ota8052.json").read_text())
b=json.loads((p/"stock8054.json").read_text())
files=a["files"];base=b["files"]
target_names=["wlan_mt7663.ko","wlan_mt7902.ko","wlan_mt7961.ko","dtv_driver.ko"]
results={"compared":["RUIOS.8052.1.0.4 Oct 2026 OTA","RUIOS.8054.1.0.1 Sep 2026 stock PKG"],"modules":[]}
for target in target_names:
    matches=sorted(set(n for n in files if n.endswith("/"+target))&set(n for n in base if n.endswith("/"+target)))
    for name in matches:
        x,y=files[name],base[name]
        sect={}
        for sec in (".text",".rodata",".modinfo",".data",".data.rel.ro"):
            lhs=x["sections"].get(sec);rhs=y["sections"].get(sec)
            sect[sec]={"same":lhs is not None and rhs is not None and lhs["sha256"]==rhs["sha256"],
                       "size_8052":lhs["bytes"] if lhs else None,
                       "size_8054":rhs["bytes"] if rhs else None}
        common=set(x.get("functions",{}))&set(y.get("functions",{}))
        changed=[k for k in sorted(common) if x["functions"][k]["sha256"]!=y["functions"][k]["sha256"]]
        result={"file":name,"same_full_file":x["sha256"]==y["sha256"],"sections":sect,
                "modinfo_8052":x.get("modinfo",[]),"modinfo_8054":y.get("modinfo",[]),
                "common_named_functions":len(common),"changed_named_functions":len(changed),
                "changed_named_sample":changed[:75]}
        results["modules"].append(result)
        print("MODULE",target,"same .text",sect[".text"]["same"],"same .rodata",sect[".rodata"]["same"],
              "same modinfo",sect[".modinfo"]["same"],"common functions",len(common),flush=True)
out=Path("analysis/Stock_Custom_Architecture_20261021")
(out/"mt7663_module_metadata.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
lines=["# Исходный драйвер MT7663 и альтернативные Wi-Fi модули: сравнительная метаинформация","",
"Сравнение SHA-верифицированной октябрьской OTA 8052.1.0.4 и сентябрьской заводской 8054.1.0.1.",
"Источник: два успешных job инвентаризации ELF (run 39574844708), без запуска модулей.",
"**Наличие модуля в образе не означает его загрузку на конкретном устройстве.**",
"",
"| Модуль | Полный файл совпадает? | Машинный код (.text) совпадает? | Константы (.rodata) совпадают? | .modinfo совпадает? | Общих функций / разный код |",
"|---|---|---|---|---|---|"]
for r in results["modules"]:
    lines.append("| "+r["file"]+" | "+str(r["same_full_file"])+" | "+str(r["sections"][".text"]["same"])+
                 " | "+str(r["sections"][".rodata"]["same"])+" | "+str(r["sections"][".modinfo"]["same"])+
                 " | "+str(r["common_named_functions"])+"/"+str(r["changed_named_functions"])+" |")
for r in results["modules"]:
    lines+=["","## "+r["file"],"",
            "- Изменена .text: "+str(not r["sections"][".text"]["same"])+
            ". Это не доказывает исправление драйвера.",
            "- Текст version/vermagic/depends/srcversion из .modinfo 8052: "+(str(r["modinfo_8052"]) if r["modinfo_8052"] else "нет извлечённых полей"),
            "- Те же поля для 8054: "+(str(r["modinfo_8054"]) if r["modinfo_8054"] else "нет извлечённых полей")]
lines+=["","## Источники возможного обновления","",
"- Mainline Linux mt76/mt7615 supports MT7663 over PCIe/USB/SDIO, but a generic kernel 6.x module is not an interchangeable replacement for the OEM 5.10 BSP driver.",
"- linux-firmware provides device microcode/firmware; firmware files, kernel Wi-Fi module and Bluetooth driver must be checked separately.",
"- MediaTek Genio/Yocto announcement in Aug 2026 is *not* proof of Bluetooth restrictions in OEM RUIOS Android 13.",
"- To choose a newer module: detect real Wi-Fi chip and bus, identify 8052/8054 OEM kernel vermagic/modversions, get compatible source + firmware, confirm WLAN/BT HAL/SELinux/power-management compatibility, then test rollback.",
"- If the chip is not MT7663, defer the detailed 7663 driver port entirely.",
"",
"## Источники",
"",
"- https://wireless.docs.kernel.org/en/latest/en/users/drivers/mediatek.html",
"- https://github.com/torvalds/linux/blob/master/drivers/net/wireless/mediatek/mt76/mt7615/Kconfig",
"- https://github.com/morrownr/mt76",
"- https://genio-community.mediatek.com/t/bluetooth-support-for-mt7663-in-yocto/2775",
""]
(out/"MT7663_DRIVER_COMPARISON_RU.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
