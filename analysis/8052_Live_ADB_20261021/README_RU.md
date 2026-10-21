# Живые ADB-проверки Everycom 8052: 21 октября 2026

Источник: два присланных владельцем TXT-отчёта, особенно `everycom_8052_extra_20261021_215945.txt`. Это только **инженерное резюме без идентификаторов, полного системного дампа, адресов/MAC, серийных номеров**. Дамп не включён в репозиторий.

## Подтверждено

| Параметр | Значение и следствие |
| --- | --- |
| SKU | `ro.rjpj.machine.id=8052`, 1 HDMI, Everycom |
| Версия | `RUIOS.8052.1.0.4`, `eng.suhaix.20261012.025220`, Android 13 |
| Сборка | `userdebug/test-keys`, `ro.debuggable=1`, `ro.adb.secure=0`, SELinux Permissive. Публичные заводские test keys и открытый adb могут быть рисками. |
| Root | `/system/xbin/su` существует, но **не исполнялся** в отчёте, root не доказан |
| Bootloader / AVB | `ro.boot.vbmeta.device_state=locked`, `ro.boot.verifiedbootstate=green`; править system на устройстве или прошивать модифицированные разделы без проверки совместимого AVB-ключа/разблокировки/доверенной установки **нельзя** |
| OTA | A/B, активный `_b`, `bootctl`: 2 слота / current 1, `update_engine=running`. `ro.rjpj.yunota.url=mt9660/8052/8052_ota.json`. Публичная GitHub OTA не становится установимой лишь от смены URL |
| Разделы | Существуют `super`, `boot_a/b`, `vbmeta_a/b`, `vbmeta_system_a/b`, `dtbo_a/b`, `bootdata_a/b`, `tvconfig_a/b`, `tvservice_a/b`, `linux_rootfs_a_a/a_b`, `3rd_a_a/a_b`, factory, persist, private, eeprom, project_id. OEM-данные не трогать |
| ФС | Android system/vendor/product/system_ext — EROFS read-only; `/data` — F2FS; `/vendor/tvconfig` — RW ext4; bootdata TVservice Linux_rootfs защищены AVB по fstab |
| Settings | `development_settings_enabled=1` уже, `settings get global adb_enabled=0` несмотря на рабочий ADB (не считать поле надёжным индикатором ADB); стандартный implicit SETTINGS разрешается в `com.my.settings/.SettingActivity`; HOME в `com.zeasn.whale.saas`; `com.android.tv.settings.MainSettings` и `uicustom.MainActivity` доступны в манифесте |
| Thermal | `thermal_zone0=mtk-thermal`, в момент опроса 58000 (58°C). Android HAL CPU 57°C, кэш 62°C. `apu-thermal` и `gpu-thermal` disabled, `temp` Invalid argument. Остальные HAL температуры 0.0 не считать реальными датчиками. `thermalservice Thermal Status=0`. |
| Linux trip | `mtk-thermal`: `hot=80000` (80°C), `passive=122000/125000` и `critical=135000`; не выдавать за допустимые температуры LCD/LED или за весь OEM тепловой алгоритм |
| Fan | HAL `CoolingDevice{name=fan,value=0}`, но нет подтверждённого RPM; Linux `cooling_device0=cpufreq-cpu0,cur_state=0,max_state=4` — это throttling CPU, **не вентилятор**. Цифровую кривую вентилятора пока не нашли |
| Dreams | `screensaver_enabled=1`, `screensaver_components=null`, `dumpsys dreams`: `mCurrentDream=null` на момент сбора. Нет доказательства, что Dream никогда не запускается |
| TrdDreamPic | `com.trd.dream/.DreamSceneService` — реальный `android.service.dreams.DreamService`; не удалять до анализа |
| RetailDisplay | настоящий package = `fusion.android.tv.demo`, установлен в `/system_ext/priv-app/RetailDisplay/`; дополнительный отчёт ошибочно запрашивал `com.android.retaildemo`, поэтому вывод о его receiver/services **неполный** |
| AirPlay | `com.android.toofifi` установлен, сохраняем |
| Miracast | `com.mediatek.miracast` установлен в `WFDSinkTest`; имеет `MiracastServiceReceiver` на BOOT_COMPLETED; сохраняем |
| Logo | `bootlogo.ini` явно указывает `type=JPEG;path=/boot0.jpg;width=1920;height=1080`; `boot0.raw` существует, но **не используется** описанным `[logo]` и его роль пока неизвестна. `boot0.mp3` присутствует |
| ToF | sysfs I²C зарегистрирован `2-005c` с именем `tof_nds03`, хотя `ro.rjpj.support.toffunction=0`. Это не доказывает, что аппаратный ToF работает/должен быть включён. |
| Пульт | `getevent -pl` показал виртуальные `trd_keyinput`, но не захвачены реальные нажатия; маппинг SETTINGS/FOCUS/SOURCE на пульте всё ещё требует интерактивной проверки |

## Следствия для Custom v0

1. Доработанный информационный экран `ThermalInfoActivity` может показывать `mtk-thermal`/CPU, но не LCD или LED и не RPM из `fan=0`. Подпись сырых узлов обязательна.
2. Сохраняем `FTAirplayWireless`, `WFDSinkTest`, `KuSetupWizard`, `trdservice`, `RJBluetoothSpeaker`.
3. `RetailDisplay` — приоритетный кандидат на исследование, не удалять по одному имени. `TrdDreamPic` — реально DreamService, удаление пока отложить; можно после проверки выключить лишь штатную заставку.
4. `boot0.jpg` и MP3 патчить только при правильном профиле 8052; `boot0.raw` не менять до атрибуции, проверку AVB bootdata обязательно пройти.
5. **Критический gate:** locked/green AVB = пока никаких прошиваемых кастомных пакетов даже при наличии `su`. Разработку исходников можно продолжать.
6. Developer options уже включены на тестовом 8052, но статус надо проверить в 8054 и после first boot/сброса для Custom v0.
7. Отсутствие заводских полных thermal fan curves в Android Thermal HAL не доказывает отсутствия аппаратного MCU управления.

## Оставшиеся read-only проверки

- `adb shell su -c id` — только подтвердить root, не трогая разделы.
- `dumpsys package fusion.android.tv.demo` и активные службы/приёмники — закрыть RetailDisplay gate.
- При отдельном согласованном сеансе — нажатия Settings/Source/Focus через `getevent -lt`.
- Статическое исследование `RuiYunOta` APK для конфигурации hostname + формата GitHub OTA и аппаратного/AVB контроля.
- Проверка работающих сенсоров LCD/LED через TRD Binder, без записи PWM/I²C.

Следующий короткий диагностический скрипт на телефоне: `everycom_8052_focus_check_termux.sh`; сохраняет TXT в Downloads и не изменяет проектор.
