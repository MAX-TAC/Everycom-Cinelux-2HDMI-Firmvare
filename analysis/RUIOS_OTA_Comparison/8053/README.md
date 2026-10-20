# Extracted RUIOS OTA 8053 image inventory

This was reconstructed with payload-dumper-go from a genuine stock Android A/B OTA. No firmware executed or flashed.

## Partitions
| Partition | Bytes | Type |
|---|---:|---|
| 3rd_a | 31457280 | Squashfs filesystem, little endian, version 4.0, lzo compressed, 697258 bytes, 19 inodes, blocksize: 131072 bytes, created: Fri Jun 12 08:41:51 2026 |
| armfw | 77824 | data |
| boot | 78643200 | Android bootimg, kernel, ramdisk (0x1000000), page size: 2048, cmdline (androidboot.boot_devices=1c660000.mtk-mmc-fcie bootvideo.enable=1 buildvariant=userdebug |
| bootdata | 41943040 | Linux rev 1.0 ext4 filesystem data, UUID=e68dbd2f-2e7d-4a3c-b5f2-7bbd23264b88, volume name "mnt/vendor/bootd/mnt/vendor/bootdata" (extents) (large files) (huge  |
| dtbo | 8388608 | data |
| factory_a | 8388608 | Linux rev 1.0 ext2 filesystem data, UUID=fdaf9097-d4eb-40fd-8fd4-808f13f50dc8, volume name "vendor/factory" (extents) (large files) (huge files) |
| linux_rootfs_a | 57671680 | Squashfs filesystem, little endian, version 4.0, lzo compressed, 52006958 bytes, 1124 inodes, blocksize: 131072 bytes, created: Fri Jun 12 08:41:49 2026 |
| mboot | 2654208 | data |
| optee | 2809856 | data |
| product | 77152256 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=64705B0F-EFFF-1C5B-B55E-A6FADB34C470, incompat: LZ4_0PADDING |
| system | 681955328 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=B3905ECD-07DF-9354-BDF8-E568586F719D, incompat: LZ4_0PADDING |
| system_ext | 87937024 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=FC60EC69-A0D5-365C-8CB7-ACB292488881, incompat: LZ4_0PADDING |
| tvconfig | 157286400 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files) |
| tvservice | 175112192 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files) |
| vbmeta | 12288 | data |
| vbmeta_system | 4096 | data |
| vendor | 254906368 | EROFS filesystem, compat: SB_CHKSUM MTIME, blocksize=12, exslots=0, uuid=AB90628A-318A-6A58-B59C-D67A48306214, incompat: LZ4_0PADDING |

## System versions
- system/system/build.prop:ro.build.display.id = mt5873_cd-userdebug 13 TP1A.220624.021.A1 eng.luzhih.20260612.083454 test-keys
- system/system/build.prop:ro.build.version.incremental = eng.luzhih.20260612.083454
- system/system/build.prop:ro.build.date = Fri Jun 12 08:36:19 UTC 2026
- system/system/build.prop:ro.build.date.utc = 1781253379
- vendor/build.prop:ro.product.model = Projetor

## OEM and selected Android APKs

| APK | Package | Version |
|---|---|---|
| system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk | 13 | 13 |
| system/system/priv-app/RuiYunOta/RuiYunOta.apk | 13 | 1.0 |
| system/system/app/KuSettings/KuSettings.apk | 14 | 1.0 |
| system/system/app/RuiAutoFocus/RuiAutoFocus.apk | 9 | 4.2 |
| system/system/app/TrdDreamPic/TrdDreamPic.apk | 13 | 1.0 |
| system/system/app/zxlauncher/zxlauncher.apk | 10 | 2.0.37 |
| system/system/app/trdservice/trdservice.apk | 13 | 13 |
| system/system/app/KuSourceRJ/KuSourceRJ.apk | 15 | 3.6 |
| system/system/app/zxstore/zxstore.apk | 10 | 4.1.52 |
| system/system/app/TrdFactoryTest/TrdFactoryTest.apk | 9 | 1.0 |
| system/system/apex/com.android.permission/priv-app/SafetyCenterResources@TP1A.220624.021.A1/SafetyCenterResources.apk | 13 | 33 system image |
| system/system/apex/com.android.uwb/priv-app/ServiceUwbResources@TP1A.220624.021.A1/ServiceUwbResources.apk | 13 | T-initial |
| system/system/apex/com.android.wifi/priv-app/ServiceWifiResources@TP1A.220624.021.A1/ServiceWifiResources.apk | 13 | R-initial |
| system/system/apex/com.android.tethering.inprocess/priv-app/ServiceConnectivityResources@TP1A.220624.021.A1/ServiceConnectivityResources.apk | com.android.connectivity.resources | S-initial |
| system_ext/priv-app/Provision/Provision.apk | 13 | 13 |
| system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk | 13 | 1.0 |
| system_ext/priv-app/RemoteProvisioner/RemoteProvisioner.apk | 13 | 13 |
| system_ext/priv-app/MtkNetworkMonitorService/MtkNetworkMonitorService.apk | 13 | 2.1 |
| system_ext/priv-app/SystemUI/SystemUI.apk | 13 | 13 |
| system_ext/priv-app/MtkTvInput/MtkTvInput.apk | 13 | 13 |
| system_ext/priv-app/LiveTV/LiveTV.apk | 13 | 2.30.5 build 18321512 |
| system_ext/app/Factory/Factory.apk | 13 | 1.0 |
| vendor/priv-app/trdmiddle/trdmiddle.apk | 13 | 1.0 |

Total extracted files: 3949, APK: 87
