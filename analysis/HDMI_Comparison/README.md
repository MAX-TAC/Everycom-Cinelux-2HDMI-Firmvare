# Everycom CineLux 1 HDMI vs 2 HDMI: decrypted firmware comparison

Official firmware files were decrypted and inspected offline. No projectors were flashed.
One HDMI release: Original_Firmware_for_1_HDMI_ports (2026-08-13 filename)
Two HDMI release: Original_Firmware (2026-09-30 filename).

## Overall file comparison

| Metric | Value |
|---|---:|
| one_file_count | 3948 |
| two_file_count | 3956 |
| common_paths | 3944 |
| byte_identical_file_paths | 2267 |
| changed_common_paths | 1677 |
| only_in_one | 4 |
| only_in_two | 12 |
| common_identical_percent | 57.48 |

## Android logical partitions

| Partition | One HDMI size | Two HDMI size | Exact SHA256 match |
|---|---:|---:|---|
| product_a | 77152256 | 77152256 | NO |
| system_a | 683675648 | 866844672 | NO |
| system_ext_a | 87269376 | 87273472 | NO |
| vendor_a | 255242240 | 262610944 | NO |

## Other selected flashed partitions (whole-image SHA256)

| Partition | One HDMI size | Two HDMI size | Exact match |
|---|---:|---:|---|
| 3rd_a_a | 31457280 | 31457280 | NO |
| 3rd_rw | 31457280 | 31457280 | NO |
| armfw_a | 77088 | 77088 | YES |
| boot_a | 78643200 | 78643200 | NO |
| bootdata_a | 41943040 | 41943040 | NO |
| cache | 41036 | 41036 | NO |
| dtbo_a | 8388608 | 8388608 | NO |
| emmc_boot | 451840 | 451840 | NO |
| factory_a_a | 8388608 | 8388608 | NO |
| linux_rootfs_a_a | 57671680 | 57671680 | NO |
| mboot_a | 2657792 | 2658304 | NO |
| metadata | 16777216 | 16777216 | YES |
| optee_a | 2806432 | 2806432 | NO |
| persist | 20971520 | 20971520 | NO |
| private | 10485760 | 10485760 | NO |
| project_id | 5242880 | 5242880 | NO |
| trddev | 2097152 | 2097152 | YES |
| tvconfig_a | 157286400 | 157286400 | NO |
| tvservice_a | 175112192 | 175112192 | NO |
| vbmeta_a | 12288 | 12288 | NO |
| vbmeta_system_a | 4096 | 4096 | NO |

## Bootloader/GPT script comparison

GPT partition layout identical: True
Board flags identical: True
One-HDMI filepartload commands: 31, super fragments: 10
Two-HDMI filepartload commands: 33, super fragments: 12

### One HDMI boot flags
~~~
setenv verify n
setenv devicestate lock
setenv android_product griggs
setenv android_manufacturer Mediatek
setenv dtbo_cfg_sel config/dtb/mt5873_h1v1_cd.ini
addbootargs androidboot.selinux permissive
~~~
### Two HDMI boot flags
~~~
setenv verify n
setenv devicestate lock
setenv android_product griggs
setenv android_manufacturer Mediatek
setenv dtbo_cfg_sel config/dtb/mt5873_h1v1_cd.ini
addbootargs androidboot.selinux permissive
~~~

## Android build properties differing

| Property (partition:path:key) | 1 HDMI | 2 HDMI |
|---|---|---|
| system_a:system/build.prop:ro.build.date | Thu Aug 13 01:42:18 UTC 2026 | Wed Sep 30 07:41:37 UTC 2026 |
| system_a:system/build.prop:ro.build.display.id | mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.luzhih.20260813.014112 test-keys | mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.suhaix.20260930.074037 test-keys |
| system_a:system/build.prop:ro.build.version.incremental | eng.luzhih.20260813.014112 | eng.suhaix.20260930.074037 |
| vendor_a:build.prop:ro.vendor.build.fingerprint | MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys | MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys |

