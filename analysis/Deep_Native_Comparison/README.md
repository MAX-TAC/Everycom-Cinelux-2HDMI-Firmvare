# MediaTek / OEM native libraries, service configuration and DTBO diff

The executable .text ELF sections were hashed separately from the whole binary. When full binary SHA differs but .text agrees, differences may be metadata, other data, or non-executable code; not proof of identical function.
Privacy-related configuration strings were filtered before comparison.

## Shared library comparison

- total_one: **1333**
- total_two: **1335**
- identical: **88**
- changed_binary: **1245**
- code_text_changed: **4**
- code_text_same_but_binary_diff: **1241**

## Apparatus-related native libraries with different binary SHA

| ELF | Same executable .text? | 1 HDMI text bytes | 2 HDMI text bytes | Dependencies difference |
|---|---|---:|---:|---|
| product_a/lib/libmtkmtalservice_hwbinder_vendor.so | True | 3056 | 3056 | + ; -  |
| product_a/lib/vendor.mediatek.tv.mtkmtalservice@1.0.so | True | 165468 | 165468 | + ; -  |
| system_a/system/apex/com.android.media.swcodec/bin/mediaswcodec | True | 4200 | 4200 | + ; -  |
| system_a/system/apex/com.android.media.swcodec/lib/libcodec2_hidl@1.0.so | True | 119940 | 119940 | + ; -  |
| system_a/system/apex/com.android.media.swcodec/lib/libcodec2_hidl@1.1.so | True | 40220 | 40220 | + ; -  |
| system_a/system/apex/com.android.media.swcodec/lib/libcodec2_hidl@1.2.so | True | 41400 | 41400 | + ; -  |
| system_a/system/apex/com.android.media.swcodec/lib/libstagefright_foundation.so | True | 89252 | 89252 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.audio.common-V1-ndk.so | True | 4916 | 4916 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.audio.common@2.0.so | True | 424 | 424 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.bluetooth.audio-V2-ndk.so | True | 51004 | 51004 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.common-V1-ndk.so | True | 2320 | 2320 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.device-V1-ndk.so | True | 52268 | 52268 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.metadata-V1-ndk.so | True | 32 | 32 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.camera.provider-V1-ndk.so | True | 17596 | 17596 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.power-V3-ndk.so | True | 13112 | 13112 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.power.stats-V1-ndk.so | True | 16272 | 16272 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.hardware.rebootescrow-V1-ndk.so | True | 5548 | 5548 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/android.media.audio.common.types-V1-ndk.so | True | 14420 | 14420 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/libaudioroute.so | True | 4720 | 4720 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/libaudioutils.so | True | 53576 | 53576 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/libcamera_metadata.so | True | 18456 | 18456 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/libcodec2.so | True | 32 | 32 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/libmkbootimg_abi_check.so | True | 32 | 32 | + ; -  |
| system_a/system/apex/com.android.vndk.current/lib/libpower.so | True | 5592 | 5592 | + ; -  |
| system_a/system/bin/audioserver | True | 4160 | 4160 | + ; -  |
| system_a/system/bin/bootanimation | True | 3884 | 3884 | + ; -  |
| system_a/system/bin/bootctl | True | 7736 | 7736 | + ; -  |
| system_a/system/bin/bootstat | True | 68416 | 68416 | + ; -  |
| system_a/system/bin/cameraserver | True | 4172 | 4172 | + ; -  |
| system_a/system/bin/mtk_screenrecord | True | 7296 | 7296 | + ; -  |
| system_a/system/bin/mtk_screenrecord_mr | True | 2943584 | 2943584 | + ; -  |
| system_a/system/bin/reboot | True | 532 | 532 | + ; -  |
| system_a/system/lib/aaudio-aidl-cpp.so | True | 26544 | 26544 | + ; -  |
| system_a/system/lib/android.frameworks.cameraservice.common@2.0.so | True | 556 | 556 | + ; -  |
| system_a/system/lib/android.frameworks.cameraservice.device@2.0.so | True | 80280 | 80280 | + ; -  |
| system_a/system/lib/android.frameworks.cameraservice.device@2.1.so | True | 31820 | 31820 | + ; -  |
| system_a/system/lib/android.frameworks.cameraservice.service@2.0.so | True | 50512 | 50512 | + ; -  |
| system_a/system/lib/android.frameworks.cameraservice.service@2.1.so | True | 46276 | 46276 | + ; -  |
| system_a/system/lib/android.frameworks.cameraservice.service@2.2.so | True | 26516 | 26516 | + ; -  |
| system_a/system/lib/android.frameworks.displayservice@1.0.so | True | 60396 | 60396 | + ; -  |
| system_a/system/lib/android.hardware.audio.common-V1-ndk.so | True | 4916 | 4916 | + ; -  |
| system_a/system/lib/android.hardware.audio.common-util.so | True | 780 | 780 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@2.0.so | True | 424 | 424 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@4.0-util.so | True | 3512 | 3512 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@4.0.so | True | 424 | 424 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@5.0-util.so | True | 4420 | 4420 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@5.0.so | True | 2664 | 2664 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@6.0-util.so | True | 4452 | 4452 | + ; -  |
| system_a/system/lib/android.hardware.audio.common@6.0.so | True | 2664 | 2664 | + ; -  |
| system_a/system/lib/android.hardware.audio.effect@4.0-util.so | True | 476 | 476 | + ; -  |
| system_a/system/lib/android.hardware.audio.effect@4.0.so | True | 660024 | 660024 | + ; -  |
| system_a/system/lib/android.hardware.audio.effect@5.0-util.so | True | 476 | 476 | + ; -  |
| system_a/system/lib/android.hardware.audio.effect@5.0.so | True | 660040 | 660040 | + ; -  |
| system_a/system/lib/android.hardware.audio.effect@6.0-util.so | True | 476 | 476 | + ; -  |
| system_a/system/lib/android.hardware.audio.effect@6.0.so | True | 660184 | 660184 | + ; -  |
| system_a/system/lib/android.hardware.audio@4.0-util.so | True | 5232 | 5232 | + ; -  |
| system_a/system/lib/android.hardware.audio@4.0.so | True | 361332 | 361332 | + ; -  |
| system_a/system/lib/android.hardware.audio@5.0-util.so | True | 4516 | 4516 | + ; -  |
| system_a/system/lib/android.hardware.audio@5.0.so | True | 364660 | 364660 | + ; -  |
| system_a/system/lib/android.hardware.audio@6.0-util.so | True | 4516 | 4516 | + ; -  |
| system_a/system/lib/android.hardware.audio@6.0.so | True | 409328 | 409328 | + ; -  |
| system_a/system/lib/android.hardware.bluetooth.audio-V2-ndk.so | True | 50960 | 50960 | + ; -  |
| system_a/system/lib/android.hardware.bluetooth.audio@2.0.so | True | 75500 | 75500 | + ; -  |
| system_a/system/lib/android.hardware.bluetooth.audio@2.1.so | True | 51832 | 51832 | + ; -  |
| system_a/system/lib/android.hardware.boot@1.0.so | True | 36156 | 36156 | + ; -  |
| system_a/system/lib/android.hardware.boot@1.1.so | True | 28284 | 28284 | + ; -  |
| system_a/system/lib/android.hardware.boot@1.2.so | True | 28324 | 28324 | + ; -  |
| system_a/system/lib/android.hardware.camera.common-V1-ndk.so | True | 2320 | 2320 | + ; -  |
| system_a/system/lib/android.hardware.camera.common@1.0.so | True | 556 | 556 | + ; -  |
| system_a/system/lib/android.hardware.camera.device-V1-ndk.so | True | 52192 | 52192 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@1.0.so | True | 133432 | 133432 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@3.2.so | True | 80276 | 80276 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@3.3.so | True | 27400 | 27400 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@3.4.so | True | 50192 | 50192 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@3.5.so | True | 84252 | 84252 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@3.6.so | True | 81120 | 81120 | + ; -  |
| system_a/system/lib/android.hardware.camera.device@3.7.so | True | 101008 | 101008 | + ; -  |
| system_a/system/lib/android.hardware.camera.metadata-V1-ndk.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/android.hardware.camera.metadata@3.2.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/android.hardware.camera.metadata@3.3.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/android.hardware.camera.metadata@3.4.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/android.hardware.camera.metadata@3.5.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/android.hardware.camera.metadata@3.6.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/android.hardware.camera.provider-V1-ndk.so | True | 17572 | 17572 | + ; -  |
| system_a/system/lib/android.hardware.camera.provider@2.4.so | True | 53556 | 53556 | + ; -  |
| system_a/system/lib/android.hardware.camera.provider@2.5.so | True | 26796 | 26796 | + ; -  |
| system_a/system/lib/android.hardware.camera.provider@2.6.so | True | 49296 | 49296 | + ; -  |
| system_a/system/lib/android.hardware.camera.provider@2.7.so | True | 31952 | 31952 | + ; -  |
| system_a/system/lib/android.hardware.power-V2-cpp.so | True | 11460 | 11460 | + ; -  |
| system_a/system/lib/android.hardware.power-V3-cpp.so | True | 11460 | 11460 | + ; -  |
| system_a/system/lib/android.hardware.power.stats-V1-cpp.so | True | 15380 | 15380 | + ; -  |
| system_a/system/lib/android.hardware.power.stats-V1-ndk.so | True | 16272 | 16272 | + ; -  |
| system_a/system/lib/android.hardware.power.stats@1.0.so | True | 36904 | 36904 | + ; -  |
| system_a/system/lib/android.hardware.power@1.0.so | True | 26568 | 26568 | + ; -  |
| system_a/system/lib/android.hardware.power@1.1.so | True | 26884 | 26884 | + ; -  |
| system_a/system/lib/android.hardware.power@1.2.so | True | 26512 | 26512 | + ; -  |
| system_a/system/lib/android.hardware.power@1.3.so | True | 28424 | 28424 | + ; -  |
| system_a/system/lib/android.hardware.tv.input@1.0.so | True | 42972 | 42972 | + ; -  |
| system_a/system/lib/android.media.audio.common.types-V1-cpp.so | True | 17912 | 17912 | + ; -  |
| system_a/system/lib/android.media.audio.common.types-V1-ndk.so | True | 14420 | 14420 | + ; -  |
| system_a/system/lib/audioclient-types-aidl-cpp.so | True | 19864 | 19864 | + ; -  |
| system_a/system/lib/audioflinger-aidl-cpp.so | True | 132160 | 132160 | + ; -  |
| system_a/system/lib/audiopolicy-aidl-cpp.so | True | 137388 | 137388 | + ; -  |
| system_a/system/lib/audiopolicy-types-aidl-cpp.so | True | 11600 | 11600 | + ; -  |
| system_a/system/lib/bootstrap/libc.so | True | 562732 | 562732 | + ; -  |
| system_a/system/lib/bootstrap/libm.so | True | 91968 | 91968 | + ; -  |
| system_a/system/lib/libaaudio.so | True | 9476 | 9476 | + ; -  |
| system_a/system/lib/libaaudio_internal.so | True | 164596 | 164596 | + ; -  |
| system_a/system/lib/libaaudioservice.so | True | 127016 | 127016 | + ; -  |
| system_a/system/lib/libaudioclient.so | True | 407900 | 407900 | + ; -  |
| system_a/system/lib/libaudioclient_aidl_conversion.so | True | 121624 | 121624 | + ; -  |
| system_a/system/lib/libaudioeffect_jni.so | True | 23216 | 23216 | + ; -  |
| system_a/system/lib/libaudioflinger.so | True | 711104 | 711104 | + ; -  |
| system_a/system/lib/libaudiofoundation.so | True | 121180 | 121180 | + ; -  |
| system_a/system/lib/libaudiohal.so | True | 6304 | 6304 | + ; -  |
| system_a/system/lib/libaudiohal@4.0.so | True | 80688 | 80688 | + ; -  |
| system_a/system/lib/libaudiohal@5.0.so | True | 81344 | 81344 | + ; -  |
| system_a/system/lib/libaudiohal@6.0.so | True | 85500 | 85500 | + ; -  |
| system_a/system/lib/libaudiohal@7.0.so | True | 989752 | 989752 | + ; -  |
| system_a/system/lib/libaudiohal@7.1.so | True | 1244336 | 1244336 | + ; -  |
| system_a/system/lib/libaudiohal_deathhandler.so | True | 4460 | 4460 | + ; -  |
| system_a/system/lib/libaudiomanager.so | True | 2752 | 2752 | + ; -  |
| system_a/system/lib/libaudiopolicy.so | True | 39136 | 39136 | + ; -  |
| system_a/system/lib/libaudiopolicyengineconfigurable.so | True | 271456 | 271456 | + ; -  |
| system_a/system/lib/libaudiopolicyenginedefault.so | True | 277644 | 277644 | + ; -  |
| system_a/system/lib/libaudiopolicymanagercustom.so | True | 6112 | 6112 | + ; -  |
| system_a/system/lib/libaudiopolicymanagerdefault.so | True | 535200 | 535200 | + ; -  |
| system_a/system/lib/libaudiopolicyservice.so | True | 243912 | 243912 | + ; -  |
| system_a/system/lib/libaudioprocessing.so | True | 463656 | 463656 | + ; -  |
| system_a/system/lib/libaudiospdif.so | True | 3312 | 3312 | + ; -  |
| system_a/system/lib/libaudioutils.so | True | 53576 | 53576 | + ; -  |
| system_a/system/lib/libbootanimation.so | True | 28664 | 28664 | + ; -  |
| system_a/system/lib/libbootloader_message.so | True | 53908 | 53908 | + ; -  |
| system_a/system/lib/libcamera2ndk.so | True | 141496 | 141496 | + ; -  |
| system_a/system/lib/libcamera_client.so | True | 231564 | 231564 | + ; -  |
| system_a/system/lib/libcamera_metadata.so | True | 18456 | 18456 | + ; -  |
| system_a/system/lib/libcameraservice.so | True | 1262732 | 1262732 | + ; -  |
| system_a/system/lib/libcodec2.so | True | 32 | 32 | + ; -  |
| system_a/system/lib/libcodec2_client.so | True | 77232 | 77232 | + ; -  |
| system_a/system/lib/libcodec2_hidl@1.0.so | True | 120904 | 120904 | + ; -  |
| system_a/system/lib/libcodec2_hidl@1.1.so | True | 41404 | 41404 | + ; -  |
| system_a/system/lib/libcodec2_hidl@1.2.so | True | 42788 | 42788 | + ; -  |
| system_a/system/lib/libcodec2_hidl_client@1.0.so | True | 46984 | 46984 | + ; -  |
| system_a/system/lib/libcodec2_hidl_client@1.1.so | True | 4120 | 4120 | + ; -  |
| system_a/system/lib/libcodec2_hidl_client@1.2.so | True | 4120 | 4120 | + ; -  |
| system_a/system/lib/libcodec2_hidl_plugin_stub.so | True | 5108 | 5108 | + ; -  |
| system_a/system/lib/libcodec2_soft_aacdec.so | True | 556748 | 556748 | + ; -  |
| system_a/system/lib/libcodec2_soft_aacenc.so | True | 370356 | 370356 | + ; -  |
| system_a/system/lib/libcodec2_soft_amrnbdec.so | True | 92268 | 92268 | + ; -  |
| system_a/system/lib/libcodec2_soft_amrnbenc.so | True | 74736 | 74736 | + ; -  |

