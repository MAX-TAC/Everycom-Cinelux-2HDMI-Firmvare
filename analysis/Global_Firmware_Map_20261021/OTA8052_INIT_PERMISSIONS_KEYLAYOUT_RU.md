# Оригинальная OTA 8052.1.0.4: init, разрешения, раскладки пульта и системные APK

Сканирование только оригинальных распакованных readonly partitions Android; не заменяет реальные PackageManager и сервисы в памяти.

## Количество найденных компонентов

- apk_paths: 85
- init_service_entries_matching_oem_or_hardware: 36
- key_layout_files: 179
- privilege_xml_declarations: 13
- overlay_apks: 3

## Аппаратные/OEM init services

| Service | Executable | .rc source |
|---|---|---|
| apexd-bootstrap | `/system/bin/apexd` | system/system/etc/init/apexd.rc |
| audioserver | `/system/bin/audioserver` | system/system/etc/init/audioserver.rc |
| bootanim | `/system/bin/bootanimation` | system/system/etc/init/bootanim.rc |
| boottrace | `/system/bin/atrace` | system/system/etc/init/atrace.rc |
| bootvideo | `/vendor/bin/sh` | vendor/etc/init/bootvideo.rc |
| cpu-audio | `/vendor/bin/sh` | vendor/etc/init/cpu_audio.rc |
| dtv-svc | `/vendor/bin/sh` | vendor/etc/init/dtv_svc.rc |
| factory_svc | `/mnt/vendor/factory/bin/factory_svc` | vendor/etc/init/factory_svc.rc |
| mtk_rm | `/vendor/bin/sh` | vendor/etc/init/mtk_rm.rc |
| networkproxy-hal-1-0 | `/vendor/bin/hw/vendor.mediatek.hardware.tv.networkproxy@1.0-service` | vendor/etc/init/vendor.mediatek.hardware.tv.networkproxy@1.0-service.rc |
| perfetto_trace_on_boot | `/system/bin/perfetto` | system/system/etc/init/perfetto.rc |
| sample-hal-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.cmpb@1.0-service` | vendor/etc/init/vendor.mediatek.tv.cmpb@1.0-service.rc |
| screenrecord | `/vendor/bin/hw/vendor.mediatek.tv.screenrecord@1.0-service` | vendor/etc/init/vendor.mediatek.tv.screenrecord@1.0-service.rc |
| trd_boot | `/system/bin/sh` | system/init.trd.rc |
| trd_module_loader | `/vendor/bin/trd_module_loader.sh` | system/init.trd.rc |
| tv-input-1-0 | `/vendor/bin/hw/android.hardware.tv.input@1.0-service-mediatek` | vendor/etc/init/android.hardware.tv.input@1.0-service-mediatek.rc |
| tv-mtkcalman-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.mtkcalman@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtkcalman@1.0-service.rc |
| tv-mtkdmservice-hal-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.mtkdmservice@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtkdmservice@1.0-service.rc |
| tv-mtkmtalservice-hal-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.mtkmtalservice@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtkmtalservice@1.0-service.rc |
| tv-mtkrm-hal-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.mtkrm@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtkrm@1.0-service.rc |
| tv-mtktvapi-1-0 | `/vendor/bin/hw/vendor.mediatek.api.mtktvapi@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtktvapi@1.0-service.rc |
| tv-mtktvfactory-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.mtktvfactory@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtktvfactory@1.0-service.rc |
| tv-mtktvvoc-1-0 | `/vendor/bin/hw/vendor.mediatek.tv.mtktvvoc@1.0-service` | vendor/etc/init/vendor.mediatek.tv.mtktvvoc@1.0-service.rc |
| vendor.audio-hal | `/vendor/bin/hw/vendor.mediatek.hardware.audio.service` | vendor/etc/init/vendor.mediatek.hardware.audio.service.rc |
| vendor.bluetooth-1-1 | `/vendor/bin/hw/android.hardware.bluetooth@1.1-service` | vendor/etc/init/android.hardware.bluetooth@1.1-service.rc |
| vendor.boot-hal-1-2 | `/vendor/bin/hw/android.hardware.boot@1.2-service` | vendor/etc/init/android.hardware.boot@1.2-service.rc |
| vendor.cec-hal-1-0 | `/vendor/bin/hw/android.hardware.tv.cec@1.0-service` | vendor/etc/init/android.hardware.tv.cec@1.0-service.rc |
| vendor.hwtrd-1-0 | `/vendor/bin/hw/vendor.trd.hardware.hwtrd@1.0-service` | vendor/etc/init/vendor.trd.hardware.hwtrd@1.0-service.rc |
| vendor.power-mediatek | `/vendor/bin/hw/mediatek.hardware.power-service` | vendor/etc/init/power-mediatek.rc |
| vendor.thermal-hal-2-0-mock | `/vendor/bin/hw/android.hardware.thermal@2.0-service.mediatek` | vendor/etc/init/android.hardware.thermal@2.0-service.mediatek.rc |
| vendor.tof-hal-1-0 | `/vendor/bin/hw/vendor.trd.hardware.tof@1.0-service` | vendor/etc/init/vendor.trd.hardware.tof@1.0-service.rc |
| vendor.wifi_hal_legacy | `/vendor/bin/hw/android.hardware.wifi@1.0-service-lazy` | vendor/etc/init/android.hardware.wifi@1.0-service-lazy.rc |
| wificond | `/system/bin/wificond` | system/system/etc/init/wificond.rc |
| wificond | `/system/bin/wificond` | vendor/etc/init/hw/init.common.rc |
| wifidisplay-hal-1-0 | `/vendor/bin/hw/vendor.mediatek.hardware.wifidisplay@1.0-service` | vendor/etc/init/vendor.mediatek.hardware.wifidisplay@1.0-service.rc |
| wlan_dongle_detect | `/vendor/bin/wlan_dongle_detect` | vendor/etc/init/init.insmod.rc |