## APK packages

| Group | Count |
|---|---:|
| one_only | 1 |
| two_only | 4 |
| changed | 19 |
| identical | 65 |

### one_only

- system_ext_a/priv-app/Provision/Provision.apk

### two_only

- system_a/system/app/KuSetupWizard/KuSetupWizard.apk
- system_a/system/preinstall_del/AmazonPrimeVideo_v3.0.459.345.apk
- system_a/system/preinstall_del/Netfix_v8.110.0.apk
- system_a/system/preinstall_del/YouTube_v4.40.313.apk.apk

### changed

- system_a/system/apex/com.android.extservices/priv-app/ExtServices@TP1A.220624.021.A1/ExtServices.apk
- system_a/system/apex/com.android.mediaprovider/priv-app/MediaProvider@TP1A.220624.021.A1/MediaProvider.apk
- system_a/system/apex/com.android.tethering.inprocess/priv-app/InProcessTethering@TP1A.220624.021.A1/InProcessTethering.apk
- system_a/system/app/KuSettings/KuSettings.apk
- system_a/system/app/KuSourceRJ/KuSourceRJ.apk
- system_a/system/app/RuiAutoFocus/RuiAutoFocus.apk
- system_a/system/app/trdservice/trdservice.apk
- system_a/system/app/zxlauncher/zxlauncher.apk
- system_a/system/app/zxstore/zxstore.apk
- system_a/system/priv-app/InProcessNetworkStack/InProcessNetworkStack.apk
- system_a/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk
- system_a/system/priv-app/SettingsProvider/SettingsProvider.apk
- system_ext_a/app/AutoPair/AutoPair.apk
- system_ext_a/app/Factory/Factory.apk
- system_ext_a/app/WFDSinkTest/WFDSinkTest.apk
- system_ext_a/priv-app/LiveTV/LiveTV.apk
- system_ext_a/priv-app/MultiMediaPlayer/MultiMediaPlayer.apk
- system_ext_a/priv-app/TvServices/TvServices.apk
- system_ext_a/priv-app/TvSettingsPlus/TvSettingsPlus.apk

### identical

