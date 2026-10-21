# Critical OEM Settings / Setup Wizard static control-flow indicators

Verified source: October 8052.1.0.4. The equivalent APKs in **factory 8054.1.0.1** have identical SHA, except those previously documented as differing. This file is not a comparison to a current 8054.1.0.4 firmware.

**This is a guided static review, not verified bug reproduction.** Each method has approximate counts of branches and exact names of side-effect APIs; there are no decompiled bodies in this report.


## KuSetupWizard


### com/my/settings/wifi/ProvisionWifiActivity.java

- \`next()\` at JADX line 93: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`onCreate()\` at JADX line 73: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys 
- \`onBackPressed()\` at JADX line 83: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`dispatchKeyEvent()\` at JADX line 87: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

### com/my/settings/bluetooth/ProvisionBluetoothActivity.java

- \`next()\` at JADX line 228: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`onCreate()\` at JADX line 58: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys 
- \`onBackPressed()\` at JADX line 67: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`dispatchKeyEvent()\` at JADX line 71: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

### com/my/service/BootupReceiver.java

- \`onReceive()\` at JADX line 10: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

### com/my/utils/IntentUtils.java

- \`provisionWifiIntent()\` at JADX line 118: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'thirdparty': 1}, keys 
- \`provisionBluetoothIntent()\` at JADX line 113: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'thirdparty': 1}, keys 
- \`provisionMenuIntent()\` at JADX line 123: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'thirdparty': 1}, keys 
- \`myWifi()\` at JADX line 16: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'thirdparty': 1}, keys 
- \`startOta()\` at JADX line 64: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 2}, keys android.settings.SYSTEMUPDATE

## KuSettings


### com/my/service/BootupReceiver.java

- \`onReceive()\` at JADX line 10: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

### com/my/service/ScreenServices.java

- \`onStartCommand()\` at JADX line 32: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`setKeyStore()\` at JADX line 37: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'property_write': 1}, keys 
- \`takeScreenShot()\` at JADX line 64: branches {'if': 2, 'switch': 0, 'try': 1, 'catch': 1}, signals {'intent': 1, 'lifecycle': 2, 'errors': 2}, keys 
- \`startShot()\` at JADX line 43: branches {'if': 1, 'switch': 0, 'try': 1, 'catch': 1}, signals {'errors': 2, 'steps': 2}, keys 

### com/my/service/MySetTimeService.java

- \`onStartCommand()\` at JADX line 25: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`registerTimeTick()\` at JADX line 29: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'lifecycle': 1}, keys 

### com/my/settings/SettingActivity.java

- \`onCreate()\` at JADX line 44: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys 
- \`enterClick()\` at JADX line 142: branches {'if': 20, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 19}, keys 
- \`onDestroy()\` at JADX line 68: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

### com/my/utils/IntentUtils.java

- \`startOta()\` at JADX line 64: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 2}, keys android.settings.SYSTEMUPDATE
- \`imageDigitalIntent()\` at JADX line 109: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`keystoneIntent()\` at JADX line 105: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys android.settings.KEYSTONE_SETTINGS
- \`bootSoure()\` at JADX line 81: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys android.settings.BOOTSOURE_SETTINGS
- \`poweron()\` at JADX line 85: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys android.settings.POWERMODE_SETTINGS
- \`startUniversalKJ()\` at JADX line 133: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

## TvSettingsPlus


### com/android/tv/settings/MainSettings.java

- \`createSettingsFragment()\` at JADX line 11: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 2}, keys 

### com/android/tv/settings/MainFragment.java

- \`onCreatePreferences()\` at JADX line 161: branches {'if': 7, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys KEY_ACCESSORIES, KEY_ACCOUNTS_AND_SIGN_IN, KEY_APPLICATIONS, KEY_DISPLAY_AND_SOUND, KEY_PRIVACY
- \`onPreferenceTreeClick()\` at JADX line 498: branches {'if': 3, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'thirdparty': 3}, keys KEY_ACCESSORIES, KEY_ACCOUNTS_AND_SIGN_IN, KEY_BASIC_MODE_EXIT, KEY_CHANNELS_AND_INPUTS, KEY_DISPLAY_AND_SOUND

### com/android/tv/settings/uicustom/MainActivity.java

- \`onCreate()\` at JADX line 111: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys 
- \`onKeyDown()\` at JADX line 293: branches {'if': 14, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 2}, keys 
- \`initPageManager()\` at JADX line 233: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 2}, keys 

### com/android/tv/settings/uicustom/fragment/projector/FocusSettingsFragment.java

- \`setPowerOnAutoFocus()\` at JADX line 67: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys persist.rjpj.autofocus.poweron
- \`setMoveAutoFocus()\` at JADX line 73: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys persist.rjpj.autofocus.move
- \`setAccurateFocus()\` at JADX line 79: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 1}, keys persist.rjpj.tof.autofocus

### com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java

- \`resetFactoryCalibrationData()\` at JADX line 346: branches {'if': 0, 'switch': 0, 'try': 1, 'catch': 1}, signals {'intent': 2, 'property_write': 4, 'binder_hal': 2, 'errors': 2, 'thirdparty': 2}, keys 
- \`startFactoryCalib()\` at JADX line 328: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 2, 'thirdparty': 3}, keys 
- \`saveFactoryCalibrationData()\` at JADX line 388: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 3}, keys 
- \`checkFactoryData()\` at JADX line 150: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 

### com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java

- \`startAutoFocus()\` at JADX line 146: branches {'if': 1, 'switch': 0, 'try': 1, 'catch': 1}, signals {'intent': 2, 'property_read': 2, 'errors': 2, 'thirdparty': 1}, keys 
- \`startAutoKeystone()\` at JADX line 166: branches {'if': 1, 'switch': 0, 'try': 1, 'catch': 1}, signals {'intent': 2, 'property_read': 2, 'errors': 2, 'thirdparty': 1}, keys 
- \`resetTrapezoid()\` at JADX line 219: branches {'if': 0, 'switch': 0, 'try': 1, 'catch': 1}, signals {'intent': 2, 'binder_hal': 1, 'errors': 2}, keys 
- \`jumpActivityByAction()\` at JADX line 232: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'binder_hal': 1}, keys 

### com/android/tv/settings/uicustom/floatmenu/controller/source/SourceSubMenuController.java

- \`initBoardConfig()\` at JADX line 99: branches {'if': 9, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`validateEdidVersion()\` at JADX line 379: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`updateEdidEnableState()\` at JADX line 384: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`checkBluetoothSpeakerPackage()\` at JADX line 417: branches {'if': 0, 'switch': 0, 'try': 1, 'catch': 1}, signals {'errors': 1}, keys BLUETOOTH_SPEAKER_PACKAGE
- \`switchToHDMI()\` at JADX line 425: branches {'if': 2, 'switch': 0, 'try': 0, 'catch': 0}, signals {'binder_hal': 1, 'thirdparty': 1}, keys 
- \`switchToAV()\` at JADX line 442: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {'binder_hal': 1, 'thirdparty': 1}, keys 
- \`switchToUSB()\` at JADX line 457: branches {'if': 0, 'switch': 0, 'try': 1, 'catch': 1}, signals {'intent': 1, 'binder_hal': 1, 'errors': 2, 'thirdparty': 1}, keys 

### com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java

- \`onReceive()\` at JADX line 6: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'intent': 1, 'thirdparty': 1}, keys 

### com/android/tv/settings/partnercustomizer/tvsettingservice/WirelessSpeakerServices.java

- \`onCreate()\` at JADX line 161: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {'thirdparty': 2}, keys 
- \`onDestroy()\` at JADX line 176: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`updateWirelessSpeakerService()\` at JADX line 202: branches {'if': 1, 'switch': 0, 'try': 0, 'catch': 0}, signals {'property_read': 1}, keys 

### com/android/tv/settings/partnercustomizer/utils/SoundEARCReceiver.java

- \`onReceive()\` at JADX line 8: branches {'if': 0, 'switch': 0, 'try': 0, 'catch': 0}, signals {}, keys 
- \`updateEARCSettingValueToDrive()\` at JADX line 12: branches {'if': 0, 'switch': 0, 'try': 2, 'catch': 2}, signals {'property_read': 1, 'binder_hal': 1, 'errors': 4, 'thirdparty': 2}, keys KEY_SOUND_EARC

## Practical interpretation

- \`KuSetupWizard\`: inspect \`ProvisionWifiActivity.next\` and \`ProvisionBluetoothActivity.next\` for how first-run flow is terminated and which service marks provisioning complete; do not remove from factory reset path based on duplicated library code.
- \`KuSettings\`: inspect \`ScreenServices\` system property writes and screenshot service access, plus time service and boot receiver. These can be retained in an adapter or omitted only after proving unused.
- \`TvSettingsPlus\`: preserve \`KeystoneCalibrationActivity\` factory parameters and confirmation guards; never invoke factory resets automatically.
- \`SourceSubMenuController\` depends on board config and Android Settings.Global; never expose a nonexistent second HDMI on 8052.
- \`WirelessSpeakerServices\` starts on boot and should be checked for Bluetooth receiver mode; do not confuse it with A2DP output.
- \`SoundEARCReceiver\` syncs Settings.Global to TV audio control: retain until confirmed not required.
- Error log/printStackTrace is not a bug by itself; review whether failure updates UI or leaves a stale state.
- No Android app or hardware controls were executed or altered.