## Native binaries only in one-HDMI


## Native binaries only in two-HDMI

- system_a/system/lib/libfactoryi2c_jni.so
- system_a/system/lib/libsettingsi2c_jni.so

## Configuration comparison

- one: 210
- two: 210
- same_files: 202
- changed_files: 8
- only_one: 0
- only_two: 0

### Important differing config fragments

#### product_a/etc/build.prop

~~~diff
--- one-HDMI/product_a/etc/build.prop

+++ two-HDMI/product_a/etc/build.prop

@@ -8,11 +8,11 @@

 ro.product.product.model=DEMO
 ro.product.product.name=mt5873_cd
-ro.product.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.product.build.date.utc=1786585338
-ro.product.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.product.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.product.build.date.utc=1790754097
+ro.product.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.product.build.id=TP1A.220624.021.A1
 ro.product.build.tags=test-keys
 ro.product.build.type=userdebug
-ro.product.build.version.incremental=eng.luzhih.20260813.014112
+ro.product.build.version.incremental=eng.suhaix.20260930.074037
 ro.product.build.version.release=13
 ro.product.build.version.release_or_codename=13
~~~

#### system_a/system/build.prop

~~~diff
--- one-HDMI/system_a/system/build.prop

+++ two-HDMI/system_a/system/build.prop

