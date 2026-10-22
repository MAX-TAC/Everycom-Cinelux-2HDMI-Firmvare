# @category ReverseEngineering
# AARCH64 MT9660 U-Boot raw image, file-offset mapped at 0.
# Header is 0x400 bytes. Entry at file offset 0x400.
from ghidra.program.model.symbol import SourceType
entry=toAddr(0x400)
print("BOOT_ENTRY_ENTRYPOINT "+str(entry))
try:
    disassemble(entry)
    print("BOOT_ENTRY_DISASSEMBLED")
except Exception as e:
    print("BOOT_ENTRY_DISASSEMBLY_ERROR "+str(e))
try:
    f=getFunctionAt(entry)
    if f is None:
        f=createFunction(entry,"mboot_entry_0x400")
    print("BOOT_ENTRY_FUNCTION "+str(f))
except Exception as e:
    print("BOOT_ENTRY_FUNCTION_ERROR "+str(e))
try:
    currentProgram.getSymbolTable().addExternalEntryPoint(entry)
except Exception as e:
    print("EXTERNAL_ENTRY_ERR "+str(e))
