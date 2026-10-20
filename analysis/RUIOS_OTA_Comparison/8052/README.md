# Extracted RUIOS OTA 8052 image inventory

This was reconstructed with payload-dumper-go from a genuine stock Android A/B OTA. No firmware executed or flashed.

## Partitions
| Partition | Bytes | Type |
|---|---:|---|
| 3rd_a | 31457280 | Squashfs filesystem, little endian, version 4.0, lzo compressed, 697255 bytes, 19 inodes, blocksize: 131072 bytes, created: Mon Oct 12 02:58:43 2026 |
| armfw | 77824 | data |
| boot | 78643200 | Android bootimg, kernel, ramdisk (0x1000000), page size: 2048, cmdline (androidboot.boot_devices=1c660000.mtk-mmc-fcie bootvideo.enable=1 buildvariant=userdebug |
| bootdata | 41943040 | Linux rev 1.0 ext4 filesystem data, UUID=bc7d4e1a-b06d-4910-a307-3263be3442fa, volume name "mnt/vendor/bootd/mnt/vendor/bootdata" (extents) (large files) (huge  |
| dtbo | 8388608 | data |
| factory_a | 8388608 | Linux rev 1.0 ext2 filesystem data, UUID=b943bb6b-a01c-43f7-86aa-c81bec7516b4, volume name "vendor/factory" (extents) (large files) (huge files) |
| linux_rootfs_a | 57671680 | Squashfs filesystem, little endian, version 4.0, lzo compressed, 48992680 bytes, 1124 inodes, blocksize: 131072 bytes, created: Mon Oct 12 02:58:41 2026 |
| mboot | 2658304 | data |
| optee | 2809856 | data |
| product | 77152256 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=525C8E0B-76E5-985B-9AD7-52426B93906E, incompat: LZ4_0PADDING |
| system | 696111104 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=0813EC73-BA86-525C-9489-F2EC51F9F67D, incompat: LZ4_0PADDING |
| system_ext | 87273472 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=0B1BB1CD-0662-645D-9EB3-8828AE47B741, incompat: LZ4_0PADDING |
| tvconfig | 157286400 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files) |
| tvservice | 175112192 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files) |
| vbmeta | 12288 | data |
| vbmeta_system | 4096 | data |
| vendor | 255258624 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=96ECD9B2-63B4-BB5F-8E11-2AEA3CB377E1, incompat: LZ4_0PADDING |

## System versions
- system/system/build.prop:ro.build.display.id = mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.suhaix.20261012.025220 test-keys
- system/system/build.prop:ro.build.version.incremental = eng.suhaix.20261012.025220
- system/system/build.prop:ro.build.date = Mon Oct 12 02:53:19 UTC 2026
- system/system/build.prop:ro.build.date.utc = 1791773599
- vendor/build.prop:ro.product.model = Projetor

## OEM and selected Android APKs

| APK | Package | Version |
|---|---|---|
| system/system/app/KuSettings/KuSettings.apk | 14 | 1.0 |
| system/system/app/KuSetupWizard/KuSetupWizard.apk | 14 | 1.0 |
| system/system/app/zxlauncher/zxlauncher.apk | 10 | 2.0.43 |
| system/system/app/KuSourceRJ/KuSourceRJ.apk | 15 | 5.3 |
| system/system/app/zxstore/zxstore.apk | 10 | 4.1.52 |
| system/system/app/RuiAutoFocus/RuiAutoFocus.apk | 9 | 4.2 |
| system/system/app/trdservice/trdservice.apk | 13 | 13 |
| system/system/app/TrdDreamPic/TrdDreamPic.apk | 13 | 1.0 |
| system/system/app/TrdFactoryTest/TrdFactoryTest.apk | 9 | 1.0 |
| system/system/priv-app/RuiYunOta/RuiYunOta.apk | 13 | 1.0 |
| system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk | 13 | 13 |
| system/system/apex/com.android.uwb/priv-app/ServiceUwbResources@TP1A.220624.021.A1/ServiceUwbResources.apk | 13 | T-initial |
| system/system/apex/com.android.tethering.inprocess/priv-app/ServiceConnectivityResources@TP1A.220624.021.A1/ServiceConnectivityResources.apk | com.android.connectivity.resources | S-initial |
| system/system/apex/com.android.wifi/priv-app/ServiceWifiResources@TP1A.220624.021.A1/ServiceWifiResources.apk | 13 | R-initial |
| system/system/apex/com.android.permission/priv-app/SafetyCenterResources@TP1A.220624.021.A1/SafetyCenterResources.apk | 13 | 33 system image |
| system_ext/app/Factory/Factory.apk | 13 | 1.0 |
| system_ext/priv-app/LiveTV/LiveTV.apk | 13 | 2.30.5 build 18321512 |
| system_ext/priv-app/MtkTvInput/MtkTvInput.apk | 13 | 13 |
| system_ext/priv-app/SystemUI/SystemUI.apk | 13 | 13 |
| system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk | 13 | 1.0 |
| system_ext/priv-app/MtkNetworkMonitorService/MtkNetworkMonitorService.apk | 13 | 2.1 |
| system_ext/priv-app/RemoteProvisioner/RemoteProvisioner.apk | 13 | 13 |
| vendor/priv-app/trdmiddle/trdmiddle.apk | 13 | 1.0 |

Total extracted files: 3949, APK: 85
