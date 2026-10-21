# Bootchain partitions: latest 8052 OTA versus original factory 8054

SHA from SHA256-verified release artifacts. No bootloader code executed or firmware flashed.

| Partition | Same bytes? | OTA bytes | Factory 8054 bytes |
|---|---|---:|---:|
| boot | False | 78643200 | 78643200 |
| mboot | False | 2658304 | 2658304 |
| optee | False | 2809856 | 2806432 |
| vbmeta | False | 12288 | 12288 |
| vbmeta_system | False | 4096 | 4096 |
| dtbo | False | 8388608 | 8388608 |
| armfw | False | 77824 | 77088 |

Interpretation: byte differences are not yet classified as changed executable code, bug fixes, signatures, dates or board-specific constants.
Do not combine images from different revisions until live boot trust and recovery are understood.

