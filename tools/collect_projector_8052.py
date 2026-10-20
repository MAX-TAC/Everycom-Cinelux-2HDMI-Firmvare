#!/usr/bin/env python3
"""Read-only ADB inventory for projector RUIOS 8052. Runs on an Android phone in Termux.
No su, no writes, no logcat, no bugreport, no APK/key dumps, no connected device names.
Only STDOUT from an explicitly bounded set of commands is retained.
"""
import argparse
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time
import zipfile
import shlex

SENSITIVE_KEY = re.compile(
    r"(?i)(serial|imei|meid|imsi|iccid|mac[_-]?addr|bssid|ssid|password|passwd|secret|"
    r"token|private[_-]?key|api[_-]?key|widevine|hdcp|uuid|unique[_-]?id|android[_-]?id|"
    r"device[_-]?id|bluetooth[_-]?name|host[_-]?name|wifi[_-]?password|wlan[_-]?mac)"
)
MAC = re.compile(r"\b(?:[0-9a-fA-F]{2}:){5}[0-9a-fA-F]{2}\b")
IPV4 = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
EMAIL = re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I)
ANDROID_ID = re.compile(r"(?i)(?:android[_-]?id|serial(?:no|number)?|imsi|imei|macaddr|bssid|ssid|ssid=|deviceaddr|btaddr)\s*[:=]\s*\S+")

ALLOW_PROPERTY = re.compile(
    r"^(ro\.(?:rjpj\.|product\.|build\.|vendor\.build\.|vendor\.product\.|"
    r"hardware(?:\.|$)|soc\.|sf\.|board\.|boot\.hardware|boot\.dtbo|"
    r"zeasn\.devicetype)|persist\.rjpj\.|persist\.(?:sys|vendor)\.(?:hdmi|display|projector|focus|keystone)\."
    r"|init\.svc\.(?:trd|mtk|tv|camera|tof|focus)|"
    r"persist\.(?:bluetooth|vendor\.bluetooth)\.(?:a2dp|le_audio|audio)|"
    r"bluetooth\.(?:a2dp|audio|le_audio))",
    re.I,
)
HARDWARE_WORDS = re.compile(r"(?i)(trd|rjpj|projector|mtk|mediatek|mstar|tof|motor|focus|i2c|"
                            r"keystone|hdmi|camera|video|audio|bluetooth|panel|display|drm|codec|cec|sensor)")
PACKAGE_WORDS = re.compile(r"(?i)(trd|rjpj|projector|tv\.settings|coolux|hysd|ku|factory|"
                           r"zeasn|mtk|mediatek|mstar|bluetooth|keystone|zxlauncher|zxstore|"
                           r"rui|provision|setupwizard|tcorrection|tvservices|television)")
DEVICE_LINE_UNSAFE = re.compile(r"(?i)(device\s*name|alias|paired devices|bonded devices|"
                                r"deviceaddress|maddress|remoteaddress|owner|account|ssid|bssid|"
                                r"bluetoothdevice\{|bluetoothdevice\(|name\s*[:=]|"
                                r"connected\s+devices?|paired\s+devices?|bonded\s+devices?|"
                                r"active\s+devices?|remote\s+devices?|mActiveDevice|mConnectedDevices)")

parser = argparse.ArgumentParser(description="Read-only projector OEM 8052 inventory via ADB/Termux")
parser.add_argument("--serial", help="ADB device selection, only if several ADB devices connected")
parser.add_argument("--out", help="Folder in Termux home (optional)")
args = parser.parse_args()
if shutil.which("adb") is None:
    sys.exit("Не найден adb. В Termux: pkg install android-tools")

listing = subprocess.run(["adb", "devices"], capture_output=True, text=True, timeout=15)
devices = [line.split()[0] for line in listing.stdout.splitlines()[1:]
           if len(line.split()) >= 2 and line.split()[1] == "device"]
if args.serial:
    if args.serial not in devices: sys.exit("Указанный --serial не подключён. Проверьте adb devices")
    serial = args.serial
elif len(devices) != 1:
    sys.exit("Нужен ровно один подключённый ADB-проектор. adb devices; либо запустите с --serial")
else:
    serial = devices[0]

stamp = dt.datetime.now().strftime("%Y%m%d_%H%M%S")
folder = Path(args.out).expanduser() if args.out else Path.home() / ("projector_8052_report_" + stamp)
folder.mkdir(parents=True, exist_ok=True)
errors = []
summary = {}


def clean(text):
    text = MAC.sub("[MAC REDACTED]", text)
    text = IPV4.sub("[IP REDACTED]", text)
    text = EMAIL.sub("[EMAIL REDACTED]", text)
    text = ANDROID_ID.sub("[DEVICE ID REDACTED]", text)
    return text.replace("\r", "")