## Android privilege XML for OEM and TV Settings

### com.mediatek.tvinput
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.CHANGE_HDMI_CEC_ACTIVE_SOURCE, android.permission.HDMI_CEC, android.permission.MODIFY_PARENTAL_CONTROLS, android.permission.TV_INPUT_HARDWARE

### com.mediatek.wwtv.setupwizard
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.MODIFY_PARENTAL_CONTROLS, android.permission.MOUNT_FORMAT_FILESYSTEMS, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.SET_TIME_ZONE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS

### com.mediatek.wwtv.mediaplayer
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.CHANGE_CONFIGURATION, android.permission.FORCE_STOP_PACKAGES, android.permission.HDMI_CEC, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.READ_EXTERNAL_STORAGE, android.permission.REAL_GET_TASKS, android.permission.REBOOT, android.permission.SET_TIME_ZONE, android.permission.SHUTDOWN, android.permission.TV_INPUT_HARDWARE, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS

### com.mediatek.tv.agent
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.CHANGE_CONFIGURATION, android.permission.DEVICE_POWER, android.permission.INTERACT_ACROSS_USERS, android.permission.INTERACT_ACROSS_USERS_FULL, android.permission.MANAGE_USERS, android.permission.MASTER_CLEAR, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.PACKAGE_USAGE_STATS, android.permission.READ_DREAM_STATE, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_LOGS, android.permission.REAL_GET_TASKS, android.permission.SET_ACTIVITY_WATCHER, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.TV_INPUT_HARDWARE, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS

### com.mediatek.tv.service
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.CHANGE_COMPONENT_ENABLED_STATE, android.permission.CHANGE_CONFIGURATION, android.permission.DEVICE_POWER, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.HDMI_CEC, android.permission.INTERACT_ACROSS_USERS, android.permission.INTERACT_ACROSS_USERS_FULL, android.permission.MANAGE_USERS, android.permission.MASTER_CLEAR, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.PACKAGE_USAGE_STATS, android.permission.READ_DREAM_STATE, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_LOGS, android.permission.REAL_GET_TASKS, android.permission.SET_ACTIVITY_WATCHER, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.TV_INPUT_HARDWARE, android.permission.WAKE_LOCK, android.permission.WRITE_DREAM_STATE, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS

### com.mediatek.wwtv.tvcenter
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.BIND_TV_INPUT, android.permission.BIND_TV_REMOTE_SERVICE, android.permission.CHANGE_CONFIGURATION, android.permission.CHANGE_HDMI_CEC_ACTIVE_SOURCE, android.permission.DEVICE_POWER, android.permission.HDMI_CEC, android.permission.INTERACT_ACROSS_USERS, android.permission.KILL_BACKGROUND_PROCESSES, android.permission.MANAGE_EXTERNAL_STORAGE, android.permission.MODIFY_AUDIO_ROUTING, android.permission.MODIFY_PARENTAL_CONTROLS, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.READ_CONTENT_RATING_SYSTEMS, android.permission.READ_DREAM_STATE, android.permission.REAL_GET_TASKS, android.permission.RECOVERY, android.permission.SET_TIME_ZONE, android.permission.SHUTDOWN, android.permission.SYSTEM_ALERT_WINDOW, android.permission.TV_INPUT_HARDWARE, android.permission.WRITE_DREAM_STATE, android.permission.WRITE_SECURE_SETTINGS

### com.mediatek.hotkey.dispatcher
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.READ_DREAM_STATE, android.permission.REAL_GET_TASKS, android.permission.WRITE_DREAM_STATE

### com.mediatek.alphonso.acr
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.PACKAGE_USAGE_STATS

### com.android.tv.settings
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.BACKUP, android.permission.BIND_TV_INPUT, android.permission.BLUETOOTH_PRIVILEGED, android.permission.DELETE_CACHE_FILES, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_ACCOUNTS_PRIVILEGED, android.permission.MANAGE_DEBUGGING, android.permission.MANAGE_USERS, android.permission.OVERRIDE_WIFI_CONFIG, android.permission.REBOOT, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.SET_UNRESTRICTED_KEEP_CLEAR_AREAS, android.permission.START_ACTIVITIES_FROM_BACKGROUND, android.permission.TV_INPUT_HARDWARE, android.permission.USE_RESERVED_DISK, android.permission.WRITE_EPG_DATA, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS

### com.mediatek.tv.freeviewplay
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.CHANGE_COMPONENT_ENABLED_STATE, android.permission.HDMI_CEC, android.permission.INTERACT_ACROSS_USERS, android.permission.MANAGE_USERS, android.permission.REAL_GET_TASKS, android.permission.WRITE_SECURE_SETTINGS

### com.mediatek.bluetooth
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.BLUETOOTH_PRIVILEGED, android.permission.MODIFY_PHONE_STATE, android.permission.RECEIVE_BLUETOOTH_MAP

### com.mediatek.opapp
From `system_ext/etc/permissions/privapp-permissions-mediatek.xml`
Permissions: android.permission.INSTALL_PACKAGES, android.permission.REQUEST_DELETE_PACKAGES, android.permission.REQUEST_INSTALL_PACKAGES

### com.rjpj.yunota
From `system/system/etc/permissions/privapp-permissions-com.rjpj.yunota.xml`
Permissions: android.permission.BACKUP, android.permission.DELETE_CACHE_FILES, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_ACCOUNTS_PRIVILEGED, android.permission.MANAGE_USERS, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.OVERRIDE_WIFI_CONFIG, android.permission.REBOOT, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.USE_RESERVED_DISK, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS


## KeyLayout files relevant to HOME/SETTINGS/INPUT