@@ -11,11 +11,11 @@

 ro.system.product.cpu.abilist32=armeabi-v7a,armeabi
 ro.system.product.cpu.abilist64=
-ro.system.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.system.build.date.utc=1786585338
-ro.system.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.system.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.system.build.date.utc=1790754097
+ro.system.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.system.build.id=TP1A.220624.021.A1
 ro.system.build.tags=test-keys
 ro.system.build.type=userdebug
-ro.system.build.version.incremental=eng.luzhih.20260813.014112
+ro.system.build.version.incremental=eng.suhaix.20260930.074037
 ro.system.build.version.release=13
 ro.system.build.version.release_or_codename=13
@@ -27,6 +27,6 @@

 # autogenerated by buildinfo.sh
 ro.build.id=TP1A.220624.021.A1
-ro.build.display.id=mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.luzhih.20260813.014112 test-keys
-ro.build.version.incremental=eng.luzhih.20260813.014112
+ro.build.display.id=mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.suhaix.20260930.074037 test-keys
+ro.build.version.incremental=eng.suhaix.20260930.074037
 ro.build.version.sdk=33
 ro.build.version.preview_sdk=0
@@ -41,8 +41,8 @@

 ro.build.version.base_os=
 ro.build.version.min_supported_target_sdk=23
-ro.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.build.date.utc=1786585338
+ro.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.build.date.utc=1790754097
 ro.build.type=userdebug
