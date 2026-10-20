#!/usr/bin/env python3
"""Reconstruct vendor firmware partitions from a previously DECRYPTED MStar/MTK REE body.
READ-ONLY on the source. Do not run binaries. Do not publish calibration/DRM/serial partitions.
Usage: python3 tools/reconstruct_cinelux.py /tmp/cinelux-plain-body.bin /tmp/cinelux-parts
Requires: lz4 CLI, verified decrypted upgrade_script.txt in the repository.
"""
import sys,struct,json,re,subprocess,shutil,hashlib
from pathlib import Path
SRC=Path(sys.argv[1])
BASE=Path(sys.argv[2])
BASE.mkdir(parents=True,exist_ok=True)
TEMP=BASE/"tmp"
TEMP.mkdir(exist_ok=True)
SCRIPT=Path("analysis/Original_Firmware/decrypted/upgrade_script.txt").read_text(encoding="utf8")
OUT=Path("analysis/Original_Firmware/reconstructed")
OUT.mkdir(parents=True,exist_ok=True)
MAGIC=0xed26ff3a
data={"source":{"path":str(SRC),"size":SRC.stat().st_size},
      "segments":[],"super":{},"partitions":{},"errors":[]}
def cmd(args):
    r=subprocess.run(args,capture_output=True,text=True,errors="replace",timeout=150)
    return r.returncode,r.stdout[-1500:],r.stderr[-1500:]
def copy_n(src,dst,count):
    left=count
    while left:
        b=src.read(min(left,4*1024*1024))
        if not b:raise EOFError("Unexpected end of stream")
        dst.write(b);left-=len(b)
def fmt(path):
    x=cmd(["file","-b",str(path)])
    return x[1].strip()[:220]
def sha(path):
    h=hashlib.sha256()
    with path.open("rb") as f:
        for b in iter(lambda:f.read(4*1024*1024),b""):h.update(b)
    return h.hexdigest()
