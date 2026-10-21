# Custom v0 — две успешные STAGING сборки (НЕ прошивать)

**Дата сборки:** 2026-10-21.  
**GitHub Actions:** https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/actions/runs/39624844811 (оба задания **SUCCESS**).  
**Статус:** подготовленные **APK-overlay ZIP**, а **не** модифицированные `system.img` / `super.img`, не `update.pkg` и не установочный BIN.

| Сборка | Верифицированный стоковый оригинал | GitHub artifact | SHA256 внутреннего staging ZIP | Размер внутреннего ZIP |
|---|---|---|---|---:|
| **8052 (1 HDMI)** | `RUIOS.8052.1.0.4`, октябрьская OTA ZIP с подтверждённым SHA | [cinelux-custom-v0-8052-NONFLASHABLE](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/actions/runs/39624844811) | `7cb5f6cd169bae4abce77601e80602570cc78dbfc364866251ad093e5cd85e46` | 26 395 985 байт |
| **8054 (2 HDMI)** | `RUIOS.8054.1.0.1`, сентябрьский PKG внутри SHA-проверенного RAR, AES decrypted и извлечён исходный EROFS | [cinelux-custom-v0-8054-NONFLASHABLE](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/actions/runs/39624844811) | `4453b57de7a9fc726aef48bb4c77399abbc1d339c2e6be9109b2da32987c438c` | 26 396 287 байт |

**Как скачать:** перейти по ссылке запуска GitHub Actions → внизу страницы раздел **Artifacts** → скачать нужный `cinelux-custom-v0-8052-NONFLASHABLE` или `cinelux-custom-v0-8054-NONFLASHABLE`. GitHub даст внешний ZIP, **внутри находится основной staging ZIP** и `*_build_manifest.json` с хешами стоковых APK. Срок хранения артефактов установлен на 30 дней.

## Реальные результаты

- Общий APK FLauncher 0.18.0 загружен с **официального GitLab** и хеш зафиксирован: `376fc528c880cdf7c7c04b2d3708c69f911144498218babb6300808b772af32e`; `me.efesser.flauncher`, Android 13 API 33 поддержан в APK metadata.
- Реально собран и подписан development-ключом `org.cinelux.settingsshortcut`; создаёт иконку «Настройки Android TV» и явно запускает `com.android.tv.settings.MainSettings`.
- В обоих profiles удалось распаковать и **проверить наличие/хеши** сохранённых `KuSetupWizard`, `KuSettings`, `TvSettingsPlus` и целевых `zxlauncher`, `zxstore`.
- Для 8054 отдельно доказано наличие в оригинале `preinstall_del` Netflix, Prime Video и YouTube. По planned removal Netflix и Prime исключаются, YouTube сохраняется.
- Проверка ZIP CRC и целостности содержимого прошла в обоих jobs.

## Что НЕ сделано (важные ограничения)

- Собранный комплект ещё не изменяет исходный `system.img`/EROFS. Все удаления пока представлены **REMOVALS.txt** и проверяемыми хешами исходных APK; сами старые приложения **не удалены из изменённого образа**, потому что такой образ не создавался.
- `KuSettings` целиком **сохранён** до завершения миграции сервисов; `KuSetupWizard` сохранён по решению пользователя.
- Пока нет физического испытания FLauncher в роли HOME, Android TV shortcut, YouTube, 4K HDR, HDMI1/2, Bluetooth и первого запуска.
- Пока не проверены особенности системной установки Flutter APK (`extractNativeLibs`, упаковка `.so`, ABI), подпись AVB/OTA, размеры dynamic partitions, SELinux xattrs/UID/GID, безопасный rollback.
- Подпись SettingsShortcut **временная** и не предназначена для постоянного обновляемого приложения; в финальной сборке нужен один стабильный приватный signing key проекта (не секрет OEM).
- Ничего не загружали на проектор; не создавали ни одного установочного образа/PKG/BIN.

## Что будет после ADB данных

Только после установления реального AVB/загрузчика, схемы разделов и recovery метода:
1. исправить возможные проблемы APK (native lib/compression, stable signer);
2. применить manifest к **копии штатных разделов** с сохранением owners/modes/xattrs/SELinux context;
3. сформировать два отдельных модифицированных EROFS image, проверить в offline reader, сравнить с baseline;
4. затем отдельно решать формат доставки/подпись/откат и испытания на настоящих 8052 и 8054.

**Не переименовывать staging ZIP в update.zip и не передавать в обновление системы.**
