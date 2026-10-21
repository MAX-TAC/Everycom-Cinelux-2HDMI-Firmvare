# Image and source defaults: ConfigDefaultValue.ini, Oct 8052 vs Sep 8054

Factory 8054 metadata was extracted from the SHA-verified stock PKG in GitHub Actions run 39452884650.
October 8052 file was extracted read-only from the verified OTA payload.

Stock lines: 11265; OTA lines: 11265; changed blocks: 14; removed/added lines: 14/14.

Note: differences in config text can be changed defaults, comments or firmware version updates; not proof of physical board differences.

## Changed ranges and sanitized excerpts

### Change 1 (replace)
Stock lines [686, 686], OTA lines [686, 686]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 2 (replace)
Stock lines [693, 693], OTA lines [693, 693]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 3 (replace)
Stock lines [700, 700], OTA lines [700, 700]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 4 (replace)
Stock lines [707, 707], OTA lines [707, 707]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 5 (replace)
Stock lines [714, 714], OTA lines [714, 714]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 6 (replace)
Stock lines [721, 721], OTA lines [721, 721]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 7 (replace)
Stock lines [728, 728], OTA lines [728, 728]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 8 (replace)
Stock lines [735, 735], OTA lines [735, 735]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 9 (replace)
Stock lines [742, 742], OTA lines [742, 742]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 10 (replace)
Stock lines [749, 749], OTA lines [749, 749]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 11 (replace)
Stock lines [756, 756], OTA lines [756, 756]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 12 (replace)
Stock lines [763, 763], OTA lines [763, 763]

8054 stock:
- 70,75,50,\

8052 OTA:
- 80,75,50,\

### Change 13 (replace)
Stock lines [11077, 11077], OTA lines [11077, 11077]

8054 stock:
- # [redacted]

8052 OTA:
- [sensitive key redacted]

### Change 14 (replace)
Stock lines [11079, 11079], OTA lines [11079, 11079]

8054 stock:
- # [redacted]

8052 OTA:
- [sensitive key redacted]

## Interpretation

- Do not swap the entire file across profiles based only on a small diff.
- Determine which of the changed keys influences input source, picture defaults, brightness and panel calibration before changing values.
- Read-only static evidence: no GPIO, I2C, flash or display setting was modified.

