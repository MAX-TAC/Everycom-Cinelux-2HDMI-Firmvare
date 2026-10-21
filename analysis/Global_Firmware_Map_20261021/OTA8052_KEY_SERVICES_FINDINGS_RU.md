# Новые факты из октябрьской OTA 8052: init.rc, аппаратные службы, пульт и права

Источник: [OTA8052_INIT_PERMISSIONS_KEYLAYOUT_RU.md](OTA8052_INIT_PERMISSIONS_KEYLAYOUT_RU.md), [JSON](ota8052_init_permissions_keylayout.json), GitHub Actions 39608516488. Оригинальный `RJMT9660_firmware_8052.zip` проверен SHA256, разделы readonly распакованы, сервисы не запускались.

## Подтверждённый масштаб

- **85 путей APK** в оригинальных Android-разделах октябрьской OTA 8052. В двух старых заводских образах 89 уникальных factory-путей в объединении; это **разные выборки**, и их количества не следует считать ошибкой.
- **36** отдельных упоминаний hardware/platform/OEM услуг в `init*.rc` (это *отфильтрованное* подмножество всех init services).
- **179** файлов `.kl` (большинство общесистемных, не обязательно относящихся к комплектному пульту).
- **13** проверенных XML declaration blocks для OEM/MTK привилегированных приложений.
- **3** vendor RRO overlay APK для Wi-Fi и tethering.

## Почему это существенно для кастома

### 1. TRD и TV services запускаются из init, а не из лаунчера

В `system/init.trd.rc` обнаружены:
- `trd_boot` → `/system/bin/sh`;
- `trd_module_loader` → `/vendor/bin/trd_module_loader.sh`.

В `vendor/etc/init/` зарегистрированы `dtv-svc`, `factory_svc`, `tv-mtktvapi-1-0`, `tv-mtktvfactory-1-0`, `tv-mtkcalman-1-0`, `tv-input-1-0`, `vendor.hwtrd-1-0`, `vendor.tof-hal-1-0`, `vendor.cec-hal-1-0`, `vendor.audio-hal`, `vendor.thermal-hal-2-0-mock`, `vendor.wifi_hal_legacy` и другие.

**Вывод:** удаление `zxlauncher` само по себе не равно отключению аппаратного слоя. Но эти init службы и соответствующие `vendor`/factory разделы следует оставить штатными, а их зависимости и порядок запуска подробно проверить до перепаковки.

Название `vendor.thermal-hal-2-0-mock` **не означает**, что в проекторе отсутствует настоящая защита от перегрева: необходимо анализировать реализацию и другие аппаратные уровни. Не менять thermal/power control без доказательств.

### 2. Отдельный пульт, отдельные проекторные KeyEvents

Файл `vendor/usr/keylayout/Vendor_3697_Product_0001.kl` содержит:

| Key scan code | Android key | Назначение (по имени) |
|---|---|---|
| 528 | FOCUS | фокус |
| 744 | FOCUS_PLUS | увеличение шага фокуса |
| 745 | FOCUS_MINUS | уменьшение шага фокуса |
| 747 | TRD_POPMENU | проекторное pop-menu / возможно OEM Settings |
| 751 | FOCUS_RESET | сброс фокуса |
| 755 | SOURCE | источник сигнала |
| 139 | MENU | стандартное меню |
| 102 | HOME | главный экран |
| 79 | TV_INPUT | TV input |

**Это статическая карта событий, а не факт**, что комплектный пульт использует именно USB/HID ID `3697:0001` или что `TRD_POPMENU` открывает текущий KuSettings. Нужно проверить VID/PID выбранного устройства и реальные `getevent` на 8052 и 8054, либо другое неразрушающее наблюдение.

**Приоритетная цепочка:** `key 747 TRD_POPMENU` / `key 139 MENU` → `InputManager` → `trdservice.GlobalKeyEventProcess` → Intent Activity. Если подтвердится, перенаправить **только кнопку настроек** к `com.android.tv.settings`, не меняя FOCUS/SOURCE.

### 3. Android TV Settings требует штатного privilege set

`system_ext/etc/permissions/privapp-permissions-mediatek.xml` содержит для `com.android.tv.settings` **20 указанных разрешений**, включая `WRITE_SECURE_SETTINGS`, `BLUETOOTH_PRIVILEGED`, `TV_INPUT_HARDWARE`, `REBOOT`, `WRITE_EPG_DATA`, `MANAGE_USERS`, `FORCE_STOP_PACKAGES` и `START_ACTIVITIES_FROM_BACKGROUND`.

Это не гарантия, что каждое из них реально предоставлено на работающем устройстве — это whitelist/request declarations. Но заменять `TvSettingsPlus` произвольным APK с новой подписью без проверки platform signature/shared UID/privapp policy и SELinux **опасно**: UI может установиться и при этом потерять аппаратные функции.

Также найдены отдельные декларации `com.mediatek.hotkey.dispatcher`, `com.mediatek.tv.service`, `com.mediatek.tvinput` и др. XML запись **не доказывает**, что пакет реально установлен или запущен.

### 4. Wi-Fi не обязательно зависит только от драйвера

В vendor overlay APK:
- `WifiRROOverlay.apk`;
- `TetheringInprocessRROOverlay.apk`;
- `TetheringRROOverlay.apk`.

Это ещё один повод не приписывать неподтверждённую скорость WLAN одному `wlan_mt7663.ko`: на связь влияют policy и ресурсные конфигурации. Содержимое overlay и их активное состояние ещё отдельно требуется проверить. Пользователь решил пока отложить проблемы WLAN/LAN.

## Что нужно исследовать после этого сканирования

1. В `init.trd.rc` проверить условия `on property:`, запуск `trd_boot`, драйверный loader, зависимость от package launcher и TV service.
2. Разобрать `GlobalKeyEventProcess`: реальные обработчики `TRD_POPMENU`/`MENU`/`SOURCE`, какие Intent пересылаются, как обработать отсутствие старого KuSettings.
3. Проверить какая именно keylayout выбирается для штатного пульта; при необходимости сравнить keymaps в 8054.
4. Разобрать `TvSettingsPlus` privilege model и безопасный способ изменения UI с сохранением исходного набора прав.
5. Проверить, какие приложения OEM действительно содержат boot receivers и кто запускает их после boot.
6. Для RRO overlay — ограничиться read-only описанием до выяснения сетевых/TV зависимостей.
7. Не пытаться удалить TRD/TOF/Factory/MTK службы, даже если их непосредственный пользовательский UI заменяется.

## Степень уверенности

| Факт | Уверенность |
|---|---|
| Файлы и объявленные services/permissions в оригинальной OTA | Высокая, SHA-verified |
| `TRD_POPMENU` является собственным Android key symbol | Высокая, виден в .kl |
| Кнопка Settings на физическом пульте вызывает `TRD_POPMENU` | Пока не установлено |
| `TRD_POPMENU` приводит к `KuSettings` | Пока не установлено |
| Замена `TvSettingsPlus` не нарушит grants | Пока не установлено |
