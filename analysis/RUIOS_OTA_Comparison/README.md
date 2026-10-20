# RUIOS 8052 vs 8053 reconstructed Android OTA

8052 = 2026-10-12 eng.suhaix.20261012.025220, 8053 = 2026-06-12 eng.luzhih.20260612.083454.

Common Android file paths: 3941
Identical files: 2155
Different same-path files: 1786
Only 8052: 8; only 8053: 8

## OTA partitions
| Partition | 8052 bytes | 8053 bytes | Exact match |
|---|---:|---:|---|
| 3rd_a | 31457280 | 31457280 | False |
| armfw | 77824 | 77824 | True |
| boot | 78643200 | 78643200 | False |
| bootdata | 41943040 | 41943040 | False |
| dtbo | 8388608 | 8388608 | False |
| factory_a | 8388608 | 8388608 | False |
| linux_rootfs_a | 57671680 | 57671680 | False |
| mboot | 2658304 | 2654208 | False |
| optee | 2809856 | 2809856 | False |
| product | 77152256 | 77152256 | False |
| system | 696111104 | 681955328 | False |
| system_ext | 87273472 | 87937024 | False |
| tvconfig | 157286400 | 157286400 | False |
| tvservice | 175112192 | 175112192 | False |
| vbmeta | 12288 | 12288 | False |
| vbmeta_system | 4096 | 4096 | False |
| vendor | 255258624 | 254906368 | False |

## OEM APK versions and exact hashes
| APK | 8052 version | 8053 version | Exact match |
|---|---|---|---|
| system/system/apex/com.android.permission/priv-app/SafetyCenterResources@TP1A.220624.021.A1/SafetyCenterResources.apk | 33 system image | 33 system image | True |
| system/system/apex/com.android.tethering.inprocess/priv-app/ServiceConnectivityResources@TP1A.220624.021.A1/ServiceConnectivityResources.apk | S-initial | S-initial | True |
| system/system/apex/com.android.uwb/priv-app/ServiceUwbResources@TP1A.220624.021.A1/ServiceUwbResources.apk | T-initial | T-initial | True |
| system/system/apex/com.android.wifi/priv-app/ServiceWifiResources@TP1A.220624.021.A1/ServiceWifiResources.apk | R-initial | R-initial | True |
| system/system/app/KuSettings/KuSettings.apk | 1.0 | 1.0 | False |
| system/system/app/KuSourceRJ/KuSourceRJ.apk | 5.3 | 3.6 | False |
| system/system/app/RuiAutoFocus/RuiAutoFocus.apk | 4.2 | 4.2 | False |
| system/system/app/TrdDreamPic/TrdDreamPic.apk | 1.0 | 1.0 | True |
| system/system/app/TrdFactoryTest/TrdFactoryTest.apk | 1.0 | 1.0 | True |
| system/system/app/trdservice/trdservice.apk | 13 | 13 | False |
| system/system/app/zxlauncher/zxlauncher.apk | 2.0.43 | 2.0.37 | False |
| system/system/app/zxstore/zxstore.apk | 4.1.52 | 4.1.52 | True |
| system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk | 13 | 13 | False |
| system/system/priv-app/RuiYunOta/RuiYunOta.apk | 1.0 | 1.0 | False |
| system/system/priv-app/SettingsProvider/SettingsProvider.apk | 13 | 13 | False |
| system/system/priv-app/TvProvider/TvProvider.apk | 13 | 13 | True |
| system_ext/app/Factory/Factory.apk | 1.0 | 1.0 | False |
| system_ext/app/TvFrameworkPackageStubs/TvFrameworkPackageStubs.apk | 1.0.1 | 1.0.1 | True |
| system_ext/priv-app/LiveTV/LiveTV.apk | 2.30.5 build 18321512 | 2.30.5 build 18321512 | False |
| system_ext/priv-app/MtkTvInput/MtkTvInput.apk | 13 | 13 | True |
| system_ext/priv-app/TvServices/TvServices.apk | 1.3 | 1.3 | False |
| system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk | 1.0 | 1.0 | False |
| vendor/priv-app/trdmiddle/trdmiddle.apk | 1.0 | 1.0 | False |

