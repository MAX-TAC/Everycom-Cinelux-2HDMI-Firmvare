# TvSettingsPlus MOD — карта замены KuSettings и зависимостей (стадия 1)

**Исходные данные:** SHA-проверенная OTA `RUIOS.8052.1.0.4` и оригинальная заводская `8054.1.0.1`. В этих двух сборках `TvSettingsPlus.apk` и `KuSettings.apk` побайтно совпадают. **Актуальная 8054.1.0.4 не исследована**.

**Цель:** обновить существующий системный пакет `com.android.tv.settings` через PackageManager, сохранив аппаратные OEM-бэкенды, затем безопасно отключить `com.my.settings` для user 0. Не изменять AVB, разделы и загрузчик.

## Сразу важный факт

`KuSettings` — `com.my.settings`: **11 Activity, 2 Service, 2 Receiver, 1 Provider**. Единственный функциональный receiver: `com.my.service.BootupReceiver` (BOOT_COMPLETED). Второй — `androidx.profileinstaller.ProfileInstallReceiver`, библиотечный служебный компонент; не переносить без причины.

### Собственные службы и загрузка

| Компонент | Что подтверждено в JADX/manifest | Для переноса |
|---|---|---|
| `com.my.service.MySetTimeService` | `onStartCommand`, `registerTimeTick`, `onReceive`; регистрация динамического time-tick receiver | Проверить, влияет ли на системное время или только обновляет UI; заменить стандартным TV DateTime либо мигрировать необходимый побочный эффект |
| `com.my.service.ScreenServices` | `startShot`, `takeScreenShot`, привязка к `SystemUI`, `SystemProperties.set`, чтение SharedPreferences | Отдельно перенести путь скриншота с корректными привилегиями, выяснить точный property и внешний интерфейс; без прямой миграции экран Screenshot может пропасть |
| `com.my.service.BootupReceiver` | `BOOT_COMPLETED`, `onReceive` с одной условной ветвью | Восстановить цепочку фактических запусков (возможно MySetTimeService/TimeService), прежде чем отключать пакет |

`KuSourceRJ` — **отдельный** системный пакет `com.coolux.source`, сохраняется полностью. В нём собственные `com.coolux.source.service.TimeService` и `com.coolux.source.service.BootupReceiver`. В `KuSettings/com.my.utils.IntentUtils` существуют `startSourceService` / `startSourceTimeService` и `setComponent` + `startService` в сторону `com.coolux.source`. **Отключение KuSettings без учёта этих стартов может нарушить функции, хотя сам KuSourceRJ не будет удалён.** Нельзя утверждать, что старт уже покрывается KuSourceRJ.BootupReceiver, пока не проверен lifecycle.

## Маршруты, которые нужно сохранить

| OEM действие/экран | Целевой системный компонент | Статус |
|---|---|---|
| Обычное `android.settings.SETTINGS` | `com.android.tv.settings/.MainSettings` | Готова текстовая Manifest-правка; runtime не проверен |
| Wi-Fi | `com.android.tv.settings.connectivity.NetworkActivity` | TV Activity в APK есть; проверить сохранение Wi-Fi setup |
| Bluetooth, сопряжение пульта | `BluetoothAccessoryActivity`, `AddAccessoryActivity` + AutoPair | Код есть; не удалять AutoPair / KuSetupWizard |
| Дата / время / язык | TV `system.DateTimeActivity`, `system.LanguageActivity` | Код есть; выяснить MySetTimeService |
| Установленные приложения | TV `device.apps.AllAppsActivity` | Код есть |
| Об устройстве | TV `about.AboutActivity` | Код есть; добавить модель / актуальную OTA |
| HDMI источники и источник при загрузке | `KuSourceRJ.BootSoureActivity`, `SourceSubMenuController` | Сохранить ID отдельных плат 8052/8054 |
| Режим питания | `KuSourceRJ.PoweronModeActivity` | OEM Activity есть |
| Изображение / яркость | `KuSourceRJ.BrightActivity`, TV `BrightnessModeSettingsFragment` / `PictureModeFragment` | Сопоставить реальные уровни без заводской калибровки |
| Звук / eARC | `KuSourceRJ.VoiceActivity`, TV `AudioOutputFragment` | Не трогать HAL |
| Трапеция, ручной фокус, ToF | `KeystoneCorrection`, `RuiAutoFocus`, TV `uicustom` | Использовать OEM Binder/JNI; не показывать factory reset calibration |
| Зеркальность проекции | `KuSourceRJ.ProjectModelActivity`, TV `ProjectorModeFragment` | Код есть |
| Цифровой zoom | `KuSourceRJ` / `RuiAutoFocus` | Точный безопасный UI-роут ещё не доказан |
| OTA | `com.rjpj.yunota.OTASystemNetworkUpdateActivity` | Сохраняем OEM OTA |
| Скриншот | `KuSettings.ScreenServices` → `SystemUI.TakeScreenshotService` | НУЖЕН ПЕРЕНОС/эквивалент; нельзя считать реализованным |
| Температуры | Thermal HAL: `cpu`, `/sys/class/thermal/thermal_zone0` | 8052 CPU/SoC ~61–67 °C на отдельных замерах; GPU/APU недоступны; только read-only |

