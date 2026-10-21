# Wi-Fi and Ethernet: RUIOS 8052 factory vs OTA, and factory 8054

Sources are three original SHA256-verified images. No network access on a projector, no configuration changes.
Variants: August 2026 factory 8052, October 2026 OTA 8052.1.0.4, September 2026 factory 8054.1.0.1.

## Is an updated 8052 driver a plausible regression cause?

| Module | Factory 8052 → OTA 8052 .text identical? | OTA 8052 ↔ factory 8054 .text identical? | Versions in .modinfo |
|---|---|---|---|
| mtk_gmac_mt5896.ko | True | True | 8052-factory:=5.15.189-android13-8-gc519afa5fccf-dirty / 8052-ota:=5.15.189-android13-8-g887c38a79694-dirty / 8054-factory:=5.15.189-android13-8-g9d1556453fde-dirty |
| phy-mtk-tphy-tv.ko | True | True | 8052-factory:=5.15.189-android13-8-gc519afa5fccf-dirty / 8052-ota:=5.15.189-android13-8-g887c38a79694-dirty / 8054-factory:=5.15.189-android13-8-g9d1556453fde-dirty |
| wlan_mt7663.ko | False | False | 8052-factory:=5.15.189-android13-8-gc519afa5fccf-dirty / 8052-ota:=5.15.189-android13-8-g887c38a79694-dirty / 8054-factory:=5.15.189-android13-8-g9d1556453fde-dirty |
| wlan_mt7902.ko | True | True | 8052-factory:=5.15.189-android13-8-gc519afa5fccf-dirty / 8052-ota:=5.15.189-android13-8-g887c38a79694-dirty / 8054-factory:=5.15.189-android13-8-g9d1556453fde-dirty |
| wlan_mt7961.ko | True | True | 8052-factory:=5.15.189-android13-8-gc519afa5fccf-dirty / 8052-ota:=5.15.189-android13-8-g887c38a79694-dirty / 8054-factory:=5.15.189-android13-8-g9d1556453fde-dirty |

## Firmware files with Wi-Fi/BT-related filename