## Changed hardware-related paths
- product/lib/libmtkmtalservice_hwbinder_vendor.so
- product/lib/vendor.mediatek.tv.mtkmtalservice@1.0.so
- system/init.trd.rc
- system/system/apex/com.android.vndk.current/lib/android.hardware.audio.common-V1-ndk.so
- system/system/apex/com.android.vndk.current/lib/android.hardware.audio.common@2.0.so
- system/system/apex/com.android.vndk.current/lib/android.hardware.bluetooth.audio-V2-ndk.so
- system/system/apex/com.android.vndk.current/lib/android.hardware.soundtrigger3-V1-ndk.so
- system/system/apex/com.android.vndk.current/lib/android.hardware.soundtrigger@2.0-core.so
- system/system/apex/com.android.vndk.current/lib/android.hardware.soundtrigger@2.0.so
- system/system/apex/com.android.vndk.current/lib/android.media.audio.common.types-V1-ndk.so
- system/system/apex/com.android.vndk.current/lib/android.media.soundtrigger.types-V1-ndk.so
- system/system/apex/com.android.vndk.current/lib/libaudioroute.so
- system/system/apex/com.android.vndk.current/lib/libaudioutils.so
- system/system/app/RuiAutoFocus/RuiAutoFocus.apk
- system/system/app/RuiAutoFocus/oat/arm/RuiAutoFocus.odex
- system/system/app/RuiAutoFocus/oat/arm/RuiAutoFocus.vdex
- system/system/app/TrdDreamPic/oat/arm/TrdDreamPic.odex
- system/system/app/TrdFactoryTest/oat/arm/TrdFactoryTest.odex
- system/system/app/trdservice/oat/arm/trdservice.odex
- system/system/app/trdservice/oat/arm/trdservice.vdex
- system/system/app/trdservice/trdservice.apk
- system/system/bin/audioserver
- system/system/bin/mtk_screenrecord
- system/system/bin/mtk_screenrecord_mr
- system/system/framework/oat/arm/com.android.media.remotedisplay.odex
- system/system/lib/aaudio-aidl-cpp.so
- system/system/lib/android.hardware.audio.common-V1-ndk.so
- system/system/lib/android.hardware.audio.common-util.so
- system/system/lib/android.hardware.audio.common@2.0.so
- system/system/lib/android.hardware.audio.common@4.0-util.so
- system/system/lib/android.hardware.audio.common@4.0.so
- system/system/lib/android.hardware.audio.common@5.0-util.so
- system/system/lib/android.hardware.audio.common@5.0.so
- system/system/lib/android.hardware.audio.common@6.0-util.so
- system/system/lib/android.hardware.audio.common@6.0.so
- system/system/lib/android.hardware.audio.effect@4.0-util.so
- system/system/lib/android.hardware.audio.effect@4.0.so
- system/system/lib/android.hardware.audio.effect@5.0-util.so
- system/system/lib/android.hardware.audio.effect@5.0.so
- system/system/lib/android.hardware.audio.effect@6.0-util.so
- system/system/lib/android.hardware.audio.effect@6.0.so
- system/system/lib/android.hardware.audio@4.0-util.so
- system/system/lib/android.hardware.audio@4.0.so
- system/system/lib/android.hardware.audio@5.0-util.so
- system/system/lib/android.hardware.audio@5.0.so
- system/system/lib/android.hardware.audio@6.0-util.so
- system/system/lib/android.hardware.audio@6.0.so
- system/system/lib/android.hardware.bluetooth.audio-V2-ndk.so
- system/system/lib/android.hardware.bluetooth.audio@2.0.so
- system/system/lib/android.hardware.bluetooth.audio@2.1.so
- system/system/lib/android.media.audio.common.types-V1-cpp.so
- system/system/lib/android.media.audio.common.types-V1-ndk.so
- system/system/lib/audioclient-types-aidl-cpp.so
- system/system/lib/audioflinger-aidl-cpp.so
- system/system/lib/audiopolicy-aidl-cpp.so
- system/system/lib/audiopolicy-types-aidl-cpp.so
- system/system/lib/libaaudio.so
- system/system/lib/libaaudio_internal.so
- system/system/lib/libaaudioservice.so
- system/system/lib/libaudioclient.so
- system/system/lib/libaudioclient_aidl_conversion.so
- system/system/lib/libaudioeffect_jni.so
- system/system/lib/libaudioflinger.so
- system/system/lib/libaudiofoundation.so
- system/system/lib/libaudiohal.so
- system/system/lib/libaudiohal@4.0.so
- system/system/lib/libaudiohal@5.0.so
- system/system/lib/libaudiohal@6.0.so
- system/system/lib/libaudiohal@7.0.so
- system/system/lib/libaudiohal@7.1.so
- system/system/lib/libaudiohal_deathhandler.so
- system/system/lib/libaudiomanager.so
- system/system/lib/libaudiopolicy.so
- system/system/lib/libaudiopolicyengineconfigurable.so
- system/system/lib/libaudiopolicyenginedefault.so
- system/system/lib/libaudiopolicymanagercustom.so
- system/system/lib/libaudiopolicymanagerdefault.so
- system/system/lib/libaudiopolicyservice.so
- system/system/lib/libaudioprocessing.so
- system/system/lib/libaudiospdif.so
- system/system/lib/libaudioutils.so
- system/system/lib/libi2c_jni.so
- system/system/lib/libmtkscreenrecord.so
- system/system/lib/libmtkvoc.so
- system/system/lib/libremote-processor.so
- system/system/lib/libsoundpool.so
- system/system/lib/libtrdclient.so
- system/system/lib/libvintf.so
- system/system/lib/mstar.hardware.imgdisp@1.0.so
- system/system/lib/mstar.hardware.imghwdec@1.0.so
- system/system/lib/mstar.hardware.intertunnel@1.0.so
- system/system/lib/vendor.mediatek.tv.mtktvvoc@1.0.so
- system/system/lib/vendor.trd.hardware.hwtrd@1.0.so
- system/system/lib/vendor.trd.hardware.tof@1.0.so
- system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk
- system/system/priv-app/SoundPicker/oat/arm/SoundPicker.odex
- system_ext/framework/oat/arm/com.mstar.android.odex
- system_ext/lib/libmtkcmpb.so
- system_ext/lib/libmtkrm_hwbinder.so
- system_ext/lib/vendor.mediatek.api.mtktvapi@1.0.so
- system_ext/lib/vendor.mediatek.custom.mtktvapicustom@1.0.so
- system_ext/lib/vendor.mediatek.tv.mtkcalman@1.0.so
- system_ext/lib/vendor.mediatek.tv.mtkdmservice@1.0.so
- system_ext/lib/vendor.mediatek.tv.mtkmtalservice@1.0.so
- system_ext/lib/vendor.mediatek.tv.mtkrm@1.0.so
- system_ext/lib/vendor.mediatek.tv.mtktvfactory@1.0.so
- system_ext/priv-app/MtkNetworkMonitorService/oat/arm/MtkNetworkMonitorService.odex
- system_ext/priv-app/MtkTvInput/oat/arm/MtkTvInput.odex
- system_ext/priv-app/RemoteProvisioner/oat/arm/RemoteProvisioner.odex
- vendor/bin/MtkRmInitServer
- vendor/bin/MtkRmServer
- vendor/bin/hw/mstar.hardware.imgdisp@1.0-service
- vendor/bin/hw/mstar.hardware.imghwdec@1.0-service
- vendor/bin/hw/mstar.hardware.mmdisp@1.0-service
- vendor/bin/hw/vendor.mediatek.api.mtktvapi@1.0-service
- vendor/bin/hw/vendor.mediatek.hardware.audio.service
- vendor/bin/hw/vendor.mediatek.tv.mtkcalman@1.0-service
- vendor/bin/hw/vendor.mediatek.tv.mtkdmservice@1.0-service
- vendor/bin/hw/vendor.mediatek.tv.mtkmtalservice@1.0-service
- vendor/bin/hw/vendor.mediatek.tv.mtkrm@1.0-service
- vendor/bin/hw/vendor.mediatek.tv.mtktvfactory@1.0-service
- vendor/bin/hw/vendor.mediatek.tv.mtktvvoc@1.0-service
- vendor/bin/postinst_mtk
- vendor/bin/trd_module_loader.sh
- vendor/lib/android.hardware.audio.common-util.so
- vendor/lib/android.hardware.audio.common@5.0.so
- vendor/lib/android.hardware.audio.common@7.0-enums.so
- vendor/lib/android.hardware.audio.common@7.0-util.so
- vendor/lib/android.hardware.audio.common@7.0.so
- vendor/lib/android.hardware.audio.common@7.1-enums.so
- vendor/lib/android.hardware.audio.common@7.1-util.so
- vendor/lib/android.hardware.audio.effect@7.0-util.so
- vendor/lib/android.hardware.audio.effect@7.0.so
- vendor/lib/android.hardware.audio@7.0.so
- vendor/lib/android.hardware.audio@7.1-util.so
- vendor/lib/android.hardware.audio@7.1.so
- vendor/lib/android.hardware.bluetooth.audio-impl.so
- vendor/lib/android.hardware.bluetooth.audio@2.0.so
- vendor/lib/android.hardware.bluetooth.audio@2.1.so
- vendor/lib/android.media.audio.common.types-V1-cpp.so
- vendor/lib/audioclient-types-aidl-cpp.so
- vendor/lib/hw/android.hardware.audio.effect@7.0-impl.so
- vendor/lib/hw/android.hardware.audio@7.1-impl.so
- vendor/lib/hw/android.hardware.bluetooth.audio@2.1-impl.so
- vendor/lib/hw/audio.bluetooth.default.so
- vendor/lib/hw/audio.primary.default.so
- vendor/lib/hw/audio.primary.mt5873.so
- vendor/lib/hw/audio.r_submix.default.so
- vendor/lib/hw/audio.usb.default.so
- vendor/lib/libMtkAiVisionVbClUtil.so
- vendor/lib/libMtkRmClient.so
- vendor/lib/libaudioclient_aidl_conversion.so
- vendor/lib/libaudiofoundation.so
- vendor/lib/libaudioparser.so
- vendor/lib/libbluetooth_audio_session.so
- vendor/lib/libbluetooth_audio_session_aidl.so
- vendor/lib/libcodec2.MTK.so
- vendor/lib/libcodec2_mtk_audio.so
- vendor/lib/libcodec2_mtk_c2store.so
- vendor/lib/libcodec2_mtk_vdec.so
