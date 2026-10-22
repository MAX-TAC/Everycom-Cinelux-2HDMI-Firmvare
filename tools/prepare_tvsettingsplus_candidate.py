#!/usr/bin/env python3
"""Prepare decoded ORIGINAL TvSettingsPlus APK for EXPERIMENTAL candidate build.

Never modifies vendor/kernel, installs apps, disables KuSettings or touches Android.
Works only on apktool decoded tree from verified 8052 system_ext/priv-app.
"""
from __future__ import annotations
import argparse
import re
from pathlib import Path

from lxml import etree
from patch_tvsettingsplus_manifest import patch_manifest

ANDROID = "http://schemas.android.com/apk/res/android"
NAME = "{" + ANDROID + "}name"
EXPORT = "{" + ANDROID + "}exported"
TV = "com.android.tv.settings"
ROUTER = TV + ".cinelux.LegacySettingsRouterActivity"
TEMP = TV + ".cinelux.TemperatureInfoActivity"
LEGACY = (
 "android.settings.WIFI_SETTINGS",
 "android.settings.BLUETOOTH_SETTINGS",
 "android.settings.AUTO_BLUETOOTH",
 "android.settings.DATETIME_SETTINGS",
 "android.settings.LAUGUAGE_SETTINGS",
 "android.settings.LAUGUAGE_LOCAL_SETTINGS",
 "android.settings.ALLAPPS",
 "android.settings.PROJECTABOUT_SETTINGS",
 "android.settings.BRIGHT_SETTINGS",
 "android.settings.VOICE_SETTINGS",
 "android.settings.PROJECTMODEL_SETTINGS",
 "android.settings.BOOTSOURE_SETTINGS",
 "android.settings.POWERMODE_SETTINGS",
 "android.settings.KEYSTONE_SETTINGS",
 "android.settings.SYSTEMUPDATE",
)

def prepare(decoded: Path) -> tuple[int, int]:
    manifest = decoded / "AndroidManifest.xml"
    print(patch_manifest(manifest, True))
    parser = etree.XMLParser(remove_blank_text=False, resolve_entities=False, no_network=True)
    tree = etree.parse(str(manifest), parser)
    root = tree.getroot()
    if root.get("package") != TV:
        raise ValueError("wrong package after patch")
    app = root.find("application")
    if app is None:
        raise ValueError("No <application> tag")
    for cls in (ROUTER, TEMP):
        matching = [x for x in app.findall("activity") if x.get(NAME) == cls]
        if matching:
            raise ValueError("Activity already present; fail rather than duplicate: " + cls)
    router = etree.SubElement(app, "activity", {
        NAME: ROUTER, EXPORT: "true", "{" + ANDROID + "}label": "Настройки проектора"
    })
    # Grouping actions into one filter is safe: the router inspects getAction().
    filters = etree.SubElement(router, "intent-filter")
    for action in LEGACY:
        etree.SubElement(filters, "action", {NAME: action})
    etree.SubElement(filters, "category", {NAME: "android.intent.category.DEFAULT"})
    temp = etree.SubElement(app, "activity", {
        NAME: TEMP, EXPORT: "true", "{" + ANDROID + "}label": "Температура оборудования"
    })
    # Temporary launcher entry for bench-testing, prior to integration in System menu.
    launcher = etree.SubElement(temp, "intent-filter")
    etree.SubElement(launcher, "action", {NAME: "android.intent.action.MAIN"})
    etree.SubElement(launcher, "category", {NAME: "android.intent.category.LEANBACK_LAUNCHER"})
    tree.write(str(manifest), encoding="utf-8", xml_declaration=True, pretty_print=False)

    # Apktool stores versionCode in apktool.yml. Do not mutate Android:sharedUserId.
    yml = decoded / "apktool.yml"
    source = yml.read_text(encoding="utf-8")
    match = re.search(r"(?m)^(\s*versionCode:\s*)(['\"]?)(\d+)(['\"]?)(\s*)$", source)
    if not match:
        raise ValueError("versionCode missing or unsupported format in apktool.yml")
    original = int(match.group(3))
    if original >= 2147483000:
        raise ValueError("versionCode too large for safe increment")
    candidate = original + 1
    start, end = match.span(3)
    yml.write_text(source[:start] + str(candidate) + source[end:], encoding="utf-8")
    print(f"Candidate app versionCode {original} -> {candidate}")
    print("No KuSettings, KuSourceRJ, HAL or other packages modified.")
    return original, candidate

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("decoded", type=Path)
    args = ap.parse_args()
    original, next_code = prepare(args.decoded)
    print(f"EXPERIMENTAL ONLY: version codes {original}->{next_code}")
    print("Actual package installation, signature match, and app functions remain untested.")

if __name__ == "__main__":
    main()
