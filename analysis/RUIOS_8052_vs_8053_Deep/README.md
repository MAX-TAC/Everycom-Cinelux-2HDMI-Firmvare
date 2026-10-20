# Deep comparison of public RUIOS 8052 and 8053 OTA builds

Static audit only: verified ZIPs, two differing DTBO blobs, manufacturer TV configuration, Android image inventory.

## Versions and device identity

| | RUIOS 8052 | RUIOS 8053 |
|---|---|---|
| Public OTA | RUIOS.8052.1.0.4 | RUIOS.8053.1.0.0 |
| Android build | eng.suhaix.20261012.025220 | eng.luzhih.20260612.083454 |
| Android / pre-device | 13 / mt5873 | 13 / mt5873 |
| Hardware model | Everycom 1 HDMI (photographic confirmation) | Unknown OEM product |
| OTA machine ID | 8052 | 8053 |
| Configured HDMI ports | 1 | not specified in vendor build.prop |
| ToF function | 0 | not specified in vendor build.prop |
| Autokeystone power on | 0 | 0 |

## DTBO overview

Both DTBO images contain 207 entries, of which **205 exact DTB contents** are common as a multiset.
These two unmatched blob pairs are matched by DTS line similarity, NOT by entry index.

### Changed DTBO profile 1: 10704 → 10704 bytes

- 8052 entry index/ID: 34/34; SHA256: ce500de3b701285f471ad473cc1c7c0e32119e2a5dba28a676335b3167a20c15
- 8053 entry index/ID: 41/41; SHA256: 9727bc37fa26fab29a11d326804906c6e51ae50e697fd6082974adf97b8e7dd9
- DTS line similarity: 94.309%; unified-diff lines: 135

~~~diff
--- 8052
+++ 8053
@@ -27,12 +27,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				max_v_total_panelprotect = <0xb54>;
 				min_v_total_panelprotect = <0x898>;
 				typ_clk_high = <0x00>;
@@ -65,12 +65,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				max_v_total_panelprotect = <0xb54>;
 				min_v_total_panelprotect = <0x898>;
 				typ_clk_high = <0x00>;
@@ -339,12 +339,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				typ_clk_high = <0x00>;
 				typ_clk_low = <0x2367b880>;
 				output_format = <0x00>;
@@ -372,12 +372,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				typ_clk_high = <0x00>;
 				typ_clk_low = <0x2367b880>;
 				output_format = <0x00>;
@@ -405,12 +405,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				typ_clk_high = <0x00>;
 				typ_clk_low = <0x2367b880>;
 				output_format = <0x00>;
@@ -447,12 +447,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				typ_clk_high = <0x00>;
 				typ_clk_low = <0x2367b880>;
 				output_format = <0x08>;
@@ -471,12 +471,12 @@
 				de_vstart = <0x53>;
 				resolution_width = <0xf00>;
 				resolution_height = <0x870>;
-				max_h_total = <0x1162>;
-				typ_h_total = <0x1130>;
-				min_h_total = <0x10fe>;
-				max_v_total = <0x8fc>;
-				typ_v_total = <0x8ca>;
-				min_v_total = <0x898>;
+				max_h_total = <0x11f8>;
+				typ_h_total = <0x1130>;
+				min_h_total = <0x10cc>;
+				max_v_total = <0x92e>;
+				typ_v_total = <0x8ca>;
+				min_v_total = <0x866>;
 				typ_clk_high = <0x00>;
 				typ_clk_low = <0x2367b880>;
 			};
~~~

### Changed DTBO profile 2: 1004 → 972 bytes

- 8052 entry index/ID: 117/117; SHA256: e1242cf41e005a442146439184f36e119526231c0550a378bc2518e5585fbead
- 8053 entry index/ID: 51/51; SHA256: bb87edc8b839f2ebac6bd38aec7a058f1fc1d14eb0c3420d4b2f2ef7f694ab99
- DTS line similarity: 97.297%; unified-diff lines: 11

