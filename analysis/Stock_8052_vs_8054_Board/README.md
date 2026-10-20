# Stock Everycom 8052 versus 8054 — board configuration comparison

Read-only analysis of SHA256-verified original factory archives, decrypted PKGs, ext4 config files and DTBO.
8052 is the 1-HDMI profile; 8054 is the 2-HDMI/ToF profile used in two-port CineLux OEM firmware.
A two-HDMI FlixTone also displays 8054; this does not prove that its PCB matches the CineLux PCB.

## Android OEM settings

Values extracted from the independent verified vendor build.prop comparison.

| Property | Stock 8052 (Aug) | Stock 8054 (Sep) |
|---|---|---|
| ro.rjpj.machine.id | 8052 | 8054 |
| ro.rjpj.yunota.version | RUIOS.8052.1.0.1 | RUIOS.8054.1.0.1 |
| ro.product.ota | V618RJEN | V618RJENHD |
| ro.zeasn.devicetype | rjpj9660global | rjpj9660fordexp |
| ro.rjpj.hdmi.ports | HW6:HDMI | HW6:HDMI1,HW7:HDMI2 |
| ro.rjpj.hdmi.port.count | 1 | 2 |
| ro.rjpj.support.toffunction | 0 | 1 |
| ro.rjpj.autokeystone.poweron | 0 | 1 |
| ro.rjpj.autokeystone.move | 0 | 1 |
| ro.rjpj.yunota.url | mt9660/8052/8052_ota.json | mt9660/8054/8054_ota.json |
| ro.rjpj.yunota.zip | RJMT9660_firmware_8052.zip | RJMT9660_firmware_8054.zip |

## Important crosscheck: latest 8052 OTA from October 12, 2026

The **October 8052 OTA** has an OEM machine ID of **8052**, but its extracted stock configuration files are **byte-for-byte identical to the September 8054 factory image**:

| Config file | August stock 8052 vs September stock 8054 | October OTA 8052 vs September stock 8054 |
|---|---|---|
| `board.ini` | Different | Exact same SHA-256 |
| `tvconfig/config/dtbo_mapping.ini` | Different | Exact same SHA-256 |
| `bootdata/config/dtbo_mapping.ini` | Different | Exact same SHA-256 |

Therefore the changed GPIO table and DTBO ordering seen in the two original factory packages **cannot by themselves be attributed to the number of HDMI ports**. They may reflect a common manufacturer firmware revision subsequently delivered to the 8052 channel. This finding does **not** prove that physical boards or calibrations are interchangeable.

These checks rely on independent SHA-256 values from `analysis/RUIOS_8053_Hardware_Identity/8052.json` in the earlier research branch and the newly decoded factory 8054 files.

## Notes on RUIOS 8053 (not a hardware target)

Do not use 8053 as a base for a shared firmware. Its `A2dpSinkPlayerTCN` could be examined as an optional Bluetooth-audio receiver component, and `Provision` as a reference for first-boot setup, but functionality and dependencies have not been validated. Copying these older APKs directly into 8052/8054 is not recommended.

## Board pins and GPIO from board.ini

- Full SHA identical: False
- Modified config values: 9, added: 3, removed: 0.
- Text diff lines: 48.

| Group | Property | 8052 | 8054 |
|---|---|---|---|
| BOARD_GPIO_SETTING | BOARD_GPIO_19_ID | 0x363 | 0x336 |
| BOARD_GPIO_SETTING | BOARD_GPIO_20_ID | 0x33E | 0x363 |
| BOARD_GPIO_SETTING | BOARD_GPIO_21_ID | 0x33F | 0x33E |
| BOARD_GPIO_SETTING | BOARD_GPIO_22_ID | 0x340 | 0x33F |
| BOARD_GPIO_SETTING | BOARD_GPIO_NUM | 23 | 24 |
| BOARD_GPIO_SETTING | Board_GPIO_19_PAD_NO | 16 | 334 |
| BOARD_GPIO_SETTING | Board_GPIO_20_PAD_NO | 176 | 16 |
| BOARD_GPIO_SETTING | Board_GPIO_21_PAD_NO | 5 | 176 |
| BOARD_GPIO_SETTING | Board_GPIO_22_PAD_NO | 46 | 5 |

