# Custom v0 — логотип, Android TV 11 анимация, бесшумный старт (8052 и 8054)

**Статус: подготовлены ТОЛЬКО исходники будущих изменений. Сборка НЕ ЗАПУСКАЛАСЬ. Файл прошивки НЕ СОЗДАН.**
Ветка: custom-v0-boot-visuals-silent-PREPARE-20261021. База: custom-v0-staging-8052-8054-20261021.

## Состав изменений

| Компонент | Планируемые замены |
| --- | --- |
| Ранний статический logo 1080p | Чёрный фон с надписью android tv и четырьмя цветными точками, JPEG 1920×1080: bootdata/boot0.jpg и tvconfig/bsp/common/misc/boot0.jpg |
| Статический logo 4K | Такой же дизайн, JPEG 3840×2160: tvconfig/bsp/common/misc/boot0_4K.jpg |
| OEM звук старта | Две валидные беззвучные копии boot0.mp3 в bootdata и tvconfig; не удаляем и не ломаем декодер |
| Android boot animation | Android TV 11 от khurramrizvi, вариант Working and Tested; без аудио; ZIP-кадры STORED: system/media/bootanimation.zip |

Ссылка на выбранную анимацию: https://github.com/khurramrizvi/atv11_bootanimation/tree/master/Working%20and%20Tested

Фиксированный Git blob SHA-1 исходника Working and Tested: 3b1f39b90f7ffe28d5c4a7219190d411d3913fc5. Top-level архив в репозитории другой. SHA-256 самого входного ZIP и число кадров будут записаны в manifest при выполнении подготовки.

**Настоящее разрешение кадров этого ZIP пока не подтверждено.** Скрипт при выполнении читает desc.txt и реальные размеры изображений и сохраняет оригинал. Опциональный режим --upscale-4k создаёт только масштабированный 4K, НЕ настоящую 4K детализацию; до проверки памяти на устройстве применять не рекомендуется. Ранние статические JPEG будут сразу двух требуемых размеров независимо от разрешения Android-анимации.

## Основание для замены

- 8052 (1 HDMI): RUIOS.8052.1.0.4, октябрьская OTA, оригинал boot0.jpg 1920×1080 имеет SHA-256 453a75b9a6d37227910065a2aefb13600fcda5a855cd95e2ef92d76308d75485. Две копии boot0.mp3 идентичны, SHA-256 0f41508a306beb457e4cf9ddd265b11d95879e5c7e82b52e07e6fed832014bf7.
- 8054 (2 HDMI): RUIOS.8054.1.0.1, сентябрьский factory PKG, оригинал boot0.jpg 1920×1080 имеет SHA-256 c61563b2580ab2a4a74cc3a958aa0c9f0b789cc19c96ecc5cddac4df7d5d56db. SHA 8054 MP3 НЕ установлен (известен размер 59 952 байта), поэтому скрипт сверит обе его копии между собой и запишет оригинальный SHA в будущий манифест.
- Общее для обеих ревизий: штатный boot0_4K.jpg 3840×2160 SHA-256 9d161b79603b1d2ddb0c23b0fe120a013775a7995f93296014fb24fe10ff1b9c.
- Документация оригиналов и их файлы доступны в исследовательской ветке inspect-stock-boot-visuals-20261021, раздел analysis/Boot_Visuals_20261021.

## Подготовленные исходники

- tools/prepare_boot_visuals_stage.py: проверка идентичности штатных файлов по SHA; генерация JPEG 1080/4K на чёрном фоне, двух копий тишины MP3 с параметрами штатной дорожки, проверка исходного ZIP и перепаковка с удалением аудиофайлов/аудиодиректив. Выход — только новый каталог с overlay и manifest.
- tools/build_custom_v0_overlay_stage.py: новый необязательный аргумент --boot-visuals-stage. Проверяет профиль и хеши ровно 6 ожидаемых файлов и при будущем запуске включает их в NONFLASHABLE staging ZIP вместе с существующими APK FLauncher и SettingsShortcut.

Ни существующий staging Custom v0, ни штатные образы, ни GitHub Actions не изменены и не пересобраны. Эта ветка не совпадает с branch-фильтрами запуска существующего workflow.

## Будущее выполнение — НЕ запускалось

Нужны Python 3 + Pillow, ffmpeg/ffprobe, fonts-dejavu-core. Указывать ТОЛЬКО распакованные копии конкретной заводской файловой системы, не системные каталоги включённого проектора.

~~~bash
python3 tools/prepare_boot_visuals_stage.py \
  --variant 8052 \
  --bootdata-root /tmp/stock-8052/bootdata \
  --tvconfig-root /tmp/stock-8052/tvconfig \
  --animation-zip "/tmp/atv11/Working and Tested/bootanimation.zip" \
  --out /tmp/cinelux-8052-boot-overlay

python3 tools/prepare_boot_visuals_stage.py \
  --variant 8054 \
  --bootdata-root /tmp/stock-8054/bootdata \
  --tvconfig-root /tmp/stock-8054/tvconfig \
  --animation-zip "/tmp/atv11/Working and Tested/bootanimation.zip" \
  --out /tmp/cinelux-8054-boot-overlay

# Только при последующем разрешении на создание промежуточного NONFLASHABLE ZIP:
# к штатной команде build_custom_v0_overlay_stage.py
# добавить --boot-visuals-stage /tmp/cinelux-8052-boot-overlay
# либо --boot-visuals-stage /tmp/cinelux-8054-boot-overlay
~~~

## Границы безопасности

1. Нельзя считать подтверждённым, что обе копии boot0.jpg/boot0.mp3 используются в реальном включении. Проверить активный источник по ADB/наблюдению.
2. У октябрьской 8052 в распакованных Android system/product готовый bootanimation.zip отсутствовал. Хотя Android bootanim существует, дополнительный vendor bootvideo может переопределять показ. Требуется ADB проверка актуальных путей приоритетов и служб.
3. Нет подтверждения, что иных звуковых сигналов запуска нет. В этом исходнике отключается только доказанная дорожка boot0.mp3 плюс звук внутри ZIP. Обычные медиазвуки, HDMI и Bluetooth не трогаются.
4. Не копировать целые разделы bootdata/tvconfig между 8052 и 8054. Менять исключительно перечисленные ресурсы с проверкой исходных SHA.
5. Любое будущее внесение замены в IMG/PKG зависит от проверки AVB/SELinux/UID/GID/rollback и безопасного восстановительного пути. Сейчас эти ресурсы не являются установочным образом.
6. Для будущего теста на проекторе начинать с native-разрешения Android-анимации, чтобы не получить bootloop из-за 4K-кадров.

**Запрещено передавать подготовительный overlay ZIP в OTA updater или переименовывать в update.zip.**
