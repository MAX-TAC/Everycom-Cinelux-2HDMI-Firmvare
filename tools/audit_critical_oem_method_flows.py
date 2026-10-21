#!/usr/bin/env python3
"""Targeted static behavioral inventory of OEM Settings and first-boot control paths.
Produces a sequence of known method-call/condition markers, not decompiled OEM code.
Never calls any firmware function or modifies settings.
"""
from pathlib import Path
import collections,json,re,subprocess,shutil
BASE=Path("/tmp/erofs")
OUT=Path("analysis/Settings_Wizard_Debloat_20261021")
OUT.mkdir(parents=True,exist_ok=True)
TARGETS={
"KuSetupWizard":("system/system/app/KuSetupWizard/KuSetupWizard.apk",{
 "com/my/settings/wifi/ProvisionWifiActivity.java":["next","onCreate","onBackPressed","dispatchKeyEvent"],
 "com/my/settings/bluetooth/ProvisionBluetoothActivity.java":["next","onCreate","onBackPressed","dispatchKeyEvent"],
 "com/my/service/BootupReceiver.java":["onReceive"],
 "com/my/utils/IntentUtils.java":["provisionWifiIntent","provisionBluetoothIntent","provisionMenuIntent","myWifi","startOta"]
}),
"KuSettings":("system/system/app/KuSettings/KuSettings.apk",{
 "com/my/service/BootupReceiver.java":["onReceive"],
 "com/my/service/ScreenServices.java":["onStartCommand","setKeyStore","takeScreenShot","startShot"],
 "com/my/service/MySetTimeService.java":["onStartCommand","registerTimeTick"],
 "com/my/settings/SettingActivity.java":["onCreate","enterClick","onDestroy"],
 "com/my/utils/IntentUtils.java":["startOta","imageDigitalIntent","keystoneIntent","bootSoure","poweron","startUniversalKJ"]
}),
"TvSettingsPlus":("system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk",{
 "com/android/tv/settings/MainSettings.java":["createSettingsFragment"],
 "com/android/tv/settings/MainFragment.java":["onCreatePreferences","onPreferenceTreeClick"],
 "com/android/tv/settings/uicustom/MainActivity.java":["onCreate","onKeyDown","initPageManager"],
 "com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java":["setPowerOnAutoFocus","setMoveAutoFocus","setAccurateFocus"],
 "com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java":["resetFactoryCalibrationData","startFactoryCalib","saveFactoryCalibrationData","checkFactoryData"],
 "com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java":["startAutoFocus","startAutoKeystone","resetTrapezoid","jumpActivityByAction"],
 "com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java":["initBoardConfig","validateEdidVersion","updateEdidEnableState","checkBluetoothSpeakerPackage","switchToHDMI","switchToAV","switchToUSB"],
 "com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java":["onReceive"],
 "com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java":["onCreate","onDestroy","updateWirelessSpeakerService"],
 "com/android/tv/settings/partnercustomizer/utils/SoundEARCReceiver.java":["onReceive","updateEARCSettingValueToDrive"]
})}
HEAD=re.compile(r"(?m)^\s*(?:(?:public|private|protected|static|final|synchronized|native)\s+){1,5}[\w<>\[\]$.?, ]+?\s+([A-Za-z_$][\w$]*)\s*\([^;{}]*?\)\s*(?:throws\s+[\w., ]+)?\{")
OPS={
 "intent":r"startActivity(?:AsUser)?|startService|setComponent|setClassName|setAction|sendBroadcast|finish[(]",
 "property_read":r"SystemProperties[.]get|Settings[.](?:Global|Secure|System)[.]get",
 "property_write":r"SystemProperties[.]set|Settings[.](?:Global|Secure|System)[.]put",
 "binder_hal":r"IProjectorCtrl|TrdSystemManager|ProjectorManager|ITofCtrl|I2CDevice|MotorJNI|MtkTv|MtkTvInput",
 "destructive":r"resetFactoryCalibrationData|clearAllCalibrationFiles|delete[(]|deleteFile|format[(]|resetKeyStone|resetTrapezoid",
 "lifecycle":r"registerReceiver|unregisterReceiver|bindService|unbindService",
 "errors":r"throw\s+|printStackTrace|Log[.][ew][(]|catch\s*[(]",
 "steps":r"Thread[.]sleep|Handler[.]post|CountDownTimer|finish[(]|setResult[(]",
 "thirdparty":r"com[.]my[.]settings|com[.]coolux[.]source|com[.]android[.]tv[.]settings|com[.]hysd[.]screen|com[.]rjpj[.]yunota"
}
RX={k:re.compile(v) for k,v in OPS.items()}
# Stable public names used in settings/property values; do not dump all quoted strings.
KEYS=re.compile(r'(?:persist[.][a-zA-Z0-9_.-]+|ro[.]rjpj[.][a-zA-Z0-9_.-]+|android[.]settings[.][A-Z_]+|android[.]intent[.][A-Z_.]+|KEY_[A-Z_]+|DEVICE_PROVISIONED|USER_SETUP_COMPLETE|WIFI_[A-Z_]+|BLUETOOTH_[A-Z_]+)')
results={"source":"verified Oct 8052.1.0.4 OTA","targets":{},"limitations":[
 "JADX source is reconstructed; method boundaries are approximate.",
 "Do not infer runtime invocation from static method content.",
 "AOSP Android 13 stock base tag not proven to be OEM's actual fork.",
 "No branch is a confirmed bug without reproducible behavior and logs."]}