### Added in 8054

- `BOARD_GPIO_SETTING/BOARD_GPIO_23_ID=0x340`
- `BOARD_GPIO_SETTING/Board_GPIO_23_INVERTOR=0`
- `BOARD_GPIO_SETTING/Board_GPIO_23_PAD_NO=46`

### Removed in 8054


### Board.ini text diff

~~~diff
--- 8052
+++ 8054
@@ -280,5 +280,5 @@
 ###############################################
 [BOARD_GPIO_SETTING]
-BOARD_GPIO_NUM = 23;
+BOARD_GPIO_NUM = 24;
 
 BOARD_GPIO_0_ID = 0x300; #E_MI_SYS_BOARD_INFO_ID_GPIO_MUTE
@@ -438,23 +438,23 @@
 Board_GPIO_18_PAD_NO = 329; #PAD_PWM_PM
 
-#BOARD_GPIO_19_ID = 0x336; #E_MI_SYS_BOARD_INFO_ID_GPIO_AUDIO_HEADPHONE_MUTE
-#Board_GPIO_19_INVERTOR = 0;
-#Board_GPIO_19_PAD_NO = 352; #PAD_SAR0
-
-BOARD_GPIO_19_ID = 0x363; #E_MI_SYS_BOARD_INFO_ID_GPIO_WIFI_RESET
+BOARD_GPIO_19_ID = 0x336; #E_MI_SYS_BOARD_INFO_ID_GPIO_AUDIO_HEADPHONE_MUTE
 Board_GPIO_19_INVERTOR = 0;
-Board_GPIO_19_PAD_NO = 16; #PAD_GPIO10_PM
-
-BOARD_GPIO_20_ID = 0x33E; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_VBIAS
+Board_GPIO_19_PAD_NO = 334; #PAD_SAR0
+
+BOARD_GPIO_20_ID = 0x363; #E_MI_SYS_BOARD_INFO_ID_GPIO_WIFI_RESET
 Board_GPIO_20_INVERTOR = 0;
-Board_GPIO_20_PAD_NO = 176; #LCD_Vbias_En PAD_PCM_D0
-
-BOARD_GPIO_21_ID = 0x33F; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_STB
+Board_GPIO_20_PAD_NO = 16; #PAD_GPIO10_PM
+
+BOARD_GPIO_21_ID = 0x33E; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_VBIAS
 Board_GPIO_21_INVERTOR = 0;
-Board_GPIO_21_PAD_NO = 5; #LCD_STB PAD_GPIO5
-
-BOARD_GPIO_22_ID = 0x340; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_RST
+Board_GPIO_21_PAD_NO = 176; #LCD_Vbias_En PAD_PCM_D0
+
+BOARD_GPIO_22_ID = 0x33F; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_STB
 Board_GPIO_22_INVERTOR = 0;
-Board_GPIO_22_PAD_NO = 46; #LCD_RST PAD_GPIO46
+Board_GPIO_22_PAD_NO = 5; #LCD_STB PAD_GPIO5
+
+BOARD_GPIO_23_ID = 0x340; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_RST
+Board_GPIO_23_INVERTOR = 0;
+Board_GPIO_23_PAD_NO = 46; #LCD_RST PAD_GPIO46
 
 ###############################################
~~~

## DTBO content and indexes

- DTBO entries: [207, 207].
- Identical blobs regardless of order: 207.
- Matching at same index: 4.
- Different position: 203.

### Representative moves

| ID | 8052 position | 8054 position |
|---|---:|---:|
| 0 | 0 | 131 |
| 1 | 1 | 129 |
| 2 | 2 | 130 |
| 3 | 3 | 135 |
| 4 | 4 | 134 |
| 5 | 5 | 133 |
| 6 | 6 | 129 |
| 7 | 7 | 1 |
| 8 | 8 | 32 |
| 9 | 9 | 13 |
| 10 | 10 | 6 |
| 11 | 11 | 31 |
| 12 | 12 | 35 |
| 13 | 13 | 37 |
| 14 | 14 | 16 |
| 16 | 16 | 29 |
| 17 | 17 | 19 |
| 18 | 18 | 3 |