~~~diff
--- 8052
+++ 8053
@@ -26,7 +26,7 @@
 				protocol = <0x01>;
 				keymap_name = "trd-tv";
 				customercode = <0x1fe>;
-				ir_key_table = <0x74 0x00 0x67 0x0d 0x69 0x10 0x1c 0x11 0x6a 0x12 0x6c 0x15 0x9e 0x0e 0x66 0x41 0x8b 0x0c 0x73 0x06 0x72 0x09 0x71 0x1a 0xd9 0x66 0x2f3 0xdc 0x2e8 0x73 0x2e9 0x72 0x2ea 0x05 0x2fa 0x0a 0x2fb 0x0b 0x2fc 0x1c 0x2fd 0x1e>;
+				ir_key_table = <0x74 0x00 0x67 0x0d 0x69 0x10 0x1c 0x11 0x6a 0x12 0x6c 0x15 0x9e 0x0e 0x66 0x41 0x8b 0x0c 0x73 0x06 0x72 0x09 0x71 0x1a 0xd9 0x66 0x2f3 0xdc 0x2e8 0x73 0x2e9 0x72 0x2ea 0x05>;
 			};
 		};
 	};
~~~

## TV configuration differences

### board_ini

- Equal SHA256: **False**. Sizes: [79598, 79601].
- Total diff lines: 44; text similarity: 99.11%.

~~~diff
--- 8052
+++ 8053
@@ -281,3 +281,3 @@
 [BOARD_GPIO_SETTING]
-BOARD_GPIO_NUM = 24;
+BOARD_GPIO_NUM = 23;
 
@@ -439,21 +439,21 @@
 
-BOARD_GPIO_19_ID = 0x336; #E_MI_SYS_BOARD_INFO_ID_GPIO_AUDIO_HEADPHONE_MUTE
+#BOARD_GPIO_19_ID = 0x336; #E_MI_SYS_BOARD_INFO_ID_GPIO_AUDIO_HEADPHONE_MUTE
+#Board_GPIO_19_INVERTOR = 0;
+#Board_GPIO_19_PAD_NO = 352; #PAD_SAR0
+
+BOARD_GPIO_19_ID = 0x363; #E_MI_SYS_BOARD_INFO_ID_GPIO_WIFI_RESET
 Board_GPIO_19_INVERTOR = 0;
-Board_GPIO_19_PAD_NO = 334; #PAD_SAR0
-
-BOARD_GPIO_20_ID = 0x363; #E_MI_SYS_BOARD_INFO_ID_GPIO_WIFI_RESET
+Board_GPIO_19_PAD_NO = 16; #PAD_GPIO10_PM
+
+BOARD_GPIO_20_ID = 0x33E; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_VBIAS
 Board_GPIO_20_INVERTOR = 0;
-Board_GPIO_20_PAD_NO = 16; #PAD_GPIO10_PM
-
-BOARD_GPIO_21_ID = 0x33E; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_VBIAS
+Board_GPIO_20_PAD_NO = 176; #LCD_Vbias_En PAD_PCM_D0
+
+BOARD_GPIO_21_ID = 0x33F; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_STB
 Board_GPIO_21_INVERTOR = 0;
-Board_GPIO_21_PAD_NO = 176; #LCD_Vbias_En PAD_PCM_D0
-
-BOARD_GPIO_22_ID = 0x33F; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_STB
+Board_GPIO_21_PAD_NO = 5; #LCD_STB PAD_GPIO5
+
+BOARD_GPIO_22_ID = 0x340; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_RST
 Board_GPIO_22_INVERTOR = 0;
-Board_GPIO_22_PAD_NO = 5; #LCD_STB PAD_GPIO5
-
-BOARD_GPIO_23_ID = 0x340; #E_MI_SYS_BOARD_INFO_ID_GPIO_PANEL_RST
-Board_GPIO_23_INVERTOR = 0;
-Board_GPIO_23_PAD_NO = 46; #LCD_RST PAD_GPIO46
+Board_GPIO_22_PAD_NO = 46; #LCD_RST PAD_GPIO46
 
~~~

### dtbo_mapping_tv

