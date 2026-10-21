#!/usr/bin/env python3
"""Assemble a non-flashable signed-APK + explicit-overlay staging ZIP for a known
RUIOS 8052/8054 *source tree*. Do not edit, sign, or generate partition images.
All selected removals are explicit, auditable, and scoped to Android SYSTEM.
"""
import argparse,hashlib,json,subprocess,zipfile,datetime,re,os
from pathlib import Path

PROFILES={
"8052":{
  "version":"RUIOS.8052.1.0.4 (October verified OTA)",
  "system_dir":"system",
  "sys_prefix":"system",
  "ext_dir":"system_ext",
  "removals":["system/app/zxlauncher/zxlauncher.apk","system/app/zxstore/zxstore.apk"],
  "retain":["system/app/KuSetupWizard/KuSetupWizard.apk","system/app/KuSettings/KuSettings.apk",
            "system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk"],
  "target_hdmi_ports":1,
  "notes":["Vendor is not included or modified.","Netflix / Prime / YouTube might be present in userdata even when absent from current OTA.","KuSettings stays until its system service dependencies are validated."]
},
"8054":{
  "version":"RUIOS.8054.1.0.1 (September verified factory PKG; not claimed latest OTA)",
  "system_dir":"system_a",
  "sys_prefix":"system",
  "ext_dir":"system_ext_a",
  "removals":["system/app/zxlauncher/zxlauncher.apk","system/app/zxstore/zxstore.apk",
              "system/preinstall_del/Netfix_v8.110.0.apk",
              "system/preinstall_del/AmazonPrimeVideo_v3.0.459.345.apk"],
  "retain":["system/app/KuSetupWizard/KuSetupWizard.apk","system/app/KuSettings/KuSettings.apk",
            "system/preinstall_del/YouTube_v4.40.313.apk.apk",
            "system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk"],
  "target_hdmi_ports":2,
  "notes":["Unmodified board-specific vendor/TVservice/kernel/DTBO remain stock.","KuSettings stays until system service removal is proven safe.","The source is September 8054.1.0.1, not a rumored 8054.1.0.4."]
}}
def digest(path):
 h=hashlib.sha256()
 with open(path,"rb") as fd:
  for buf in iter(lambda:fd.read(1024*1024),b""):h.update(buf)
 return h.hexdigest()
def checked_apk(path,expected_package):
 assert zipfile.is_zipfile(path),f"Not a zip/APK: {path}"
 info=subprocess.run(["aapt","dump","badging",str(path)],capture_output=True,text=True,errors="replace",timeout=40)
 assert info.returncode==0,info.stderr
 pack=re.search(r"package: name='([^']+)'",info.stdout)
 assert pack and pack.group(1)==expected_package,(path,pack.group(1) if pack else info.stdout[:200],expected_package)
 sdk=re.search(r"sdkVersion:'(\d+)'",info.stdout)
 assert not sdk or int(sdk.group(1))<=33,f"{path} requires API {sdk.group(1)}; device is Android 13/API33"
 return {"package":pack.group(1),"sha256":digest(path),"bytes":path.stat().st_size}