## Vendor TV configuration files

| File | Byte-identical? | Sizes (8052 / 8054) | Changed keys | Added / removed keys |
|---|---|---|---:|---|
| board.ini | False | 79601 / 79598 | 9 | 3 / 0 |
| tvconfig/dtbo_mapping.ini | False | 5557 / 5557 | 203 | 0 / 0 |
| bootdata/dtbo_mapping.ini | False | 5557 / 5557 | 203 | 0 / 0 |
| BasicSound_HDMI.ini | False | 6077 / 6077 | 0 | 0 / 0 |
| BasicSound_DTV.ini | False | 5886 / 5886 | 0 | 0 / 0 |
| BasicSound_MM.ini | False | 6015 / 6015 | 0 | 0 / 0 |
| ConfigDefaultValue.ini | False | 216002 / 216002 | 0 | 0 / 0 |
| gammatable_1.ini | False | 19336 / 19326 | 0 | 0 / 0 |
| pmu_mcs51_sign.bin | False | 65792 / 65792 | 0 | 0 / 0 |

### tvconfig/dtbo_mapping.ini

Same SHA256: False; modified config keys: 203; added: 0; removed: 0; text diff lines: 460.

~~~diff
--- 8052
+++ 8054
@@ -1,230 +1,230 @@
+[panel]
+vby1_8k_60_1div_osd_4k60_5bytes_trunk=0
+vby1_4k120_8div_4bytes=1
+lvds_fhd60=2
+vby1_4k120_2div_4bytes_Vtt2250_BOE_DLG240=3
+vby1_4k120_2div_4bytes_Vtt2250_ST5461D19_4=4
+vby1_4k120_2div_4bytes=5
+vby1_8k60_vrr=6
+vby1_4k60_1div_4bytes=7
+lvds_hd120=8
+vby1_4k120_2div_4bytes_Vtt2250=9
+vby1_4k1k240_2div_4bytes=10
+vby1_4k120_2div_5bytes=11
+vby1_fhd240=12
+vby1_4k1k120_1div_4bytes=13
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type0=14
+tcon_hd60=15
+vby1_4k144_2div_4bytes_reduce_blank=16
+vby1_fhd120=17
+vby1_4k120_2div_4bytes_Vtt2250_OLED=18
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type1=19
+lvds_hd60=20
+vby1_4k120_1div_4bytes=21
+tcon_4k120_ST7461D04_4_cust_ic=22
+vby1_8k_60_1div_osd_4k60_5bytes=23
+vby1_4k120_1div_4bytes_Vtt2250=24
+vby1_4k1k120_1div_bl0_4bytes=25
+vby1_8k60=26
+tcon_fhd60=27
+tcon_4k120_HV650QUB_E72_cust_ic=28
+vby1_4k120_2div_4bytes_osd_4k60_5bytes=29
+vby1_4k120_4div_4bytes_Vtt2250=30
+vby1_4k120_4div_4bytes=31
+vby1_cam=32
+vby1_fhd60=33
+vby1_4k60_1div_bl0_4bytes=34
+tcon_4k120_PT650GT02_3_cust_ic=35
+tcon=36
+vby1_4k144_2div_4bytes_high_clock=37
+vby1_4k144_1div_4bytes=38
+[mmap]
+mmap_mt5873_h1v1_an_1g_iommu=39
+mmap_mt5876_h1v1_an_2g_cma=40
+mmap_mt5873_h1v1_an_1point5g_iommu_cd=41
+mmap_mt5879_h1v1_aosp_4g_iommu_cd=42
+mmap_mt5897_h1v1_linux_3g=43
+mmap_mt5879_h3v1_aosp_3g_k32=44
+mmap_mt5879_h1v1_aosp_3g_iommu=45
+mmap_mt5873_h1v1_an_2g_iommu_cd=46
+mmap_mt5873_h1v1_an_1g_midgard=47
+mmap_mt5873_h1v1_an_1g_iommu_cd=48
+mmap_mt5873_h1v1_an_2g_cma=49
+mmap_mt5873_h1v1_an_2g_iommu=50
+mmap_mt5897_h1v1_an_2g=51
+mmap_mt5879_h1v1_aosp_6g_iommu=52
+mmap_mt5873_h1v1_linux_1g_iommu=53
+mmap_mt5879_mtk_2g_an_iommu_h1v1=54
+mmap_mt5897_haps_an_2g=55
+mmap_mt5879_h1v1_linux_3g_iommu=56
+mmap_mt5896_h1v1_an_6g=57
+mmap_mt5879_h1v1_aosp_4g_iommu=58
+mmap_mt5873_h1v1_linux_1point5g_iommu=59
+mmap_mt5873_h1v1_an_1point5g_midgard=60
+mmap_mt5873_h1v1_linux_2g_iommu=61
+mmap_mt5879_h1v1_aosp_3g_iommu_cd=62
+mmap_mt5873_h1v1_an_3g_iommu=63
+mmap_mt5896_haps_an_2g=64
+mmap_mt5873_h1v1_an_4g_iommu_cd=65
+mmap_mt5876_h1v1_an_2g_iommu=66
+mmap_mt5879_h1v1_linux_4g_iommu=67
+mmap_mt5873_h1v1_an_2g_midgard=68
+mmap_mt5873_h1v1_an_2g_static_only=69
+mmap_mt5873_h1v1_an_4g_iommu=70
+mmap_mt5876_h1v1_an_2g_static_only=71
+mmap_mt5873_h1v1_an_1point5g_iommu=72
+[ldm]
+ldm_iw7039=73
+ldm_iw7038=74
+ldm_BCON=75
+ldm_iw7027=76
+ldm_DCON=77
+ldm_128x128=78
+[pmu]
+pmu_mcs51_rproc=79
+pmu_cm4_rproc=80
+[vad]
+vad_cm4_rproc=81
~~~

