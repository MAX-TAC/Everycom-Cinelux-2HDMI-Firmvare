# Баг-аудит изменённого TvSettingsPlus: подтверждённые функции и кандидаты на ошибки

**Проверено:** оригинальная октябрьская OTA 8052.1.0.4 (SHA verified), decompiled TvSettingsPlus и связанные KuSetupWizard/KuSettings; Android TV Settings upstream `android-13.0.0_r56` **только как эталон доступных классов**. Сентябрьская заводская 8054.1.0.1 содержит **побайтно идентичные** `TvSettingsPlus`/`KuSettings`/`trdservice`, но актуальная 8054.1.0.4 не получена.

## Общий результат

- **Не подтверждено ни одной воспроизводимой ошибки TvSettingsPlus:** статический просмотр APK не воспроизводит ошибки приложения на устройстве.
- Найдено **несколько конкретных высокорискованных или потенциально некорректных участков**, которые нужно изолировать при модификации UI.
- 475 путей классов открытого AOSP Android 13 найдены в OEM APK, 512 дополнительных путей, в т.ч. 142 `uicustom`, 164 `partnercustomizer`, 189 `library`. Методное сравнение AOSP vs JADX содержит шум синтетических методов и не должно интерпретироваться как фиксы или баги.
- Уже существуют обработчики фокуса, трапеции, источников, HDMI EDID/CEC, Audio/eARC, режимов картинки. Значит общий UI должен открывать исходные безопасные обработчики, а не напрямую трогать нативный драйвер.

## Конкретная очередь проверки (с местами JADX)

| ID | Файл/метод | Установленный статический факт | Возможная проблема | Рекомендация для кастома |
|---|---|---|---|---|
| RISK-01 | `uicustom/fragment/projector/KeystoneCalibrationActivity.resetFactoryCalibrationData` (~346 строка) | Есть **4 SystemProperties.set**, обращения к аппаратной прослойке и обработчик исключения | Потеря или несогласованность заводских калибровок, если функцию неверно открыть пользователю | Не показывать в обычном «Сброс трапеции»; не вызывать при миграции |
| RISK-02 | `KeystoneCalibrationActivity.startFactoryCalib` / `saveFactoryCalibrationData` | Есть factory calibration state и вызовы других компонентов | Неправильное прохождение/прерывание заводской калибровки | Держать отдельным инженерным экраном, не применять после обновления автоматически |
| RISK-03 | `uicustom/floatmenu/controller/source/SourceSubMenuController.initBoardConfig` (~99) и `switchToHDMI` (~425) | 9 ветвей проверки board config, 2 условные ветки переключения HDMI, MediaTek/OEM ссылки | Неверный HDMI index на ревизии 8052 или неправильный resume/source | Не объединять hardware source IDs; испытать HDMI1 и HDMI2 на 8054 отдельно |
| RISK-04 | `FocusSettingsFragment.setPowerOnAutoFocus`, `setMoveAutoFocus`, `setAccurateFocus` | Используются свойства **`persist.rjpj.autofocus.poweron`**, **`persist.rjpj.autofocus.move`**, **`persist.rjpj.tof.autofocus`** | Пункт ToF или режим движения может появиться у ревизии без датчика и давать ложные настройки | Проверить `ro.rjpj.support.toffunction` и реальное наличие ToF, не копировать profile defaults |
| RISK-05 | `ProjectorFragment.startAutoFocus` / `startAutoKeystone` | Проводится чтение свойств и dispatch в OEM-сервис, `try/catch` с логированием | UI мог оставить прежнее состояние при недоступности OEM-службы | После подтверждения воспроизведения добавить корректную обратную связь/timeout, не менять мотор |
| RISK-06 | `SourceSubMenuController.checkBluetoothSpeakerPackage` | Проверяет пакет Bluetooth speaker; есть обработка исключений | После удаления A2DP Sink UI может по-прежнему показывать пункт или пытаться открыть отсутствующий пакет | Убрать пункт/зависимость только в UI, сохранить BT output/remote |
| RISK-07 | `partnercustomizer/utils/SoundEARCReceiver.updateEARCSettingValueToDrive` | Читает `KEY_SOUND_EARC` и вызывает TV API, есть два обработчика исключений | Несохранение/рассинхронизация eARC или необработанная ошибка драйвера | Не удалять при очистке; проверять ARC/eARC после reboot |
| RISK-08 | `TvBootupReceiver.onReceive` | **Без ветвей** запускает `WirelessSpeakerServices` при BOOT_COMPLETED | Потенциальная ненужная активность A2DP Sink, если режим не используется | Выяснить необходимость Wireless Speaker, только затем отключать соответствующую ветку |
| RISK-09 | `uicustom.MainActivity.onKeyDown` | 14 условных ветвей обработки клавиш | Вероятные коллизии навигации при подмене Settings / D-pad | Не менять keylayout пульта без необходимости, сначала FLauncher shortcut |
| RISK-10 | `KuSettings.ScreenServices` | Пишет SystemProperties, делает screenshot через `SystemUI`, binding/unbinding, Thread.sleep | Если удалить KuSettings, может пропасть скриншот/доп. служебная функция; возможна блокировка потока при screenshot | Установить вызывающих и исходное свойство; оставить/перенести лишь если используется |
| RISK-11 | `KuSettings.MySetTimeService` | Регистрирует time tick и не показывает прямого аналогичного UX в Android TV Settings | Возможно лишняя фоновая служба, возможна потеря OEM time refresh | Проверить жизненный цикл и реальные callers |
| RISK-12 | `KuSetupWizard.ProvisionWifiActivity` / `ProvisionBluetoothActivity` | Обработка первоначального Wi-Fi/BT; в manifest `HOME`+`SETUP_WIZARD` | Отсутствие рабочего мастера после factory reset и сбой initial provisioning | **Сохранить в первой прошивке** до проверки first boot и replacement |

