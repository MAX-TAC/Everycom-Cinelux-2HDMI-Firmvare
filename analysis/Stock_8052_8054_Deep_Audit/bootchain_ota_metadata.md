# Bootchain and AVB: original October OTA 8052

All metadata obtained by read-only inspection of the original OTA payload. No device was accessed.

## Image headers, cryptographic fields and software provenance

| Partition | Bytes | SHA-256 prefix | Key checks |
|---|---:|---|---|
| boot | 78643200 | 094585da7764ff78c9 | Android boot header=True |
| mboot | 2658304 | 8819cc068a7a05243e |  |
| optee | 2809856 | 7f1b13494c08f5b796 |  |
| vbmeta | 12288 | d9c0035e7884d7dcd6 | AVB=True, key_equal_factory8054=True, flags=0, rollback_index=0, algo=2 |
| vbmeta_system | 4096 | 11989885485f32576a | AVB=True, key_equal_factory8054=True, flags=0, rollback_index=0, algo=2 |
| dtbo | 8388608 | 755b9158991a31c88c | DTBO entries=207 |
| armfw | 77824 | 8809923c93bd860ae2 |  |

## Bootloader and OP-TEE static string hints (counts are NOT capabilities)

- mboot: {'fastboot': 17, 'vbmeta': 39, 'verity': 20, 'rollback': 14, 'secureboot': 0, 'androidboot': 43, 'bootargs': 42, 'recovery': 44, 'unlock': 17, 'dtbo': 104, 'optee': 15, 'usb': 330, 'avb': 81, 'verify': 91}
- optee: {'fastboot': 0, 'vbmeta': 0, 'verity': 0, 'rollback': 0, 'secureboot': 0, 'androidboot': 0, 'bootargs': 0, 'recovery': 0, 'unlock': 0, 'dtbo': 0, 'optee': 2, 'usb': 0, 'avb': 0, 'verify': 0}

## Hardware-only unknowns and release blockers

- Cannot conclude the bootloader trusts a user-signed PKG or vbmeta. A matching public key only identifies the stock signing key.
- Cannot conclude that a live device allows fastboot/fastbootd, OEM unlock, root or a downgrade.
- Need actual slot/SELinux/verifiedbootstate/flash.locked/avb rollback values from a real device.
- Device-specific unique partitions and calibration require a private backup and verified restoration path BEFORE any update.
- Never use factory updater commands containing erase/wipe as the custom installer.

