#!/usr/bin/env python3
"""Inventory machine-code sections and function-level hashes of native ELF files.
Run on unmodified, SHA-verified images. No ELF binaries/source or machine code published.
"""
import argparse,hashlib,json,re
from pathlib import Path
from elftools.elf.elffile import ELFFile
from capstone import Cs, CS_ARCH_ARM, CS_MODE_ARM, CS_MODE_THUMB, CS_MODE_LITTLE_ENDIAN

p=argparse.ArgumentParser()
p.add_argument("--root",type=Path,required=True)
p.add_argument("--variant",required=True)
p.add_argument("--out",type=Path,required=True)
a=p.parse_args();a.out.parent.mkdir(exist_ok=True,parents=True)
hashstr=lambda x:hashlib.sha256(x).hexdigest()
interesting=re.compile(r"(?:trd|motor|tof|focus|keystone|source|hdmi|cec|audio|i2c|mtk|medi(a|ate)k|camera|display|tv|factory|projector|boot|pmu)",re.I)
relevant_sections=(".text",".rodata",".data",".data.rel.ro",".got",".plt",".bss",".rela.dyn",".rel.dyn",".dynstr",".modinfo")
results={"variant":a.variant,"root_style":"Android extracted directories named system_a/system_ext_a/vendor_a/product_a",
         "apps":"excluded","files":{},"failed":[]}
for item in sorted(a.root.iterdir()):
    if not item.is_dir() or not item.name.endswith("_a"):continue
    part=item.name
    candidates=(x for x in item.rglob("*") if x.is_file() and
                (x.suffix==".so" or x.name.endswith("-service") or x.name.endswith(".ko")
                 or ("/bin/" in x.as_posix() and interesting.search(x.name))))
    for f in candidates:
        # Relative root path is stable on stock and OTA after partition-name alignment.
        rel=f.relative_to(a.root).as_posix()
        try:
            with f.open("rb") as bf:
                if bf.read(4)!=b"\x7fELF":continue
                bf.seek(0)
                elf=ELFFile(bf)
                sections={}
                for s in elf.iter_sections():
                    if s.name in relevant_sections:
                        if s['sh_type']=="SHT_NOBITS":
                            secsha=None
                        else:
                            secsha=hashstr(s.data())
                        sections[s.name]={"bytes":int(s['sh_size']),"sha256":secsha}
                dynamics=[]
                sec=elf.get_section_by_name(".dynamic")
                if sec is not None:
                    for tag in sec.iter_tags():
                        if tag.entry.d_tag=="DT_NEEDED":dynamics.append(tag.needed)
                syms={}
                dynsym=elf.get_section_by_name(".dynsym")
                if dynsym is None and re.search(r"(wlan_mt|dtv_driver|mali_kbase|kdrv_ldm)",rel,re.I):
                    dynsym=elf.get_section_by_name(".symtab")
                text=elf.get_section_by_name(".text")
                if dynsym is not None and text is not None and interesting.search(rel):
                    code=text.data()
                    textbase=int(text['sh_addr'])
                    for sym in dynsym.iter_symbols():
                        if sym['st_info']['type']!="STT_FUNC" or not sym.name:continue
                        start=int(sym['st_value'])-textbase
                        size=int(sym['st_size'])
                        # ARM thumb symbols can carry address LSB. Derive equivalent code region.
                        if start&1:start-=1
                        if size<=0 or start<0 or start+size>len(code):continue
                        
                        metadata={"bytes":size,"sha256":hashstr(code[start:start+size])}
                        if rel.endswith("/libmediatek_tv_basic.so") and elf['e_machine']=="EM_ARM":
                            try:
                                mode=(CS_MODE_THUMB if int(sym['st_value'])&1 else CS_MODE_ARM)|CS_MODE_LITTLE_ENDIAN
                                dis=Cs(CS_ARCH_ARM,mode)
                                opcodes=[ins.mnemonic for ins in dis.disasm(code[start:start+size],int(sym['st_value'])&~1)]
                                if opcodes:
                                    metadata["disasm_instructions"]=len(opcodes)
                                    metadata["opcode_only_sha256"]=hashstr(" ".join(opcodes).encode())
                                    metadata["branch_mnemonics"]=sum(1 for mnemonic in opcodes if mnemonic.startswith(("b","cb","tb")) or mnemonic in ("bl","blx"))
                            except Exception as err:
                                metadata["disasm_error"]=type(err).__name__
                        syms[sym.name[:250]]=metadata
                # This is a binary hash, distinct from .text equality.
                bf.seek(0)
                digest=hashlib.sha256()
                for chunk in iter(lambda:bf.read(8*1024*1024),b""):digest.update(chunk)
                modinfo=elf.get_section_by_name(".modinfo")
                modentries=[]
                if modinfo is not None:
                    for item in modinfo.data().split(bytes([0])):
                        val=item.decode(errors="replace")
                        if val.startswith(("vermagic=","srcversion=","version=","depends=")):
                            modentries.append(val[:180])
                results["files"][rel]={"sha256":digest.hexdigest(),"bytes":f.stat().st_size,"modinfo":sorted(set(modentries)),
                     "class":elf.elfclass,"machine":elf['e_machine'],"type":str(elf['e_type']),
                     "build_id":next((s.data().hex()[:130] for s in elf.iter_sections() if s.name==".note.gnu.build-id"),None),
                     "sections":sections,"deps":sorted(set(dynamics)),"functions":syms}
        except Exception as e:
            results["failed"].append({"file":rel,"type":type(e).__name__,"message":str(e)[:150]})
    print("PARTITION",part,"ELF total",len(results["files"]),"errors",len(results["failed"]),flush=True)
a.out.write_text(json.dumps(results,ensure_ascii=False,indent=2)+"\n")
print("DONE",a.variant,"ELF",len(results["files"]),"errors",len(results["failed"]),flush=True)
