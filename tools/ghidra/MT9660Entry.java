// @category ReverseEngineering
import ghidra.app.script.GhidraScript;
import ghidra.program.model.address.Address;
import ghidra.program.model.listing.Function;

public class MT9660Entry extends GhidraScript {
    @Override protected void run() throws Exception {
        Address entry = toAddr(0x0);
        println("MT9660_ENTRY=" + entry);
        try { disassemble(entry); println("MT9660_DISASSEMBLE_OK"); }
        catch (Exception e) { println("MT9660_DISASSEMBLE_ERROR " + e.toString()); }
        try {
            Function f = getFunctionAt(entry);
            if (f == null) f = createFunction(entry, "mboot_entry_0x0");
            println("MT9660_ENTRY_FUNCTION=" + f);
        } catch (Exception e) { println("MT9660_ENTRY_FUNCTION_ERROR " + e.toString()); }
        try { currentProgram.getSymbolTable().addExternalEntryPoint(entry); }
        catch (Exception e) { println("MT9660_ENTRY_SYMBOL_ERROR " + e.toString()); }
    }
}
