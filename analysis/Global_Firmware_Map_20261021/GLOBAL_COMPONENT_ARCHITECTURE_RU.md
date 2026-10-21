# Глобальная карта Everycom CineLux / FlixTone D11: границы будущих двух RUIOS Custom

**Статус:** инженерная схема, составлена 21.10.2026 по результатам статических исследований оригинальных factory 8052/8054 и OTA 8052.1.0.4. Ничего в образах не менялось. **Не считать полным подтверждением работоспособности на физическом железе.**

**Принято:** один **общий набор пользовательских модификаций** + два **отдельных родных аппаратных baselines**. Целевой HOME — **FLauncher**. Магазин `zxstore` исключить; отдельный экран `KuSettings` заменить возможностями доработанного `TvSettingsPlus` после детального gap analysis. Нативные MediaTek и OEM TRD службы не переписываем «из принципа», исправляем только подтверждённые недостатки.

## 1. Что именно имеется в прошивке — карта зависимостей

```text
Пульт IR/BT → KeyLayout (*.kl), InputManager, global key handler в trdservice
    ├── HOME → будущий FLauncher (общий UI)
    │     ├── Settings shortcut → TvSettingsPlus / Android TV Settings
    │     ├── Sources → существующая KuSourceRJ / TV Input
    │     └── Projector → существующая TvSettingsPlus или RuiAutoFocus Activity
    ├── SETTINGS button → trdservice.GlobalKeyEventProcess → нужный entrypoint TvSettingsPlus
    └── INPUT / HDMI → KuSourceRJ → TRD/MediaTek TV Input/HAL

TvSettingsPlus (com.android.tv.settings; штатный APK уже OEM-расширен)
    ├── Android: Wi-Fi, Bluetooth, Date/Time, Language, Apps
    ├── Picture/PQ, Gamma, Brightness, Sound, Sources
    ├── ProjectorMode, FocusSettings, KeystoneCalibration
    └── Android↔OEM Intent, Binder, settingsi2c_jni

KuSettings (com.my.settings; отдельное OEM меню)
    ├── заводские пользовательские экраны Wi-Fi/BT/System
    ├── отдельные ScreenServices и настройки производителя
    └── переходы в RuiYunOta, KuSourceRJ; цель — перенос уникальных функций в TvSettingsPlus

RuiAutoFocus, KeystoneCorrection, KuSourceRJ
    → OEM TRD IProjectorCtrl / ITofCtrl / ISystemCtrl
    → trdmiddle / trdservice / JNI
    → MediaTek TV HAL / native TV service / I2C / motor / ToF / TV Input
    → kernel modules + tvconfig/bootdata/DTBO/PMU/panel calibration

MediaTek TV services:
   Android HAL/HIDL ⇄ TVservice (отдельная Linux/TV среда)
   и platform components (MtkTvInput, TvServices, HDMI CEC, SystemUI)

A/B OTA:
   RuiYunOta + update_engine/payload/vbmeta/bootloader/board identifiers
   (путь кастомного подписанного обновления НЕ подтверждён)
```

Стрелки схемы — **логическая интеграция, выведенная из статических вызовов**. Далеко не все пути прослежены до реальных register writes. Не считать схему подтверждённой runtime трассировкой.

## 2. Матрица слоёв и окончательных решений