def unsparse(fragment, dest, logical_start):
    with fragment.open("rb") as src:
        hdr=src.read(28)
        if len(hdr)!=28:raise ValueError("Too short for Android sparse header")
        magic,major,minor,fh,cs,blk,total_blocks,total_chunks,checksum=struct.unpack("<IHHHHIIII",hdr)
        if magic!=MAGIC:
            raise ValueError("Not Android sparse: "+hdr[:28].hex(" "))
        if major!=1 or fh<28 or cs<12 or not (512<=blk<=65536):
            raise ValueError("Unexpected sparse header "+str((major,fh,cs,blk)))
        src.seek(fh)
        cursor=logical_start
        counts={}
        for index in range(total_chunks):
            chunk=src.read(cs)
            if len(chunk)!=cs:raise EOFError("Sparse chunk header short")
            kind,_res,nblocks,totalsz=struct.unpack("<HHII",chunk[:12])
            nbytes=blk*nblocks
            if kind==0xCAC1: # RAW
                if totalsz!=cs+nbytes:raise ValueError("RAW size mismatch")
                dest.seek(cursor)
                copy_n(src,dest,nbytes)
            elif kind==0xCAC2: # FILL
                if totalsz!=cs+4:raise ValueError("FILL mismatch")
                fill=src.read(4)
                if fill!=b"\0\0\0\0":
                    dest.seek(cursor)
                    buf=fill*min(nbytes//4,16384)
                    left=nbytes
                    while left:
                        to_write=min(left,len(buf))
                        dest.write(buf[:to_write])
                        left-=to_write
            elif kind==0xCAC3: # DONT CARE
                if totalsz!=cs:raise ValueError("DONTCARE mismatch")
            elif kind==0xCAC4: # CRC
                if totalsz!=cs+4:raise ValueError("CRC mismatch")
                src.read(4)
            else:raise ValueError("Unknown sparse chunk 0x%04X"%kind)
            if kind!=0xCAC4:cursor+=nbytes
            counts[hex(kind)]=counts.get(hex(kind),0)+1
        expanded=cursor-logical_start
        if expanded!=blk*total_blocks:raise ValueError("Sparse blocks mismatch %d/%d"%(expanded,blk*total_blocks))
        return {"expanded_bytes":expanded,"block_size":blk,"chunks":total_chunks,"kinds":counts}
lines=SCRIPT.splitlines()
seq=[]
for i,line in enumerate(lines):
    if not line.startswith("filepartload "):continue
    fields=line.split()
    if len(fields)<5:continue
    compressed_size=int(fields[3],16)
    file_offset=int(fields[4],16)
    following=[]
    for other in lines[i+1:]:
        if other.startswith("filepartload "):break
        following.append(other.strip())
    decompress=next((x for x in following if x.startswith("unlz4 ")),None)
    destinations=[]
    sparse=False
    for x in following:
        t=x.split()
        if len(t)>=5 and t[:2] in (["partition","write"],["partition","swrite"]):
            destinations.append(t[4]);sparse=sparse or t[1]=="swrite"
        elif x.startswith("partition write.boot"):
            destinations.append("emmc_boot")
    # Deduplicate
    destinations=list(dict.fromkeys(destinations))
    seq.append({"index":len(seq)+1,"offset":file_offset,
      "compressed_size":compressed_size,"unlz4":decompress is not None,
      "target":destinations,"sparse":sparse,
      "expected_uncompressed_size":int(decompress.split()[-1],16) if decompress else None})
print("Identified",len(seq),"segments",flush=True)
superpath=BASE/"super.img"
with SRC.open("rb") as inp,superpath.open("wb+") as superout:
    super_cursor=0
    for obj in seq:
        n=obj["index"]
        item=dict(obj)
        try:
            start=obj["offset"]-0x1000
            if start<0 or start+obj["compressed_size"]>SRC.stat().st_size:
                raise ValueError("Partition source offset outside decrypted body")
            compressed=TEMP/("segment%02d.lz4"%n)
            with compressed.open("wb") as dst:
                inp.seek(start)
                copy_n(inp,dst,obj["compressed_size"])
            if obj["unlz4"]:
                decoded=TEMP/("segment%02d.raw"%n)
                rc,stdout,stderr=cmd(["lz4","-d","-f","-q",str(compressed),str(decoded)])
                if rc:raise RuntimeError("LZ4 failed "+stderr)
            else:
                decoded=compressed
            item["decoded_bytes"]=decoded.stat().st_size
            item["format"]=fmt(decoded)
            exp=obj["expected_uncompressed_size"]
            # allow actual image to be smaller than memory buffer
            if exp and item["decoded_bytes"]>exp:
                item["warning"]="Decompressed file larger than expected buffer"
            if obj["sparse"] and "super" in obj["target"]:
                item["sparse_result"]=unsparse(decoded,superout,super_cursor)
                super_cursor+=item["sparse_result"]["expanded_bytes"]
            elif obj["target"]:
                target=obj["target"][0]
                # Keep one copy for A/B duplicated payloads, skip private data.
                saved=BASE/(target+".img")
                shutil.copyfile(decoded,saved)
                data["partitions"][target]={"size":saved.stat().st_size,"format":item["format"]}
            else:
                item["warning"]="No named destination in upgrade script"
        except Exception as e:
            item["error"]=str(e)
            data["errors"].append({"index":n,"error":str(e)})
        finally:
            data["segments"].append(item)
            for p in [TEMP/("segment%02d.lz4"%n),TEMP/("segment%02d.raw"%n)]:
                p.unlink(missing_ok=True)
        print("Segment",n,",".join(obj["target"]),item.get("format"),item.get("error","ok"),flush=True)
    superout.truncate(super_cursor)
data["super"]={"path":str(superpath),"size":superpath.stat().st_size,
               "format":fmt(superpath),"logical_bytes_written":super_cursor,
               "expected_gpt_super_size":int("84a00000",16)}
(OUT/"segments.json").write_text(json.dumps(data,indent=2,ensure_ascii=False),encoding="utf8")
lines=["# CineLux source firmware reconstructed partitions",
       "Only static file extraction; original update archive was not executed or flashed.",
       "",
       "## Super partition",
       "Size: "+str(data["super"]["size"])+" bytes",
       "Format: "+data["super"]["format"],
       "Expected GPT space: "+str(data["super"]["expected_gpt_super_size"]),
       "","## Segment table",
       "| # | Destination | Input bytes | Decompressed bytes | Format | Status |",
       "|---:|---|---:|---:|---|---|"]
for item in data["segments"]:
    lines.append("| "+str(item["index"])+" | "+", ".join(item["target"])+" | "+str(item["compressed_size"])+
      " | "+str(item.get("decoded_bytes","-"))+" | "+item.get("format","?").replace("|","/")[:70]+
      " | "+item.get("error","ok").replace("|","/")+" |")
lines+=["","## Other copied partitions (not published as binaries)"]
for name,item in data["partitions"].items():
    lines+=["- "+name+" : "+str(item["size"])+" bytes, "+item["format"]]
(OUT/"README.md").write_text("\n".join(lines)+"\n",encoding="utf8")
print("Completed, super:",data["super"],"errors:",data["errors"],flush=True)