| File | Original 8052 | OTA 8052 | Original 8054 |
|---|---|---|---|
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10101.sh | be7b58eee4a4e8 | be7b58eee4a4e8 | be7b58eee4a4e8 |
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10201.sh | c331d3ed7fce98 | c331d3ed7fce98 | c331d3ed7fce98 |
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10301.sh | cc91e74c173047 | cc91e74c173047 | cc91e74c173047 |
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10401.sh | 3b4f2370f0f381 | 3b4f2370f0f381 | 3b4f2370f0f381 |
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10501.sh | 0cbc64cbf5d9db | 0cbc64cbf5d9db | 0cbc64cbf5d9db |
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10601.sh | d51e481499a06b | d51e481499a06b | d51e481499a06b |
| vendor_a/bin/autolog/modules/bsp/wifi/scenario/wifi_10701.sh | 52e189bdb97c85 | 52e189bdb97c85 | 52e189bdb97c85 |
| vendor_a/bin/autolog/modules/bsp/wifi/wifi.sh | 652e787541c0e3 | 652e787541c0e3 | 652e787541c0e3 |
| vendor_a/bin/autolog/modules/platform/bluetooth/bluetooth_android.sh | cab782495d138d | cab782495d138d | cab782495d138d |
| vendor_a/etc/wifi/wifi.cfg | f5c587f26c3779 | f5c587f26c3779 | f5c587f26c3779 |
| vendor_a/firmware/BT_RAM_CODE_MT7902_1_1_hdr.bin | 8d12742e919c21 | 8d12742e919c21 | 8d12742e919c21 |
| vendor_a/firmware/BT_RAM_CODE_MT7961_1_2_hdr.bin | 75afdc2f0b101e | 75afdc2f0b101e | 75afdc2f0b101e |
| vendor_a/firmware/BT_RAM_CODE_MT7961_1a_2_hdr.bin | 5aacb03eace3d2 | 5aacb03eace3d2 | 5aacb03eace3d2 |
| vendor_a/firmware/EEPROM_MT7663.bin | dece9d9570bf0e | dece9d9570bf0e | dece9d9570bf0e |
| vendor_a/firmware/EEPROM_MT7902_1.bin | 3846db74cde187 | 3846db74cde187 | 3846db74cde187 |
| vendor_a/firmware/EEPROM_MT7961_1.bin | 1e076fa1ff0ba1 | 1e076fa1ff0ba1 | 1e076fa1ff0ba1 |
| vendor_a/firmware/EEPROM_MT7961_1a.bin | 024548428ef5a6 | 024548428ef5a6 | 024548428ef5a6 |
| vendor_a/firmware/WIFI_MT7902_patch_mcu_1_1_hdr.bin | 8e6f841af4296d | 8e6f841af4296d | 8e6f841af4296d |
| vendor_a/firmware/WIFI_MT7961_patch_mcu_1_2_hdr.bin | 001c91a9530896 | 001c91a9530896 | 001c91a9530896 |
| vendor_a/firmware/WIFI_MT7961_patch_mcu_1a_2_hdr.bin | dea36196e5ed59 | dea36196e5ed59 | dea36196e5ed59 |
| vendor_a/firmware/WIFI_RAM_CODE_MT7663.bin | 57a8a980a65b1a | 57a8a980a65b1a | 57a8a980a65b1a |
| vendor_a/firmware/WIFI_RAM_CODE_MT7902_1.bin | c0d47fedbf8ce8 | c0d47fedbf8ce8 | c0d47fedbf8ce8 |
| vendor_a/firmware/WIFI_RAM_CODE_MT7961_1.bin | e4012e613366bf | e4012e613366bf | e4012e613366bf |
| vendor_a/firmware/WIFI_RAM_CODE_MT7961_1a.bin | c1333d06c7003d | c1333d06c7003d | c1333d06c7003d |
| vendor_a/firmware/bt_mt7902_1_1.cfg | 5c9468840916e7 | 5c9468840916e7 | 5c9468840916e7 |
| vendor_a/firmware/bt_mt7961_1_1.cfg | d78f3403891686 | d78f3403891686 | d78f3403891686 |
| vendor_a/firmware/bt_mt7961_1_2.cfg | 7f93ec9df528b4 | 7f93ec9df528b4 | 7f93ec9df528b4 |
| vendor_a/firmware/bt_mt7961_1a_1.cfg | d78f3403891686 | d78f3403891686 | d78f3403891686 |
| vendor_a/firmware/bt_mt7961_1a_2.cfg | 0df347949aec32 | 0df347949aec32 | 0df347949aec32 |
| vendor_a/firmware/mt7663_patch_e2_hdr.bin | ad79a3d3acbdf5 | ad79a3d3acbdf5 | ad79a3d3acbdf5 |
| vendor_a/firmware/wifi_mt7663.cfg | 8fe77a833ea2ac | 8fe77a833ea2ac | 8fe77a833ea2ac |
| vendor_a/firmware/wifi_mt7902.cfg | a59ae7bfc97f63 | a59ae7bfc97f63 | a59ae7bfc97f63 |
| vendor_a/firmware/wifi_mt7961.cfg | c19128712708df | c19128712708df | c19128712708df |

## Network init and configuration file references

Only selected network-related lines are retained; sensitive identifiers, NVRAM, per-device calibration and passwords are excluded.

### 8052-factory

**system_a/init.trd.rc**
- 66: setprop wifi.direct.interface p2p0