### bootdata/dtbo_mapping.ini

Same SHA256: False; modified config keys: 203; added: 0; removed: 0; text diff lines: 460.

~~~diff
--- 8052
+++ 8054
@@ -1,230 +1,230 @@
+[panel]
+vby1_8k_60_1div_osd_4k60_5bytes_trunk=0
+vby1_4k120_8div_4bytes=1
+lvds_fhd60=2
+vby1_4k120_2div_4bytes_Vtt2250_BOE_DLG240=3
+vby1_4k120_2div_4bytes_Vtt2250_ST5461D19_4=4
+vby1_4k120_2div_4bytes=5
+vby1_8k60_vrr=6
+vby1_4k60_1div_4bytes=7
+lvds_hd120=8
+vby1_4k120_2div_4bytes_Vtt2250=9
+vby1_4k1k240_2div_4bytes=10
+vby1_4k120_2div_5bytes=11
+vby1_fhd240=12
+vby1_4k1k120_1div_4bytes=13
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type0=14
+tcon_hd60=15
+vby1_4k144_2div_4bytes_reduce_blank=16
+vby1_fhd120=17
+vby1_4k120_2div_4bytes_Vtt2250_OLED=18
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type1=19
+lvds_hd60=20
+vby1_4k120_1div_4bytes=21
+tcon_4k120_ST7461D04_4_cust_ic=22
+vby1_8k_60_1div_osd_4k60_5bytes=23
+vby1_4k120_1div_4bytes_Vtt2250=24
+vby1_4k1k120_1div_bl0_4bytes=25
+vby1_8k60=26
+tcon_fhd60=27
+tcon_4k120_HV650QUB_E72_cust_ic=28
+vby1_4k120_2div_4bytes_osd_4k60_5bytes=29
+vby1_4k120_4div_4bytes_Vtt2250=30
+vby1_4k120_4div_4bytes=31
+vby1_cam=32
+vby1_fhd60=33
+vby1_4k60_1div_bl0_4bytes=34
+tcon_4k120_PT650GT02_3_cust_ic=35
+tcon=36
+vby1_4k144_2div_4bytes_high_clock=37
+vby1_4k144_1div_4bytes=38
+[mmap]
+mmap_mt5873_h1v1_an_1g_iommu=39
+mmap_mt5876_h1v1_an_2g_cma=40
+mmap_mt5873_h1v1_an_1point5g_iommu_cd=41
+mmap_mt5879_h1v1_aosp_4g_iommu_cd=42
+mmap_mt5897_h1v1_linux_3g=43
+mmap_mt5879_h3v1_aosp_3g_k32=44
+mmap_mt5879_h1v1_aosp_3g_iommu=45
+mmap_mt5873_h1v1_an_2g_iommu_cd=46
+mmap_mt5873_h1v1_an_1g_midgard=47
+mmap_mt5873_h1v1_an_1g_iommu_cd=48
+mmap_mt5873_h1v1_an_2g_cma=49
+mmap_mt5873_h1v1_an_2g_iommu=50
+mmap_mt5897_h1v1_an_2g=51
+mmap_mt5879_h1v1_aosp_6g_iommu=52
+mmap_mt5873_h1v1_linux_1g_iommu=53
+mmap_mt5879_mtk_2g_an_iommu_h1v1=54
+mmap_mt5897_haps_an_2g=55
+mmap_mt5879_h1v1_linux_3g_iommu=56
+mmap_mt5896_h1v1_an_6g=57
+mmap_mt5879_h1v1_aosp_4g_iommu=58
+mmap_mt5873_h1v1_linux_1point5g_iommu=59
+mmap_mt5873_h1v1_an_1point5g_midgard=60
+mmap_mt5873_h1v1_linux_2g_iommu=61
+mmap_mt5879_h1v1_aosp_3g_iommu_cd=62
+mmap_mt5873_h1v1_an_3g_iommu=63
+mmap_mt5896_haps_an_2g=64
+mmap_mt5873_h1v1_an_4g_iommu_cd=65
+mmap_mt5876_h1v1_an_2g_iommu=66
+mmap_mt5879_h1v1_linux_4g_iommu=67
+mmap_mt5873_h1v1_an_2g_midgard=68
+mmap_mt5873_h1v1_an_2g_static_only=69
+mmap_mt5873_h1v1_an_4g_iommu=70
+mmap_mt5876_h1v1_an_2g_static_only=71
+mmap_mt5873_h1v1_an_1point5g_iommu=72
+[ldm]
+ldm_iw7039=73
+ldm_iw7038=74
+ldm_BCON=75
+ldm_iw7027=76
+ldm_DCON=77
+ldm_128x128=78
+[pmu]
+pmu_mcs51_rproc=79
+pmu_cm4_rproc=80
+[vad]
+vad_cm4_rproc=81
~~~

