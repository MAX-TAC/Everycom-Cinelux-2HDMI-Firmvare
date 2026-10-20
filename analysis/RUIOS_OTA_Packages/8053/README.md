# RUIOS OTA package 8053

ZIP size: 841648271 bytes
File count: 7

## ZIP file entries

| Name | Uncompressed bytes | Compressed bytes |
|---|---:|---:|
| META-INF/com/android/metadata | 698 | 698 |
| META-INF/com/android/metadata.pb | 1179 | 1179 |
| apex_info.pb | 0 | 0 |
| care_map.pb | 563 | 563 |
| payload.bin | 841642056 | 841642056 |
| payload_properties.txt | 154 | 154 |
| META-INF/com/android/otacert | 1675 | 943 |

## Android payload format
~~~json
{
  "size": 841642056,
  "magic": "CrAU",
  "format_version": 2,
  "manifest_size": 45920,
  "metadata_signature_size": 267
}
~~~

## Small OTA metadata files

### META-INF/com/android/metadata
~~~
ota-property-files=payload_metadata.bin:2719:46211,payload.bin:2719:841642056,payload_properties.txt:841644833:154,apex_info.pb:2062:0,care_map.pb:2109:563,metadata:69:698,metadata.pb:835:1179                      
ota-required-cache=0
ota-streaming-property-files=payload.bin:2719:841642056,payload_properties.txt:841644833:154,apex_info.pb:2062:0,care_map.pb:2109:563,metadata:69:698,metadata.pb:835:1179                        
ota-type=AB
post-build=MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/eng.luzhih.20260612.083454:userdebug/test-keys
post-build-incremental=eng.luzhih.20260612.083454
post-sdk-level=33
post-security-patch-level=2026-04-05
post-timestamp=1781253379
pre-device=mt5873

~~~

### META-INF/com/android/metadata.pb
~~~
"�
ota-property-files�payload_metadata.bin:2719:46211,payload.bin:2719:841642056,payload_properties.txt:841644833:154,apex_info.pb:2062:0,care_map.pb:2109:563,metadata:69:698,metadata.pb:835:1179                      "�
ota-streaming-property-files�payload.bin:2719:841642056,payload_properties.txt:841644833:154,apex_info.pb:2062:0,care_map.pb:2109:563,metadata:69:698,metadata.pb:835:1179                        *
mt58732�
mt5873^MediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/eng.luzhih.20260612.083454:userdebug/test-keyseng.luzhih.20260612.083454 ����*332
2026-04-05:q
bootmt5873UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys"
1781253379:t
productmt5873UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys"
1781253379:s
systemmt5873UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys"
1781253379:w

system_extmt5873UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys"
1781253379:s
vendormt5873UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys"
1781253379
~~~

### care_map.pb
~~~

�
product	2,0,18461ro.product.build.fingerprint"UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys
�
system
2,0,151044ro.system.build.fingerprint"UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys
�

system_ext	2,0,21046ro.system_ext.build.fingerprint"UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys
�
vendor	2,0,43311ro.vendor.build.fingerprint"UMediaTek/mt5873_cd/mt5873:13/TP1A.220624.021.A1/luzhiheng06120828:userdebug/test-keys
~~~

### payload_properties.txt
~~~
FILE_HASH=L9iiH5WmIgIbt8+a1IafosdeXdeZrq7vwG4ps1TBjNc=
FILE_SIZE=841642056
METADATA_HASH=1/y5SElq38DBO2EQ8tJsRvOtBKKfJuo26VNkAozfmF8=
METADATA_SIZE=45944

~~~

### META-INF/com/android/otacert
~~~
-----BEGIN CERTIFICATE-----
MIIEqDCCA5CgAwIBAgIJAJNurL4H8gHfMA0GCSqGSIb3DQEBBQUAMIGUMQswCQYD
VQQGEwJVUzETMBEGA1UECBMKQ2FsaWZvcm5pYTEWMBQGA1UEBxMNTW91bnRhaW4g
VmlldzEQMA4GA1UEChMHQW5kcm9pZDEQMA4GA1UECxMHQW5kcm9pZDEQMA4GA1UE
AxMHQW5kcm9pZDEiMCAGCSqGSIb3DQEJARYTYW5kcm9pZEBhbmRyb2lkLmNvbTAe
Fw0wODAyMjkwMTMzNDZaFw0zNTA3MTcwMTMzNDZaMIGUMQswCQYDVQQGEwJVUzET
MBEGA1UECBMKQ2FsaWZvcm5pYTEWMBQGA1UEBxMNTW91bnRhaW4gVmlldzEQMA4G
A1UEChMHQW5kcm9pZDEQMA4GA1UECxMHQW5kcm9pZDEQMA4GA1UEAxMHQW5kcm9p
ZDEiMCAGCSqGSIb3DQEJARYTYW5kcm9pZEBhbmRyb2lkLmNvbTCCASAwDQYJKoZI
hvcNAQEBBQADggENADCCAQgCggEBANaTGQTexgskse3HYuDZ2CU+Ps1s6x3i/waM
qOi8qM1r03hupwqnbOYOuw+ZNVn/2T53qUPn6D1LZLjk/qLT5lbx4meoG7+yMLV4
wgRDvkxyGLhG9SEVhvA4oU6Jwr44f46+z4/Kw9oe4zDJ6pPQp8PcSvNQIg1QCAcy
4ICXF+5qBTNZ5qaU7Cyz8oSgpGbIepTYOzEJOmc3Li9kEsBubULxWBjf/gOBzAzU
RNps3cO4JFgZSAGzJWQTT7/emMkod0jb9WdqVA2BVMi7yge54kdVMxHEa5r3b97s
zI5p58ii0I54JiCUP5lyfTwE/nKZHZnfm644oLIXf6MdW2r+6R8CAQOjgfwwgfkw
HQYDVR0OBBYEFEhZAFY9JyxGrhGGBaR0GawJyowRMIHJBgNVHSMEgcEwgb6AFEhZ
AFY9JyxGrhGGBaR0GawJyowRoYGapIGXMIGUMQswCQYDVQQGEwJVUzETMBEGA1UE
CBMKQ2FsaWZvcm5pYTEWMBQGA1UEBxMNTW91bnRhaW4gVmlldzEQMA4GA1UEChMH
QW5kcm9pZDEQMA4GA1UECxMHQW5kcm9pZDEQMA4GA1UEAxMHQW5kcm9pZDEiMCAG
CSqGSIb3DQEJARYTYW5kcm9pZEBhbmRyb2lkLmNvbYIJAJNurL4H8gHfMAwGA1Ud
EwQFMAMBAf8wDQYJKoZIhvcNAQEFBQADggEBAHqvlozrUMRBBVEY0NqrrwFbinZa
J6cVosK0TyIUFf/azgMJWr+kLfcHCHJsIGnlw27drgQAvilFLAhLwn62oX6snb4Y
LCBOsVMR9FXYJLZW2+TcIkCRLXWG/oiVHQGo/rWuWkJgU134NDEFJCJGjDbiLCpe
+ZTWHdcwauTJ9pUbo8EvHRkU3cYfGmLaLfgn9gP+pWA7LFQNvXwBnDa6sppCccEX
31I828XzgXpJ4O+mDL1/dBd+ek8ZPUP0IgdyZm5MTYPhvVqGCHzzTy3sIeJFymwr
sBbmg2OAUNLEMO6nwmocSdN2ClirfxqCzJOLSDE4QyS9BAH6EhY6UFcOaE0=
-----END CERTIFICATE-----

~~~