-ro.build.user=luzhiheng
+ro.build.user=suhaixiong
 ro.build.host=5a7517920bed
 ro.build.tags=test-keys
@@ -58,5 +58,5 @@

 ro.build.product=mt5873
 # Do not try to parse description or thumbprint
-ro.build.description=mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.luzhih.20260813.014112 test-keys
+ro.build.description=mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.suhaix.20260930.074037 test-keys
 # end build properties
 ####################################
~~~

#### system_a/system/system_dlkm/etc/build.prop

~~~diff
--- one-HDMI/system_a/system/system_dlkm/etc/build.prop

+++ two-HDMI/system_a/system/system_dlkm/etc/build.prop

@@ -8,11 +8,11 @@

 ro.product.system_dlkm.model=DEMO
 ro.product.system_dlkm.name=mt5873_cd
-ro.system_dlkm.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.system_dlkm.build.date.utc=1786585338
-ro.system_dlkm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.system_dlkm.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.system_dlkm.build.date.utc=1790754097
+ro.system_dlkm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.system_dlkm.build.id=TP1A.220624.021.A1
 ro.system_dlkm.build.tags=test-keys
 ro.system_dlkm.build.type=userdebug
-ro.system_dlkm.build.version.incremental=eng.luzhih.20260813.014112
+ro.system_dlkm.build.version.incremental=eng.suhaix.20260930.074037
 ro.system_dlkm.build.version.release=13
 ro.system_dlkm.build.version.release_or_codename=13
