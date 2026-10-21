# MT9660: тепловая защита, вентиляторы, LCD и необязательные idle/demo APK

**Дата:** 2026-10-21. **Статус:** статическая проверка ранее полученных заводских образов 8052/8054 и октябрьской OTA 8052.1.0.4; живых датчиков, RPM и fan curves пока НЕ считывали. Никаких прошиваемых образов/служб не изменяли.

## 1. Что подтверждено в исходниках/аудите

- TRD SDK / service: классы `com.trd.framework.ITemperatureCtrl`, `com.trd.sdk.TemperatureCtrl`, `com.trd.sdk.impl.TemperatureCtrlImpl`, `ISensorCtrl`, `SensorCtrlImpl`, `trdservice/ui/FanDialog`, `TemperatueDialog`, `ShutdownCoolDownDialog`; оригинальные Java-class paths в `analysis/Deep_APK_Comparison/apk_method_diff.json`, строки интересующих классов для `trdservice` и `trdmiddle`. Имена предполагают чтение/управление температурой и предупреждения, но сами по себе не доказывают реальные доступные показания или кривые.
- `Factory` содержит строку `com.trd.factory.fan.FanActivity` в списке межкомпонентных ссылок. Нужна расшифровка вызовов, прав и подтверждение работы на обоих SKU. **Не запускать заводские процедуры изменения Fan/PWM без резервной копии и понимания пределов.**
- `KuSourceRJ` содержит `com.coolux.source.activity.HighTemperatureActivity` в `analysis/Deep_Stock_Audit_20261021/oem_intent_call_chains.json`. Наличие компонента не подтверждает пороги.
- Для 8052 в `vendor/etc/init/android.hardware.thermal@2.0-service.mediatek.rc` объявлен сервис `vendor.thermal-hal-2-0-mock` -> `/vendor/bin/hw/android.hardware.thermal@2.0-service.mediatek`. Название mock не доказывает, что другая OEM термозащита отсутствует.
- В inventory kernel/vendor найдены `mt58xx-thermal.ko`, `mtk-module_thermal.ko`, `mtktv-thermal.ko`, `pwm-mt5896.ko`, `pwm_bl.ko`, `pwmadc-mt5896.ko`, `pwmscan-mt5896.ko`, `pwmseg-mtktv.ko`: `analysis/Deep_Stock_Audit_20261021/native_ota8052_vs_stock8054.json` и `analysis/HDMI_Comparison/comparison.json`. Важно: **наличие PWM-модуля не доказывает управление вентиляторами; PWM может использоваться для подсветки/экрана/другой периферии.**

### Непроверенное
- Наличие физического NTC на LCD, LED, радиаторе и адрес его чтения.
- Температура SoC != температура LCD. Не отображать одно под видом другого.
- Количество вентиляторов, их скорость в RPM, тахометры, возможность менять обороты.
- Функция управления оборотами vs ступенчатые пороги в MCU/TVservice; точные таблицы и hysteresis.
- В каком разделе находятся заводские пороги (board.ini, tvconfig, tvservice, firmware MCU) — не найдено прямой доказательной привязки.

## 2. Предлагаемое отображение Custom v0

В Android TV Settings -> «Система» -> «Температуры и охлаждение» предусмотреть **только показ данных**:
- «LCD-матрица» — показывать только если сенсор реально подписан/верифицирован, иначе «Датчик не подтверждён».
- «LED / радиатор», «Процессор» — только при подтверждении каждого канала.
- «Вентилятор 1 / 2», RPM — если существует достоверный тахометр (не подменять PWM % как RPM).
- «Режим охлаждения» = автоматический/состояние, но без права менять штатные предохранительные пороги.

Сначала подключить read-only источник через Android Thermal HAL/`dumpsys thermalservice` или `/sys/class/thermal`/`/sys/class/hwmon`; если информация идёт только через TRD Binder, определить контракт и signature/SELinux, добавить минимальное привилегированное API-чтение; никакого root-сервиса/фонового опроса с частотой, влияющей на стабильность.

**Никаких редактируемых fan curves/ручных RPM/управления светодиодной мощностью в v0**: реальный поток охлаждения LCD/LED и защитное охлаждение при выключении важнее тишины.

## 3. RetailDisplay / TrdDreamPic и AirPlay/Miracast

Инвентаризация 8052.1.0.4 (`analysis/Global_Firmware_Map_20261021/ota8052_init_permissions_keylayout.json`) подтверждает:
- `system_ext/priv-app/RetailDisplay/RetailDisplay.apk`;
- `system/app/TrdDreamPic/TrdDreamPic.apk`.

Оба имени также присутствуют в factory inventory 8052/8054 (`analysis/HDMI_Comparison/comparison.json`).

Это **пока только наличие файлов**, а не доказательство, что они запускаются при бездействии или безопасны к удалению. Полные manifest + зависимости обоих конкретных APK ещё не получены; `RetailDisplay` может быть службой демо/торгового режима, а `TrdDreamPic` — механизмом Dream/заставки, но нужно подтвердить реальные Activity/Service/Receiver, intents/permissions и возможные ссылки из OEM `TvSettingsPlus`, `trdservice`, `KuSettings`, `KuSetupWizard`.

Решение:
- `FTAirplayWireless` + `WFDSinkTest` (и связанный кастинг backend) **KEEP — сохраняем AirPlay и Miracast**.
- `RetailDisplay` -> REVIEW_BEFORE_REMOVE, исследовать Service/Receiver, использование retail mode и наличие зависимостей от первоначальной настройки.
- `TrdDreamPic` -> REVIEW_BEFORE_REMOVE, проверить `DreamService`, активный компонент screensaver и интеграцию с OEM сервисом.
- Никогда не удалять `BasicDreams`, `DreamManager`, `SystemUI`, `TvSettingsPlus` автоматически по сходству имён.
- Проверять reversibly: `pm disable-user --user 0` только после live manifests, backup/re-enable и с тестами reboot, standby/wake, FLauncher, HDMI, температуры. Пока **не отключаем ни один APK**.

## 4. Добавленная безопасная диагностическая процедура

`tools/collect_thermal_readonly.sh` — только **чтение** Android thermalservice, Linux thermal zones/trip points, cooling devices, hwmon temperature/fan/PWM и screensaver settings; пакетные имена для RetailDisplay/TrdDreamPic. Проводить после получения ADB доступа. Отчёт не содержит принудительных действий и не вызывает заводское FanActivity.

Важно: `trip_point_N_temp` описывает Linux thermal control, но **может не совпадать** с OEM порогами MCU, контролирующего поток воздуха.

## 5. Критерий решения об удалении

1. Извлечь `aapt dump badging` и `aapt dump xmltree AndroidManifest.xml` из APK 8052 и 8054, сравнить package/activity/service/receiver/signer.
2. Для каждого искать прямые cross-app Intent/ContentProvider/DreamService обращения в распакованных `TvSettingsPlus`, `KuSettings`, `trdservice`, `KuSetupWizard`, `zxlauncher`, `Factory`.
3. ADB: `dumpsys dreams` + `settings get secure screensaver_enabled`, `pm list packages -f`, `dumpsys package <фактический package>`, `dumpsys activity services`, `logcat` при idle/standby. Сначала только чтение.
4. И только при подтверждении реальной ненужности и отсутствия зависимостей — обратимое отключение на тестовом устройстве, сравнение до/после и возможное исключение из будущего Custom v0.

**Общий итог:** возможность вывести фактические температуры в «Систему» перспективна; заявлять температуру именно LCD, готовую кривую вентилятора или безопасное удаление двух APK пока рано.
