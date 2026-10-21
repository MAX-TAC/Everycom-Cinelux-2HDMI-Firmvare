# Оставшиеся исследования для release-grade карты RUIOS 8052 / 8054

**Интерпретация статуса:** `STATIC` — доказано по оригинальным образам; `NEEDS_CODE_FLOW` — метод/компонент известен, требуется проследить вызов и обработку состояний; `NEEDS_DEVICE` — без проектора не доказывается; `OPEN` — данных пока недостаточно.

Общая цель — знать **почему** каждый компонент оставлен/исключён и уметь проверить результат, а не декомпилировать всё без практической цели.

## Этап 1. Точное проекторное меню и пульт (обязателен до удаления KuSettings/zxlauncher)

| № | Вопрос | Известный вход | Тип | Готовый результат |
|---|---|---|---|---|
| UI-01 | Какой компонент реально получает Settings на пульте? | `trdservice.GlobalKeyEventProcess`, `KeyLayout` | NEEDS_CODE_FLOW + DEVICE | KeyCode → dispatch → concrete Activity + резервная ветка |
| UI-02 | Почему штатный Android TV Settings не показывается? | `TvSettingsPlus.MainSettings`, `uicustom.MainActivity`, `KuSettings.SettingActivity` | NEEDS_CODE_FLOW + DEVICE | таблица entrypoints и intent resolver |
| UI-03 | Все 100% OEM пунктов: где хранится значение и какой его set/get? | `KuSettings`, `TvSettingsPlus`, `Factory`, `KuSourceRJ` | NEEDS_CODE_FLOW | перечень экрана → метод → настройка → разрешение |
| UI-04 | Какие TV Settings OEM разделы скрыты, ограничены по props или неактивны? | `ProjectorFragment`, `FocusSettingsFragment`, `PictureModeValueFragment` | NEEDS_CODE_FLOW + DEVICE | список доступных и отсутствующих пунктов для 8052/8054 |
| UI-05 | Android TV Settings privileges и подпись после изменений | `com.android.tv.settings`, `priv-app`, `privapp-permissions`, platform signatures | NEEDS_CODE_FLOW + DEVICE | список permission/UID, стратегия сохранения подписи/разрешений |
| UI-06 | Android Settings без OEM меню vs overlay/shortcut | PackageManager `resolve-activity`, launcher manifest | NEEDS_DEVICE | 2 проверенных пути: домашний ярлык и кнопка пульта |

**Завершение этапа:** цель будущей сборки должна содержать все штатные пользовательские регулировки, либо чётко объяснено, зачем какая-то из них сознательно не переносится.

## Этап 2. Надёжность аппаратных OEM алгоритмов (не заменяем их до тестов)

| № | Алгоритм / служба | Риск/известная точка | Тип | Результат |
|---|---|---|---|---|
| HW-01 | Motor front/back/stop, концевики, неверные шаги | `RuiCameraApi`, `MotorJNI`, `ruimotor.ko` | NEEDS_CODE_FLOW + DEVICE | таблица пределов, timeout и гарантированного Stop |
| HW-02 | ToF/автофокус на 1/2 HDMI, обработка отсутствия датчика | `RuiCameraApi.startTof`, `ITofCtrl`, `stmvl53l1.ko` | NEEDS_CODE_FLOW + DEVICE | подтверждённый state-machine обеих ревизий, причина 10 diff методов |
| HW-03 | Автотрапеция, ручная коррекция, зеркальность и цифровой зум | `KeystoneCorrection`, `IProjectorCtrl`, `TvSettingsPlus` | NEEDS_CODE_FLOW + DEVICE | таблица координат, range, сохранение после reboot |
| HW-04 | Файлы индивидуальной калибровки и операции удаления | `AiFileUtils.clearAllCalibrationFiles/getFileMd5AndDelete` | NEEDS_CODE_FLOW | условия удаления/восстановления, private backup; **не выполнять методы на чужом устройстве** |
| HW-05 | HDMI/CEC/hotplug/boot source 1 vs 2 ports | `KuSourceRJ`, MediaTek TV Input, `SourceSubMenuController` | NEEDS_CODE_FLOW + DEVICE | source ID mapping, focus after HDMI, resume/sleep |
| HW-06 | TV gamma, picture mode, profile сохранение | `ConfigDefaultValue.ini`, gamma/PMU, `TvSettingsPlus.partnercustomizer.picture` | NEEDS_CODE_FLOW + DEVICE | точная семантика `InputSourceID` и других различающихся строк |
| HW-07 | Питание света, термозащита, кулеры | TV platform HAL/PMU, device tree, thermal service | OPEN + DEVICE | карта daemon / sensors / safety path; сохранить original until proven |
| HW-08 | Звук HDMI/ARC/eARC/USB/BT и маршрутизация | `BasicSound_*`, Audio HAL, policy files | NEEDS_CODE_FLOW + DEVICE | маршруты выходов и устранение зависимостей после удаления мусора |
| HW-09 | Внешние подключаемые устройства Wi-Fi/LAN | `wlan_mt7663`, другие chipsets, GMAC, DTB | NEEDS_DEVICE | определить активное железо; проблемы Wi-Fi/LAN ведутся отдельно и не блокируют UI |

**Завершение этапа:** для всех опасных управляющих функций должен быть известен проверенный OEM метод и способ не записывать некорректные значения.

## Этап 3. Низкоуровневые системные зависимости, ещё не покрытые глубоко

