package solution1;
public class ElfSphereBig extends Elf {

    public ElfSphereBig() {
        super("Kula");
    }

    @Override
    public void addBauble(Bauble bombka) {
        if (bombka instanceof BaubleSphereBig) {
            baublesCounter++;
            baubles.add(bombka);
            showMsg("Bombka dodana!");

            // Logika dla pełnego pudełka
            if (baublesCounter == SIZE_OF_BOX && numberOfBoxes > 0) {
                numberOfBoxes--;
                baublesCounter = 0;
                showMsg("Pudelko z kulami jest pełne! Elf rzucił je za siebie i wziął nowe!");
            }
            if(numberOfBoxes == 0) {
                isElfDone = true;
                showMsg("Elf nie ma już pudełek!");
            }
         } else {
            showMsg("Jasny gwint! Bombka nie pasuje do pudełka!");
        }
    }

    @Override
    public boolean doesBaubleFit(Bauble bombka) {
        return bombka instanceof BaubleSphereBig;
    }

    @Override
    public String toString(){
        return("ElfSphereBig = { rodzajPudelka = " + boxType + ", liczbaBombek = " + baublesCounter + " }");
    }
}

// Analogicznie dla ElfSopelka i ElfGrzybka