- product_a/app/Camera2/Camera2.apk
- product_a/app/LatinIME/LatinIME.apk
- product_a/app/ModuleMetadata/ModuleMetadata.apk
- product_a/app/VendorDisclaimer/VendorDisclaimer.apk
- product_a/app/WallpaperPicker/WallpaperPicker.apk
- product_a/app/webview/webview.apk
- system_a/system/apex/com.android.adservices/app/SdkSandbox@TP1A.220624.021.A1/SdkSandbox.apk
- system_a/system/apex/com.android.adservices/priv-app/AdServicesApk@TP1A.220624.021.A1/AdServicesApk.apk
- system_a/system/apex/com.android.btservices/app/Bluetooth@TP1A.220624.021.A1/Bluetooth.apk
- system_a/system/apex/com.android.ondevicepersonalization/app/OnDevicePersonalization@TP1A.220624.021.A1/OnDevicePersonalization.apk
- system_a/system/apex/com.android.permission/priv-app/PermissionController@TP1A.220624.021.A1/PermissionController.apk
- system_a/system/apex/com.android.permission/priv-app/SafetyCenterResources@TP1A.220624.021.A1/SafetyCenterResources.apk
- system_a/system/apex/com.android.tethering.inprocess/priv-app/ServiceConnectivityResources@TP1A.220624.021.A1/ServiceConnectivityResources.apk
- system_a/system/apex/com.android.uwb/priv-app/ServiceUwbResources@TP1A.220624.021.A1/ServiceUwbResources.apk
- system_a/system/apex/com.android.wifi/app/OsuLogin@TP1A.220624.021.A1/OsuLogin.apk
- system_a/system/apex/com.android.wifi/app/WifiDialog@TP1A.220624.021.A1/WifiDialog.apk
- system_a/system/apex/com.android.wifi/priv-app/ServiceWifiResources@TP1A.220624.021.A1/ServiceWifiResources.apk
- system_a/system/app/BasicDreams/BasicDreams.apk
- system_a/system/app/CertInstaller/CertInstaller.apk
- system_a/system/app/CompanionDeviceManager/CompanionDeviceManager.apk
- system_a/system/app/CtsShimPrebuilt/CtsShimPrebuilt.apk
- system_a/system/app/ExtShared/ExtShared.apk
- system_a/system/app/FTAirplayWireless/FTAirplayWireless.apk
- system_a/system/app/HTMLViewer/HTMLViewer.apk
- system_a/system/app/KeyChain/KeyChain.apk
- system_a/system/app/PacProcessor/PacProcessor.apk
- system_a/system/app/PlatformCaptivePortalLogin/PlatformCaptivePortalLogin.apk
- system_a/system/app/PrintSpooler/PrintSpooler.apk
- system_a/system/app/RJBluetoothSpeaker/RJBluetoothSpeaker.apk
- system_a/system/app/SecureElement/SecureElement.apk
- system_a/system/app/TrdDreamPic/TrdDreamPic.apk
- system_a/system/app/TrdFactoryTest/TrdFactoryTest.apk
- system_a/system/app/WallpaperBackup/WallpaperBackup.apk
- system_a/system/framework/framework-res.apk
- system_a/system/priv-app/BackupRestoreConfirmation/BackupRestoreConfirmation.apk
- system_a/system/priv-app/CalendarProvider/CalendarProvider.apk
- system_a/system/priv-app/ContactsProvider/ContactsProvider.apk
- system_a/system/priv-app/CtsShimPrivPrebuilt/CtsShimPrivPrebuilt.apk
- system_a/system/priv-app/DownloadProvider/DownloadProvider.apk
- system_a/system/priv-app/DynamicSystemInstallationService/DynamicSystemInstallationService.apk
- system_a/system/priv-app/ExternalStorageProvider/ExternalStorageProvider.apk
- system_a/system/priv-app/FusedLocation/FusedLocation.apk
- system_a/system/priv-app/InputDevices/InputDevices.apk
- system_a/system/priv-app/LocalTransport/LocalTransport.apk
- system_a/system/priv-app/MediaProviderLegacy/MediaProviderLegacy.apk
- system_a/system/priv-app/PackageInstaller/PackageInstaller.apk
- system_a/system/priv-app/ProxyHandler/ProxyHandler.apk
- system_a/system/priv-app/RuiYunOta/RuiYunOta.apk
- system_a/system/priv-app/SharedStorageBackup/SharedStorageBackup.apk
- system_a/system/priv-app/Shell/Shell.apk
- system_a/system/priv-app/SoundPicker/SoundPicker.apk
- system_a/system/priv-app/StatementService/StatementService.apk
- system_a/system/priv-app/TvProvider/TvProvider.apk
- system_a/system/priv-app/UserDictionaryProvider/UserDictionaryProvider.apk
- system_a/system/priv-app/VpnDialogs/VpnDialogs.apk
- system_ext_a/app/TvFrameworkPackageStubs/TvFrameworkPackageStubs.apk
- system_ext_a/priv-app/MtkNetworkMonitorService/MtkNetworkMonitorService.apk
- system_ext_a/priv-app/MtkTvInput/MtkTvInput.apk
- system_ext_a/priv-app/RemoteProvisioner/RemoteProvisioner.apk
- system_ext_a/priv-app/RetailDisplay/RetailDisplay.apk
- system_ext_a/priv-app/SystemUI/SystemUI.apk
- vendor_a/overlay/TetheringInprocessRROOverlay.apk
- vendor_a/overlay/TetheringRROOverlay.apk
- vendor_a/overlay/WifiRROOverlay.apk
- vendor_a/priv-app/trdmiddle/trdmiddle.apk

## Hardware and device service differences

Paths highlighted because they may matter for HDMI, autofocus, keystone, audio, vendor framework or boot safety.

