# Почему открывается OEM Settings вместо Android TV Settings — установленная причина

**Статус:** причина для стандартного implicit Intent `android.settings.SETTINGS` **выявлена статически**. Фактические `pm resolve-activity` и `am start` на физическом проекторе пока не проверены. Источник: оригинальная OTA `RUIOS.8052.1.0.4`, проверенная SHA256; соответствующие APK **побайтно идентичны** в заводской `8054.1.0.1`.

## Оригинальные системные Activity

| Приложение / компонент | Оригинальные действия и категории | Вывод |
|---|---|---|
| `com.my.settings/.SettingActivity` (`KuSettings`) | **action `android.settings.SETTINGS`**, `MAIN`; `DEFAULT` + `LAUNCHER`; `exported=true` | Объявлен обработчиком стандартного implicit Settings Intent, виден обычному launcher |
| `com.android.tv.settings/.MainSettings` (`TvSettingsPlus`) | action `MAIN`; `LEANBACK_SETTINGS`, `LEANBACK_LAUNCHER`; `exported=true` | Основной Android TV Settings; нет зафиксированного standard `ACTION_SETTINGS` на этой Activity |
| `com.android.tv.settings/.uicustom.MainActivity` | `android.settings.RJ_SETTINGS`, `android.settings.PICTURE_SETTINGS`, `android.settings.SOUND_SETTINGS`; `DEFAULT`, `exported=true` | OEM/Projector UI внутри того же TvSettingsPlus APK — не путать с MainSettings |
| `com.zeasn.launcher.ui.MainActivity` | `MAIN` / `HOME`, `DEFAULT`, `LAUNCHER`, `LEANBACK_LAUNCHER` | Заводской HOME; `TvSetting` / `AppUtil` у ZEASN формируют `android.settings.SETTINGS` |
| `com.android.tv.settings.device.storage.ResetActivity` | Используется в явных ссылках `trdservice.GlobalKeyEventProcess` | Важно: это Reset/Storage, не основная Android TV Settings |
| `com.trd.projector.settings.MainSettingsActivity` | Строковый кандидат в TRD service; соответствующий APK/target в текущей OTA не установлен по одному литералу | Не считать установленной альтернативой MainSettings |

**Наиболее вероятная фактическая последовательность на штатной системе:** кнопка «Настройки» в ZEASN → `Intent(android.settings.SETTINGS)` → `KuSettings.SettingActivity`. Эта цепь соответствует и исходным манифестам, и найденному Java-вызову. Однако выбор resolver (включая приоритеты/изменения в `/data`) ещё предстоит проверить.

Это **не** означает, что `TvSettingsPlus` удалён или скрыт от Android: `MainSettings` экспортируется, но использует телевизионную категорию `LEANBACK_SETTINGS`, а не обычный стандартный `LAUNCHER`.

## Простое решение в кастоме с FLauncher

**Не нужно менять штатный TvSettingsPlus APK только ради ярлыка.**

Способ A: если выбранный FLauncher поддерживает действие/ярлык с ComponentName, настроить точный компонент

```text
package = com.android.tv.settings
class   = com.android.tv.settings.MainSettings
action  = android.intent.action.MAIN
```

Способ B (если FLauncher не показывает этот системный пакет или не позволяет создавать кастомные ярлыки): сделать крошечный **обычный SettingsShortcut.apk** с `MAIN`+`LEANBACK_LAUNCHER`; при клике он явно запускает `ComponentName("com.android.tv.settings", "com.android.tv.settings.MainSettings")`. Для ярлыка нет оснований требовать platform signature: вызываемый MainSettings `exported=true`, не обнаружено per-activity permission; проверка на реальном устройстве обязательна. Shortcut APK можно подписать **отдельным собственным ключом** и не модифицировать TvSettingsPlus. В launcher будет отдельный «Android TV Settings».

**Неразрушающая проба по ADB** (после успешного ADB подключения; без root):

```sh
adb shell am start -n com.android.tv.settings/.MainSettings
```

И дополнительная read-only проверка:

