# CineLux source firmware reconstructed partitions
Only static file extraction; original update archive was not executed or flashed.

## Super partition
Size: 2225078272 bytes
Format: data
Expected GPT space: 2225078272

## Segment table
| # | Destination | Input bytes | Decompressed bytes | Format | Status |
|---:|---|---:|---:|---|---|
| 1 | tvconfig_a, tvconfig_b | 9728033 | 157286400 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc | ok |
| 2 | project_id | 21435 | 5242880 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc | ok |
| 3 | emmc_boot | 414795 | 451840 | data | ok |
| 4 | mboot_a, mboot_b | 1282607 | 2658304 | data | ok |
| 5 | vbmeta_a, vbmeta_b | 7621 | 12288 | data | ok |
| 6 | vbmeta_system_a, vbmeta_system_b | 2324 | 4096 | data | ok |
| 7 | boot_a, boot_b | 37623217 | 78643200 | Android bootimg, kernel, ramdisk (0x1000000), page size: 2048, cmdline | ok |
| 8 | optee_a, optee_b | 2806432 | 2806432 | data | ok |
| 9 | armfw_a, armfw_b | 77088 | 77088 | data | ok |
| 10 | dtbo_a, dtbo_b | 1686560 | 8388608 | data | ok |
| 11 | metadata | 66432 | 16777216 | Linux rev 1.0 ext4 filesystem data, UUID=cf1115cc-5b7f-474e-9b5e-796f4 | ok |
| 12 | linux_rootfs_a_a, linux_rootfs_a_b | 48313788 | 57671680 | Squashfs filesystem, little endian, version 4.0, lzo compressed, 48992 | ok |
| 13 | 3rd_a_a, 3rd_a_b | 818590 | 31457280 | Squashfs filesystem, little endian, version 4.0, lzo compressed, 69726 | ok |
| 14 | 3rd_rw | 124045 | 31457280 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc | ok |
| 15 | super | 98683490 | 104853608 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 16 | super | 94747289 | 96874572 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 17 | super | 99801099 | 104853580 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 18 | super | 90757037 | 96473164 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 19 | super | 100881754 | 104853580 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 20 | super | 91486887 | 96473164 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 21 | super | 98933685 | 104853580 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 22 | super | 101690006 | 104521844 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 23 | super | 98241869 | 104853580 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 24 | super | 96709850 | 104853648 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 25 | super | 99551359 | 104853632 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 26 | super | 31406792 | 37134440 | Android sparse image, version: 1.0, Total of 543232 4096-byte output b | ok |
| 27 | cache | 701 | 41036 | Android sparse image, version: 1.0, Total of 1280 4096-byte output blo | ok |
| 28 | tvservice_a, tvservice_b | 88538574 | 175112192 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc | ok |
| 29 | factory_a_a, factory_a_b | 58630 | 8388608 | Linux rev 1.0 ext2 filesystem data, UUID=8fdf0e8a-e9c9-4dbc-a793-f8a30 | ok |
| 30 | bootdata_a, bootdata_b | 5125425 | 41943040 | Linux rev 1.0 ext4 filesystem data, UUID=87818157-033f-4c84-be2b-21f21 | ok |
| 31 | persist | 103422 | 20971520 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc | ok |
| 32 | private | 49141 | 10485760 | Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc | ok |
| 33 | trddev | 8382 | 2097152 | data | ok |

## Other copied partitions (not published as binaries)
- tvconfig_a : 157286400 bytes, Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
- project_id : 5242880 bytes, Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
- emmc_boot : 451840 bytes, data
- mboot_a : 2658304 bytes, data
- vbmeta_a : 12288 bytes, data
- vbmeta_system_a : 4096 bytes, data
- boot_a : 78643200 bytes, Android bootimg, kernel, ramdisk (0x1000000), page size: 2048, cmdline (androidboot.boot_devices=1c660000.mtk-mmc-fcie bootvideo.enable=1 buildvariant=userdebug)
- optee_a : 2806432 bytes, data
- armfw_a : 77088 bytes, data
- dtbo_a : 8388608 bytes, data
- metadata : 16777216 bytes, Linux rev 1.0 ext4 filesystem data, UUID=cf1115cc-5b7f-474e-9b5e-796f485f4abd, volume name "metadata" (extents) (large files) (huge files)
- linux_rootfs_a_a : 57671680 bytes, Squashfs filesystem, little endian, version 4.0, lzo compressed, 48992685 bytes, 1124 inodes, blocksize: 131072 bytes, created: Wed Sep 30 07:47:49 2026
- 3rd_a_a : 31457280 bytes, Squashfs filesystem, little endian, version 4.0, lzo compressed, 697267 bytes, 19 inodes, blocksize: 131072 bytes, created: Wed Sep 30 07:47:50 2026
- 3rd_rw : 31457280 bytes, Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
- cache : 41036 bytes, Android sparse image, version: 1.0, Total of 1280 4096-byte output blocks in 4 input chunks.
- tvservice_a : 175112192 bytes, Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
- factory_a_a : 8388608 bytes, Linux rev 1.0 ext2 filesystem data, UUID=8fdf0e8a-e9c9-4dbc-a793-f8a30554e80c, volume name "vendor/factory" (extents) (large files) (huge files)
- bootdata_a : 41943040 bytes, Linux rev 1.0 ext4 filesystem data, UUID=87818157-033f-4c84-be2b-21f218b6b4d4, volume name "mnt/vendor/bootd/mnt/vendor/bootdata" (extents) (large files) (huge files)
- persist : 20971520 bytes, Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
- private : 10485760 bytes, Linux rev 1.0 ext4 filesystem data, UUID=57f8f4bc-abf4-655f-bf67-946fc0f9f25b (extents) (large files)
- trddev : 2097152 bytes, data
