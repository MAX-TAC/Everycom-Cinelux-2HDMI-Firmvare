# Сводка нового аудита 21 октября 2026: маршрутизация настроек, подписи, автозапуск

**Источники**:
- исходная проверенная OTA `RUIOS.8052.1.0.4`;
- оригинальная заводская `RUIOS.8054.1.0.1` (APK/DEX diff из ранних аудитов);
- официальный public OTA index 8052 (HTTP 200) и 8054 (HTTP 404 на дату проверки);
- GitHub Actions 39611564480 (APK manifests and signatures), 39611875380 (OTA index), 39612636685 (boot receivers).

Все изменения ниже — документация и read-only сканирование, **не модификация прошивки**.

## 1. Причина OEM Settings через стандартный Intent

### Подтверждённый манифест
- `com.my.settings/.SettingActivity` (`KuSettings`) зарегистрирован для `android.settings.SETTINGS` и `MAIN/LAUNCHER`, `exported=true`.
- `com.android.tv.settings/.MainSettings` (`TvSettingsPlus`) зарегистрирован для `MAIN/LEANBACK_SETTINGS` и `LEANBACK_LAUNCHER`, `exported=true`; прямого `android.settings.SETTINGS` в его фильтре нет.
- `com.android.tv.settings/.uicustom.MainActivity` также существует; её действия `android.settings.RJ_SETTINGS`, `PICTURE_SETTINGS`, `SOUND_SETTINGS`. Это **отдельный OEM экран внутри Android TV Settings APK**.
- `zxlauncher` `com.zeasn.utils.TvSetting` и `AppUtil` формируют `Intent("android.settings.SETTINGS")`. По исходным манифестам этот путь ведёт к OEM KuSettings. **Фактический resolver ещё проверить на реальном устройстве**, учитывая package manager state/пользовательские настройки.
- `trdservice.GlobalKeyEventProcess` содержит явную ссылку к старому `com.trd.projector.settings.MainSettingsActivity`, а явная ссылка на `com.android.tv.settings.device.storage.ResetActivity` — **сброс устройства, не главные настройки**. Это отдельный путь, не надо его путать с нажатием FLauncher shortcut.
- Важная граница: если владелец видит именно проекторное окно `uicustom`, его источник может быть `RJ_SETTINGS` или аппаратное OSD, а не `KuSettings.SettingActivity`. Конкретную foreground Activity подтвердит работающий проектор.

### Решение для первой версии кастома
Сделать **Settings shortcut** на `com.android.tv.settings/.MainSettings` в FLauncher. Если FLauncher не позволяет показывать экспортированную системную Activity, которая не имеет обычной категории `LAUNCHER`, создать отдельный маленький `SettingsShortcut` APK с `MAIN+LEANBACK_LAUNCHER`, который посылает **explicit ComponentName**. Такой shortcut не требует изменений `TvSettingsPlus` или TRD. Проверить на двух ревизиях.

Проверка после ADB:
```sh
adb shell am start -n com.android.tv.settings/.MainSettings
adb shell cmd package resolve-activity --brief -a android.settings.SETTINGS
```

## 2. Проверено: AOSP test platform certificate

Анализатор `apksigner verify --print-certs` выдал **один и тот же сертификат SHA256** `C8A2E9BCCF597C2FB6DC66BEE293FC13F2FC47EC77BC6B2B0D52C11F51192AB8` для:
`TvSettingsPlus`, `KuSettings`, `trdservice`, `zxlauncher`, `RuiAutoFocus`, `KuSetupWizard`, `KeystoneCorrection`, `KuSourceRJ`, `RuiYunOta`, `SystemUI`, `SettingsProvider`.

Он совпадает с публичным **AOSP platform test certificate**, не с общим `testkey.x509.pem`: публичный platform test key pair имеет соответствующий `platform.pk8` в AOSP source. Это означает, что в будущем технически возможно подписать изменённый APK **той же identity**. Следует беречь приватную часть тестового ключа на стороне сборщика, несмотря на его публичность, и понимать риск публичного platform ключа для безопасности устройства.

ОГРАНИЧЕНИЯ: `sharedUserId`, подпись preinstalled replacement, APK signature scheme, priv-app whitelist, разрешения и compatibility требуют тестов; **AVB RSA-4096 подпись образов — другой ключ**. Публичный AOSP platform key не даёт право перепрошивать загрузчик/boot/vbmeta.

## 3. Что выяснено о BOOT_COMPLETED

