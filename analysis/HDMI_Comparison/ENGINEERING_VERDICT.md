# CineLux 1-HDMI vs 2-HDMI: engineering verdict and reflashing plan

Verified on 20 October 2026 using the original releases in this repo. Reproducible workflow: https://github.com/MAX-TAC/Everycom-Cinelux-2HDMI-Firmvare/actions/runs/39400245357

## Comparison summary

- Both are `upgrade_image.pkg` MStar Secure New, encrypted by same public MSTAR_SECURE AES-256-CBC key. Both decrypt, LZ4-decompress, and reconstruct as standard Android 13 EROFS dynamic-partition images.
- Both use identical GPT partition layout and boot environment fields: `android_product griggs`, `dtbo_cfg_sel config/dtb/mt5873_h1v1_cd.ini`, `androidboot.selinux permissive`, `setenv devicestate lock`, `setenv verify n`. These boot script strings **do not prove** live secure-boot enforcement or ability to unlock.
- One-HDMI has 31 `filepartload` commands and 10 `super` sparse pieces, two-HDMI has 33 commands and 12 `super` pieces. The latter has 183,169,024 additional raw `system_a` EROFS bytes (not directly equal to added app footprint).
- The Android logical filesystems all differ in SHA-256: `system_a`, `vendor_a`, `product_a`, `system_ext_a`. One-HDMI `system_a` 683,675,648 bytes and two-HDMI 866,844,672 bytes.
- Overall the extracted EROFS trees contain 3,944 shared file paths; 2,267 (57.48%) are byte-identical; 1,677 differ; 4 paths are unique to 1-HDMI and 12 paths are unique to 2-HDMI.
- Stock builds are from 13 Aug 2026 (user/build author `luzhih`) and 30 Sep 2026 (`suhaix`), both Android 13 SDK 33, build type `userdebug`, `test-keys`, reported security patch 2026-04-05. A changed binary hash does not necessarily imply a functional change due to recompilation.

### Components

- Exact identical OEM APK: `RuiYunOta`, `trdmiddle`. Multiple core Android/system APK also identical.
- Changed OEM APK: `KuSettings`, `KuSourceRJ`, `RuiAutoFocus`, `KeystoneCorrection`, `TvSettingsPlus`, `zxlauncher`, `zxstore`, `trdservice`, `LiveTV`, `TvServices`, `Factory`.
- Two HDMI only: `KuSetupWizard`, preinstall_del Netflix/YouTube/PrimeVideo APKs; `libfactoryi2c_jni.so`, `libsettingsi2c_jni.so`; four additional keylayouts, including two `Everycom_remote_*` files.
- One HDMI only: system_ext `Provision` app and permission xml.
- Both vendor HAL manifests declare the same services, including MediaTek TV Input, CEC, display, audio and proprietary TRD/ToF APIs. However, audio HAL binaries, HDMI-CEC service and `vendor.trd.hardware.tof@1.0.so` differ in hash.
- Physical flashed image hashes differ for `boot_a`, `dtbo_a`, `mboot_a`, `optee_a`, `linux_rootfs_a_a`, `tvconfig_a`, `tvservice_a`, `factory_a_a`, `project_id`, `persist`, `vbmeta_a`. Hence a cross-flash is not safe without identifying exact board.

## AVB digital signatures: direct inspection of both original packages

Stock `vbmeta_a` and `vbmeta_system_a` in **both** versions have header magic `AVB0`, algorithm ID **2** (`SHA256_RSA4096`), an authentication block of 576 bytes (hash + RSA-4096 signature, padded), and a non-zero auxiliary block. Report: [AVB.md](AVB.md).

Therefore an offline-built custom image can't simply be swapped into signed stock `super` or `boot` while maintaining the existing signature. New AVB data may be generated using avbtool with an owned key, but the bootloader must trust it (unlocked state or supported user-installed root of trust). Public-key extraction doesn't provide the original private RSA signing key.

## Distinct signature and encryption checkpoints