| Слой | Бинарная/аппаратная общность | Решение для двух будущих прошивок | Доказано / ограничение |
|---|---|---|---|
| Boot ROM/U-Boot/mboot | образ заводских ревизий различается | **KEEP PER PROFILE**, не переподписывать/заменять сейчас | Различаются factory images; runtime AVB и установка ждут владельцев |
| `boot`, kernel, DTBO, OP-TEE, `vbmeta` | образы различаются по SHA | **KEEP PER PROFILE**, собственный rollback отдельно | Код и dtbo mapping не достаточно для безопасного cross-flash |
| `tvconfig` / `bootdata`, panel, gamma, PMU | часть файлов уже побайтно одинакова в Oct8052↔Sep8054, gamma/PMU отличаются | **KEEP PER PROFILE**, можно документировать общий материал | 6/9 контрольных конфигов идентичны, 3 нет |
| Factory, persist, eeprom, project_id, private, calibration | индивидуальные либо factory данные, не обычный софт | **PRESERVE NEVER OVERWRITE**, резервировать приватно | Не было живого бэкапа; особенно риск автоочистки Hysd calibration |
| Отдельная Linux среда `linux_rootfs`, `3rd`, `tvservice` | заводские бинарники близки, есть изменения | **KEEP PER PROFILE** до сравнения актуальных файлов и сценариев запуска | Старые factory сравнения есть, полная связь с Android ещё не доказана |
| Android `vendor` HAL и нативные библиотеки | 1527 общих ELF; 2 разных `.text`, часть различается данными | **KEEP PER PROFILE**, приоритет на совместимость, а не копирование «более нового» | 8052 Oct vs 8054 Sep: машинный код большинства одинаков, но данные / ABI могут отличаться |
| WLAN/BT kernel modules & firmware | MT7663 отличается `.text`, два варианта вермагика 5.15.189 | **KEEP PER PROFILE**, диагностировать если реально активен | Не доказан активный Wi-Fi chipset и полезность newer driver |
| HDMI TV Input / CEC / Audio / Display services | часть общих APK идентична, profile flags разные | **KEEP BACKEND, COMMON UI** | 1/2 HDMI; безопасные ID источников ещё проверить runtime |
| TOF, мотор, автофокус, трапеция `RuiAutoFocus` | 10 Java-методов отличаются Oct8052/Sep8054; нативные hardware paths возможны | **KEEP PER PROFILE** пока не объяснены 10 методов, общий экран управления | У 8052 ToF capability flag=0, у 8054=1; физика уточняется |
| OEM TRD Binder/JNI (`trdservice`, `trdmiddle`) | APK побайтно идентичны между актуальными исследованными версиями | **KEEP** в обоих исходных образах; пользоваться единым API | API и манифесты найдены; разрешения/ошибки связи на устройстве не подтверждены |
| `KuSourceRJ`, `KeystoneCorrection` | в октябрьской 8052 и сентябрьской 8054 APK одинаковые | **KEEP**, UI вызывать из TvSettingsPlus | Hardware backend, menu/gesture/geometry могут быть привязаны к ним |
| `TvSettingsPlus` `com.android.tv.settings` | APK идентичен | **COMMON PATCH** будущего единого Android TV Settings | Нужны точные entrypoint, права, разделы и default intent |
| `KuSettings` `com.my.settings` | APK идентичен | **MIGRATE THEN REMOVE** после сохранения функций | Сейчас отдельный OEM UI с уникальными переходами |
| HOME `zxlauncher` | APK двух версий отличаются | **REMOVE + FLauncher** (общий) | Пока нет теста на real target, проверять HOME/Settings/remote fallback |
| Store `zxstore` | различается | **REMOVE** | Не вырезать стандартный PackageInstaller, не углубляться в OEM магазин |
| `KuSetupWizard`/`Provision`, `AutoPair` | factory отличается по поколению, Oct8052 содержит KuSetupWizard | **KEEP FIRST BOOT** | Первичная настройка, настройки прав, привязка пульта; Android setup flags требуют проверки |
| `RuiYunOta` | APK одинаков | **KEEP OTA** без переписывания | Подпись и адрес обновления не доказаны для собственного пакета |
| Android APEX, `SystemUI`, PackageInstaller, PermissionController, TvServices/Provider | платформа Android 13 | **KEEP CORE** | Риск аварийной загрузки при изменении/удалении |
| Остальные factory APK (см. 89-packages inventory) | классификация начата, 14 OEM APK глубоко сканированы | **KEEP PENDING AUDIT / OPTIONAL** | Не делать bulk debloat до полного списка current OTA и проверок receivers/services |
| KeyLayouts, overlays, `etc/permissions`, `sepolicy`, init.rc | отдельные ресурсы и права OEM сервисов, не APK | **KEEP, MAP BEFORE PATCH** | Не всё перечислено в глубоком аудите; влияет на HOME и кнопку Settings |

## 3. Главное правило выбора «более новой версии»

Не переносить бинарники между устройствами по имени файла и дате компиляции.

Вводим 4 причины: **аппаратный профиль**, **обновление программы с поведением**, **другие данные/сборка без изменения доказанного кода**, **причина не установлена**. Решение принимать только после:
1. точного SHA и версии исходной сборки;
2. ABI, динамических зависимостей, подтверждённой доступности HAL/JNI/Binder на обоих устройствах;
3. сравнения изменённых функций и значений конфигурации;
4. подтверждения, что компонент реально используется на обеих ревизиях;
5. оценки пути отката и теста на 8052 и 8054.

Если фактически одинаковый APK — исходные оригиналы оставить и применить **общий патч логики интерфейса**, не подменять части `vendor` без причины.

## 4. Остающиеся фундаментальные вопросы

Подробный контрольный список в [UNRESOLVED_AUDIT_GATES_RU.md](UNRESOLVED_AUDIT_GATES_RU.md). В особенности: какие стандартные и OEM настройки реально доступны пользователю, где хранится значение каждого параметра, куда нажимает пульт, какие права у новых компонент Settings, какие OEM службы пишут в калибровочные файлы, что изменено в tvservice и как проверяется первый запуск.

## 5. Границы текущего исследования

Уже сделаны: два расшифрованных factory PKG, последняя OTA 8052.1.0.4, разделы и DTBO, baseline TVservice/Linux, сравнение Android ELF 1527 файлов и 14 OEM APK, JNI/Binder map, отдельная карта 89 factory APK.

**Не сделаны:** runtime исследование реальной 8054.1.0.4, полный разбор всех APK Android, побайтовый/семантический diff latest 8052 Linux/TVservice к 8054, точное действие Settings remote key, релизная подпись/install/recovery. Этим документом они не объявляются выполненными.

## Источники

- [Latest Oct 8052 vs Sep 8054](../Latest_8052_OTA_vs_8054_Stock/README.md)
- [ELF machine code](../Deep_Stock_Audit_20261021/NATIVE_8052_OTA_VS_8054_RU.md)
- [OEM Intent candidate edges](../Deep_Stock_Audit_20261021/OEM_INTENT_CALL_CHAINS_RU.md)
- [Source OEM API](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/blob/research-oem-settings-api-20261020/analysis/OEM_API_8052_Latest/IMPLEMENTATION_RU.md)
- [All APK inventory](APK_ALL_PACKAGES_RU.md)
