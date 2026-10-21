# OEM → Android TV Settings: карта функций и план сохранения штатного управления

## Важно: заводское меню не является частью zxlauncher

Из оригинальной OTA RUIOS.8052.1.0.4, проверенной SHA256, установлено:
- `zxlauncher.apk`, Android package `com.zeasn.whale.saas`, — отдельная HOME/контентная оболочка.
- `KuSettings.apk`, Android package `com.my.settings`, — отдельное OEM-меню Wi-Fi/Bluetooth/первичных системных настроек.
- `TvSettingsPlus.apk`, package `com.android.tv.settings`, — самостоятельное Android TV Settings, **уже содержащее собственные OEM экраны** (`com.android.tv.settings.uicustom`, `partnercustomizer`).
- `KuSourceRJ.apk` = `com.coolux.source`: выбор/управление HDMI, boot source, связанные OEM интерфейсы.
- `RuiAutoFocus.apk` = `com.hysd.screen`: мотор и фокусировка.
- Управление через Binder/JNI сохраняется за `trdservice`, `trdmiddle`, `KeystoneCorrection`, нативными службами MediaTek.

Поэтому **не нужно копировать заводские регулировки из zxlauncher**. Для будущего кастома правильнее использовать существующие OEM интерфейсы TvSettingsPlus или высокоуровневый штатный Binder, сохранить аппаратные приложения/службы, а навигацию заменить.

Но ещё требуется runtime-проверка: какой именно компонент откроет кнопка «Настройки» на пульте, что установлено в default Intent resolve, нет ли переадресации в `GlobalKeyEventProcess`.

## Карта функций и покрытия

Уровни достоверности: **сигнатура/класс** — найден в декомпилированном APK; **связь** — обнаружен статический Intent-кандидат/вызов; **поведение** — нужна проверка на реальном 8052 или 8054.

| Раздел | Что уже есть в TV Settings или OEM | Что сохранить/сделать | Динамическая проверка |
|---|---|---|---|
| Главные системные настройки | `TvSettingsPlus.MainSettings` (`com.android.tv.settings`) | Восстановить штатный экран и ярлык с рабочего стола | Явный/неявный intent, resolver, права |
| Wi-Fi / сеть | AOSP TV Settings и `KuSettings.SettingActivity/MyWifiActivity` | Использовать TV Settings, OEM оставить пока есть уникальные параметры | Сопряжение, авто-Wi-Fi, reset/reboot |
| Bluetooth | `TvSettingsPlus` accessories, `KuSettings.MyBluetoothActivity`; часть vendor `WirelessSpeakerServices` | Единая навигация в TV Settings, A2DP Sink в кастом не включать | BT пульт, A2DP Output, pairing |
| Язык, время | `KuSettings` + AOSP TV | Оставить Android TV варианты, не потерять системные права | Timezone/locale после reboot |
| Параметры изображения | `TvSettingsPlus.partnercustomizer.picture.PictureModeFragment`, `GammaFragment`, `PictureModeValueFragment` | Встроить в одно меню «Изображение», проверить OEM PQ/HDR и пользовательские профили | Видимость пунктов, реальные значения, сохранение |
| Яркость | `BrightnessModeSettingsFragment`, `ColorTuneBrightnessFragment`; `KuSourceRJ.BrightActivity` | Разделить оптическую/ламповую яркость, программную яркость, заводские параметры | Безопасный диапазон, реакция аппаратной части |
| Переворот/монтаж | `TvSettingsPlus.ProjectorModeFragment`, `ProjectorManager.getProjectorMirrorMode/setProjectorMirrorMode` | Перенести/показать штатный пункт в «Проектор» | 4 положения, сохранение после перезапуска |
| Автофокус | `TvSettingsPlus.FocusSettingsFragment`, OEM `IProjectorCtrl.get/setAutoFocusBoot` | Оставить OEM Binder, включить корректное отображение режима в UI | Работа на 8052 и 8054, разрешения |
| Ручной фокус | `RuiAutoFocus` / `RuiCameraApi.MotorFrontStep/BackStep/Stop` | Вызывать через проверенный OEM путь; лимиты движения | Motor stop, timeout, крайние положения |
| Автотрапеция | `ProjectorFragment`, `ProjectorSubMenuController`, `IProjectorCtrl.get/setAutoKeystoneBoot` | Единый UI без изменения двигательных/геометрических алгоритмов | Автоматика on/off, reset, profiles |
| Ручная трапеция | `KeystoneCalibrationActivity`, `KeystoneCorrection`, `IProjectorCtrl.setKeystoneValue` | Пункт в «Геометрия» с прежним OEM механизмом | Диапазон углов, restore previous settings |
| ToF | `RuiAutoFocus.RuiCameraApi.getTofIcExist/startTof`, `TofCtrlService` | Пункт только при наличии реального аппаратного датчика и поддерживающего профиля | В первую очередь 8054, отличать false capability |
| Источники | `TvSettingsPlus.SourceSubMenuController` → `KuSourceRJ` | Ярлык источников в UI и в лаунчере | 1/2 HDMI, CEC, без сигнала, resume |
| HDMI при включении | `KuSourceRJ.BootSoureActivity`, `ISystemCtrl.setBootSource` | Сохранить OEM настройки, не использовать числовой ID другой платы | 8052/8054 явно отдельные варианты |
| Звук | `TvSettingsPlus.AudioOutputFragment`, vendor TV/audio HAL | Собственное меню интерфейса к текущим AOSP/OEM опциям | HDMI ARC/eARC/BT/speaker |
| OTA | `RuiYunOta.OTASystemNetworkUpdateActivity` | Сохранить штатную реализацию, дать ссылку в Android TV «Об устройстве» | Проверить, какая сборка и URL принимаются |
| Первоначальная настройка | `KuSetupWizard`, package `com.android.provision` | Пока сохранить, несмотря на 99.39% общего Java-кода с KuSettings | DEVICE_PROVISIONED, USER_SETUP_COMPLETE, factory reset |
| Экранное плавающее меню | `TvSettingsPlus.FloatMenuService` и контроллеры `uicustom.floatmenu` | Сохранить/аккуратно переорганизовать в единый UX | Кнопки пульта, Overlay permissions, key handling |