~~~

#### system_ext_a/etc/build.prop

~~~diff
--- one-HDMI/system_ext_a/etc/build.prop

+++ two-HDMI/system_ext_a/etc/build.prop

@@ -8,11 +8,11 @@

 ro.product.system_ext.model=DEMO
 ro.product.system_ext.name=mt5873_cd
-ro.system_ext.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.system_ext.build.date.utc=1786585338
-ro.system_ext.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.system_ext.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.system_ext.build.date.utc=1790754097
+ro.system_ext.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.system_ext.build.id=TP1A.220624.021.A1
 ro.system_ext.build.tags=test-keys
 ro.system_ext.build.type=userdebug
-ro.system_ext.build.version.incremental=eng.luzhih.20260813.014112
+ro.system_ext.build.version.incremental=eng.suhaix.20260930.074037
 ro.system_ext.build.version.release=13
 ro.system_ext.build.version.release_or_codename=13
~~~

#### vendor_a/build.prop

~~~diff
--- one-HDMI/vendor_a/build.prop

+++ two-HDMI/vendor_a/build.prop

@@ -11,11 +11,11 @@

 ro.vendor.product.cpu.abilist32=armeabi-v7a,armeabi
 ro.vendor.product.cpu.abilist64=
-ro.vendor.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.vendor.build.date.utc=1786585338
-ro.vendor.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.vendor.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.vendor.build.date.utc=1790754097
+ro.vendor.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.vendor.build.id=TP1A.220624.021.A1
 ro.vendor.build.tags=test-keys
 ro.vendor.build.type=userdebug
