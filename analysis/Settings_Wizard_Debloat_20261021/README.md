# Аудит KuSetupWizard, KuSettings, TvSettingsPlus и очистка RUIOS — 21.10.2026

**Источник доказательств:** SHA-проверенная официальная октябрьская OTA `RUIOS.8052.1.0.4`; для 8054 сравниваются **только заводская `8054.1.0.1`** и её совпадающие APK. Исходная более новая 8054.1.0.4 не получена. Никакие пакеты не удалены и не прошивались.

## Практические выводы

- Из скриншота подтверждён рабочий `com.android.tv.settings/.MainSettings`. Это главный ярлык **«Настройки»** в будущем FLauncher.
- Для отдельного OEM меню есть ещё экспортированная `com.android.tv.settings/.uicustom.MainActivity`: предложено тестировать как ярлык **«Проектор»**. Эта Activity расположена **внутри** TvSettingsPlus, не в KuSettings.
- **Не удалять KuSetupWizard** до проверки сценария первого включения после factory reset, сопряжения пульта и provision flags: он package `com.android.provision`, имеет `SETUP_WIZARD` и `HOME` категорию.
- **KuSettings — цель удаления**, но требует решения по `BootupReceiver`, `ScreenServices`, `MySetTimeService`, скриншотам и связям с `KuSetupWizard`.
- `TvSettingsPlus` лучше сохранять как платформенную основу; в нём есть 475 совпадающих Java class-paths с AOSP Android 13 reference и 512 дополнительных, в том числе `uicustom=142` и `partnercustomizer=164`. Нельзя делать вывод об идентичности методов по совпадению имён.
- В TvSettingsPlus найдены конкретные **риски** factory calibration, HDMI capability mapping, audio eARC state и A2DP sink. Пока **нет подтверждённых воспроизводимых багов**.
- `zxlauncher` и `zxstore` запланированы к исключению после работы нового FLauncher; Netflix и Prime Video также исключить из factory 8054; YouTube сохранить.
- Тестовый AOSP platform certificate — подпись многих штатных APK, не ключ AVB OEM.

## Отчёты

1. [**SETTINGS_MIGRATION_FINAL_RU.md**](SETTINGS_MIGRATION_FINAL_RU.md) — полная карта функций KuSettings → TvSettingsPlus / KuSourceRJ; два Activity и конкретные места интеграции.
2. [**TVSETTINGS_BUG_RISK_REVIEW_RU.md**](TVSETTINGS_BUG_RISK_REVIEW_RU.md) — 12 адресных рисков изменённых OEM компонентов, влияние и рекомендации.
3. [**DEEP_SETTINGS_WIZARD_RU.md**](DEEP_SETTINGS_WIZARD_RU.md) — ~3 471 классов KuSetupWizard, ~3 470 KuSettings, ~5 796 TvSettingsPlus, записи по методам и ссылкам.
4. [**CRITICAL_METHOD_FLOWS_RU.md**](CRITICAL_METHOD_FLOWS_RU.md) — конкретные методы `next`, `resetFactoryCalibrationData`, `initBoardConfig`, `switchToHDMI`, `updateEARCSettingValueToDrive` и side-effects.
5. [**AOSP_TVSETTINGS_13_REFERENCE_RU.md**](AOSP_TVSETTINGS_13_REFERENCE_RU.md) — конкретное сравнение дерева классов официального Android 13 `android-13.0.0_r56` с OEM TvSettingsPlus, указаны ограничения методологий.
6. [**DEBLOAT_POLICY_RU.md**](DEBLOAT_POLICY_RU.md) — точные пути Netflix, Prime Video, YouTube, ZEASN в обеих оригинальных сборках.
7. [**debloat_build_manifest_proposed.json**](debloat_build_manifest_proposed.json) — будущий разделённый по ревизиям машиночитаемый manifest удаления/сохранения; **не исполняется**.

## JSON-результаты

- [deep_settings_wizard_analysis.json](deep_settings_wizard_analysis.json)
- [aosp_tvsettings_13_reference_diff.json](aosp_tvsettings_13_reference_diff.json)
- [critical_method_flow_indicators.json](critical_method_flow_indicators.json)

## Конкретные ограничения и следующий безопасный тест

Для 8054 существует factory 1.0.1, но нет новой оригинальной 1.0.4. Runtime 8052 и 8054, особенно выбор Settings Activity, binder privileges и аппаратные controls, ещё не проверены.

Проверить без модификации:
```sh
adb shell am start -n com.android.tv.settings/.MainSettings
adb shell am start -n com.android.tv.settings/.uicustom.MainActivity
```

Первая команда соответствует уже подтверждённому пользователем экрану; вторая ещё не проверена вживую. Не вызывать `resetFactoryCalibrationData`, `I2C` или ручные двигательные JNI методы ради эксперимента.

Перед изменением `TvSettingsPlus` после первых проверок потребуется подпись APK, platform privileges и независимая стратегия AVB/firmware update.
