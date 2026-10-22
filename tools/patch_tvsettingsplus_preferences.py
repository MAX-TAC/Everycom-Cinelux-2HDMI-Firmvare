#!/usr/bin/env python3
"""Integrate read-only/status and safe OEM projector settings shortcuts into TvSettingsPlus System menu.

For APKTOOL-DECODED 8052 TvSettingsPlus. Does not alter system/vendor, motor or calibration.
All four known screen variants must contain a System device preference root.
"""
from __future__ import annotations
import argparse
from pathlib import Path
from lxml import etree

ANDROID = "{http://schemas.android.com/apk/res/android}"
SCREEN_FILES = (
    "device.xml", "device_two_panel.xml", "device_vendor.xml", "device_x.xml",
)
SHORTCUTS = (
    # Title, summary, package, class. All target Activity components verified exported=true
    ("cinelux_projector_panel", "Настройки проектора",
     "Фокус, трапеция, изображение и другие аппаратные функции",
     "com.android.tv.settings", "com.android.tv.settings.uicustom.MainActivity"),
    ("cinelux_temperature", "Температура оборудования",
     "Температура процессора и подтверждённые датчики",
     "com.android.tv.settings", "com.android.tv.settings.cinelux.TemperatureInfoActivity"),
    ("cinelux_brightness", "Яркость",
     "Штатная настройка яркости проектора",
     "com.coolux.source", "com.coolux.source.activity.BrightActivity"),
    ("cinelux_sound", "Звук проектора",
     "Оригинальная панель звуковых настроек",
     "com.coolux.source", "com.coolux.source.activity.VoiceActivity"),
    ("cinelux_boot_source", "Источник при включении",
     "Выбор HDMI или другого источника после запуска",
     "com.coolux.source", "com.coolux.source.activity.BootSoureActivity"),
    ("cinelux_power_mode", "Режим питания",
     "Оригинальные настройки включения и ожидания",
     "com.coolux.source", "com.coolux.source.activity.PoweronModeActivity"),
    ("cinelux_orientation", "Установка проектора",
     "Проекция спереди, сзади и ориентация изображения",
     "com.coolux.source", "com.coolux.source.activity.ProjectModelActivity"),
    ("cinelux_keystone", "Трапеция",
     "Оригинальное пользовательское меню геометрии",
     "com.coolux.source", "com.coolux.source.activity.KeystoneActivity"),
    ("cinelux_ota", "Обновление системы",
     "Штатный клиент OTA-прошивки",
     "com.rjpj.yunota", "com.rjpj.yunota.OTASystemNetworkUpdateActivity"),
)

def patch(decoded: Path) -> list[tuple[str, int]]:
    directory = decoded / "res" / "xml"
    files = []
    # Parse and verify everything BEFORE modifying anything.
    for name in SCREEN_FILES:
        path = directory / name
        tree = etree.parse(str(path), etree.XMLParser(resolve_entities=False, no_network=True, remove_blank_text=False))
        root = tree.getroot()
        if root.tag.split("}")[-1] != "PreferenceScreen":
            raise ValueError(f"{name}: not PreferenceScreen")
        keys = {node.get(ANDROID+"key") for node in root.iter()}
        if "about_device" not in keys:
            raise ValueError(f"{name}: expected System screen key about_device missing")
        if "cinelux_projector" in keys or any(key in keys for key, *_ in SHORTCUTS):
            raise ValueError(f"{name}: already modified; refusing duplicate")
        files.append((path, tree, root))
    output = []
    for path, tree, root in files:
        group = etree.Element("PreferenceCategory", {
            ANDROID+"key": "cinelux_projector", ANDROID+"title": "Проектор"
        })
        for key, title, summary, package, cls in SHORTCUTS:
            pref = etree.SubElement(group, "Preference", {
                ANDROID+"key": key, ANDROID+"title": title, ANDROID+"summary": summary
            })
            etree.SubElement(pref, "intent", {
                ANDROID+"action": "android.intent.action.MAIN",
                ANDROID+"targetPackage": package,
                ANDROID+"targetClass": cls
            })
        # Keep original entries (including critical developer options and factory reset)
        # untouched; insert before restart if present.
        children = list(root)
        reboot_idx = next((i for i,x in enumerate(children) if x.get(ANDROID+"key") == "reboot"), len(children))
        root.insert(reboot_idx, group)
        tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=False)
        output.append((path.name, len(SHORTCUTS)))
    return output

def main() -> None:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("decoded", type=Path)
    args = argp.parse_args()
    for name, count in patch(args.decoded):
        print(f"Patched {name}: {count} supported user shortcut preferences")
    print("No factory/service/calibration routes created, no OEM APKs disabled.")

if __name__ == "__main__":
    main()
