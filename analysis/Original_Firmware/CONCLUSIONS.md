# Everycom CineLux 2-HDMI — firmware analysis conclusions

Source release: Original_Firmware / 4KTOF.HDMI-.-DPLS.-09.30.rar. Firmware was NOT installed on any device.

## Verified structure

- RAR size: 1,301,025,233 bytes; SHA-256 `170f745dc1711c2dae6410dd51f0a8bf5bb7c637e11b8dd3e5f59fbea8c388f3`.
- Only RAR member: `upgrade_image.pkg`, 1,301,025,152 bytes; SHA-256 `4abef5d594803d09c20316a7cd52ab623dd7fb1a228472eb0e243d6d750ebb4c`.
- Archive is almost exactly same size as internal PKG, with only 81 bytes difference. Typical of incompressible data.
- Standard `file` only identifies the PKG as generic `data`. Its initial bytes do not show a conventional Android boot, sparse, EROFS, SquashFS, ZIP, or MStar upgrade header.
- Full-file Binwalk reported many mutually inconsistent magic coincidences (e.g., MySQL, Cisco IOS, SWF), almost certainly false positives. Do NOT treat these as partitions.

## Entropy sampling (1 MiB samples at eight different offsets)

| Offset | Shannon entropy, bits per byte |
|---:|---:|
| 0 | 7.998171 |
| 4,096 | 7.999837 |
| 65,536 | 7.999841 |
| 1,048,576 | 7.999839 |
| 325,256,288 | 7.999819 |
| 650,512,576 | 7.999813 |
| 975,768,864 | 7.999830 |
| 1,299,976,576 | 7.999816 |

Entropy is consistently almost the maximum of 8 bits/byte. Combined with an incompressible archive and no intelligible partitions/strings, this is **strong evidence of encrypted or extremely densely packed data**, but not proof of a particular cipher or header format. A version-like ASCII fragment `V_0.0.0` occurs in the header; no board model is verified.

## Specialized unpacking attempt

- Built openlgtv/epk2extract v4.8 from pinned Git commit `2b6af078b56dbedb89efc0f4943036150f1ecae9` on a GitHub Actions runner, read-only.
- Tool output: `Unsupported input file format: /tmp/firmware/upgrade_image.pkg`, exit 1.
- This means epk2extract's known MTK PKG variants do NOT decode this particular file using its available keys or auto-detection. It does **not** prove that decoding is fundamentally impossible.
- Build logs and entropy/probe artifact: GitHub Actions run 39385888104, named `mtkpkg-probe`.

## Relation to FlixTone D11 Master

- Everycom describes two-HDMI CineLux as Android 13, MTK9660, 2 GB RAM, 32 GB storage, autofocus and keystone. Source: https://everycomprojector.com/blogs/blog/everycom-cinelux-4k-projector-the-ultimate-home-entertainment-gaming-solution
- These public specs are consistent with a closely related D11 Master **variant**, but neither exact PCB revision nor pinout, bootloader, DTB, EEPROM/NVRAM/calibration partition layout or AVB keys are available from this opaque package.
- Do **not** flash CineLux PKG on D11 until a manufacturer confirms compatibility or board identifiers have been independently matched. Matching 2x HDMI/1x USB and SoC is not sufficient.
- Claims about Dolby certification or audio features must be checked against the actual vendor build and hardware, not inferred from connector counts or image name.

## Next engineering options

1. Obtain an unpacked or non-encrypted `system.img` / `super.img` / partition dump from a compatible projector; ask seller for `flash-tool` / engineering package, device PCB ID and recovery instructions.
2. When D11 arrives, run read-only ADB diagnostics (getprop, mount info, `/dev/block/by-name`, `/dev/block/mapper`, VINTF and SELinux). If rooted, take hashed read-only dumps of non-sensitive system, vendor, product and boot partitions, and private backup of device-specific calibration before experimenting.
3. Identify the exact loader/recovery accepted PKG format and whether the version is decryptable in the OEM SDK. Do not attempt to repack or bypass signatures blindly.
4. For custom Android TV settings, retain hardware HAL and write device-specific bridges as demonstrated by Lumen OS. A decrypted partition dump is more valuable for this than a black-box PKG.

## Reproducible reports

- [Full file triage](README.md)
- [Machine-readable scan](triage.json)
- [Quick structure](quick_structure.md)
- [Actions: full scan](https://github.com/MAX-TAC/Everycom-Cinelux-2HDMI-Firmvare/actions/runs/39384955783)
- [Actions: MTK PKG extraction probe](https://github.com/MAX-TAC/Everycom-Cinelux-2HDMI-Firmvare/actions/runs/39385888104)
