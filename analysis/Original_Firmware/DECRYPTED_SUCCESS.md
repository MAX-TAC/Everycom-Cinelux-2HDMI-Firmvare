# Everycom CineLux 2-HDMI — расшифровка и восстановление Android 13 (20 октября 2026)

## Итог: ПОЛНОСТЬЮ РАСШИФРОВАНО И РАСПАКОВАНО ДЛЯ АНАЛИЗА

Файл `4KTOF摄像头双HDMI-智象简易版-DPLS定制-09.30.rar` содержит один `upgrade_image.pkg` — **полный установочный образ для конкретной платы**, а не просто инкрементальный OTA. Тот же образ НЕЛЬЗЯ без проверки платы прошивать на FlixTone D11 Master.

1. SHA-256 RAR: `170f745dc1711c2dae6410dd51f0a8bf5bb7c637e11b8dd3e5f59fbea8c388f3`.
2. SHA-256 PKG: `4abef5d594803d09c20316a7cd52ab623dd7fb1a228472eb0e243d6d750ebb4c`.
3. Контейнер обнаружен как `mstar_secure_new`. Заголовок: 256-байтовая область, `V_0.0.0`, `REE_OFFSET_START=0x1000`, `REE_OFFSET_LEN=0x4d8c0000`, `MTK.....` по 0x500 и `.....mtk` по 0x578.
4. **Ключ расшифровки найден** в исходниках проекта [theubusu/unixtract](https://github.com/theubusu/unixtract), раздел `MSTAR_SECURE`, ключ `default` (`CKB_D_UPG_Key256`). Алгоритм AES-256-CBC с нулевым IV на старте и цепочкой IV между 8 сегментами. После расшифровки: `gpt clean mmc 0`, `gpt create ...`, `filepartload`, `unlz4`, `partition swrite ...`.
5. Всего **33 сегмента**; стандартный LZ4 (все декодируются `lz4 -d`). Для многотомного `super` 12 Android sparse-обновлений описывают **одну и ту же логическую область**, поэтому их необходимо **накладывать на одинаковые адреса**, а не склеивать.
6. Восстановлен `super.img` размером **2 225 078 272 байта** (соответствует GPT), из него успешно извлечены EROFS: `system_a` 866 844 672 байта, `vendor_a` 262 610 944, `product_a` 77 152 256, `system_ext_a` 87 273 472 байта.
7. **Android 13** (SDK 33), `ro.build.version.security_patch=2026-04-05`, тип `userdebug`, заводская платформа `mt5873_cd`, product `griggs`, DTBO `mt5873_h1v1_cd.ini`. Vendor fingerprint: `MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/suhaixiong09300739:userdebug/test-keys`.
8. OEM APK: `KuSettings`, `KuSetupWizard`, `KuSourceRJ`, `RuiAutoFocus`, `KeystoneCorrection`, `trdservice`, `trdmiddle`, `zxlauncher`, `zxstore`, `RuiYunOta`, `FTAirplayWireless`. **Также уже имеется `TvSettingsPlus` в `/system_ext/priv-app`**. По названиям приложений нельзя заключать об их фактической безопасности или качестве без анализа кода.
9. Вендорский HAL включает `vendor.mediatek.tv.Mm.Mm.mtktvfapicustom`, `IMtkTvFApiCustom`, `IMtkTvFApiAudio`, `IMtkTvFApiDisplay`, `IMtkTvFApiInputSource`, `android.hardware.tv.input`, `android.hardware.tv.cec` и MStar hardware HAL. Это хорошие точки интеграции собственного ProjectorControlService.

## Безопасность и ограничения

- **Расшифровка НЕ равнозначна возможности прошить модифицированный PKG**. Контейнер включает отдельные области подписи/контрольных структур; подлинность и требования загрузчика к подписи пока не проверены.
- В U-Boot сценарии явно есть опасные команды: `gpt clean mmc 0`, `wipeuserdata`, `partition erase mmc 0 persist`, `mmc erase.p eeprom_a`. Это может стирать пользовательские и калибровочные данные, не проверять на FlixTone до точного совпадения аппаратных ревизий и способа восстановления.
- Сценарий задаёт `androidboot.selinux permissive`, сборка `userdebug` и `test-keys`: проверить безопасность позже на реальном устройстве; успешность применения этих свойств не подтверждена живым тестом.
- `project_id`, `persist`, `factory` и разделы с калибровками не включать в публичные публикации с реальных устройств. Здесь анализ выполнен на публичном заводском образе.

## Рекомендация

Для родственного **D11 Master** основная ветка — модификация подходящего родного Android 13 с сохранением HAL, медиакодеков и драйверов. В первую очередь заменить `zxlauncher` на Projectivy (тестом и с возвратом), восстановить `TvSettingsPlus` и исследовать зависимость `KuSettings`, `KuSourceRJ`, `RuiAutoFocus`, `KeystoneCorrection` от HAL. Встроить регулировки в Android TV Settings через собственный системный сервис. Эксперимент с LineageOS отделить, он требует работы с ABI, Treble/VINTF, AVB и средой восстановления.

## Файлы исследования

- [Расшифрованный сценарий](decrypted/upgrade_script.txt)
- [Отчёт по реконструкции всех 33 компонентов](reconstructed/README.md)
- [Android build.prop, список приложений, HAL](reconstructed/ANDROID_AUDIT.md)
- [Инвентаризация JSON](reconstructed/android_inventory.json)
- [Исходный код реконструкции sparse super](../../tools/reconstruct_cinelux.py)
- [Workflow полного анализа](../../.github/workflows/reconstruct-cinelux.yml)

**Все эксперименты только читали исходный PKG и извлекали файлы на GitHub runner. Ни одно устройство не прошивалось.**
