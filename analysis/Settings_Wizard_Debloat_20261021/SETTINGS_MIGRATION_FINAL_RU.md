# Практическая миграция KuSettings в штатные Android TV Settings (TvSettingsPlus)

## Критически важное различие трёх интерфейсов

Все три Activity есть в исходном APK RUIOS 8052.1.0.4:

| Activity | Пакет | Назначение | План |
|---|---|---|---|
| `com.android.tv.settings.MainSettings` | `com.android.tv.settings` | **Основное полноценное Android TV Settings**, как на присланном фото | В FLauncher основной ярлык «Настройки» |
| `com.android.tv.settings.uicustom.MainActivity` | `com.android.tv.settings` | **Отдельная OEM панель** внутри TvSettingsPlus, 142 Java-файла uicustom | В начале оставить отдельный доступ «Проектор»; в дальнейшем интегрировать разделы внутрь MainSettings |
| `com.my.settings.SettingActivity` | `com.my.settings` | Второе, независимое OEM приложение KuSettings, обработчик `android.settings.SETTINGS` | Функциональная миграция, затем исключить при соблюдении boot/setup зависимостей |

Скриншоты пользователя **подтверждают только запуск первого экрана**. Нельзя без проверки утверждать, что другое заводское окно, видимое на устройстве, относится именно к KuSettings, а не к `TvSettingsPlus.uicustom`.

## Рекомендация для первого теста: два независимых ярлыка без переподписи TvSettingsPlus

Основные Android TV Settings:
```sh
adb shell am start -n com.android.tv.settings/.MainSettings
```

Штатное дополнительное проекторное меню:
```sh
adb shell am start -n com.android.tv.settings/.uicustom.MainActivity
```

Обе Activity имеют `exported=true` в оригинальном манифесте. Вторая команда ещё не была выполнена на устройстве — возможно, ей требуется дополнительный контекст/ресурсы/доступ к Binder. Если работает, это сохранит большинство аппаратных настроек без изменения APK.

## Реальная матрица переходов KuSettings.IntentUtils

`KuSettings` и `KuSetupWizard` содержат сходную библиотеку `com.my.utils.IntentUtils` (проверено JADX). Наличие метода **не означает**, что он обязательно зарегистрирован в первом запуске или доступен пользователю.

| Функция KuSettings | Уже есть в TvSettingsPlus или OEM-бэкенде | Решение для MainSettings | Что не переносить механически |
|---|---|---|---|
| `myWifi` | `NetworkActivity`, Wi-Fi Android TV | Использовать штатное меню сети | OEM Wi-Fi pairing при первом запуске отдельно |
| `myBluetooth`, `autoBluetooth` | `BluetoothAccessoryActivity`, `AddAccessoryActivity` | Стандартное управление Bluetooth | Не удалить `AutoPair` и boot `BluetoothDevicesService` |
| `myDateTime`, `timeZone` | `DateTimeActivity` | Стандартные дата, время и часовой пояс | Уникальную `MySetTimeService` изучить на предмет фоновых эффектов |
| `myLanguage`, `languageLocal` | `LanguageActivity`, системные locale | Стандартные языковые настройки | `KuSetupWizard` сохраняет свои значения первого запуска |
| `projectAbout` | `AboutActivity`, `KuSettings.ProjectionActivity` | Стандартные «Об устройстве» + OEM технические поля | Заводские тесты `ProjectionActivity.testAction` в пользовательский UI не переносить |
| `startOta` | `RuiYunOta.OTASystemNetworkUpdateActivity` | Ссылка в «Об устройстве / Обновление» | Не заменять update_engine и механизм проверки подписи |
| `brightIntent` | `KuSourceRJ.BrightActivity`, `TvSettingsPlus.BrightnessModeSettingsFragment` | Добавить/показать «Яркость» | Не путать мощность источника света, PQ и сервисную калибровку |
| `voiceIntent` | `KuSourceRJ.VoiceActivity`, `TvSettingsPlus.SoundActivity` | Стандартное меню звука + аппаратные пункты | Не менять Audio HAL |
| `bootSoure` | `KuSourceRJ.BootSoureActivity` | Раздел «Источники» | Разные HDMI source ID у 8052/8054 |
| `poweron` | `KuSourceRJ.PoweronModeActivity` | Раздел «Питание» / OEM Activity | Не менять низкоуровневое питание |
| `projectModel` | `KuSourceRJ.ProjectModelActivity`, `TvSettingsPlus.ProjectorModeFragment` | Режим установки/зеркальности | Сохранять профиль |
| `keystoneIntent`, `startUniversalKJ` | `KeystoneCorrection`, `TvSettingsPlus.ProjectorFragment` | Раздел «Трапеция» с оригинальным сервисом | Factory calibration и пользовательская трапеция — разные операции |
| `imageDigitalIntent` | `KuSourceRJ` / `RuiAutoFocus` цифровой zoom | Раздел «Зум» после проверки числового диапазона | Не работать с мотором напрямую |
| `mircastIntent`, `airplayIntent` | `WFDSinkTest`, `FTAirplayWireless` (кандидаты) | Пользовательская опция, отдельно решить о сохранении | Сначала проверить реальное назначение и зависимости |
| `screenshot` | `KuSettings.ScreenServices` + `SystemUI.TakeScreenshotService` | Опциональная функция, в базовых TV Settings её нет | Системное свойство/привязка к SystemUI требуют аудита |
| `restoreIntent` | `KuSourceRJ.RestoreActivity`, в TV Settings `FactoryResetActivity` | Сначала **сопоставить семантику** | OEM reset текущего режима и заводской Android wipe неэквивалентны |
| `startTest`, `startKJTest` | OEM factory/test | Не включать в обычное пользовательское меню | Сохранить инженерную диагностику |
| `provisionBluetoothIntent`, `provisionWifiIntent` | `KuSetupWizard` | **Не переносить** в MainSettings | Это первоначальное сопряжение/настройка, оставить отдельным flow |
| `warnIntent`, `provisionMenuIntent` | OEM setup/info экраны | Отдельное решение по смыслу | Может использоваться в первом запуске |