**Важно:** класс в APK доказывает лишь существование реализации, а не наличие/доступность пункта меню на данной плате. Наличие `A2dpSinkProfile` в AOSP TV Settings не означает, что Bluetooth Sink нужно сохранять.

## Переадресация кнопок пульта

Статические кандидаты, которые необходимо проследить до реальных действий:

- `trdservice.GlobalKeyEventProcess` → `com.android.tv.settings` (переход к TvSettingsPlus).
- `trdservice.GlobalKeyEventProcess` → `com.trd.projector.settings.MainSettingsActivity` (OEM старый/альтернативный компонент; нужно проверить, установлен ли получатель).
- `TvSettingsPlus.GeneralFragment` → `KuSourceRJ`.
- `TvSettingsPlus.ProjectorFragment` / `KeystoneCalibrationActivity` → `RuiAutoFocus`.
- `KuSettings.IntentUtils` → `KuSourceRJ`.

Это не runtime-трассы; реальный `pm resolve-activity`, `dumpsys package` и логи при нажатии кнопки сообщит владелец.

## Стратегия будущего переноса

1. **Не трогая штатные APK**, выяснить, что открывает стандартное `android.settings.SETTINGS` и какие аппаратные экраны TvSettingsPlus доступны через явные Activity.
2. Сделать inventory всех экранов OEM: раздел, соответствующая Activity/Fragment, Binder/JNI, разрешение, сохраняемая настройка. Списки из старой прошивки не переносятся наугад.
3. Для каждого пункта присвоить статус: **уже есть в TvSettingsPlus** / **только KuSettings** / **только другое OEM-приложение** / **недоступно или не подтверждено**.
4. Если уже есть — активировать пункт и привести к общей навигации. Если нет — добавить только новый UI и высокоуровневый переход/адаптер.
5. Сохранить системные разрешения/SELinux/priv-app whitelist и signing requirements. `TvSettingsPlus` нельзя безнаказанно переподписывать и заменять обычным APK.
6. Добавить `Android TV Settings` в новый лаунчер и в меню по кнопке Settings (с проверенным fallback).
7. На реальных 8052/8054 проверить все функциональные ветви: HDMI1/2, ToF, автофокус, ручной фокус, трапеция, зеркальность, standby и OTA.
8. Только после этого убрать `KuSettings`, если полный функциональный охват доказан. Аппаратные службы `KuSourceRJ`, `RuiAutoFocus`, TRD сохранить.

## Почему OTA и Android ТВ уже могут быть общими

Актуальная октябрьская OTA 8052 и заводская сентябрьская 8054 имеют **побайтно одинаковые** `TvSettingsPlus`, `KuSettings`, `KuSourceRJ`, `KeystoneCorrection`, `trdservice`, `trdmiddle`, `RuiYunOta`. Поэтому отдельные версии кода UI делать не требуется до доказанного отличия. Функции, зависящие от железа, скрываем по capability-профилю.

## Источники

- [Аудит OEM Binder/JNI и меню](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/blob/research-oem-settings-api-20261020/analysis/OEM_API_8052_Latest/IMPLEMENTATION_RU.md).
- [Цепочки Intent и component](../Deep_Stock_Audit_20261021/OEM_INTENT_CALL_CHAINS_RU.md).
- [Общий APK дифф](../Latest_8052_OTA_vs_8054_Stock/README.md).
