# Latest 8052 stock APK dependency and code review index

Read-only AAPT/JADX scan of verified October OTA. Only code reference identifiers and locations are retained.
Presence of a token in decompiled output **does not prove invocation, dependency or bug**.

| App | Package | Decompiled Java files | BOOT_COMPLETED | Manifest HOME/LAUNCHER hint | OEM hardware references |
|---|---|---:|---|---|---:|
| zxlauncher | com.zeasn.whale.saas | 10819 | False | True | 0 |
| zxstore | zeasn.open.technical.tv.store | 10729 | True | True | 4 |
| KuSettings | com.my.settings | 3470 | True | True | 1 |
| TvSettingsPlus | com.android.tv.settings | 5796 | True | True | 221 |
| RuiYunOta | com.rjpj.yunota | 75 | True | False | 0 |
| KuSourceRJ | com.coolux.source | 3007 | True | True | 172 |
| RuiAutoFocus | com.hysd.screen | 1091 | True | False | 328 |
| KeystoneCorrection | com.rjpj.tcorrection | 449 | False | False | 186 |
| trdservice | com.trd.service | 438 | False | False | 70 |
| trdmiddle | com.trd.framework | 568 | False | False | 26 |
| Factory | mediatek.factorymenu.ui | 1866 | False | False | 26 |
| TvServices | com.mediatek.tv.service | 474 | True | False | 3 |
| LiveTV | com.mediatek.wwtv.tvcenter | 2246 | True | False | 23 |
| KuSetupWizard | com.android.provision | 3471 | True | True | 1 |

## zxlauncher

- APK SHA256: 9a0e4b69eff2e1264e45810746e16acc26b598f186dd04e19089830164af4ffd
- Component counts: {'activity': 19, 'provider': 2, 'service': 4, 'receiver': 4}
- Launcher activities: ['com.zeasn.launcher.ui.MainActivity', 'com.zeasn.launcher.ui.MainActivity']
- Permissions: android.permission.ACCESS_DOWNLOAD_MANAGER, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.CAMERA, android.permission.CHANGE_NETWORK_STATE, android.permission.DELETE_PACKAGES, android.permission.DOWNLOAD_WITHOUT_NOTIFICATION, android.permission.FOREGROUND_SERVICE, android.permission.INSTALL_PACKAGES, android.permission.INTERNET, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_PHONE_STATE, android.permission.READ_PRIVILEGED_PHONE_STATE, android.permission.REQUEST_DELETE_PACKAGES, android.permission.REQUEST_INSTALL_PACKAGES, android.permission.REQUEST_INSTALL_PACKAGES , android.permission.SYSTEM_ALERT_WINDOW, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_SECURE_SETTINGS, com.google.android.gms.permission.AD_ID
- Signal occurrences: {'review': 9, 'installer': 153, 'settings': 2}

### Candidate review locations
- review: com/zeasn/utils/AppUtil.java:741 (System.exit)
- review: com/zeasn/utils/AppUtil.java:766 (ProcessBuilder)
- review: com/zeasn/utils/ActivityManager.java:147 (System.exit)
- review: com/zeasn/launcher/dialog/AuthDialogBuilder.java:65 (ProcessBuilder)
- review: com/zeasn/launcher/dialog/AuthDialogBuilder.java:91 (System.exit)
- review: com/zeasn/launcher/base/ui/dialog/BaseMacAuthDialogBuilder.java:103 (System.exit)
- review: com/android/media/api/service_api/utils/AppUtils.java:103 (ProcessBuilder)
- review: kotlin/system/ProcessKt.java:8 (System.exit)
- installer: com/zeasn/utils/AppUtil.java:757 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:899 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:899 (packageInstaller)
- installer: com/zeasn/utils/AppUtil.java:899 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:900 (packageInstaller)
- installer: com/zeasn/utils/AppUtil.java:900 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:901 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:905 (PackageInstaller)
- settings: com/zeasn/ad/connector/access/ABSettingHelper.java:93 (Settings.Secure.put)
- settings: com/zeasn/ad/connector/access/ABSettingHelper.java:94 (Settings.Secure.put)

## zxstore

- APK SHA256: d2f646175e0abb1f5abfe3b1d0915e40ca40cb3d5112edd7085b560ee6df6586
- Component counts: {'activity': 13, 'provider': 3, 'receiver': 5, 'service': 4}
- Launcher activities: ['zeasn.open.technical.tv.store.ui.MainActivity', 'zeasn.open.technical.tv.store.ui.MainActivity']
- Permissions: android.permission.ACCESS_COARSE_LOCATION, android.permission.ACCESS_COARSE_UPDATES, android.permission.ACCESS_DOWNLOAD_MANAGER, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BROADCAST_STICKY, android.permission.CHANGE_CONFIGURATION, android.permission.CHANGE_WIFI_STATE, android.permission.CLEAR_APP_CACHE, android.permission.CLEAR_APP_USER_DATA, android.permission.DELETE_PACKAGES, android.permission.DOWNLOAD_WITHOUT_NOTIFICATION, android.permission.FOREGROUND_SERVICE, android.permission.INSTALL_PACKAGES, android.permission.INTERACT_ACROSS_USERS, android.permission.INTERNET, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_PHONE_STATE, android.permission.READ_PRIVILEGED_PHONE_STATE, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.REORDER_TASKS, android.permission.REQUEST_DELETE_PACKAGES, android.permission.REQUEST_INSTALL_PACKAGES, android.permission.RESTART_PACKAGES, android.permission.SYSTEM_ALERT_WINDOW, android.permission.SYSTEM_OVERLAY_WINDOW, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, com.google.android.gms.permission.AD_ID
- Signal occurrences: {'installer': 196, 'review': 9, 'hdmi': 4, 'settings': 3}

