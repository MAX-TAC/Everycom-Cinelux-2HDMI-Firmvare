# Native machine-code comparison: latest 8052 OTA vs stock 8054

Original SHA256-verified 8052.1.0.4 OTA vs 8054.1.0.1 factory PKG. ELF sections and named function bytes compared by SHA.
Different .text SHA means different machine-code bytes, not necessarily a bug fix or board-specific functionality.

## ELF totals

- ota_all: 1527
- stock_all: 1527
- shared: 1527
- only_in_ota: 0
- only_in_stock: 0
- code_changed: 2
- identical_file: 1383
- text_same_other_changed: 133
- text_same_rodata_changed: 9

## Projector hardware-relevant native ELF changes

| File | Category | Same .text? | Same .rodata? | Changed named functions |
|---|---|---|---|---:|
| vendor_a/lib/libmediatek_tv_basic.so | code_changed | False | False | 55 |
| vendor_a/lib/libmediatek_tv_rpcwrapper.so | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/btmtk_usb.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/btmtk_usb_unify.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/dtv_driver.ko | text_same_rodata_changed | True | False | 0 |
| vendor_a/lib/modules/emi-cen-tv.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/extcon-mtk-headset.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/fusion_mtk.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/i2c-dev.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/i2c-gpio.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/i2c-mt5896.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/leds-mtk-irtx.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-ab-boot.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-aloop.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-audio-mcu-communication.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-audio-mcu.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-bdma.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-boottime.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-bw.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-db-tool.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-dramc-ca.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-dramc.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-es-buf-mgr.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-ir-tx.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-ir.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-kmiup.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-memory.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-mic-capture.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-mic-communication.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-miup.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-miup_debug.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-module_thermal.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-pm.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-pmu-cec.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-pmu-ir.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-pmu-keypad.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-smi-tv.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-stctrl.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-tv-atrace.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-v4l2-jpd.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-vcodec-common.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-vcodec-dec.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-vcodec-enc.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk-vcu.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_als.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_dmx.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_gmac_mt5896.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_iommu.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_irs.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_light.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_mic_mute_drv.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_pmu_rproc.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_realtime_example.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_realtime_producer.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_tee.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_test_cdev.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_v4l2loopback.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_zdec_drv.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_zram.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_zram_genpool.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtk_zsmalloc.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-cpufreq-ca.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-cpufreq-dbg.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-cpufreq.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-regulator-mt5876-core-power.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-regulator-mt5876.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-regulator-mt5896.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mtktv-thermal.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/mzc-mtk.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/phy-mtk-tphy-tv.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/pwmseg-mtktv.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/spi-mtkdtv-ci.ko | text_same_other_changed | True | True | 0 |
| vendor_a/lib/modules/xhci-mtk-hcd-tv.ko | text_same_other_changed | True | True | 0 |

## Changes in executable machine code


### vendor_a/lib/libmediatek_tv_basic.so

- .text sizes OTA / stock: 166304/166304
- Named functions common / changed: 800/55
- Dynamic dependency set changed: False
- Changed exported function examples:
- Different disassembled mnemonic sequences: 5
- Identical mnemonic sequence despite code byte changes: 50
- `cfg_parser_list_all_configs_info`
- `cfg_parser_set_config_value`
- `cli_alias`
- `cli_feature_dump`
- `cli_parse_cmd_from_root`
- `dbg_init_count_data`
- `dbg_set_enable_log2file`
- `get_alita_version`
- `handle_alloc`
- `handle_free_all`
- `kbir_main`
- `multi_byte_to_unicode`
- `multi_byte_to_unicode_ex`
- `os_linux_ion_mmap_with_fd`
- `os_linux_ion_register_mmap_fd_callback`
- `os_linux_ion_send_mmap_fd_async`
- `test_msgq_health_check_operations`
- `test_msgq_operations`
- `test_timer_operations`
- `thread_init`
- `timer_init`
- `x_cli_feature_init_cmd`
- `x_cli_show_log_level`
- `x_dbg_abort`
- `x_dbg_dump_trace_buff`
- `x_do_dbg_abort`
- `x_feature_is_ci_plus_record_suppport`
- `x_feature_is_ci_plus_tz_support`
- `x_feature_is_cli_support`
- `x_feature_is_debug_support`

## Confidence and next steps

Confirmed: differences in .text, read-only constant data, function SHA and dynamic symbol names.
Unconfirmed: why code changed, intended hardware, fault fixes, runtime ABI behavior and safe backports.
Prioritize ARM disassembly and control-flow diff for affected functions, then check real 8052 and 8054.
Analysis excludes most non-ELF boot firmware, OP-TEE/PMU, DTBO and embedded TV Linux userspace.
The actual 8054.1.0.4 firmware is not available for the binary comparison yet.

