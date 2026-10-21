# OEM application deep audit — latest 8052 OTA vs factory 8054

Verified factory stock-method hash artifact + latest OTA APK decompilation and AndroidManifest trees.
NO app removed, no signed APK recreated, no OEM code or private data redistributed.

## Replacement and removal risk

| App | Risk and plan | APK same? | JADX method deltas* | Exported components |
|---|---|---|---:|---:|
| Factory | keep_for_recovery_diagnostics | True | 0 | 1 |
| KeystoneCorrection | keep_hardware_core | True | 0 | 6 |
| KuSettings | UI_replacement_only_after_proof | True | 2 | 13 |
| KuSetupWizard | keep_for_first_boot | True | 1 | 3 |
| KuSourceRJ | keep_until_adapter_tested | True | 1 | 37 |
| LiveTV | keep_until_input_regression_test | True | 1 | 39 |
| RuiAutoFocus | keep_hardware_core | False | 10 | 2 |
| RuiYunOta | keep_until_rollback_ready | True | 0 | 2 |
| TvServices | keep_until_tv_regression_test | True | 0 | 30 |
| TvSettingsPlus | privileged_core_until_adapter | True | 1 | 141 |
| trdmiddle | keep_hardware_core | True | 1 | 2 |
| trdservice | keep_hardware_core | True | 0 | 4 |
| zxlauncher | candidate_replacement | False | 6308 | 14 |
| zxstore | candidate_later_disable | False | 1118 | 12 |

**Data-validation note:** when APK/DEX SHA256 is identical, non-zero normalized-method differences are artifacts of JADX extraction, not differences in the original firmware. This applies to KuSettings, KuSetupWizard, KuSourceRJ, LiveTV, TvSettingsPlus and trdmiddle in the table above. The really changed DEX packages in this inventory are RuiAutoFocus, zxlauncher and zxstore.

**Permission/package-data caveat:** Some empty package fields and permission subsets can result from truncation of the legacy aapt badging output; never infer that an Android component has no privileges from an empty value. Exported components also may require permissions.

**Bug review caveat:** Risk indicators are regex sightings across OEM and bundled third-party classes. For example, a catch block heuristic alone does not prove a defect, and Thread.sleep does not prove it occurs on the UI thread.

## App-by-app evidence and required runtime validation

### Factory

- Recommendation: keep_for_recovery_diagnostics; inspect factory test and native I2C.
- Package: mediatek.factorymenu.ui; privileges: [].
- Dynamic libraries: ['com_mediatek_net_jni', 'com_mediatek_twoworlds_tv_jni', 'factoryi2c_jni'].
- Android components: {'activity': 21, 'service': 2}.
- Method digest comparison: {'same': 23304}.
- Code review indicators (not proven bugs): {'exception_swallowed': 354, 'system_process_exit': 8, 'sleep_on_ui_candidate': 9, 'cross_app_intent': 58, 'android_settings_write': 6, 'privileged_property_write': 172, 'raw_i2c_write': 4, 'shell_execution': 4, 'forced_permission_change': 1, 'binder_service_access': 1}.

Selected exported components (not confirmed accessible):

- service mediatek.tvsetting.factory.ui.ApiService

### KeystoneCorrection

- Recommendation: keep_hardware_core; inspect projector trapezoid and display functions.
- Package: com.rjpj.tcorrection; privileges: [].
- Dynamic libraries: ['i2c_jni'].
- Android components: {'activity': 4, 'receiver': 1, 'provider': 1}.
- Method digest comparison: {'same': 5098}.
- Code review indicators (not proven bugs): {'raw_i2c_write': 67, 'privileged_property_write': 9, 'binder_service_access': 18, 'exception_swallowed': 116, 'cross_app_intent': 5}.

Selected exported components (not confirmed accessible):

- activity com.rjpj.tcorrection.FourCornerActivity, actions=rjpj.action.keystone.FOUR_CORNER, android.intent.category.DEFAULT
- activity com.rjpj.tcorrection.DigitalZoomActivity, actions=rjpj.action.keystone.DIGITAL_ZOOM, android.intent.category.DEFAULT
- activity com.rjpj.tcorrection.HVKeystoneActivity, actions=rjpj.action.keystone.HV, android.intent.category.DEFAULT
- activity com.rjpj.tcorrection.MainActivity
- receiver com.rjpj.tcorrection.TCorrectionBroadcastReceiver
- provider androidx.startup.InitializationProvider