### system/system/usr/keylayout/Vendor_046d_Product_b501.kl

- SHA256: 44f92cd2121beceb55fba4dcdeab16a2cac002dba7b9d167bece46aeac643851
- Mapped relevant keys: 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 353→DPAD_CENTER, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 152→POWER, 158→BACK, 172→HOME

### system/system/usr/keylayout/Vendor_046d_Product_c216.kl

- SHA256: 7851977e760ef0bfee7c184f35e0da2076264a701f609a6c4fab2de1bea85312
- Mapped relevant keys: 0x128→BACK

### system/system/usr/keylayout/Vendor_046d_Product_c219.kl

- SHA256: 738ea5393578328f9a3bfe70b527e520d133b83f5b4e5d34da94930f1b471b63
- Mapped relevant keys: 312→BACK

### system/system/usr/keylayout/Vendor_046d_Product_c21d.kl

- SHA256: eee743911e25fb58e8288b285c2dc2046f4ccb381eb881d1465e7ddfab5abf4e
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_046d_Product_c21f.kl

- SHA256: ff5da9a1d4944cdd5e7e6921867e54fac9747735fef196f16c83d696f3f3d10e
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_046d_Product_c532.kl

- SHA256: adb12e9f67cecb798648e46e71c437000d69b76ee284188064e2b462fc2c16c7
- Mapped relevant keys: 43→BACKSLASH, 96→DPAD_CENTER, 102→MOVE_HOME, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 127→MENU, 158→BACK, 172→HOME

### system/system/usr/keylayout/Vendor_054c_Product_0268.kl

- SHA256: f6822cb5260de37e318f5bc9f1dad5ad068ecf6d8263abe6fa66fe8b53139e9f
- Mapped relevant keys: 0x124→DPAD_UP, 0x125→DPAD_RIGHT, 0x126→DPAD_DOWN, 0x127→DPAD_LEFT

### system/system/usr/keylayout/Vendor_054c_Product_0268_Version_8000.kl

- SHA256: 469bd4666efad0e0cc96be3b3d78b73c7b1210fba03d180f6a5af9816dd51c61
- Mapped relevant keys: 0x220→DPAD_UP, 0x223→DPAD_RIGHT, 0x221→DPAD_DOWN, 0x222→DPAD_LEFT

### system/system/usr/keylayout/Vendor_054c_Product_0268_Version_8100.kl

- SHA256: 469bd4666efad0e0cc96be3b3d78b73c7b1210fba03d180f6a5af9816dd51c61
- Mapped relevant keys: 0x220→DPAD_UP, 0x223→DPAD_RIGHT, 0x221→DPAD_DOWN, 0x222→DPAD_LEFT

### system/system/usr/keylayout/Vendor_054c_Product_0268_Version_8111.kl

- SHA256: 85619e7d8dd97e14c29ba8be399569a19d46acef974d2fec220d2ee1c89f3153
- Mapped relevant keys: 0x220→DPAD_UP, 0x223→DPAD_RIGHT, 0x221→DPAD_DOWN, 0x222→DPAD_LEFT

### system/system/usr/keylayout/Vendor_056e_Product_2010.kl

- SHA256: 22a64d217961878f5ce31f3b39963ea95b9175af4be778651c2b66877d0fdd14
- Mapped relevant keys: 314→BACK

### system/system/usr/keylayout/Vendor_056e_Product_2013.kl

- SHA256: 6342165aa0b2f6a7256e242aefdd8b0f3238117f41d292bcda0d7b550b450365
- Mapped relevant keys: 314→BACK

### system/system/usr/keylayout/Vendor_057e_Product_2009.kl

- SHA256: 8dedcb73a98a3c26e1227506ed625bd0a3a0d8c91ade46cfdca223754d35495c
- Mapped relevant keys: 0x220→DPAD_UP, 0x221→DPAD_DOWN, 0x222→DPAD_LEFT, 0x223→DPAD_RIGHT, 0x13c→HOME

