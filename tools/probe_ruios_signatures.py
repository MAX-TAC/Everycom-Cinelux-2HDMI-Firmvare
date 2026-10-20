#!/usr/bin/env python3
"""Inspect Android A/B OTA payload signature representation and compare to advertised cert.
No exploit or modifications; read only and do not export any private keys.
"""
from pathlib import Path
import sys,zipfile,subprocess,hashlib,json
zip_path=Path(sys.argv[1]);out=Path(sys.argv[2]);out.parent.mkdir(parents=True,exist_ok=True)
with zipfile.ZipFile(zip_path) as z:
  cert=z.read('META-INF/com/android/otacert')
  with z.open('payload.bin') as p:
    head=p.read(24)
    manifest=p.read(int.from_bytes(head[12:20],'big'))
    sigblob=p.read(int.from_bytes(head[20:24],'big'))
def varint(buf,idx):
  v=0;shift=0
  while idx<len(buf):
    n=buf[idx];idx+=1;v|=(n&127)<<shift
    if n<128:return v,idx
    shift+=7
  raise ValueError('incomplete varint')
def parse(buf):
  fields=[];pos=0
  while pos<len(buf):
    fieldtag,pos=varint(buf,pos);wire=fieldtag&7;num=fieldtag>>3
    if wire==2:
      n,pos=varint(buf,pos);value=buf[pos:pos+n];pos+=n
    elif wire==0:value,pos=varint(buf,pos)
    elif wire==5:value=buf[pos:pos+4];pos+=4
    elif wire==1:value=buf[pos:pos+8];pos+=8
    else:raise ValueError('wire='+str(wire)+' position='+str(pos))
    fields.append((num,wire,value))
  return fields
report={'head':head.hex(),'sigblob_length':len(sigblob),'sigblob_first_64_hex':sigblob[:64].hex(),
        'fields':[],'tests':[]}
candidates=[]
try:
  fields=parse(sigblob)
  for num,wire,val in fields:
    report['fields'].append({'field':num,'wire':wire,'len':len(val) if isinstance(val,bytes) else None,
                             'preview':val[:30].hex() if isinstance(val,bytes) else val})
    if isinstance(val,bytes) and len(val) in (128,256,384,512):candidates.append(val)
    if isinstance(val,bytes):
      try:
        for num2,w2,val2 in parse(val):
          report['fields'].append({'nested':num,'field':num2,'wire':w2,'len':len(val2) if isinstance(val2,bytes) else None,
                    'preview':val2[:20].hex() if isinstance(val2,bytes) else val2})
          if isinstance(val2,bytes) and len(val2) in (128,256,384,512):candidates.append(val2)
      except Exception as e:report['fields'].append({'nested':num,'error':str(e)[:150]})
except Exception as e:report['parsing_error']=str(e)
if len(sigblob) in (128,256,384,512):candidates.append(sigblob)
Path('/tmp/cert.pem').write_bytes(cert)
subprocess.run(['openssl','x509','-in','/tmp/cert.pem','-pubkey','-noout','-out','/tmp/ota_pub.pem'],check=True)
meta=head+manifest
pre=bytes.fromhex('3031300d060960864801650304020105000420')
for candidate in candidates:
  Path('/tmp/sig.bin').write_bytes(candidate)
  p=subprocess.run(['openssl','pkeyutl','-verifyrecover','-pubin','-inkey','/tmp/ota_pub.pem',
                   '-in','/tmp/sig.bin','-pkeyopt','rsa_padding_mode:pkcs1','-out','/tmp/decrypted_sig.bin'],
                   capture_output=True,text=True)
  dec=Path('/tmp/decrypted_sig.bin').read_bytes() if p.returncode==0 else b''
  digest=hashlib.sha256(meta).digest()
  checks={'sig_len':len(candidate),'recovered_len':len(dec),'public_key_check_success':p.returncode==0,
          'raw_sha256_match':dec==digest,'digestinfo_sha256_match':dec==pre+digest,
          'sha256_digestinfo_suffix_match':dec.endswith(digest),'recovered_preview':dec[:32].hex(),
          'error':p.stderr[-200:] if p.returncode else ''}
  report['tests'].append(checks)
out.write_text(json.dumps(report,indent=2))
print(json.dumps(report,indent=2))