for app,(rel,mapping) in TARGETS.items():
 apk=BASE/rel
 assert apk.exists(),str(apk)
 dst=Path("/tmp/critical-jadx-"+app)
 run=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3","-d",str(dst),str(apk)],capture_output=True,text=True,errors="replace",timeout=960)
 root=dst/"sources"
 assert root.is_dir(),app+" failed decompile"
 listed={}
 for source,methods in mapping.items():
  f=root/source
  if not f.exists():
   listed[source]={"missing":True};continue
  raw=f.read_text(errors="replace")
  method_matches=list(HEAD.finditer(raw))
  outputs=[]
  for wanted in methods:
   possible=[m for m in method_matches if m.group(1)==wanted]
   for found in possible[:4]:
    start=found.end()
    depth=1;idx=start
    while idx<len(raw) and depth>0:
     c=raw[idx]
     if c=="{":depth+=1
     elif c=="}":depth-=1
     idx+=1
    if depth>0:continue
    body=raw[start:idx-1]
    linenum=raw[:found.start()].count("\n")+1
    cnt={k:len(rx.findall(body)) for k,rx in RX.items()}
    keys=sorted(set(KEYS.findall(body)))[:60]
    # summary only, no source
    outputs.append({"method":wanted,"start_line":linenum,"bytes":len(body),
       "branches":{"if":len(re.findall(r"\bif\s*[(]",body)),"switch":len(re.findall(r"\bswitch\s*[(]",body)),
                   "try":len(re.findall(r"\btry\s*\{",body)),"catch":len(re.findall(r"\bcatch\s*[(]",body))},
       "call_indicators":{k:v for k,v in cnt.items() if v},"public_keys":keys,
       "called_public_api_tokens":sorted(set(m.group(0) for rx in RX.values() for m in rx.finditer(body)))[:35]})
  listed[source]={"methods":outputs,"requested":methods,"missing_methods":sorted(set(methods)-set(x["method"] for x in outputs))}
 results["targets"][app]=listed
 shutil.rmtree(dst,ignore_errors=True)
 print("APP",app,"summarized",sum(len(x.get("methods",[])) for x in listed.values()),flush=True)
(OUT/"critical_method_flow_indicators.json").write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
lines=["# Critical OEM Settings / Setup Wizard static control-flow indicators","",
"Verified source: October 8052.1.0.4. The equivalent APKs in **factory 8054.1.0.1** have identical SHA, except those previously documented as differing. This file is not a comparison to a current 8054.1.0.4 firmware.",
"",
"**This is a guided static review, not verified bug reproduction.** Each method has approximate counts of branches and exact names of side-effect APIs; there are no decompiled bodies in this report.",
""]
for app,files in results["targets"].items():
 lines+=["","## "+app,""]
 for file,v in files.items():
  lines+=["","### "+file,""]
  if v.get("missing"):lines.append("Source absent");continue
  if v.get("missing_methods"):lines.append("Not decompiled/recognized: "+", ".join(v["missing_methods"]))
  for x in v["methods"]:
   lines+=["- \`"+x["method"]+"()\` at JADX line "+str(x["start_line"])+
     ": branches "+str(x["branches"])+", signals "+str(x["call_indicators"])+
     ", keys "+", ".join(x["public_keys"][:20])]
lines+=["","## Practical interpretation","",
"- \`KuSetupWizard\`: inspect \`ProvisionWifiActivity.next\` and \`ProvisionBluetoothActivity.next\` for how first-run flow is terminated and which service marks provisioning complete; do not remove from factory reset path based on duplicated library code.",
"- \`KuSettings\`: inspect \`ScreenServices\` system property writes and screenshot service access, plus time service and boot receiver. These can be retained in an adapter or omitted only after proving unused.",
"- \`TvSettingsPlus\`: preserve \`KeystoneCalibrationActivity\` factory parameters and confirmation guards; never invoke factory resets automatically.",
"- \`SourceSubMenuController\` depends on board config and Android Settings.Global; never expose a nonexistent second HDMI on 8052.",
"- \`WirelessSpeakerServices\` starts on boot and should be checked for Bluetooth receiver mode; do not confuse it with A2DP output.",
"- \`SoundEARCReceiver\` syncs Settings.Global to TV audio control: retain until confirmed not required.",
"- Error log/printStackTrace is not a bug by itself; review whether failure updates UI or leaves a stale state.",
"- No Android app or hardware controls were executed or altered.",
""]
(OUT/"CRITICAL_METHOD_FLOWS_RU.md").write_text("\n".join(lines)+"\n")
