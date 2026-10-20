# MStar unpacker test on CineLux firmware
The unchanged upgrade_image.pkg was accessed under the name upgrade_image.bin using a symlink.
Tool: dipcore/mstar-bin-tool commit edd1a54cd5531ee98b82378ceeff9a246aced064.
The tool expects a 16 KiB header with a readable MStar command script.
First FF delimiter offset: 205
Initial 80 bytes (hex): 49 e2 5e 4b b3 5e 20 b1 a9 ba 43 32 e2 3a 74 9d ba a6 ad b6 d0 66 86 da 82 99 b9 c0 cf 6f 9a a2 be 7b 37 9a 63 88 ae 7c 32 51 4e 77 f3 1a 22 5c db 8b d4 03 18 d0 dc 29 12 c1 07 ce f0 0b 21 e2 08 56 08 a3 9f 5d cc af 06 38 02 41 58 67 c1 c1
Pre-delimiter header decodes as UTF-8: NO, 'utf-8' codec can't decode byte 0xe2 in position 1: invalid continuation byte
Original unpack.py exit code: 1
STDOUT:
[i] Analizing header ...

STDERR:
/tmp/mstar-bin-tool/utils.py:152: SyntaxWarning: invalid escape sequence '\$'
  keys = re.findall('\$\((\w+)\)', line)
/tmp/mstar-bin-tool/utils.py:159: SyntaxWarning: invalid escape sequence '\s'
  args = re.findall('([^\s]+)\s+([^\s]+)\s*(.*)', line)
/tmp/mstar-bin-tool/utils.py:167: SyntaxWarning: invalid escape sequence '\s'
  return re.findall('([^\s]+)', string)
Traceback (most recent call last):
  File "/tmp/mstar-bin-tool/unpack.py", line 44, in <module>
    headerScript = header[:offset].decode()
                   ^^^^^^^^^^^^^^^^^^^^^^^^
UnicodeDecodeError: 'utf-8' codec can't decode byte 0xe2 in position 1: invalid continuation byte

Extracted output files: ['/tmp/mstar-output/~header']