**system_a/system/build.prop**
- 56: ro.wifi.channels=
- 117: bluetooth.profile.hfp.ag.enabled=true
- 118: bluetooth.profile.hfp.hf.enabled=true
- 119: bluetooth.profile.pan.nap.enabled=false
- 120: bluetooth.profile.pan.panu.enabled=false
- 121: bluetooth.profile.pbap.client.enabled=false
- 122: bluetooth.profile.pbap.server.enabled=false
- 123: bluetooth.profile.map.client.enabled=false
- 124: bluetooth.profile.map.server.enabled=false
- 125: bluetooth.profile.opp.enabled=false
- 126: bluetooth.profile.hid.device.enabled=true
- 127: bluetooth.profile.hid.host.enabled=true
- 128: bluetooth.profile.a2dp.sink.enabled=true
- 129: bluetooth.profile.a2dp.source.enabled=true

**system_a/system/etc/init/wifi.rc**
- 17: # These are needed for migration of data to wifi apex directory.
- 19: restorecon_recursive /data/misc/apexdata/com.android.wifi
- 22: restorecon_recursive /data/misc_ce/0/apexdata/com.android.wifi
- 30: mkdir /sys/kernel/debug/tracing/instances/wifi 711
- 31: restorecon_recursive /sys/kernel/debug/tracing/instances/wifi
- 32: write /sys/kernel/debug/tracing/instances/wifi/tracing_on 0
- 33: write /sys/kernel/debug/tracing/instances/wifi/buffer_size_kb 1
- 34: write /sys/kernel/debug/tracing/instances/wifi/trace_options disable_on_free
- 36: mkdir /sys/kernel/tracing/instances/wifi 711
- 37: restorecon_recursive /sys/kernel/tracing/instances/wifi
- 38: write /sys/kernel/tracing/instances/wifi/tracing_on 0
- 39: write /sys/kernel/tracing/instances/wifi/buffer_size_kb 1
- 40: write /sys/kernel/tracing/instances/wifi/trace_options disable_on_free
- 44: #   /sys/kernel/debug/tracing/instances/wifi/tracing_on.

**system_a/system/etc/init/wificond.rc**
- 3: user wifi
- 4: group wifi net_raw net_admin

**system_a/system/etc/init/hw/init.rc**
- 696: mkdir /data/vendor/tombstones/wifi 0771 wifi wifi
- 764: mkdir /data/misc/bluedroid 02770 bluetooth bluetooth
- 767: chown bluetooth bluetooth /data/misc/bluedroid/bt_config.conf
- 768: mkdir /data/misc/bluetooth 0770 bluetooth bluetooth
- 769: mkdir /data/misc/bluetooth/logs 0770 bluetooth bluetooth
- 787: mkdir /data/misc/wifi 0770 wifi wifi
- 788: mkdir /data/misc/wifi/sockets 0770 wifi wifi
- 789: mkdir /data/misc/wifi/wpa_supplicant 0770 wifi wifi
- 790: mkdir /data/misc/ethernet 0770 system system
- 794: chmod 0660 /data/misc/wifi/wpa_supplicant.conf

**vendor_a/build.prop**
- 147: bluetooth.device.class_of_device=44,4,32
- 181: wifi.interface=wlan0
- 182: ro.vendor.wifi.sap.interface=ap0
- 183: wifi.concurrent.interface=ap0
- 265: persist.vendor.bluetooth.a2dp_src_sink_both_enable=true
- 266: persist.vendor.bluetooth.mtk_bt_consumer_feature=true
- 267: persist.vendor.bluetooth.a2dp_dualaudio_enable=true
- 269: ro.bt.bdaddr_path=/vendor/etc/bluetooth/bt_addr.conf
- 283: persist.bluetooth.btsnoopenable=false
- 284: persist.bluetooth.btsnooppath=/sdcard/btsnoop_hci.cfa
- 285: persist.bluetooth.btsnoopsize=0xffff
- 286: persist.bluetooth.aiccoex=true
- 287: bluetooth.enable_timeout_ms=11000
- 299: service.bluetooth.enablesink=false

