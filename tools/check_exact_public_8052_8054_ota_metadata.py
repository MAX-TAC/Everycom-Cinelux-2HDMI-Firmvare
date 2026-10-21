#!/usr/bin/env python3
"""Fetch exactly two known public RUIOS OTA JSON indexes; do not download firmware.
Do not infer installed version or existence of full image from JSON alone.
"""
import hashlib,json,urllib.request,urllib.error,re,datetime
from pathlib import Path
OUT=Path("analysis/Global_Firmware_Map_20261021")
OUT.mkdir(exist_ok=True,parents=True)
records=[]
for model in (8052,8054):
 url="https://www.szrjyun.com/ota/android/mt9660/"+str(model)+"/"+str(model)+"_ota.json"
 row={"model":model,"index":url}
 try:
  req=urllib.request.Request(url,headers={"User-Agent":"CineLuxFirmwareAudit/1.0 (metadata-only; contact GitHub MAX-TAC)"})
  with urllib.request.urlopen(req,timeout=35) as r:
   buf=r.read(262145)
   row["http"]=r.status;row["bytes"]=len(buf);row["sha256"]=hashlib.sha256(buf).hexdigest()
   if len(buf)>262144:row["error"]="Response too large, skipped";records.append(row);continue
   js=json.loads(buf)
   row["json_type"]=type(js).__name__
   s=json.dumps(js,ensure_ascii=False)
   row["version_mentions"]=sorted(set(re.findall(r"RUIOS[.][A-Za-z0-9_.-]{4,60}",s)))[:20]
   row["firmware_zip_mentions"]=sorted(set(re.findall(r"RJMT9660_firmware_805[24][.]zip",s)))[:15]
   # Do not expose uncontrolled URLs or credentials and avoid treating JSON as signed truth.
   row["top_keys"]=sorted(js.keys()) if isinstance(js,dict) else []
 except Exception as e:row["error"]=type(e).__name__+": "+str(e)[:160]
 records.append(row)
 print("CHECK",model,row,flush=True)
(OUT/"PUBLIC_8052_8054_OTA_METADATA.json").write_text(json.dumps(records,indent=2,ensure_ascii=False)+"\n")
lines=["# Проверка публичных индексов OTA RUIOS 8052 и 8054","",
"Только 2 публичных адреса JSON, без загрузки ZIP/PKG и без обращения к неизвестным ID.",
"Даже существующий индекс и строка RUIOS не доказывают, что полноценный образ доступен или соответствует проектору.",
"",
"| ID | HTTP | Версии, найденные в ответе | Имя архива |",
"|---|---|---|---|"]
for d in records:
 lines.append("| "+str(d["model"])+" | "+str(d.get("http","недоступно"))+
              " | "+", ".join(d.get("version_mentions",[]))+
              " | "+", ".join(d.get("firmware_zip_mentions",[]))+" |")
 lines.append("")
 if "error" in d:lines.append("- "+str(d["model"])+": "+d["error"])
lines+=["","## Ограничения","",
"Это сетевой срез на момент выполнения GitHub Actions; производитель может менять файл. Наличие RUIOS.8054.1.0.4 в JSON, если оно будет найдено, не равнозначно наличию проверенного образа 8054.1.0.4 для бинарного сравнения.",
"Проверенные локальные firmware artifacts пока: октябрьская 8052 OTA 1.0.4 и сентябрьская 8054 factory 1.0.1.",
""]
(OUT/"PUBLIC_8052_8054_OTA_METADATA_RU.md").write_text("\n".join(lines)+"\n")
