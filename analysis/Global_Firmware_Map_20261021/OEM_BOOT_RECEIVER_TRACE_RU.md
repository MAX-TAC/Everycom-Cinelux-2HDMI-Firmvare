# Обработчики BOOT_COMPLETED и служебная логика KuSettings / TvSettingsPlus / TRD

Static JADX call markers only. A method name near a BOOT_COMPLETED receiver does **not** prove invocation without a full control-flow/data-flow trace.
Source: verified Oct OTA RUIOS.8052.1.0.4. No proprietary decompiled source exported.

## Почему этот аудит нужен

- \`KuSettings\` является отдельным OEM UI, но его манифест содержит \`com.my.service.BootupReceiver\` с BOOT_COMPLETED.
- \`TvSettingsPlus\` тоже содержит штатный \`BootReceiver\`, \`TvBootupReceiver\` и \`SoundEARCReceiver\`.
- \`KuSetupWizard\` похож на KuSettings в Java-коде, но имеет другое package identity и first-boot component.
- Для решения о полном удалении KuSettings нужно убедиться, что собственный receiver не запускает уникальные hardware services/TV initialization.

## Извлечённые маркеры вызовов


## KuSettings


### com/my/service/BootupReceiver.java

Source lines: 17
- 6: android.intent.action.BOOT_COMPLETED; refs ACTION_BOOT,android.intent.action.BOOT_COMPLETED
- 10: onReceive; refs android.content.Context,android.content.Intent
- 13: android.intent.action.BOOT_COMPLETED; refs android.intent.action.BOOT_COMPLETED

### com/my/service/ScreenServices.java

Source lines: 106
- 32: onStartCommand; refs android.content.Intent
- 39: SystemProperties.set; refs android.os.SystemProperties.set
- 70: setClassName; refs com.android.systemui,com.android.systemui.screenshot.TakeScreenshotService
- 102: bindService; refs bindService,serviceConnection

### com/my/settings/SettingActivity.java

Source lines: 235
- 35: onReceive; refs android.content.Context,android.content.Intent
- 44: onCreate; refs android.os.Bundle
- 45: onCreate; refs 
- 224: registerReceiver; refs registerReceiver,this.isUpdataOtaReceiver

### com/my/utils/IntentUtils.java

Source lines: 272
- 19: startActivity; refs 
- 24: startActivity; refs 
- 116: startActivity; refs 
- 121: startActivity; refs 
- 126: startActivity; refs 
- 131: startActivity; refs 
- 150: setAction; refs 
- 153: startActivity; refs 
- 167: setAction; refs 
- 171: startActivity; refs 
- 188: startActivity; refs 
- 194: startActivity; refs 
- 206: setComponent; refs android.content.ComponentName
- 208: startActivity; refs 
- 227: getSystemService; refs android.app.ActivityManager,context.getSystemService
- 238: startService; refs context.startService
- 256: getSystemService; refs android.app.ActivityManager,context.getSystemService
- 268: setComponent; refs android.content.ComponentName,com.coolux.source,com.coolux.source.service.TimeService
- 269: startService; refs context.startService

## TvSettingsPlus


### com/android/tv/settings/BootReceiver.java

Source lines: 16
- 10: onReceive; refs android.content.Context,android.content.Intent
- 14: startService; refs android.content.Intent,com.android.tv.settings.accessories.BluetoothDevicesService.class,context.startService

### com/android/tv/settings/partnercustomizer/tvsettingservice/TvBootupReceiver.java

Source lines: 10
- 6: onReceive; refs android.content.Context,android.content.Intent
- 8: startService; refs android.content.Intent,com.android.tv.settings.partnercustomizer.tvsettingservice.WirelessSpeakerServices.class,context.startService

### com/android/tv/settings/partnercustomizer/utils/SoundEARCReceiver.java

Source lines: 28
- 8: onReceive; refs android.content.Context,android.content.Intent
- 9: onReceive; refs com.mediatek.wwtv.tvcenter.util.MtkLog.d
- 16: Settings.Global; refs android.provider.Settings.Global.getInt,com.android.tv.settings.partnercustomizer.tvsettingservice.util.PreferenceConfigUtilsBase.KEY_SOUND_EARC

### com/android/tv/settings/MainSettings.java

Source lines: 14

### com/android/tv/settings/uicustom/MainActivity.java

Source lines: 491
- 58: onReceive; refs android.content.Context,android.content.Intent
- 107: registerReceiver; refs registerReceiver,this.mBroadcastReceiver
- 111: onCreate; refs android.os.Bundle
- 112: onCreate; refs 
- 189: android.settings.SETTINGS; refs android.settings.SETTINGS
- 293: onKeyDown; refs android.view.KeyEvent,keyEvent,onKeyDown
- 341: onKeyDown; refs android.util.Log.i,onKeyDown,previousFocus
- 348: onKeyDown; refs keyEvent,super.onKeyDown

## KuSetupWizard


### com/my/settings/wifi/ProvisionWifiActivity.java

Source lines: 622
- 54: onReceive; refs android.content.Context,android.content.Intent
- 73: onCreate; refs android.os.Bundle
- 74: onCreate; refs 
- 88: getKeyCode; refs event.getKeyCode
- 300: getSystemService; refs android.net.ConnectivityManager,ctx.getSystemService
- 358: Settings.Global; refs android.provider.Settings.Global.getInt,wifiScanningMode,wifi_scan_always_enabled
- 389: getSystemService; refs android.app.admin.DevicePolicyManager,context.getSystemService
- 406: Settings.Global; refs android.provider.Settings.Global.getInt,wifi_device_owner_configs_lockdown
- 606: registerReceiver; refs registerReceiver,this.wifiReceiver

### com/my/utils/IntentUtils.java

Source lines: 272
- 19: startActivity; refs 
- 24: startActivity; refs 
- 116: startActivity; refs 
- 121: startActivity; refs 
- 126: startActivity; refs 
- 131: startActivity; refs 
- 150: setAction; refs 
- 153: startActivity; refs 
- 167: setAction; refs 
- 171: startActivity; refs 
- 188: startActivity; refs 
- 194: startActivity; refs 
- 206: setComponent; refs android.content.ComponentName
- 208: startActivity; refs 
- 227: getSystemService; refs android.app.ActivityManager,context.getSystemService
- 238: startService; refs context.startService
- 256: getSystemService; refs android.app.ActivityManager,context.getSystemService
- 268: setComponent; refs android.content.ComponentName,com.coolux.source,com.coolux.source.service.TimeService
- 269: startService; refs context.startService

## trdservice


### com/trd/service/communication/GlobalKeyEventProcess.java

Source lines: 141
- 41: getSystemService; refs android.app.ActivityManager,android.app.ActivityManager.RunningTaskInfo,context.getSystemService
- 52: SystemProperties.get; refs android.os.SystemProperties.get,persist.trd.machine,trd
- 110: setComponent; refs android.content.ComponentName,com.trd.factory,com.trd.factory.SplashActivity
- 112: startActivity; refs 
- 118: setComponent; refs android.content.ComponentName,com.trd.projector.settings,com.trd.projector.settings.MainSettingsActivity
- 120: startActivity; refs 
- 126: setComponent; refs android.content.ComponentName,com.mediatek.wwtv.tvcenter,com.mediatek.wwtv.tvcenter.nav.inputpanel.InputsPanelActivity
- 128: startActivity; refs 
- 133: setComponent; refs android.content.ComponentName,com.android.tv.settings,com.android.tv.settings.device.storage.ResetActivity
- 135: startActivity; refs 
- 139: SystemProperties.get; refs android.os.SystemProperties.get,service.trd.age.mode

### com/trd/service/TrdService.java

Source lines: 348
- 79: onReceive; refs android.content.Context,android.content.Intent
- 100: onReceive; refs android.content.Context,android.content.Intent
- 115: onReceive; refs android.content.Context,android.content.Intent
- 148: onCreate; refs 
- 149: onCreate; refs 
- 172: onCreate; refs 
- 178: onCreate; refs 
- 190: registerReceiver; refs registerReceiver,this.mNetworkReceiver
- 200: SystemProperties.get; refs android.os.SystemProperties.get
- 204: getSystemService; refs android.net.ConnectivityManager,android.net.NetworkInfo,getSystemService
- 222: setComponent; refs android.content.ComponentName,com.rjpj.yunota.OTACheckService
- 224: startService; refs mContext.startService
- 225: SystemProperties.set; refs android.os.SystemProperties.set
- 237: onStartCommand; refs android.content.Intent
- 283: setComponent; refs android.content.ComponentName,com.rjpj.tcorrection.TCorrectionBroadcastReceiver
- 286: sendBroadcast; refs 
- 297: SystemProperties.set; refs android.os.SystemProperties.set
- 307: SystemProperties.set; refs android.os.SystemProperties.set
- 315: onCreate; refs 
- 319: SystemProperties.set; refs android.os.SystemProperties.set,persist.rjpj.projector.mode
- 321: SystemProperties.set; refs android.os.SystemProperties.set,persist.rjpj.projector.mode
- 323: SystemProperties.set; refs android.os.SystemProperties.set,persist.rjpj.projector.mode
- 325: SystemProperties.set; refs android.os.SystemProperties.set,persist.rjpj.projector.mode
- 327: SystemProperties.set; refs android.os.SystemProperties.set,persist.rjpj.projector.mode
- 336: onCreate; refs 
- 338: Settings.Secure; refs android.provider.Settings.Secure.getInt
- 339: Settings.Secure; refs android.provider.Settings.Secure.putInt
- 341: Settings.Secure; refs android.provider.Settings.Secure.getInt
- 342: Settings.Secure; refs android.provider.Settings.Secure.putInt

## Решения до полного удаления

1. Использовать явный FLauncher shortcut на \`com.android.tv.settings/.MainSettings\`. Не полагаться на ACTION_SETTINGS, потому что этот Intent объявлен в KuSettings.
2. Нельзя автоматически удалять \`KuSettings\`, пока \`BootupReceiver\` и \`ScreenServices\` не проверены по фактическим веткам вызова.
3. Проверить индивидуальные preferences/global settings и linked service lifecycle после reboot/sleep.
4. Подписи всех основных проверенных OEM и AOSP приложений соответствуют AOSP platform test certificate — см. соседний SETTINGS_DISPATCH_8052_RU.md; это **не** AVB signing key.
5. Указанные методы и Java-классы совпадают для 8052 Oct и заводской 8054 Sep, если APK SHA совпадает; реально работающая 8054.1.0.4 ещё не изучена.