### ConfigDefaultValue.ini

Same SHA256: False; modified config keys: 0; added: 0; removed: 0; text diff lines: 86.

~~~diff
--- 8052
+++ 8054
@@ -684,5 +684,5 @@
 InputSourceID[0]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -691,5 +691,5 @@
 InputSourceID[1]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -698,5 +698,5 @@
 InputSourceID[2]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -705,5 +705,5 @@
 InputSourceID[3]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -712,5 +712,5 @@
 InputSourceID[4]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -719,5 +719,5 @@
 InputSourceID[5]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -726,5 +726,5 @@
 InputSourceID[6]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -733,5 +733,5 @@
 InputSourceID[7]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -740,5 +740,5 @@
 InputSourceID[8]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -747,5 +747,5 @@
 InputSourceID[9]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -754,5 +754,5 @@
 InputSourceID[10]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
@@ -761,5 +761,5 @@
 InputSourceID[11]=\
 50,60,70,\
-80,75,50,\
+70,75,50,\
 50,50,40,\
 60,40,50,\
~~~

### BasicSound_HDMI.ini

Same SHA256: False; modified config keys: 0; added: 0; removed: 0; text diff lines: 27.

~~~diff
--- 8052
+++ 8054
@@ -163,14 +163,14 @@
     { \
         0x7F00, \
-        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x1200, \
-        0x11C0, 0x1180, 0x1160, 0x1120, 0x1100, 0x10C0, 0x1080, 0x1060, 0x1020, 0x1000, \
-        0x0FC0, 0x0F80, 0x0F60, 0x0F20, 0x0F00, 0x0EC0, 0x0E80, 0x0E60, 0x0E20, 0x0E00, \
-        0x0DC0, 0x0D80, 0x0D60, 0x0D20, 0x0D00, 0x0CC0, 0x0C80, 0x0C60, 0x0C20, 0x0C00, \
-        0x0BE0, 0x0BC0, 0x0BA0, 0x0B80, 0x0B80, 0x0B60, 0x0B40, 0x0B20, 0x0B00, 0x0B00, \
-        0x0AE0, 0x0AC0, 0x0AA0, 0x0A80, 0x0A80, 0x0A60, 0x0A40, 0x0A20, 0x0A00, 0x0A00, \
-        0x09E0, 0x09C0, 0x09A0, 0x0980, 0x0980, 0x0960, 0x0940, 0x0920, 0x0900, 0x0900, \
-        0x08E0, 0x08C0, 0x08A0, 0x0880, 0x0880, 0x0860, 0x0840, 0x0820, 0x0800, 0x0800, \
-        0x07E0, 0x07C0, 0x07A0, 0x0780, 0x0780, 0x0760, 0x0740, 0x0720, 0x0700, 0x0700, \
-        0x06E0, 0x06C0, 0x06A0, 0x0680, 0x0680, 0x0660, 0x0640, 0x0620, 0x0600, 0x0600  \
+        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x3200, \
+        0x3000, 0x2E00, 0x2D00, 0x2C00, 0x2B00, 0x2A00, 0x2900, 0x2800, 0x2700, 0x2600, \
+        0x2500, 0x2400, 0x2300, 0x2200, 0x2100, 0x2000, 0x1F00, 0x1E80, 0x1E00, 0x1D80, \
+        0x1D00, 0x1C80, 0x1C00, 0x1B80, 0x1B00, 0x1A80, 0x1A00, 0x1980, 0x1900, 0x1880, \
+        0x1800, 0x1780, 0x1700, 0x1680, 0x1600, 0x1580, 0x1540, 0x1500, 0x14C0, 0x1480, \
+        0x1440, 0x1400, 0x13C0, 0x1380, 0x1340, 0x1300, 0x12C0, 0x1280, 0x1240, 0x1200, \
+        0x11C0, 0x1180, 0x1140, 0x1100, 0x10C0, 0x1080, 0x1040, 0x1000, 0x0FE0, 0x0FC0, \
+        0x0FA0, 0x0F80, 0x0F60, 0x0F40, 0x0F20, 0x0F00, 0x0EE0, 0x0EC0, 0x0EA0, 0x0E80, \
+        0x0E60, 0x0E40, 0x0E20, 0x0E00, 0x0DE0, 0x0DC0, 0x0DA0, 0x0D80, 0x0D60, 0x0D40, \
+        0x0D20, 0x0D00, 0x0CE0, 0x0CC0, 0x0CA0, 0x0C80, 0x0C60, 0x0C40, 0x0C20, 0x0C00  \
     }
 