**vendor_a/etc/init/init.insmod.rc**
- 78: # for mtk bluetooth
- 212: # for mtk bluetooth
- 269: on property:vendor.mtk.wifi.driver=mt7663
- 270: setprop bluetooth.profile.hfp.ag.enabled false
- 271: setprop bluetooth.profile.hfp.hf.enabled false
- 273: # wlan dongle detect service

**vendor_a/etc/init/bootvideo.rc**
- 5: group media system graphics input bluetooth shell drmrpc mediacodec vendor_dtv_ww_rpc

**vendor_a/etc/init/android.hardware.wifi@1.0-service-lazy.rc**
- 13: user wifi
- 14: group wifi gps

**vendor_a/etc/init/hostapd.android.rc**
- 10: mkdir /data/vendor/wifi 0770 wifi wifi
- 11: mkdir /data/vendor/wifi/hostapd 0770 wifi wifi
- 12: mkdir /data/vendor/wifi/hostapd/sockets 0770 wifi wifi
- 15: interface aidl android.hardware.wifi.hostapd.IHostapd/default
- 18: user wifi
- 19: group wifi net_raw net_admin

**vendor_a/etc/init/android.hardware.bluetooth@1.1-service.rc**
- 6: user bluetooth
- 7: group bluetooth

**vendor_a/etc/init/dtv_svc.rc**
- 6: group media system audio graphics input bluetooth shell drmrpc vendor_mtk_rm

**vendor_a/etc/init/vendor.mediatek.tv.mtktvfactory@1.0-service.rc**
- 5: group system media system graphics input bluetooth shell drmrpc media_rw everybody

**vendor_a/etc/init/init.fusion.rc**
- 209: # wifi tput
- 210: write /sys/class/net/wlan0/queues/rx-0/rps_cpus "e"
- 211: write /sys/class/net/wlan0/queues/rx-1/rps_cpus "e"
- 212: write /sys/class/net/wlan0/queues/rx-2/rps_cpus "e"
- 213: write /sys/class/net/wlan0/queues/rx-3/rps_cpus "e"
- 219: on property:sys.boot_completed=1 && property:vendor.mtk.wifi.driver=mt6639
- 220: # wifi tput - CPU performance mode
- 229: # wifi tput - TCP mem

**vendor_a/etc/init/hw/init.common.rc**
- 52: mkdir /data/system/wpa_supplicant 0770 wifi wifi
- 57: # realtek bluetooth
- 58: mkdir /data/misc/bluedroid 0770 bluetooth bluetooth
- 59: # bluetooth LPM
- 60: chown bluetooth bluetooth /proc/bluetooth/sleep/lpm
- 61: chown bluetooth bluetooth /proc/bluetooth/sleep/btwrite
- 65: chown bluetooth bluetooth /sys/class/rfkill/rfkill0/state
- 66: chown bluetooth bluetooth /sys/class/rfkill/rfkill0/type
- 67: # bluetooth MAC address programming
- 68: chown bluetooth bluetooth "/data/misc/bluetooth/bdaddr"
- 94: mkdir /data/vendor/wifi 0770 wifi wifi
- 95: mkdir /data/vendor/wifi/wpa 0770 wifi wifi
- 96: mkdir /data/vendor/wifi/wpa/sockets 0770 wifi wifi
- 132: user wifi

### 8052-ota

**system_a/init.trd.rc**
- 66: setprop wifi.direct.interface p2p0

**system_a/system/build.prop**
- 56: ro.wifi.channels=
- 117: bluetooth.profile.hfp.ag.enabled=true
- 118: bluetooth.profile.hfp.hf.enabled=true
- 119: bluetooth.profile.pan.nap.enabled=false
- 120: bluetooth.profile.pan.panu.enabled=false
- 121: bluetooth.profile.pbap.client.enabled=false
- 122: bluetooth.profile.pbap.server.enabled=false
- 123: bluetooth.profile.map.client.enabled=false
- 124: bluetooth.profile.map.server.enabled=false
- 125: bluetooth.profile.opp.enabled=false
- 126: bluetooth.profile.hid.device.enabled=true
- 127: bluetooth.profile.hid.host.enabled=true
- 128: bluetooth.profile.a2dp.sink.enabled=true
- 129: bluetooth.profile.a2dp.source.enabled=true

