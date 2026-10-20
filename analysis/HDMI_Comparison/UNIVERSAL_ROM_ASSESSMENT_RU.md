# CineLux 1 HDMI / 2 HDMI: сводный инженерный аудит

Дата: 20 октября 2026. Исследования выполнены **статически на заводских PKG**; ни один проектор не прошивался.

## 1. Вердикт по универсальной прошивке

**Общая кодовая база и сборочная система — реалистичны. Один универсальный заводской PKG, гарантированно работающий на обеих платах, — не подтверждён.**

- Обе ревизии основаны на MediaTek MT5873, Android 13 / SDK 33; совпадают GPT, кодовое имя `griggs`, аппаратные интерфейсы и все четыре логических раздела (`system_a`, `vendor_a`, `product_a`, `system_ext_a`).
- Android-файлы в сумме: 3 944 общих пути, 2 267 идентичных, 1 677 отличаются; 4 файла уникальны для 1 HDMI, 12 для 2 HDMI.
- Отдельный Linux rootfs: 848/878 файлов одинаковы. `tvconfig`: 804/812 одинаковы. `tvservice`: 135/185 одинаковы. `project_id`: файл одинаков.
- Отличаются `boot`, `mboot`, `dtbo`, `optee`, `persist`, `tvconfig`, `tvservice`, `factory` и часть низкоуровневого vendor. Их смешивание без подтверждённой аппаратной ревизии небезопасно.
- Критичные конфигурации с различиями: `board.ini`, `BasicSound_HDMI.ini`, `BasicSound_DTV.ini`, `BasicSound_MM.ini`, `gammatable_1.ini`, `ConfigDefaultValue.ini`, `dtbo_mapping.ini`, `boot0.jpg`.
- Отличаются и сервисы телевизионной подсистемы Linux (`dtv_svc`, `app_man`, `libmediatek_tv_services.so`, `libmtal*.so`, и другие).
- **Рекомендуемая архитектура:** общие настройки, Android-приложения и Projector Control; заводские аппаратные профили для 1 HDMI/2 HDMI. Сначала два артефакта из единого дерева исходников. Универсальный паковщик/установщик только после проверки идентификации платы и восстановления.

## 2. Подписи и ограничения установки

- Оба заводских PKG расшифровываются AES-256-CBC открытым ключом `MSTAR_SECURE/default`; зашифровать содержимое тем же ключом технически возможно, но это не доказывает возможность создать **валидную криптографическую подпись PKG**.
- В обоих заводских `vbmeta_a` и `vbmeta_system_a` используется **SHA256_RSA4096** (алгоритм 2), авторизационный блок 576 байт, флаги 0 и rollback index 0.
- Хеш сериализованного встроенного публичного ключа одинаков во всех четырёх образах: `dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe`.
- Закрытого RSA-ключа нет; переподписать через `avbtool` своим ключом можно технически, но доверие загрузчика к нему **не подтверждено**.
- В скрипте OEM присутствуют `setenv verify n` и `setenv devicestate lock`. Это не доказывает ни принудительного AVB, ни разблокированного загрузчика.
- Установочный скрипт опасен: `gpt clean mmc 0`, `wipeuserdata`, `partition erase mmc 0 persist`, `mmc erase.p eeprom_a`. **Нельзя экспериментально загружать чужой PKG на несовпадающей плате.**
- Варианты установки: (а) обратимые Android-приложения; (б) root при наличии восстановления; (в) fastbootd/инженерный режим при реальной поддержке разблокировки и AVB; (г) собственный USB PKG только после проверки требований его подписи и совместимости.

## 3. Системные APK и зависимости

