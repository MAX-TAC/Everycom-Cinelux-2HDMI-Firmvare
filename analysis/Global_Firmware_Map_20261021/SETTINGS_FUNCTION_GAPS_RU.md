# План переноса всех значимых OEM-настроек в Android TV Settings

**Важно:** в прошивке уже присутствует отдельный `KuSettings` (`com.my.settings`) и доработанный AOSP `TvSettingsPlus` (`com.android.tv.settings`) с собственными `uicustom` и `partnercustomizer`. Это не означает, что все обнаруженные Java-классы доступны пользователю без правок. Матрица определяет, **что доразобрать до удаления KuSettings**.

**Выбранная архитектура первой версии:** FLauncher → `TvSettingsPlus.MainSettings` → встроенные стандартные разделы и штатные OEM активности/службы. OEM HAL/TRD/Motor остаются. Кнопку Settings пульта перенаправить тем же безопасным маршрутом, не перехватывать низкоуровневые сканкоды в самом FLauncher.

## Функциональная матрица

Легенда: `STANDARD` — стандартный Android TV framework; `TV_CODE` — в APK TvSettingsPlus обнаружен класс/метод; `OEM_ONLY` — соответствующий путь документирован в отдельном OEM APK; `UNKNOWN` — фактическое присутствие/обработчик на живом устройстве не доказаны. `UI_EXISTS?` означает **потребность в runtime проверке**, а не наличие готовой работающей настройки.

| Раздел | Где код существует сейчас | Можно ли считать готовым TV Settings? | Что делать | Проверка |
|---|---|---|---|---|
| Wi-Fi | STANDARD + `KuSettings.MyWifiActivity` | STANDARD likely | Сначала включить штатный экран; сохранить сопутствующие OEM сетевые prefs только если действительно уникальны | DHCP/sleep/wake |
| Bluetooth & пульт | STANDARD + `KuSettings.MyBluetoothActivity`, `AutoPair` | STANDARD likely | Сохранить BT профиль пульта/AutoPair; OEM UI убрать после тестов | pair/reconnect |
| Язык, раскладка, время | STANDARD + KuSettings | STANDARD likely | Вести в штатные TV Settings, не удалять `KuSetupWizard` | reboot/setup |
| Об устройстве, дата версии, обновление | `TvSettingsPlus` + `RuiYunOta.OTASystemNetworkUpdateActivity` | UI_EXISTS? | Стандартное About + проверенный OEM update Intent | OTA page opens |
| Установка APK, apps | STANDARD PackageInstaller / TvSettingsPlus | STANDARD | Сохранить системный установщик после удаления zxstore | install/uninstall |
| Изображение, picture modes | `partnercustomizer.picture.PictureModeFragment`, `PictureModeValueFragment` | TV_CODE; UI_EXISTS? | Проверить доступность, точные сеттеры MediaTek TV, save/reboot | PQ profiles |
| HDR processing | MediaTek TV HAL + picture code | UNKNOWN | Определить различия HDR10/HLG tone mapping и доступные control settings, без raw I2C | signal format |
| Gamma / color temperature | `GammaFragment`, `ColorTuneBrightnessFragment`, gamma in tvconfig | TV_CODE; UI_EXISTS? | Не переписывать заводскую gamma, сохранить source & profile defaults | HDR/non-HDR |
| Яркость | `BrightnessModeSettingsFragment`, `KuSourceRJ.BrightActivity` | TV_CODE; OEM_ONLY | Сопоставить аппаратную/алгоритмическую яркость с программной PQ | level + thermal |
| Contrast/sharpness/saturation | TV Picture customization | TV_CODE; UI_EXISTS? | Проверить, доступны ли все пользовательские значения, не затрагивать service calibration | persistence |
| Звук / HDMI / digital output | `TvSettingsPlus.AudioOutputFragment`, Audio HAL | TV_CODE; UI_EXISTS? | Свести звуковые настройки в раздел Audio, оставить маршрутизацию OEM/MediaTek | ARC/BT/speaker |
| Источник сигнала / HDMI 1/2 | `SourceSubMenuController` → `KuSourceRJ` | TV_CODE, external OEM activity | В разделе «Источники» запускать штатный OEM backend; список по hardware capabilities | 1 vs 2 HDMI |
| Источник при запуске | `KuSourceRJ.BootSoureActivity.setBootSource(int)` | OEM_ONLY; not public API | Статически проследить exact source ID/permission, UI добавить только после проверки | reboot source |
| HDMI CEC/ARC/eARC | Android HDMI stack + MediaTek HAL + TV settings | UNKNOWN | Выявить реально поддержанные CEC режимы и их UI | hotplug/sleep |
| Режим установки / поворот | `ProjectorModeFragment`, `ProjectorManager.get/setProjectorMirrorMode` | TV_CODE; UI_EXISTS? | Открыть существующий пункт в Projector без произвольной записи register | 4 modes |
| Автофокус при включении | `FocusSettingsFragment`, `IProjectorCtrl.setAutoFocusBoot` | TV_CODE | Проверить permission, persisted state и profile defaults | startup |
| Автофокус при перемещении | `IProjectorCtrl.setAutoFocusMove` | OEM Binder; UI_EXISTS? | Добавить экран/переключатель при наличии sensor | 8052/8054 |
| Ручной фокус и мотор | `RuiCameraApi.MotorFrontStep/BackStep/Stop` | OEM_ONLY (UI path TBD) | Использовать проверенный OEM экран/сервис с лимитами, не вызывать JNI напрямую | endpoint safety |
| ToF | `getTofIcExist`, `startTof`, `ITofCtrl` | OEM_ONLY | Показывать только при физической доступности и hardware 8054 | no-sensor |
| Автотрапеция при включении | `IProjectorCtrl.get/setAutoKeystoneBoot`, `ProjectorFragment` | TV_CODE; UI_EXISTS? | Сохранить триггеры и значение, отображать в Projector | reboot |
| Автотрапеция при движении | `IProjectorCtrl.get/setAutoKeystoneMove` | OEM Binder | Выяснить действительный hardware trigger, добавить при наличии | move |
| Четыре угла / ручная трапеция | `KeystoneCalibrationActivity`, `KeystoneCorrection`, `setKeystoneValue` | TV_CODE + OEM backend | Перенести навигацию и экран, параметры write-only не угадывать | 4 corners |
| Reset / восстановление геометрии | `resetKeyStone`, `cusRestoreKeyStone` | OEM Binder | Различить обычный пользовательский сброс и заводскую калибровку | non-destructive |
| Цифровой zoom | `DigitalZoomActivity` / `RuiCameraApi.get/setProjectorZoom` | OEM_ONLY; TV path TBD | Добавить TV-экран или ссылку на существующий safe OEM screen | 100-? percent unknown |
| Плавающее меню / OSD | `TvSettingsPlus.uicustom.floatmenu.FloatMenuService` | TV_CODE | Проверить overlay и реакцию пульта, оставить как опциональный UI | key overlay |
| Настройки режима ожидания | TV Services, `trdservice`, OEM | UNKNOWN | Разобрать pipeline standby/wake и значения power saving | wake time |
| Вентилятор/термозащита | native TV services/PMU/device thermal HAL | UNKNOWN | **Не переносить заводские сервисные регуляторы** в пользовательский UI без безопасной спецификации | observation only |
| HDMI EDID/HDCP | MediaTek TV Factory API | NOT user-level | Не копировать инженерные команды в TV Settings; оставить диагностику | 4K input |
| I²C/Factory register & project calibration | `Factory.ProjectorManager.i2c`, `libsettingsi2c_jni`, `AiFileUtils` | NOT user-level | Сохранить factory, запретить прямые записи из UI | static only |
| Bluetooth speaker receiver mode | `RJBluetoothSpeaker` / A2DP sink | OPTIONAL, not output | Исключить из UI и позже удалить при проверенной независимости от BT-пульта/A2DP output | BT output unaffected |

