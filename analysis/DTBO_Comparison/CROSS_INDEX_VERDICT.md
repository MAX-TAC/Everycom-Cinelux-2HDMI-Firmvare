# Correct DTBO comparison: ignore entry ordering

The preliminary same-index diff flags 203 / 207 entries as different; **that is a misleading comparison because the overlay records were reordered between the two firmware builds**.

A content-based comparison of all 207 decompressed device-tree blobs from the one-HDMI and two-HDMI images finds **207 / 207 identical entries as a multiset (SHA256, including multiplicities)**.

- 207 total entries in both images.
- 4 matching at the same index.
- 203 reordered entries (content preserved).
- **0 device-tree blobs are present only in one firmware.**
- Both DTBO tables use the same 32-byte-entry format, the same entry IDs and revision metadata per index. The table header and ordering differ.
- Selection by an index, rather than by content, could still result in wrong electrical configuration if a DTBO image is cross-flashed.

This is very strong static evidence that **the stock kernel DTBO overlay repertoire is shared**. It is **not proof that the physical PCBs are interchangeable**, that the same particular overlay is active, or that cross-flashing stock DTBO is safe.

Verification: [raw DTBO extracted hashes and per-index comparison](diff.json). This note supersedes the naive "203 entries differ" interpretation.