**system_a/system/etc/init/wifi.rc**
- 17: # These are needed for migration of data to wifi apex directory.
- 19: restorecon_recursive /data/misc/apexdata/com.android.wifi
- 22: restorecon_recursive /data/misc_ce/0/apexdata/com.android.wifi
- 30: mkdir /sys/kernel/debug/tracing/instances/wifi 711
- 31: restorecon_recursive /sys/kernel/debug/tracing/instances/wifi
- 32: write /sys/kernel/debug/tracing/instances/wifi/tracing_on 0
- 33: write /sys/kernel/debug/tracing/instances/wifi/buffer_size_kb 1
- 34: write /sys/kernel/debug/tracing/instances/wifi/trace_options disable_on_free
- 36: mkdir /sys/kernel/tracing/instances/wifi 711
- 37: restorecon_recursive /sys/kernel/tracing/instances/wifi
- 38: write /sys/kernel/tracing/instances/wifi/tracing_on 0
- 39: write /sys/kernel/tracing/instances/wifi/buffer_size_kb 1
- 40: write /sys/kernel/tracing/instances/wifi/trace_options disable_on_free
- 44: #   /sys/kernel/debug/tracing/instances/wifi/tracing_on.

**system_a/system/etc/init/wificond.rc**
- 3: user wifi
- 4: group wifi net_raw net_admin

**system_a/system/etc/init/hw/init.rc**
- 696: mkdir /data/vendor/tombstones/wifi 0771 wifi wifi
- 764: mkdir /data/misc/bluedroid 02770 bluetooth bluetooth
- 767: chown bluetooth bluetooth /data/misc/bluedroid/bt_config.conf
- 768: mkdir /data/misc/bluetooth 0770 bluetooth bluetooth
- 769: mkdir /data/misc/bluetooth/logs 0770 bluetooth bluetooth
- 787: mkdir /data/misc/wifi 0770 wifi wifi
- 788: mkdir /data/misc/wifi/sockets 0770 wifi wifi
- 789: mkdir /data/misc/wifi/wpa_supplicant 0770 wifi wifi
- 790: mkdir /data/misc/ethernet 0770 system system
- 794: chmod 0660 /data/misc/wifi/wpa_supplicant.conf

**vendor_a/build.prop**
- 147: bluetooth.device.class_of_device=44,4,32
- 181: wifi.interface=wlan0
- 182: ro.vendor.wifi.sap.interface=ap0
- 183: wifi.concurrent.interface=ap0
- 265: persist.vendor.bluetooth.a2dp_src_sink_both_enable=true
- 266: persist.vendor.bluetooth.mtk_bt_consumer_feature=true
- 267: persist.vendor.bluetooth.a2dp_dualaudio_enable=true
- 269: ro.bt.bdaddr_path=/vendor/etc/bluetooth/bt_addr.conf
- 283: persist.bluetooth.btsnoopenable=false
- 284: persist.bluetooth.btsnooppath=/sdcard/btsnoop_hci.cfa
- 285: persist.bluetooth.btsnoopsize=0xffff
- 286: persist.bluetooth.aiccoex=true
- 287: bluetooth.enable_timeout_ms=11000
- 299: service.bluetooth.enablesink=false

**vendor_a/etc/init/init.insmod.rc**
- 78: # for mtk bluetooth
- 212: # for mtk bluetooth
- 269: on property:vendor.mtk.wifi.driver=mt7663
- 270: setprop bluetooth.profile.hfp.ag.enabled false
- 271: setprop bluetooth.profile.hfp.hf.enabled false
- 273: # wlan dongle detect service

