# RUIOS 8053 hardware identity — inspected genuine OTA partitions

Read-only audit; hardware compatibility or safe cross-flashing NOT established.

## OEM profile properties

| Property | 8052 OTA | 8053 OTA | 8054 factory (2 HDMI) |
|---|---|---|---|
| ro.rjpj.machine.id | 8052 | 8053 | 8054 |
| ro.rjpj.yunota.version | RUIOS.8052.1.0.4 | RUIOS.8053.1.0.0 | RUIOS.8054.1.0.1 |
| ro.rjpj.hdmi.ports | HW6:HDMI | — | HW6:HDMI1,HW7:HDMI2 |
| ro.rjpj.hdmi.port.count | 1 | — | 2 |
| ro.rjpj.support.toffunction | 0 | — | 1 |
| ro.rjpj.autokeystone.poweron | 0 | 0 | 1 |
| ro.rjpj.autokeystone.move | 0 | 0 | 1 |
| ro.rjpj.yunota.url | mt9660/8052/8052_ota.json | mt9660/8053/8053_ota.json | mt9660/8054/8054_ota.json |
| ro.rjpj.yunota.zip | RJMT9660_firmware_8052.zip | RJMT9660_firmware_8053.zip | RJMT9660_firmware_8054.zip |

## DTBO content-level overlap
- Matching blobs (8052 OTA vs 8053 OTA, multiset): 205/207.
- OTA 8052 matches known 8054 stock blob hashes: 203/203.
- OTA 8053 matches known 8054 stock blob hashes: 201/203.
- Stock 8054 reference contains hashes for 203 of 207 blobs; this comparison does not certify the active DTBO or index mapping.

## Selected firmware files

| File | 8052 vs 8053 SHA256 identical? |
|---|---|
| tvconfig_board_ini | False |
| tvconfig_dtbo_mapping | False |
| bootdata_dtbo_mapping | False |

### Selected TV config excerpts

#### 8052

**tvconfig_board_ini** (SHA256: 803b19c1781a0f88137184fa2ea879a4a88fd6cd8aa0eb1a4532b89a9f6c1229)
- `[BOARD_CONFIG]`
- `BOARD_NAME = "MT5873_H1V1_B6_S";`
- `BOARD_MMAP_FILE_NAME = "/application/MMAP_MI.h";`
- `#GPIO_DEMOD_RST = 0;`
- `[BOARD_SYSTEM_TV_PARAM]`
- `HDMI_FOR_MHL_PORT = 23; #///<HDMI 1          23`
- `[BOARD_TV_PARAM]`
- `BOARD_TV_PRODUCT_TYPE = 2; #E_ATV_Only = 0, E_DTV_Only=1, E_ATV_Plus_DTV=2`
- `BOARD_ATV_SYSTEM_TYPE = 1; #E_NTSC_ENABLE = 0, E_PAL_ENABLE = 1, E_CHINA_ENABLE = 2,E_PAL_M_ENABLE = 3`
- `BOARD_DTV_TYPE = 0x83; #DTMB_ENABLE=BIT7, DVBC_ENABLE=BIT1, DVBT_ENABLE=BIT0`
- `BOARD_AUDIO_SYSTEM_TYPE = 1; #E_BTSC_ENABLE = 0, E_A2_ENABLE = 1, E_EIAJ_ENABLE = 2`
- `BOARD_STB_SYSTEM_TYPE = 0; #E_STB_DISABLE = 0,E_STB_ENABLE = 1`
- `BOARD_IP_ENABLE = 0; # BOARD_COMMON_NULL       0x00`
- `BOARD_ROUTE_PATH_NUM = 4;`
- `BOARD_ROUTE_PATH_0 = 0x10; # ISDB_ENABLE = BIT4`
- `BOARD_ROUTE_PATH_1 = 0; #BOARD_COMMON_NULL       0x00`
- `BOARD_ROUTE_PATH_2 = 0; #BOARD_COMMON_NULL       0x00`
- `BOARD_ROUTE_PATH_3 = 0; #BOARD_COMMON_NULL       0x00`
- `BOARD_DAC_CURRENT_MODE = 0; # E_CURRENT_MODE_FULL=0, E_CURRENT_MODE_HALF=1,E_CURRENT_MODE_QUART=2`
- `BOARD_SAW_TYPE = 6; #DUAL_SAW = 0,EXTERNAL_SINGLE_SAW=1,SILICON_TUNER=2, INTERNAL_SINGLE_SAW_DIF=3,NO_SAW=4,INTERNAL_SINGLE_SAW_VIF=5,NO_SAW_DIF=6,SAW6=7`