### KuSettings

- Recommendation: UI_replacement_only_after_proof; inspect OEM settings, privileged permissions and TRD control.
- Package: None; privileges: [].
- Dynamic libraries: [].
- Android components: {'activity': 11, 'service': 2, 'receiver': 2, 'provider': 1}.
- Method digest comparison: {'same': 47107, 'changed': 2, 'stock_only': 1, 'ota_only': 1}.
- Code review indicators (not proven bugs): {'exception_swallowed': 373, 'cross_app_intent': 38, 'android_settings_write': 10, 'binder_service_access': 5, 'privileged_property_write': 1, 'sleep_on_ui_candidate': 2, 'system_process_exit': 2}.

Selected exported components (not confirmed accessible):

- activity com.my.settings.SettingActivity, actions=android.intent.action.MAIN, android.intent.category.LAUNCHER, android.settings.SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.wifi.MyWifiActivity, actions=android.settings.WIFI_SETTINGS
- activity com.my.settings.bluetooth.MyBluetoothActivity, actions=android.settings.BLUETOOTH_SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.bluetooth.MyAutoBluetoothActivity, actions=android.settings.AUTO_BLUETOOTH, android.intent.category.DEFAULT
- activity com.my.settings.language.LanguageActivity, actions=android.settings.LAUGUAGE_SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.language.LanguageLocalActivity, actions=android.settings.LAUGUAGE_LOCAL_SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.time.DateTimeActivity, actions=android.settings.DATETIME_SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.activity.ScreenshotActivity, actions=android.settings.SCREENSHOT_SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.activity.ProjectionActivity, actions=android.settings.PROJECTABOUT_SETTINGS, android.intent.category.DEFAULT
- activity com.my.settings.activity.AllAppActivity, actions=android.settings.ALLAPPS, android.intent.category.DEFAULT
- receiver com.my.service.BootupReceiver, actions=android.intent.action.BOOT_COMPLETED
- provider androidx.startup.InitializationProvider
- receiver androidx.profileinstaller.ProfileInstallReceiver, permission=android.permission.DUMP, actions=androidx.profileinstaller.action.INSTALL_PROFILE, androidx.profileinstaller.action.SKIP_FILE, androidx.profileinstaller.action.SAVE_PROFILE, androidx.profileinstaller.action.BENCHMARK_OPERATION

### KuSetupWizard

- Recommendation: keep_for_first_boot; inspect first boot and provisioning.
- Package: None; privileges: [].
- Dynamic libraries: [].
- Android components: {'activity': 3, 'provider': 1, 'receiver': 1}.
- Method digest comparison: {'same': 47109, 'changed': 1}.
- Code review indicators (not proven bugs): {'exception_swallowed': 373, 'cross_app_intent': 38, 'android_settings_write': 10, 'binder_service_access': 5, 'privileged_property_write': 1, 'sleep_on_ui_candidate': 2, 'system_process_exit': 2}.

Selected exported components (not confirmed accessible):

- activity com.my.settings.wifi.ProvisionWifiActivity, actions=android.intent.action.MAIN, android.intent.category.HOME, android.intent.category.DEFAULT, android.intent.category.SETUP_WIZARD
- provider androidx.startup.InitializationProvider
- receiver androidx.profileinstaller.ProfileInstallReceiver, permission=android.permission.DUMP, actions=androidx.profileinstaller.action.INSTALL_PROFILE, androidx.profileinstaller.action.SKIP_FILE, androidx.profileinstaller.action.SAVE_PROFILE, androidx.profileinstaller.action.BENCHMARK_OPERATION

### KuSourceRJ

- Recommendation: keep_until_adapter_tested; inspect input source switching and HDMI boot selection.
- Package: None; privileges: ['android.permission.BIND_TV_INPUT', 'android.permission.TV_INPUT_HARDWARE'].
- Dynamic libraries: [].
- Android components: {'activity': 33, 'receiver': 3, 'service': 1, 'provider': 1}.
- Method digest comparison: {'same': 38829, 'ota_only': 1, 'stock_only': 1, 'changed': 1}.
- Code review indicators (not proven bugs): {'android_settings_write': 4, 'shell_execution': 6, 'cross_app_intent': 37, 'privileged_property_write': 8, 'exception_swallowed': 328, 'sleep_on_ui_candidate': 9, 'binder_service_access': 78, 'system_process_exit': 1}.

Selected exported components (not confirmed accessible):