**vendor_a/etc/init/bootvideo.rc**
- 5: group media system graphics input bluetooth shell drmrpc mediacodec vendor_dtv_ww_rpc

**vendor_a/etc/init/android.hardware.wifi@1.0-service-lazy.rc**
- 13: user wifi
- 14: group wifi gps

**vendor_a/etc/init/hostapd.android.rc**
- 10: mkdir /data/vendor/wifi 0770 wifi wifi
- 11: mkdir /data/vendor/wifi/hostapd 0770 wifi wifi
- 12: mkdir /data/vendor/wifi/hostapd/sockets 0770 wifi wifi
- 15: interface aidl android.hardware.wifi.hostapd.IHostapd/default
- 18: user wifi
- 19: group wifi net_raw net_admin

**vendor_a/etc/init/android.hardware.bluetooth@1.1-service.rc**
- 6: user bluetooth
- 7: group bluetooth

**vendor_a/etc/init/dtv_svc.rc**
- 6: group media system audio graphics input bluetooth shell drmrpc vendor_mtk_rm

**vendor_a/etc/init/vendor.mediatek.tv.mtktvfactory@1.0-service.rc**
- 5: group system media system graphics input bluetooth shell drmrpc media_rw everybody

**vendor_a/etc/init/init.fusion.rc**
- 209: # wifi tput
- 210: write /sys/class/net/wlan0/queues/rx-0/rps_cpus "e"
- 211: write /sys/class/net/wlan0/queues/rx-1/rps_cpus "e"
- 212: write /sys/class/net/wlan0/queues/rx-2/rps_cpus "e"
- 213: write /sys/class/net/wlan0/queues/rx-3/rps_cpus "e"
- 219: on property:sys.boot_completed=1 && property:vendor.mtk.wifi.driver=mt6639
- 220: # wifi tput - CPU performance mode
- 229: # wifi tput - TCP mem

**vendor_a/etc/init/hw/init.common.rc**
- 52: mkdir /data/system/wpa_supplicant 0770 wifi wifi
- 57: # realtek bluetooth
- 58: mkdir /data/misc/bluedroid 0770 bluetooth bluetooth
- 59: # bluetooth LPM
- 60: chown bluetooth bluetooth /proc/bluetooth/sleep/lpm
- 61: chown bluetooth bluetooth /proc/bluetooth/sleep/btwrite
- 65: chown bluetooth bluetooth /sys/class/rfkill/rfkill0/state
- 66: chown bluetooth bluetooth /sys/class/rfkill/rfkill0/type
- 67: # bluetooth MAC address programming
- 68: chown bluetooth bluetooth "/data/misc/bluetooth/bdaddr"
- 94: mkdir /data/vendor/wifi 0770 wifi wifi
- 95: mkdir /data/vendor/wifi/wpa 0770 wifi wifi
- 96: mkdir /data/vendor/wifi/wpa/sockets 0770 wifi wifi
- 132: user wifi

### 8054-factory

**system_a/init.trd.rc**
- 66: setprop wifi.direct.interface p2p0

**system_a/system/build.prop**
- 56: ro.wifi.channels=
- 117: bluetooth.profile.hfp.ag.enabled=true
- 118: bluetooth.profile.hfp.hf.enabled=true
- 119: bluetooth.profile.pan.nap.enabled=false
- 120: bluetooth.profile.pan.panu.enabled=false
- 121: bluetooth.profile.pbap.client.enabled=false
- 122: bluetooth.profile.pbap.server.enabled=false
- 123: bluetooth.profile.map.client.enabled=false
- 124: bluetooth.profile.map.server.enabled=false
- 125: bluetooth.profile.opp.enabled=false
- 126: bluetooth.profile.hid.device.enabled=true
- 127: bluetooth.profile.hid.host.enabled=true
- 128: bluetooth.profile.a2dp.sink.enabled=true
- 129: bluetooth.profile.a2dp.source.enabled=true