### Candidate review locations
- installer: pm/PackageManager.java:246 (PackageInstaller)
- installer: pm/PackageManager.java:246 (PackageInstaller)
- installer: pm/PackageManager.java:363 (packageinstaller)
- installer: com/zeasn/utils/AppUtil.java:763 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:913 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:920 (PackageInstaller)
- installer: com/zeasn/utils/AppUtil.java:920 (packageInstaller)
- installer: com/zeasn/utils/AppUtil.java:920 (PackageInstaller)
- review: com/zeasn/utils/AppUtil.java:746 (System.exit)
- review: com/zeasn/utils/AppUtil.java:772 (ProcessBuilder)
- review: com/zeasn/utils/ActivityManager.java:147 (System.exit)
- review: com/android/media/api/service_api/utils/AppUtils.java:104 (ProcessBuilder)
- review: zeasn/open/technical/tv/store/app/InstallRunnable.java:72 (ProcessBuilder)
- review: zeasn/open/technical/tv/store/ui/dialogbuilder/BaseMacAuthDialogBuilder.java:151 (System.exit)
- review: zeasn/open/technical/tv/store/ui/dialogbuilder/NetworkWrongDialogBuilder.java:28 (System.exit)
- review: kotlin/system/ProcessKt.java:8 (System.exit)
- hdmi: com/hisilicon/android/tvapi/SourceManager.java:63 (setBootSource)
- hdmi: com/hisilicon/android/tvapi/constant/EnumSystemCmd.java:481 (SETBOOTSOURCE)
- hdmi: com/hisilicon/android/tvapi/impl/SourceManagerImpl.java:160 (setBootSource)
- hdmi: com/hisilicon/android/tvapi/impl/SourceManagerImpl.java:161 (SETBOOTSOURCE)
- settings: zeasn/open/technical/tv/store/app/InstallRunnable.java:292 (Settings.Global.put)
- settings: zeasn/open/technical/tv/store/app/AppDetailBoner.java:599 (Settings.Global.put)
- settings: zeasn/open/technical/tv/store/ui/UpgradeClientActivity.java:163 (Settings.Global.put)

## KuSettings

- APK SHA256: bd678e646a0cbc164f34273bcd396f9cf9221037b4c688d9d08464840cfca58b
- Component counts: {'activity': 11, 'service': 2, 'receiver': 2, 'provider': 1}
- Launcher activities: ['com.my.settings.SettingActivity']
- Permissions: android.permission.ACCESS_FINE_LOCATION, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BACKUP, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.BLUETOOTH_CONNECT, android.permission.BLUETOOTH_PRIVILEGED, android.permission.BLUETOOTH_SCAN, android.permission.CHANGE_NETWORK_STATE, android.permission.CHANGE_WIFI_STATE, android.permission.CLEAR_APP_USER_DATA, android.permission.CONNECTIVITY_INTERNAL, android.permission.DELETE_CACHE_FILES, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_ACCOUNTS, android.permission.GET_PACKAGE_SIZE, android.permission.INJECT_EVENTS, android.permission.INTERNET, android.permission.MANAGE_ACCOUNTS, android.permission.MANAGE_USERS, android.permission.MASTER_CLEAR, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.OVERRIDE_WIFI_CONFIG, android.permission.QUERY_ALL_PACKAGES, android.permission.READ_CONTACTS, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_PHONE_STATE, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.RECOVERY, android.permission.SET_PREFERRED_APPLICATIONS, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.SYSTEM_ALERT_WINDOW, android.permission.TETHER_PRIVILEGED, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, com.my.settings.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
- Signal occurrences: {'ota': 1, 'settings': 8, 'binder': 1, 'review': 3, 'installer': 2}

### Candidate review locations
- ota: com/my/utils/IntentUtils.java:68 (OTASystemNetworkUpdateActivity)
- settings: com/my/settings/AirplaneModeEnabler.java:41 (Settings.Global.put)
- settings: com/my/service/ScreenServices.java:39 (SystemProperties.set)
- settings: com/my/settings/language/InputMethodManagerUtils.java:33 (Settings.Secure.put)
- settings: com/my/settings/time/DateTimeUtils.java:33 (Settings.Global.put)
- settings: com/my/settings/time/DateTimeUtils.java:37 (Settings.Global.put)
- settings: com/my/settings/activity/WarningActivity.java:36 (Settings.Global.put)
- settings: com/my/settings/activity/WarningActivity.java:37 (Settings.Secure.put)
- settings: com/my/settings/activity/WarningActivity.java:38 (Settings.Secure.put)
- binder: com/my/settings/Utils.java:310 (ServiceManager.getService)
- review: com/my/settings/activity/WarningActivity.java:49 (System.exit)
- review: kotlin/system/ProcessKt.java:8 (System.exit)
- review: kotlin/system/ProcessKt.java:9 (System.exit)
- installer: androidx/profileinstaller/ProfileInstaller.java:50 (INSTALL_SUCCESS)
- installer: androidx/profileinstaller/ProfileInstaller.java:105 (INSTALL_SUCCESS)

## TvSettingsPlus