- Equal SHA256: **False**. Sizes: [5557, 5557].
- Total diff lines: 456; text similarity: 3.04%.

~~~diff
--- 8052
+++ 8053
@@ -1,230 +1,230 @@
+[amp]
+ntp8825_mt5873_h1v1=0
+rt9114_mt5897_h1v1=1
+rt9120_mt5876_h1v1=2
+rt9120_mt5873_h1v1=3
+rt9120_mt5879_h1v1=4
+rt9114_mt5896_h1v1=5
+rt9114_mt5896_h2v1=6
 [panel]
-vby1_8k_60_1div_osd_4k60_5bytes_trunk=0
-vby1_4k120_8div_4bytes=1
-lvds_fhd60=2
-vby1_4k120_2div_4bytes_Vtt2250_BOE_DLG240=3
-vby1_4k120_2div_4bytes_Vtt2250_ST5461D19_4=4
-vby1_4k120_2div_4bytes=5
-vby1_8k60_vrr=6
-vby1_4k60_1div_4bytes=7
-lvds_hd120=8
-vby1_4k120_2div_4bytes_Vtt2250=9
-vby1_4k1k240_2div_4bytes=10
-vby1_4k120_2div_5bytes=11
-vby1_fhd240=12
-vby1_4k1k120_1div_4bytes=13
-vby1_4k120_2div_4bytes_osd_4k60_4bytes_type0=14
+vby1_4k120_8div_4bytes=7
+vby1_cam=8
+vby1_4k1k120_1div_4bytes=9
+vby1_8k60_vrr=10
+vby1_4k120_4div_4bytes=11
+tcon_4k120_PT650GT02_3_cust_ic=12
+vby1_4k144_2div_4bytes_high_clock=13
+vby1_4k144_2div_4bytes_reduce_blank=14
 tcon_hd60=15
-vby1_4k144_2div_4bytes_reduce_blank=16
-vby1_fhd120=17
-vby1_4k120_2div_4bytes_Vtt2250_OLED=18
-vby1_4k120_2div_4bytes_osd_4k60_4bytes_type1=19
-lvds_hd60=20
-vby1_4k120_1div_4bytes=21
+vby1_4k120_2div_4bytes_osd_4k60_5bytes=16
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type1=17
+vby1_4k120_2div_4bytes_Vtt2250_BOE_DLG240=18
+vby1_4k120_2div_4bytes_Vtt2250_ST5461D19_4=19
+vby1_fhd240=20
+vby1_8k60=21
 tcon_4k120_ST7461D04_4_cust_ic=22
-vby1_8k_60_1div_osd_4k60_5bytes=23
-vby1_4k120_1div_4bytes_Vtt2250=24
-vby1_4k1k120_1div_bl0_4bytes=25
-vby1_8k60=26
-tcon_fhd60=27
-tcon_4k120_HV650QUB_E72_cust_ic=28
-vby1_4k120_2div_4bytes_osd_4k60_5bytes=29
-vby1_4k120_4div_4bytes_Vtt2250=30
-vby1_4k120_4div_4bytes=31
-vby1_cam=32
-vby1_fhd60=33
-vby1_4k60_1div_bl0_4bytes=34
-tcon_4k120_PT650GT02_3_cust_ic=35
-tcon=36
-vby1_4k144_2div_4bytes_high_clock=37
-vby1_4k144_1div_4bytes=38
+vby1_4k144_1div_4bytes=23
+lvds_hd60=24
+vby1_fhd120=25
+vby1_4k1k240_2div_4bytes=26
+lvds_hd120=27
+vby1_fhd60=28
+vby1_8k_60_1div_osd_4k60_5bytes_trunk=29
+tcon=30
+lvds_fhd60=31
+vby1_4k120_2div_4bytes_Vtt2250_OLED=32
+vby1_4k120_4div_4bytes_Vtt2250=33
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type0=34
+vby1_4k120_2div_4bytes=35
+vby1_4k120_1div_4bytes=36
+vby1_4k120_1div_4bytes_Vtt2250=37
+tcon_fhd60=38
+vby1_4k1k120_1div_bl0_4bytes=39
+vby1_4k120_2div_4bytes_Vtt2250=40
+vby1_4k60_1div_bl0_4bytes=41
+vby1_4k60_1div_4bytes=42
+vby1_4k120_2div_5bytes=43
+vby1_8k_60_1div_osd_4k60_5bytes=44
+tcon_4k120_HV650QUB_E72_cust_ic=45
+[iommu]
+iommu_4k=46
+iommu_8k=47
+[sample]
+sample=48
+sample2=49
+[ir]
+ir_customize0=50
+ir_base=51
+[wakeup_key]
+wakeup_ww=52
+wakeup_base=53
+wakeup_linux=54
+[vad]
+vad_cm4_rproc=55
+vad_HK=56
+vad_rv33_rproc=57
+vad_NULL_rproc=58
+[ldm]
+ldm_iw7027=59
+ldm_DCON=60
+ldm_iw7038=61
+ldm_128x128=62
+ldm_BCON=63
+ldm_iw7039=64
 [mmap]
