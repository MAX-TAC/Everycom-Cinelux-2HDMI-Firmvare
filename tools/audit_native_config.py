#!/usr/bin/env python3
"""Static native ELF/config/DTBO inspection, no execution of OEM binaries."""
from pathlib import Path
import sys,json,re,hashlib,subprocess,collections,struct
from elftools.elf.elffile import ELFFile
base=Path(sys.argv[1]);parts=Path(sys.argv[2]);name=sys.argv[3];dest=Path(sys.argv[4]);dest.parent.mkdir(exist_ok=True,parents=True)
sensitive=re.compile(r'(?i)(serial|password|passwd|secret|token|private|mac_address|macaddr|imei|ssid|widevine|hdcp|drm.?key|device.?id|auth.?key|public.?key)')
focus=re.compile(r'(?i)(mtk|mstar|trd|i2c|hdmi|cec|audio|display|video|tof|focus|motor|camera|keystone|project|tvconfig|tvservice|dolby|dts|alsa|codec|vintf|init.|boot|power|input|source)')
extensions=('.xml','.prop','.rc','.ini','.cfg','.conf','.properties','.kl','.json','.txt')
result={'variant':name,'native':{},'configs':{},'dtbo':{},'firmware_images':{}}
def sha(b):return hashlib.sha256(b).hexdigest()
for partition in base.iterdir():
  if not partition.is_dir():continue
  for f in partition.rglob('*'):
    if not f.is_file() or f.is_symlink():continue
    rel=partition.name+'/'+f.relative_to(partition).as_posix()
    if '/firmware/' in rel and f.stat().st_size>=1000000:continue
    if f.suffix=='.so' or f.name.endswith('-service') or ('/bin/' in rel and focus.search(f.name)):
      with f.open('rb') as stream:
        if stream.read(4)!=b'\x7fELF':continue
        stream.seek(0)
        try:
          elf=ELFFile(stream)
          sections={}
          for section in ('.text','.rodata','.data.rel.ro'):
            part=elf.get_section_by_name(section)
            if part is not None and part['sh_size']<100*1024*1024:
              sections[section]={'size':part['sh_size'],'sha256':sha(part.data())}
          dyn=elf.get_section_by_name('.dynamic')
          deps=[]
          if dyn:
            for tag in dyn.iter_tags():
              if tag.entry.d_tag=='DT_NEEDED':deps.append(tag.needed)
          exports=set()
          sym=elf.get_section_by_name('.dynsym')
          if sym:
            for item in sym.iter_symbols():
              if len(exports)>120:break
              symbol=item.name
              if symbol and focus.search(symbol):exports.add(symbol[:150])
          result['native'][rel]={'sha256':sha(f.read_bytes()) if f.stat().st_size<35*1024*1024 else None,
            'bytes':f.stat().st_size,'elf_class':elf.elfclass,'machine':elf.get_machine_arch(),
            'sections':sections,'needed':sorted(deps),'hardware_exports':sorted(exports)}
        except Exception as e:
          result['native'][rel]={'error':str(e)[:250]}
    if f.suffix.lower() in extensions and f.stat().st_size<512*1024:
      if not focus.search(rel) and f.name not in ('build.prop','default.prop'):continue
      try:
        txt=f.read_text(errors='replace')
        if '\0' in txt[:500]:continue
        lines=[]
        for line in txt.splitlines()[:2000]:
          if sensitive.search(line):
            lines.append('[REDACTED SENSITIVE LINE]')
          else:
            # Preserve only lines likely to describe hardware/software config, not personal state
            lines.append(line[:400])
        result['configs'][rel]={'sha256':sha(f.read_bytes()),'bytes':f.stat().st_size,
            'lines':lines}
      except Exception:pass
for target in ('dtbo_a','boot_a','mboot_a','tvconfig_a','tvservice_a','project_id','emmc_boot'):
  f=parts/(target+'.img')
  if not f.exists():continue
  buf=f.open('rb').read(65536)
  result['firmware_images'][target]={'size':f.stat().st_size,'header32':buf[:32].hex(' ')}
  if target=='dtbo_a':
    result['dtbo']={'bytes':f.stat().st_size,'head64':buf[:64].hex(' ')}
    if buf[:4]==bytes.fromhex('d7b7ab1e'):
      # Android DTBO image header: >8 u32s (magic, total_size, header_size, entry_size,
      # entry_count, entries_offset, page_size, version)
      vals=struct.unpack('>8I',buf[:32])
      result['dtbo']['table']={
       'magic':hex(vals[0]),'total_size':vals[1],'header_size':vals[2],
       'dt_entry_size':vals[3],'dt_entry_count':vals[4],'dt_entries_offset':vals[5],
       'page_size':vals[6],'version':vals[7]}
dest.write_text(json.dumps(result,ensure_ascii=False,indent=1),encoding='utf8')
print(name,'native',len(result['native']),'configs',len(result['configs']),
     'dtbo',result['dtbo'],'size',dest.stat().st_size,flush=True)
