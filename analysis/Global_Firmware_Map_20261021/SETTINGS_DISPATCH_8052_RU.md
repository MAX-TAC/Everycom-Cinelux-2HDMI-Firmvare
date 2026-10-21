# TvSettingsPlus versus KuSettings versus Zeasn launcher: where Settings opens

Source: Oct 8052.1.0.4 verified OTA. Important: TvSettingsPlus, KuSettings, trdservice APKs are **byte-identical** to the only available Sep stock 8054.1.0.1. That does not guarantee same runtime components or settings launch policy.

## APK certificates, package and exported activity candidates

| App | Package | Cert SHA256 | Entry candidates |
|---|---|---|---:|
| TvSettingsPlus | com.android.tv.settings | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 88 |
| KuSettings | com.my.settings | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 10 |
| trdservice | com.trd.service | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 1 |
| zxlauncher | com.zeasn.whale.saas | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 2 |
| RuiAutoFocus | com.hysd.screen | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 1 |
| KuSetupWizard | com.android.provision | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 1 |
| KeystoneCorrection | com.rjpj.tcorrection | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 4 |
| KuSourceRJ | com.coolux.source | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 33 |
| RuiYunOta | com.rjpj.yunota | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 2 |
| SystemUI | com.android.systemui | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 23 |
| SettingsProvider | com.android.providers.settings | c8a2e9bccf597c2fb6dc66bee293fc13f2fc47ec77bc6b2b0d52c11f51192ab8 | 0 |

## TvSettingsPlus declared activity entrypoints