def remote(command, key, timeout=25, max_bytes=1000000):
    """Run a fixed, read-only shell command. Never store stderr or unfiltered shell output."""
    try:
        p = subprocess.run(["adb", "-s", serial, "shell", "sh -c " + shlex.quote(command)],
                           capture_output=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        errors.append({"step": key, "issue": "timeout"})
        return ""
    if p.returncode != 0:
        errors.append({"step": key, "issue": "command_failed", "returncode": p.returncode})
    data = p.stdout[:max_bytes]
    if len(p.stdout) > max_bytes:
        errors.append({"step": key, "issue": "output_truncated"})
    return data.decode("utf-8", errors="replace")


def save(relative, text, max_lines=4000, max_len=500000):
    lines = [clean(line) for line in text.splitlines()[:max_lines]]
    body = "\n".join(lines)[:max_len] + "\n"
    path = folder / relative
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body, encoding="utf-8")
    summary[relative] = len(body.encode("utf-8"))
    print("[+]", relative, f"({len(body)} chars)", flush=True)


def selected_lines(text, regex, limit=250):
    rx = re.compile(regex, re.I)
    lines = []
    for line in text.splitlines():
        if rx.search(line) and not SENSITIVE_KEY.search(line) and not DEVICE_LINE_UNSAFE.search(line):
            lines.append(line[:350])
            if len(lines) >= limit: break
    return "\n".join(lines)


print("[*] Connected to ADB device; collecting read-only metadata...", flush=True)
raw = remote("getprop", "getprop", timeout=25)
props = {}
for line in raw.splitlines():
    m = re.match(r"^\[(.+?)\]:\s*\[(.*)\]$", line.strip())
    if not m: continue
    key, val = m.groups()
    if ALLOW_PROPERTY.search(key) and not SENSITIVE_KEY.search(key):
        if len(val) > 300 or SENSITIVE_KEY.search(val) or key.lower().endswith("wifi.id"): continue
        props[key] = clean(val)
save("01_identity/safe_getprop.txt", "\n".join(f"{k}={v}" for k,v in sorted(props.items())))
identity = {k: props.get(k, "not reported") for k in (
    "ro.rjpj.machine.id", "ro.rjpj.yunota.version", "ro.rjpj.hdmi.port.count",
    "ro.rjpj.hdmi.ports", "ro.rjpj.support.toffunction", "ro.product.board",
    "ro.product.model", "ro.build.version.release", "ro.build.version.incremental")}
(folder / "01_identity" / "identity.json").write_text(json.dumps(identity, indent=2, ensure_ascii=False) + "\n")
if props.get("ro.rjpj.machine.id") and props.get("ro.rjpj.machine.id") != "8052":
    print("[!] ВНИМАНИЕ: Проектор не сообщает ro.rjpj.machine.id=8052 — проверьте, то ли устройство!", flush=True)

read_commands = [
    ("02_system/kernel.txt", "uname -r; cat /proc/version", r".", 120),
    ("02_system/cpu.txt", "cat /proc/cpuinfo", r"processor|hardware|features|architecture|revision|implementer|variant|part|model", 100),
    ("02_system/memory.txt", "cat /proc/meminfo", r"^(MemTotal|MemFree|MemAvailable|SwapTotal|SwapFree|CmaTotal):", 30),
    ("02_system/modules.txt", "cat /proc/modules", r".", 1000),
    ("02_system/selinux_adb.txt", "id; getenforce; getprop ro.secure; getprop ro.debuggable; getprop ro.adb.secure", r".", 45),
    ("02_system/display.txt", "wm size; wm density; cat /sys/class/graphics/fb0/virtual_size", r".", 70),
    ("02_system/device_tree.txt", "for f in /proc/device-tree/model /proc/device-tree/compatible; do if [ -r \"$f\" ]; then echo \"$f\"; tr '\\000' ' ' < \"$f\"; echo; fi; done", r".", 25),
    ("03_hardware/device_nodes.txt", "ls -lZ /dev/i2c* /dev/video* /dev/tof* /dev/ruimotor* /dev/mtk* 2>/dev/null", r".", 200),
    ("03_hardware/i2c_devices.txt", "for f in /sys/bus/i2c/devices/*/name; do [ -r \"$f\" ] && { echo \"$f\"; cat \"$f\"; }; done", r".", 220),
    ("03_hardware/drm_connectors.txt", "for f in /sys/class/drm/*/status; do [ -r \"$f\" ] && { echo \"$f\"; cat \"$f\"; }; done", r".", 120),
    ("03_hardware/thermal_zones.txt", "for f in /sys/class/thermal/thermal_zone*/type; do [ -r \"$f\" ] && { echo \"$f\"; cat \"$f\"; }; done", r".", 130),
    ("03_hardware/mounted_oem_parts.txt", "mount", r"tvconfig|bootdata|tvservice|system|vendor|super|odm", 90),
    ("04_interfaces/binder_services.txt", "service list", r".", 500),
    ("04_interfaces/hidl_services.txt", "command -v lshal >/dev/null 2>&1 && lshal || true", r"vendor\.trd|mediatek|mstar|tof|motor|camera|hdmi|projector|tv", 130),
    ("04_interfaces/android_features.txt", "pm list features", r"bluetooth|television|leanback|camera|audio|usb|wifi|sensor|microphone|hdmi", 160),
    ("04_interfaces/settings_resolver.txt", "cmd package resolve-activity --brief -a android.settings.SETTINGS", r".", 30),
]
for path,cmd,rx,max_lines in read_commands:
    txt = remote(cmd, path, timeout=30)
    save(path, selected_lines(txt,rx,max_lines), max_lines=max_lines)

