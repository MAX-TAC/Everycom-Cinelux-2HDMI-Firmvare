# AVB (vbmeta) comparison

Info extracted directly from stock vendor images. This is NOT verification that the bootloader is unlocked.

| Partition | 1 HDMI algorithm ID | 2 HDMI algorithm ID | 1 HDMI auth size | 2 HDMI auth size |
|---|---:|---:|---:|---:|
| vbmeta_a | 2 | 2 | 576 | 576 |
| vbmeta_system_a | 2 | 2 | 576 | 576 |

AVB algorithm ID 0 means NONE. Other IDs refer to cryptographic signature algorithms and require matching trusted keys.
Stock PKG wrapper signatures are independent of AVB metadata.