-mmap_mt5873_h1v1_an_1g_iommu=39
-mmap_mt5876_h1v1_an_2g_cma=40
-mmap_mt5873_h1v1_an_1point5g_iommu_cd=41
-mmap_mt5879_h1v1_aosp_4g_iommu_cd=42
-mmap_mt5897_h1v1_linux_3g=43
-mmap_mt5879_h3v1_aosp_3g_k32=44
-mmap_mt5879_h1v1_aosp_3g_iommu=45
-mmap_mt5873_h1v1_an_2g_iommu_cd=46
-mmap_mt5873_h1v1_an_1g_midgard=47
-mmap_mt5873_h1v1_an_1g_iommu_cd=48
-mmap_mt5873_h1v1_an_2g_cma=49
-mmap_mt5873_h1v1_an_2g_iommu=50
-mmap_mt5897_h1v1_an_2g=51
-mmap_mt5879_h1v1_aosp_6g_iommu=52
-mmap_mt5873_h1v1_linux_1g_iommu=53
-mmap_mt5879_mtk_2g_an_iommu_h1v1=54
-mmap_mt5897_haps_an_2g=55
-mmap_mt5879_h1v1_linux_3g_iommu=56
-mmap_mt5896_h1v1_an_6g=57
-mmap_mt5879_h1v1_aosp_4g_iommu=58
-mmap_mt5873_h1v1_linux_1point5g_iommu=59
-mmap_mt5873_h1v1_an_1point5g_midgard=60
-mmap_mt5873_h1v1_linux_2g_iommu=61
-mmap_mt5879_h1v1_aosp_3g_iommu_cd=62
-mmap_mt5873_h1v1_an_3g_iommu=63
-mmap_mt5896_haps_an_2g=64
-mmap_mt5873_h1v1_an_4g_iommu_cd=65
-mmap_mt5876_h1v1_an_2g_iommu=66
+mmap_mt5876_h1v1_an_2g_cma=65
+mmap_mt5873_h1v1_an_2g_static_only=66
 mmap_mt5879_h1v1_linux_4g_iommu=67
-mmap_mt5873_h1v1_an_2g_midgard=68
-mmap_mt5873_h1v1_an_2g_static_only=69
-mmap_mt5873_h1v1_an_4g_iommu=70
-mmap_mt5876_h1v1_an_2g_static_only=71
-mmap_mt5873_h1v1_an_1point5g_iommu=72
-[ldm]
-ldm_iw7039=73
-ldm_iw7038=74
-ldm_BCON=75
-ldm_iw7027=76
-ldm_DCON=77
-ldm_128x128=78
+mmap_mt5873_h1v1_an_4g_iommu_cd=68
+mmap_mt5897_h1v1_linux_3g=69
+mmap_mt5873_h1v1_an_2g_iommu=70
~~~

### dtbo_mapping_boot

- Equal SHA256: **False**. Sizes: [5557, 5557].
- Total diff lines: 456; text similarity: 3.04%.