~~~

### BasicSound_DTV.ini

Same SHA256: False; modified config keys: 0; added: 0; removed: 0; text diff lines: 27.

~~~diff
--- 8052
+++ 8054
@@ -163,14 +163,14 @@
     { \
         0x7F00, \
-        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x1200, \
-        0x11C0, 0x1180, 0x1160, 0x1120, 0x1100, 0x10C0, 0x1080, 0x1060, 0x1020, 0x1000, \
-        0x0FC0, 0x0F80, 0x0F60, 0x0F20, 0x0F00, 0x0EC0, 0x0E80, 0x0E60, 0x0E20, 0x0E00, \
-        0x0DC0, 0x0D80, 0x0D60, 0x0D20, 0x0D00, 0x0CC0, 0x0C80, 0x0C60, 0x0C20, 0x0C00, \
-        0x0BE0, 0x0BC0, 0x0BA0, 0x0B80, 0x0B80, 0x0B60, 0x0B40, 0x0B20, 0x0B00, 0x0B00, \
-        0x0AE0, 0x0AC0, 0x0AA0, 0x0A80, 0x0A80, 0x0A60, 0x0A40, 0x0A20, 0x0A00, 0x0A00, \
-        0x09E0, 0x09C0, 0x09A0, 0x0980, 0x0980, 0x0960, 0x0940, 0x0920, 0x0900, 0x0900, \
-        0x08E0, 0x08C0, 0x08A0, 0x0880, 0x0880, 0x0860, 0x0840, 0x0820, 0x0800, 0x0800, \
-        0x07E0, 0x07C0, 0x07A0, 0x0780, 0x0780, 0x0760, 0x0740, 0x0720, 0x0700, 0x0700, \
-        0x06E0, 0x06C0, 0x06A0, 0x0680, 0x0680, 0x0660, 0x0640, 0x0620, 0x0600, 0x0600  \
+        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x3200, \
+        0x3000, 0x2E00, 0x2D00, 0x2C00, 0x2B00, 0x2A00, 0x2900, 0x2800, 0x2700, 0x2600, \
+        0x2500, 0x2400, 0x2300, 0x2200, 0x2100, 0x2000, 0x1F00, 0x1E80, 0x1E00, 0x1D80, \
+        0x1D00, 0x1C80, 0x1C00, 0x1B80, 0x1B00, 0x1A80, 0x1A00, 0x1980, 0x1900, 0x1880, \
+        0x1800, 0x1780, 0x1700, 0x1680, 0x1600, 0x1580, 0x1540, 0x1500, 0x14C0, 0x1480, \
+        0x1440, 0x1400, 0x13C0, 0x1380, 0x1340, 0x1300, 0x12C0, 0x1280, 0x1240, 0x1200, \
+        0x11C0, 0x1180, 0x1140, 0x1100, 0x10C0, 0x1080, 0x1040, 0x1000, 0x0FE0, 0x0FC0, \
+        0x0FA0, 0x0F80, 0x0F60, 0x0F40, 0x0F20, 0x0F00, 0x0EE0, 0x0EC0, 0x0EA0, 0x0E80, \
+        0x0E60, 0x0E40, 0x0E20, 0x0E00, 0x0DE0, 0x0DC0, 0x0DA0, 0x0D80, 0x0D60, 0x0D40, \
+        0x0D20, 0x0D00, 0x0CE0, 0x0CC0, 0x0CA0, 0x0C80, 0x0C60, 0x0C40, 0x0C20, 0x0C00  \
     }
 