- **Побайтно одинаковы:** `trdmiddle`, `RuiYunOta`, `MtkTvInput` и ряд системных компонентов.
- **APK отличаются:** `KuSettings`, `KeystoneCorrection`, `RuiAutoFocus`, `KuSourceRJ`, `TvSettingsPlus`, `trdservice`, `zxlauncher`, `zxstore`, `LiveTV`, `TvServices`, `Factory`.
- 2 HDMI: `KuSetupWizard`, дополнительные I²C JNI-библиотеки, раскладки пульта, лежащие в `preinstall_del` APK Netflix/YouTube/Prime Video.
- 1 HDMI: `Provision`.
- `TvSettingsPlus` уже содержит `ProjectorManager`, `I2CDevice`, `settingsi2c_jni` и обращения к MediaTek TV API.
- `RuiAutoFocus` использует `MotorJNI`, `RuiCameraApi`, ToF и JNI. `KeystoneCorrection` — `KeystoneUtil`, `I2CDevice`, `i2c_jni`, `IProjectorCtrl`. `trdmiddle` — `TrdSystemService`, `TofController`, `trd_jni`, `tof_jni`.
- Одинаковый файл `trdmiddle.apk` **не означает** одинаковое поведение оборудования — драйверы, JNI и конфигурация могут различаться.
- Различный SHA256 одного APK может означать изменение ресурсов, локализации, иконок, сборочного времени, библиотеки или логики. Требуется декомпиляция и нормализованный diff классов/методов; не приписывать изменения функциональности одному хешу.

## 4. Диагностика с живого проектора (ТОЛЬКО ЧТЕНИЕ)

Не открывать ADB TCP-порт напрямую в Интернет через проброс роутера. Если нужен удалённый доступ, использовать WireGuard/Tailscale VPN или попросить владельца прислать очищенные от персональных данных результаты.

```sh
adb shell getprop ro.product.cpu.abilist
adb shell getprop ro.zygote
adb shell getprop ro.build.fingerprint
adb shell getprop ro.vendor.build.fingerprint
adb shell getprop ro.boot.verifiedbootstate
adb shell getprop ro.boot.flash.locked
adb shell getprop ro.boot.vbmeta.device_state
adb shell getprop ro.boot.slot_suffix
adb shell getprop ro.build.type
adb shell getprop ro.debuggable
adb shell getprop ro.adb.secure
adb shell getenforce
adb shell id
adb shell command -v su
adb shell ls -l /dev/block/by-name
adb shell cat /proc/cmdline
adb shell pm list packages -s
```

Вывод `getprop` может быть пустым, а наличие `su` — не гарантировать рабочий root. Никаких `adb root`, `adb disable-verity`, `fastboot flashing unlock`, `dd of=`, `mtkupgrade` для начальной диагностики.

## 5. Критерии единой прошивки

1. Один Android framework и единая логика настройки оборудования на обеих ревизиях.
2. Автоматическое **достоверное** определение платы до применения несовместимого профиля.
3. Все аппаратные библиотеки и настройки сохраняются ревизионно.
4. У каждой платы проверенный возврат к заводскому состоянию, резервные копии калибровок.
5. Прогон тестов HDMI, CEC, звук, HDR, фокус, ToF, трапеция, пульт, сон, нагрев и OTA на **обоих физических устройствах**.
6. Только после этого — эксперимент с общим единым образом или безопасным установщиком.

## 6. Словарь

- **APK:** установочный пакет Android-приложения.
- **JNI:** способ, которым приложение Android вызывает нативную библиотеку `.so`.
- **HAL:** программный интерфейс управления конкретным оборудованием.
- **I²C:** соединение процессора с микроконтроллерами, датчиками и иной периферией.
- **VINTF:** декларация доступных аппаратных сервисов Android.
- **Vendor:** часть Android с драйверами и службами производителя чипа.
- **DTBO:** выбор аппаратного описания платы и периферии.
- **Super:** контейнер логических разделов Android (`system`, `vendor`, и т. п.).
- **AVB/vbmeta:** проверка целостности прошивки при загрузке.
- **AES:** симметричное шифрование прошивки; оно не заменяет цифровую подпись.
- **RSA:** цифровая подпись, доверенная производителем.
- **TEE/OP-TEE:** защищённая среда для ключей и привилегированных операций.
- **OTA:** штатное обновление через Интернет.
- **Root:** доступ суперпользователя к системе.
- **U-Boot/MBOOT:** загрузчик, который запускается до Android.

## Исходные отчёты
- [Структура и хеши Android](README.md)
- [TV-service и tvconfig](../TV_Service_Comparison/README.md)
- [Отдельная Linux-система](../Embedded_Linux/README.md)
- [Подписи Android](AVB.md)
- [Первичный анализ APK](../App_Research/README.md)
- [Технические ограничения прошивки](ENGINEERING_VERDICT.md)

Все выводы относятся к конкретным изученным пакетам, а не к аппаратному устройству FlixTone D11 без его проверки.