- activity com.coolux.source.MainActivity, actions=android.intent.action.MAIN, android.settings.SOURCE_SETTINGS, android.intent.category.LAUNCHER, android.intent.category.DEFAULT
- activity com.coolux.source.activity.BootSoureActivity, actions=android.settings.BOOTSOURE_SETTINGS, android.intent.category.DEFAULT
- activity com.coolux.source.activity.BrightActivity, actions=android.settings.BRIGHT_SETTINGS, android.intent.category.DEFAULT
- activity com.coolux.source.activity.VoiceActivity, actions=android.settings.VOICE_SETTINGS, android.intent.category.DEFAULT
- activity com.coolux.source.activity.RestoreActivity, actions=android.settings.RESTORE_SETTINGS, android.intent.category.DEFAULT
- activity com.coolux.source.activity.HighTemperatureActivity, actions=android.high.temperature, android.intent.category.DEFAULT
- activity com.coolux.source.activity.FanDetectionActivity, actions=android.fan.detection, android.intent.category.DEFAULT
- activity com.coolux.source.activity.AllAppAutoActivity, actions=android.settings.ALLAPPSAUTO, android.intent.category.DEFAULT
- activity com.coolux.source.activity.AuthorizationActivity, actions=android.auth.Authorization, android.intent.category.DEFAULT
- activity com.coolux.source.activity.DustproofActivity
- receiver com.coolux.source.service.BootupReceiver, actions=android.intent.action.BOOT_COMPLETED
- receiver com.coolux.source.service.ScreensaverReceiver, actions=com.action.screensaver
- receiver com.coolux.source.service.BrightReceiver, actions=com.action.brightReceiver
- activity com.coolux.source.activity.PoweronModeActivity, actions=android.settings.POWERMODE_SETTINGS, android.intent.category.DEFAULT
- activity com.coolux.source.activity.ProjectModelActivity, actions=android.settings.PROJECTMODEL_SETTINGS, android.intent.category.DEFAULT
- activity com.coolux.source.activity.KeystoneActivity, actions=android.settings.KEYSTONE_SETTINGS, android.intent.category.DEFAULT

### LiveTV

- Recommendation: keep_until_input_regression_test; inspect TV input framework and HDMI handling.
- Package: None; privileges: ['android.permission.BIND_TV_INPUT', 'android.permission.TV_INPUT_HARDWARE'].
- Dynamic libraries: ['com_mediatek_twoworlds_tv_jni'].
- Android components: {'activity': 28, 'provider': 2, 'receiver': 5, 'service': 4}.
- Method digest comparison: {'same': 26942, 'changed': 1}.
- Code review indicators (not proven bugs): {'cross_app_intent': 164, 'exception_swallowed': 285, 'sleep_on_ui_candidate': 30, 'binder_service_access': 9, 'shell_execution': 1, 'android_settings_write': 11, 'privileged_property_write': 1}.

Selected exported components (not confirmed accessible):

- activity com.mediatek.wwtv.tvcenter.nav.TurnkeyUiMainActivity, actions=android.intent.action.MAIN, com.android.tv.action.FORCE_LAUNCH_ON_BOOT, android.intent.category.DEFAULT, android.mtk.intent.action.ACTION_REQUEST_TOP_RESUME, android.intent.category.DEFAULT
- provider androidx.startup.InitializationProvider
- activity com.mediatek.wwtv.tvcenter.capturelogo.CaptureLogoActivity
- activity com.mediatek.wwtv.tvcenter.oad.NavOADActivity
- activity com.mediatek.wwtv.tvcenter.oad.NavOADActivityNew
- activity com.mediatek.wwtv.tvcenter.epg.us.EPGUsActivity
- activity com.mediatek.wwtv.tvcenter.epg.eu.EPGEuActivity
- activity com.mediatek.wwtv.tvcenter.epg.eu.EPGEu2ndActivity
- activity com.mediatek.wwtv.tvcenter.epg.sa.EPGSaActivity
- activity com.mediatek.wwtv.tvcenter.epg.sa.EPGSa2ndActivity
- activity com.mediatek.wwtv.tvcenter.epg.cn.EPGCnActivity
- receiver com.mediatek.wwtv.tvcenter.util.BootBroadcastReceiver, actions=android.intent.action.GLOBAL_BUTTON, android.mediatek.intent.logcattousb, android.intent.action.BOOT_COMPLETED, com.mediatek.wwtv.tvcenter.schedule.dvr, com.mediatek.wwtv.tvcenter.soft.keyboard
- receiver com.android.tv.livetv.receiver.GlobalKeyReceiver, actions=android.intent.action.GLOBAL_BUTTON, android.media.tv.action.QUERY_CONTENT_RATING_SYSTEMS
- receiver com.mediatek.wwtv.tvcenter.epg.sa.AlarmReceiver, actions=com.mediatek.wwtv.tvcenter.saepgreceiver
- activity com.mediatek.wwtv.tvcenter.epg.sa.DialogActivity, actions=com.mediatek.wwtv.tvcenter.saepg.activity, android.intent.category.DEFAULT
- activity com.mediatek.wwtv.setting.EditTextActivity