### system/system/usr/keylayout/Vendor_05ac_Product_0239.kl

- SHA256: 6e31ce1f1b45147002a5b83f37ba1caf4242ea6db6a85dec40ad0c8af91b9276
- Mapped relevant keys: 43→BACKSLASH, 102→MOVE_HOME, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP

### system/system/usr/keylayout/Vendor_0957_Product_0001.kl

- SHA256: b49f9661f8102c67ab5ad619e355b2a9b3df8004367d6bd3a0ab9efdd6cdc0bf
- Mapped relevant keys: 116→TV_POWER, 103→DPAD_UP, 108→DPAD_DOWN, 105→DPAD_LEFT, 106→DPAD_RIGHT, 353→DPAD_CENTER, 158→BACK, 172→HOME, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP

### system/system/usr/keylayout/Vendor_0b05_Product_4500.kl

- SHA256: 70272b1f948db26f53d2a6ca5f5f021244dfea93e96908860cd2290e4e78101e
- Mapped relevant keys: 158→BACK, 172→HOME

### system/system/usr/keylayout/Vendor_0f0d_Product_00c1.kl

- SHA256: 58558b6c03a75c81abf5d197a99768870dc26a43444adf856d641022e1742bca
- Mapped relevant keys: 0x13c→HOME

### system/system/usr/keylayout/Vendor_1532_Product_0705.kl

- SHA256: 91d1677bc91663763ae987e9698f3dd5533bb755dc374e50591656bf68375691
- Mapped relevant keys: 0x9e→BACK

### system/system/usr/keylayout/Vendor_1532_Product_0707.kl

- SHA256: beebe0b2f5b537cda3fc41610f55cf7d787d961698df815b8d2b972ffcf17e61
- Mapped relevant keys: 0x9e→BACK

### system/system/usr/keylayout/Vendor_1532_Product_0900.kl

- SHA256: 7ff33cb3da1e1a2d1fed903e1ce0b70ce5b480232cc8bcb17fdc81c5e3e0a0b9
- Mapped relevant keys: 158→BACK, 172→HOME

### system/system/usr/keylayout/Vendor_1689_Product_fd00.kl

- SHA256: 947e09d1c0f79e71a581c8861609eec2da8b084df0e34c20a27336aa4bb678f3
- Mapped relevant keys: 314→BACK, 316→HOME, 706→DPAD_UP, 705→DPAD_RIGHT, 707→DPAD_DOWN, 704→DPAD_LEFT

### system/system/usr/keylayout/Vendor_1689_Product_fd01.kl

- SHA256: b1e954b43b52ad82290859c8d9737f24b927e3cec5cc6a04d7cd011c62963a7a
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_1689_Product_fe00.kl

- SHA256: 83d9e1841f261d174ae5b3a675fa2c71fdabf9bf770710b1be079cd1cb5b8ee7
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_18d1_Product_0200.kl

- SHA256: 61b2626d7ea43a31e5971e39461ffeb7f518d6544e1bdfc0966805bee7d008a2
- Mapped relevant keys: 103→DPAD_UP, 108→DPAD_DOWN, 105→DPAD_LEFT, 106→DPAD_RIGHT

### system/system/usr/keylayout/Vendor_18d1_Product_2c40.kl

- SHA256: 8472bad0e70434cb7d61313ffa6a6bf2e97b77131b8d56f483b4d1412f417ca6
- Mapped relevant keys: 158→BACK, 172→HOME

### system/system/usr/keylayout/Vendor_18d1_Product_5018.kl

- SHA256: 81c355325515df84293b2746e0c9176f7d549b39d84be8c73723c7d7fef9a7f3
- Mapped relevant keys: 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN

### system/system/usr/keylayout/Vendor_1949_Product_0401.kl