## Какие OEM разделы уже явно существуют в TvSettingsPlus

`uicustom` содержит проекторные `FocusSettingsFragment`, `ProjectorFragment`, `KeystoneCalibrationActivity`, `BrightnessModeSettingsFragment`, `PictureModeValueFragment`, контроллеры `SourceSubMenuController`, `ProjectorSubMenuController`. Дополнительно `partnercustomizer` содержит `PictureModeFragment`, `GammaFragment`, TV audio/eARC и службы совместимости MediaTek.

Это подтверждённые Java-классы/методы в SHA-верифицированном APK. Из этого пока не следует, что все настройки пользователь может открыть из `MainSettings` без дополнительного перехода.

**В начале лучше открывать штатную `uicustom.MainActivity` как отдельный экран из нового лаунчера, а не копировать заново низкоуровневые обработчики.** Затем можно встроить Projector entry внутри MainSettings после проверки API и подписи.

## Что отсутствует или пока не подтвердилось

- Одинаковая для обеих ревизий фактическая видимость пунктов настройки в MainSettings — не проверена на реальной 8054 новой версии.
- Полный набор пользовательских настроек `KuSettings` (по UI и сохранённым значениям) без запуска заводского экрана на реальном устройстве не гарантирован.
- Корректность каждого save/reboot сценария, переходов HDMI/ARC/eARC/ToF/ручного фокуса.
- Значение `KuSettings.ScreenServices` для screenshot/Power/LCD status.
- Реальная роль `KuSetupWizard` в флагах provision и при factory reset.

## Вывод

**Для первого кастома реальная задача — UI-навигация и проверка эквивалентности режимов, а не перенос всех OEM алгоритмов.** Вторая очередь — убрать KuSettings после проверки его сервисов и проведения boot/wifi/remote/factory reset тестов.

Источники:
- [Deep JADX inventory](DEEP_SETTINGS_WIZARD_RU.md)
- [Фото Activity пользователя подтверждает MainSettings; код TvSettingsPlus.MAIN + LEANBACK_LAUNCHER](../Global_Firmware_Map_20261021/SETTINGS_DISPATCH_8052_RU.md)
- [OEM source call graph](../Deep_Stock_Audit_20261021/OEM_INTENT_CALL_CHAINS_RU.md)
