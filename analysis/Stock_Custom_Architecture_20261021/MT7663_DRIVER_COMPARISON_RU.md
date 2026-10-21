# Исходный драйвер MT7663 и альтернативные Wi-Fi модули: сравнительная метаинформация

Сравнение SHA-верифицированной октябрьской OTA 8052.1.0.4 и сентябрьской заводской 8054.1.0.1.
Источник: два успешных job инвентаризации ELF (run 39574844708), без запуска модулей.
**Наличие модуля в образе не означает его загрузку на конкретном устройстве.** По vermagic все исследованные модули собраны для 5.15.189-android13-8, но разными коммитами ядра: 8052 g887c38a79694, 8054 g9d1556453fde. Уточнить фактически запущенное ядро на устройстве.

| Модуль | Полный файл совпадает? | Машинный код (.text) совпадает? | Константы (.rodata) совпадают? | .modinfo совпадает? | Общих функций / разный код |
|---|---|---|---|---|---|
| vendor_a/lib/modules/wlan_mt7663.ko | False | False | False | False | 0/0 |
| vendor_a/lib/modules/wlan_mt7902.ko | False | True | False | False | 0/0 |
| vendor_a/lib/modules/wlan_mt7961.ko | False | True | False | False | 0/0 |
| vendor_a/lib/modules/dtv_driver.ko | False | True | False | False | 5524/0 |

## vendor_a/lib/modules/wlan_mt7663.ko

- Изменена .text: True. Это не доказывает исправление драйвера.
- Текст version/vermagic/depends/srcversion из .modinfo 8052: ['depends=cfg80211,mtreset_,wlan_mt7663_prealloc', 'vermagic=5.15.189-android13-8-g887c38a79694-dirty SMP preempt mod_unload modversions aarch64']
- Те же поля для 8054: ['depends=cfg80211,mtreset_,wlan_mt7663_prealloc', 'vermagic=5.15.189-android13-8-g9d1556453fde-dirty SMP preempt mod_unload modversions aarch64']

## vendor_a/lib/modules/wlan_mt7902.ko

- Изменена .text: False. Это не доказывает исправление драйвера.
- Текст version/vermagic/depends/srcversion из .modinfo 8052: ['depends=cfg80211,mtreset,mtprealloc', 'vermagic=5.15.189-android13-8-g887c38a79694-dirty SMP preempt mod_unload modversions aarch64']
- Те же поля для 8054: ['depends=cfg80211,mtreset,mtprealloc', 'vermagic=5.15.189-android13-8-g9d1556453fde-dirty SMP preempt mod_unload modversions aarch64']

## vendor_a/lib/modules/wlan_mt7961.ko

- Изменена .text: False. Это не доказывает исправление драйвера.
- Текст version/vermagic/depends/srcversion из .modinfo 8052: ['depends=cfg80211,mtreset,mtprealloc', 'vermagic=5.15.189-android13-8-g887c38a79694-dirty SMP preempt mod_unload modversions aarch64']
- Те же поля для 8054: ['depends=cfg80211,mtreset,mtprealloc', 'vermagic=5.15.189-android13-8-g9d1556453fde-dirty SMP preempt mod_unload modversions aarch64']

## vendor_a/lib/modules/dtv_driver.ko

- Изменена .text: False. Это не доказывает исправление драйвера.
- Текст version/vermagic/depends/srcversion из .modinfo 8052: ['depends=mik,time_stamp,mtk-sti_wrapper,iniparser,leds-breath,mtk-efuse,cb2', 'vermagic=5.15.189-android13-8-g887c38a79694-dirty SMP preempt mod_unload modversions aarch64']
- Те же поля для 8054: ['depends=mik,time_stamp,mtk-sti_wrapper,iniparser,leds-breath,mtk-efuse,cb2', 'vermagic=5.15.189-android13-8-g9d1556453fde-dirty SMP preempt mod_unload modversions aarch64']

## Источники возможного обновления

- Mainline Linux mt76/mt7615 supports MT7663 over PCIe/USB/SDIO, but a generic kernel 6.x module is not an interchangeable replacement for this OEM Android 13 / Linux 5.15.189 BSP driver.
- linux-firmware provides device microcode/firmware; firmware files, kernel Wi-Fi module and Bluetooth driver must be checked separately.
- MediaTek Genio/Yocto announcement in Aug 2026 is *not* proof of Bluetooth restrictions in OEM RUIOS Android 13.
- To choose a newer module: detect real Wi-Fi chip and bus, identify 8052/8054 OEM kernel vermagic/modversions, get compatible source + firmware, confirm WLAN/BT HAL/SELinux/power-management compatibility, then test rollback.
- If the chip is not MT7663, defer the detailed 7663 driver port entirely.

## Источники

- https://wireless.docs.kernel.org/en/latest/en/users/drivers/mediatek.html
- https://github.com/torvalds/linux/blob/master/drivers/net/wireless/mediatek/mt76/mt7615/Kconfig
- https://github.com/morrownr/mt76
- https://genio-community.mediatek.com/t/bluetooth-support-for-mt7663-in-yocto/2775