~~~diff
--- 8052
+++ 8053
@@ -1,230 +1,230 @@
+[amp]
+ntp8825_mt5873_h1v1=0
+rt9114_mt5897_h1v1=1
+rt9120_mt5876_h1v1=2
+rt9120_mt5873_h1v1=3
+rt9120_mt5879_h1v1=4
+rt9114_mt5896_h1v1=5
+rt9114_mt5896_h2v1=6
 [panel]
-vby1_8k_60_1div_osd_4k60_5bytes_trunk=0
-vby1_4k120_8div_4bytes=1
-lvds_fhd60=2
-vby1_4k120_2div_4bytes_Vtt2250_BOE_DLG240=3
-vby1_4k120_2div_4bytes_Vtt2250_ST5461D19_4=4
-vby1_4k120_2div_4bytes=5
-vby1_8k60_vrr=6
-vby1_4k60_1div_4bytes=7
-lvds_hd120=8
-vby1_4k120_2div_4bytes_Vtt2250=9
-vby1_4k1k240_2div_4bytes=10
-vby1_4k120_2div_5bytes=11
-vby1_fhd240=12
-vby1_4k1k120_1div_4bytes=13
-vby1_4k120_2div_4bytes_osd_4k60_4bytes_type0=14
+vby1_4k120_8div_4bytes=7
+vby1_cam=8
+vby1_4k1k120_1div_4bytes=9
+vby1_8k60_vrr=10
+vby1_4k120_4div_4bytes=11
+tcon_4k120_PT650GT02_3_cust_ic=12
+vby1_4k144_2div_4bytes_high_clock=13
+vby1_4k144_2div_4bytes_reduce_blank=14
 tcon_hd60=15
-vby1_4k144_2div_4bytes_reduce_blank=16
-vby1_fhd120=17
-vby1_4k120_2div_4bytes_Vtt2250_OLED=18
-vby1_4k120_2div_4bytes_osd_4k60_4bytes_type1=19
-lvds_hd60=20
-vby1_4k120_1div_4bytes=21
+vby1_4k120_2div_4bytes_osd_4k60_5bytes=16
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type1=17
+vby1_4k120_2div_4bytes_Vtt2250_BOE_DLG240=18
+vby1_4k120_2div_4bytes_Vtt2250_ST5461D19_4=19
+vby1_fhd240=20
+vby1_8k60=21
 tcon_4k120_ST7461D04_4_cust_ic=22
-vby1_8k_60_1div_osd_4k60_5bytes=23
-vby1_4k120_1div_4bytes_Vtt2250=24
-vby1_4k1k120_1div_bl0_4bytes=25
-vby1_8k60=26
-tcon_fhd60=27
-tcon_4k120_HV650QUB_E72_cust_ic=28
-vby1_4k120_2div_4bytes_osd_4k60_5bytes=29
-vby1_4k120_4div_4bytes_Vtt2250=30
-vby1_4k120_4div_4bytes=31
-vby1_cam=32
-vby1_fhd60=33
-vby1_4k60_1div_bl0_4bytes=34
-tcon_4k120_PT650GT02_3_cust_ic=35
-tcon=36
-vby1_4k144_2div_4bytes_high_clock=37
-vby1_4k144_1div_4bytes=38
+vby1_4k144_1div_4bytes=23
+lvds_hd60=24
+vby1_fhd120=25
+vby1_4k1k240_2div_4bytes=26
+lvds_hd120=27
+vby1_fhd60=28
+vby1_8k_60_1div_osd_4k60_5bytes_trunk=29
+tcon=30
+lvds_fhd60=31
+vby1_4k120_2div_4bytes_Vtt2250_OLED=32
+vby1_4k120_4div_4bytes_Vtt2250=33
+vby1_4k120_2div_4bytes_osd_4k60_4bytes_type0=34
+vby1_4k120_2div_4bytes=35
+vby1_4k120_1div_4bytes=36
+vby1_4k120_1div_4bytes_Vtt2250=37
+tcon_fhd60=38
+vby1_4k1k120_1div_bl0_4bytes=39
+vby1_4k120_2div_4bytes_Vtt2250=40
+vby1_4k60_1div_bl0_4bytes=41
+vby1_4k60_1div_4bytes=42
+vby1_4k120_2div_5bytes=43
+vby1_8k_60_1div_osd_4k60_5bytes=44
+tcon_4k120_HV650QUB_E72_cust_ic=45
+[iommu]
+iommu_4k=46
+iommu_8k=47
+[sample]
+sample=48
+sample2=49
+[ir]
+ir_customize0=50
+ir_base=51
+[wakeup_key]
+wakeup_ww=52
+wakeup_base=53
+wakeup_linux=54
+[vad]
+vad_cm4_rproc=55
+vad_HK=56
+vad_rv33_rproc=57
+vad_NULL_rproc=58
+[ldm]
+ldm_iw7027=59
+ldm_DCON=60
+ldm_iw7038=61
+ldm_128x128=62
+ldm_BCON=63
+ldm_iw7039=64
 [mmap]