## Неочевидные обратные зависимости (важно)

1. **`KuSourceRJ` → `android.settings.SETTINGS`**: обнаружен вызов в `com/coolux/source/utils/IntentUtils.java:171`. Добавление `android.settings.SETTINGS` в MainSettings восстанавливает **неявные** вызовы после отключения KuSettings.
2. **`KuSettings` → `KuSourceRJ`**: вызов `startService` из `com/my/utils/IntentUtils.java:258`. Перенести фактически необходимый запуск, не заменять KuSourceRJ.
3. **`KuSetupWizard` → `com.my.settings`**: клонированные `IntentUtils` вызывают `setComponent` и `startActivity` (`IntentUtils.java:196`). **Явный ComponentName в другом пакете невозможно перенаправить одним intent-filter в TvSettingsPlus.** Нужна проверка, вызываются ли эти пути при заводском сбросе; если вызываются, требуется модификация вызывающего APK либо отказ от полного отключения KuSettings.
4. **`TvSettingsPlus` → `KuSourceRJ`**: найден `setComponent/startService` в `ProjectorFragment.java:149`, `KeystoneCalibrationActivity.java:330`, `ProjectorSubMenuController.java:135`. Эти связи сохранять.
5. **`zxlauncher` и `zxstore` → `android.settings.SETTINGS`**: неявные переходы; до замены лаунчера возможен конфликт обработчиков.
6. **`trdservice`** содержит ссылки на `TvSettingsPlus`, OTA и сторонние OEM Activity. Пакет не отключать.

## Стоп-условия перед отключением `com.my.settings`

- [ ] Все функции обычного пользовательского OEM-меню доступны через MainSettings/раздел «Проектор».
- [ ] Реальные вызовы `BootupReceiver`, `MySetTimeService`, `ScreenServices` восстановлены и заменены/признаны ненужными по трассе.
- [ ] Внешние *явные* вызовы `com.my.settings.*` (особенно KuSetupWizard после factory reset) обработаны, а не просто перенаправлены фильтрами.
- [ ] 8052: проверен пакетный upgrade `TvSettingsPlus` (тот же package, signer, versionCode, privapp permissions, shared UID и ресурсы), отработан rollback.
- [ ] 8054: проверен его текущий фактический APK и системный профиль, а не только старый factory 1.0.1.
- [ ] Пройдены reboot/standby, пульт, Ethernet/Wi-Fi, Bluetooth, HDMI, фокус/трапеция, OTA и reset-путь.
- [ ] Безопасное восстановление `pm enable --user 0 com.my.settings` проверено.

## Техническое состояние

Собран **экспериментальный APK для 8052** на основе SHA-проверенного `TvSettingsPlus.apk` из OTA 8052.1.0.4. Сборка/подпись и статическая проверка успешны; 16 оригинальных DEX сохранены и `classes17.dex` добавлен. Проверены 140 штатных manifest-компонентов, 67 разрешений и 9 переходов в 4 вариантах экрана System. **Не установлен и не испытан на реальном проекторе; KuSettings оставлен включённым.** До отключения необходимы миграция screenshot/time/внешних явных вызовов, проверка текущей 8054, профили устройств и безопасный откат. [Сборка CI](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/actions/runs/39844298261).

## Дорасследование после успешного GitHub Actions JADX (2026-10-22)

[Запуск анализа](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/actions/runs/39836787344) проверил исходные APK прямо из SHA-верифицированной OTA 8052 и нашёл все целевые Java-файлы. Результаты — **статические сигналы**:

- `KuSettings.BootupReceiver.onReceive`: присутствует `BOOT_COMPLETED`, **прямых вызовов `startService`, `startActivity`, `bindService` не обнаружено**. Это **ещё не гарантия отсутствия косвенных побочных эффектов**.
- `KuSettings.MySetTimeService.registerTimeTick`: регистрируется `android.intent.action.TIME_TICK`; `onStartCommand` не содержал непосредственного системного вызова из проверенного набора.
- `KuSettings.ScreenServices`: в `onStartCommand` вызывается `startShot`, в `setKeyStore` — `SystemProperties.set`, в `takeScreenShot` — `bindService` и `com.android.systemui.screenshot.TakeScreenshotService`. Требуется функциональная миграция, иначе скриншоты могут перестать работать.
- `KuSettings.IntentUtils.startMyTimeService`: есть `startService`. `startSourceTimeService`: `setComponent + startService` для `com.coolux.source.service.TimeService`.
- `KuSetupWizard.IntentUtils.startSourceTimeService`: такой же явный запуск `KuSourceRJ.TimeService`. Это может независимо сохранять время после отказа от KuSettings, но нужно выяснить действительные вызовы.
- `KuSourceRJ.BootupReceiver.onReceive`: `BOOT_COMPLETED` найден, прямых сервисных вызовов из выбранных маркеров нет. `TimeService.onStartCommand` найден; назначение и требуемость выясняем.
- Все проверки этой секции относятся к **8052.1.0.4**. Текущую установленную 8054.1.0.4 пока не считали.

**Практическое решение:** не копировать весь `KuSettings` в `TvSettingsPlus`. Переносить только подтверждённые функции и внешние интерфейсы. До признания зависимостей заменёнными держать `com.my.settings` включённым.