### Only 1 HDMI (0 paths)


### Only 2 HDMI (2 paths)

- system_a/system/lib/libfactoryi2c_jni.so
- system_a/system/lib/libsettingsi2c_jni.so

### Files with changed hash (374 paths)

- product_a/lib/libmtkmtalservice_hwbinder_vendor.so
- product_a/lib/vendor.mediatek.tv.mtkmtalservice@1.0.so
- system_a/system/apex/com.android.btservices/lib/libbluetooth_jni.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.audio.common-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.audio.common@2.0.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.bluetooth.audio-V2-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.common-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.device-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.metadata-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.provider-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.rebootescrow-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.soundtrigger3-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.soundtrigger@2.0-core.so
- system_a/system/apex/com.android.vndk.current/lib/android.hardware.soundtrigger@2.0.so
- system_a/system/apex/com.android.vndk.current/lib/android.media.audio.common.types-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/android.media.soundtrigger.types-V1-ndk.so
- system_a/system/apex/com.android.vndk.current/lib/libaudioroute.so
- system_a/system/apex/com.android.vndk.current/lib/libaudioutils.so
- system_a/system/apex/com.android.vndk.current/lib/libcamera_metadata.so
- system_a/system/apex/com.android.vndk.current/lib/libmkbootimg_abi_check.so
- system_a/system/app/KuSettings/KuSettings.apk
- system_a/system/app/KuSettings/oat/arm/KuSettings.odex
- system_a/system/app/KuSettings/oat/arm/KuSettings.vdex
- system_a/system/app/KuSourceRJ/KuSourceRJ.apk
- system_a/system/app/KuSourceRJ/oat/arm/KuSourceRJ.odex
- system_a/system/app/KuSourceRJ/oat/arm/KuSourceRJ.vdex
- system_a/system/app/RuiAutoFocus/RuiAutoFocus.apk
- system_a/system/app/RuiAutoFocus/oat/arm/RuiAutoFocus.odex
- system_a/system/app/RuiAutoFocus/oat/arm/RuiAutoFocus.vdex
- system_a/system/app/trdservice/oat/arm/trdservice.odex
- system_a/system/app/trdservice/oat/arm/trdservice.vdex
- system_a/system/app/trdservice/trdservice.apk
- system_a/system/app/zxlauncher/oat/arm/zxlauncher.odex
- system_a/system/app/zxlauncher/oat/arm/zxlauncher.vdex
- system_a/system/app/zxlauncher/zxlauncher.apk
- system_a/system/bin/audioserver
- system_a/system/bin/bootanimation
- system_a/system/bin/bootctl
- system_a/system/bin/bootstat
- system_a/system/bin/bootstrap/linkerconfig
- system_a/system/bin/cameraserver
- system_a/system/bin/mtk_screenrecord
- system_a/system/bin/mtk_screenrecord_mr
- system_a/system/bin/reboot
- system_a/system/framework/oat/arm/apex@com.android.btservices@javalib@service-bluetooth.jar@classes.odex
- system_a/system/lib/aaudio-aidl-cpp.so
- system_a/system/lib/android.frameworks.cameraservice.common@2.0.so
- system_a/system/lib/android.frameworks.cameraservice.device@2.0.so
- system_a/system/lib/android.frameworks.cameraservice.device@2.1.so
- system_a/system/lib/android.frameworks.cameraservice.service@2.0.so
- system_a/system/lib/android.frameworks.cameraservice.service@2.1.so
- system_a/system/lib/android.frameworks.cameraservice.service@2.2.so
- system_a/system/lib/android.frameworks.displayservice@1.0.so
- system_a/system/lib/android.hardware.audio.common-V1-ndk.so
- system_a/system/lib/android.hardware.audio.common-util.so
- system_a/system/lib/android.hardware.audio.common@2.0.so
- system_a/system/lib/android.hardware.audio.common@4.0-util.so
- system_a/system/lib/android.hardware.audio.common@4.0.so
- system_a/system/lib/android.hardware.audio.common@5.0-util.so
- system_a/system/lib/android.hardware.audio.common@5.0.so
- system_a/system/lib/android.hardware.audio.common@6.0-util.so
- system_a/system/lib/android.hardware.audio.common@6.0.so
- system_a/system/lib/android.hardware.audio.effect@4.0-util.so
- system_a/system/lib/android.hardware.audio.effect@4.0.so
- system_a/system/lib/android.hardware.audio.effect@5.0-util.so
- system_a/system/lib/android.hardware.audio.effect@5.0.so
- system_a/system/lib/android.hardware.audio.effect@6.0-util.so
- system_a/system/lib/android.hardware.audio.effect@6.0.so
- system_a/system/lib/android.hardware.audio@4.0-util.so
- system_a/system/lib/android.hardware.audio@4.0.so
- system_a/system/lib/android.hardware.audio@5.0-util.so
- system_a/system/lib/android.hardware.audio@5.0.so
- system_a/system/lib/android.hardware.audio@6.0-util.so
- system_a/system/lib/android.hardware.audio@6.0.so
- system_a/system/lib/android.hardware.bluetooth.audio-V2-ndk.so
- system_a/system/lib/android.hardware.bluetooth.audio@2.0.so
- system_a/system/lib/android.hardware.bluetooth.audio@2.1.so
- system_a/system/lib/android.hardware.bluetooth@1.0.so
- system_a/system/lib/android.hardware.bluetooth@1.1.so
- system_a/system/lib/android.hardware.boot@1.0.so
- system_a/system/lib/android.hardware.boot@1.1.so
- system_a/system/lib/android.hardware.boot@1.2.so
- system_a/system/lib/android.hardware.camera.common-V1-ndk.so
- system_a/system/lib/android.hardware.camera.common@1.0.so
- system_a/system/lib/android.hardware.camera.device-V1-ndk.so
- system_a/system/lib/android.hardware.camera.device@1.0.so
- system_a/system/lib/android.hardware.camera.device@3.2.so
- system_a/system/lib/android.hardware.camera.device@3.3.so
- system_a/system/lib/android.hardware.camera.device@3.4.so
- system_a/system/lib/android.hardware.camera.device@3.5.so
- system_a/system/lib/android.hardware.camera.device@3.6.so
- system_a/system/lib/android.hardware.camera.device@3.7.so
- system_a/system/lib/android.hardware.camera.metadata-V1-ndk.so
- system_a/system/lib/android.hardware.camera.metadata@3.2.so
- system_a/system/lib/android.hardware.camera.metadata@3.3.so
- system_a/system/lib/android.hardware.camera.metadata@3.4.so
- system_a/system/lib/android.hardware.camera.metadata@3.5.so
- system_a/system/lib/android.hardware.camera.metadata@3.6.so
- system_a/system/lib/android.hardware.camera.provider-V1-ndk.so
- system_a/system/lib/android.hardware.camera.provider@2.4.so
- system_a/system/lib/android.hardware.camera.provider@2.5.so
- system_a/system/lib/android.hardware.camera.provider@2.6.so
- system_a/system/lib/android.hardware.camera.provider@2.7.so
- system_a/system/lib/android.media.audio.common.types-V1-cpp.so
- system_a/system/lib/android.media.audio.common.types-V1-ndk.so
- system_a/system/lib/audioclient-types-aidl-cpp.so
- system_a/system/lib/audioflinger-aidl-cpp.so
- system_a/system/lib/audiopolicy-aidl-cpp.so
- system_a/system/lib/audiopolicy-types-aidl-cpp.so
- system_a/system/lib/bootstrap/libc.so
- system_a/system/lib/bootstrap/libm.so
- system_a/system/lib/libaaudio.so
- system_a/system/lib/libaaudio_internal.so
- system_a/system/lib/libaaudioservice.so
- system_a/system/lib/libaudioclient.so
- system_a/system/lib/libaudioclient_aidl_conversion.so
- system_a/system/lib/libaudioeffect_jni.so
- system_a/system/lib/libaudioflinger.so
- system_a/system/lib/libaudiofoundation.so
- system_a/system/lib/libaudiohal.so
- system_a/system/lib/libaudiohal@4.0.so
- system_a/system/lib/libaudiohal@5.0.so
- system_a/system/lib/libaudiohal@6.0.so
- system_a/system/lib/libaudiohal@7.0.so
- system_a/system/lib/libaudiohal@7.1.so
- system_a/system/lib/libaudiohal_deathhandler.so
- system_a/system/lib/libaudiomanager.so
- system_a/system/lib/libaudiopolicy.so
- system_a/system/lib/libaudiopolicyengineconfigurable.so
- system_a/system/lib/libaudiopolicyenginedefault.so
- system_a/system/lib/libaudiopolicymanagercustom.so
- system_a/system/lib/libaudiopolicymanagerdefault.so
- system_a/system/lib/libaudiopolicyservice.so
- system_a/system/lib/libaudioprocessing.so
- system_a/system/lib/libaudiospdif.so
- system_a/system/lib/libaudioutils.so
- system_a/system/lib/libbootanimation.so
- system_a/system/lib/libbootloader_message.so
- system_a/system/lib/libcamera2ndk.so
- system_a/system/lib/libcamera_client.so
- system_a/system/lib/libcamera_metadata.so
- system_a/system/lib/libcameraservice.so
- system_a/system/lib/libdatasource.so
- system_a/system/lib/libdisplayservicehidl.so
- system_a/system/lib/libext2_quota.so
- system_a/system/lib/libmtkscreenrecord.so
- system_a/system/lib/libmtkvoc.so
- system_a/system/lib/libnativedisplay.so
- system_a/system/lib/libresourcemanagerservice.so
- system_a/system/lib/libsoundpool.so
- system_a/system/lib/libtrdclient.so
- system_a/system/lib/mstar.hardware.imgdisp@1.0.so
- system_a/system/lib/mstar.hardware.imghwdec@1.0.so
- system_a/system/lib/mstar.hardware.intertunnel@1.0.so
- system_a/system/lib/vendor.mediatek.tv.mtktvvoc@1.0.so
- system_a/system/lib/vendor.trd.hardware.hwtrd@1.0.so
- system_a/system/lib/vendor.trd.hardware.tof@1.0.so
- system_a/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk
- system_a/system/priv-app/SettingsProvider/SettingsProvider.apk
- system_a/system/priv-app/SettingsProvider/oat/arm/SettingsProvider.odex
- system_a/system/priv-app/SettingsProvider/oat/arm/SettingsProvider.vdex
- system_ext_a/app/Factory/Factory.apk
- system_ext_a/lib/libmtkcmpb.so
- system_ext_a/lib/libmtkrm_hwbinder.so
- system_ext_a/lib/vendor.mediatek.api.mtktvapi@1.0.so
- system_ext_a/lib/vendor.mediatek.custom.mtktvapicustom@1.0.so
- system_ext_a/lib/vendor.mediatek.tv.mtkcalman@1.0.so
- system_ext_a/lib/vendor.mediatek.tv.mtkdmservice@1.0.so
- system_ext_a/lib/vendor.mediatek.tv.mtkmtalservice@1.0.so
- system_ext_a/lib/vendor.mediatek.tv.mtkrm@1.0.so
(204 additional changed paths in JSON)

## Completeness and warnings

Identical file hash means byte-for-byte identical; differing hash does not necessarily mean different behavior.
Different builds can contain changed timestamps, build fingerprints and identical-function recompiles.
Hardware equivalence and HDMI port routing require live testing, device tree and driver analysis.
Manufacturer PKG encryption key enables extraction but not automatically valid signing or safe flashing.
The raw file inventory used for comparison is retained as GitHub Actions artifacts, not committed to Git.

