# OEM APK: зависимости и риски замены / отключения

**Статус:** предварительная карта по статическим JVM/DEX сигнатурам заводских 8052 (август) и 8054 (сентябрь) и уже выполненной сверке октябрьской OTA 8052. **Не является разрешением удалять пакеты.**

## APK по критичности

| APK | 8054 package | JNI | Зависимости/сигналы | Решение до живого теста |
|---|---|---|---|---|
| zxlauncher | не извлечено | mmkv | com.zeasn.launcher.INSTALL_SUCCESS | Кандидат на будущую замену, но проверить HOME, auto-start, keybindings, установку/обновление приложений, интенты OTA и запуск источников |
| zxstore | не извлечено | mmkv | com.zeasn.launcher.INSTALL_SUCCESS | Кандидат на будущую замену; проверить вызовы установки APK, магазин/лаунчер и общие действия INSTALL_SUCCESS |
| KuSettings | не извлечено | — | com.coolux.launcher.TIME_12_24, com.coolux.source, com.coolux.source.service.TimeService, com.rjpj.yunota | НЕ удалять: содержит OEM UI Bluetooth, яркость/источники, ссылки на OTA и приватные настройки |
| TvSettingsPlus | не извлечено | com_mediatek_net_jni, com_mediatek_twoworlds_tv_jni, settingsi2c_jni | vendor.mstar.force.video.rotation, vendor.mstar.rotation.angle, vendor.mstar.support.video.rotation, vendor.mtk.factory.disable.input | НЕ удалять: привилегированное Android TV Settings и OEM аппаратные регулировки; основной кандидат на расширение |
| RuiYunOta | com.rjpj.yunota | — | com.rjpj.yunota, com.rjpj.yunota.OTASystemLocalUpdateActivity, com.rjpj.yunota.OTASystemNetworkUpdateActivity | НЕ удалять: OTA-клиент и интерфейсы обновления, сохранить до собственного подписанного OTA и rollback |
| KuSourceRJ | не извлечено | — | com.coolux.source.service.TimeService, com.trd.common, com.trd.common.bean.ISerialCallback, com.trd.framework.ICommunicationCtrl | НЕ удалять: HDMI source/boot source, оптика, трапеция, TRD binder |
| KeystoneCorrection | com.rjpj.tcorrection | i2c_jni | com.trd.framework.IProjectorCtrl, com.trd.framework.ITrdSystemService | НЕ удалять: JNI геометрии, TRD binder |
| RuiAutoFocus | не извлечено | com_mediatek_twoworlds_tv_jni, focusvahysd, ruicameraapi_jni | com.rjpj.intent.action.camera.calibration.finish, com.rjpj.intent.action.copy.hybin, com.rjpj.tcorrection, com.rjpj.tcorrection.TCorrectionBroadcastReceiver | НЕ удалять: управление мотором и ToF |
| trdservice | com.trd.service | rjpj_private_function | com.rjpj.tcorrection, com.rjpj.tcorrection.TCorrectionBroadcastReceiver, com.rjpj.yunota, com.rjpj.yunota.OTACheckService | НЕ удалять: системная TRD служба, motor JNI |
| trdmiddle | com.trd.framework | com_mediatek_twoworlds_tv_jni, tof_jni, trd_jni, trdmiddle | com.trd.framework.ICommunicationCtrl, com.trd.framework.IMotorCtrl, com.trd.framework.IProjectorCtrl, com.trd.framework.ISensorCtrl | НЕ удалять: промежуточная TRD Binder/HIDL инфраструктура |
| Factory | mediatek.factorymenu.ui | com_mediatek_net_jni, com_mediatek_twoworlds_tv_jni, factoryi2c_jni | com.rjpj.tcorrection, com.rjpj.tcorrection.TCorrectionBroadcastReceiver, com.trd.factory, com.trd.factory.fan.FanActivity | НЕ удалять: инженерные функции, аппаратный I2C, резерв для диагностики |
| TvServices | com.mediatek.tv.service | com_mediatek_twoworlds_tv_jni | vendor.mtk.factory.disable.input | НЕ удалять: системные сервисы Android TV и обработка TV |
| LiveTV | не извлечено | com_mediatek_twoworlds_tv_jni | com.mediatek.tv.factory.cleanstorage, vendor.mtk.factory.disable.input | ПОКА НЕ УДАЛЯТЬ: TV source/input интеграция требует проверки |
| KuSetupWizard | не извлечено | — | см. машинный JSON | НЕ удалять: первичная настройка Android в 8054 |