-ro.vendor.build.version.incremental=eng.luzhih.20260813.014112
+ro.vendor.build.version.incremental=eng.suhaix.20260930.074037
 ro.vendor.build.version.release=13
 ro.vendor.build.version.release_or_codename=13
@@ -311,5 +311,5 @@

 ro.product.model=Projetor
 persist.launcher.wallpaper=/system/core/launcher/wallpaper/picture/wallpaper.jpg
-ro.zeasn.devicetype=rjpj9660global
+ro.zeasn.devicetype=rjpj9660fordexp
 persist.sys.mphotool_dev_name=Projetor
 ro.rjpj.customer.id=0
@@ -321,8 +321,8 @@

 ro.rjpj.panel.id=0
 ro.rjpj.wifi.id=
-ro.rjpj.machine.id=8052
-ro.rjpj.yunota.version=RUIOS.8052.1.0.1
-ro.rjpj.gitrev=c519afa5fccfb0c52b2013f75b086ae46de5f732
-ro.rjpj.buildtime=20260813014113
+ro.rjpj.machine.id=8054
+ro.rjpj.yunota.version=RUIOS.8054.1.0.1
+ro.rjpj.gitrev=9d1556453fde2ee111d50176246baece41a9fc17
+ro.rjpj.buildtime=20260930074038
 ro.rjpj.support.aivoice.gsk=0
 ro.rjpj.support.suspension.settings=1
@@ -330,24 +330,24 @@

 ro.rjpj.netflix.mouse=1
 ro.rjpj.settings.show.av=0
-ro.rjpj.hdmi.ports=HW6:HDMI
-ro.rjpj.hdmi.port.count=1
-ro.rjpj.support.toffunction=0
+ro.rjpj.hdmi.ports=HW6:HDMI1,HW7:HDMI2
+ro.rjpj.hdmi.port.count=2
+ro.rjpj.support.toffunction=1
 ro.rjpj.support.otayun=1
 ro.rjpj.yunota.baseurl=https://www.szrjyun.com/ota/android/
-ro.rjpj.yunota.url=mt9660/8052/8052_ota.json
+ro.rjpj.yunota.url=mt9660/8054/8054_ota.json
 ro.rjpj.yunota.bin=upgrade_image.pkg
-ro.rjpj.yunota.zip=RJMT9660_firmware_8052.zip
+ro.rjpj.yunota.zip=RJMT9660_firmware_8054.zip
 ro.rjpj.v618rj.short.long.focus.id=1
-ro.product.ota=V618RJEN
+ro.product.ota=V618RJENHD
 ro.rjpj.autofocus.poweron=1
-ro.rjpj.autokeystone.poweron=0
+ro.rjpj.autokeystone.poweron=1
 ro.rjpj.autofocus.move=1
-ro.rjpj.autokeystone.move=0
+ro.rjpj.autokeystone.move=1
 ro.rjpj.obstacle.avoidance=0
 ro.rjpj.screen.alignment=0
 persist.rjpj.autofocus.poweron=1
-persist.rjpj.autokeystone.poweron=0
+persist.rjpj.autokeystone.poweron=1
 persist.rjpj.autofocus.move=1
-persist.rjpj.autokeystone.move=0
+persist.rjpj.autokeystone.move=1
 persist.rjpj.obstacle.avoidance=0
 persist.rjpj.screen.alignment=0
~~~

#### vendor_a/odm/etc/build.prop

~~~diff
--- one-HDMI/vendor_a/odm/etc/build.prop

+++ two-HDMI/vendor_a/odm/etc/build.prop

@@ -11,11 +11,11 @@

 ro.odm.product.cpu.abilist32=armeabi-v7a,armeabi
 ro.odm.product.cpu.abilist64=