- SHA256: 6da139238a79463fadd4eafb133ef75f3b3208d7682018f1dceab03306867a5b
- Mapped relevant keys: 103→DPAD_UP, 108→DPAD_DOWN, 105→DPAD_LEFT, 106→DPAD_RIGHT, 96→DPAD_CENTER, 158→BACK, 172→HOME

### system/system/usr/keylayout/Vendor_1bad_Product_f016.kl

- SHA256: 2b67e16a321d66ffa26ee708cfd3602ec2abe2fbeab7a457cd347eeeb30393b8
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_1bad_Product_f023.kl

- SHA256: 129334073ee5ebd742f6ee72e5f3427ce937ea8e25b49711e7eb8d0fd9ffb06d
- Mapped relevant keys: 314→BACK

### system/system/usr/keylayout/Vendor_1bad_Product_f027.kl

- SHA256: ea00e14c1f7972307f86ede2b31caf0ba1fe908fff9b8a1c5faf9fc1c410f583
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_1bad_Product_f036.kl

- SHA256: bdb74e2c1224bf33eda8a41b3ca9e77a48a2cea98a1903490889a643a7d2202d
- Mapped relevant keys: 314→BACK, 316→HOME

### system/system/usr/keylayout/Vendor_1d79_Product_0009.kl

- SHA256: 1723364da48d9a4d0a2d1e7e38dde3cc0e447f076f6ab5dd4203c70ecf5088b9
- Mapped relevant keys: 158→BACK, 172→HOME, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN

### system/system/usr/keylayout/Vendor_22b8_Product_093d.kl

- SHA256: 7f0309c1de67a80778fc204fd615de9545680f786e5a3a7781ff73385dfa7714
- Mapped relevant keys: 1→BACK, 43→BACKSLASH, 102→HOME, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 125→MENU

### system/system/usr/keylayout/Vendor_28de_Product_1102.kl

- SHA256: 3860298e64d7fbe46797c15f8cdb4b4f3df357d28d6a50c134d4a417361479a6
- Mapped relevant keys: 544→DPAD_UP, 545→DPAD_DOWN, 546→DPAD_LEFT, 547→DPAD_RIGHT

### vendor/usr/keylayout/Vendor_000d_Product_3838.kl

- SHA256: ee3994024ed680e498b4d9a04cce50e4d699e9575287a627c89b1be9edf9913f
- Mapped relevant keys: 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 116→POWER, 125→HOME, 192→BACK, 193→MENU

### vendor/usr/keylayout/Vendor_0046_Product_3838.kl

- SHA256: 0fb3ba7874c212a59199356bd58c00b640625ec01daeb1d6389fe78442257157
- Mapped relevant keys: 116→POWER, 28→DPAD_CENTER, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN

### vendor/usr/keylayout/Vendor_0094_Product_0001.kl

- SHA256: 2c6ffc85f17c3ca7185e1155376fc7cc5668fc2012f19855db81db5b8726409c
- Mapped relevant keys: 79→TV_INPUT, 88→TV_INPUT_COMPOSITE_2, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 116→POWER, 139→MENU, 158→BACK, 172→HOME, 183→TV_INPUT_COMPONENT_2, 212→TV_INPUT_VGA_1, 353→DPAD_CENTER, 376→TV_INPUT, 386→TV_INPUT_COMPOSITE_2

### vendor/usr/keylayout/Vendor_0094_Product_0002.kl

- SHA256: d3ecb000bf05d2fc904ac46b4458401657e52290312575cc1bcf3d7012de8a62
- Mapped relevant keys: 116→POWER, 103→DPAD_UP, 108→DPAD_DOWN, 105→DPAD_LEFT, 106→DPAD_RIGHT, 353→DPAD_CENTER, 158→BACK, 172→HOME, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 88→TV_INPUT_COMPOSITE_2, 183→TV_INPUT_COMPONENT_2, 212→TV_INPUT_VGA_1, 386→TV_INPUT_COMPOSITE_2, 139→MENU

