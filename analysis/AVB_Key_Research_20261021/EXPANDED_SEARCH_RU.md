# Расширенный поиск AVB-ключа RUIOS MT9660 среди прошивок бюджетных китайских проекторов

Дата исследования: 2026-10-22. Только доступные публичные оригинальные образы и открытые источники; изменений на устройствах нет.

## Проверенный ключ

**SHA-256 в формате AvbRSAPublicKeyHeader (1032 байта)**: `dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe`.

RSA modulus первых 32 байт (public): `d8165a74a308a133f8e56c5509c85f1a98f39b84ffc313a1ed4a8f813fd68b2e`.

RSA modulus 512-байт SHA-256: `a26fa2e24631b26429bf8a9dcf23b359d5af05efefb842fdca89f9db3c0c5ed6`.

Algorithm ID 2 SHA256_RSA4096. НЕ путать с SHA256 образа vbmeta, сертификатом OTA и RSA-подписью внешнего PKG.

## Подтверждено по реальным прошивкам

| Образ | Источник | vbmeta SHA256 публичного ключа | vbmeta_system |
|---|---|---|---|
| Everycom 8052.1.0.1 (factory) | расшифрованный MStar PKG | dcf38bad...046cfe | тот же |
| FlixTone/Everycom 8054.1.0.1 (factory) | расшифрованный MStar PKG | тот же | тот же |
| RUIOS OTA 8052.1.0.4 | проверенный payload.bin из OTA ZIP | тот же | тот же |
| RUIOS OTA 8053 | проверенный payload.bin из OTA ZIP | тот же | тот же |

Отчёты: [stock 8052/8054](../HDMI_Comparison/AVB.md), [OTA 8052](report.json), [OTA 8053](ota8053_key_compare.json).

Это означает **одну пару AVB-ключей как минимум между тремя идентификаторами RUIOS**, но не доказывает, что её закрытая часть общедоступна.

## Проверка известных открытых разработческих ключей

[Автоматическая сравнительная проверка](known_key_corpus_match.json): просканированы 56 потенциальных ключевых/сертификатных файлов из трёх открытых репозиториев. 22 записи RSA-4096 (часть — дубликаты) были приведены к точному бинарному формату AVB с вычислением `n0inv` и `RR mod N`. Совпадений — **0**.

Источники:
- https://github.com/nccgroup/test_avb_key — AOSP, OnePlus, Realtek и другие ключи.
- https://github.com/alltechdev/haha-you-used-testkeys — проекты с AOSP AVB testkey.
- https://github.com/TheGammaSqueeze/UnisocBypass — общедоступные ключи другой платформы.

Тестовый AOSP RSA4096 = `7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6`, не совпадает с нашим.
Другой опубликованный тестовый Realtek RSA4096 = `ec2647574df2ea01127ee210f838965daa884e61888c49bbf6a9c59457f46b89`, не совпадает.

## Поиск по интернет-индексам

Сделаны поиски полного AVB SHA256, укороченного SHA, SHA RSA modulus и начальных байтов RSA modulus (слитный hex и побайтовая запись), а также названий MT9660, MT5873, RUIOS, szrjyun, MStar и AVB в русских, английских, китайских источниках. Независимых опубликованных совпадений нашего RSA4096 найдено **0**. Неиндексированные SDK/архивы остаются возможным источником.

## Сравнение с другими бюджетными китайскими проекторами

- https://github.com/BruBread/ProjectorRoot — оригинальная `backups/vbmeta_orig.img` от Magcubic/HY300 на RK3326: **algorithm ID 0, встроенный AVB public key отсутствует**, поэтому сравнение именно ключей невозможно. [Машинный отчёт](other_projector_vbmeta_comparison.json).
- https://github.com/qdvbp/mstar-tools — содержатся распространённые MStar RSAboot/RSAimage/RSAupgrade private keys, но **все три RSA-2048**, поэтому напрямую не совпадают с нашим AVB RSA-4096.
- https://github.com/MAX-TAC/Firmware-CN-Projectors/blob/main/analysis/ET32/partition_map.json — у Touyinger ET32 `sboot` начинается на `AA5E3FDAD01DDF4AFAFE67A1B53BBB8B`, то же начало 2048-битного RSAboot modulus из MStar default key. Это убедительное свидетельство повторного использования ключа в **другой MStar-цепочке**, но нет полной байтовой сверки ключа и это **не AVB-ключ**. ET32 основан на NL_MTK9255_D1E8, а не на нашем MT9660.
- https://4pda.to/forum/index.php?showtopic=847902&st=840 — участники в обсуждении MStar связывают RSAimage/RSAboot с подписью образов/загрузчика; это старый MStar-механизм, не равно Android AVB.
- https://github.com/kmuradoff/lumen-os — образцовый кастом для XGIMI Z9X, содержит релизные APK/OTA/APEX публичные сертификаты, не доказано, что содержит AVB-ключ нашего RUIOS.
- https://github.com/BruBread/ProjectorRoot и https://github.com/maximilian-sh/hy350max-badbox-removal показывают, что и в бюджетном сегменте используются разные SoC и загрузочные модели (Rockchip / Allwinner / MediaTek), поэтому единый AVB RSA у всех проекторов не следует предполагать.

## Отличайте три независимых группы секретов

1. MStar PKG AES + возможные RSAboot/RSAimage/RSAupgrade для secure wrapper: известные default ключи **могут** иметь отношение к упаковке и ранним загрузочным ступеням, но не обязаны управлять AVB.
2. Android OTA `payload.bin`: открытый AOSP test сертификат проверяет OTA metadata в 8052, но это другая цифровая подпись, не подпись доверия vbmeta загрузчиком.
3. Android AVB: `vbmeta`/ `vbmeta_system` содержат встроенную публичную RSA4096 часть. Для нового принятого загрузчиком образа нужен соответствующий приватный ключ или документированная поддержка смены корня доверия/разблокировки.

## Оценка и следующие направления

- Наиболее перспективны исходники именно **RUIOS/проекторного ODM** и ключевые настройки `BOARD_AVB_KEY_PATH`, `oem_prvk.pem`, `avbkey.h`, `default.avbpubkey` для MT5873/MT9660.
- Поиск только по целому SHA ключа не исчерпывает задачу; теперь известны hex-префикс RSA modulus и его независимый SHA для поиска в бинарных SDK и скомпилированных загрузчиках.
- Факт одинакового ключа между 8052/8053/8054 **не позволяет вычислить закрытый ключ** и не доказывает, что он `стандартный` в смысле опубликованный.
- `green/locked` на реальном 8052 и `setenv verify n` в заводском установщике требуют отдельного безопасного исследования, без изменения параметров загрузки.
- **Не шить перепакованный PKG**, не стирать заводские persist/eeprom/tvconfig до испытанного полного восстановления.

Автоматизированные результаты расположены на ветке `research-ota8052-avb-key-match-20261021`.