### RuiAutoFocus

- Recommendation: keep_hardware_core; inspect motor, ToF, camera and optical calibration.
- Package: None; privileges: ['android.permission.INJECT_EVENTS'].
- Dynamic libraries: ['com_mediatek_twoworlds_tv_jni', 'focusvahysd', 'ruicameraapi_jni'].
- Android components: {'service': 1, 'activity': 1}.
- Method digest comparison: {'same': 15928, 'changed': 10}.
- Code review indicators (not proven bugs): {'shell_execution': 5, 'exception_swallowed': 342, 'sleep_on_ui_candidate': 21, 'cross_app_intent': 38, 'motor_control': 26, 'privileged_property_write': 167, 'binder_service_access': 76, 'android_settings_write': 1}.

Selected exported components (not confirmed accessible):

- service com.hysd.client.VAF2S
- activity com.hysd.xymscreen.MainActivity, actions=android.intent.action.MAIN, android.intent.category.DEFAULT

Relevant modified method signatures:
- changed: com/hysd/ai/RuiCameraApi.java :: startTof()

### RuiYunOta

- Recommendation: keep_until_rollback_ready; inspect OEM OTA client and update permission chain.
- Package: com.rjpj.yunota; privileges: ['android.permission.INJECT_EVENTS', 'android.permission.MANAGE_ACCOUNTS', 'android.permission.MANAGE_SCOPED_ACCESS_DIRECTORY_PERMISSIONS', 'android.permission.MANAGE_USERS', 'android.permission.REBOOT', 'android.permission.WRITE_SECURE_SETTINGS'].
- Dynamic libraries: [].
- Android components: {'activity': 4, 'service': 2}.
- Method digest comparison: {'same': 184}.
- Code review indicators (not proven bugs): {'cross_app_intent': 6, 'shell_execution': 1, 'system_process_exit': 1}.

Selected exported components (not confirmed accessible):

- activity .OTASystemNetworkUpdateActivity
- activity .OTASystemLocalUpdateActivity

### TvServices

- Recommendation: keep_until_tv_regression_test; inspect Android TV service lifecycle.
- Package: com.mediatek.tv.service; privileges: ['android.permission.INJECT_EVENTS', 'android.permission.MANAGE_USERS', 'android.permission.TV_INPUT_HARDWARE', 'android.permission.WRITE_SECURE_SETTINGS'].
- Dynamic libraries: ['com_mediatek_twoworlds_tv_jni'].
- Android components: {'receiver': 7, 'provider': 4, 'service': 17, 'activity': 2}.
- Method digest comparison: {'same': 5473}.
- Code review indicators (not proven bugs): {'cross_app_intent': 78, 'sleep_on_ui_candidate': 26, 'exception_swallowed': 65, 'binder_service_access': 7, 'android_settings_write': 29, 'shell_execution': 2, 'privileged_property_write': 1}.

Selected exported components (not confirmed accessible):

