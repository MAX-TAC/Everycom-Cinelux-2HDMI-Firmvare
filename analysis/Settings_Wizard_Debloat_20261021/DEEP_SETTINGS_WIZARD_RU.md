# Deep static audit of KuSetupWizard, KuSettings and TvSettingsPlus

Based on verified RUIOS 8052.1.0.4 source APKs. TvSettingsPlus and KuSettings are byte-identical in the archived original Sep 8054.1.0.1, while original updated 8054.1.0.4 is unavailable.

**JADX API occurrences are search signals only. They do not prove a reachable code path, a crash, or firmware incompatibility.**

## Java classes and manifest coverage

| APK | Decompiled Java files | OEM-owned files | Manifest components |
|---|---:|---:|---|
| KuSetupWizard | 3471 | 151 | {'activity': 3, 'provider': 1, 'receiver': 1} |
| KuSettings | 3470 | 150 | {'activity': 11, 'service': 2, 'receiver': 2, 'provider': 1} |
| TvSettingsPlus | 5796 | 1017 | {'provider': 6, 'activity': 120, 'receiver': 12, 'service': 8} |

## KuSetupWizard

**Namespace-group file counts:** ilogic=2, constant=1, settingslib=67, model=1, utils=10, settings=58, courview=5, adapter=1, listenner=2, service=3, provision=1

**Observed code API families:** launch=49, package_dependencies=3041, provision_components=41, remote=377, risk_candidates=97, persistence=85, boot_setup=46, lifecycle=133, provision_flag=3

### Important concrete Java classes and method names

- com/my/utils/IntentUtils.java: getInstance, myWifi, myBluetooth, autoBluetooth, myDateTime, myLanguage, languageLocal, timeZone, screenshot, projectAbout, brightIntent, voiceIntent, startOta, restoreIntent, startTest, bootSoure, poweron, projectModel, mircastIntent, airplayIntent, keystoneIntent, imageDigitalIntent, provisionBluetoothIntent, provisionWifiIntent; evidence {'package_dependencies': 14, 'launch': 17, 'boot_setup': 1, 'remote': 13, 'risk_candidates': 4}
- com/my/settings/SettingActivity.java: onClick, onReceive, onCreate, onResume, onPause, onDestroy, init, findUI, initView, isViewRemote, setVersionView, enterClick, isUpdataOtaRegister, viewIsUpdataOta; evidence {'package_dependencies': 46, 'remote': 6, 'lifecycle': 8, 'persistence': 1}
- com/my/service/BootupReceiver.java: onReceive; evidence {'boot_setup': 4, 'launch': 2}
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java: handleMessage, onReceive, onClick, onCreate, onBackPressed, dispatchKeyEvent, onResume, onPause, onDestroy, init, findUI, initView, initBtstatus, registerReceiver, getStatus, refreshDeviceList, startScan, stopScan, getIrBluetoothStatus, connectFinsh, isAutoName, enterClick, next; evidence {'package_dependencies': 28, 'remote': 3, 'lifecycle': 10}
- com/my/settings/wifi/ProvisionWifiActivity.java: onFocusChange, onClick, onReceive, onCreate, onBackPressed, dispatchKeyEvent, next, oncreatBundleStatue, initProgressDialog, onDialogCreate, init, onResume, onPause, onDestroy, initView, isWifiOpen, viewWifiStatue, openWifiSwitch, closeWifiSwitch, findUI, onItemClick, enterFocus, loseFocus, switchViewUI; evidence {'package_dependencies': 94, 'boot_setup': 39, 'remote': 10, 'lifecycle': 8, 'risk_candidates': 4, 'persistence': 4, 'provision_components': 1}
- com/my/settings/wifi/MyWifiActivity.java: onFocusChange, onClick, onReceive, onCreate, oncreatBundleStatue, initProgressDialog, onDialogCreate, init, onResume, onPause, onDestroy, initView, isWifiOpen, viewWifiStatue, openWifiSwitch, closeWifiSwitch, findUI, onItemClick, enterFocus, loseFocus, switchViewUI, lister, onSuccess, onFailure; evidence {'package_dependencies': 86, 'lifecycle': 8, 'risk_candidates': 3, 'remote': 6, 'persistence': 2, 'provision_components': 1}