1. **PKG container:** AES-256-CBC encryption of REE payload uses the publicly recovered key, so plaintext image may be recovered and ciphertext can in principle be generated. The secure container also has signing-like regions at 0x000 and 0x580. The verification rules and OEM signing key have NOT been confirmed.
2. **U-Boot / ROM chain:** may verify integrity/signature of U-Boot, OP-TEE and kernel; exact enforcement depends on chip fuses, SoC configuration and manufacturer bootloader code.
3. **Android AVB:** definitely contains SHA256_RSA4096 signed vbmeta headers. Live enforcement, unlock/verity flags and rollback policy remain unknown until device-level checks.
4. **Partition compatibility:** DTBO, PMU, ToF, HDMI and factory calibrations differ, so a correctly signed yet mismatched image can still fail boot or hardware initialization.

## Possible development and installation paths (decision tree)

| Approach | When practical | Relative risk |
|---|---|---|
| Install Projectivy / a custom settings companion as user app via ADB; keep stock HAL | Almost any Android with ADB/app install available | Low |
| Root shell + reversible changes to settings/services and system overlays; safely recover before modifying | Device has root and known working rescue method | Medium |
| Rebuild signed Android partitions and flash via `fastbootd` / bootloader `fastboot` | Bootloader permits unlocking, fastbootd available, AVB handled with own key or appropriate state | High; verify commands non-destructively first |
| Build OEM-compatible encrypted PKG/USB recovery update | Valid signature or verified acceptance of custom package and correct MStar secure container packer | Unproven and very high risk for whole-device update |
| Rename custom PKG to BIN and USB-install | Renaming changes no format or signing, so does not bypass protections | Not a viable signing workaround |
| Hardware recovery (UART, eMMC ISP, JTAG, board-specific USB BootROM) | Exact board service mode/pinout and recovery tools documented and tested | Very high / last-resort |

**Do not infer presence of SP Flash Tool/phone-style MTK USB flashing from MT5873/MT9660.** TV SoCs have different recovery environments.

## Destructive commands in BOTH vendor PKG scripts

- `gpt clean mmc 0`: delete/re-create entire partition table.
- `wipeuserdata`: destroy user apps/settings.
- `partition erase mmc 0 persist` and `mmc erase.p eeprom_a`: erase persistent/calibration-related spaces.
- Writes to both boot slots, DTBO, OP-TEE and vendor config; an unexpected board revision can cause boot failure or loss of HDMI/focus/camera functionality.

## Non-destructive device checklist when D11 arrives

- Record board name/revision, HDMI count, PCB identifiers and supported RAM/storage. Compare to vendor DTBO before attempting flashes.
- `adb shell getprop ro.boot.verifiedbootstate`, `ro.boot.flash.locked`, `ro.boot.vbmeta.device_state`, `ro.build.type`, `ro.debuggable`, `ro.adb.secure`; also `adb shell getenforce` and `adb shell id`.
- Inspect read-only `/dev/block/by-name`, `/dev/block/mapper`, `/proc/mounts` and `/vendor/etc/vintf/manifest.xml`. Determine whether `su` or `adb root` is present. Do not assume.
- Check rescue/boot modes with vendor documentation before switching recovery or unlocking. `fastbootd` is not assured by Android 13 or dynamic partitions.
- For modifications, back up public system partitions and **privately back up all device-specific persist, factory/eeprom, project ID and calibration regions** first; validate hash and restore procedure. Do not publish private dumps.

## Source reports

- [Detailed diff](README.md), [raw comparison JSON](comparison.json), [stock AVB signatures](AVB.md).
- [One HDMI vendor update script](../One_HDMI/upgrade_script.txt), [two HDMI vendor update script](../Original_Firmware/decrypted/upgrade_script.txt).

## Decision

Use a **board-matched stock Android 13** as the base, preserve Linux/MTK HAL/ToF/audio/HDMI, and replace/update manufacturer-facing interface incrementally. Existing `TvSettingsPlus` is a potentially useful entry point. A clean LineageOS/AOSP port remains an optional later experiment, not the first step.

### Evidence limitations

This report proves the static structure and hashes, not that the bootloader accepts unsigned PKGs, that AVB enforcement is active, that stock keys can be reused, or that CineLux hardware is fully interchangeable with FlixTone D11 Master. APK reverse-engineering still required to determine APIs and safe package removal dependencies.
