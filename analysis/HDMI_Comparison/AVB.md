# AVB (vbmeta) comparison

Info extracted directly from stock vendor images. This is NOT verification that the bootloader is unlocked.

| Partition | 1 HDMI algorithm ID | 2 HDMI algorithm ID | 1 HDMI auth size | 2 HDMI auth size |
|---|---:|---:|---:|---:|
| vbmeta_a | 2 | 2 | 576 | 576 |
| vbmeta_system_a | 2 | 2 | 576 | 576 |

## Stock public signing keys and verified boot flags

| Partition | Public-key SHA256 1 HDMI | Public-key SHA256 2 HDMI | Same key? | Flags (1/2) | Rollback index (1/2) |
|---|---|---|---|---|---|
| vbmeta_a | dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe | dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe | True | 0/0 | 0/0 |
| vbmeta_system_a | dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe | dcf38badcd7784d2aa892739eba5e239a649362edb03586a455b3f8ded046cfe | True | 0/0 | 0/0 |

AVB algorithm ID 0 means NONE. Other IDs refer to cryptographic signature algorithms and require matching trusted keys.
Stock PKG wrapper signatures are independent of AVB metadata.