### High-risk or migration-relevant API call sites

**boot_setup**
- com/my/utils/IntentUtils.java:120: ProvisionWifiActivity
- com/my/service/BootupReceiver.java:4: BootupReceiver
- com/my/service/BootupReceiver.java:5: BootupReceiver
- com/my/service/BootupReceiver.java:6: BOOT_COMPLETED
- com/my/service/BootupReceiver.java:13: BOOT_COMPLETED
- com/my/settings/wifi/ProvisionWifiActivity.java:4: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:10: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:36: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:40: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:42: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:46: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:49: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:52: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:57: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:61: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:62: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:64: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:65: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:67: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:113: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:205: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:209: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:212: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:213: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:214: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:215: ProvisionWifiActivity, provisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:216: provisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:219: ProvisionWifiActivity, provisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:220: provisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:224: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:225: ProvisionWifiActivity, provisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:226: provisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:248: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:253: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:256: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:261: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:264: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:269: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:367: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:424: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:427: ProvisionWifiActivity
- com/my/settings/wifi/ProvisionWifiActivity.java:432: ProvisionWifiActivity
**provision_components**
- com/my/settings/wifi/ProvisionWifiActivity.java:389: DevicePolicyManager
- com/my/settings/wifi/MyWifiActivity.java:343: DevicePolicyManager
**persistence**
- com/my/settings/SettingActivity.java:229: SharedPreferences
- com/my/settings/wifi/ProvisionWifiActivity.java:358: Settings.Global.get
- com/my/settings/wifi/ProvisionWifiActivity.java:406: Settings.Global.get
- com/my/settings/wifi/ProvisionWifiActivity.java:618: SharedPreferences
- com/my/settings/wifi/ProvisionWifiActivity.java:619: SharedPreferences
- com/my/settings/wifi/MyWifiActivity.java:312: Settings.Global.get
- com/my/settings/wifi/MyWifiActivity.java:360: Settings.Global.get
**lifecycle**
- com/my/settings/SettingActivity.java:53: onResume
- com/my/settings/SettingActivity.java:54: onResume
- com/my/settings/SettingActivity.java:59: onPause
- com/my/settings/SettingActivity.java:60: onPause
- com/my/settings/SettingActivity.java:63: unregisterReceiver
- com/my/settings/SettingActivity.java:68: onDestroy
- com/my/settings/SettingActivity.java:70: onDestroy
- com/my/settings/SettingActivity.java:224: registerReceiver
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:79: onResume
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:80: onResume
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:85: onPause
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:86: onPause
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:91: unregisterReceiver
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:96: onDestroy
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:97: onDestroy
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:112: registerReceiver
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:137: registerReceiver
- com/my/settings/bluetooth/ProvisionBluetoothActivity.java:146: registerReceiver
- com/my/settings/wifi/ProvisionWifiActivity.java:137: onResume
- com/my/settings/wifi/ProvisionWifiActivity.java:138: onResume
- com/my/settings/wifi/ProvisionWifiActivity.java:147: onPause
- com/my/settings/wifi/ProvisionWifiActivity.java:148: onPause
- com/my/settings/wifi/ProvisionWifiActivity.java:157: onDestroy
- com/my/settings/wifi/ProvisionWifiActivity.java:168: onDestroy
- com/my/settings/wifi/ProvisionWifiActivity.java:606: registerReceiver
- com/my/settings/wifi/ProvisionWifiActivity.java:612: unregisterReceiver
- com/my/settings/wifi/MyWifiActivity.java:112: onResume
- com/my/settings/wifi/MyWifiActivity.java:113: onResume
- com/my/settings/wifi/MyWifiActivity.java:122: onPause
- com/my/settings/wifi/MyWifiActivity.java:123: onPause
- com/my/settings/wifi/MyWifiActivity.java:132: onDestroy
- com/my/settings/wifi/MyWifiActivity.java:143: onDestroy
- com/my/settings/wifi/MyWifiActivity.java:557: registerReceiver
- com/my/settings/wifi/MyWifiActivity.java:563: unregisterReceiver
**risk_candidates**
- com/my/utils/IntentUtils.java:158: printStackTrace
- com/my/utils/IntentUtils.java:177: printStackTrace
- com/my/utils/IntentUtils.java:227: getSystemService(
- com/my/utils/IntentUtils.java:256: getSystemService(
- com/my/settings/wifi/ProvisionWifiActivity.java:175: Open(
- com/my/settings/wifi/ProvisionWifiActivity.java:180: Open(
- com/my/settings/wifi/ProvisionWifiActivity.java:300: getSystemService(
- com/my/settings/wifi/ProvisionWifiActivity.java:389: getSystemService(
- com/my/settings/wifi/MyWifiActivity.java:150: Open(
- com/my/settings/wifi/MyWifiActivity.java:155: Open(
- com/my/settings/wifi/MyWifiActivity.java:343: getSystemService(

## KuSettings

**Namespace-group file counts:** ilogic=2, constant=1, settingslib=67, model=1, utils=10, settings=58, courview=5, adapter=1, listenner=2, service=3

**Observed code API families:** launch=49, package_dependencies=3040, provision_components=41, remote=371, risk_candidates=97, persistence=85, boot_setup=46, lifecycle=133, provision_flag=3

### Important concrete Java classes and method names

- com/my/utils/IntentUtils.java: getInstance, myWifi, myBluetooth, autoBluetooth, myDateTime, myLanguage, languageLocal, timeZone, screenshot, projectAbout, brightIntent, voiceIntent, startOta, restoreIntent, startTest, bootSoure, poweron, projectModel, mircastIntent, airplayIntent, keystoneIntent, imageDigitalIntent, provisionBluetoothIntent, provisionWifiIntent; evidence {'package_dependencies': 14, 'launch': 17, 'boot_setup': 1, 'remote': 13, 'risk_candidates': 4}
- com/my/settings/SettingActivity.java: onClick, onReceive, onCreate, onResume, onPause, onDestroy, init, findUI, initView, isViewRemote, setVersionView, enterClick, isUpdataOtaRegister, viewIsUpdataOta; evidence {'package_dependencies': 46, 'remote': 6, 'lifecycle': 8, 'persistence': 1}
- com/my/service/MySetTimeService.java: onReceive, onBind, onStartCommand, registerTimeTick; evidence {'launch': 2, 'remote': 1, 'lifecycle': 2}
- com/my/service/ScreenServices.java: handleMessage, handleMessage, onBind, onStartCommand, setKeyStore, startShot, run, takeScreenShot, onServiceConnected, handleMessage, onServiceDisconnected; evidence {'lifecycle': 3, 'persistence': 2, 'risk_candidates': 4, 'launch': 1}
- com/my/service/BootupReceiver.java: onReceive; evidence {'boot_setup': 4, 'launch': 2}
- com/my/settings/bluetooth/MyBluetoothActivity.java: handleMessage, onReceive, updateDeviceName, onFocusChange, onClick, onCreate, onResume, onPause, onDestroy, init, onResumeInit, onPauseInit, registerBluetooth, unregisterBluetooth, visionLayout, findUI, myParidViewUI, updateContent, statueOn, scanMode, isScan, startScanning, stopScan, refreshScan; evidence {'package_dependencies': 93, 'lifecycle': 12, 'remote': 5}
- com/my/settings/activity/ProjectionActivity.java: handleMessage, onKey, onClick, onCreate, onResume, onPause, onDestroy, init, findUI, initView, viewHS, viewSystemTem, enterClick, sysInfo, memInfo, ipInfo, viewKJ, testAction, testKJAction, testCPUAction; evidence {'package_dependencies': 45, 'remote': 14, 'lifecycle': 6}
- com/my/settings/wifi/MyWifiActivity.java: onFocusChange, onClick, onReceive, onCreate, oncreatBundleStatue, initProgressDialog, onDialogCreate, init, onResume, onPause, onDestroy, initView, isWifiOpen, viewWifiStatue, openWifiSwitch, closeWifiSwitch, findUI, onItemClick, enterFocus, loseFocus, switchViewUI, lister, onSuccess, onFailure; evidence {'package_dependencies': 86, 'lifecycle': 8, 'risk_candidates': 3, 'remote': 6, 'persistence': 2, 'provision_components': 1}

### High-risk or migration-relevant API call sites

**boot_setup**
- com/my/utils/IntentUtils.java:120: ProvisionWifiActivity
- com/my/service/BootupReceiver.java:4: BootupReceiver
- com/my/service/BootupReceiver.java:5: BootupReceiver
- com/my/service/BootupReceiver.java:6: BOOT_COMPLETED
- com/my/service/BootupReceiver.java:13: BOOT_COMPLETED
**provision_components**
- com/my/settings/wifi/MyWifiActivity.java:343: DevicePolicyManager
**persistence**
- com/my/settings/SettingActivity.java:229: SharedPreferences
- com/my/service/ScreenServices.java:33: SharedPreferences
- com/my/service/ScreenServices.java:39: SystemProperties.set
- com/my/settings/wifi/MyWifiActivity.java:312: Settings.Global.get
- com/my/settings/wifi/MyWifiActivity.java:360: Settings.Global.get
**lifecycle**
- com/my/settings/SettingActivity.java:53: onResume
- com/my/settings/SettingActivity.java:54: onResume
- com/my/settings/SettingActivity.java:59: onPause
- com/my/settings/SettingActivity.java:60: onPause
- com/my/settings/SettingActivity.java:63: unregisterReceiver
- com/my/settings/SettingActivity.java:68: onDestroy
- com/my/settings/SettingActivity.java:70: onDestroy
- com/my/settings/SettingActivity.java:224: registerReceiver
- com/my/service/MySetTimeService.java:25: onStartCommand
- com/my/service/MySetTimeService.java:31: registerReceiver
- com/my/service/ScreenServices.java:32: onStartCommand
- com/my/service/ScreenServices.java:81: unbindService
- com/my/service/ScreenServices.java:102: bindService
- com/my/settings/bluetooth/MyBluetoothActivity.java:116: onResume
- com/my/settings/bluetooth/MyBluetoothActivity.java:117: onResume
- com/my/settings/bluetooth/MyBluetoothActivity.java:118: onResume
- com/my/settings/bluetooth/MyBluetoothActivity.java:125: onPause
- com/my/settings/bluetooth/MyBluetoothActivity.java:126: onPause
- com/my/settings/bluetooth/MyBluetoothActivity.java:127: onPause
- com/my/settings/bluetooth/MyBluetoothActivity.java:132: onDestroy
- com/my/settings/bluetooth/MyBluetoothActivity.java:133: onDestroy
- com/my/settings/bluetooth/MyBluetoothActivity.java:153: onResume
- com/my/settings/bluetooth/MyBluetoothActivity.java:159: onPause
- com/my/settings/bluetooth/MyBluetoothActivity.java:172: registerReceiver
- com/my/settings/bluetooth/MyBluetoothActivity.java:179: unregisterReceiver
- com/my/settings/activity/ProjectionActivity.java:118: onResume
- com/my/settings/activity/ProjectionActivity.java:119: onResume
- com/my/settings/activity/ProjectionActivity.java:126: onPause
- com/my/settings/activity/ProjectionActivity.java:127: onPause
- com/my/settings/activity/ProjectionActivity.java:134: onDestroy
- com/my/settings/activity/ProjectionActivity.java:135: onDestroy
- com/my/settings/wifi/MyWifiActivity.java:112: onResume
- com/my/settings/wifi/MyWifiActivity.java:113: onResume
- com/my/settings/wifi/MyWifiActivity.java:122: onPause
- com/my/settings/wifi/MyWifiActivity.java:123: onPause
- com/my/settings/wifi/MyWifiActivity.java:132: onDestroy
- com/my/settings/wifi/MyWifiActivity.java:143: onDestroy
- com/my/settings/wifi/MyWifiActivity.java:557: registerReceiver
- com/my/settings/wifi/MyWifiActivity.java:563: unregisterReceiver
**risk_candidates**
- com/my/utils/IntentUtils.java:158: printStackTrace
- com/my/utils/IntentUtils.java:177: printStackTrace
- com/my/utils/IntentUtils.java:227: getSystemService(
- com/my/utils/IntentUtils.java:256: getSystemService(
- com/my/service/ScreenServices.java:49: Thread.sleep
- com/my/service/ScreenServices.java:51: Thread.sleep
- com/my/service/ScreenServices.java:57: printStackTrace
- com/my/service/ScreenServices.java:93: printStackTrace
- com/my/settings/wifi/MyWifiActivity.java:150: Open(
- com/my/settings/wifi/MyWifiActivity.java:155: Open(
- com/my/settings/wifi/MyWifiActivity.java:343: getSystemService(

## TvSettingsPlus

**Namespace-group file counts:** other=30, GlobalKeyReceiver.java=1, TakeBugReportController.java=1, Manifest.java=1, RestrictedSettingsFragment.java=1, TvSettingsApplication.java=1, BootReceiver.java=1, PreferenceControllerFragment$$ExternalSyntheticLambda0.java=1, MainFragment.java=1, ActionDisabledByAdminDialogHelper.java=1, HotwordSwitchController.java=1, SettingsPreferenceFragment.java=1, SystemSoundsPlayer.java=1, DeviceSettingBroadcastReceiver.java=1, HasSettingsManager.java=1, PreferenceControllerFragment.java=1, PreferenceExUtils.java=1, EventLogTags.java=1, MainSettings.java=1, LongClickPreference.java=1, TvSettingsActivity.java=1, RestrictedPreferenceAdapter.java=1, SettingsFragmentProvider.java=1, SuggestionQuickSettingPrefsContainer.java=1, RadioPreference.java=1, RemoteBugreportActivity.java=1, NopePreferenceController.java=1, R.java=1, PreferenceUtils.java=1, ActionDisabledByAdminDialog.java=1, EmptyStubActivity.java=1, BaseSettingsFragment.java=1, overlay=5, uicustom=142, slice=1, privacy=11, device=118, enterprise=29, accessories=26, system=43, name=9, deviceadmin=5, inputmethod=9, accounts=12, basic=2, help=1, about=18, partnercustomizer=164, oemlink=3, users=8, connectivity=77, compat=16, suggestions=2, dialog=15, library=189, widget=21, util=12, accessibility=9, vendor=5, autofill=3, core=1

**Observed code API families:** remote=2246, persistence=828, risk_candidates=471, launch=460, package_dependencies=18224, provision_flag=9, lifecycle=911, provision_components=258, hardware=39, boot_setup=3

### Important concrete Java classes and method names

- com/android/tv/settings/BootReceiver.java: onReceive; evidence {'package_dependencies': 4, 'remote': 1, 'launch': 1}
- com/android/tv/settings/MainFragment.java: onReceive, getPageId, newInstance, getPreferenceScreenResId, onAttach, onCreate, onConnectivityChange, onConnectivityChange, isWifiScanOptimisationEnabled, onCreateView, updateConnectivityType, onCreatePreferences, getStringResource, getDrawableResource, systemIntentIsHandled, getProviderInfo, isRestricted, updateChannelsAndInputs, onStart, onStop, onPreferenceTreeClick, onDestroy, onCreatePreferenceControllers, onSuggestionClosed; evidence {'package_dependencies': 79, 'remote': 33, 'lifecycle': 7, 'persistence': 1, 'launch': 1}
- com/android/tv/settings/MainSettings.java: isStartupVerificationRequired, createSettingsFragment; evidence {'package_dependencies': 5}
- com/android/tv/settings/uicustom/MainActivity.java: onReceive, onTick, onFinish, resetExitTimer, onStart, onCreate, onResume, onStop, onDestroy, finish, onConfigurationChanged, initData, initView, initPageManager, initMenuEvents, setItemListener, onFocusChange, switchPage, switchPage2, onKeyDown, onFragmentEvent, onGetFragmentData, onResetExitTimer, requestFocusToFirstFragmentItem; evidence {'package_dependencies': 49, 'remote': 18, 'launch': 5, 'lifecycle': 9}
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java: getLayoutResId, onFirstLoad, onReLoad, refreshTexts, initData, initView, onSwitchChangeListener, onSwitchChangeListener, onSwitchChangeListener, setPowerOnAutoFocus, setMoveAutoFocus, setAccurateFocus; evidence {'package_dependencies': 27, 'persistence': 6}
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java: handleMessage, checkFactoryData, getEnvFactorySensorBiasAccXYZ, init, onResume, onCreate, onStop, initView, initListener, updateCorrectionStatus, setEnvSensorBiasAccXYZ, getIntByString, setEnvFactorySensorBiasAccXYZ, getCalibrationStatus, startFactoryCalib, resetFactoryCalibrationData, resetFactoryCalibrationDialog, onClick, saveFactoryCalibrationData, isAutoFocusFileExist, onClick; evidence {'package_dependencies': 80, 'persistence': 21, 'risk_candidates': 3, 'lifecycle': 4, 'launch': 4}
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java: getLayoutResId, onFirstLoad, initData, initView, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onReLoad, refreshTexts, startAutoFocus, startAutoKeystone, toTrapezoidCorrection, showResetDialog, onClick, onClick, resetTrapezoid, jumpActivityByAction; evidence {'package_dependencies': 59, 'hardware': 2, 'remote': 3, 'persistence': 2, 'launch': 10, 'risk_candidates': 4}
- com/android/tv/settings/uicustom/fragment/general/BrightnessModeSettingsFragment.java: getLayoutResId, onFirstLoad, onReLoad, refreshTexts, initData, initView, initCheck, initListener, onCheckedChanged, onCheckedChanged, onCheckedChanged, onCheckedChanged; evidence {'package_dependencies': 50, 'launch': 6}
- com/android/tv/settings/uicustom/fragment/picture/PictureModeValueFragment.java: getLayoutResId, onFirstLoad, refreshTexts, initData, initView, onValueChanged, onValueChanged, onValueChanged, onValueChanged, onValueChanged, onReLoad, handleActivityEvent; evidence {'package_dependencies': 50}
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java: onAttach, onResume, onKey, initData, initBoardConfig, initView, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onSwitchChangeListener, onSwitchChangeListener, onSwitchChangeListener, onSwitchChangeListener, getEdidVersion, validateEdidVersion, updateEdidEnableState, showCecEnergyDialog; evidence {'package_dependencies': 84, 'remote': 103, 'lifecycle': 2, 'persistence': 5, 'provision_components': 2, 'risk_candidates': 9, 'launch': 6}
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java: onAttach, onResume, onKey, initData, initView, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, onClick, startAutoFocus, startAutoKeystone, showResetDialog, onClick, resetTrapezoid, jumpActivityByAction; evidence {'package_dependencies': 50, 'lifecycle': 1, 'hardware': 2, 'remote': 3, 'persistence': 2, 'launch': 7, 'risk_candidates': 3}
- com/android/tv/settings/device/sound/AudioOutputFragment.java: getMetricsCategory, onCreatePreferences, onResume, onStart, onPreferenceTreeClick, getDigitalOutputEntries, initPreferences, onPreferenceChange, showVolumeTipsDialog, onClick; evidence {'package_dependencies': 25, 'remote': 4, 'persistence': 6, 'lifecycle': 2, 'launch': 1, 'risk_candidates': 1}
- com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java: onReceive; evidence {'package_dependencies': 2, 'boot_setup': 2, 'launch': 1}
- com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java: handleChangeSpeakerToSettings, handleSpeakerServiceStarted, handleSpeakerConnectedNotification, handleSpeakerDisconnectedNotification, handleSpeakerServiceDied, handleSpeakerInfoNotification, handleSpeakerOTAStatusNotification, handleSpeakerJitterStatusNotification, handleMessage, onBind, getService, onCreate, onDestroy, initWindowManager, updateWirelessSpeakerService, getWirelessShowInfo, showMessage, showJitterBufferDialog, onClick, onClick; evidence {'package_dependencies': 57, 'risk_candidates': 2, 'lifecycle': 3, 'persistence': 1}
- com/android/tv/settings/partnercustomizer/utils/SoundEARCReceiver.java: onReceive, updateEARCSettingValueToDrive; evidence {'package_dependencies': 3, 'remote': 1, 'persistence': 1, 'risk_candidates': 1}
- com/android/tv/settings/partnercustomizer/picture/PictureModeFragment.java: onReceive, getMetricsCategory, newInstance, onCreate, onStart, onDestroy, onCreatePreferences, accept, decline, getEntriesValue, getEntries, isSupportImaxAutoDetect, insert, onPreferenceTreeClick, showConfirmation, confirmed, finishActivity, onPfTreeClick; evidence {'package_dependencies': 80, 'lifecycle': 4, 'persistence': 4, 'remote': 24, 'launch': 2}
- com/android/tv/settings/partnercustomizer/picture/GammaFragment.java: getMetricsCategory, onCreate, onCreatePreferences, accept, decline, onPreferenceTreeClick, showConfirmation, confirmed, onPfTreeClick; evidence {'package_dependencies': 30, 'persistence': 4, 'remote': 4, 'launch': 1}

### High-risk or migration-relevant API call sites

**boot_setup**
- com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java:4: BootupReceiver
- com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java:7: BootupReceiver
**provision_components**
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:351: Settings.Global.putInt
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:411: Settings.Global.putInt
**hardware**
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:37: ProjectorManager
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:126: ProjectorManager
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:34: ProjectorManager
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:55: ProjectorManager
**persistence**
- com/android/tv/settings/MainFragment.java:497: PreferenceManager
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java:31: SystemProperties.get, persist.
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java:32: SystemProperties.get, persist.
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java:33: SystemProperties.get, persist.
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java:69: persist.
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java:75: persist.
- com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java:82: persist.
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:29: persist.
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:30: persist.
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:31: persist.
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:63: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:99: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:104: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:256: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:257: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:258: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:259: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:260: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:261: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:262: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:285: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:313: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:320: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:355: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:356: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:357: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:361: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:402: SystemProperties.set
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:148: SystemProperties.get
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:168: SystemProperties.get
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:94: SystemProperties.get, persist.
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:338: SystemProperties.set, persist.
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:351: Settings.Global.put
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:411: Settings.Global.put
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:482: SystemProperties.get, persist.
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:134: SystemProperties.get
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:154: SystemProperties.get
- com/android/tv/settings/device/sound/AudioOutputFragment.java:17: PreferenceManager
- com/android/tv/settings/device/sound/AudioOutputFragment.java:38: PreferenceManager
- com/android/tv/settings/device/sound/AudioOutputFragment.java:49: PreferenceManager
- com/android/tv/settings/device/sound/AudioOutputFragment.java:58: PreferenceManager
- com/android/tv/settings/device/sound/AudioOutputFragment.java:61: PreferenceManager
**lifecycle**
- com/android/tv/settings/MainFragment.java:488: registerReceiver
- com/android/tv/settings/MainFragment.java:492: onStop
- com/android/tv/settings/MainFragment.java:493: onStop
- com/android/tv/settings/MainFragment.java:494: unregisterReceiver
- com/android/tv/settings/MainFragment.java:513: onDestroy
- com/android/tv/settings/MainFragment.java:514: onDestroy
- com/android/tv/settings/MainFragment.java:515: onDestroy
- com/android/tv/settings/uicustom/MainActivity.java:107: registerReceiver
- com/android/tv/settings/uicustom/MainActivity.java:122: onResume
- com/android/tv/settings/uicustom/MainActivity.java:123: onResume
- com/android/tv/settings/uicustom/MainActivity.java:128: onStop
- com/android/tv/settings/uicustom/MainActivity.java:129: onStop
- com/android/tv/settings/uicustom/MainActivity.java:132: unregisterReceiver
- com/android/tv/settings/uicustom/MainActivity.java:138: onDestroy
- com/android/tv/settings/uicustom/MainActivity.java:152: onDestroy
- com/android/tv/settings/uicustom/MainActivity.java:463: onDestroy
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:187: onResume
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:202: onResume
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:220: onStop
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:222: onStop
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:53: onResume
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:54: onResume
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:33: onResume
- com/android/tv/settings/device/sound/AudioOutputFragment.java:22: onResume
- com/android/tv/settings/device/sound/AudioOutputFragment.java:29: onResume
- com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java:176: onDestroy
- com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java:177: onDestroy
- com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java:181: onDestroy
- com/android/tv/settings/partnercustomizer/picture/PictureModeFragment.java:49: registerReceiver
- com/android/tv/settings/partnercustomizer/picture/PictureModeFragment.java:59: onDestroy
- com/android/tv/settings/partnercustomizer/picture/PictureModeFragment.java:60: unregisterReceiver
- com/android/tv/settings/partnercustomizer/picture/PictureModeFragment.java:61: onDestroy
**risk_candidates**
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:143: printStackTrace
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:364: printStackTrace
- com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:383: printStackTrace
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:161: printStackTrace
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:181: printStackTrace
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:194: printStackTrace
- com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:227: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:354: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:414: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:428: getSystemService(
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:445: getSystemService(
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:465: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:477: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:536: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:542: getSystemService(
- com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java:546: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:147: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:167: printStackTrace
- com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:194: printStackTrace
- com/android/tv/settings/device/sound/AudioOutputFragment.java:49: getSystemService(
- com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java:166: getSystemService(
- com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java:186: getSystemService(
- com/android/tv/settings/partnercustomizer/utils/SoundEARCReceiver.java:25: printStackTrace

## Decision discipline

- \`KuSetupWizard\` cannot be removed just because its Java library copies \`KuSettings\`; its package \`com.android.provision\` has different setup lifecycle and intent filters.
- \`TvSettingsPlus\` is a modified Android TV Settings; existing \`uicustom\` and \`partnercustomizer\` should be reused where tested; AOSP baseline source comparison is required to assign a defect to an OEM change.
- FLauncher must explicitly open \`com.android.tv.settings/.MainSettings\`; \`android.settings.SETTINGS\` resolves to OEM \`KuSettings\` on stock manifests.
- For any apparent bug candidate, read the full method and inbound call chain, check error handling and show a reproducible device scenario before calling it a confirmed defect.
- No APK code or binaries were altered, no device was accessed.