pkg_raw = remote("cmd package list packages -f", "packages", timeout=35)
pkgs = []
for line in pkg_raw.splitlines():
    if not line.startswith("package:"): continue
    pkg = line.rsplit("=", 1)[-1].strip() if "=" in line else line[8:].strip()
    if PACKAGE_WORDS.search(pkg) and not SENSITIVE_KEY.search(pkg):
        pkgs.append((pkg, line.replace("package:", "", 1)))
pkgs.sort()
save("04_interfaces/oem_packages.txt", "\n".join(f"{k} | {v}" for k, v in pkgs), 250)

TARGETS = [
    "com.android.tv.settings", "mediatek.factorymenu.ui", "com.hysd.screen",
    "com.rjpj.tcorrection", "com.coolux.source", "com.trd.framework",
    "com.trd.service", "com.my.settings", "com.android.bluetooth",
    "com.android.settings", "com.android.providers.settings",
]
seen = {k for k, _ in pkgs}
for pkg in TARGETS:
    if pkg not in seen: continue
    text = remote("dumpsys package " + shlex.quote(pkg), "package:" + pkg, timeout=28, max_bytes=1200000)
    selected = selected_lines(text,
         r"(versionName=|versionCode=|userId=|pkgFlags=|privateFlags=|"
         r"uses-permission:|permission\.|android\.permission\.|granted=|"
         r"android\.intent\.action\.|exported=|Activities:|Services:|Receivers:|"
         r"com\.trd\.|android\.settings|com\.rjpj\.|com\.mediatek\.|"
         r"com\.coolux\.|mediatek\.factory|com\.hysd\.|\b[a-zA-Z0-9._]+Activity\b|"
         r"\b[a-zA-Z0-9._]+Service\b)", 160)
    save("04_interfaces/package_details/" + pkg + ".txt", selected, 180)

# Current state, but intentionally do not include paired-device names, MACs or logs.
for title,cmd in [
    ("05_bluetooth/audio_policy_dumpsys.txt", "dumpsys media.audio_policy"),
    ("05_bluetooth/bluetooth_capabilities.txt", "dumpsys bluetooth_manager"),
]:
    text = remote(cmd, title, timeout=35, max_bytes=1400000)
    if "bluetooth_capabilities" in title:
        rx = r"A2DP|LE_Audio|LeAudio|offload|dual|multiple|simultaneous|max.*connect|audio routing|AudioProfile"
    else:
        rx = r"A2DP|BLE_HEADSET|BLUETOOTH|LE_AUDIO|mixport|audio output|routing|DevicePort|available output"
    filtered = selected_lines(text, rx, 100)
    if "bluetooth_capabilities" in title:
        # Capability terms only: do not share currently connected headset names.
        filtered = "\n".join(ln for ln in filtered.splitlines()
              if not re.search(r"(?i)(connected|paired|bonded|active\s*device|device\s*[:=]|alias|name\s*[:=])", ln))
    save(title, filtered, 110)

# Only stock public configuration, never device calibration, Wi-Fi DB, crypto keys or credentials.
audio_files = [
    "/vendor/etc/audio_policy_configuration.xml",
    "/vendor/etc/bluetooth_audio_policy_configuration.xml",
    "/vendor/etc/audio_policy_engine_configuration.xml",
    "/vendor/etc/audio_policy_engine_product_strategies.xml",
    "/vendor/etc/audio_policy_engine_criteria.xml",
    "/vendor/etc/audio_policy_engine_criterion_types.xml",
]
for path in audio_files:
    content = remote("cat " + shlex.quote(path), "audio_file:"+path, timeout=20, max_bytes=450000)
    if not content.strip(): continue
    safe_lines = [line for line in content.splitlines() if not SENSITIVE_KEY.search(line)]
    save("05_bluetooth/configs/"+path.rsplit("/", 1)[-1],"\n".join(safe_lines), 6500, 450000)