- APK SHA256: e4184a13fbf56fa069effc6a40ea50c0da7e9190321b389f59ba34700a80d0a1
- Component counts: {'provider': 6, 'activity': 120, 'receiver': 12, 'service': 8}
- Launcher activities: ['com.android.tv.settings.MainSettings']
- Permissions: android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BACKUP, android.permission.BIND_TV_INPUT, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.BLUETOOTH_ADVERTISE, android.permission.BLUETOOTH_CONNECT, android.permission.BLUETOOTH_PRIVILEGED, android.permission.BLUETOOTH_SCAN, android.permission.CHANGE_WIFI_STATE, android.permission.CLEAR_APP_USER_DATA, android.permission.DELETE_CACHE_FILES, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_ACCOUNTS_PRIVILEGED, android.permission.GET_PACKAGE_SIZE, android.permission.INJECT_EVENTS, android.permission.INTERNET, android.permission.MANAGE_ACCOUNTS, android.permission.MANAGE_DEBUGGING, android.permission.MANAGE_EXTERNAL_STORAGE, android.permission.MANAGE_PROFILE_AND_DEVICE_OWNERS, android.permission.MANAGE_SCOPED_ACCESS_DIRECTORY_PERMISSIONS, android.permission.MANAGE_SENSOR_PRIVACY, android.permission.MANAGE_SLICE_PERMISSIONS, android.permission.MANAGE_USERS, android.permission.NETWORK_SETTINGS, android.permission.OBSERVE_SENSOR_PRIVACY, android.permission.OVERRIDE_WIFI_CONFIG, android.permission.PEERS_MAC_ADDRESS, android.permission.QUERY_ALL_PACKAGES, android.permission.READ_CONTACTS, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_PROFILE, android.permission.REBOOT, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.RECORD_AUDIO, android.permission.REQUEST_DELETE_PACKAGES, android.permission.SET_PREFERRED_APPLICATIONS, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.SET_UNRESTRICTED_KEEP_CLEAR_AREAS, android.permission.START_ACTIVITIES_FROM_BACKGROUND, android.permission.SUGGEST_MANUAL_TIME_AND_ZONE, android.permission.TV_INPUT_HARDWARE, android.permission.USE_RESERVED_DISK, android.permission.WRITE_EPG_DATA, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, androidx.appcompat.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.leanback.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.leanback.preference.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.legacy.preference.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.legacy.v4.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.preference.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.recyclerview.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, com.android.providers.tv.permission.WRITE_EPG_DATA, com.android.settingslib.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, com.android.tv.settings.library.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, com.android.tv.twopanelsettings.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, com.google.android.assistant.READ_HOTWORD_STATE, com.google.android.assistant.WRITE_HOTWORD_STATE, com.mediatek.tv.permission.BROADCAST, com.netflix.ninja.permission.ESN, com.netflix.ninja.permission.ESN_RESPONSE
- Signal occurrences: {'binder': 20, 'hdmi': 175, 'installer': 254, 'settings': 375, 'i2c': 26, 'ota': 12, 'review': 7}