-mmap_mt5873_h1v1_an_1g_iommu=39
-mmap_mt5876_h1v1_an_2g_cma=40
-mmap_mt5873_h1v1_an_1point5g_iommu_cd=41
-mmap_mt5879_h1v1_aosp_4g_iommu_cd=42
-mmap_mt5897_h1v1_linux_3g=43
-mmap_mt5879_h3v1_aosp_3g_k32=44
-mmap_mt5879_h1v1_aosp_3g_iommu=45
-mmap_mt5873_h1v1_an_2g_iommu_cd=46
-mmap_mt5873_h1v1_an_1g_midgard=47
-mmap_mt5873_h1v1_an_1g_iommu_cd=48
-mmap_mt5873_h1v1_an_2g_cma=49
-mmap_mt5873_h1v1_an_2g_iommu=50
-mmap_mt5897_h1v1_an_2g=51
-mmap_mt5879_h1v1_aosp_6g_iommu=52
-mmap_mt5873_h1v1_linux_1g_iommu=53
-mmap_mt5879_mtk_2g_an_iommu_h1v1=54
-mmap_mt5897_haps_an_2g=55
-mmap_mt5879_h1v1_linux_3g_iommu=56
-mmap_mt5896_h1v1_an_6g=57
-mmap_mt5879_h1v1_aosp_4g_iommu=58
-mmap_mt5873_h1v1_linux_1point5g_iommu=59
-mmap_mt5873_h1v1_an_1point5g_midgard=60
-mmap_mt5873_h1v1_linux_2g_iommu=61
-mmap_mt5879_h1v1_aosp_3g_iommu_cd=62
-mmap_mt5873_h1v1_an_3g_iommu=63
-mmap_mt5896_haps_an_2g=64
-mmap_mt5873_h1v1_an_4g_iommu_cd=65
-mmap_mt5876_h1v1_an_2g_iommu=66
+mmap_mt5876_h1v1_an_2g_cma=65
+mmap_mt5873_h1v1_an_2g_static_only=66
 mmap_mt5879_h1v1_linux_4g_iommu=67
-mmap_mt5873_h1v1_an_2g_midgard=68
-mmap_mt5873_h1v1_an_2g_static_only=69
-mmap_mt5873_h1v1_an_4g_iommu=70
-mmap_mt5876_h1v1_an_2g_static_only=71
-mmap_mt5873_h1v1_an_1point5g_iommu=72
-[ldm]
-ldm_iw7039=73
-ldm_iw7038=74
-ldm_BCON=75
-ldm_iw7027=76
-ldm_DCON=77
-ldm_128x128=78
+mmap_mt5873_h1v1_an_4g_iommu_cd=68
+mmap_mt5897_h1v1_linux_3g=69
+mmap_mt5873_h1v1_an_2g_iommu=70
~~~

### tv_defaults

- Equal SHA256: **True**. Sizes: [216002, 216002].
- Total diff lines: 0; text similarity: 100.00%.

~~~diff
~~~