# Read-only inventory of firmware libraries. Do not copy vendor binaries.
libcheck = (
    'for f in /system/lib/libsettingsi2c_jni.so /system/lib/libfactoryi2c_jni.so '
    '/system/lib/libi2c_jni.so /system/lib/librjpj_private_function.so '
    '/system/lib/libtof_jni.so /system/lib/libtrd_jni.so '
    '/vendor/lib/modules/ruimotor.ko /vendor/lib/modules/stmvl53l1.ko; do '
    'if [ -r "$f" ]; then ls -l "$f"; sha256sum "$f"; fi; done'
)
save("03_hardware/oem_binary_hashes.txt", remote(libcheck, "oem_binary_hashes", timeout=45), 90)

# Some firmware mounts expose the partition as /tvconfig or /bootdata; never traverse data/user.
locate = ("for d in /tvconfig /bootdata /mnt/tvconfig /mnt/bootdata /mnt/vendor/tvconfig "
          "/mnt/vendor/bootdata /vendor/tvconfig /vendor/etc /odm/etc; do "
          "[ -d \"$d\" ] || continue; "
          "find \"$d\" -type f \\( -name board.ini -o -name dtbo_mapping.ini "
          "-o -name BasicSound_HDMI.ini -o -name ConfigDefaultValue.ini \\) 2>/dev/null; done")
found_text = remote(locate, "hardware_config_paths", timeout=38, max_bytes=80000)
paths = []
for line in found_text.splitlines():
    line = line.strip()
    if not line.startswith("/") or ".." in line or not re.search(r"/(?:board|dtbo_mapping|BasicSound_HDMI|ConfigDefaultValue)\.ini$", line):
        continue
    if line not in paths: paths.append(line)
paths = paths[:18]
save("03_hardware/oem_config_paths.txt", "\n".join(paths), 30)
for index,path in enumerate(paths):
    val = remote("cat " + shlex.quote(path), "config:"+path, timeout=22, max_bytes=310000)
    if val.strip():
        cleaned = "\n".join("[REDACTED]" if SENSITIVE_KEY.search(line) else line for line in val.splitlines())
        outfile = "03_hardware/configs/%02d_%s" % (index, path.rsplit("/", 1)[-1])
        save(outfile, "# Source: "+path+"\n"+cleaned, 5000, 285000)

metadata = {
    "profile_expected": "8052 / one HDMI",
    "device_reported_machine_id": props.get("ro.rjpj.machine.id", "not reported"),
    "created_date": dt.date.today().isoformat(),
    "privacy": "No serial numbers, MAC addresses, IPs, paired Bluetooth names, raw logs, accounts, APKs, keys or calibration are intended to be included.",
    "read_only": True,
    "root_used": False,
    "collected_files": summary,
    "error_steps": errors,
}
(folder / "REPORT_INDEX.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n")
(folder / "START_HERE.txt").write_text(
    "RUIOS 8052 / one HDMI — ADB diagnostic information.\n"
    "Commands are read-only; no firmware settings were changed.\n"
    "Check REPORT_INDEX.json for command failures and 01_identity/identity.json for project ID.\n"
    "Folder contains only selected diagnostic text, not bugreport/logcat, apps or calibration data.\n"
    "Please personally review the content before sharing to a public forum.\n", encoding="utf-8")

archive = folder.parent / (folder.name + ".zip")
with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=8) as z:
    for file in sorted(folder.rglob("*")):
        if file.is_file(): z.write(file, arcname=folder.name + "/" + file.relative_to(folder).as_posix())

print("\n[OK] Saved:", archive, flush=True)
print("[i] Steps with access/command problems:", len(errors), "(see REPORT_INDEX.json)", flush=True)
downloads = Path.home() / "storage" / "downloads"
if downloads.is_dir() and os.access(downloads, os.W_OK):
    dest = downloads / archive.name
    try:
        shutil.copy2(archive, dest)
        print("[OK] Copy in Android Downloads:", dest, flush=True)
    except OSError as ex:
        print("[!] Cannot copy to Downloads:", str(ex), flush=True)
else:
    print("[i] To share from Android Downloads: termux-setup-storage, then copy the ZIP from Termux home.", flush=True)
print("[i] Disconnect ADB and turn off wireless debugging when finished.", flush=True)