### Candidate review locations
- binder: com/mediatek/dm/DMServer.java:44 (ServiceManager.getService)
- binder: com/android/settingslib/dream/DreamBackend.java:76 (ServiceManager.getService)
- binder: com/android/settingslib/fuelgauge/PowerAllowlistBackend.java:15 (ServiceManager.getService)
- binder: com/android/tv/settings/device/apps/ClearDefaultsPreference.java:10 (ServiceManager.getService)
- binder: com/android/tv/settings/device/apps/ClearDefaultsPreference.java:60 (ServiceManager.getService)
- binder: com/android/tv/settings/system/development/AdbKeysDialog.java:25 (ServiceManager.getService)
- binder: com/android/tv/settings/system/development/WirelessDebuggingFragment.java:51 (ServiceManager.getService)
- binder: com/android/tv/settings/system/development/WirelessDebuggingFragment.java:385 (ServiceManager.getService)
- hdmi: com/mediatek/tv/ui/R.java:7745 (hdmi_cec)
- hdmi: com/mediatek/tv/ui/R.java:9886 (hdmi_cec)
- hdmi: com/mediatek/support/androidversioncompatiblelib/CompatibleApis.java:6 (HdmiControlManager)
- hdmi: com/mediatek/support/androidversioncompatiblelib/CompatibleApis.java:11 (HdmiControlManager)
- hdmi: com/mediatek/support/androidversioncompatiblelib/CompatibleApis.java:11 (HdmiControlManager)
- hdmi: com/mediatek/support/sharecode/R.java:7745 (hdmi_cec)
- hdmi: com/mediatek/support/sharecode/R.java:9886 (hdmi_cec)
- hdmi: com/google/android/setupdesign/R.java:7745 (hdmi_cec)
- installer: com/mediatek/tv/ui/R.java:9665 (install_success)
- installer: com/mediatek/tv/ui/R.java:10312 (install_success)
- installer: com/mediatek/tv/ui/R.java:10324 (install_success)
- installer: com/mediatek/tv/ui/R.java:10325 (install_success)
- installer: com/mediatek/support/sharecode/R.java:9665 (install_success)
- installer: com/mediatek/support/sharecode/R.java:10312 (install_success)
- installer: com/mediatek/support/sharecode/R.java:10324 (install_success)
- installer: com/mediatek/support/sharecode/R.java:10325 (install_success)
- settings: com/android/settingslib/Utils.java:16 (Settings.Secure.put)
- settings: com/android/settingslib/notification/ZenDurationDialog.java:85 (Settings.Secure.put)
- settings: com/android/settingslib/dream/DreamBackend.java:238 (Settings.Secure.put)
- settings: com/android/settingslib/dream/DreamBackend.java:314 (Settings.Secure.put)
- settings: com/android/settingslib/development/AbstractLogpersistPreferenceController.java:135 (SystemProperties.set)
- settings: com/android/settingslib/development/AbstractLogpersistPreferenceController.java:143 (SystemProperties.set)
- settings: com/android/settingslib/development/AbstractLogpersistPreferenceController.java:144 (SystemProperties.set)
- settings: com/android/settingslib/development/AbstractLogpersistPreferenceController.java:145 (SystemProperties.set)
- i2c: com/android/tv/settings/uicustom/I2CDevice.java:4 (I2CDevice)
- i2c: com/android/tv/settings/uicustom/I2CDevice.java:11 (readRegister)
- i2c: com/android/tv/settings/uicustom/I2CDevice.java:13 (writeRegister)
- i2c: com/android/tv/settings/uicustom/util/ProjectorManager.java:44 (I2CDevice)
- i2c: com/android/tv/settings/uicustom/util/ProjectorManager.java:44 (i2CDevice)
- i2c: com/android/tv/settings/uicustom/util/ProjectorManager.java:48 (I2CDevice)
- i2c: com/android/tv/settings/uicustom/util/ProjectorManager.java:48 (i2CDevice)
- i2c: com/android/tv/settings/uicustom/util/ProjectorManager.java:48 (I2CDevice)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:38 (UpdateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:58 (updateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:149 (updateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:189 (updateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:194 (updateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:196 (updateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:201 (updateEngine)
- ota: com/android/tv/settings/system/TextToSpeechFragment.java:318 (updateEngine)
- review: com/android/tv/settings/uicustom/util/MtkUtil.java:161 (ProcessBuilder)
- review: com/android/tv/settings/uicustom/util/MtkUtil.java:161 (processBuilder)
- review: com/android/tv/settings/uicustom/util/MtkUtil.java:161 (ProcessBuilder)
- review: com/android/tv/settings/uicustom/util/MtkUtil.java:162 (processBuilder)
- review: com/android/tv/settings/uicustom/util/MtkUtil.java:164 (processBuilder)
- review: kotlin/system/ProcessKt.java:10 (System.exit)
- review: kotlin/system/ProcessKt.java:11 (System.exit)

## RuiYunOta

- APK SHA256: 40f399ff15b692180243ce103469230bcb7f90278fc4ad5f6c7d86cbc75961a2
- Component counts: {'activity': 4, 'service': 2}
- Launcher activities: []
- Permissions: android.permission.ACCESS_DOWNLOAD_MANAGER, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BACKUP, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.CHANGE_WIFI_STATE, android.permission.CLEAR_APP_USER_DATA, android.permission.DELETE_CACHE_FILES, android.permission.DOWNLOAD_WITHOUT_NOTIFICATION, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_ACCOUNTS_PRIVILEGED, android.permission.GET_PACKAGE_SIZE, android.permission.INJECT_EVENTS, android.permission.INTERNET, android.permission.MANAGE_ACCOUNTS, android.permission.MANAGE_SCOPED_ACCESS_DIRECTORY_PERMISSIONS, android.permission.MANAGE_USERS, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.NETWORK_SETTINGS, android.permission.OVERRIDE_WIFI_CONFIG, android.permission.PEERS_MAC_ADDRESS, android.permission.READ_CONTACTS, android.permission.READ_EXTERNAL_STORAGE, android.permission.REBOOT, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.REQUEST_DELETE_PACKAGES, android.permission.SET_PREFERRED_APPLICATIONS, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.SYSTEM_ALERT_WINDOW, android.permission.USE_RESERVED_DISK, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, com.google.android.assistant.READ_HOTWORD_STATE, com.google.android.assistant.WRITE_HOTWORD_STATE, com.netflix.ninja.permission.ESN, com.netflix.ninja.permission.ESN_RESPONSE
- Signal occurrences: {'ota': 269, 'review': 1}

### Candidate review locations
- ota: com/rjpj/yunota/AbUpdate.java:45 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:45 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:261 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:261 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:458 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:478 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:481 (UpdateEngine)
- ota: com/rjpj/yunota/AbUpdate.java:495 (UpdateEngine)
- review: com/rjpj/yunota/OTASystemNetworkUpdateActivity.java:271 (System.exit)

## KuSourceRJ

- APK SHA256: 15bf7b9fe31844bace197989ae393af7c3e4ca5a9c3c2019a4f662f0a9d881cc
- Component counts: {'activity': 33, 'receiver': 3, 'service': 1, 'provider': 1}
- Launcher activities: ['com.coolux.source.MainActivity']
- Permissions: android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BIND_TV_INPUT, android.permission.CHANGE_NETWORK_STATE, android.permission.CHANGE_WIFI_STATE, android.permission.INTERNET, android.permission.TV_INPUT_HARDWARE, android.permission.WRITE_EPG_DATA, com.android.providers.tv.permission.WRITE_EPG_DATA, com.coolux.source.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
- Signal occurrences: {'binder': 118, 'hdmi': 17, 'settings': 8, 'motor_tof': 37, 'review': 4}

### Candidate review locations
- binder: com/coolux/source/utils/ImageUtils.java:49 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:53 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:71 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:75 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:79 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:89 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:98 (TrdSystemManager)
- binder: com/coolux/source/utils/ImageUtils.java:102 (TrdSystemManager)
- hdmi: com/coolux/source/utils/ImageUtils.java:117 (setBootSource)
- hdmi: com/coolux/source/activity/BootSoureActivity.java:78 (setBootSource)
- hdmi: com/coolux/source/activity/BootSoureActivity.java:79 (setBootSource)
- hdmi: com/coolux/source/activity/BootSoureActivity.java:154 (setBootSource)
- hdmi: com/coolux/source/activity/BootSoureActivityOld.java:76 (setBootSource)
- hdmi: com/coolux/source/activity/BootSoureActivityOld.java:77 (setBootSource)
- hdmi: com/coolux/source/activity/BootSoureActivityOld.java:160 (setBootSource)
- hdmi: com/coolux/source/activity/AllAppAutoActivity.java:81 (setBootSource)
- settings: com/coolux/source/utils/ImageUtils.java:137 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:430 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:438 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:446 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:454 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:462 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:470 (SystemProperties.set)
- settings: com/coolux/source/utils/ImageUtils.java:492 (SystemProperties.set)
- motor_tof: com/trd/framework/ITrdSystemService.java:43 (ITofCtrl)
- motor_tof: com/trd/framework/ITrdSystemService.java:64 (ITofCtrl)
- motor_tof: com/trd/framework/ITrdSystemService.java:149 (ITofCtrl)
- motor_tof: com/trd/framework/ITrdSystemService.java:296 (ITofCtrl)
- motor_tof: com/trd/framework/ITrdSystemService.java:305 (ITofCtrl)
- motor_tof: com/trd/framework/ITofCtrl.java:4 (ITofCtrl)
- motor_tof: com/trd/framework/ITofCtrl.java:6 (ITofCtrl)
- motor_tof: com/trd/framework/ITofCtrl.java:7 (ITofCtrl)
- review: com/trd/common/utils/FileUtil.java:474 (ProcessBuilder)
- review: com/trd/common/utils/FileUtil.java:490 (ProcessBuilder)
- review: kotlin/system/ProcessKt.java:8 (System.exit)
- review: kotlin/system/ProcessKt.java:9 (System.exit)

## RuiAutoFocus

- APK SHA256: aa5257b38dc299d2160a5b5293915f3e0b4a88e690c5b6cd5a0bc2c940dc842f
- Component counts: {'service': 1, 'activity': 1}
- Launcher activities: []
- Permissions: android.permission.ACCESS_COARSE_LOCATION, android.permission.ACCESS_FINE_LOCATION, android.permission.ACCESS_NETWORK_STATE, android.permission.ACTIVITY_RECOGNITION, android.permission.CAMERA, android.permission.DISABLE_KEYGUARD, android.permission.FLASHLIGHT, android.permission.INJECT_EVENTS, android.permission.INTERACT_ACROSS_USERS, android.permission.INTERNET, android.permission.READ_EXTERNAL_STORAGE, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.SENSOR_ENABLE, android.permission.SENSOR_INFO, android.permission.SYSTEM_ALERT_WINDOW, android.permission.SYSTEM_OVERLAY_WINDOW, android.permission.WRITE_EXTERNAL_STORAGE
- Signal occurrences: {'motor_tof': 214, 'settings': 167, 'binder': 105, 'hdmi': 9, 'review': 2}

### Candidate review locations
- motor_tof: com/rui/cameraapi/MotorJNI.java:4 (MotorJNI)
- motor_tof: com/rui/cameraapi/MotorJNI.java:21 (MotorBack)
- motor_tof: com/rui/cameraapi/MotorJNI.java:23 (MotorFront)
- motor_tof: com/rui/cameraapi/MotorJNI.java:25 (MotorStop)
- motor_tof: com/hysd/xymscreen/MainActivity.java:392 (MotorBack)
- motor_tof: com/hysd/xymscreen/MainActivity.java:394 (MotorBack)
- motor_tof: com/hysd/xymscreen/MainActivity.java:409 (MotorFront)
- motor_tof: com/hysd/xymscreen/MainActivity.java:411 (MotorFront)
- settings: com/hysd/ai/RuiCameraApi.java:337 (SystemProperties.set)
- settings: mediatek/sysprop/TestProperties.java:171 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:165 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:173 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:181 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:195 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:203 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:211 (SystemProperties.set)
- binder: com/trd/common/TrdContext.java:6 (ServiceManager.getService)
- binder: com/trd/framework/ITrdSystemService.java:4 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:9 (getProjectorCtrl)
- binder: com/trd/framework/ITrdSystemService.java:17 (getTofCtrl)
- binder: com/trd/framework/ITrdSystemService.java:21 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:22 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:26 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:31 (ITrdSystemService)
- hdmi: com/trd/framework/ISystemCtrl.java:89 (setBootSource)
- hdmi: com/trd/framework/ISystemCtrl.java:147 (setBootSource)
- hdmi: com/trd/framework/ISystemCtrl.java:470 (setBootSource)
- hdmi: com/trd/framework/ISystemCtrl.java:540 (setBootSource)
- hdmi: com/trd/framework/ISystemCtrl.java:961 (setBootSource)
- hdmi: com/trd/framework/ISystemCtrl.java:974 (setBootSource)
- hdmi: com/trd/sdk/SystemCtrl.java:91 (setBootSource)
- hdmi: com/trd/sdk/impl/SystemCtrlImpl.java:69 (setBootSource)
- review: com/trd/common/utils/FileUtil.java:473 (ProcessBuilder)
- review: com/trd/common/utils/FileUtil.java:491 (ProcessBuilder)

## KeystoneCorrection

- APK SHA256: 23c68874b1ad2147549b3538ebe7f9ad7c97987a99ccb165ec528a6467b98829
- Component counts: {'activity': 4, 'receiver': 1, 'provider': 1}
- Launcher activities: []
- Permissions: androidx.constraintlayout.widget.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
- Signal occurrences: {'i2c': 158, 'settings': 9, 'binder': 28}

### Candidate review locations
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:114 (I2CDevice)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:114 (i2CDevice)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:118 (I2CDevice)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:118 (i2CDevice)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:118 (I2CDevice)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:120 (i2CDevice)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:120 (/dev/i2c-)
- i2c: com/rjpj/tcorrection/KeystoneUtil.java:122 (i2CDevice)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:226 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:273 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:274 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:275 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:276 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:277 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:278 (SystemProperties.set)
- settings: com/rjpj/tcorrection/KeystoneUtil.java:279 (SystemProperties.set)
- binder: com/rjpj/tcorrection/KeystoneUtil.java:264 (TrdSystemManager)
- binder: com/trd/common/TrdContext.java:6 (ServiceManager.getService)
- binder: com/trd/framework/ITrdSystemService.java:4 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:5 (getProjectorCtrl)
- binder: com/trd/framework/ITrdSystemService.java:7 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:8 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:12 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:13 (ITrdSystemService)

## trdservice

- APK SHA256: 309eaf1098bf3d544907b57fa24ae6ad31c591fe942133fd8ef1c69832d538f1
- Component counts: {'activity': 1, 'service': 1, 'receiver': 1, 'provider': 1}
- Launcher activities: []
- Permissions: android.Manifest.permission.WRITE_DREAM_STATE, android.permission.ACCESS_TUNED_INFO, android.permission.ACCESS_WIFI_STATE, android.permission.BLUETOOTH_CONNECT, android.permission.HDMI_CEC, android.permission.INTERNET, android.permission.READ_EXTERNAL_STORAGE, android.permission.SYSTEM_ALERT_WINDOW, androidx.constraintlayout.widget.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
- Signal occurrences: {'binder': 35, 'ota': 4, 'settings': 12, 'motor_tof': 35}

### Candidate review locations
- binder: com/trd/common/TrdContext.java:6 (ServiceManager.getService)
- binder: com/trd/framework/ITrdSystemService.java:4 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:9 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:10 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:14 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:15 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:16 (ITrdSystemService)
- binder: com/trd/framework/ITrdSystemService.java:18 (ITrdSystemService)
- ota: com/trd/service/TrdService.java:17 (OTACheckService)
- ota: com/trd/service/TrdService.java:209 (OTACheckService)
- ota: com/trd/service/TrdService.java:211 (OTACheckService)
- ota: com/trd/service/TrdService.java:222 (OTACheckService)
- settings: com/trd/service/TrdService.java:225 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:297 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:307 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:319 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:321 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:323 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:325 (SystemProperties.set)
- settings: com/trd/service/TrdService.java:327 (SystemProperties.set)
- motor_tof: com/trd/service/jni/MotorJNI.java:4 (MotorJNI)
- motor_tof: com/trd/service/jni/MotorJNI.java:9 (MotorBack)
- motor_tof: com/trd/service/jni/MotorJNI.java:11 (MotorFront)
- motor_tof: com/trd/service/jni/MotorJNI.java:13 (MotorStop)
- motor_tof: com/trd/service/ui/RJFocusDialog.java:55 (MotorJNI)
- motor_tof: com/trd/service/ui/RJFocusDialog.java:55 (motorJNI)
- motor_tof: com/trd/service/ui/RJFocusDialog.java:55 (MotorJNI)
- motor_tof: com/trd/service/ui/RJFocusDialog.java:56 (motorJNI)

## trdmiddle

- APK SHA256: d51088086756a96ad184ec31189c2b8babe7ba3b605b55375fd9e07c4f58bfa4
- Component counts: {'activity': 1, 'service': 1}
- Launcher activities: []
- Permissions: android.Manifest.permission.WRITE_DREAM_STATE, android.permission.BLUETOOTH_CONNECT, android.permission.INTERNET, android.permission.READ_EXTERNAL_STORAGE, android.permission.SYSTEM_ALERT_WINDOW
- Signal occurrences: {'settings': 47, 'hdmi': 7, 'binder': 18, 'motor_tof': 1}

### Candidate review locations
- settings: o/a.java:263 (SystemProperties.set)
- settings: l/b.java:494 (SystemProperties.set)
- settings: l/b.java:502 (SystemProperties.set)
- settings: l/i.java:97 (SystemProperties.set)
- settings: l/i.java:106 (SystemProperties.set)
- settings: e/c.java:373 (SystemProperties.set)
- settings: e/c.java:374 (SystemProperties.set)
- settings: e/c.java:375 (SystemProperties.set)
- hdmi: e/h.java:53 (setBootSource)
- hdmi: e/c.java:474 (setBootSource)
- hdmi: e/c.java:477 (setBootSource)
- hdmi: k/a.java:1423 (setBootSource)
- hdmi: k/a.java:1424 (setBootSource)
- hdmi: com/trd/framework/e.java:42 (setBootSource)
- hdmi: com/trd/framework/e.java:469 (setBootSource)
- binder: d/d.java:23 (ServiceManager.getService)
- binder: com/trd/framework/k.java:8 (ITrdSystemService)
- binder: com/trd/framework/k.java:19 (ITrdSystemService)
- binder: com/trd/framework/k.java:24 (ITrdSystemService)
- binder: com/trd/framework/k.java:29 (ITrdSystemService)
- binder: com/trd/framework/k.java:35 (ITrdSystemService)
- binder: com/trd/framework/k.java:36 (getProjectorCtrl)
- binder: com/trd/framework/k.java:41 (ITrdSystemService)
- motor_tof: com/trd/framework/h.java:7 (ITofCtrl)

## Factory

- APK SHA256: 40e755ec443340f1df1781388cd9807822176c848fb1d3082c48ff3719a1bcab
- Component counts: {'activity': 21, 'service': 2}
- Launcher activities: []
- Permissions: android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.CHANGE_NETWORK_STATE, android.permission.CHANGE_WIFI_STATE, android.permission.INTERNET, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.NETWROK_SETTINGS, android.permission.READ_EXTERNAL_STORAGE, android.permission.RECORD_AUDIO, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, com.mediatek.select.source, com.mediatek.tv.stop.source
- Signal occurrences: {'review': 8, 'settings': 178, 'i2c': 26}

### Candidate review locations
- review: org/jtransforms/fft/BenchmarkDoubleFFT.java:540 (System.exit)
- review: org/jtransforms/fft/BenchmarkFloatFFT.java:538 (System.exit)
- review: org/jtransforms/dct/BenchmarkDoubleDCT.java:304 (System.exit)
- review: org/jtransforms/dct/BenchmarkFloatDCT.java:297 (System.exit)
- review: org/jtransforms/dht/BenchmarkDoubleDHT.java:297 (System.exit)
- review: org/jtransforms/dht/BenchmarkFloatDHT.java:297 (System.exit)
- review: org/jtransforms/dst/BenchmarkFloatDST.java:297 (System.exit)
- review: org/jtransforms/dst/BenchmarkDoubleDST.java:297 (System.exit)
- settings: com/android/tv/settings/partnercustomizer/tvsettingservice/TVSettingConfig.java:673 (Settings.Global.put)
- settings: com/android/tv/settings/partnercustomizer/tvsettingservice/TVSettingConfig.java:761 (Settings.Secure.put)
- settings: mediatek/sysprop/TestProperties.java:171 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:165 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:173 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:181 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:195 (SystemProperties.set)
- settings: mediatek/sysprop/VendorProperties.java:203 (SystemProperties.set)
- i2c: mediatek/util/I2CDevice.java:4 (I2CDevice)
- i2c: mediatek/util/I2CDevice.java:11 (readRegister)
- i2c: mediatek/util/I2CDevice.java:13 (writeRegister)
- i2c: mediatek/tvsetting/factory/ui/ProjectorManager.java:71 (I2CDevice)
- i2c: mediatek/tvsetting/factory/ui/ProjectorManager.java:71 (i2CDevice)
- i2c: mediatek/tvsetting/factory/ui/ProjectorManager.java:75 (I2CDevice)
- i2c: mediatek/tvsetting/factory/ui/ProjectorManager.java:75 (i2CDevice)
- i2c: mediatek/tvsetting/factory/ui/ProjectorManager.java:75 (I2CDevice)

## TvServices

- APK SHA256: d5260ce75c48978bd57383eed14c0ba524a73837bb079fb70147cef6078995e4
- Component counts: {'receiver': 7, 'provider': 4, 'service': 17, 'activity': 2}
- Launcher activities: []
- Permissions: adnroid.permission.ACCESS_CHECKIN_PROPERTTES, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BROADCAST_STICKY, android.permission.CHANGE_CONFIGURATION, android.permission.DEVICE_POWER, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_TASKS, android.permission.INJECT_EVENTS, android.permission.INTERACT_ACROSS_USERS, android.permission.INTERACT_ACROSS_USERS_FULL, android.permission.INTERNET, android.permission.KILL_BACKGROUND_PROCESSES, android.permission.MANAGE_USERS, android.permission.MASTER_CLEAR, android.permission.MODIFY_AUDIO_SETTINGS, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.PACKAGE_USAGE_STATS, android.permission.READ_DREAM_STATE, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_LOGS, android.permission.READ_TV_LISTINGS, android.permission.REAL_GET_TASKS, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.REORDER_TASKS, android.permission.SET_ACTIVITY_WATCHER, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.START_ANY_ACTIVITY, android.permission.SYSTEM_ALERT_WINDOW, android.permission.TV_INPUT_HARDWARE, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, androidx.tvprovider.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, com.android.providers.tv.permission.ACCESS_ALL_EPG_DATA, com.android.providers.tv.permission.READ_EPG_DATA, com.android.providers.tv.permission.WRITE_EPG_DATA, com.android.tv.permission.RECEIVE_INPUT_EVENT, com.google.android.permission.GLOBAL_BUTTON, com.google.android.tv.permission.RECEIVE_INPUT_EVENT, com.mediatek.exoplayer.permission.BROADCAST, com.mediatek.tv.permission.BROADCAST, com.netflix.ninja.permission.NETFLIX_KEY, mtk.intent.EAS.message.permission
- Signal occurrences: {'binder': 3, 'settings': 30}

### Candidate review locations
- binder: com/mediatek/dm/DMServer.java:44 (ServiceManager.getService)
- binder: com/mediatek/tv/agent/HBBTVService.java:18 (ServiceManager.getService)
- binder: com/mediatek/tv/agent/DolbyVisionService.java:57 (ServiceManager.getService)
- settings: com/mediatek/hotkey/dispatcher/action/Action.java:145 (Settings.Global.put)
- settings: com/mediatek/tv/agent/RetailModeService.java:312 (Settings.Global.put)
- settings: com/mediatek/tv/agent/RetailModeService.java:317 (Settings.Global.put)
- settings: com/mediatek/tv/agent/LiveTVLauncher.java:124 (Settings.Secure.put)
- settings: com/mediatek/tv/agent/LiveTVLauncher.java:125 (Settings.Secure.put)
- settings: com/mediatek/tv/agent/LiveTVLauncher.java:126 (Settings.Global.put)
- settings: com/mediatek/tv/agent/SetAutoSleepDefValServices.java:38 (Settings.Secure.put)
- settings: com/mediatek/tv/agent/SetAutoSleepDefValServices.java:41 (Settings.Secure.put)

## LiveTV

- APK SHA256: c7c7c8c66d927ea1e36814104e95e85bd95402d29952b973cc0ee1edde4a790b
- Component counts: {'activity': 28, 'provider': 2, 'receiver': 5, 'service': 4}
- Launcher activities: []
- Permissions: android.permission.ACCESS_CHECKIN_PROPERTTES, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BIND_TV_INPUT, android.permission.BIND_TV_REMOTE_SERVICE, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.BROADCAST_STICKY, android.permission.CHANGE_CONFIGURATION, android.permission.CHANGE_HDMI_CEC_ACTIVE_SOURCE, android.permission.DEVICE_POWER, android.permission.FOREGROUND_SERVICE, android.permission.GET_TASKS, android.permission.HDMI_CEC, android.permission.INJECT_EVENTS, android.permission.INTERACT_ACROSS_USERS, android.permission.INTERNET, android.permission.KILL_BACKGROUND_PROCESSES, android.permission.MANAGE_EXTERNAL_STORAGE, android.permission.MODIFY_AUDIO_ROUTING, android.permission.MODIFY_AUDIO_SETTINGS, android.permission.MODIFY_PARENTAL_CONTROLS, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.READ_CONTENT_RATING_SYSTEMS, android.permission.READ_DREAM_STATE, android.permission.READ_EXTERNAL_STORAGE, android.permission.REAL_GET_TASKS, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.RECOVERY, android.permission.SET_TIME_ZONE, android.permission.SHUTDOWN, android.permission.START_ANY_ACTIVITY, android.permission.SYSTEM_ALERT_WINDOW, android.permission.TV_INPUT_HARDWARE, android.permission.WAKE_LOCK, android.permission.WRITE_DREAM_STATE, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, androidx.appcompat.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.leanback.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.leanback.preference.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.legacy.preference.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.lifecycle.extensions.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.paging.runtime.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.palette.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.preference.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.recyclerview.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, androidx.tvprovider.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION, com.android.providers.tv.permission.ACCESS_ALL_EPG_DATA, com.android.providers.tv.permission.READ_EPG_DATA, com.android.providers.tv.permission.WRITE_EPG_DATA, com.android.tv.permission.RECEIVE_INPUT_EVENT, com.google.android.tv.permission.RECEIVE_INPUT_EVENT, com.mediatek.tv.permission.BROADCAST, com.mediatek.wwtv.permission.DVR_READ, com.mediatek.wwtv.permission.DVR_WRITE
- Signal occurrences: {'binder': 4, 'installer': 12, 'settings': 11, 'hdmi': 19}

### Candidate review locations
- binder: com/mediatek/dm/DMServer.java:44 (ServiceManager.getService)
- binder: com/mediatek/mtkaudiopatchmanager/MtkAudioPatchManager.java:265 (ServiceManager.getService)
- binder: com/mediatek/wwtv/tvcenter/nav/view/VgaPowerManager.java:32 (ServiceManager.getService)
- binder: com/mediatek/wwtv/tvcenter/nav/util/InputSourceManager.java:364 (ServiceManager.getService)
- installer: com/mediatek/wwtv/tvcenter/R.java:5749 (install_success)
- installer: com/mediatek/wwtv/tvcenter/R.java:8392 (install_success)
- installer: com/mediatek/wwtv/tvcenter/R.java:8393 (install_success)
- installer: com/mediatek/wwtv/tvcenter/opapp/OpAppService.java:620 (install_success)
- installer: com/mediatek/wwtv/setting/view/FacSetup.java:365 (install_success)
- installer: com/mediatek/wwtv/setting/view/FacSetup.java:695 (install_success)
- installer: com/mediatek/tv/ui/R.java:5749 (install_success)
- installer: com/mediatek/tv/ui/R.java:8392 (install_success)
- settings: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1447 (Settings.Global.put)
- settings: com/mediatek/wwtv/tvcenter/util/DestroyApp.java:141 (Settings.Global.put)
- settings: com/mediatek/wwtv/tvcenter/util/BootBroadcastReceiver.java:39 (Settings.Global.put)
- settings: com/mediatek/wwtv/tvcenter/nav/util/InputSourceManager.java:1075 (SystemProperties.set)
- settings: com/mediatek/wwtv/tvcenter/dvr/controller/StateDvr.java:112 (Settings.Global.put)
- settings: com/mediatek/wwtv/tvcenter/dvr/controller/StateDvr.java:483 (Settings.Global.put)
- settings: com/mediatek/wwtv/setting/preferences/MenuListPreferenceFragment.java:346 (Settings.Global.put)
- settings: com/mediatek/wwtv/setting/preferences/PreferenceUtil.java:722 (Settings.Global.put)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1720 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1861 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1862 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1862 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1863 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1864 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/nav/TurnkeyUiMainActivity.java:1865 (SelectInput)
- hdmi: com/mediatek/wwtv/tvcenter/search/TvProviderSearch.java:8 (switchsource)

## KuSetupWizard

- APK SHA256: 17aaba977289fce5c991e44bd6018c37549f91dae1b99154b00b80b5a3a2c898
- Component counts: {'activity': 3, 'provider': 1, 'receiver': 1}
- Launcher activities: []
- Permissions: android.permission.ACCESS_FINE_LOCATION, android.permission.ACCESS_NETWORK_STATE, android.permission.ACCESS_WIFI_STATE, android.permission.BACKUP, android.permission.BLUETOOTH, android.permission.BLUETOOTH_ADMIN, android.permission.BLUETOOTH_CONNECT, android.permission.BLUETOOTH_PRIVILEGED, android.permission.BLUETOOTH_SCAN, android.permission.CHANGE_COMPONENT_ENABLED_STATE, android.permission.CHANGE_NETWORK_STATE, android.permission.CHANGE_WIFI_STATE, android.permission.CLEAR_APP_USER_DATA, android.permission.CONNECTIVITY_INTERNAL, android.permission.DELETE_CACHE_FILES, android.permission.DUMP, android.permission.FORCE_STOP_PACKAGES, android.permission.GET_ACCOUNTS, android.permission.GET_PACKAGE_SIZE, android.permission.INJECT_EVENTS, android.permission.INTERNET, android.permission.MANAGE_ACCOUNTS, android.permission.MANAGE_USERS, android.permission.MASTER_CLEAR, android.permission.MOUNT_UNMOUNT_FILESYSTEMS, android.permission.OVERRIDE_WIFI_CONFIG, android.permission.QUERY_ALL_PACKAGES, android.permission.READ_CONTACTS, android.permission.READ_EXTERNAL_STORAGE, android.permission.READ_PHONE_STATE, android.permission.RECEIVE_BOOT_COMPLETED, android.permission.RECOVERY, android.permission.SET_PREFERRED_APPLICATIONS, android.permission.SET_TIME, android.permission.SET_TIME_ZONE, android.permission.SYSTEM_ALERT_WINDOW, android.permission.TETHER_PRIVILEGED, android.permission.WAKE_LOCK, android.permission.WRITE_EXTERNAL_STORAGE, android.permission.WRITE_MEDIA_STORAGE, android.permission.WRITE_SECURE_SETTINGS, android.permission.WRITE_SETTINGS, com.android.provision.DYNAMIC_RECEIVER_NOT_EXPORTED_PERMISSION
- Signal occurrences: {'ota': 1, 'settings': 8, 'binder': 1, 'review': 3, 'installer': 2}

### Candidate review locations
- ota: com/my/utils/IntentUtils.java:68 (OTASystemNetworkUpdateActivity)
- settings: com/my/settings/AirplaneModeEnabler.java:41 (Settings.Global.put)
- settings: com/my/service/ScreenServices.java:39 (SystemProperties.set)
- settings: com/my/settings/language/InputMethodManagerUtils.java:33 (Settings.Secure.put)
- settings: com/my/settings/time/DateTimeUtils.java:33 (Settings.Global.put)
- settings: com/my/settings/time/DateTimeUtils.java:37 (Settings.Global.put)
- settings: com/my/settings/activity/WarningActivity.java:36 (Settings.Global.put)
- settings: com/my/settings/activity/WarningActivity.java:37 (Settings.Secure.put)
- settings: com/my/settings/activity/WarningActivity.java:38 (Settings.Secure.put)
- binder: com/my/settings/Utils.java:310 (ServiceManager.getService)
- review: com/my/settings/activity/WarningActivity.java:49 (System.exit)
- review: kotlin/system/ProcessKt.java:8 (System.exit)
- review: kotlin/system/ProcessKt.java:9 (System.exit)
- installer: androidx/profileinstaller/ProfileInstaller.java:50 (INSTALL_SUCCESS)
- installer: androidx/profileinstaller/ProfileInstaller.java:105 (INSTALL_SUCCESS)

## Interpretation and next checks

- First trace actual outgoing/incoming intents, Binder calls, listener lifecycles and system permissions.
- Check launcher fallback and early-boot hooks before considering any app replacement.
- Verify OTA, HDMI selection, focus/ToF, keystone and hardware recovery on real devices.
- Never label method-pattern occurrences as confirmed defects until control flow and triggers are verified.
- No packages were disabled, removed, executed, or modified.