-ro.odm.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.odm.build.date.utc=1786585338
-ro.odm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.odm.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.odm.build.date.utc=1790754097
+ro.odm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.odm.build.id=TP1A.220624.021.A1
 ro.odm.build.tags=test-keys
 ro.odm.build.type=userdebug
-ro.odm.build.version.incremental=eng.luzhih.20260813.014112
+ro.odm.build.version.incremental=eng.suhaix.20260930.074037
 ro.odm.build.version.release=13
 ro.odm.build.version.release_or_codename=13
~~~

#### vendor_a/odm_dlkm/etc/build.prop

~~~diff
--- one-HDMI/vendor_a/odm_dlkm/etc/build.prop

+++ two-HDMI/vendor_a/odm_dlkm/etc/build.prop

@@ -8,11 +8,11 @@

 ro.product.odm_dlkm.model=DEMO
 ro.product.odm_dlkm.name=mt5873_cd
-ro.odm_dlkm.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.odm_dlkm.build.date.utc=1786585338
-ro.odm_dlkm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.odm_dlkm.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.odm_dlkm.build.date.utc=1790754097
+ro.odm_dlkm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.odm_dlkm.build.id=TP1A.220624.021.A1
 ro.odm_dlkm.build.tags=test-keys
 ro.odm_dlkm.build.type=userdebug
-ro.odm_dlkm.build.version.incremental=eng.luzhih.20260813.014112
+ro.odm_dlkm.build.version.incremental=eng.suhaix.20260930.074037
 ro.odm_dlkm.build.version.release=13
 ro.odm_dlkm.build.version.release_or_codename=13
~~~

#### vendor_a/vendor_dlkm/etc/build.prop

~~~diff
--- one-HDMI/vendor_a/vendor_dlkm/etc/build.prop

+++ two-HDMI/vendor_a/vendor_dlkm/etc/build.prop

@@ -8,11 +8,11 @@

 ro.product.vendor_dlkm.model=DEMO
 ro.product.vendor_dlkm.name=mt5873_cd
-ro.vendor_dlkm.build.date=Thu Aug 13 01:42:18 UTC 2026
-ro.vendor_dlkm.build.date.utc=1786585338
-ro.vendor_dlkm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng08130139:userdebug/test-keys
+ro.vendor_dlkm.build.date=Wed Sep 30 07:41:37 UTC 2026
+ro.vendor_dlkm.build.date.utc=1790754097
+ro.vendor_dlkm.build.fingerprint=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys
 ro.vendor_dlkm.build.id=TP1A.220624.021.A1
 ro.vendor_dlkm.build.tags=test-keys
 ro.vendor_dlkm.build.type=userdebug
-ro.vendor_dlkm.build.version.incremental=eng.luzhih.20260813.014112
+ro.vendor_dlkm.build.version.incremental=eng.suhaix.20260930.074037
 ro.vendor_dlkm.build.version.release=13
 ro.vendor_dlkm.build.version.release_or_codename=13
~~~


## Device-tree overlay format

One HDMI: {"bytes": 8388608, "head64": "d7 b7 ab 1e 00 3a 08 f0 00 00 00 20 00 00 00 20 00 00 00 cf 00 00 00 20 00 00 08 00 00 00 00 00 00 00 03 6c 00 00 1a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00", "table": {"magic": "0xd7b7ab1e", "total_size": 3803376, "header_size": 32, "dt_entry_size": 32, "dt_entry_count": 207, "dt_entries_offset": 32, "page_size": 2048, "version": 0}}
Two HDMI: {"bytes": 8388608, "head64": "d7 b7 ab 1e 00 3a 08 f0 00 00 00 20 00 00 00 20 00 00 00 cf 00 00 00 20 00 00 08 00 00 00 00 00 00 00 31 28 00 00 1a 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00", "table": {"magic": "0xd7b7ab1e", "total_size": 3803376, "header_size": 32, "dt_entry_size": 32, "dt_entry_count": 207, "dt_entries_offset": 32, "page_size": 2048, "version": 0}}

## Conclusions and limits

Equal exported interfaces or init service declarations is not proof that board-specific drivers are interchangeable.
Full hardware-specific service behavior needs live logs and tests; never flash a foreign DTBO or erase calibration before board identity and recovery are established.

