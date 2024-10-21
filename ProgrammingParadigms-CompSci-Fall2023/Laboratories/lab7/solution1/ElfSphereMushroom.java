package solution1;
public class ElfSphereMushroom extends Elf {

    public ElfSphereMushroom() {
        super("Kula");
    }

    @Override
    public void addBauble(Bauble bombka) {
        if (bombka instanceof BaubleMushroom) {
            baublesCounter++;
            baubles.add(bombka);
            showMsg("Bombka dodana!");
            // Logika dla pełnego pudełka
            if (baublesCounter == SIZE_OF_BOX && numberOfBoxes > 0) {
                numberOfBoxes--;
                baublesCounter = 0;
                showMsg("Pudelko z kulami jest pełne! Elf rzucił je za siebie i wziął nowe!");
            } else if (baublesCounter == SIZE_OF_BOX && numberOfBoxes == 0) {
                isElfDone = true;
                showMsg("Elf nie ma już pudełek!");
            }
        } else {
            showMsg("Bombka nie pasuje do pudełka!");
        }
    }

    @Override
    public boolean doesBaubleFit(Bauble bombka) {
        return bombka instanceof BaubleMushroom;
    }

    @Override
    public String toString(){
        return("ElfMushroom = { rodzajPudelka = " + boxType + ", liczbaBombek = " + baublesCounter + " }");
    }
}

// Analogicznie dla ElfSopelka i ElfGrzybka