~~~

### BasicSound_MM.ini

Same SHA256: False; modified config keys: 0; added: 0; removed: 0; text diff lines: 27.

~~~diff
--- 8052
+++ 8054
@@ -174,14 +174,14 @@
     { \
         0x7F00, \
-        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x1200, \
-        0x11C0, 0x1180, 0x1160, 0x1120, 0x1100, 0x10C0, 0x1080, 0x1060, 0x1020, 0x1000, \
-        0x0FC0, 0x0F80, 0x0F60, 0x0F20, 0x0F00, 0x0EC0, 0x0E80, 0x0E60, 0x0E20, 0x0E00, \
-        0x0DC0, 0x0D80, 0x0D60, 0x0D20, 0x0D00, 0x0CC0, 0x0C80, 0x0C60, 0x0C20, 0x0C00, \
-        0x0BE0, 0x0BC0, 0x0BA0, 0x0B80, 0x0B80, 0x0B60, 0x0B40, 0x0B20, 0x0B00, 0x0B00, \
-        0x0AE0, 0x0AC0, 0x0AA0, 0x0A80, 0x0A80, 0x0A60, 0x0A40, 0x0A20, 0x0A00, 0x0A00, \
-        0x09E0, 0x09C0, 0x09A0, 0x0980, 0x0980, 0x0960, 0x0940, 0x0920, 0x0900, 0x0900, \
-        0x08E0, 0x08C0, 0x08A0, 0x0880, 0x0880, 0x0860, 0x0840, 0x0820, 0x0800, 0x0800, \
-        0x07E0, 0x07C0, 0x07A0, 0x0780, 0x0780, 0x0760, 0x0740, 0x0720, 0x0700, 0x0700, \
-        0x06E0, 0x06C0, 0x06A0, 0x0680, 0x0680, 0x0660, 0x0640, 0x0620, 0x0600, 0x0600  \
+        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x3200, \
+        0x3000, 0x2E00, 0x2D00, 0x2C00, 0x2B00, 0x2A00, 0x2900, 0x2800, 0x2700, 0x2600, \
+        0x2500, 0x2400, 0x2300, 0x2200, 0x2100, 0x2000, 0x1F00, 0x1E80, 0x1E00, 0x1D80, \
+        0x1D00, 0x1C80, 0x1C00, 0x1B80, 0x1B00, 0x1A80, 0x1A00, 0x1980, 0x1900, 0x1880, \
+        0x1800, 0x1780, 0x1700, 0x1680, 0x1600, 0x1580, 0x1540, 0x1500, 0x14C0, 0x1480, \
+        0x1440, 0x1400, 0x13C0, 0x1380, 0x1340, 0x1300, 0x12C0, 0x1280, 0x1240, 0x1200, \
+        0x11C0, 0x1180, 0x1140, 0x1100, 0x10C0, 0x1080, 0x1040, 0x1000, 0x0FE0, 0x0FC0, \
+        0x0FA0, 0x0F80, 0x0F60, 0x0F40, 0x0F20, 0x0F00, 0x0EE0, 0x0EC0, 0x0EA0, 0x0E80, \
+        0x0E60, 0x0E40, 0x0E20, 0x0E00, 0x0DE0, 0x0DC0, 0x0DA0, 0x0D80, 0x0D60, 0x0D40, \
+        0x0D20, 0x0D00, 0x0CE0, 0x0CC0, 0x0CA0, 0x0C80, 0x0C60, 0x0C40, 0x0C20, 0x0C00  \
     }
 