### vendor/usr/keylayout/Vendor_045e_Product_077c.kl

- SHA256: 87d4e5ee8cc740569c4bf706887c0910c245fce13512b52b6a16cb49c688a2ea
- Mapped relevant keys: 43→BACKSLASH, 86→BACKSLASH, 102→MOVE_HOME, 103→DPAD_UP, 105→DPAD_LEFT, 106→DPAD_RIGHT, 108→DPAD_DOWN, 113→VOLUME_MUTE, 114→VOLUME_DOWN, 115→VOLUME_UP, 116→POWER, 127→MENU, 139→MENU, 152→POWER, 158→BACK, 172→HOME, 353→DPAD_CENTER

### vendor/usr/keylayout/Vendor_1d5a_Product_c080.kl

- SHA256: 5ad5ab29528adbb37fc4cf3d28b1f723efdc53b6edd129a192f6ee85f3e3e081
- Mapped relevant keys: 103→DPAD_UP, 105→DPAD_LEFT, 353→DPAD_CENTER, 106→DPAD_RIGHT, 108→DPAD_DOWN

### vendor/usr/keylayout/Vendor_3697_Product_0001.kl

- SHA256: 0367aa14685dc79f992c32f43d2bb9f004e40b049344dd437d785b666982a26d
- Mapped relevant keys: 116→POWER, 103→DPAD_UP, 108→DPAD_DOWN, 105→DPAD_LEFT, 106→DPAD_RIGHT, 28→DPAD_CENTER, 115→VOLUME_UP, 114→VOLUME_DOWN, 88→TV_INPUT_COMPOSITE_2, 102→HOME, 139→MENU, 158→BACK, 365→BACK, 113→VOLUME_MUTE, 212→TV_INPUT_VGA_1, 356→TV_POWER, 79→TV_INPUT, 528→FOCUS, 744→FOCUS_PLUS, 745→FOCUS_MINUS, 747→TRD_POPMENU, 751→FOCUS_RESET, 755→SOURCE

### vendor/usr/keylayout/Vendor_3697_Product_0002.kl

- SHA256: a3dfbfbb2205ef2fd2e159c28db030dd559b5c2b7e8c48b544d180b724d55aab
- Mapped relevant keys: 116→POWER, 139→MENU, 79→TV_INPUT, 402→DPAD_UP, 403→DPAD_DOWN

### vendor/usr/keylayout/Vendor_3697_Product_0003.kl

- SHA256: 2ca167e4dc39dcf528faa04edf1255af81f7db3c833769d3bad9f2ee6b166c32
- Mapped relevant keys: 116→POWER, 113→VOLUME_MUTE, 139→MENU, 158→BACK, 103→DPAD_UP, 108→DPAD_DOWN, 105→DPAD_LEFT, 106→DPAD_RIGHT, 115→VOLUME_UP, 114→VOLUME_DOWN, 102→HOME, 467→TV_INPUT


## APK and overlay coverage

All APK paths (including APEX-bundled APK) listed in JSON. APK on disk does not prove installed for user 0 or actively started.
Overlay list: vendor/overlay/WifiRROOverlay.apk, vendor/overlay/TetheringInprocessRROOverlay.apk, vendor/overlay/TetheringRROOverlay.apk

## Current unknowns and release implications

- Android Settings may be redirected by launchers, GlobalKeyEventProcess, default intents and overlay definitions; a .kl mapping alone cannot prove target Activity.
- OEM privileged permissions can depend on platform signature, shared UID, SELinux and execution context. Copying an APK to priv-app does not automatically restore those rights.
- Compare this latest 8052 index with a **verified 8054 of the same release generation** before removing OEM binaries.
- Boot service presence is a configuration fact, not proof of an active driver/daemon at runtime.
- No OEM binaries, keys, firmware or personal identifiers were exported.

