# Рассмотрение Lumen Home как общего лаунчера для кастома на стоке Android 13

**Источник:** [kmuradoff/lumen-os](https://github.com/kmuradoff/lumen-os), Apache-2.0 для основного кода (специфичные исключения отмечены в LICENSE/NOTICE). Lumen OS является системой Android TV 14 на базе LineageOS 21 для XGIMI, **но переносить всю систему в наш проект не планируется**. Рассматриваем только независимо реализованный HOME/UI и архитектурные идеи.

## Что реально есть в коде Lumen Home

- `apps/Z9xHome`, package `org.z9x.home`; `HomeActivity` содержит HOME/ленты и D-pad навигацию.
- Фоновое небо `SkyView`, Home/Apps/Projector, карточки и недавние программы.
- `ProjectorBridge` выносит *все* XGIMI-specific действия в отдельный пакет `org.z9x.projector`. Лаунчер не вызывает XGIMI HAL сам; он посылает `org.z9x.projector.action.SHOW_PANEL/SHOW_SOURCE` и читает защищённые ContentProvider, использует пакет `org.z9x.updater`.
- В `App.java` есть подсчёт повторяющихся аварийных завершений и упрощённый безопасный экран после трёх аварий за минуту (реализация находится в исходниках, а не штатное свойство всех Android).
- `Launch.java` запускает приложения как обычные Intent, а проекторные карточки делегирует `ProjectorBridge`.

**Вывод:** Архитектура (визуальная оболочка отдельно, проекторные функции отдельно) хорошо подходит для нас.

## Почему нельзя просто установить Z9xHome.apk

1. В исходном AndroidManifest.xml `apps/Z9xHome` указано `minSdkVersion=34` и `targetSdkVersion=34` (**Android 14**). Наши оригинальные RUIOS — **Android 13 / API 33**, поэтому установщик Android 13 не примет APK с minSdk 34.
2. Исходный Home использует пакетные контрактные имена XGIMI `org.z9x.projector`, `org.z9x.tvinput`, `org.z9x.updater`, которых нет в штатной Everycom RUIOS. Поэтому карточки «Источник», «Проектор» и «Обновление» не заработают из коробки.
3. Часть функций требует platform-signature/privileged разрешений (HOME switching, установка пакетов, usage stats, некоторые TV Provider API). Подписать APK своим ключом и положить в `system` **не равно** получить все заводские разрешения Android 13 и совместимость со службами.
4. Исходный UI может предполагать TV Provider, Android TV 14 конфигурации, пакетные классы и ресурсные идентификаторы несуществующих на нашем Android компонентов.
5. `SkyView`, фоновые изображения, погода, карточки и анимации следует проверять по производительности на нашей реальной GPU/дисплей-конфигурации, а не предполагать «плавно как на Z9X».

## План разумного переноса

**Вариант A (предпочтительный при сохранении понравившегося интерфейса):** форк **только** `apps/Z9xHome` под Android 13/API 33, без системного образа Lineage.

- На первом проходе адаптировать только HOME/Apps и статичный или упрощённый фон, то есть чистый launcher без проекторных зависимостей.
- Перенаправить `ProjectorBridge` на **наш локальный адаптер**, который первоначально только открывает штатный Android TV Settings `com.android.tv.settings`, `KuSourceRJ` и OEM интерфейсы через разрешённые действия. Ни одной прямой записи в I2C из HOME.
- Восстановить правильный D-pad/Back/Home, last app, фокус, fallback HOME и сохранение настроек лаунчера.
- Чуть позже, после статического аудита и runtime-диагностики, добавить карточки «Проектор/Источники»; разный набор HDMI и ToF определять capability-профилем 8052/8054.
- Не копировать XGIMI-specific `org.z9x.projector` API и не надеяться на одинаковые HAL.
- При распространении производной работы соблюдать Apache-2.0 и условия лицензий реиспользуемых зависимостей, сохранить NOTICE/атрибуцию.

**Вариант B (резервный прототип):** простой существующий HOME, совместимый с Android TV 13, для проверки устранения `zxlauncher` до начала большого UI-порта. Не выбирать конечный лаунчер до результатов измерения памяти, отзывчивости пульта, потребления CPU и стабильности.

## Контракт лаунчера для обеих версий

```text
CommonLauncher
  HOME / Apps / Settings shortcut / HDMI tiles / Projector tiles
     |
     +--> CommonSettingsNavigator
     |       `com.android.tv.settings` (TvSettingsPlus)
     |
     +--> ProjectorBridge_8052_8054 (нашей разработки; пока интерфейс, не исполняемый сервис)
             ├── проверка machineId + реальный capabilities
             ├── источники -> KuSourceRJ
             ├── фокус/трапеция -> TvSettingsPlus + штатные TRD
             └── OTA -> RuiYunOta
```

На начальном этапе HOME лучше держать максимально «тупым» и стабильным. Ядро логики — в существующем Settings/OEM адаптере. Тогда будущая смена лаунчера не нарушит физические функции проектора.

## План испытаний перед удалением zxlauncher

1. Установить/задействовать проверенный HOME и убедиться, что он становится default HOME после reboot и standby/wake.
2. Проверить нажатия HOME/Settings/Input/Back и переходы между HDMI/Android.
3. Запустить штатные настройки/фокус/трапецию через отдельные проверенные intents, убедиться, что нет вызовов `com.zeasn.whale.saas`.
4. Проверить восстановление после crash-loop (backup HOME/восстановление через ADB) прежде, чем удалить штатный HOME из будущей прошивки.
5. Проверить права Android TV, пакетный установщик и обработку нескольких пользователей, если есть.
6. Тестировать сначала на одном устройстве и делать два аппаратно-профильных пакета.

## Граница проекта

**Не переносим** LineageOS 21, XGIMI HAL, OTA-пакеты, recovery, подписывающие ключи, boot/vbmeta и ядро Lumen OS. Интересует лишь UX и разнесение HOME и аппаратной логики.

## Проверенные ссылки

- [Lumen OS README.ru.md](https://github.com/kmuradoff/lumen-os/blob/main/README.ru.md)
- [Z9xHome AndroidManifest](https://github.com/kmuradoff/lumen-os/blob/main/apps/Z9xHome/AndroidManifest.xml)
- [Z9xHome ProjectorBridge](https://github.com/kmuradoff/lumen-os/blob/main/apps/Z9xHome/src/org/z9x/home/proj/ProjectorBridge.java)
- [Z9xHome App safe-mode](https://github.com/kmuradoff/lumen-os/blob/main/apps/Z9xHome/src/org/z9x/home/App.java)
- [License](https://github.com/kmuradoff/lumen-os/blob/main/LICENSE)
