# CineLux Custom v0 — два проверяемых Android-overlay комплекта, пока БЕЗ прошивки

**Статус:** сборка APK завершена, подготовка двух staging-архивов выполняется GitHub Actions. Промежуточные пакеты **не предназначены для прошивки, установки поверх системы или обработки реальным update_engine**.

## Исходные профили

| Профиль | Доказанный исходный образ | APK-слои, которые изменяются в staging | Низкоуровневые образы |
|---|---|---|---|
| `8052` 1×HDMI | OTA `RUIOS.8052.1.0.4` (октябрь, проверенный SHA) | Только `system` overlay | Нет, без изменений |
| `8054` 2×HDMI, ToF | factory `RUIOS.8054.1.0.1` (сентябрь, PKG из архива с проверкой SHA) | Только `system_a` overlay | Нет, без изменений |

Не имеется проверенного полного оригинального образа `8054.1.0.4`. Не выдавать factory `1.0.1` за более позднюю ревизию. Когда будет получен дамп/официальный ZIP именно актуального 8054, изменения переосновать на него.

## Что реально собирается

Общие APK:
- Оригинальный **FLauncher 0.18.0** из [официального релиза](https://gitlab.com/flauncher/flauncher/-/releases/0.18.0/downloads/flauncher-0.18.0.apk), пакет `me.efesser.flauncher`. Зафиксирован **SHA256 оригинального GitLab файла `376fc528c880cdf7c7c04b2d3708c69f911144498218babb6300808b772af32e`**, не хеш зеркала/перепаковки.
- Свой `org.cinelux.settingsshortcut` — простой Android Java Activity без root/privileged permissions; запускает **явно `com.android.tv.settings/.MainSettings`**, не implicit `android.settings.SETTINGS` (который в RUIOS резолвится к `KuSettings`). Подпись ярлыка пока ephemeral sandbox/dev, при релизе потребуется стабильный ключ и обновления подписи.

Подготовленные удаления для обоих Android системных профилей:
- `zxlauncher.apk` — вместо него FLauncher. Учтён риск отсутствия fallback HOME, поэтому до ADB и проверок не применять.
- `zxstore.apk` — только OEM магазин, **не** Android `PackageInstaller`.

Только factory 8054:
- `system/preinstall_del/Netfix_v8.110.0.apk` — удалить;
- `system/preinstall_del/AmazonPrimeVideo_v3.0.459.345.apk` — удалить;
- `system/preinstall_del/YouTube_v4.40.313.apk.apk` — оставить.

В октябрьской OTA 8052 эти три APK не найдены. Это не значит, что их нет в `/data/app` у владельца, и не означает, что OTA убрала их из текущей прошивки, если разделы не обновлялись.

## Чего НЕ делаем

- `KuSetupWizard` — **оставляем** как механизм первичной настройки; никогда не удалять на этом этапе.
- `KuSettings` — **пока сохраняем**: `ScreenServices`, `MySetTimeService`, boot receiver, функции скриншота и косвенные зависимости setup ещё не признаны удаляемыми. Отдельную OEM Activity не используем для кнопки «Настройки».
- `TvSettingsPlus` — оставляем **байт-в-байт оригинальный**, не перекомпилируем до переноса функций (будет следующий этап). В наличии export `uicustom.MainActivity` (проекторное OEM меню внутри APK), реальный запуск не протестирован.
- `trdservice`, `trdmiddle`, `RuiAutoFocus`, `KeystoneCorrection`, `KuSourceRJ`, `RuiYunOta`, `AutoPair`, `Factory`, `PackageInstaller` и AOSP TV framework — оставить.
- boot, kernel, vendor, TVservice, DTBO, PMU, gamma, persist/factory calibration, vbmeta — не изменять и не включать в ZIP.
- НЕ собираем `update.pkg`, `bin`, `payload.bin`, `super.img` или даже экспериментально перепакованный `system.img`, поскольку не подтверждены SELinux metadata, UID/GID, EROFS layout, AVB и безопасный rollback.

## Результат двух jobs

Каждая успешная job `custom-v0-stage-overlay.yml` публикует отдельный artifact:
- `cinelux-custom-v0-8052-NONFLASHABLE`;
- `cinelux-custom-v0-8054-NONFLASHABLE`.

Внутри staging ZIP:
- `overlay/system/app/FLauncher/FLauncher.apk`;
- `overlay/system/app/CineLuxSettingsShortcut/CineLuxSettingsShortcut.apk`;
- `manifest.json` с точными SHA входных stock APK, состоянием сохранения/удаления;
- `REMOVALS.txt`;
- `README_NOT_FLASHABLE_RU.txt`.

**ZIP не нужно распаковывать на устройство в /system и нельзя передавать в OTA updater.** Это артефакт сборки и проверка состава, а не готовая прошивка.

## До реальных разделов и установки

1. Получить заказанный ADB отчёт и определить bootloader, AVB, активные logical partitions, актуальную версию 8054, реальную отработку first boot.
2. Проверить на живом устройстве `adb shell am start -n com.android.tv.settings/.MainSettings` и по возможности `adb shell am start -n com.android.tv.settings/.uicustom.MainActivity`.
3. На действующем стоке проверить FLauncher/ярлык/TV Settings из `/data/app`, HOME fallback, D-pad, YouTube, HDMI1/2, сеть, OTA, первый запуск, сон/пробуждение.
4. Проверить особенности подписанного официального FLauncher APK как **system app**, его native lib compression / `extractNativeLibs`. Наличие apk в overlay не гарантирует загрузку Flutter на конкретной плате без дополнительной установки/перепаковки.
5. Лишь после подтверждённого rollback/AVB/signer/SELinux — выполнять модификацию реальных `system[_a]` образов и генерировать инсталляционный контейнер.

## Официальные источники
- [FLauncher original source GPL-3.0](https://gitlab.com/flauncher/flauncher)
- [Исследование Settings и очистки](../analysis/Settings_Wizard_Debloat_20261021/README.md)
- [Инвентаризация OEM](../analysis/Global_Firmware_Map_20261021/README.md)

**Примечание о приватности:** в staging ZIP не включаются userdata, ключи, factory/calibration, личные данные и бинарники vendor. Только два конкретных APK плюс хеши original files.
