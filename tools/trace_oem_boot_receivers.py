#!/usr/bin/env python3
"""Find actual OEM boot receiver and background side-effect call sites.
Static Android 13 APK study only. Never publish decompiled source code.
"""
from pathlib import Path
import json,re,subprocess,shutil,collections
BASE=Path("/tmp/erofs")
OUT=Path("analysis/Global_Firmware_Map_20261021")
OUT.mkdir(exist_ok=True,parents=True)
APKS={
 "KuSettings":("system/system/app/KuSettings/KuSettings.apk",[
     "com/my/service/BootupReceiver.java","com/my/service/ScreenServices.java","com/my/settings/SettingActivity.java",
     "com/my/utils/IntentUtils.java"]),
 "TvSettingsPlus":("system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk",[
     "com/android/tv/settings/BootReceiver.java",
     "com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java",
     "com/android/tv/settings/partnercustomizer/utils/SoundEARCReceiver.java",
     "com/android/tv/settings/MainSettings.java",
     "com/android/tv/settings/uicustom/MainActivity.java"]),
 "KuSetupWizard":("system/system/app/KuSetupWizard/KuSetupWizard.apk",[
     "com/my/settings/wifi/ProvisionWifiActivity.java",
     "com/my/utils/IntentUtils.java"]),
 "trdservice":("system/system/app/trdservice/trdservice.apk",[
     "com/trd/service/communication/GlobalKeyEventProcess.java",
     "com/trd/service/TrdService.java"]),
}
ops=re.compile(r"\b(?:startService|startForegroundService|startActivity|sendBroadcast|registerReceiver|startActivityAsUser|setComponent|setClassName|setPackage|setAction|setEnabled|setComponentEnabledSetting|Settings\.(?:Secure|Global|System)|SystemProperties\.(?:get|set)|setProperty|exec|onReceive|onCreate|onStartCommand|onKeyDown|onKeyUp|getKeyCode|getSystemService|bindService|startTof|Set|set|android\.settings\.SETTINGS|android\.intent\.action\.BOOT_COMPLETED)\b")
SENSITIVE=re.compile(r"[A-Fa-f0-9]{20,}|https?://\S+|(?:ssid|mac|serial|uuid|token|password)[A-Za-z0-9_]*\s*=",re.I)
data={"source":"verified 8052.1.0.4 October OTA","files":{},"notes":[]}
for name,(rel,files) in APKS.items():
 apk=BASE/rel
 if not apk.is_file():data["notes"].append(name+" APK absent");continue
 work=Path("/tmp/boot-audit-"+name)
 r=subprocess.run(["/tmp/jadx-bin/bin/jadx","--no-res","--no-imports","--threads-count","3",
   "-d",str(work),str(apk)],capture_output=True,text=True,errors="replace",timeout=800)
 root=work/"sources"
 if not root.is_dir():data["notes"].append(name+": Jadx sources not recovered");continue
 selected={}
 for filename in files:
  file=root/filename
  if not file.is_file():
   matches=list(root.rglob(Path(filename).name))
   if len(matches)==1:file=matches[0]
  if not file.is_file():
   data["notes"].append(name+" missing source "+filename);continue
  src=file.read_text(errors="replace").splitlines()
  x=[]
  for i,line in enumerate(src,1):
   if not ops.search(line):continue
   if SENSITIVE.search(line):continue
   dispatch=sorted(set(m.group(0) for m in ops.finditer(line)))
   if not dispatch:continue
   # Do not publish original code lines; derive API, class and setting symbols only.
   identifiers=sorted(set(re.findall(r"[A-Z_a-z][\w$.]*",line)))
   relevant=[q for q in identifiers if re.search(r"Service|Settings|Receiver|Source|Focus|Key|TRD|OEM|android|Wifi|Bluetooth|Boot|TV|Projector|Audio|CEC|Mute|Brightness|Keystone|Properties",q,re.I)]
   method=re.search(r"\b(?:public|protected|private)\s+(?:static\s+|final\s+|synchronized\s+)*[\w<>[\].? ]+\s+([\w$]+)\s*\(",line)
   x.append({"line":i,"op":dispatch,"method_decl":method.group(1) if method else None,"identifiers":relevant[:14]})
  selected[file.relative_to(root).as_posix()]={"line_count":len(src),"markers":x[:190]}
 data["files"][name]=selected
 shutil.rmtree(work,ignore_errors=True)
 print("TRACE",name,"files",len(selected),"markers",sum(len(x["markers"]) for x in selected.values()),flush=True)
(OUT/"OEM_BOOT_RECEIVER_TRACE.json").write_text(json.dumps(data,indent=2,ensure_ascii=False)+"\n")
md=["# Обработчики BOOT_COMPLETED и служебная логика KuSettings / TvSettingsPlus / TRD","",
"Static JADX call markers only. A method name near a BOOT_COMPLETED receiver does **not** prove invocation without a full control-flow/data-flow trace.",
"Source: verified Oct OTA RUIOS.8052.1.0.4. No proprietary decompiled source exported.",
"",
"## Почему этот аудит нужен","",
"- \`KuSettings\` является отдельным OEM UI, но его манифест содержит \`com.my.service.BootupReceiver\` с BOOT_COMPLETED.",
"- \`TvSettingsPlus\` тоже содержит штатный \`BootReceiver\`, \`TvBootupReceiver\` и \`SoundEARCReceiver\`.",
"- \`KuSetupWizard\` похож на KuSettings в Java-коде, но имеет другое package identity и first-boot component.",
"- Для решения о полном удалении KuSettings нужно убедиться, что собственный receiver не запускает уникальные hardware services/TV initialization.",
"",
"## Извлечённые маркеры вызовов",""]
for app,files in data["files"].items():
 md+=["","## "+app,""]
 for name,one in files.items():
  md+=["","### "+name,"","Source lines: "+str(one["line_count"])]
  for line in one["markers"][:100]:
   if line["op"]:
    md.append("- "+str(line["line"])+": "+",".join(line["op"])+"; refs "+",".join(line["identifiers"][:6]))
md+=["","## Решения до полного удаления","",
"1. Использовать явный FLauncher shortcut на \`com.android.tv.settings/.MainSettings\`. Не полагаться на ACTION_SETTINGS, потому что этот Intent объявлен в KuSettings.",
"2. Нельзя автоматически удалять \`KuSettings\`, пока \`BootupReceiver\` и \`ScreenServices\` не проверены по фактическим веткам вызова.",
"3. Проверить индивидуальные preferences/global settings и linked service lifecycle после reboot/sleep.",
"4. Подписи всех основных проверенных OEM и AOSP приложений соответствуют AOSP platform test certificate — см. соседний SETTINGS_DISPATCH_8052_RU.md; это **не** AVB signing key.",
"5. Указанные методы и Java-классы совпадают для 8052 Oct и заводской 8054 Sep, если APK SHA совпадает; реально работающая 8054.1.0.4 ещё не изучена.",
""]
(OUT/"OEM_BOOT_RECEIVER_TRACE_RU.md").write_text("\n".join(md)+"\n")