- receiver com.mediatek.TimeMeasurementAgent.TimeMeasurementAgentActionReceiver, actions=android.intent.action.BOOT_COMPLETED
- receiver com.mediatek.hotkey.dispatcher.GlobalKeyReceiver, actions=android.intent.action.BOOT_COMPLETED, android.intent.action.GLOBAL_BUTTON
- provider com.android.tv.settings.FarFieldMicContentProvider
- provider com.android.tv.settings.HotWordMicContentProvider
- service com.mediatek.hotkey.dispatcher.HotKeyService, permission=android.permission.BIND_TV_INPUT, actions=android.hotkey.dispatcher.HotKeyService
- receiver com.mediatek.tv.agent.BootupReceiver, actions=android.intent.action.BOOT_COMPLETED
- service com.mediatek.tv.agent.BootupReceiver$ReceiverService
- receiver com.mediatek.tv.agent.TimeActionReceiver, actions=android.intent.action.BOOT_COMPLETED
- receiver com.mediatek.tv.agent.MyAgent$DiskBeforeReceiver, actions=android.os.storage.action.DISK_SCANNED, android.os.storage.action.VOLUME_STATE_CHANGED
- service com.mediatek.tv.agent.TimeActionReceiver$ReceiverService
- service com.mediatek.tv.agent.TVRemoteServiceAgent, permission=android.permission.BIND_TV_INPUT, actions=android.media.tv.TvInputService
- activity com.mediatek.tv.agent.TVRemoteServiceAgent$InputServiceSetup, actions=android.intent.action.MAIN
- service com.mediatek.tv.agent.DMRemoteServiceAgent
- service com.mediatek.tv.agent.DolbyVisionService
- service com.mediatek.tv.agent.MonitorActivityService, actions=com.mediatek.MonitorActivityService
- service com.mediatek.tv.agent.AudioCustomizedService

### TvSettingsPlus

- Recommendation: privileged_core_until_adapter; inspect Android-TV system settings, HDMI and I2C JNI.
- Package: None; privileges: ['android.permission.BIND_TV_INPUT', 'android.permission.MANAGE_SENSOR_PRIVACY', 'android.permission.MANAGE_SLICE_PERMISSIONS', 'android.permission.TV_INPUT_HARDWARE'].
- Dynamic libraries: ['com_mediatek_net_jni', 'com_mediatek_twoworlds_tv_jni', 'settingsi2c_jni'].
- Android components: {'provider': 6, 'activity': 114, 'receiver': 12, 'service': 8, 'activity-alias': 6}.
- Method digest comparison: {'same': 73539, 'changed': 1}.
- Code review indicators (not proven bugs): {'exception_swallowed': 803, 'cross_app_intent': 222, 'binder_service_access': 34, 'sleep_on_ui_candidate': 27, 'android_settings_write': 176, 'privileged_property_write': 215, 'raw_i2c_write': 4, 'shell_execution': 1, 'system_process_exit': 1}.

Selected exported components (not confirmed accessible):

- provider androidx.startup.InitializationProvider
- activity com.android.tv.settings.partnercustomizer.timer.TimerActivity, actions=android.settings.DATE_SETTINGS, android.intent.category.DEFAULT
- activity com.android.tv.settings.partnercustomizer.retailmode.RetailModeConfirmActivity
- activity com.android.tv.settings.partnercustomizer.EnergyCommonActivity
- activity com.android.tv.settings.partnercustomizer.sound.AudioResetActivity
- activity com.android.tv.settings.partnercustomizer.picture.PictureResetActivity
- activity com.android.tv.settings.partnercustomizer.inputs.InputsActivity
- activity com.android.tv.settings.partnercustomizer.power.PowerActivity
- activity com.android.tv.settings.partnercustomizer.power.PictureOffActivity
- activity com.android.tv.settings.partnercustomizer.vendor.channels.ChannelsActivity
- activity com.android.tv.settings.partnercustomizer.vendor.channels.DiseqcTypeActivity
- activity com.android.tv.settings.partnercustomizer.vendor.channels.ChannelsTwoPanalActivity
- activity com.android.tv.settings.partnercustomizer.vendor.channels.ChannelConfirmActivity
- activity com.android.tv.settings.partnercustomizer.retailmode.RetailModeActivity
- activity com.android.tv.settings.device.sound.SoundActivity, actions=android.settings.SOUND_SPEAKER_STATUS, android.settings.oem.SOUND_SETTINGS, com.android.tv.action.VIEW_SOUND_SETTINGS, android.intent.category.DEFAULT
- activity com.android.tv.settings.partnercustomizer.picture.PictureActivity, actions=android.settings.DISPLAY_SETTINGS, android.intent.category.DEFAULT

### trdmiddle

- Recommendation: keep_hardware_core; inspect TRD Binder/HIDL ToF and projector middleware.
- Package: com.trd.framework; privileges: [].
- Dynamic libraries: ['com_mediatek_twoworlds_tv_jni', 'tof_jni', 'trd_jni', 'trdmiddle'].
- Android components: {'activity': 1, 'service': 1}.
- Method digest comparison: {'same': 6451, 'changed': 1}.
- Code review indicators (not proven bugs): {'cross_app_intent': 17, 'privileged_property_write': 36, 'sleep_on_ui_candidate': 10, 'shell_execution': 1, 'exception_swallowed': 245, 'forced_permission_change': 2, 'android_settings_write': 11, 'binder_service_access': 12}.

