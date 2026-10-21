# Сопоставление ключа проекторов 8052/8054 с открытыми тестовыми ключами

Сравниваются бинарные AVB-публичные ключи RSA4096, вычисленные **из опубликованных** PEM-файлов в открытых репозиториях.
Самих закрытых ключей проекторов здесь нет. Публичные примеры тестовых ключей не публикуются повторно.

Проверено файлов: 56; распознано RSA4096-ключей: 22; совпадений: 0.

| Исходный файл в публичном репозитории | SHA256 (ключ AVB) | Совпадение |
|---|---|---|
| unisoc-reference/keys/rsa4096_modem.pem | c1694a13baf4185f6dbc522c15393dffa23de9f1276ac1d7a0d42addcd5cc60f | False |
| unisoc-reference/keys/rsa4096_system.pem | 754a54e3a8f4e8cc339cf7c55c708f9ae30bf3ee54e00bd7e935bda104ecdd6b | False |
| unisoc-reference/keys/rsa4096_product.pem | 31d44f8f7baf629fcc00bfc7f9fceea1fbdfc7fe6139e5c418efe2fe0690ab68 | False |
| unisoc-reference/keys/rsa4096_boot.pem | eb0619c347731386b26d1a116a5705a437e3268d840d892d7fa83400ea89466f | False |
| unisoc-reference/keys/rsa4096_vendor.pem | db43fce3407465af0dee506d2318108d636a756d00cae1e0be9b725b58784c78 | False |
| unisoc-reference/keys/rsa4096_vbmeta.pem | 7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6 | False |
| unisoc-reference/keys/rsa4096_recovery.pem | 54b4e2a6902dddd7e128dab52127f4c34bd178c33ac66f2f61dca54cbf7e199d | False |
| nccgroup/sample/aosp/external/avb/test/data/sign_key.pem | f2cfc4f17ccc67ac11e6223ca6a2594decf865603aed8895adb68c868e77ee47 | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_atx_psk.pem | 7ec02ee1be696366f3fa91240a8ec68125c4145d698f597aa2b3464b59ca7fc3 | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_rsa4096_oneplus.pem | cf2f0bc143c118fe0075574ae952bac295b99045c2b2557566f176f48644da5f | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_rsa4096_pub.pem | 7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6 | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_rsa4096.pem | 7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6 | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_atx_pik.pem | ce464c0fefc023760adc3fe0207c282d337e1b91e3df7ab4fee43fcd620db46d | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_rsa4096_realtek.pem | ec2647574df2ea01127ee210f838965daa884e61888c49bbf6a9c59457f46b89 | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_atx_prk.pem | 86b04a9d62807fda80cbf445118e8a4a73aa5937283b49e018e432dd8e3a76a1 | False |
| nccgroup/sample/aosp/external/avb/test/data/testkey_atx_puk.pem | c608ffa5e7ee92984f4486e03088440c360cf315ec6a5f52aef790cb30efcec9 | False |
| aosp-signing-example/tools/avb-tools/test/data/testkey_cert_pik.pem | ce464c0fefc023760adc3fe0207c282d337e1b91e3df7ab4fee43fcd620db46d | False |
| aosp-signing-example/tools/avb-tools/test/data/testkey_rsa4096_pub.pem | 7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6 | False |
| aosp-signing-example/tools/avb-tools/test/data/testkey_rsa4096.pem | 7728e30f50bfa5cea165f473175a08803f6a8346642b5aa10913e9d9e6defef6 | False |
| aosp-signing-example/tools/avb-tools/test/data/testkey_cert_puk.pem | c608ffa5e7ee92984f4486e03088440c360cf315ec6a5f52aef790cb30efcec9 | False |
| aosp-signing-example/tools/avb-tools/test/data/testkey_cert_prk.pem | 86b04a9d62807fda80cbf445118e8a4a73aa5937283b49e018e432dd8e3a76a1 | False |
| aosp-signing-example/tools/avb-tools/test/data/testkey_cert_psk.pem | 7ec02ee1be696366f3fa91240a8ec68125c4145d698f597aa2b3464b59ca7fc3 | False |

Список источников: https://github.com/nccgroup/test_avb_key ; https://github.com/alltechdev/haha-you-used-testkeys ; https://github.com/TheGammaSqueeze/UnisocBypass

Отрицательный результат относится только к перечисленным опубликованным кандидатам. Это не доказательство отсутствия ключа в интернете.