**Статус каждого RISK:** `потенциальный риск`, **НЕ воспроизведённая программная ошибка**. Наличие `printStackTrace()` или `try/catch` не означает баг само по себе.

## Спорный вопрос «полный сток против OEM»

В исследованном APK TvSettingsPlus из известных AOSP TvSettings Android 13 Java-paths совпали **все 475**. Классы в `uicustom` и `partnercustomizer` — отдельные расширения; основные классы AOSP тоже могут иметь изменённые тела.

Чтобы написать отчёт «OEM сломал конкретную функцию по сравнению с AOSP», нужны:
- реальный исходный AOSP fork point производителя;
- нормализованный bytecode diff, а не совпадение имени или различие списка методов из JADX;
- сценарий, лог или trace поведения из оригинальной RUIOS;
- обоснование исправления и проверка обеих аппаратных ревизий.

Пока делать вывод, что именно OEM доработки вызывают баги, **нельзя**.

## Практическое решение

**Первоначально не пересобирать TvSettingsPlus ради добавления ярлыка.** Для FLauncher используем экспортированную `com.android.tv.settings/.MainSettings`.

Дополнительно штатное проекторное меню `com.android.tv.settings/.uicustom.MainActivity` экспортировано и может быть протестировано как второй ярлык без модификации APK. Если открывается — пользовательские аппаратные настройки доступны без переноса низкоуровневого кода.

После реальных испытаний и проверки конкретного отсутствующего экрана интегрировать его в `MainSettings`, подписав APK AOSP platform test-key в изолированной сборочной среде, учитывая AVB и права.

## Метаданные

- [Deep settings/wizard classes](DEEP_SETTINGS_WIZARD_RU.md)
- [Critical method flow markers](CRITICAL_METHOD_FLOWS_RU.md)
- [AOSP 13 source reference](AOSP_TVSETTINGS_13_REFERENCE_RU.md)
- [Stock settings routing and APK signatures](../Global_Firmware_Map_20261021/SETTINGS_8052_VS_8054_VERDICT_RU.md)