| № | Подсистема | Что проверено | Что отсутствует | Тип |
|---|---|---|---|---|
| SYS-01 | Разделы, образы, GPT, DTBO | full factory 8052/8054, old/new config hashes | реальная active board DTBO mapping и live compatibility | NEEDS_DEVICE |
| SYS-02 | Android vendor native ELF | .text/.rodata сравнение 1527 общих ELF | для изменившихся исполняемых функций точный смысл, 8054.1.0.4 отсутствует | NEEDS_CODE_FLOW |
| SYS-03 | Встроенная Linux `linux_rootfs_a_a` | заводской файловый diff | актуальный Oct8052 vs Sep8054, сценарии вызовов из Android, IPC | OPEN |
| SYS-04 | `tvservice_a`, `tvconfig_a`, `bootdata_a` | заводской файловый diff, 9 новых config hashes | функции и динамические зависимости services/daemons Oct8052 vs Sep8054, runtime параметризация | OPEN |
| SYS-05 | `init.rc`, `init.*.rc`, `ueventd`, property triggers | разделы извлечены | полный граф порядок автозапуска, зависимости TRD, Wi-Fi, HDMI и ключевых receiver | OPEN |
| SYS-06 | SELinux/policy/permissions/privapp whitelist | manifest and exported attributes 10 OEM apps | разрешённые Binder домены, package sharedUID, права после перекомпиляции Settings | OPEN |
| SYS-07 | Remote keylayouts, key mapping, button dispatch | в старых factory определены разные `Everycom_remote*.kl` | точное сопоставление кейкодов, BTN Settings, fallback и BT remote profile | OPEN + DEVICE |
| SYS-08 | Overlays, defaults, Zygote/setup | Provision vs KuSetupWizard и пересечение KuSettings | какой overlay отключает MainSettings/кнопку, изменения на first boot | OPEN |
| SYS-09 | Ядро, модуль Wi-Fi, firmware | 5.15.189 vermagic, 8052/8054 статические модули | идентификация загруженных модулей/firmware, регрессия 8052 Wi-Fi | NEEDS_DEVICE |
| SYS-10 | 8054.1.0.4 | есть только слова владельца о версии | точный ZIP/PKG/дамп для реального file+code diff | OPEN |
| SYS-11 | OTA и recovery | архивы, подписи, A/B схема | real trust, безопасная установка/откат | NEEDS_DEVICE; **пока вне текущего приоритета** |

## Этап 4. Полная картография пользовательских пакетов и удалений

В заводских пакетах 8052/8054 — **89 APK-путей** в объединённом inventory. Глубокая OCT OTA выборка исследовала 14 OEM APK.

**Нужно получить:**
- снимок `pm list packages` и `dumpsys package` для фактически установленного набора (включая скрытые и обновлённые через /data APK);
- полный список пакетов **актуальной** OTA 8052 и **актуальной** 8054, shared UID, роли `HOME`, `SETTINGS`, boot receivers, службы и permissions;
- для кандидатов на удаление: есть ли другие APK, использующие их явный компонент/ContentProvider/Intent, и выполняются ли важные сценарии в фоне;
- разделение обязательного `SystemUI`, `PackageInstaller`, `TvServices`, `MtkTvInput`, `AutoPair` и факультативных `RJBluetoothSpeaker`, `FTAirplayWireless`, `WFDSinkTest`, `RetailDisplay`, `TrdDreamPic`, предустановленных видеоприложений;
- отдельная оценка предустановки `preinstall_del`: сам APK в system-разделе и уже скопированный в userdata — не одно и то же.

**Решение:** на первом этапе фиксируем FLauncher, `zxstore` remove и `KuSettings` migration target. Остальное оставляем по умолчанию, пока нет доказательств ненужности.

## Этап 5. Стандартизованные испытания (ПОСЛЕ офлайн анализа)

`T001` первый старт и HOME; `T002` кнопка Settings и возврат; `T003` установка APK; `T004` Ethernet/Wi-Fi/BT и пульт; `T005` HDMI1 / HDMI2; `T006` CEC/ARC; `T007` изображение и гамма; `T008` фокус/ToF/трапеция без аварийных перемещений; `T009` sleep/wake; `T010` OTA и UI обновлений; `T011` сброс и first boot; `T012` восстановление HOME после crash; `T013` термозащита и запуск вентилятора (только наблюдение).

Каждый тест фиксировать отдельно для **8052** и **8054**, указывать реальную версию сборки, тип пульта/HDMI/ToF и результат.

## Форма карточки результата

Для каждого компонента/функции сохранить:
```text
ID / Имя:
Уровень: APK, system_ext, vendor, TV Linux, boot/DTBO
Исходный baseline (8052 / 8054): файл + SHA / версия
Общее или профильно-специфичное: + доказательство
Фактический алгоритм: метод → Binder/JNI/HAL → драйвер
Конфиг и владельцы состояния / права записи:
Кого вызывают / кто вызывает:
Какая ошибка возможна / уровень уверенности:
Решение: KEEP / COMMON PATCH / MIGRATE_REMOVE / REMOVE / DEFER
Регрессионный тест, готовность к rollback:
Статус: STATIC / NEEDS_CODE_FLOW / NEEDS_DEVICE / VERIFIED
```

Никаких заявлений «всё полностью проанализировано» до заполнения критичных карточек и испытаний на реальных устройствах.