**system_a/system/etc/init/wifi.rc**
- 17: # These are needed for migration of data to wifi apex directory.
- 19: restorecon_recursive /data/misc/apexdata/com.android.wifi
- 22: restorecon_recursive /data/misc_ce/0/apexdata/com.android.wifi
- 30: mkdir /sys/kernel/debug/tracing/instances/wifi 711
- 31: restorecon_recursive /sys/kernel/debug/tracing/instances/wifi
- 32: write /sys/kernel/debug/tracing/instances/wifi/tracing_on 0
- 33: write /sys/kernel/debug/tracing/instances/wifi/buffer_size_kb 1
- 34: write /sys/kernel/debug/tracing/instances/wifi/trace_options disable_on_free
- 36: mkdir /sys/kernel/tracing/instances/wifi 711
- 37: restorecon_recursive /sys/kernel/tracing/instances/wifi
- 38: write /sys/kernel/tracing/instances/wifi/tracing_on 0
- 39: write /sys/kernel/tracing/instances/wifi/buffer_size_kb 1
- 40: write /sys/kernel/tracing/instances/wifi/trace_options disable_on_free
- 44: #   /sys/kernel/debug/tracing/instances/wifi/tracing_on.

**system_a/system/etc/init/wificond.rc**
- 3: user wifi
- 4: group wifi net_raw net_admin

**system_a/system/etc/init/hw/init.rc**
- 696: mkdir /data/vendor/tombstones/wifi 0771 wifi wifi
- 764: mkdir /data/misc/bluedroid 02770 bluetooth bluetooth
- 767: chown bluetooth bluetooth /data/misc/bluedroid/bt_config.conf
- 768: mkdir /data/misc/bluetooth 0770 bluetooth bluetooth
- 769: mkdir /data/misc/bluetooth/logs 0770 bluetooth bluetooth
- 787: mkdir /data/misc/wifi 0770 wifi wifi
- 788: mkdir /data/misc/wifi/sockets 0770 wifi wifi
- 789: mkdir /data/misc/wifi/wpa_supplicant 0770 wifi wifi
- 790: mkdir /data/misc/ethernet 0770 system system
- 794: chmod 0660 /data/misc/wifi/wpa_supplicant.conf

**vendor_a/build.prop**
- 147: bluetooth.device.class_of_device=44,4,32
- 181: wifi.interface=wlan0
- 182: ro.vendor.wifi.sap.interface=ap0
- 183: wifi.concurrent.interface=ap0
- 265: persist.vendor.bluetooth.a2dp_src_sink_both_enable=true
- 266: persist.vendor.bluetooth.mtk_bt_consumer_feature=true
- 267: persist.vendor.bluetooth.a2dp_dualaudio_enable=true
- 269: ro.bt.bdaddr_path=/vendor/etc/bluetooth/bt_addr.conf
- 283: persist.bluetooth.btsnoopenable=false
- 284: persist.bluetooth.btsnooppath=/sdcard/btsnoop_hci.cfa
- 285: persist.bluetooth.btsnoopsize=0xffff
- 286: persist.bluetooth.aiccoex=true
- 287: bluetooth.enable_timeout_ms=11000
- 299: service.bluetooth.enablesink=false

**vendor_a/etc/init/init.insmod.rc**
- 78: # for mtk bluetooth
- 212: # for mtk bluetooth
- 269: on property:vendor.mtk.wifi.driver=mt7663
- 270: setprop bluetooth.profile.hfp.ag.enabled false
- 271: setprop bluetooth.profile.hfp.hf.enabled false
- 273: # wlan dongle detect service

**vendor_a/etc/init/bootvideo.rc**
- 5: group media system graphics input bluetooth shell drmrpc mediacodec vendor_dtv_ww_rpc

**vendor_a/etc/init/android.hardware.wifi@1.0-service-lazy.rc**
- 13: user wifi
- 14: group wifi gps