- com.android.tv.settings.partnercustomizer.timer.TimerActivity, exported=True, actions=['android.settings.DATE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.partnercustomizer.EnergyCommonActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.partnercustomizer.power.PowerActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.partnercustomizer.vendor.channels.ChannelsActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.partnercustomizer.vendor.channels.DiseqcTypeActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.partnercustomizer.vendor.channels.ChannelConfirmActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.device.sound.SoundActivity, exported=True, actions=['android.settings.SOUND_SPEAKER_STATUS', 'android.settings.oem.SOUND_SETTINGS', 'com.android.tv.action.VIEW_SOUND_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.partnercustomizer.picture.PictureActivity, exported=True, actions=['android.settings.DISPLAY_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.partnercustomizer.picture.DisplayModeActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.device.sound.AudioOutputActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.partnercustomizer.vendor.ResetActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.partnercustomizer.timer.TimerSetActivity, exported=True, actions=['android.settings.CAPTIONING_SETTINGS'], categories=[]
- com.android.tv.settings.partnercustomizer.DisplayAndSoundActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.uicustom.MainActivity, exported=True, actions=['android.settings.RJ_SETTINGS', 'android.settings.PICTURE_SETTINGS', 'android.settings.SOUND_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.uicustom.fragment.projector.KeystoneCalibrationActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.MainSettings, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.LEANBACK_SETTINGS', 'android.intent.category.LEANBACK_LAUNCHER']
- com.android.tv.settings.connectivity.setup.WifiSetupActivity, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.connectivity.NetworkRequestDialogActivity, exported=True, actions=['com.android.settings.wifi.action.NETWORK_REQUEST'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.connectivity.WifiConnectionActivity, exported=True, actions=['com.android.settings.wifi.action.WIFI_CONNECTION_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.connectivity.EditProxySettingsActivity, exported=True, actions=['com.android.settings.wifi.action.EDIT_PROXY_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.connectivity.EditIpSettingsActivity, exported=True, actions=['com.android.settings.wifi.action.EDIT_IP_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.connectivity.AddWifiNetworkActivity, exported=True, actions=['com.android.settings.wifi.action.ADD_WIFI_NETWORK'], categories=['android.intent.category.DEFAULT']
- com.google.android.tv.settings.AccountActivity, exported=True, actions=['android.settings.USER_SETTINGS', 'android.intent.action.MAIN', 'android.settings.ACCOUNT_SYNC_SETTINGS', 'android.settings.SYNC_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.accounts.AccountSyncActivity, exported=True, actions=[], categories=[]
- com.google.android.tv.settings.ManageUserServicesActivity, exported=True, actions=['android.settings.MANAGE_USER_SERVICES_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.accounts.RemoveAccountDialog, exported=True, actions=[], categories=[]
- com.android.tv.settings.accounts.AddAccountWithTypeActivity, exported=True, actions=['android.settings.ADD_ACCOUNT_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.AppsActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.APPLICATION_SETTINGS', 'android.settings.MANAGE_APPLICATIONS_SETTINGS'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.android.tv.settings.device.apps.AllAppsActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.APPLICATION_SETTINGS', 'android.settings.MANAGE_ALL_APPLICATIONS_SETTINGS'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.android.tv.settings.device.apps.specialaccess.AllFilesAccessActivity, exported=True, actions=['android.settings.MANAGE_APP_ALL_FILES_ACCESS_PERMISSION'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.specialaccess.AppUsageAccessActivity, exported=True, actions=['android.settings.USAGE_ACCESS_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.specialaccess.PictureInPictureActivity, exported=True, actions=['android.settings.PICTURE_IN_PICTURE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.specialaccess.SystemAlertActivity, exported=True, actions=['android.settings.action.MANAGE_OVERLAY_PERMISSION'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.specialaccess.AlarmsAndRemindersActivity, exported=True, actions=['android.settings.REQUEST_SCHEDULE_EXACT_ALARM'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.AppManagementActivity, exported=True, actions=['android.intent.action.AUTO_REVOKE_PERMISSIONS', 'android.settings.APPLICATION_DETAILS_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.StorageResetActivity, exported=True, actions=['android.settings.INTERNAL_STORAGE_SETTINGS', 'android.settings.MEMORY_CARD_SETTINGS', 'android.intent.action.MAIN', 'android.intent.action.MANAGE_PACKAGE_STORAGE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.connectivity.NetworkActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.LOCATION_SCANNING_SETTINGS', 'android.settings.DATA_SAVER_SETTINGS', 'android.settings.DATA_ALERT_SETTINGS'], categories=['android.intent.category.LEANBACK_SETTINGS', 'android.intent.category.DEFAULT']
- com.android.tv.settings.oemlink.NetworkSettingsActivity, exported=True, actions=['android.settings.NETWORK_SETTINGS_TV_OEM_LINK'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.SecurityActivity, exported=True, actions=['android.settings.SECURITY_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.users.RestrictedProfileActivityLauncherEntry, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.LEANBACK_SETTINGS']
- com.android.tv.settings.device.displaysound.DisplaySoundActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.panel.action.VOLUME'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.google.android.tv.settings.AmbientActivity, exported=True, actions=[], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.display.daydream.DaydreamActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.device.display.daydream.DaydreamVoiceAction, exported=True, actions=['com.google.android.pano.action.SLEEP'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.CaptionSetupActivity, exported=True, actions=['android.settings.CAPTIONING_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.oemlink.AccessibilityCaptionActivity, exported=True, actions=['android.settings.ACCESSIBILITY_CAPTION_TV_OEM_LINK'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.DateTimeActivity, exported=True, actions=['android.settings.DATE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.LocationActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.LOCATION_SOURCE_SETTINGS'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.android.tv.settings.system.TextToSpeechActivity, exported=True, actions=['android.settings.TTS_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.development.DevelopmentActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.APPLICATION_DEVELOPMENT_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.inputmethod.KeyboardActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.INPUT_METHOD_SETTINGS'], categories=['android.intent.category.VOICE_LAUNCH', 'android.intent.category.DEFAULT']
- com.android.tv.settings.autofill.AutofillPickerTrampolineActivity, exported=True, actions=['android.settings.REQUEST_SET_AUTOFILL_SERVICE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.AppLanguageActivity, exported=True, actions=['android.settings.APP_LOCALE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.LanguageActivity, exported=True, actions=['android.settings.LOCALE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.InputsActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.accessories.BluetoothAccessoryActivity, exported=True, actions=[], categories=[]
- com.android.tv.settings.accessories.AddAccessoryActivity, exported=True, actions=['com.google.android.intent.action.CONNECT_INPUT'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.accessories.BluetoothPairingDialog, exported=True, actions=['android.bluetooth.device.action.PAIRING_REQUEST'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.accessories.BluetoothDevicePickerActivity, exported=True, actions=['android.bluetooth.devicepicker.action.LAUNCH'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.about.AboutActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.DEVICE_INFO_SETTINGS'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.android.tv.settings.about.StatusActivity, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.android.tv.settings.about.LicenseActivity, exported=True, actions=['android.settings.LICENSE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.name.DeviceNameSettingsActivity, exported=True, actions=['android.settings.DEVICE_NAME'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.name.DeviceNameSuggestionActivity, exported=True, actions=['android.intent.action.MAIN'], categories=[]
- com.android.tv.settings.name.setup.DeviceNameFlowStartActivity, exported=True, actions=['android.settings.START_DEVICE_NAME_FLOW'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.storage.NewStorageActivity, exported=False, actions=['com.android.tv.settings.action.NEW_STORAGE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.storage.UnmountActivity, exported=False, actions=['com.android.tv.settings.action.UNMOUNT_STORAGE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.storage.FormatActivity, exported=False, actions=[], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.storage.MigrateStorageActivity, exported=False, actions=['com.android.tv.settings.action.MIGRATE_STORAGE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.MoveAppActivity, exported=False, actions=['com.android.tv.settings.action.MOVE_APP'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.accessories.BluetoothRequestPermissionActivity, exported=True, actions=['android.bluetooth.adapter.action.REQUEST_DISCOVERABLE', 'android.bluetooth.adapter.action.REQUEST_ENABLE'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.system.FallbackHome, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.HOME', 'android.intent.category.DEFAULT']
- com.android.tv.settings.inputmethod.InputMethodAndSubtypeEnablerActivity, exported=True, actions=['android.settings.INPUT_METHOD_SUBTYPE_SETTINGS', 'android.intent.action.MAIN'], categories=['android.intent.category.DEFAULT', 'android.intent.category.VOICE_LAUNCH']
- com.android.tv.settings.device.apps.specialaccess.ExternalSourcesActivity, exported=True, actions=['android.settings.MANAGE_UNKNOWN_APP_SOURCES'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.privacy.NotificationAccessActivity, exported=True, actions=['android.settings.ACTION_NOTIFICATION_LISTENER_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.privacy.SensorToggleActivity, exported=True, actions=['android.settings.MANAGE_MICROPHONE_PRIVACY', 'android.settings.MANAGE_CAMERA_PRIVACY'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.EmptyStubActivity, exported=True, actions=['android.settings.WEBVIEW_SETTINGS', 'android.settings.IGNORE_BATTERY_OPTIMIZATION_SETTINGS', 'android.settings.REQUEST_IGNORE_BATTERY_OPTIMIZATIONS', 'android.settings.IGNORE_BACKGROUND_DATA_RESTRICTIONS_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.deviceadmin.ProfileOwnerAdd, exported=True, actions=['android.app.action.SET_PROFILE_OWNER'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.ActionDisabledByAdminDialog, exported=True, actions=['android.settings.SHOW_ADMIN_SUPPORT_DETAILS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.deviceadmin.DeviceAdminAdd, exported=True, actions=['android.app.action.ADD_DEVICE_ADMIN'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.slice.SliceActivity, exported=True, actions=['android.settings.SLICE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.oemlink.AccessibilitySettingsActivity, exported=True, actions=['android.settings.ACCESSIBILITY_TV_OEM_LINK', 'android.settings.ACCESSIBILITY_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.oemlink.AccessibilityServiceActivity, exported=True, actions=['android.settings.ACCESSIBILITY_SHORTCUT_SERVICES_TV_OEM_LINK'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.oemlink.FactoryResetActivity, exported=True, actions=['android.settings.FACTORY_RESET_TV_OEM_LINK', 'android.intent.action.FACTORY_RESET'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.vendor.VendorActivity, exported=True, actions=[], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.RemoteBugreportActivity, exported=True, actions=['android.settings.SHOW_REMOTE_BUGREPORT_DIALOG'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.enterprise.EnterprisePrivacySettingsActivity, exported=True, actions=['android.settings.ENTERPRISE_PRIVACY_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.android.tv.settings.device.apps.ConfirmationActivity, exported=True, actions=['android.settings.ui.CONFIRM'], categories=['android.intent.category.DEFAULT']

## KuSettings declared activity entrypoints

- com.my.settings.SettingActivity, exported=True, actions=['android.intent.action.MAIN', 'android.settings.SETTINGS'], categories=['android.intent.category.LAUNCHER', 'android.intent.category.DEFAULT']
- com.my.settings.wifi.MyWifiActivity, exported=True, actions=['android.settings.WIFI_SETTINGS'], categories=['android.intent.category.DEFAULT', 'android.intent.category.LEANBACK_SETTINGS']
- com.my.settings.bluetooth.MyBluetoothActivity, exported=True, actions=['android.settings.BLUETOOTH_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.my.settings.bluetooth.MyAutoBluetoothActivity, exported=True, actions=['android.settings.AUTO_BLUETOOTH'], categories=['android.intent.category.DEFAULT']
- com.my.settings.language.LanguageActivity, exported=True, actions=['android.settings.LAUGUAGE_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.my.settings.language.LanguageLocalActivity, exported=True, actions=['android.settings.LAUGUAGE_LOCAL_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.my.settings.time.DateTimeActivity, exported=True, actions=['android.settings.DATETIME_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.my.settings.activity.ScreenshotActivity, exported=True, actions=['android.settings.SCREENSHOT_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.my.settings.activity.ProjectionActivity, exported=True, actions=['android.settings.PROJECTABOUT_SETTINGS'], categories=['android.intent.category.DEFAULT']
- com.my.settings.activity.AllAppActivity, exported=True, actions=['android.settings.ALLAPPS'], categories=['android.intent.category.DEFAULT']

## trdservice declared activity entrypoints

- com.trd.service.MainActivity, exported=True, actions=['android.intent.action.MAIN'], categories=[]

## zxlauncher declared activity entrypoints

- com.zeasn.launcher.ui.MainActivity, exported=None, actions=['android.intent.action.MAIN'], categories=['android.intent.category.HOME', 'android.intent.category.DEFAULT', 'android.intent.category.LAUNCHER', 'android.intent.category.LEANBACK_LAUNCHER']
- com.zeasn.plugin.StubActivity, exported=True, actions=[], categories=[]

## RuiAutoFocus declared activity entrypoints

- com.hysd.xymscreen.MainActivity, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.DEFAULT']

## KuSetupWizard declared activity entrypoints

- com.my.settings.wifi.ProvisionWifiActivity, exported=True, actions=['android.intent.action.MAIN'], categories=['android.intent.category.HOME', 'android.intent.category.DEFAULT', 'android.intent.category.SETUP_WIZARD']

## TvSettingsPlus key code / settings dispatch evidence

### com/android/tv/settings/MainSettings.java

- line 1: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings
- line 4: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.TvSettingsActivity
- line 5: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.TvSettingsActivity
- line 10: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.TvSettingsActivity
- line 12: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.MainFragment.class.getName, com.android.tv.settings.overlay.FlavorUtils.getFeatureFactory
### com/android/tv/settings/uicustom/MainActivity.java

- line 1: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom
- line 4: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.app.Activity, com.android.tv.settings.uicustom.fragment.BaseFragment.OnFragmentInteractionListener
- line 40: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 41: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 42: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 43: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 44: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 45: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 46: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 47: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 48: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.manager.PageManager
- line 50: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusResponsiveLayout
- line 55: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.util.DebounceHelper
- line 56: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.content.BroadcastReceiver, com.android.tv.settings.uicustom.MainActivity.1
- line 61: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.SYSTEM_DIALOG_REASON_KEY
- line 66: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.SYSTEM_DIALOG_REASON_HOME_KEY
- line 69: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.SYSTEM_DIALOG_REASON_RECENT_APPS
- line 75: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.this.finish
- line 81: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.this.hideMainContainer
- line 85: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.os.CountDownTimer, com.android.tv.settings.uicustom.MainActivity.2
- line 92: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.this.finish
- line 113: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.layout.activity_main
- line 140: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.manager.PageManager
- line 159: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.anim.slide_in_left, com.android.tv.settings.R.anim.slide_out_left
- line 176: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.android.tv.settings.R.id.main_container
- line 177: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.view_menu_bar, com.android.tv.settings.uicustom.view.FocusResponsiveLayout
- line 178: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.widget.FrameLayout, com.android.tv.settings.R.id.content_container
- line 179: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_projector, com.android.tv.settings.uicustom.view.FocusItemView
- line 180: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_wifi, com.android.tv.settings.uicustom.view.FocusItemView
- line 181: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_bluetooth, com.android.tv.settings.uicustom.view.FocusItemView
- line 182: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_source, com.android.tv.settings.uicustom.view.FocusItemView
- line 183: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_picture, com.android.tv.settings.uicustom.view.FocusItemView
- line 184: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_sound, com.android.tv.settings.uicustom.view.FocusItemView
- line 185: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_general, com.android.tv.settings.uicustom.view.FocusItemView
- line 186: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.item_system, com.android.tv.settings.uicustom.view.FocusItemView
- line 189: android.settings.SETTINGS; dispatch APIs nearby: ; symbols: android.settings.SETTINGS
- line 235: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.content_container, com.android.tv.settings.uicustom.manager.PageManager
- line 249: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.FocusItemView
- line 250: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.View.OnFocusChangeListener, com.android.tv.settings.uicustom.MainActivity
- line 322: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 336: com.android.tv.settings; dispatch APIs nearby: onKeyDown; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 351: com.android.tv.settings; dispatch APIs nearby: onKeyDown; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment.OnFragmentInteractionListener
- line 428: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment.OnFragmentInteractionListener
- line 433: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment.OnFragmentInteractionListener
- line 439: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 440: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.manager.PageManager
- line 449: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.animation.Animation, android.view.animation.AnimationUtils.loadAnimation, com.android.tv.settings.R.anim.slide_out_left
- line 451: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.animation.Animation.AnimationListener, com.android.tv.settings.uicustom.MainActivity.3
- line 462: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.this.main_container.setVisibility
- line 463: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.MainActivity.this.onDestroy
### com/android/tv/settings/uicustom/fragment/general/GeneralFragment.java

- line 1: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.general
- line 4: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 6: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleContentIconView
- line 7: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleContentIconView
- line 8: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleContentIconView
- line 9: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleContentIconView
- line 10: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleContentIconView
- line 11: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleSwitchView
- line 18: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_font_size_small
- line 21: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_font_size_medium
- line 24: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_font_size_large
- line 26: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_font_size_medium, com.android.tv.settings.R.string.general_font_size_xlarge
- line 31: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_projection_brightness_mode_eco
- line 34: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_projection_brightness_mode_standard
- line 37: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_projection_brightness_mode_highlight
- line 39: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.general_projection_brightness_mode_auto, com.android.tv.settings.R.string.general_projection_brightness_mode_standard
- line 42: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 44: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.layout.fragment_general
- line 47: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 51: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 53: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.util.MtkUtil.getInstance
- line 56: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.util.MtkUtil.getInstance
- line 59: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 61: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.tciv_general_language_settings, com.android.tv.settings.uicustom.view.TitleContentIconView
- line 62: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.tciv_general_date_time, com.android.tv.settings.uicustom.view.TitleContentIconView
- line 63: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.tciv_general_font_size, com.android.tv.settings.uicustom.view.TitleContentIconView
- line 64: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.tciv_general_screensaver_settings, com.android.tv.settings.uicustom.view.TitleContentIconView
- line 65: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.tciv_general_projection_brightness_mode, com.android.tv.settings.uicustom.view.TitleContentIconView
- line 66: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.id.tsv_general_power_on_up, com.android.tv.settings.uicustom.view.TitleSwitchView
- line 76: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.View.OnClickListener, com.android.tv.settings.uicustom.fragment.general.GeneralFragment.1
- line 81: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.sendEventToActivity
- line 84: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.View.OnClickListener, com.android.tv.settings.uicustom.fragment.general.GeneralFragment.2
- line 89: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.sendEventToActivity
- line 92: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.View.OnClickListener, com.android.tv.settings.uicustom.fragment.general.GeneralFragment.3
- line 97: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.sendEventToActivity
- line 100: com.android.tv.settings; dispatch APIs nearby: ; symbols: android.view.View.OnClickListener, com.android.tv.settings.uicustom.fragment.general.GeneralFragment.4
- line 105: com.android.tv.settings; dispatch APIs nearby: setComponent; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.sendEventToActivity
- line 108: com.android.tv.settings; dispatch APIs nearby: setComponent, startActivity; symbols: android.view.View.OnClickListener, com.android.tv.settings.uicustom.fragment.general.GeneralFragment.5
- line 115: com.android.tv.settings; dispatch APIs nearby: setComponent, startActivity; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment, com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this
- line 120: com.android.tv.settings; dispatch APIs nearby: setComponent, startActivity; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.sendEventToActivity
- line 123: com.android.tv.settings; dispatch APIs nearby: startActivity; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.6, com.android.tv.settings.uicustom.view.TitleSwitchView.onTitleSwitchListener
- line 124: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.view.TitleSwitchView.onTitleSwitchListener
- line 126: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.isEnablePowerOnUp
- line 127: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.general.GeneralFragment.this.isEnablePowerOnUp, com.android.tv.settings.uicustom.util.MtkUtil.getInstance
- line 132: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 144: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.util.MtkUtil.getInstance
- line 149: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment
- line 151: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.R.string.system_language
- line 154: com.android.tv.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings.uicustom.fragment.BaseFragment

## KuSettings key code / settings dispatch evidence

### com/my/settings/SettingActivity.java

- line 1: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings
- line 4: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.BaseActivity
- line 27: com.my.settings; dispatch APIs nearby: ; symbols: android.view.View.OnClickListener, com.my.settings.SettingActivity.1
- line 30: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.SettingActivity.this.enterClick
- line 33: com.my.settings; dispatch APIs nearby: ; symbols: android.content.BroadcastReceiver, com.my.settings.SettingActivity.2
- line 38: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.SettingActivity.this.viewIsUpdataOta
- line 46: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.layout.activity_set
- line 80: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.wifi_layout
- line 81: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.bluetooth_layout
- line 82: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.remote_control_layout
- line 83: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.general_time_layout
- line 84: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.language_method_layout
- line 85: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.screens_hot_layout
- line 86: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.projection_about_layout
- line 87: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.bright_layout
- line 88: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.voice_layout
- line 89: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.RelativeLayout, com.my.settings.R.id.online_upgrade_layout
- line 90: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.restore_layout
- line 91: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.boot_source_layout
- line 92: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.poweron_mode_layout
- line 93: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.model_project_layout
- line 94: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.mircast_layout
- line 95: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.airplay_layout
- line 96: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.keystone_layout
- line 97: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.LinearLayout, com.my.settings.R.id.image_digital_layout
- line 98: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.ImageView, com.my.settings.R.id.is_ota_image
- line 99: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.TextView, com.my.settings.R.id.set_version
- line 143: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.wifi_layout
- line 147: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.bluetooth_layout
- line 151: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.remote_control_layout
- line 155: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.general_time_layout
- line 159: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.language_method_layout
- line 163: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.screens_hot_layout
- line 167: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.projection_about_layout
- line 171: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.bright_layout
- line 175: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.voice_layout
- line 179: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.online_upgrade_layout
- line 185: com.my.settings; dispatch APIs nearby: ; symbols: android.widget.Toast.makeText, com.my.settings.R.string.not_network
- line 192: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.restore_layout
- line 196: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.boot_source_layout
- line 200: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.poweron_mode_layout
- line 204: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.model_project_layout
- line 208: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.mircast_layout
- line 212: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.airplay_layout
- line 214: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.keystone_layout
- line 216: com.my.settings; dispatch APIs nearby: ; symbols: com.my.settings.R.id.image_digital_layout
### com/my/utils/IntentUtils.java

- line 18: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.content.Intent, com.my.settings.wifi.MyWifiActivity.class
- line 23: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.content.Intent, com.my.settings.bluetooth.MyBluetoothActivity.class
- line 40: com.my.settings; dispatch APIs nearby: ; symbols: android.content.Intent, com.my.settings.language.LanguageLocalActivity.class
- line 45: com.my.settings; dispatch APIs nearby: ; symbols: android.content.Intent, com.my.settings.time.MyZonePicker.class
- line 115: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.content.Intent, com.my.settings.bluetooth.ProvisionBluetoothActivity.class
- line 120: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.content.Intent, com.my.settings.wifi.ProvisionWifiActivity.class
- line 125: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.content.Intent, com.my.settings.activity.MenuPromptActivity.class
- line 130: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.content.Intent, com.my.settings.activity.WarningActivity.class
- line 155: com.my.settings; dispatch APIs nearby: resolveActivity, setAction, startActivity; symbols: android.widget.Toast.makeText, com.my.settings.R.string.app_notinstall
- line 174: com.my.settings; dispatch APIs nearby: resolveActivity, setAction, startActivity; symbols: android.widget.Toast.makeText, com.my.settings.R.string.app_notinstall
- line 196: com.my.settings; dispatch APIs nearby: startActivity; symbols: android.widget.Toast.makeText, com.my.settings.R.string.app_notinstall
- line 210: com.my.settings; dispatch APIs nearby: setComponent, startActivity; symbols: android.widget.Toast.makeText, com.my.settings.R.string.app_notinstall

## trdservice key code / settings dispatch evidence

### com/trd/service/communication/GlobalKeyEventProcess.java

- line 4: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: 
- line 5: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: 
- line 6: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: com.trd.service.communication.GlobalKeyEventProcess
- line 16: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: com.trd.service.communication.GlobalKeyEventProcess
- line 18: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: com.trd.service.communication.GlobalKeyEventProcess.class
- line 20: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: com.trd.service.communication.GlobalKeyEventProcess
- line 27: GlobalKeyEventProcess; dispatch APIs nearby: ; symbols: 
- line 37: com.android.tv.settings, com.trd.projector.settings; dispatch APIs nearby: ; symbols: com.android.tv.settings, com.trd.projector.settings
- line 118: com.trd.projector.settings; dispatch APIs nearby: setComponent, startActivity; symbols: android.content.ComponentName, com.trd.projector.settings, com.trd.projector.settings.MainSettingsActivity
- line 133: com.android.tv.settings; dispatch APIs nearby: setComponent, startActivity; symbols: android.content.ComponentName, com.android.tv.settings, com.android.tv.settings.device.storage.ResetActivity

## zxlauncher key code / settings dispatch evidence

### com/zeasn/utils/TvSetting.java

- line 7: android.settings.SETTINGS; dispatch APIs nearby: startActivity; symbols: android.content.Intent, android.settings.SETTINGS
### com/zeasn/utils/AppUtil.java

- line 645: android.settings.SETTINGS; dispatch APIs nearby: startActivity; symbols: android.content.Intent, android.settings.SETTINGS
### com/zeasn/launcher/CustomApplication.java

- line 178: com.zeasn.whale.saas; dispatch APIs nearby: ; symbols: com.zeasn.launcher.base.viewbuilder.effect.ScaleFocusEffect, com.zeasn.whale.saas.R.drawable.bg_solid_transparent_white_selector

## RuiAutoFocus key code / settings dispatch evidence


## Physical remote caveat

Hardware key layout maps TRD_POPMENU but does not prove which button sends it or which target Activity ultimately launches. Photo of remote alone cannot establish dispatch.

## Signing distinction

- Any modified APK must be signed with a key. OEM platform signature may be required for signature-level permissions; a new key is **not** equivalent.
- privapp-permissions XML can allow privileged permissions, but not change APK signer identity, existing package upgrade checks or all signature-only permissions.
- System partitions may separately be verified by AVB; signing APK alone cannot make a modified system image bootable.
- Do not ship re-signed TvSettingsPlus before checking cert relations with SystemUI/SettingsProvider and whether sharedUserId/signature checks exist.

## Runtime unverified

- ACTION_SETTINGS/Settings intent resolution, getComponentEnabledSettings, privileged grants, keyboard dispatch and installed updated apps need actual device evidence.
- Current binary comparison of two board profiles has 8052 Oct 1.0.4 vs **8054 Sep 1.0.1**, not latest 8054 1.0.4.