- `KuSettings`: `com.my.service.BootupReceiver` зарегистрирован на `android.intent.action.BOOT_COMPLETED`. Его Java-код небольшой (17 строк), прямых вызовов `startService` / `startActivity` в стандартном сканировании не найдено. Это **не доказывает отсутствия косвенных эффектов**. Анализ условий внутри onReceive требует ручной проверки.
- `KuSettings.com.my.service.ScreenServices` содержит `SystemProperties.set`, `bindService`, `setClassName` к `com.android.systemui.screenshot.TakeScreenshotService`. Наличие `SystemProperties.set` означает, что этот компонент **потенциально не просто UI**; для удаления установить caller и какие свойства меняются.
- `TvSettingsPlus.BootReceiver` запускает `BluetoothDevicesService`;
- `TvSettingsPlus.partnercustomizer.tvsettingservice.TvBootupReceiver` запускает `WirelessSpeakerServices` (отдельно изучить режим A2DP Sink и не путать с Bluetooth output);
- `TvSettingsPlus.partnercustomizer.utils.SoundEARCReceiver` обращается к `Settings.Global` для eARC.
- `KuSetupWizard` / `com.android.provision` использует собственную точку первичной настройки Wi-Fi, которая не является заменой самого KuSettings при полном удалении APK; есть кросс-пакетные ссылки на `com.my.settings`.
- `trdservice.TrdService` запускает `com.rjpj.yunota.OTACheckService`, обновляет `persist.rjpj.projector.mode` и несколько значений `Settings.Secure`. Эти функции **сохраняем неизменными**.

## 4. Состояние offline исследования обеих ревизий

| Компонент | 8052 Oct 1.0.4 | 8054 Sep 1.0.1 | Вывод |
|---|---|---|---|
| `TvSettingsPlus` | SHA подтверждён | такой же SHA | одна база UI и манифеста |
| `KuSettings` | SHA подтверждён | такой же SHA | одна обработка ACTION_SETTINGS |
| `trdservice` | SHA подтверждён | такой же SHA | одна ветка key dispatch code, но разный runtime возможен |
| `KuSourceRJ`, `KeystoneCorrection` | SHA подтверждён | такой же SHA | сохранять hardware API |
| `RuiAutoFocus` | Есть изменения относительно Sep8054 | другое APK | профильный оригинал до semantic diff ToF |
| `zxlauncher`, `zxstore` | другие OEM сборки | другие OEM сборки | удалять в будущих кастомах; FLauncher общий |
| Устройство с якобы `8054.1.0.4` | нет данных для сравнения | нет официально проверенного образа | не приписывать ему результаты factory .1.0.1 |

Известный индекс `https://www.szrjyun.com/ota/android/mt9660/8054/8054_ota.json` вернул **HTTP 404**. Нельзя доказать, что самая поздняя `8054` вообще доступна по этой ссылке. Возможно, новый OTA канал другой или версия сообщена с ошибкой.

## 5. Классификация к следующему этапу

- **KEEP PER BOARD:** boot, kernel, vendor HAL, tvservice/tvconfig, dtbo, gamma, PMU, индивидуальные калибровки, motor/ToF профили.
- **KEEP COMMON INTERFACE:** `trdservice`, `trdmiddle`, `KuSourceRJ`, `KeystoneCorrection`, `RuiYunOta`, `KuSetupWizard` (при необходимости раздельно сохраняются штатные одинаковые копии).
- **COMMON MODIFICATION:** FLauncher + SettingsShortcut, **без редактирования TvSettingsPlus на первом этапе**.
- **NEXT MODIFICATION:** TvSettingsPlus new menu item/Fragment только при реальном отсутствии OEM функции. После подтверждения целевой подписи AOSP public platform test identity.
- **DELETE after tests:** `zxlauncher`, `zxstore`; `KuSettings` только после аудита BootupReceiver/ScreenServices и полного функционального покрытия.
- **DEFER:** непроверенные Wi-Fi/LAN жалобы; глубокая переделка TV HAL, Tof, мотор; bootloader verification до ADB данных.

## 6. Оставшиеся блокеры полноты

Не было доступа к **фактической 8054.1.0.4**, физическому PackageManager resolver, запущенной Activity, данным состояния/привилегий. Без этого не выдавать глобальный offline audit за полностью воспроизведённое поведение. Первым неразрушающим тестом будет явный запуск `MainSettings` на 8052 и 8054 и проверка текущего resolved implicit ACTION_SETTINGS.

Дополнительные материалы:
- [Манифесты, APK fingerprints, entrypoints](SETTINGS_DISPATCH_8052_RU.md)
- [BOOT_RECEIVER trace](OEM_BOOT_RECEIVER_TRACE_RU.md)
- [Публичные OTA JSON](PUBLIC_8052_8054_OTA_METADATA_RU.md)
- [Глобальная системная карта](GLOBAL_COMPONENT_ARCHITECTURE_RU.md)