Selected exported components (not confirmed accessible):

- activity com.trd.framework.MainActivity, actions=android.intent.action.MAIN
- service com.trd.framework.TrdSystemService, actions=com.trd.framework.service

Relevant modified method signatures:
- changed: com/trd/framework/tof/TofCtrlService.java :: invokeTofDataListenersOnReceived(int i2, int i3, byte[] bArr)

### trdservice

- Recommendation: keep_hardware_core; inspect motor, key and boot event service.
- Package: com.trd.service; privileges: [].
- Dynamic libraries: ['rjpj_private_function'].
- Android components: {'activity': 1, 'service': 1, 'receiver': 1, 'provider': 1}.
- Method digest comparison: {'same': 4860}.
- Code review indicators (not proven bugs): {'sleep_on_ui_candidate': 7, 'binder_service_access': 24, 'cross_app_intent': 17, 'privileged_property_write': 10, 'android_settings_write': 2, 'motor_control': 9, 'shell_execution': 1, 'exception_swallowed': 80}.

Selected exported components (not confirmed accessible):

- activity com.trd.service.MainActivity, actions=android.intent.action.MAIN
- service com.trd.service.TrdService, actions=com.trd.service.service
- receiver com.trd.service.system.shutdown.PreShutdownReceiver, actions=com.android.server.power.ACTION_PRE_SHUTDOWN
- provider androidx.startup.InitializationProvider

### zxlauncher

- Recommendation: candidate_replacement; inspect HOME role, key routing, boot startup, callbacks, TV/source actions.
- Package: None; privileges: [].
- Dynamic libraries: ['mmkv'].
- Android components: {'activity': 19, 'provider': 2, 'service': 4, 'receiver': 4}.
- Method digest comparison: {'ota_only': 22180, 'same': 71961, 'stock_only': 24802, 'changed': 6308}.
- Code review indicators (not proven bugs): {'exception_swallowed': 981, 'cross_app_intent': 134, 'sleep_on_ui_candidate': 15, 'shell_execution': 20, 'system_process_exit': 5, 'forced_permission_change': 2, 'android_settings_write': 2, 'binder_service_access': 21}.

Selected exported components (not confirmed accessible):

- provider androidx.core.content.FileProvider
- service com.zeasn.ad.connector.access.ABService, permission=android.permission.BIND_ACCESSIBILITY_SERVICE, actions=android.accessibilityservice.AccessibilityService
- receiver com.zeasn.installer.UninstallReceiverFor28, actions=android.content.pm.extra.STATUS
- receiver com.zeasn.installer.InstallReceiverFor28, actions=android.content.pm.extra.STATUS
- activity com.zeasn.weatherplugin.ui.WeeklyActivity, actions=cn.zeasn.general.services.OPEN_WEEKLY
- activity com.zeasn.weatherplugin.ui.SearchActivity, actions=cn.zeasn.general.services.OPEN_SEARCH
- activity com.zeasn.weatherplugin.ui.TouchWeeklyActivity, actions=cn.zeasn.general.services.OPEN_TOUCH_SEARCH
- activity com.zeasn.weatherplugin.ui.TouchSearchActivity, actions=cn.zeasn.general.services.OPEN_TOUCH_SEARCH
- activity com.zeasn.weatherplugin.ui.WhaleSearchActivity, actions=cn.zeasn.general.services.OPEN_SEARCH_WHALE
- activity com.zeasn.weatherplugin.ui.WhaleSearchNewActivity, actions=cn.zeasn.general.services.OPEN_SEARCH_WHALE
- activity com.zeasn.weatherplugin.ui.WhaleSearchTouchActivity, actions=cn.zeasn.general.services.OPEN_TOUCH_SEARCH_WHALE
- activity com.zeasn.plugin.StubActivity
- activity com.google.android.gms.common.api.GoogleApiActivity
- provider androidx.lifecycle.ProcessLifecycleOwnerInitializer

