# CineLux embedded Linux environments (not Android)

Both firmware packages contain separate compressed Linux rootfs images. This scan compares file hashes and service configurations without running any firmware binaries.

## linux_rootfs_a_a

1 HDMI files: 878
2 HDMI files: 878
Unchanged: 848
Different same paths: 30
Unique one: 0
Unique two: 0

### Changed binaries and configuration files

- basic/app_man
- basic/dtv_svc
- basic/lib/libcmd_convert.so
- basic/lib/libnetwork_detect.so
- basic/lib/libsmartfs.so
- basic/libMtkRmClient.so
- basic/libgam_client.so
- basic/libmtal.so
- basic/libmtal_custom.so
- basic/libmtkdrm.so
- lib/libmediatek_tv_basic.so
- lib/libmediatek_tv_cas.so
- lib/libmediatek_tv_cmpb.so
- lib/libmediatek_tv_mwif.so
- lib/libmediatek_tv_rpccore.so
- lib/libmediatek_tv_rpchandler.so
- lib/libmediatek_tv_rpcwrapper.so
- lib/libmediatek_tv_services.so
- lib/libmediatek_tv_util.so
- lib/libmediatek_tv_weak.so
- lib/libmtkapp.so
- lib/libplayback_inet.so
- lib/libstdc++.so.6.0.21
- lib/libtvcli.so
- lib/libvendor_agent.so
- tinycap-master
- tinymix-master
- tinypcminfo-master
- tinyplay-master
- usr/bin/cli

### One-HDMI-only files


### Two-HDMI-only files


### Service and startup scripts in Linux rootfs

- basic/autorun.sh
- etc/init.d/checkroot.sh
- etc/init.d/halt
- etc/init.d/ifupdown
- etc/init.d/inetd
- etc/init.d/init-functions
- etc/init.d/mountall.sh
- etc/init.d/mountvirtfs
- etc/init.d/networking
- etc/init.d/portmap
- etc/init.d/rc
- etc/init.d/rcS
- etc/init.d/rcS.ko.linux
- etc/init.d/rcS.utopia.linux
- etc/init.d/reboot
- etc/init.d/sendsigs
- etc/init.d/single
- etc/init.d/udev
- etc/init.d/umountfs
- etc/scripts/auto_launch.sh
- etc/scripts/basic_mount_ro.sh
- etc/scripts/basic_mount_rw.sh
- etc/scripts/dhcpv6.sh
- etc/scripts/ext4_mount_3rd.sh
- etc/scripts/ext4_mount_perm.sh
- etc/scripts/ext4_unmount_3rd.sh
- etc/scripts/ext4_unmount_perm.sh
- etc/scripts/gen_env.sh
- etc/scripts/init_all.sh
- etc/scripts/init_daemon.sh
- etc/scripts/ins_all_mod.sh
- etc/scripts/ins_basic_mod.sh
- etc/scripts/ins_blk_mod.sh
- etc/scripts/ins_drv.sh
- etc/scripts/ins_dtv.sh
- etc/scripts/ins_eth_mod.sh
- etc/scripts/ins_fs_mod.sh
- etc/scripts/ins_usb_core_mod.sh
- etc/scripts/ins_usb_sub_mod.sh
- etc/scripts/ins_wifi_mod.sh
- etc/scripts/kill_3rd_app.sh
- etc/scripts/manual_launch.sh
- etc/scripts/mkpts.sh
- etc/scripts/rm_usb_mod.sh
- etc/scripts/squash_mount_emmc_3rd_ro.sh
- etc/scripts/squash_unmount_3rd_ro.sh
- etc/scripts/usb_console.sh
- etc/udev/scripts/cdsymlinks.sh
- etc/udev/scripts/dvb.sh
- etc/udev/scripts/ide-devfs.sh
- etc/udev/scripts/ide-model.sh
- etc/udev/scripts/inputdev.sh
- etc/udev/scripts/raid-devfs.sh
- etc/udev/scripts/scsi-devfs.sh
- sbin/coredump.sh
- usr/bin/suspend.sh


## 3rd_a_a

1 HDMI files: 6
2 HDMI files: 6
Unchanged: 6
Different same paths: 0
Unique one: 0
Unique two: 0

### Changed binaries and configuration files


### One-HDMI-only files


### Two-HDMI-only files


### Service and startup scripts in Linux rootfs



