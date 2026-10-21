# October OTA 8052 vs September stock 8054

Comparison of verified original sources, no OEM code published, no device flashed.
Old August 8052 versus September 8054 differences can reflect software updates instead of board changes.

## Board and audio configuration SHA comparison

| File | Identical latest 8052 vs factory 8054 |
|---|---|
| board.ini | YES |
| tvconfig/dtbo_mapping.ini | YES |
| bootdata/dtbo_mapping.ini | YES |
| BasicSound_HDMI.ini | YES |
| BasicSound_DTV.ini | YES |
| BasicSound_MM.ini | YES |
| ConfigDefaultValue.ini | NO |
| gammatable_1.ini | NO |
| pmu_mcs51_sign.bin | NO |

## Android OEM app APK and DEX comparison

| App | OTA present | APK identical to 8054 | All DEX identical to 8054 |
|---|---|---|---|
| TvSettingsPlus | True | True | True |
| Factory | True | True | True |
| KeystoneCorrection | True | True | True |
| RuiAutoFocus | True | False | False |
| KuSourceRJ | True | True | True |
| trdservice | True | True | True |
| trdmiddle | True | True | True |
| KuSettings | True | True | True |
| RuiYunOta | True | True | True |
| KuSetupWizard | True | None | None |
| Provision | False | None | None |

## OTA 8052 vs factory 8054 profile values

| Property | OTA 8052 | Factory 8054 |
|---|---|---|
| ro.product.ota | V618RJEN | V618RJENHD |
| ro.rjpj.autofocus.move | 1 | None |
| ro.rjpj.autofocus.poweron | 1 | None |
| ro.rjpj.autokeystone.move | 0 | 1 |
| ro.rjpj.autokeystone.poweron | 0 | 1 |
| ro.rjpj.hdmi.port.count | 1 | 2 |
| ro.rjpj.hdmi.ports | HW6:HDMI | HW6:HDMI1,HW7:HDMI2 |
| ro.rjpj.machine.id | 8052 | 8054 |
| ro.rjpj.support.toffunction | 0 | 1 |
| ro.rjpj.yunota.url | mt9660/8052/8052_ota.json | mt9660/8054/8054_ota.json |
| ro.rjpj.yunota.version | RUIOS.8052.1.0.4 | RUIOS.8054.1.0.1 |
| ro.rjpj.yunota.zip | RJMT9660_firmware_8052.zip | RJMT9660_firmware_8054.zip |
| ro.zeasn.devicetype | rjpj9660global | rjpj9660fordexp |

## Key OEM drivers/libraries in latest 8052 OTA

| File | Present in latest 8052 OTA |
|---|---|
| system/system/lib/libsettingsi2c_jni.so | True |
| system/system/lib/libfactoryi2c_jni.so | True |
| system/system/lib/libi2c_jni.so | True |
| system/system/lib/libtrd_jni.so | True |
| system/system/lib/libtof_jni.so | True |
| system/system/lib/librjpj_private_function.so | True |
| vendor/lib/modules/ruimotor.ko | True |
| vendor/lib/modules/stmvl53l1.ko | True |
| vendor/etc/audio_policy_configuration.xml | True |

## Limits and recommended next research

- Identical APKs mean identical bytes; differing hashes do not identify particular changed methods.
- OEM driver binary equality with factory 8054 cannot be inferred from OTA file presence alone.
- DTBO per-blob match with 8054 needs verified stock per-entry hashes in a later run.
- Never deduce physical wiring from identical firmware config hashes.
- Real device tests must verify Binder service permissions, bootloader/AVB enforcement, recovery and HDMI/ToF behavior.
- Keep separate board profiles and use device-matched installation packages until recovery and signatures are proven.
- 8053 is not a target hardware profile.

