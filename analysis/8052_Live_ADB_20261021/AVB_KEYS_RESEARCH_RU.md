# Everycom CineLux 8052 — AVB и OTA ключи: сверка с AOSP (21.10.2026)

**Важно: никаких изменений прошивки/подписей не выполнено.** Это анализ **публичных** ключей и опубликованных проверок, не утверждение о поддержке кастомного OTA загрузчиком.

## Подтверждённые подписи и их различия

1. В заводских **исходных PKG 8052/8054** извлечены `vbmeta_a` и `vbmeta_system_a`. Обе ревизии имеют идентичный **AVB public key**, `SHA256_RSA4096`, флаги `0`, rollback index `0`. SHA-256 **полного AVB-формата публичного ключа**: `dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe`. См. `analysis/HDMI_Comparison/AVB.md`.
2. Публичный тестовый ключ **AOSP external/avb/test/data/testkey_rsa4096_pub.pem** (официальное дерево: https://android.googlesource.com/platform/external/avb/+/refs/heads/main/test/data/ ) был приведён к бинарному формату AvbRSAPublicKey (`big endian: key_num_bits, n0inv, modulus, RR`). Получен SHA-256: `7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6`. **Не совпадает** с `dcf38bad…`. Это отвергает *конкретную* гипотезу об использовании стандартного AOSP RSA4096 тестового ключа в **этих заводских PKG**, но не исключает другие публичные, широко применяемые OEM ключи.
3. В **октябрьской OTA 8052.1.0.4** сертификат `META-INF/com/android/otacert` идентифицирован как публичный AOSP `testkey.x509.pem`. В позднем корректном разборе `analysis/RUIOS_OTA_Signatures/` криптографическая подпись **метаданных payload** проверена как RSA-2048/SHA-256 этим сертификатом. Ранний отчёт `analysis/RUIOS_OTA_Comparison/8052/signature_check.json` содержит `matches_embedded_ota_test_cert=false` из-за неполного первого метода извлечения; не использовать его как итоговую оценку.
4. Рабочий аппарат 8052.1.0.4 сообщает `verifiedbootstate=green`, `vbmeta.device_state=locked`, `vbmeta.digest=6fa46834…`. Последний digest — **хеш vbmeta**, не хеш открытого RSA-ключа. Публичный ключ **актуального `vbmeta_b`** ещё не извлечён из живого устройства и может отличаться от августовского заводского PKG.
5. **Частные RSA-ключи** никаким образом не восстанавливаются из открытого ключа, сертификата, SHA-256 fingerprint или `vbmeta.digest`; совпадение OTA testkey не гарантирует принятия кастомных разделов загрузчиком.
6. Шифрование OEM PKG и возможная упаковочная подпись — другие механизмы. Открытый/общий ключ расшифровки OEM PKG не является ключом подписи Android AVB. Существуют также platform APK signing certs и `otacerts.zip`.

## Новый сбор информации

Нужен **один** итоговый run read-only TXT-файла `everycom_8052_ONE_SHOT_DEEP_ADB_20261021.txt` из Termux:
- проверка настоящего `adb shell su -c id`, таймаут 15 сек;
- карта A/B, fstab и AVB-свойства;
- dumpsys OEM приложений, демо, AirPlay, Miracast, Settings, OTA;
- thermal, hwmon, fans, input key names, read-only I²C names;
- **если uid=0 подтверждён**, GZIP+Base64 **только первых 64 KiB** `vbmeta_a`, `vbmeta_b`, `vbmeta_system_a`, `vbmeta_system_b` в одном TXT. Никаких заводских секретных или калибровочных разделов.

**После получения TXT** декодировать дампы, извлечь из AVB заголовка `public_key_offset/public_key_size`, SHA-256 ключа, проверить криптографическую подпись самой vbmeta и сравнить с эталоном `dcf38bad…` и `7728e30…`. `verify_image` без `--key` проверяет корректность подписи относительно вложенного ключа, но **не доказывает доверие загрузчика**.

## Источники

- Внутренний статический анализ: `analysis/HDMI_Comparison/AVB.md`, `analysis/Full_Audit/README.md`, `analysis/RUIOS_OTA_Comparison/ENGINEERING_SUMMARY_RU.md`, `analysis/RUIOS_OTA_Signatures/README.md`.
- Официальный Android Verified Boot: https://android.googlesource.com/platform/external/avb/+/refs/heads/main/README.md
- AOSP тестовые AVB ключи: https://android.googlesource.com/platform/external/avb/+/refs/heads/main/test/data/
- Android подпись APK и OTA: https://source.android.com/docs/core/ota/sign_builds
- MediaTek reference secure boot (не спецификация этого MT9660 OEM): https://baylibre.pages.baylibre.com/mediatek/rita/device/mediatek/mtk-android-12/docs/bootloader/secure-boot.html

**Статус установки кастома:** заблокирован до проверки реального AVB, допускаемого trust anchor, безопасного восстановления и фактических прав. Публичный OTA-testkey этого препятствия не снимает.