## Почему нельзя утверждать, что всё уже «есть» в TvSettingsPlus

APK действительно содержит много нужных классов, однако реальные экраны могут зависеть от:
- параметров `ro.rjpj.*`, `ro.zeasn.devicetype`, HDMI/ToF flag;
- system property/Settings Provider и overlays;
- наличия соответствующих Activity/Fragment, XML preference tree и видимости;
- protected permission или `signature|privileged` ограничения;
- регистрации Binder служб и состояния TV Input.

Поэтому для каждого пункта нужно выделить **UI entrypoint → get-state → set-state → persistence → hardware operation**. Если `get/set` уже существует, переносится навигация, а не устройство управления.

## Особая задача: физическая кнопка Settings

Из `trdservice.GlobalKeyEventProcess` известны статические ссылки на `com.android.tv.settings` и старый/альтернативный `com.trd.projector.settings.MainSettingsActivity`. В частности, **строка/класс ещё не доказывает активную ветку**. Требуются:
1. разобрать switch-case по input keycode и выбор пакета/Activity;
2. проверить `pm resolve-activity` и доступные exported Activity на каждом устройстве;
3. определить, достаточно ли изменить default settings intent, overlay или требуется правка `trdservice` обработчика;
4. предусмотреть безопасную альтернативную кнопку/ярлык в FLauncher при сбое Settings;
5. проверить кнопки Settings/Home/Back/Input после standby/reboot.

## Готовность к удалению KuSettings

`KuSettings` можно исключить, если:
- ни один критичный пункт из списка не остаётся только внутри KuSettings;
- отсутствуют обязательные boot-receiver/service/provider зависимости или они перенесены;
- `KuSetupWizard` и `AutoPair` работают отдельно;
- системные permission, persistence, remote key mapping и OTA открываются нормально;
- тесты проходят на **8052 и 8054 по отдельности**.

## Источники

- [Существующая предварительная карта](../Stock_Custom_Architecture_20261021/OEM_SETTINGS_MIGRATION_RU.md)
- [OEM Binder/JNI исследования](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/blob/research-oem-settings-api-20261020/analysis/OEM_API_8052_Latest/IMPLEMENTATION_RU.md)
- [Android Intent candidates](../Deep_Stock_Audit_20261021/OEM_INTENT_CALL_CHAINS_RU.md)
