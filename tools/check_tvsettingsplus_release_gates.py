#!/usr/bin/env python3
"""Fail-closed release gate for any future KuSettings disable operation.

Default: prints status and returns 0.
--require-ready: returns 2 until ALL required checks have verifiable done:true
and tested variants are marked as passed. Does not make Android changes.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

def check_gates(data: dict) -> list[str]:
    errors = []
    if data.get("schema") != 1:
        errors.append("unsupported gate schema")
    if data.get("disable_kusettings_allowed") is not True:
        errors.append("KuSettings disable NOT authorized in release_gates.json")
    for row in data.get("requirements", []):
        if row.get("required") and row.get("done") is not True:
            errors.append(f"{row.get('id')}: {row.get('reason', 'not verified')}")
    for variant, row in data.get("device_profiles", {}).items():
        if row.get("live_target_upgrade_test") is not True:
            errors.append(f"{variant}: updated TvSettingsPlus not tested on real hardware")
        if variant == "8054" and row.get("current_running_rom_apk_verified") is not True:
            errors.append("8054: current installed TvSettingsPlus.apk not verified")
    for flag in ["compiled", "signed", "installed"]:
        if data.get("mod_apk", {}).get(flag) is not True:
            errors.append(f"mod_apk.{flag} not verified")
    if not data.get("requirements"):
        errors.append("missing requirements list")
    return errors

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=Path("tvsettingsplus-mod/release_gates.json"))
    parser.add_argument("--require-ready", action="store_true")
    args = parser.parse_args()
    data = json.loads(args.manifest.read_text(encoding="utf-8"))
    errors = check_gates(data)
    if errors:
        print("BLOCKED: cannot disable KuSettings until every gate passes:")
        for item in errors:
            print(" - " + item)
        return 2 if args.require_ready else 0
    print("All specified release gates passed (requires separate physical verification).")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