**tvconfig_dtbo_mapping** (SHA256: bedc690bf595e8d52fefbb4f8189991994f95c74fbff57b2ecd4bae49c378ba7)
- `[panel]`
- `[input]`
- `inputdev_cm4=136`
- `inputdev_mcs51=137`
- `inputdev_arm=138`

**bootdata_dtbo_mapping** (SHA256: bedc690bf595e8d52fefbb4f8189991994f95c74fbff57b2ecd4bae49c378ba7)
- `[panel]`
- `[input]`
- `inputdev_cm4=136`
- `inputdev_mcs51=137`
- `inputdev_arm=138`

#### 8053

**tvconfig_board_ini** (SHA256: 8e10a83824d4d6d52cb197b631b98215af26adffbf6fddb7de53213022c0da2e)
- `[BOARD_CONFIG]`
- `BOARD_NAME = "MT5873_H1V1_B6_S";`
- `BOARD_MMAP_FILE_NAME = "/application/MMAP_MI.h";`
- `#GPIO_DEMOD_RST = 0;`
- `[BOARD_SYSTEM_TV_PARAM]`
- `HDMI_FOR_MHL_PORT = 23; #///<HDMI 1          23`
- `[BOARD_TV_PARAM]`
- `BOARD_TV_PRODUCT_TYPE = 2; #E_ATV_Only = 0, E_DTV_Only=1, E_ATV_Plus_DTV=2`
- `BOARD_ATV_SYSTEM_TYPE = 1; #E_NTSC_ENABLE = 0, E_PAL_ENABLE = 1, E_CHINA_ENABLE = 2,E_PAL_M_ENABLE = 3`
- `BOARD_DTV_TYPE = 0x83; #DTMB_ENABLE=BIT7, DVBC_ENABLE=BIT1, DVBT_ENABLE=BIT0`
- `BOARD_AUDIO_SYSTEM_TYPE = 1; #E_BTSC_ENABLE = 0, E_A2_ENABLE = 1, E_EIAJ_ENABLE = 2`
- `BOARD_STB_SYSTEM_TYPE = 0; #E_STB_DISABLE = 0,E_STB_ENABLE = 1`
- `BOARD_IP_ENABLE = 0; # BOARD_COMMON_NULL       0x00`
- `BOARD_ROUTE_PATH_NUM = 4;`
- `BOARD_ROUTE_PATH_0 = 0x10; # ISDB_ENABLE = BIT4`
- `BOARD_ROUTE_PATH_1 = 0; #BOARD_COMMON_NULL       0x00`
- `BOARD_ROUTE_PATH_2 = 0; #BOARD_COMMON_NULL       0x00`
- `BOARD_ROUTE_PATH_3 = 0; #BOARD_COMMON_NULL       0x00`
- `BOARD_DAC_CURRENT_MODE = 0; # E_CURRENT_MODE_FULL=0, E_CURRENT_MODE_HALF=1,E_CURRENT_MODE_QUART=2`
- `BOARD_SAW_TYPE = 6; #DUAL_SAW = 0,EXTERNAL_SINGLE_SAW=1,SILICON_TUNER=2, INTERNAL_SINGLE_SAW_DIF=3,NO_SAW=4,INTERNAL_SINGLE_SAW_VIF=5,NO_SAW_DIF=6,SAW6=7`

**tvconfig_dtbo_mapping** (SHA256: 339e8b4fd19df9acd23cd629d70d31dcf262a263fe7cb05e6290c847bb3ecc26)
- `[panel]`
- `[input]`
- `inputdev_cm4=204`
- `inputdev_mcs51=205`
- `inputdev_arm=206`

**bootdata_dtbo_mapping** (SHA256: 339e8b4fd19df9acd23cd629d70d31dcf262a263fe7cb05e6290c847bb3ecc26)
- `[panel]`
- `[input]`
- `inputdev_cm4=204`
- `inputdev_mcs51=205`
- `inputdev_arm=206`