~~~

## Software differences relevant to porting

### Applications added in the 8054 factory image

- `system_a/system/app/KuSetupWizard/KuSetupWizard.apk`
- `system_a/system/preinstall_del/AmazonPrimeVideo_v3.0.459.345.apk`
- `system_a/system/preinstall_del/Netfix_v8.110.0.apk`
- `system_a/system/preinstall_del/YouTube_v4.40.313.apk.apk`

### Applications present only in 8052

- `system_ext_a/priv-app/Provision/Provision.apk`

### Different manufacturer packages

- `system_a/system/app/KuSettings/KuSettings.apk`
- `system_a/system/app/KuSourceRJ/KuSourceRJ.apk`
- `system_a/system/app/RuiAutoFocus/RuiAutoFocus.apk`
- `system_a/system/app/trdservice/trdservice.apk`
- `system_a/system/app/zxlauncher/zxlauncher.apk`
- `system_a/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk`
- `system_ext_a/app/Factory/Factory.apk`
- `system_ext_a/priv-app/TvSettingsPlus/TvSettingsPlus.apk`

## Engineering conclusions

- Keep one shared Android codebase with separate board profiles 8052 and 8054.
- A DTBO with the same blobs but different entry order requires its matching DTBO mapping.
- Preserve board GPIO, PMU, HDMI audio, focus/ToF and panel defaults per variant.
- Do not assume identical physical PCBs from a common hardware machine ID.
- OTA 8053 is excluded as a supported hardware profile; consider its APKs only for optional software features.
- No image was installed and no device state or calibration was modified.