```sh
adb shell cmd package resolve-activity --brief -a android.settings.SETTINGS
adb shell dumpsys package com.android.tv.settings
adb shell dumpsys package com.my.settings
```

Вторая/третья команды выводят большой дамп: при публикации обезличить идентификаторы. Для проверки можно ограничиться relevant activity резолвером. Для удаления KuSettings этого теста **недостаточно** (см. BootupReceiver ниже).

## Крайне существенное отличие: Key для APK найден

Через `apksigner verify --print-certs` извлечён signer certificate SHA256:
`C8A2E9BCCF597C2FB6DC66BEE293FC13F2FC47EC77BC6B2B0D52C11F51192AB8`.

**Одинаковый fingerprint** у:
- TvSettingsPlus, KuSettings, trdservice, zxlauncher;
- RuiAutoFocus, KuSetupWizard, KeystoneCorrection, KuSourceRJ, RuiYunOta;
- SystemUI, SettingsProvider.

Fingerprint — **AOSP platform test certificate**, открытый тестовый ключ доступен в исходниках Android:
- AOSP `platform.x509.pem` (этот сертификат соответствует наблюдаемому hash);
- AOSP `platform.pk8` — приватная часть публичного тестового ключа. Это не секрет OEM.

Это даёт **практический путь пересборки и повторной подписи системного TvSettingsPlus** под той же cert identity, если будут нужны функциональные изменения. Но:
1. сначала подтвердить `sharedUserId`, privapp whitelist, signer identity на живом устройстве и схемы v1/v2/v3 при переподписи;
2. ресурсные package splits, обновления в `/data`, platform key signature могут иметь дополнительные ограничения;
3. **AVB RSA-4096 image signing — другой ключ**: тестовый AOSP platform.pk8 не позволяет прошить изменённый system/vendor на проверяющем загрузчике;
4. ключ AOSP test является **публичным и не предназначен для безопасного production trust**; нельзя выдавать его за защищённый заводской ключ или использовать для доказательства device security.

Источник fingerprint: [SETTINGS_DISPATCH_8052_RU.md](SETTINGS_DISPATCH_8052_RU.md). Публичное AOSP определение fingerprint: https://gitlab.com/fdroid/fdroiddata/-/blob/HEAD/config.yml (AOSP platform.x509.pem).

## Перед удалением KuSettings проверяем фоновую роль

`KuSettings` содержит `com.my.service.BootupReceiver` с `android.intent.action.BOOT_COMPLETED`.
У `TvSettingsPlus` свои независимые `BootReceiver`, `TvBootupReceiver`, `SoundEARCReceiver`.

**Поэтому удаление KuSettings до выяснения, какие эффекты вызывает его boot receiver и `ScreenServices`, потенциально опасно.** Отдельный статический аудит этих обработчиков запущен. Также `KuSetupWizard` имеет отдельный `com.android.provision` и ссылки на `com.my.settings`, несмотря на 99,39% сходства Java-кода.

## Почему задача одна для 8052/8054

В проверенных сравниваемых образах `TvSettingsPlus`, `KuSettings` и `trdservice` **байт в байт одинаковы**. Значит их manifest exported/action/категории и signer одинаковы. Различия стартового поведения всё ещё могут возникать от `/data` package state/приоритетов/оверлеев и разных версий лаунчера.

Нет доступного полного образа более новой 8054.1.0.4. Публичный индекс `.../8054/8054_ota.json` на момент проверки 21.10.2026 вернул HTTP 404. Без реального дампа нельзя утверждать, что её компоненты совпадают с 8054.1.0.1.

## Итог

**Проблема появления заводских настроек по стандартному Intent доказуема уже сейчас; первичный Fix — явный запуск `TvSettingsPlus.MainSettings`, без вмешательства в драйверы и без обязательной пересборки системного APK.**

**Изменение функциональности TvSettingsPlus** — отдельный следующий этап: с общим тестовым AOSP platform key это технически намного реалистичнее, но bootloader/AVB и user runtime нужно исследовать независимо.
