#!/usr/bin/env python3
"""Read-only audit of publicly exposed RUIOS OTA index files.
Respect resource limits, no credential bypass, no binary downloads, no directory probing.
"""
import urllib.request,urllib.error,time,json,hashlib,re
from pathlib import Path
root=Path('analysis/RUIOS_OTA_Discovery_Extended');root.mkdir(exist_ok=True,parents=True)
codes=list(range(8000,8045))+list(range(8071,8101))
results=[]
ua={'User-Agent':'CineLux-Firmware-Research/1.0 (small read-only public OTA metadata audit)'}
for code in codes:
    url=f'https://www.szrjyun.com/ota/android/mt9660/{code}/{code}_ota.json'
    record={'code':code,'url':url}
    try:
        req=urllib.request.Request(url,headers=ua,method='GET')
        with urllib.request.urlopen(req,timeout=12) as resp:
            raw=resp.read(256*1024+1)
            record.update({'status':resp.status,'bytes':len(raw),'content_type':resp.headers.get('Content-Type')})
        if len(raw)>256*1024:
            record['error']='unusually large JSON; skipped'
        else:
            try:
                doc=json.loads(raw)
                record['json']=doc
            except Exception:
                record['error']='response not valid JSON'
                record['preview']=raw[:80].decode(errors='replace')
    except urllib.error.HTTPError as e:record.update({'status':e.code})
    except Exception as e:record.update({'error':str(e)[:200]})
    results.append(record)
    print(str(code),record.get('status'),list(record.get('json',{}))[:15] if isinstance(record.get('json'),dict) else record.get('error'),flush=True)
    time.sleep(1.2)
(root/'discovered.json').write_text(json.dumps(results,indent=2,ensure_ascii=False),encoding='utf8')
lines=['# RUIOS OTA public indexes, model codes 8000–8100 excluding 8045–8070','',
       'Only publicly accessible, predictable OTA metadata JSON; one GET per candidate (1.1s apart), no firmware files downloaded.',
       'A matching OTA family/model number does not prove hardware compatibility.',
       '',
       '| ID | HTTP | OTA version(s) | Preview |','|---|---|---|---|']
for r in results:
    data=r.get('json')
    txt=json.dumps(data,ensure_ascii=False) if data is not None else ''
    versions=sorted(set(re.findall(r'RUIOS[.][A-Za-z0-9_.-]{2,100}',txt)))
    safe=', '.join(versions[:8])
    lines.append('| '+str(r['code'])+' | '+str(r.get('status','error'))+
       ' | '+(safe or '-')+' | '+txt[:220].replace('|','/')+' |')
lines+=['','## Full fetched metadata','']
for r in results:
    if 'json' in r:lines+=['### '+str(r['code']),'','~~~json',json.dumps(r['json'],ensure_ascii=False,indent=2),'~~~','']
(root/'README.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
