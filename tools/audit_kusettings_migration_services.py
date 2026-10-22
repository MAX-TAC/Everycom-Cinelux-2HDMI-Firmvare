#!/usr/bin/env python3
"""Summarize call sites of four OEM packages from locally decompiled verified APKs.
Does not publish decompiled Java or run anything on a projector.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

TARGETS = {
 "KuSettings": {
  "com/my/service/BootupReceiver.java": ["onReceive"],
  "com/my/service/MySetTimeService.java": ["onStartCommand", "registerTimeTick"],
  "com/my/service/ScreenServices.java": ["onStartCommand", "setKeyStore", "startShot", "takeScreenShot", "handleMessage"],
  "com/my/utils/IntentUtils.java": [
   "startMyTimeService", "startSourceService", "startSourceTimeService", "startTime",
   "myWifi", "myBluetooth", "autoBluetooth", "myDateTime", "myLanguage", "languageLocal", "timeZone",
   "screenshot", "projectAbout", "brightIntent", "voiceIntent", "startOta", "restoreIntent",
   "bootSoure", "poweron", "projectModel", "mircastIntent", "airplayIntent",
   "keystoneIntent", "imageDigitalIntent", "startUniversalKJ",
   "provisionBluetoothIntent", "provisionWifiIntent"
  ]
 },
 "KuSetupWizard": {"com/my/utils/IntentUtils.java": [
  "startMyTimeService", "startSourceService", "startSourceTimeService",
  "myWifi", "myBluetooth", "provisionBluetoothIntent", "provisionWifiIntent", "screenshot"
 ]},
 "KuSourceRJ": {
  "com/coolux/source/service/BootupReceiver.java": ["onReceive"],
  "com/coolux/source/service/TimeService.java": ["onCreate", "onStartCommand"],
  "com/coolux/source/utils/IntentUtils.java": ["startTime"]
 },
 "TvSettingsPlus": {
  "com/android/tv/settings/BootReceiver.java": ["onReceive"],
  "com/android/tv/settings/MainSettings.java": ["createSettingsFragment"]
 }
}
OPERATIONS = (
 "startService", "startForegroundService", "bindService", "stopService",
 "registerReceiver", "startActivity", "setComponent", "setClassName",
 "SystemProperties.set", "Settings.Global", "Settings.Secure",
 "sendBroadcast", "startShot", "takeScreenShot", "getAction", "getStringExtra", "putExtra"
)
TARGET_LITERALS = re.compile(
 r"com\.(?:coolux\.source|my\.settings|android\.systemui|android\.tv\.settings|rjpj\.yunota)[A-Za-z0-9_.$/]*"
 r"|android\.settings\.[A-Z_]+|android\.intent\.action\.[A-Z_]+"
 r"|TIME_TICK|BOOT_COMPLETED"
 r"|(?:persist|ro|sys|service|vendor)\\.[A-Za-z0-9_.-]+"
)

def method_text(src: str, name: str) -> str | None:
    m = re.search(r"\b" + re.escape(name) + r"\s*\([^;{}]*\)\s*(?:throws\s+[^{]+)?\{", src)
    if m is None:
        return None
    depth, end = 1, m.end()
    while end < len(src) and depth:
        if src[end] == "{": depth += 1
        elif src[end] == "}": depth -= 1
        end += 1
    return src[m.start():end] if depth == 0 else None

def audit(root: Path) -> dict:
    result = {}
    for app, files in TARGETS.items():
        result[app] = {}
        for name, methods in files.items():
            found = list((root / app).rglob(name))
            if len(found) != 1:
                result[app][name] = {"status": "missing/ambiguous", "methods": {}}
                continue
            src = found[0].read_text(encoding="utf-8", errors="replace")
            details = {}
            for method in methods:
                body = method_text(src, method)
                details[method] = {
                    "found": body is not None,
                    "calls": {key: body.count(key) for key in OPERATIONS if body and key in body},
                    "known_component_or_action_strings": sorted(set(TARGET_LITERALS.findall(body)))[:50] if body else []
                }
            result[app][name] = {"status": "analyzed", "methods": details}
    return result

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--jadx", type=Path, required=True)
    ap.add_argument("--out", type=Path, required=True)
    args = ap.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    report = audit(args.jadx)
    (args.out / "kusettings_service_calls.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False)+"\n", encoding="utf-8")
    lines = ["# OEM службы — дополнительные маркеры вызовов", "",
             "Статический JADX-анализ оригинальной OTA 8052.1.0.4. Это НЕ runtime тест.", ""]
    missing = []
    for app, files in report.items():
        lines += ["## "+app, ""]
        for name, entry in files.items():
            lines += ["### "+name, "Status: "+entry["status"]]
            if entry["status"] != "analyzed": missing.append(app+"/"+name)
            for m, record in entry["methods"].items():
                lines.append("- "+m+": "+("found" if record["found"] else "missing")+
                   "; API: "+str(record["calls"])+
                   "; contracts: "+", ".join(record["known_component_or_action_strings"]))
            lines.append("")
    lines += ["Missing decompiled source: "+str(missing), "",
              "Не отключать KuSettings, пока не сопоставлены все явные и неявные вызовы,",
              "а поведение BootupReceiver/ScreenServices/TimeService не замещено или признано ненужным."]
    (args.out / "kusettings_service_calls_RU.md").write_text("\n".join(lines)+"\n", encoding="utf-8")
    print("Audited", len(report), "packages;", len(missing), "missing files")
    return 2 if missing else 0

if __name__ == "__main__":
    raise SystemExit(main())