Relevant modified method signatures:
- stock_only: android/support/customtabs/ICustomTabsService.java :: Proxy(android.os.IBinder iBinder)
- ota_only: android/support/customtabs/ICustomTabsService.java :: Proxy(android.os.IBinder remote)
- stock_only: android/support/customtabs/ICustomTabsService.java :: asInterface(android.os.IBinder iBinder)
- ota_only: android/support/customtabs/ICustomTabsService.java :: asInterface(android.os.IBinder obj)
- ota_only: android/support/customtabs/ICustomTabsService.java :: extraCommand(java.lang.String commandName, android.os.Bundle args)
- stock_only: android/support/customtabs/ICustomTabsService.java :: extraCommand(java.lang.String str, android.os.Bundle bundle)
- ota_only: android/support/customtabs/ICustomTabsService.java :: mayLaunchUrl(android.support.customtabs.ICustomTabsCallback callback, android.net.Uri url, android.os.Bundle extras, java.util.List<android.os.Bundle> otherLikelyB)
- stock_only: android/support/customtabs/ICustomTabsService.java :: mayLaunchUrl(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback, android.net.Uri uri, android.os.Bundle bundle, java.util.List<android.os.Bundle> l)
- ota_only: android/support/customtabs/ICustomTabsService.java :: newSession(android.support.customtabs.ICustomTabsCallback callback)
- stock_only: android/support/customtabs/ICustomTabsService.java :: newSession(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback)
- ota_only: android/support/customtabs/ICustomTabsService.java :: newSessionWithExtras(android.support.customtabs.ICustomTabsCallback callback, android.os.Bundle extras)
- stock_only: android/support/customtabs/ICustomTabsService.java :: newSessionWithExtras(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback, android.os.Bundle bundle)
- ota_only: android/support/customtabs/ICustomTabsService.java :: postMessage(android.support.customtabs.ICustomTabsCallback callback, java.lang.String message, android.os.Bundle extras)
- stock_only: android/support/customtabs/ICustomTabsService.java :: postMessage(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback, java.lang.String str, android.os.Bundle bundle)
- ota_only: android/support/customtabs/ICustomTabsService.java :: receiveFile(android.support.customtabs.ICustomTabsCallback callback, android.net.Uri uri, int purpose, android.os.Bundle extras)
- stock_only: android/support/customtabs/ICustomTabsService.java :: receiveFile(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback, android.net.Uri uri, int i, android.os.Bundle bundle)
- ota_only: android/support/customtabs/ICustomTabsService.java :: requestPostMessageChannel(android.support.customtabs.ICustomTabsCallback callback, android.net.Uri postMessageOrigin)
- stock_only: android/support/customtabs/ICustomTabsService.java :: requestPostMessageChannel(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback, android.net.Uri uri)
- ota_only: android/support/customtabs/ICustomTabsService.java :: requestPostMessageChannelWithExtras(android.support.customtabs.ICustomTabsCallback callback, android.net.Uri postMessageOrigin, android.os.Bundle extras)
- stock_only: android/support/customtabs/ICustomTabsService.java :: requestPostMessageChannelWithExtras(android.support.customtabs.ICustomTabsCallback iCustomTabsCallback, android.net.Uri uri, android.os.Bundle bundle)

### zxstore

- Recommendation: candidate_later_disable; inspect APK install/update dependencies, intents, package events, download provider.
- Package: None; privileges: [].
- Dynamic libraries: ['mmkv'].
- Android components: {'activity': 13, 'provider': 3, 'receiver': 5, 'service': 4}.
- Method digest comparison: {'same': 99786, 'changed': 1118, 'stock_only': 3929, 'ota_only': 865}.
- Code review indicators (not proven bugs): {'exception_swallowed': 1172, 'cross_app_intent': 106, 'shell_execution': 20, 'system_process_exit': 5, 'forced_permission_change': 2, 'sleep_on_ui_candidate': 13, 'binder_service_access': 20, 'android_settings_write': 3}.

Selected exported components (not confirmed accessible):

- activity zeasn.open.technical.tv.store.ui.SearchActivity
- activity zeasn.open.technical.tv.store.ui.SettingTouActivity
- activity zeasn.open.technical.tv.store.ui.AppDetailActivity, actions=android.intent.action.VIEW, android.intent.category.DEFAULT, android.intent.category.BROWSABLE, android.intent.action.VIEW, android.intent.category.DEFAULT
- provider androidx.core.content.FileProvider
- service zeasn.open.technical.tv.store.app.StoreService
- receiver com.zeasn.installer.UninstallReceiverFor28, actions=android.content.pm.extra.STATUS
- receiver com.zeasn.installer.InstallReceiverFor28, actions=android.content.pm.extra.STATUS
- receiver com.zeasn.installer.InstallReceiverForXpak, actions=android.content.pm.extra.STATUS
- activity com.zeasn.plugin.StubActivity
- provider com.squareup.picasso.PicassoProvider
- activity com.google.android.gms.common.api.GoogleApiActivity
- provider androidx.lifecycle.ProcessLifecycleOwnerInitializer

