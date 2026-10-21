# Corrected AndroidManifest component exported flags

Source: verified RUIOS 8052 OTA. A previous static parser mistook the Boolean TYPE marker for the value true. This report reads the value AFTER the marker.

| App | Components | Explicit exported=true | Explicit exported=false | Not specified |
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

## Review candidates (not confirmed security defects)

Listed services/providers/receivers are explicitly exported without a direct per-component permission. App-level checks, inherited privileges, SELinux and runtime restrictions may still apply.

- zxlauncher: receiver com.zeasn.installer.UninstallReceiverFor28
- zxlauncher: receiver com.zeasn.installer.InstallReceiverFor28
- zxstore: service zeasn.open.technical.tv.store.app.StoreService
- zxstore: receiver com.zeasn.installer.UninstallReceiverFor28
- zxstore: receiver com.zeasn.installer.InstallReceiverFor28
- zxstore: receiver com.zeasn.installer.InstallReceiverForXpak
- KuSettings: receiver com.my.service.BootupReceiver
- TvSettingsPlus: provider com.android.tv.settings.partnercustomizer.TvSettingsSliceProvider
- TvSettingsPlus: provider com.android.tv.settings.partnercustomizer.CustomizedContentProvider
- TvSettingsPlus: service com.android.tv.settings.partnercustomizer.tvsettingservice.BluetoothReconnectService
- TvSettingsPlus: service com.android.tv.settings.partnercustomizer.switchofftimer.SwitchOffTimerService
- TvSettingsPlus: service com.android.tv.settings.partnercustomizer.tvsettingservice.WirelessSpeakerServices
- TvSettingsPlus: receiver com.android.tv.settings.partnercustomizer.utils.SoundEARCReceiver
- TvSettingsPlus: receiver com.android.tv.settings.partnercustomizer.tvsettingservice.TvBootupReceiver
- TvSettingsPlus: service com.android.tv.settings.uicustom.floatmenu.FloatMenuService
- TvSettingsPlus: receiver com.android.tv.settings.accessories.BluetoothPairingRequest
- TvSettingsPlus: receiver com.android.tv.settings.users.UserSwitchListenerService$BootReceiver
- TvSettingsPlus: receiver com.android.tv.settings.device.storage.DiskReceiver
- TvSettingsPlus: provider com.android.tv.settings.name.SuggestionContentProvider
- TvSettingsPlus: provider com.android.tv.settings.accessories.ConnectedDevicesSliceProvider
- TvSettingsPlus: receiver com.android.tv.settings.BootReceiver
- TvSettingsPlus: receiver com.android.tv.settings.GlobalKeyReceiver
- KuSourceRJ: receiver com.coolux.source.service.BootupReceiver
- KuSourceRJ: receiver com.coolux.source.service.ScreensaverReceiver
- KuSourceRJ: receiver com.coolux.source.service.BrightReceiver
- RuiAutoFocus: service com.hysd.client.VAF2S
- trdservice: service com.trd.service.TrdService
- trdservice: receiver com.trd.service.system.shutdown.PreShutdownReceiver
- trdmiddle: service com.trd.framework.TrdSystemService

## Interpretation

- Unspecified exported flag does not mean false; Android defaults depend on component kind and intent filters.
- A listed candidate does not establish untrusted-app reachability or privilege escalation.
- Do not send test intents to safety-sensitive functions on another person's projector.