### hdmi_audio

- Equal SHA256: **False**. Sizes: [6077, 6077].
- Total diff lines: 25; text similarity: 94.76%.

~~~diff
--- 8052
+++ 8053
@@ -164,12 +164,12 @@
         0x7F00, \
-        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x3200, \
-        0x3000, 0x2E00, 0x2D00, 0x2C00, 0x2B00, 0x2A00, 0x2900, 0x2800, 0x2700, 0x2600, \
-        0x2500, 0x2400, 0x2300, 0x2200, 0x2100, 0x2000, 0x1F00, 0x1E80, 0x1E00, 0x1D80, \
-        0x1D00, 0x1C80, 0x1C00, 0x1B80, 0x1B00, 0x1A80, 0x1A00, 0x1980, 0x1900, 0x1880, \
-        0x1800, 0x1780, 0x1700, 0x1680, 0x1600, 0x1580, 0x1540, 0x1500, 0x14C0, 0x1480, \
-        0x1440, 0x1400, 0x13C0, 0x1380, 0x1340, 0x1300, 0x12C0, 0x1280, 0x1240, 0x1200, \
-        0x11C0, 0x1180, 0x1140, 0x1100, 0x10C0, 0x1080, 0x1040, 0x1000, 0x0FE0, 0x0FC0, \
-        0x0FA0, 0x0F80, 0x0F60, 0x0F40, 0x0F20, 0x0F00, 0x0EE0, 0x0EC0, 0x0EA0, 0x0E80, \
-        0x0E60, 0x0E40, 0x0E20, 0x0E00, 0x0DE0, 0x0DC0, 0x0DA0, 0x0D80, 0x0D60, 0x0D40, \
-        0x0D20, 0x0D00, 0x0CE0, 0x0CC0, 0x0CA0, 0x0C80, 0x0C60, 0x0C40, 0x0C20, 0x0C00  \
+        0x4700, 0x4400, 0x4100, 0x3E00, 0x3C00, 0x3A00, 0x3800, 0x3600, 0x3400, 0x1200, \
+        0x11C0, 0x1180, 0x1160, 0x1120, 0x1100, 0x10C0, 0x1080, 0x1060, 0x1020, 0x1000, \
+        0x0FC0, 0x0F80, 0x0F60, 0x0F20, 0x0F00, 0x0EC0, 0x0E80, 0x0E60, 0x0E20, 0x0E00, \
+        0x0DC0, 0x0D80, 0x0D60, 0x0D20, 0x0D00, 0x0CC0, 0x0C80, 0x0C60, 0x0C20, 0x0C00, \
+        0x0BE0, 0x0BC0, 0x0BA0, 0x0B80, 0x0B80, 0x0B60, 0x0B40, 0x0B20, 0x0B00, 0x0B00, \
+        0x0AE0, 0x0AC0, 0x0AA0, 0x0A80, 0x0A80, 0x0A60, 0x0A40, 0x0A20, 0x0A00, 0x0A00, \
+        0x09E0, 0x09C0, 0x09A0, 0x0980, 0x0980, 0x0960, 0x0940, 0x0920, 0x0900, 0x0900, \
+        0x08E0, 0x08C0, 0x08A0, 0x0880, 0x0880, 0x0860, 0x0840, 0x0820, 0x0800, 0x0800, \
+        0x07E0, 0x07C0, 0x07A0, 0x0780, 0x0780, 0x0760, 0x0740, 0x0720, 0x0700, 0x0700, \
+        0x06E0, 0x06C0, 0x06A0, 0x0680, 0x0680, 0x0660, 0x0640, 0x0620, 0x0600, 0x0600  \
     }
~~~

## Android file comparison

- Common file paths: **3941**
- Identical full SHA256: **2155**
- Different SHA256: **1786**
- Only 8052: **8**; only 8053: **8**.

### Files unique to OTA 8052

