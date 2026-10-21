# Очистка RUIOS 8052 / 8054: оставить YouTube, удалить Netflix, Prime Video и ZEASN

**Дата:** 2026-10-21. **Статус:** проектное решение и подтверждённый **список путей APK** из исходных образов. **Ничего из образов не удалено.**

## Принятая политика

- Единый домашний экран: **FLauncher**. Удаляем заводской `zxlauncher` только после готовности нового HOME.
- Удаляем **`zxstore`** и его рекламу/каталог, сохраняя системный Android `PackageInstaller`.
- Убираем **Netflix** и **Amazon Prime Video** из будущих образов, включая механизм их factory preinstall. **YouTube оставляем**.
- Убираем графическую оболочку `KuSettings` после подтверждения, что её системные функции покрыты `TvSettingsPlus` или оставленными аппаратными службами.
- Не трогаем Android 13 `APEX`, system `priv-app`, TV HAL, MediaTek, TRD, Bluetooth, пульт, `KuSetupWizard`/Provision, OTA, FallbackHome, не проверив индивидуально.
- Дополнительно рассматриваем удаление необязательных демо/мультимедиа/каст-сервисов, но **не приравниваем их к Netflix или Prime без проверки функций**.

## Конкретные находки в оригинальных файлах

| Программа | Найдено в original factory 8054.1.0.1 | В актуальной OTA 8052.1.0.4 | Будущий статус |
|---|---|---|---|
| Netflix (в архиве имя с опечаткой `Netfix`) | `system_a/system/preinstall_del/Netfix_v8.110.0.apk` | **Не найдено** среди 85 APK OTA | Удалить из preinstall, не включать в сборку |
| Prime Video | `system_a/system/preinstall_del/AmazonPrimeVideo_v3.0.459.345.apk` | **Не найдено** среди 85 APK OTA | Удалить |
| YouTube | `system_a/system/preinstall_del/YouTube_v4.40.313.apk.apk` | **Не найдено** среди 85 APK OTA | **Сохранить**, не удалять |
| ZEASN `zxlauncher` | `system_a/system/app/zxlauncher/zxlauncher.apk` | `system/system/app/zxlauncher/zxlauncher.apk` | Заменить FLauncher |
| ZEASN `zxstore` | `system_a/system/app/zxstore/zxstore.apk` | `system/system/app/zxstore/zxstore.apk` | Удалить |
| `KuSettings` | `system_a/system/app/KuSettings/KuSettings.apk` | `system/system/app/KuSettings/KuSettings.apk` | Перенос интерфейса, удалить после тестов |

**Ограничение:** отсутствие YouTube/Netflix/Prime в Android OTA `8052.1.0.4` не означает отсутствие ранее установленных копий на живом устройстве в `/data/app` и не доказывает отсутствие их в старом базовом разделе, если OTA обновляет не все разделы. Проверка `pm list packages` остаётся обязательной.

**Важно:** `preinstall_del` обычно отражает механику поставки/предустановки приложений в пользовательский раздел. Даже если исключить APK из будущего образа, уже установленный пакет в `/data/app` может сохраниться без отдельного механизма очистки. **Не добавлять принудительную очистку `/data` или factory reset.** Механизм preinstall в этой прошивке требует подтверждения.

## Дополнительные кандидаты по заводскому inventory

| Пакет | Пока принято |
|---|---|
| `FTAirplayWireless` | Проверить, не требуется ли пользователю AirPlay/кастинг; при желании удалить отдельно |
| `WFDSinkTest` | Возможная тестовая Miracast-служба — нужна проверка, влияет ли на приемное дублирование |
| `RetailDisplay` | Проверить реальное назначение kiosk/demo |
| `TrdDreamPic` | Проверить заставку/idle, может использоваться OEM |
| `VendorDisclaimer` | Проверить связи с первичным SetupWizard/legal |
| `RJBluetoothSpeaker` | Кандидат на удаление BT A2DP Sink; проверить не влияет ли на BT output и пульт |
| `AdServicesApk` (Android APEX) | **Не трогать сейчас:** это Android system module, не ZEASN реклама |
| `Camera2`, `TvServices`, `MtkTvInput`, `PackageInstaller`, `AutoPair` | **Сохранить:** возможные системные и аппаратные зависимости |

## Проверки перед исключением

- Подтвердить точные package names и сертификаты Netflix/Prime/YouTube, чтобы удалить именно нужные приложения.
- Проверить список предустановки в 8054 и реальные APK/user packages на 8052; две ревизии могут отличаться.
- Проверить стандартный установщик приложений после удаления `zxstore`.
- FLauncher должен запускаться и восстанавливаться после reboot/standby, иначе возможен blank HOME.
- Не удалять OTA (`RuiYunOta`), `TvSettingsPlus`, `KuSourceRJ`, `trdservice`, `trdmiddle`, `RuiAutoFocus` или `Provision` в рамках очистки.

## Ссылки

- [Инвентаризация 89 factory APK](../Global_Firmware_Map_20261021/APK_ALL_PACKAGES_RU.md)
- [Актуальная OTA 8052, 85 APK](../Global_Firmware_Map_20261021/OTA8052_INIT_PERMISSIONS_KEYLAYOUT_RU.md)
- [Global architecture](../Global_Firmware_Map_20261021/GLOBAL_COMPONENT_ARCHITECTURE_RU.md)
