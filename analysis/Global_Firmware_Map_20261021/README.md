# Глобальная карта будущей RUIOS Custom для 8052/8054 — 21 октября 2026

Цель: **один общий набор изменений на двух разных оригинальных стоковых базах**. FLauncher — выбранный HOME; отдельные `zxstore` и `zxlauncher` будут исключены, `KuSettings` — после переноса его функций в `TvSettingsPlus`. Hardware HAL/TRD/TV services остаются штатными, если не обнаружен подтверждённый дефект. Никаких изменений в оригинальных образах в ходе этой работы не выполнялось.

## Отчёты по порядку использования

1. [**GLOBAL_COMPONENT_ARCHITECTURE_RU.md**](GLOBAL_COMPONENT_ARCHITECTURE_RU.md) — полная схема зависимостей Android / MediaTek / OEM / TV Linux и карта сохранения компонентов для каждой ревизии.
2. [**APK_ALL_PACKAGES_RU.md**](APK_ALL_PACKAGES_RU.md) — 89 APK из объединённого каталога заводских образов с решениями KEEP / REPLACE / MIGRATE / OPTIONAL.
3. [**SETTINGS_FUNCTION_GAPS_RU.md**](SETTINGS_FUNCTION_GAPS_RU.md) — карта Android TV Settings и OEM экранов: что уже реализовано как код, какие функции нужно открыть, перенести, проверить.
4. [**UNRESOLVED_AUDIT_GATES_RU.md**](UNRESOLVED_AUDIT_GATES_RU.md) — полный реестр оставшихся вопросов и условий, при которых можно безопасно начинать редактирование.
5. [**OTA8052_INIT_PERMISSIONS_KEYLAYOUT_RU.md**](OTA8052_INIT_PERMISSIONS_KEYLAYOUT_RU.md) — новый статический аудит оригинальных `init.rc`, privilege XML, всех APK и раскладок пульта из октябрьской OTA 8052 (генерируется GitHub Actions).
6. Машинные данные: [apk_all_packages.json](apk_all_packages.json), [ota8052_init_permissions_keylayout.json](ota8052_init_permissions_keylayout.json).

## Короткие инженерные решения

| Категория | Статус |
|---|---|
| **Общий UI** | FLauncher, будущие патчи TvSettingsPlus, штатные входы в OEM HDMI/Focus |
| **Общий неизменный OEM код** | Там, где идентичные APK и они доказанно работают на обеих ревизиях, не нужно держать две независимые версии кода патчей |
| **Сохранить оригинал каждой платы** | boot/kernel/DTBO/vbmeta, tvconfig/PMU/gamma, TV Linux, vendor, HAL, firmware, RuiAutoFocus до установления причины diff |
| **Потенциальные удаления после тестов** | zxlauncher, zxstore, KuSettings после миграции; возможные demo/предустановки после явной проверки |
| **Не удалять по названию** | PackageInstaller, AutoPair, TvProvider, SystemUI, TvServices, input, OEM hardware TRD, firmware и первое включение |
| **Не блокирует первый UI этап** | Пока неподтверждённые Wi-Fi/LAN жалобы, перенос Lumen/Google TV, новая Linux/AOSP база |
| **Блокирует прошиваемый релиз** | Подтверждённый recovery/rollback, подписи и физическая идентификация платы, реальный тест на обеих ревизиях |

## Что значит «полностью исследовано»

Для каждого изменяемого компонента нужно иметь:
- назначение, путь, SHA-256, версию, аппаратную специфику и факт реального использования;
- входящие/исходящие Intent/Binder/HAL и необходимые разрешения;
- сохранённые настройки, startup/sleep/reboot и условия первой загрузки;
- классификацию отличий по четырём причинам (hardware / software release / data/build / unresolved);
- сценарий регрессионного теста на 8052 и 8054 и возможность вернуть сток.

**Глобальная карта — это ещё не полный динамический анализ всей системы.** Она определяет, какие операции имеют высокий риск и чего именно не хватает в исследовании.

## Источники предшествующих работ

- [Stock-custom architecture](../Stock_Custom_Architecture_20261021/README.md)
- [Последняя 8052 vs factory 8054](../Latest_8052_OTA_vs_8054_Stock/README.md)
- [Нативные ELF и OEM-приложения](../Deep_Stock_Audit_20261021/README.md)
- [Первичный полный factory audit](../Full_Audit/README.md)
- [Оригинальные OEM API](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/blob/research-oem-settings-api-20261020/analysis/OEM_API_8052_Latest/IMPLEMENTATION_RU.md)

**Версии:** подтверждённые офлайн-образы для прямого сравнения — **8052.1.0.4** (октябрь OTA) и **8054.1.0.1** (сентябрь PKG). Заявленная версия 8054.1.0.4 на устройстве владельца пока не подтверждена оригинальным образом для побайтового diff.