- system/system/app/KuSetupWizard/KuSetupWizard.apk
- system/system/app/KuSetupWizard/oat/arm/KuSetupWizard.odex
- system/system/app/KuSetupWizard/oat/arm/KuSetupWizard.vdex
- system/system/lib/libfactoryi2c_jni.so
- system/system/lib/librjpj_private_function.so
- system/system/lib/libsettingsi2c_jni.so
- vendor/lib/modules/ruimotor.ko
- vendor/lib/modules/stmvl53l1.ko

### Files unique to OTA 8053

- system/system/priv-app/Telecom/Telecom.apk
- system/system/priv-app/Telecom/oat/arm/Telecom.odex
- system/system/priv-app/Telecom/oat/arm/Telecom.vdex
- system_ext/app/A2dpSinkPlayerTCN/A2dpSinkPlayerTCN.apk
- system_ext/etc/permissions/com.android.provision.xml
- system_ext/priv-app/Provision/Provision.apk
- system_ext/priv-app/Provision/oat/arm/Provision.odex
- system_ext/priv-app/Provision/oat/arm/Provision.vdex

### Selected manufacturer apps

| App path | 8052 version | 8053 version | Identical SHA? |
|---|---|---|---|
| system/system/apex/com.android.permission/priv-app/SafetyCenterResources@TP1A.220624.021.A1/SafetyCenterResources.apk | 33 system image | 33 system image | True |
| system/system/apex/com.android.tethering.inprocess/priv-app/ServiceConnectivityResources@TP1A.220624.021.A1/ServiceConnectivityResources.apk | S-initial | S-initial | True |
| system/system/apex/com.android.uwb/priv-app/ServiceUwbResources@TP1A.220624.021.A1/ServiceUwbResources.apk | T-initial | T-initial | True |
| system/system/apex/com.android.wifi/priv-app/ServiceWifiResources@TP1A.220624.021.A1/ServiceWifiResources.apk | R-initial | R-initial | True |
| system/system/app/KuSettings/KuSettings.apk | 1.0 | 1.0 | False |
| system/system/app/KuSetupWizard/KuSetupWizard.apk | 1.0 | not recorded | False |
| system/system/app/KuSourceRJ/KuSourceRJ.apk | 5.3 | 3.6 | False |
| system/system/app/RuiAutoFocus/RuiAutoFocus.apk | 4.2 | 4.2 | False |
| system/system/app/TrdDreamPic/TrdDreamPic.apk | 1.0 | 1.0 | True |
| system/system/app/TrdFactoryTest/TrdFactoryTest.apk | 1.0 | 1.0 | True |
| system/system/app/trdservice/trdservice.apk | 13 | 13 | False |
| system/system/app/zxlauncher/zxlauncher.apk | 2.0.43 | 2.0.37 | False |
| system/system/priv-app/KeystoneCorrection/KeystoneCorrection.apk | 13 | 13 | False |
| system/system/priv-app/RuiYunOta/RuiYunOta.apk | 1.0 | 1.0 | False |
| system/system/priv-app/SettingsProvider/SettingsProvider.apk | 13 | 13 | False |
| system_ext/app/Factory/Factory.apk | 1.0 | 1.0 | False |
| system_ext/priv-app/Provision/Provision.apk | not recorded | 13 | False |
| system_ext/priv-app/RemoteProvisioner/RemoteProvisioner.apk | 13 | 13 | True |
| system_ext/priv-app/TvSettingsPlus/TvSettingsPlus.apk | 1.0 | 1.0 | False |
| vendor/priv-app/trdmiddle/trdmiddle.apk | 1.0 | 1.0 | False |

## Image partitions

| Partition | 8052 bytes | 8053 bytes | Exact SHA match? |
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

## Interpretation and limitations

The two OTA channels are siblings on the same Android/MediaTek platform, but different OEM profiles and notably different build dates.
Two DTBO contents vary, and board/DTBO mapping is not identical. This is evidence against considering the binaries interchangeable.
Presence of hardware module names is evidence about software packaging, not proof of a physical sensor.
OTA 8053 is NOT identified as a one-HDMI or two-HDMI projector without device-side confirmation.
No projector was flashed; all steps used static read-only tools.

