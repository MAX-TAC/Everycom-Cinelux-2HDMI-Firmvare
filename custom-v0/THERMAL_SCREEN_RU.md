# Custom v0 — «Система → Температуры и охлаждение»

Статус: исходники read-only TV Activity готовы. APK, IMG, PKG, OTA **не собирались**. Изменения штатного TvSettingsPlus **не делались**.

## Уже реализовано

- Отдельный TV-экран `org.cinelux.settingsshortcut/.ThermalInfoActivity` с русскими подписями и кнопкой обновления, рассчитанный на пульт.
- Чтение доступных Linux `thermal_zone*/type,temp`, `hwmon/temp*_input`, `hwmon/fan*_input`, `cooling_device*/cur_state,max_state`; общий статус PowerManager Android.
- Автообновление раз в 10 секунд только при открытом экране. Избегаем постоянной фоновой нагрузки.
- LCD и LED в интерфейсе честно помечены «Датчик не подтверждён». **Нельзя** приписывать им значения SoC.
- Обороты показываются в RPM исключительно из `fan*_input`, а `cooling_device/cur_state` называется состоянием, не оборотами.
- Отсутствие показаний или SELinux-разрешений = «Недоступно» без обхода защиты.
- В будущем новый экран доступен отдельной иконкой в TV лаунчере, после сборки APK с новой Activity.

## Не завершено — интеграция непосредственно в «Система»

У штатного `TvSettingsPlus.MainSettings` пока не пропатчен экран «Система»: неизвестен точный Fragment / Preference для вставки элемента. Нужно исследовать его в реальном APK и подтвердить права после переподписи.

Когда получится это сделать, пункт будет вызывать явный Intent:
- package = `org.cinelux.settingsshortcut`
- class = `org.cinelux.settingsshortcut.ThermalInfoActivity`

Это позволит оставить оригинальные аппаратные службы и прочие функции TvSettingsPlus. Раньше того функциональный экран можно вызвать по ADB, **после установки APK**:

    adb shell am start -n org.cinelux.settingsshortcut/.ThermalInfoActivity

## Безопасность и диагностика

Запрет на изменение термозащиты, контроллеров вентилятора, PWM, fan curves, GPIO, светодиодной мощности. Никаких shell-команд, root и I2C в приложении. Официально показание LCD можно будет добавить только когда будет доказана его физическая привязка и реально доступный API.

При невозможности чтения датчиков сторонним APK исследуем OEM TRD API и минимальный read-only bridge с подходящими правами. Не отключать SELinux глобально.

Файлы: `ThermalInfoActivity.java`, `ThermalProbe.java`, AndroidManifest, русские строки, векторная иконка, изменённые будущие GitHub Actions Java-компиляция и проверка Activity в staging manifest.

Оба профиля: 8052 Everycom CineLux и 8054 FlixTone D11 Master. Сборка не запускалась.