**vendor_a/etc/init/hostapd.android.rc**
- 10: mkdir /data/vendor/wifi 0770 wifi wifi
- 11: mkdir /data/vendor/wifi/hostapd 0770 wifi wifi
- 12: mkdir /data/vendor/wifi/hostapd/sockets 0770 wifi wifi
- 15: interface aidl android.hardware.wifi.hostapd.IHostapd/default
- 18: user wifi
- 19: group wifi net_raw net_admin

**vendor_a/etc/init/android.hardware.bluetooth@1.1-service.rc**
- 6: user bluetooth
- 7: group bluetooth

**vendor_a/etc/init/dtv_svc.rc**
- 6: group media system audio graphics input bluetooth shell drmrpc vendor_mtk_rm

**vendor_a/etc/init/vendor.mediatek.tv.mtktvfactory@1.0-service.rc**
- 5: group system media system graphics input bluetooth shell drmrpc media_rw everybody

**vendor_a/etc/init/init.fusion.rc**
- 209: # wifi tput
- 210: write /sys/class/net/wlan0/queues/rx-0/rps_cpus "e"
- 211: write /sys/class/net/wlan0/queues/rx-1/rps_cpus "e"
- 212: write /sys/class/net/wlan0/queues/rx-2/rps_cpus "e"
- 213: write /sys/class/net/wlan0/queues/rx-3/rps_cpus "e"
- 219: on property:sys.boot_completed=1 && property:vendor.mtk.wifi.driver=mt6639
- 220: # wifi tput - CPU performance mode
- 229: # wifi tput - TCP mem

**vendor_a/etc/init/hw/init.common.rc**
- 52: mkdir /data/system/wpa_supplicant 0770 wifi wifi
- 57: # realtek bluetooth
- 58: mkdir /data/misc/bluedroid 0770 bluetooth bluetooth
- 59: # bluetooth LPM
- 60: chown bluetooth bluetooth /proc/bluetooth/sleep/lpm
- 61: chown bluetooth bluetooth /proc/bluetooth/sleep/btwrite
- 65: chown bluetooth bluetooth /sys/class/rfkill/rfkill0/state
- 66: chown bluetooth bluetooth /sys/class/rfkill/rfkill0/type
- 67: # bluetooth MAC address programming
- 68: chown bluetooth bluetooth "/data/misc/bluetooth/bdaddr"
- 94: mkdir /data/vendor/wifi 0770 wifi wifi
- 95: mkdir /data/vendor/wifi/wpa 0770 wifi wifi
- 96: mkdir /data/vendor/wifi/wpa/sockets 0770 wifi wifi
- 132: user wifi

## Distinguishing LAN problems

- **No link**: router port LED off, kernel sysfs carrier 0/operstate down even when eth0 UP; investigate PHY power, device-tree enablement, board wiring, speed negotiation, cable, vendor Ethernet driver.
- **Link but no IP**: carrier 1, speed negotiated, no IPv4; investigate Android EthernetManager/netd, DHCP, static IP and network priority.
- **No eth0 interface**: verify /sys/class/net and loaded/built-in driver, DT/PHY and init services. A physical RJ45 port does not ensure enabled Ethernet in the current SKU.
- **Wi-Fi slow but linked**: distinguish RSSI, link PHY rate, channel/band, iperf3 LAN test vs public speedtest, Bluetooth coexistence and kernel/firmware driver logs.
- **Regression after OTA**: determine if link/speed changed after upgrade; static hashes alone cannot prove actual cause.

## What this offline scan cannot establish

- Ethernet MAC might be built directly into the kernel; no external .ko does not prove missing Ethernet support.
- DTBO blobs and factory TV service may configure PHY/MAC independently of Android vendor init files.
- Kernel module with any name may remain unused; report cannot identify physical Wi-Fi chip without live interface/driver details.
- Do not mix kernel modules across versions while vermagic / CONFIG_MODVERSIONS differs.
- No firmware replacement proposed until actual chipset, chip bus and reference performance are verified.

