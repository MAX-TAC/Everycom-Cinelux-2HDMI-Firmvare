#!/usr/bin/env python3
"""Stage-1 safe AndroidManifest patch for DECODED OEM TvSettingsPlus.
Does not build/sign APK, disable packages, flash, or touch the projector.
Use: python3 tools/patch_tvsettingsplus_manifest.py /path/to/apktool-decoded [--apply]
Requires: pip install lxml
"""
from __future__ import annotations

import argparse
import shutil
import sys
from pathlib import Path

try:
    from lxml import etree
except ImportError:
    sys.exit("lxml required: python3 -m pip install lxml")

ANDROID = "http://schemas.android.com/apk/res/android"
ATTR_NAME = "{" + ANDROID + "}name"
ATTR_EXPORTED = "{" + ANDROID + "}exported"
PKG = "com.android.tv.settings"
TARGET_ACTIVITY = PKG + ".MainSettings"
ACTION = "android.settings.SETTINGS"
CATEGORY = "android.intent.category.DEFAULT"


def full_name(pkg: str, name: str) -> str:
    return pkg + name if name.startswith(".") else (pkg + "." + name if "." not in name else name)


def patch_manifest(path: Path, apply: bool) -> str:
    if not path.is_file():
        raise ValueError(f"AndroidManifest.xml absent: {path}")
    parser = etree.XMLParser(remove_blank_text=False, resolve_entities=False, no_network=True)
    tree = etree.parse(str(path), parser)
    root = tree.getroot()
    pkg = root.get("package")
    if pkg != PKG:
        raise ValueError(f"Unexpected APK package: {pkg!r}; expected {PKG!r}")
    app = root.find("application")
    if app is None:
        raise ValueError("Missing application element")
    matches = [
        element for element in app.findall("activity")
        if full_name(pkg, element.get(ATTR_NAME, "")) == TARGET_ACTIVITY
    ]
    if len(matches) != 1:
        raise ValueError(f"Expected exactly one MainSettings Activity; found {len(matches)}")
    target = matches[0]
    if target.get(ATTR_EXPORTED) != "true":
        raise ValueError("MainSettings exported!=true: unsafe baseline, refusing")
    for intent_filter in target.findall("intent-filter"):
        actions = {x.get(ATTR_NAME) for x in intent_filter.findall("action")}
        categories = {x.get(ATTR_NAME) for x in intent_filter.findall("category")}
        if ACTION in actions and CATEGORY in categories:
            return "ALREADY PRESENT: MainSettings handles android.settings.SETTINGS; no changes"
    if not apply:
        return "DRY RUN: would add ACTION_SETTINGS + DEFAULT filter to MainSettings; no files changed"
    intent_filter = etree.Element("intent-filter")
    etree.SubElement(intent_filter, "action", {ATTR_NAME: ACTION})
    etree.SubElement(intent_filter, "category", {ATTR_NAME: CATEGORY})
    target.append(intent_filter)
    backup = path.with_suffix(".xml.before-cinelux")
    if backup.exists():
        raise ValueError(f"Refusing to overwrite existing backup: {backup}")
    shutil.copy2(path, backup)
    tree.write(str(path), encoding="utf-8", xml_declaration=True, pretty_print=False)
    return f"PATCHED {path}; original backup: {backup}; did NOT build an APK"


def main() -> int:
    argp = argparse.ArgumentParser(description=__doc__)
    argp.add_argument("decoded_apk_dir", type=Path)
    argp.add_argument("--apply", action="store_true", help="Modify decoded AndroidManifest.xml; default only validates")
    args = argp.parse_args()
    try:
        print(patch_manifest(args.decoded_apk_dir / "AndroidManifest.xml", args.apply))
    except (ValueError, etree.XMLSyntaxError, OSError) as exc:
        print("BLOCKED:", exc, file=sys.stderr)
        return 2
    print("NOTE: KuSettings still handles this intent until disabled; DO NOT disable it until service,")
    print("explicit caller and factory reset checks in tvsettingsplus-mod/MIGRATION_AUDIT_RU.md pass.")
    print("NOTE: This patch does NOT transfer settings, ScreenServices, TimeService or OTA; it is route stage 1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