def main():
 p=argparse.ArgumentParser()
 p.add_argument("--variant",choices=PROFILES,required=True)
 p.add_argument("--source",type=Path,required=True,help="EROFS extracted root, containing system and system_ext logical partitions")
 p.add_argument("--flauncher",type=Path,required=True)
 p.add_argument("--shortcut",type=Path,required=True)
 p.add_argument("--dest",type=Path,required=True)
 args=p.parse_args()
 cfg=PROFILES[args.variant];source=args.source.resolve();dest=args.dest.resolve()
 assert source.is_dir(),"Missing extracted source tree"
 # "/system" path inside extracted image may be nested under extracted partition name.
 mappings={
  "system":source/cfg["system_dir"]/"system",
  "system_ext":source/cfg["ext_dir"]
 }
 assert mappings["system"].is_dir(),f"Missing {mappings['system']}"
 assert mappings["system_ext"].is_dir(),f"Missing {mappings['system_ext']}"
 def absolute(logical):
  part=logical.split("/",1)[0];sub=logical.split("/",1)[1]
  return mappings[part]/sub
 for item in cfg["removals"]+cfg["retain"]:
  assert absolute(item).is_file(),f"BLOCKED: expected stock APK absent: {item} -> {absolute(item)}"
 fl=checked_apk(args.flauncher,"me.efesser.flauncher")
 sc=checked_apk(args.shortcut,"org.cinelux.settingsshortcut")
 checked={}
 for path in cfg["removals"]+cfg["retain"]:
  p=absolute(path);checked[path]={"sha256":digest(p),"bytes":p.stat().st_size}
 # Native libs compressed can be unsupported by an installed system app with extractNativeLibs false:
 # we expose evidence and keep unsigned img generation blocked until target runtime check.
 with zipfile.ZipFile(args.flauncher) as z:
  native=[{"name":x.filename,"method":x.compress_type,"bytes":x.file_size} for x in z.infolist() if x.filename.startswith("lib/") and x.filename.endswith(".so")]
 archive=dest/f"CineLux-Custom-v0-{args.variant}-STAGING-NOT-FLASHABLE.zip"
 dest.mkdir(parents=True,exist_ok=True)
 additions={
 "system/app/FLauncher/FLauncher.apk":args.flauncher,
 "system/app/CineLuxSettingsShortcut/CineLuxSettingsShortcut.apk":args.shortcut
 }
 manifest={
  "bundle_kind":"overlay-delta-APK-STAGING-NOT-FLASHABLE",
  "variant":args.variant,"baseline":cfg["version"],"hdmi_port_count":cfg["target_hdmi_ports"],
  "minimum_android_api":33,"files_to_remove":cfg["removals"],
  "files_to_keep":cfg["retain"],"stock_files_verified":checked,
  "files_to_add":{p:{"sha256":digest(v),"size":v.stat().st_size} for p,v in additions.items()},
  "flauncher":fl,"shortcut":sc,"flauncher_native_libraries":native,
  "android_settings_component":"com.android.tv.settings/.MainSettings",
  "projector_settings_component":"com.android.tv.settings/.uicustom.MainActivity",
  "preserve_hardware":["vendor","dtbo","boot","vbmeta","tvconfig","tvservice","PMU","factory","persist"],
  "status":"NOT_INSTALLED; NO IMG/PKG/BIN; Android system overlays only",
  "notes":cfg["notes"],
  "blockers":["Target signature/AVB constraints unresolved.",
              "Boot/root fallback HOME has not been tested on real 8052 and 8054.",
              "May require unpacked Flutter native libraries and signed APK compatibility depending on manifest.",
              "System partition size, SELinux xattrs, uid/gid and preinstall_del semantics not validated.",
              "No partition filesystem regenerated to avoid invalid SELinux labels and OTA signatures."]
 }
 notice=("НЕ ПРОШИВАТЬ! / DO NOT FLASH\n"
 "Этот ZIP НЕ является прошивкой, OTA-пакетом или установщиком.\n"
 "Содержит готовые APK и проверенные списки изменений для указанных stock Android разделов.\n"
 "Образы system.img, super.img, PKG, BIN, OTA payload не сформированы.\n"
 "Не менять boot/vendor/tvservice/калибровки. KuSetupWizard и KuSettings пока сохранены.\n"
 "Оставить первоначальный HOME как аварийный fallback до живых испытаний; "
 "пакет описывает план исключения OEM HOME только на следующей стадии применения.\n")
 with zipfile.ZipFile(archive,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=6) as z:
  z.writestr("README_NOT_FLASHABLE_RU.txt",notice)
  z.writestr("manifest.json",json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
  z.writestr("REMOVALS.txt","\n".join(cfg["removals"])+"\n")
  for name,file in additions.items():z.write(file,"overlay/"+name)
 assert zipfile.is_zipfile(archive)
 with zipfile.ZipFile(archive) as z:
  for name,file in additions.items():
   assert hashlib.sha256(z.read("overlay/"+name)).hexdigest()==digest(file)
 (dest/f"{args.variant}_build_manifest.json").write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+"\n")
 print(json.dumps({"variant":args.variant,"archive":str(archive),"zip_sha256":digest(archive),
    "archive_bytes":archive.stat().st_size,"remove":cfg["removals"],"retained":cfg["retain"],
    "native_lib_count":len(native)},ensure_ascii=False,indent=2))
if __name__=="__main__":main()
