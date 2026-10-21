# Проверка TV Settings по официальному исходнику AOSP Android 13

Comparison: original SHA-verified RUIOS 8052.1.0.4 TvSettingsPlus APK (JADX class names/method surfaces) **versus** public AOSP TvSettings tag \`android-13.0.0_r56\`.

**Внимание:** это НЕ доказательство, что OEM использовал именно r56. Исходный commit производителя неизвестен, а результат JADX не равен исходному Java. Здесь выявляем OEM namespace/classes и потенциальные различия API, но не объявляем баги.

| Показатель | Количество |
|---|---:|
 | AOSP Java классы | 475 |
 | OEM JADX Java классы | 987 |
 | Путь класса найден с обеих сторон | 475 |
 | Пути только в OEM | 512 |
 | Пути только в AOSP | 0 |

## OEM-only namespace names

- library: 189 Java classes
- partnercustomizer: 164 Java classes
- uicustom: 142 Java classes
- device: 9 Java classes
- top-level: 5 Java classes
- users: 1 Java classes
- accessories: 1 Java classes
- util: 1 Java classes

## Differing method names in shared class paths (bounded sample)

Method names, not machine-code semantics. Differences also include changes from the exact upstream tag chosen as reference.

- TvSettingsActivity.java: AOSP-only notifyUpdate, notifyUpdateAll, notifyUpdateScreenTitle; OEM-only accept, run, test
- dialog/old/LiteFragment.java: AOSP-only getActivity, getArguments, getResources, getView, isAdded, startActivity; OEM-only 
- dialog/PinDialogFragment.java: AOSP-only dispatchOnIsPinSet; OEM-only accept, onFocusChange, onKey, run
- system/development/DevelopmentFragment.java: AOSP-only updateAudioRecordingMetrics; OEM-only accept, apply, onUpdateMetrics, run
- connectivity/NetworkConfiguration.java: AOSP-only getIpConfiguration, getPrintableName, save, setIpConfiguration; OEM-only 
- dialog/old/ActionAdapter.java: AOSP-only onActionClicked, onActionFocused, onActionSelect, onActionUnselect; OEM-only 
- SettingsPreferenceFragment.java: AOSP-only ; OEM-only onChanged, onLayoutChange, onTouch
- accessories/AddAccessoryActivity.java: AOSP-only ; OEM-only onComplete, run, test
- accessories/BluetoothA2dpConnector.java: AOSP-only failed, handleMessage, succeeded; OEM-only 
- accessories/BluetoothDevicesService.java: AOSP-only onDeviceUpdated; OEM-only accept, run
- autofill/AutofillPickerFragment.java: AOSP-only ; OEM-only onClick, onShow, run
- compat/PreferenceControllerFragmentCompat.java: AOSP-only updatePref; OEM-only accept, onTouch
- device/storage/ClearCachedDataPreference.java: AOSP-only clearCache; OEM-only apply, onPreferenceClick
- inputmethod/KeyboardFragment.java: AOSP-only updatePhysicalKeyboards; OEM-only onPreferenceChange, run
- privacy/SensorFragment.java: AOSP-only ; OEM-only onPreferenceClick, onSensorPrivacyChanged, run
- ActionDisabledByAdminDialogHelper.java: AOSP-only ; OEM-only getEnforcementAdminUserId, onClick
- MainFragment.java: AOSP-only ; OEM-only onConnectivityChange, onPreferenceClick
- accessories/AccessoryUtils.java: AOSP-only ; OEM-only call, onBluetoothManagerInitialized
- accounts/AccountsFragment.java: AOSP-only ; OEM-only onAccountsUpdate, onPreferenceClick
- compat/RenderUtil.java: AOSP-only ; OEM-only accept, test
- connectivity/ConnectivityListener.java: AOSP-only ; OEM-only execute, onInterfaceStateChanged
- connectivity/NetworkFragment.java: AOSP-only ; OEM-only accept, onPreferenceClick
- connectivity/NetworkRequestDialogFragment.java: AOSP-only ; OEM-only onItemClick, onShow
- connectivity/WifiDetailsFragment.java: AOSP-only ; OEM-only onPreferenceChange, onPreferenceClick
- device/apps/specialaccess/NotificationAccess.java: AOSP-only ; OEM-only onPreferenceChange, onServicesReloaded
- device/apps/specialaccess/NotificationAccessCompat.java: AOSP-only updatePref; OEM-only accept
- device/apps/specialaccess/SpecialAccessControllerFragmentCompat.java: AOSP-only updatePref; OEM-only accept
- device/display/daydream/EnergySaverFragment.java: AOSP-only ; OEM-only onClick, onPreferenceClick
- device/displaysound/RadioPreferencesFragmentCompat.java: AOSP-only updatePref; OEM-only accept
- device/storage/AllAppsSession.java: AOSP-only ; OEM-only compare, test
- device/storage/FreeUpStorageFragment.java: AOSP-only ; OEM-only apply, onUpdateAppList
- deviceadmin/DeviceAdminAdd.java: AOSP-only ; OEM-only run, test
- deviceadmin/DeviceAdminListPreferenceController.java: AOSP-only ; OEM-only onPreferenceChange, onPreferenceClick
- enterprise/EnterpriseSetDefaultAppsListPreferenceController.java: AOSP-only updateUi; OEM-only run
- inputmethod/AvailableVirtualKeyboardFragmentCompat.java: AOSP-only updatePref; OEM-only accept
- system/LanguageFragmentCompat.java: AOSP-only updatePref; OEM-only accept
- system/LocationFragment.java: AOSP-only ; OEM-only apply, onPreferenceClick
- system/development/LogpersistPreferenceController.java: AOSP-only ; OEM-only onClick, onDismiss
- widget/ScrollAdapterBase.java: AOSP-only getScrapView, viewRemoved; OEM-only 
- widget/ScrollAdapterView.java: AOSP-only onItemSelected, onScrolled; OEM-only 
- RestrictedSettingsFragment.java: AOSP-only ; OEM-only onDismiss
- SuggestionQuickSettingPrefsContainer.java: AOSP-only ; OEM-only onPreferenceClick
- about/AboutFragment.java: AOSP-only ; OEM-only apply
- about/LegalFragment.java: AOSP-only ; OEM-only onClick
- about/RebootConfirmFragment.java: AOSP-only ; OEM-only onCreateGuidance
- accessibility/AccessibilityFragment.java: AOSP-only ; OEM-only onAccessibilityStateChanged
- accessibility/AccessibilityFragmentCompat.java: AOSP-only updatePref; OEM-only 
- accessibility/AccessibilityServiceFragmentCompat.java: AOSP-only updatePref; OEM-only 
- accessibility/AccessibilityShortcutFragment.java: AOSP-only ; OEM-only onPreferenceChange
- accessibility/AccessibilityShortcutFragmentCompat.java: AOSP-only ; OEM-only onPreferenceChange
- accessibility/AccessibilityShortcutServiceFragment.java: AOSP-only ; OEM-only onPreferenceChange
- accessibility/AccessibilityShortcutServiceFragmentCompat.java: AOSP-only updatePref; OEM-only 
- accessories/AccessoriesFragment.java: AOSP-only ; OEM-only getImageIdForDevice
- accessories/ConnectedDevicesSliceProvider.java: AOSP-only ; OEM-only run
- accounts/AccountSyncFragment.java: AOSP-only ; OEM-only onPreferenceClick
- accounts/AccountsUtil.java: AOSP-only ; OEM-only getAccountsFragmentToLaunch
- connectivity/ActiveNetworkProvider.java: AOSP-only ; OEM-only apply
- connectivity/EditIpSettingsActivity.java: AOSP-only ; OEM-only onFinish
- connectivity/EditProxySettingsActivity.java: AOSP-only ; OEM-only onFinish
- connectivity/EthernetConfig.java: AOSP-only ; OEM-only execute
- connectivity/NetworkFragmentCompat.java: AOSP-only updatePref; OEM-only 
- connectivity/NetworkRequestErrorDialogFragment.java: AOSP-only ; OEM-only onClick
- connectivity/setup/EnterPasswordState.java: AOSP-only ; OEM-only onClick
- connectivity/setup/SelectFromListWizardFragment.java: AOSP-only ; OEM-only onPreDraw
- connectivity/util/StateMachine.java: AOSP-only ; OEM-only onComplete

## Correct bug-review procedure

1. Focus only on project-owned \`uicustom\`, \`partnercustomizer\`, fork-specific extensions, and changes to common entrypoints.
2. For a candidate with direct hardware or settings writes: analyze branch conditions, exception handling, permissions, and persistence.
3. Compare exact methods only after establishing OEM's real AOSP fork point; a single Android 13 release tag is NOT sufficient to attribute a fault.
4. Confirm any crash/regression with real-device logcat and reproducible conditions; never call harmless-looking factory calibration methods on another user's projector.

Source reference: https://android.googlesource.com/platform/packages/apps/TvSettings/+/refs/tags/android-13.0.0_r56

