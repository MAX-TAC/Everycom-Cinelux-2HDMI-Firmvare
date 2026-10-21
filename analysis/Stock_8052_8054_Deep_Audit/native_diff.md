# Latest 8052 OTA vs factory 8054: native executable code and boot partition audit

Source 1: verified RUIOS.8052.1.0.4 official A/B OTA payload (October 2026).
Source 2: SHA-verified RUIOS.8054.1.0.1 original September factory archive, *previous run native and physical inventories*.
Scripts only read trusted source images, never execute binaries or flash the device.

## Native ELF comparison

| Classification | Number |
|---|---:|
| byte_identical | 1333 |
| executable_text_differs | 1 |
| same_executable_text_but_other_bytes_differ | 1 |

- Matched native ELF paths: 1335
- ELF paths only in OTA/factory: 0/0
- Relevant ELF with changed .text: 0.

## Changed .text in likely hardware code

| Path | Bytes OTA / factory | Added dependencies | Removed dependencies |
|---|---|---|---|
| No differing code-section SHA in selected paths | — | — | — |

## Full original physical boot / TV partitions

| Partition | SHA identical? | OTA bytes | 8054 factory bytes |
|---|---|---:|---:|
| 3rd | not comparable | — | — |
| armfw | False | 77824 | 77088 |
| boot | False | 78643200 | 78643200 |
| bootdata | False | 41943040 | 41943040 |
| dtbo | False | 8388608 | 8388608 |
| factory | not comparable | — | — |
| linux_rootfs | not comparable | — | — |
| mboot | False | 2658304 | 2658304 |
| optee | False | 2809856 | 2806432 |
| tvconfig | False | 157286400 | 157286400 |
| tvservice | False | 175112192 | 175112192 |
| vbmeta | False | 12288 | 12288 |
| vbmeta_system | False | 4096 | 4096 |

## Code vs metadata vs hardware inference

- **Byte-identical** indicates same full ELF bytes.
- **Same executable .text** indicates the same .text bytecode but differences may remain in data, relocations or dynamic symbols.
- **Different executable .text** confirms machine-code changes, but does not tell whether a bug fix, OEM enhancement or a board-dependent change.
- Firmware image SHA differences can reflect embedded build dates and signatures as well as functional changes.
- No conclusions about compatibility or actual fuse/locked boot state follow from images alone.
- Do not swap any boot, OP-TEE, PMU, ToF, panel or TVservice component until there is a proven recovery path and live board identification.

## Prioritized follow-up

1. For each changed ELF .text identify matching source-service/ABI and symbol changes; disassembly and targeted manual review required to classify intent.
2. Compare bootloader bootargs and AVB policies via header inspection on stock images, not just SHA.
3. On a real 8052 and 8054 confirm boot state, running services and relevant hardware instances.
4. Keep this as reference metadata for future test builds; no modification until safe restoration verified.