Relevant modified method signatures:
- changed: androidx/appcompat/widget/DropDownListView.java :: measureHeightOfChildrenCompat(int i, int i2, int i3, int i4, int i5)
- changed: androidx/core/app/JobIntentService.java :: serviceProcessingStarted()
- changed: androidx/core/graphics/TypefaceCompat.java :: createFromResourcesFamilyXml(android.content.Context context, androidx.core.content.res.FontResourcesParserCompat.FamilyResourceEntry familyResourceEntry, android.content.res.Reso)
- changed: androidx/core/view/ViewCompat.java :: getAvailableActionIdFromResources(android.view.View view, java.lang.CharSequence charSequence)
- changed: androidx/core/widget/NestedScrollView.java :: findFocusableViewInBounds(boolean z, int i, int i2)
- changed: androidx/fragment/app/FragmentTransition.java :: addToFirstInLastOut(androidx.fragment.app.BackStackRecord backStackRecord, androidx.fragment.app.FragmentTransaction.Op op, android.util.SparseArray<androidx.fragment.app)
- changed: androidx/leanback/media/MediaPlayerGlue.java :: onKey(android.view.View view, int i, android.view.KeyEvent keyEvent)
- changed: androidx/leanback/media/PlaybackControlGlue.java :: dispatchAction(androidx.leanback.widget.Action action, android.view.KeyEvent keyEvent)
- changed: androidx/leanback/widget/DetailsOverviewRowPresenter.java :: bindImageDrawable(androidx.leanback.widget.DetailsOverviewRowPresenter.ViewHolder viewHolder)
- ota_only: androidx/leanback/widget/GuidedActionAdapterGroup.java :: focusToNextAction(androidx.leanback.widget.GuidedActionAdapter r7, androidx.leanback.widget.GuidedAction r8, long r9)
- stock_only: androidx/leanback/widget/GuidedActionAdapterGroup.java :: focusToNextAction(androidx.leanback.widget.GuidedActionAdapter r8, androidx.leanback.widget.GuidedAction r9, long r10)
- changed: androidx/vectordrawable/graphics/drawable/AnimatorInflaterCompat.java :: dumpKeyframes(java.lang.Object[] objArr, java.lang.String str)
- changed: androidx/vectordrawable/graphics/drawable/PathInterpolatorCompat.java :: initPath(android.graphics.Path path)
- changed: com/airbnb/lottie/parser/KeyframeParser.java :: parseKeyframe(com.airbnb.lottie.LottieComposition lottieComposition, com.airbnb.lottie.parser.moshi.JsonReader jsonReader, float f, com.airbnb.lottie.parser.ValuePa)
- changed: com/airbnb/lottie/parser/moshi/JsonUtf8Reader.java :: peekKeyword()
- changed: com/alibaba/fastjson/util/TypeUtils.java :: castToFloat(java.lang.Object obj)
- changed: com/android/media/api/service_api/ServiceADManager.java :: getAppSilentApi()
- changed: com/android/media/api/service_api/ServiceADManager.java :: handleMessage(android.os.Message message)
- changed: com/android/media/api/service_api/ServiceADManager.java :: startADService()
- changed: com/android/media/api/service_api/receiver/AdConnectReceiver.java :: isSameDay(long j, long j2, java.util.TimeZone timeZone)

## Critical uninstall/replacement test gates

- Replace the stock launcher only after HOME selection, reboot, remote inputs, suspend/resume and HDMI return are tested.
- Do not remove proprietary TRD/ToF/motor/keystone/TV input services until a tested replacement exists.
- OEM store is only a candidate for disable; verify any installed-package callback, provider authority and firmware-linked download activity.
- Replace settings UI behind a verified adapter that preserves Binder, system permissions and essential JNI paths.
- Keep OEM OTA service and wizard until update/recovery and first-boot behavior are tested.
- Do not report code-heuristic indicators as confirmed defects without manual control-flow review and reproduced behavior.
- Watch both 8052 and 8054 test results; the same Java APK can act differently due to native HAL and build.prop.

