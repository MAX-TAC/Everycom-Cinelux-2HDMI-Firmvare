# MediaTek TV HAL против OEM TRD/RJ/HYSD — можно ли заменить OEM решения?

**Дата:** 2026-10-21. **Задача:** определить, какие функции штатного проектора можно перевести на Android/MediaTek, а какие требуют сохранения заводских программных адаптеров. Статический анализ — не runtime-доказательство.

## Сначала определить слои

**Это не две независимые ОС и не две полностью дублирующиеся реализации управления проектором.**

| Слой | Найденные компоненты | Что делает в архитектуре |
|---|---|---|
| Framework Android 13 | TvSettingsPlus, стандартные настройки, Android Audio/Input/Network API | UI, система пользовательских разрешений, Bluetooth-профили, сеть, язык, время |
| MediaTek TV stack | `vendor.mediatek.tv.mtktvfactory@1.0-service`, `vendor.mediatek.tv.mtktvfactory@1.0-imp.so`, `libmediatek_tv_basic.so`, `libcom_mediatek_twoworlds_tv_jni.so` | TV API/HAL, HDMI/CEC/PQ, диагностика и низкоуровневые операции чипсета |
| OEM RUIOS/TRD | `trdservice`, `trdmiddle`, `ITrdSystemService`, `ISystemCtrl`, `IProjectorCtrl`, `ITofCtrl`, `KuSourceRJ`, `RuiAutoFocus` | Связывание HAL и пользовательских действий, параметры конкретной модели, GPIO/I2C/motor/ToF |
| Device-specific драйверы/конфиги | `ruimotor.ko`, `stmvl53l1.ko`, `tvconfig`, `board.ini`, DTBO, PMU/gamma | Различия конкретного железа, сенсоров, оптики, панели |

**Типовые схемы взаимодействия:**
- Android TV Settings `TvSettingsPlus.GeneralFragment` → Intent к `KuSourceRJ` → OEM TRD / `ISystemCtrl` → MediaTek TV HAL/input switching.
- Android TV Settings `ProjectorFragment` / `KeystoneCalibrationActivity` → `RuiAutoFocus` или `IProjectorCtrl` → OEM JNI/драйвер мотора/ToF; **нельзя предполагать**, что MediaTek TV HAL поддерживает готовую автомобильную/проекторную автофокусировку.
- `trdservice.GlobalKeyEventProcess` → OEM или Android TV меню на кнопке пульта. При удалении меню требуется изменить/переадресовать точку входа, иначе аппаратная кнопка может перестать открывать настройки.
- `TvSettingsPlus.partnercustomizer.picture` / MediaTek TV API → PQ/HDR/гамма. В данном случае **действительно возможна прямая API-интеграция**, но необходимо сопоставить все штатные параметры.

## Какие OEM решения заменить разумно

| Функция | Возможная замена | Уверенность | Условие |
|---|---|---|---|
| Wi-Fi/язык/дата/время | штатные Android TV Settings API | высокая | проверить привилегированные права записи и first boot |
| Bluetooth pairing (включая BT-пульт) | Android TV Settings / Bluetooth stack | высокая для UI, неизвестна для OEM автоматического reconnect | сохранять важные startup-процессы до испытаний |
| Показ списка HDMI и переходы в настройки источника | штатные TV Input/MediaTek API + общий экран | средняя | проверить source ID 8052/8054, CEC, HDMI hotplug/standby |
| HDMI boot source | MediaTek `ISystemCtrl.setBootSource` или штатный OEM `KuSourceRJ` | средняя | API может быть доступен только через TRD, проверить разрешения, конкретный profile ID |
| Режим изображения/HDR/PQ | TV HAL + штатные `partnercustomizer.picture` | средняя | сохранить gamma/параметры завода, не переписывать прямой hardware register |
| Яркость | отдельные интерфейсы TV / OEM | пока не определена | различать программную яркость и мощность лампы |
| Ручная трапеция/автотрапеция | `KeystoneCorrection`, OEM TRD и native геометрия | низкая | для прямого HAL нет доказанного полного аналога |
| Автофокус и ручное управление мотором | `RuiAutoFocus`, `RuiCameraApi`, моторный JNI | низкая | HAL MTK не гарантирует поддержки этой оптики; нужны защита от крайних положений и таймаут |
| ToF | OEM `TofCtrlService`, соответствующий драйвер | низкая | присутствует не на всех аппаратных профилях |
| Вентилятор, питание оптики, защита от перегрева | штатный аппаратный слой | низкая | нельзя заменять без конкретной схемы и полного теста |
| Factory/testcast, I2C, GPIO, NVM | заводские служб / диагностические компоненты | очень низкая | возможны уникальные заводские калибровки |

## Почему не удалять весь OEM TRD

1. Средства MediaTek TV могут оперировать HDMI/PQ, но **не обязаны** реализовывать UX-сценарии именно этого проектора.
2. Заводская конфигурация различает `ro.rjpj.machine.id`, порты HDMI, ToF, установочные значения и индивидуальные калибровки. MediaTek TV API может вообще не читать эту конфигурацию.
3. Есть JNI `libsettingsi2c_jni.so`, `libfactoryi2c_jni.so`, `librjpj_private_function.so`; такие компоненты взаимодействуют с устройствами с потенциально опасными настройками.
4. Удаление Binder-сервиса может повлиять на обработку кнопок, OTA, стартовую инициализацию и sleep/wake.
5. В двух последних исследованных прошивках `TvSettingsPlus`, `trdservice`, `trdmiddle` и `KuSourceRJ` **побайтно совпадают**. Это позволяет повторно использовать один и тот же высокоуровневый интерфейс и не требует переписывания драйверов.

## Как измерить, дублируются ли конкретные действия

Для каждого пункта OEM настроек:
- определить Activity/Fragment и слушатель UI;
- получить точный вызываемый метод, входные аргументы, enum и ограничения;
- проследить цепочку `Android UI → OEM Binder/JNI → MediaTek HAL/kernel`;
- найти возможный **стандартный MediaTek API** с тем же результатом и безопасными ограничениями;
- проверить на живых 8052 и 8054 неизменность картинки/звука и состояния после reboot/standby;
- только после этого заменить конкретный вызов, сохранив штатный backend как запасной при несовместимости.

**Список «похожих» методов или наличие класса `MtkTvInputSource` в декомпилированном APK не доказывают одинаковое действие или активный сервис.**

## Практическое решение для первой версии

- `zxlauncher` и `zxstore` — исключить после испытаний нового HOME и жизненного цикла приложения.
- `KuSettings` как отдельный OEM UI — целевой кандидат на исключение, **после** функционального покрытия.
- `TvSettingsPlus` оставить и расширить, включая настройку кнопки пульта.
- MediaTek HAL и OEM TRD/мотор/ToF/PMU оставить без изменений.
- В будущем постепенно исключать лишь те OEM вызовы, для которых доказана эквивалентность штатному Android/MediaTek API.

## Источники внутри проекта

- [OEM Binder / JNI](https://github.com/MAX-TAC/Everycom-Cinelux-Firmware/blob/research-oem-settings-api-20261020/analysis/OEM_API_8052_Latest/IMPLEMENTATION_RU.md)
- [OEM Intent map](../Deep_Stock_Audit_20261021/OEM_INTENT_CALL_CHAINS_RU.md)
- [Код TV factory HAL](../Deep_Stock_Audit_20261021/ELF_CODE_DIFFERENCES_RU.md)
- [Современная 8052 vs 8054](../Deep_Stock_Audit_20261021/MAJOR_FINDINGS_RU.md)
