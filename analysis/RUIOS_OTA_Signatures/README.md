# OTA payload metadata signatures (RUIOS 8052 / 8053)

Static tests against the included AOSP test certificate. This does NOT prove device will accept a custom OTA.

| OTA | Signature protobuf fields | Candidate RSA signatures | RSA signatures valid for stock OTA metadata using embedded key |
|---|---:|---:|---:|
| 8052 | 3 | 1 | 1 |

## 8052
~~~json
{
  "head": "437241550000000000000002000000000000b4b70000010b",
  "sigblob_length": 267,
  "sigblob_first_64_hex": "0a88021280021e19e1537782c64a68e7e5bdd133b2f6f29d20648f589c9c53a4d5bfbde540f08467ee4aefda39da3f702def83861a144b2e0d954051b0a79525",
  "fields": [
    {
      "field": 1,
      "wire": 2,
      "len": 264,
      "preview": "1280021e19e1537782c64a68e7e5bdd133b2f6f29d20648f589c9c53a4d5"
    },
    {
      "nested": 1,
      "field": 2,
      "wire": 2,
      "len": 256,
      "preview": "1e19e1537782c64a68e7e5bdd133b2f6f29d2064"
    },
    {
      "nested": 1,
      "field": 3,
      "wire": 5,
      "len": 4,
      "preview": "00010000"
    }
  ],
  "tests": [
    {
      "sig_len": 256,
      "recovered_len": 51,
      "public_key_check_success": true,
      "raw_sha256_match": false,
      "digestinfo_sha256_match": true,
      "sha256_digestinfo_suffix_match": true,
      "recovered_preview": "3031300d060960864801650304020105000420a813c376011a72578ef74e88c2",
      "error": ""
    }
  ]
}
~~~
| 8053 | 3 | 1 | 1 |

## 8053
~~~json
{
  "head": "437241550000000000000002000000000000b3600000010b",
  "sigblob_length": 267,
  "sigblob_first_64_hex": "0a880212800206ea805c0fbe38eb951d11abdfa6d054773ab7f30064bfe8fcf7001a170f483609dbed4a3ec6f21804482358fa13e8bb040e69967c0a0b05bdb3",
  "fields": [
    {
      "field": 1,
      "wire": 2,
      "len": 264,
      "preview": "12800206ea805c0fbe38eb951d11abdfa6d054773ab7f30064bfe8fcf700"
    },
    {
      "nested": 1,
      "field": 2,
      "wire": 2,
      "len": 256,
      "preview": "06ea805c0fbe38eb951d11abdfa6d054773ab7f3"
    },
    {
      "nested": 1,
      "field": 3,
      "wire": 5,
      "len": 4,
      "preview": "00010000"
    }
  ],
  "tests": [
    {
      "sig_len": 256,
      "recovered_len": 51,
      "public_key_check_success": true,
      "raw_sha256_match": false,
      "digestinfo_sha256_match": true,
      "sha256_digestinfo_suffix_match": true,
      "recovered_preview": "3031300d060960864801650304020105000420d7fcb948496adfc0c13b6110f2",
      "error": ""
    }
  ]
}
~~~