## Отмеченные статически межприложенческие зависимости

- `zxstore` и `zxlauncher` используют совместимую строку действия `com.zeasn.launcher.INSTALL_SUCCESS`: **возможная** зависимость между магазином и уведомлением лаунчера об установке; требуется изучить отправителя и получателя в Manifest/коде.
- `KuSettings` ссылается на `com.rjpj.yunota.OTASystemNetworkUpdateActivity`: замена меню должна сохранить вход в штатный OTA-клиент.
- `trdservice` содержит ссылку `com.rjpj.yunota.OTACheckService`: OTA-клиент может использоваться не только из меню.
- `KuSourceRJ` и `RuiAutoFocus` ссылаются на интерфейсы `IProjectorCtrl`/`ITofCtrl`/`ITrdSystemService`: загрузка и переключение входов проходят через TRD, а не только activity.
- `TvSettingsPlus` загружает `settingsi2c_jni`: замена штатного системного меню без переноса высокоуровневой логики потенциально нарушит аппаратные регулировки.
- `KeystoneCorrection` загружает `i2c_jni`, `trdservice` загружает `rjpj_private_function`, `trdmiddle` загружает `tof_jni` и `trd_jni`: эти компоненты не являются косметическими приложениями.

## Важно: две эпохи сборок

Таблица ниже фиксирует ABI заводского 8054. Октябрьская 8052 побайтно совпадает по восьми ключевым APK: `TvSettingsPlus`, `Factory`, `KeystoneCorrection`, `KuSourceRJ`, `trdservice`, `trdmiddle`, `KuSettings`, `RuiYunOta`. `RuiAutoFocus` отличается только в десяти нормализованных методах. Для лаунчера/магазина прямой октябрьский SHA-сравнительный результат в данном отчёте ещё не получен.

## Проверки до решения об удалении APK

1. Сохранить исходный system/vendor без модификаций; подключить logcat/dumpsys для безопасных тестов на живом устройстве.
2. Разобрать AndroidManifest каждого APK: `HOME`, BOOT_COMPLETED, службы, broadcasts, providers, экспортируемые components, shared UID, подпись.
3. Построить граф `Intent`/Binder вызовов с направлением отправитель→получатель и обязательным сценарием воспроизведения.
4. Показать, кто запускает APK во время загрузки, переключения HDMI, выхода из standby, OTA, Bluetooth, настроек фокуса.
5. Тестировать сперва временное отключение соответствующего необязательного пакета с возможностью моментального возврата, не удалять файлы на этапе исследования.
6. Для каждого дефекта фиксировать класс, метод, условия, конкретный возможный путь сбоя и подтверждение; *детектированный подозрительный шаблон не является доказанным багом*.

## Непроверенные вопросы надежности

- Обработка нулевого ответа Binder/ServiceManager, отключения/смерти OEM-сервиса.
- Потоки/таймауты I2C, motor JNI, уведомление об окончании фокусировки.
- Отработка одновременных intents HDMI/keystone/focus, ожидание завершения конфигурации.
- Проверка привилегированных разрешений при вызовах из доработанного Settings.
- Возможность обхода загрузки через дефектный/удалённый HOME.
- OTA retry/rollbacks, контроль подписи, обработка потери сети и питания.

## Статус проверки ошибок

На этом этапе **нет подтверждённых эксплуатационных ошибок**. Наличие методов, которые могут быть опасны без проверок, не доказывает дефект. Следующее исследование должно сопоставить поведение через код и реальные журналы.
