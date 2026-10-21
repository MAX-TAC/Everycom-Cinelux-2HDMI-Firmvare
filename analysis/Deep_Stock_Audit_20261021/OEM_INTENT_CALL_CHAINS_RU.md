# OEM Intent/receiver/service call-site candidates — RUIOS 8052.1.0.4

Static AndroidManifest and JADX source-code reference scan. This is not live execution proof.
A target literal and dispatch function in the same source window is a candidate edge, not a proven dependency.

## Exported and internal component inventory (corrected)

| App | Components | True | False | Unspecified |
|---|---:|---:|---:|---:|
| zxlauncher | 29 | 4 | 10 | 15 |
| zxstore | 25 | 7 | 5 | 13 |
| KuSettings | 16 | 12 | 1 | 3 |
| TvSettingsPlus | 146 | 99 | 42 | 5 |
| RuiYunOta | 6 | 2 | 0 | 4 |
| KuSourceRJ | 38 | 36 | 1 | 1 |
| RuiAutoFocus | 2 | 2 | 0 | 0 |
| trdservice | 4 | 3 | 1 | 0 |
| trdmiddle | 2 | 2 | 0 | 0 |
| KuSetupWizard | 5 | 2 | 1 | 2 |

See corrected verification: [MANIFEST_EXPORTED_VERIFIED_RU.md](MANIFEST_EXPORTED_VERIFIED_RU.md).

## OEM cross-app call candidates


### KuSettings → com.coolux.source

- `com/my/utils/IntentUtils.java:258` — setComponent, startService

### KuSetupWizard → com.coolux.source

- `com/my/utils/IntentUtils.java:258` — setComponent, startService

### KuSetupWizard → com.my.settings

- `com/my/settingslib/RestrictedLockUtilsInternal.java:329` — startActivity
- `com/my/utils/IntentUtils.java:18` — startActivity
- `com/my/utils/IntentUtils.java:155` — setAction, startActivity
- `com/my/utils/IntentUtils.java:196` — setComponent, startActivity
- `com/my/settings/wifi/WifiConfigController.java:1443` — setClassName
- `com/my/settings/activity/ScreenshotActivity.java:188` — startService

### KuSourceRJ → android.settings.SETTINGS

- `com/coolux/source/utils/IntentUtils.java:171` — startActivity

### KuSourceRJ → com.hysd.screen

- `com/coolux/source/utils/IntentUtils.java:29` — startActivity

### RuiYunOta → com.rjpj.yunota.OTACheckService

- `com/rjpj/yunota/OTACheckService.java:154` — setComponent, startActivity

### RuiYunOta → com.rjpj.yunota.OTASystemNetworkUpdateActivity

- `com/rjpj/yunota/OTASystemNetworkUpdateActivity.java:603` — setComponent, startActivity
- `com/rjpj/yunota/OTACheckService.java:143` — setComponent, startActivity

### TvSettingsPlus → android.settings.SETTINGS

- `com/android/tv/settings/accessories/ConnectedDevicesSliceProvider.java:54` — bindService

### TvSettingsPlus → com.coolux.source

- `com/android/tv/settings/uicustom/fragment/general/GeneralFragment.java:113` — setComponent, startActivity
- `com/android/tv/settings/uicustom/floatmenu/controller/general/GeneralSubMenuController.java:135` — setComponent

### TvSettingsPlus → com.hysd.screen

- `com/android/tv/settings/uicustom/fragment/projector/ProjectorFragment.java:149` — setComponent, startService
- `com/android/tv/settings/uicustom/fragment/projector/KeystoneCalibrationActivity.java:330` — setComponent, startService
- `com/android/tv/settings/uicustom/floatmenu/controller/projector/ProjectorSubMenuController.java:135` — setComponent, startService

### trdservice → com.android.tv.settings

- `com/trd/service/communication/GlobalKeyEventProcess.java:133` — setComponent, startActivity

### trdservice → com.rjpj.yunota

- `com/trd/service/TrdService.java:222` — setComponent, startService

### trdservice → com.rjpj.yunota.OTACheckService

- `com/trd/service/TrdService.java:222` — setComponent, startService

### trdservice → com.trd.factory.SplashActivity

- `com/trd/service/communication/GlobalKeyEventProcess.java:110` — setComponent, startActivity

### trdservice → com.trd.projector.settings.MainSettingsActivity

- `com/trd/service/communication/GlobalKeyEventProcess.java:118` — setComponent, startActivity

### zxlauncher → android.settings.SETTINGS

- `com/zeasn/utils/AppUtil.java:645` — startActivity
- `com/zeasn/utils/TvSetting.java:7` — startActivity

### zxstore → android.settings.SETTINGS

- `com/zeasn/utils/AppUtil.java:650` — startActivity
- `com/zeasn/utils/TvSetting.java:7` — startActivity
- `zeasn/open/technical/tv/store/ui/UpgradeClientActivity.java:149` — startActivity

### zxstore → com.android.tv.settings

- `zeasn/open/technical/tv/store/ui/dialogbuilder/NetworkWrongDialogBuilder.java:58` — setComponent, startActivity

## Runtime validation requirements

- Verify exported flags and actual package manager visibility on both real hardware profiles.
- For each candidate, inspect exact data flow from intent creation to dispatch and receiver/action handler.
- Confirm shared UID / signature permissions, service availability and boot-time ordering.
- If disabling app later, test OTA, Home, remote key events, HDMI, focus, keystone and provisioning with rollback.
- A class reference to an OEM package may be dead code or a copied SDK. Do not treat it as a confirmed dependency.

