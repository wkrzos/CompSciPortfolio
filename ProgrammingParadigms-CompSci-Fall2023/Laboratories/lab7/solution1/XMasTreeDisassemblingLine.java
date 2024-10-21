package solution1;

import java.util.ArrayList;
import java.util.List;
import java.util.Iterator;

public class XMasTreeDisassemblingLine {
    public List<Elf> elves;
    public List<Bauble> baubles;

    public XMasTreeDisassemblingLine(){
        elves = new ArrayList<>();
        baubles = new ArrayList<>();

        elves.add(new ElfSphereBig());
        elves.add(new ElfSphereBigAndSmall());
        elves.add(new ElfSphereSmall());
    }

    public void addBauble(Bauble bauble){
        baubles.add(bauble);
    }

    public void startDisassembling() {
        Iterator<Bauble> iterator = baubles.iterator();
        while (iterator.hasNext()) {
            Bauble bauble = iterator.next();
            boolean isBaubleInBox = false;

            for (Elf elf : elves) {
                if (elf.doesBaubleFit(bauble) && !elf.isBoxFull()) {
                    System.out.println("Pasuje i jest następne pudełko!");
                    elf.addBauble(bauble);
                    isBaubleInBox = true;        
                    iterator.remove(); // Safely remove the bauble
                    break;
                }
            }

            if (!isBaubleInBox) {
                bauble.setBroken(true);
                System.out.println("Whoops! The bauble has been shattered: " + bauble + ". Either the boxes are full, or no elf wnated it :c");
            }
        }
    }

    public void printBaubles(){
        for(Bauble bauble : baubles){
            System.out.println(bauble.toString());
        }
    }

    public void printElves(){
        for(Elf elf : elves){
            System.out.println("==================================");
            System.out.println(elf.toString());
            System.out.println(elf.toStringBaublesArrayString());
        }
    }

    public static void main(String[] args){
        XMasTreeDisassemblingLine line = new XMasTreeDisassemblingLine();

        line.addBauble(new BaubleIcecycle("red", "striped", 1));
        line.addBauble(new BaubleIcecycle("red", "striped", 1));
        line.addBauble(new BaubleIcecycle("red", "striped", 1));
        line.addBauble(new BaubleIcecycle("red", "striped", 1));
        line.addBauble(new BaubleIcecycle("red", "striped", 1));
        line.addBauble(new BaubleIcecycle("red", "striped", 1));
        line.addBauble(new BaubleSphereBig("red", "plain", 2));
        line.addBauble(new BaubleSphereBig("red", "plain", 2));
        line.addBauble(new BaubleSphereBig("red", "plain", 2));
        line.addBauble(new BaubleSphereBig("red", "plain", 2));
        line.addBauble(new BaubleSphereBig("red", "plain", 2));
        line.addBauble(new BaubleSphereBig("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
        line.addBauble(new BaubleSphereSmall("red", "plain", 2));
    
        System.out.print("Starting disassembling line...");

        line.startDisassembling();

        System.out.println("Disassembling line finished." + System.lineSeparator());
        System.out.println("Printing baubles and elves..." + System.lineSeparator());

        line.printElves();
        
        System.out.println("==================================");

        line.printBaubles();
    }
}
