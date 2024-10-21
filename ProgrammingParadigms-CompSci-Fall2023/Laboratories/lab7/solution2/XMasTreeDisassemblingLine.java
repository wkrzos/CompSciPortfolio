package solution2;

import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

public class XMasTreeDisassemblingLine {

    private List<Elf> elves;
    private List<Bauble> baubles;

    public XMasTreeDisassemblingLine() {
        elves = new ArrayList<>();
        baubles = new ArrayList<>();

        // Initialize Elves with different bauble types
        elves.add(new Elf(BaubleType.SPHERE_BIG_AND_SMALL, 0));
        elves.add(new Elf(BaubleType.SPHERE_SMALL, 0));
        elves.add(new Elf(BaubleType.ICECYCLE, 0));
        elves.add(new Elf(BaubleType.MUSHROOM, 0));
        // Add more elves for different bauble types if needed
    }

    public void addBauble(Bauble bauble) {
        baubles.add(bauble);
    }

    //Was implemented with an array, caused ConcurrentModificationException
    public void startDisassembling() {
        Iterator<Bauble> iterator = baubles.iterator();
        while (iterator.hasNext()) {
            Bauble bauble = iterator.next();
            boolean baubleHandled = false;
            for (Elf elf : elves) {
                if (elf.czyPasuje(bauble) && !elf.isBoxFull()) {
                    elf.addBaubles(bauble);
                    iterator.remove(); // This safely removes the bauble from the list
                    baubleHandled = true;
                    break;
                }
            }
            if (!baubleHandled) {
                bauble.setIsBroken(true);
                System.out.println("Bauble dropped on the floor: " + bauble);
            }
        }
    }
    
    public void printBaubles() {
        for (Bauble bauble : baubles) {
            System.out.println(bauble.toString());
        }
    }

    public void printElves() {
        for (Elf elf : elves) {
            System.out.println("==================================");
            System.out.println(elf.toString());
            System.out.println(elf.toStringBaublesArrayString());
        }
    }

    public static void main(String[] args) {
        XMasTreeDisassemblingLine disassemblingLine = new XMasTreeDisassemblingLine();

        // Add some baubles to the disassembling line
        disassemblingLine.addBauble(new Bauble(BaubleType.SPHERE_BIG, "Red", "Glittery"));
        disassemblingLine.addBauble(new Bauble(BaubleType.SPHERE_BIG, "Red", "Glittery"));
        disassemblingLine.addBauble(new Bauble(BaubleType.SPHERE_BIG, "Red", "Glittery"));
        disassemblingLine.addBauble(new Bauble(BaubleType.SPHERE_SMALL, "Red", "Glittery"));
        disassemblingLine.addBauble(new Bauble(BaubleType.ICECYCLE, "Blue", "Matte"));
        disassemblingLine.addBauble(new Bauble(BaubleType.SPHERE_SMALL, "Red", "Glittery"));
        disassemblingLine.addBauble(new Bauble(BaubleType.SPHERE_SMALL, "Red", "Glittery"));
        disassemblingLine.addBauble(new Bauble(BaubleType.MUSHROOM, "Green", "Shiny"));
        // Add more baubles as needed

        System.out.println("Starting disassembling line...");

        disassemblingLine.startDisassembling();

        System.out.println("Disassembling line finished." + System.lineSeparator());
        System.out.println("Printing baubles and elves..." + System.lineSeparator());
        
        disassemblingLine.printElves();
        disassemblingLine.printBaubles();
    }
}
