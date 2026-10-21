# ELF-код: первичный аудит отличий двух заводских ревизий

Исходные данные: SHA256-проверенные заводские 8052 августа и 8054 сентября; для октябрьской 8052 бинарное сопоставление HAL **ещё требуется**.

## Результаты раздельного сравнения секций

- Сканировалось ELF 8052: 1333, 8054: 1335.
- Полностью совпадающих ELF: 88.
- ELF с отличающимся общим SHA: 1245.
- ELF с одинаковой секцией .text, но разным общим SHA: 1241.
- ELF с отличающейся секцией .text: **4**.

**Важно:** идентичная .text не доказывает одинаковость поведения: отличаться могут .rodata, .data, динамические конфигурации, DTBO, окружение и драйверы.

## Четыре ELF с отличающейся исполняемой секцией .text

### `vendor_a/bin/hw/vendor.mediatek.tv.mtktvfactory@1.0-service`

- .text размеры: 45324 / 45324; в обоих ELF класс 32-бит.
- Зависимости DT_NEEDED изменились? false.
- Экспортируемых имён только в старом/новом: 48/48.

**Выборка отличающихся символов 8052:**
- `_Z33a_mtktvfapi_disptst_set_pq_on_offh`
- `_Z35a_mtktvfapi_inpsrc_get_input_timingRN9fapi_core20MtkTvFApiVideoTimingE`
- `_Z43a_mtktvfapi_inpsrc_get_current_input_sourcePh`
- `_Z48a_mtktvfapi_inpsrc_get_current_input_source_typePh`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest11linkToDeathERKN7android2spINS5_8hardware20hidl_death_recipientEEEy`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest12getDebugInfoENSt3__18functionIFvRKN7android4hidl4base4V1_09DebugInfoEEEE`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest12getHashChainENSt3__18functionIFvRKN7android8hardware8hidl_vecINS8_10hidl_arrayIhLj32`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest13unlinkToDeathERKN7android2spINS5_8hardware20hidl_death_recipientEEE`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest14interfaceChainENSt3__18functionIFvRKN7android8hardware8hidl_vecINS8_11hidl_stringEEE`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest19interfaceDescriptorENSt3__18functionIFvRKN7android8hardware11hidl_stringEEEE`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest21notifySyspropsChangedEv`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest21setHALInstrumentationEv`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest4pingEv`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiDisplayTest5debugERKN7android8hardware11hidl_handleERKNS6_8hidl_vecINS6_11hidl_stringEEE`
- `_ZN6vendor8mediatek2tv12mtktvfactory4V1_021IMtkTvFApiInputSource14interfaceChainENSt3__18functionIFvRKN7android8hardware8hidl_vecINS8_11hidl_stringEEE`

**Выборка отличающихся символов 8054:**
- `_Z29a_mtktvfapi_prphrl_enable_cech`
- `_Z29a_mtktvfapi_prphrl_enable_iici`
- `_Z30a_mtktvfapi_prphrl_disable_iici`
- `_Z31a_mtktvfapi_prphrl_control_gpiojj`
- `_Z31a_mtktvfapi_prphrl_set_hdmi_hpdhh`
- `_Z31a_mtktvfapi_prphrl_write_to_iicittPKhtS0_`
- `_Z32a_mtktvfapi_prphrl_read_from_iicitttPKhtPh`
- `_Z33a_mtktvfapi_prphrl_get_cec_statusPa`
- `_Z34a_mtktvfapi_prphrl_get_earc_statusPi`
- `_Z34a_mtktvfapi_prphrl_get_gpio_statusjPh`
- `_Z36a_mtktvfapi_prphrl_gpio_monitor_stopv`
- `_Z37a_mtktvfapi_prphrl_get_hdmi_edid_datajPN9fapi_core25MtkTvFApiHDMI_EDID_Data_tE`
- `_Z37a_mtktvfapi_prphrl_gpio_monitor_startjjj`
- `_Z37a_mtktvfapi_prphrl_set_hdmi_edid_datajajPKh`
- `_Z40a_mtktvfapi_prphrl_get_iic_slave_addressttPt`

**Интерпретация:** подтверждённо изменён машинный код, но источник различия (рефакторинг, оптимизация, багфикс, аппаратная специфика) по контрольным суммам и списку экспортов доказать нельзя. Следующий шаг — выровнять функции по адресам, дизассемблировать и классифицировать семантические изменения.

### `vendor_a/lib/libcom_mediatek_twoworlds_tv_jni.so`

- .text размеры: 242232 / 242232; в обоих ELF класс 32-бит.
- Зависимости DT_NEEDED изменились? false.
- Экспортируемых имён только в старом/новом: 80/80.

**Выборка отличающихся символов 8052:**

**Выборка отличающихся символов 8054:**
- `a_mtktvapi_get_earc_caps`

**Интерпретация:** подтверждённо изменён машинный код, но источник различия (рефакторинг, оптимизация, багфикс, аппаратная специфика) по контрольным суммам и списку экспортов доказать нельзя. Следующий шаг — выровнять функции по адресам, дизассемблировать и классифицировать семантические изменения.

### `vendor_a/lib/libmediatek_tv_basic.so`

- .text размеры: 166304 / 166304; в обоих ELF класс 32-бит.
- Зависимости DT_NEEDED изменились? false.
- Экспортируемых имён только в старом/новом: 0/0.

**Выборка отличающихся символов 8052:**

**Выборка отличающихся символов 8054:**

**Интерпретация:** подтверждённо изменён машинный код, но источник различия (рефакторинг, оптимизация, багфикс, аппаратная специфика) по контрольным суммам и списку экспортов доказать нельзя. Следующий шаг — выровнять функции по адресам, дизассемблировать и классифицировать семантические изменения.

### `vendor_a/lib/vendor.mediatek.tv.mtktvfactory@1.0-imp.so`

- .text размеры: 90156 / 90156; в обоих ELF класс 32-бит.
- Зависимости DT_NEEDED изменились? false.
- Экспортируемых имён только в старом/новом: 0/0.

**Выборка отличающихся символов 8052:**

**Выборка отличающихся символов 8054:**

**Интерпретация:** подтверждённо изменён машинный код, но источник различия (рефакторинг, оптимизация, багфикс, аппаратная специфика) по контрольным суммам и списку экспортов доказать нельзя. Следующий шаг — выровнять функции по адресам, дизассемблировать и классифицировать семантические изменения.

## Проверки для классификации изменений

1. Сопоставить актуальную OTA 8052 с 8054, чтобы отделить возраст сборки от аппаратного профиля.
2. Проверить Build-ID, ABI, экспортируемые символы, DT_NEEDED, .text/.rodata/.data и relocations.
3. Для каждого различающегося исполнения построить function-level diff (Ghidra/BinDiff/radiff2), не публикуя OEM код.
4. Классифицировать: только метаданные; кодовая оптимизация; исправление дефекта; изменение интерфейса ABI; ветка по HDMI/ToF; неустановлено.
5. Не подменять эти HAL в кастомной сборке, пока не подтверждена совместимость.

## Внимание к прежнему анализу

Утверждение «1241 ELF различаются только метаданными» **неверно**. Проверялась только секция .text; все остальные области могли измениться. Сначала повторить сравнение с актуальной 8052.
