package solution1;
import java.util.ArrayList;
import java.util.List;

public abstract class Elf {
    public final int SIZE_OF_BOX = 2;
    protected int numberOfBoxes = 2;

    protected String boxType;
    protected int baublesCounter;
    protected List<Bauble> baubles;
    protected boolean isElfDone = false;

    public Elf(String boxType) {
        this.boxType = boxType;
        this.baublesCounter = 0;
        this.baubles = new ArrayList<>();
    }

    public abstract void addBauble(Bauble bombka);

    public abstract boolean doesBaubleFit(Bauble bombka);

    public boolean isBoxFull() {return isElfDone; };

    protected void showMsg(String komunikat) {
        System.out.println(komunikat);
    }

    public String toStringBaublesArrayString() {
        StringBuilder stringBuilder = new StringBuilder();
        for(Bauble bauble : baubles) {
            stringBuilder.append(bauble.toString());
            stringBuilder.append("\n");
        }
        return stringBuilder.toString();
    }

    @Override
    public String toString(){
        return("Elf = { rodzajPudelka = " + boxType + ", liczbaBombek = " + baublesCounter + " }");
    }

    public int getSIZE_OF_BOX() {
        return SIZE_OF_BOX;
    }

    public String getBoxType() {
        return boxType;
    }

    public void setBoxType(String rodzajPudelka) {
        this.boxType = rodzajPudelka;
    }

    public int getBaublesCounter() {
        return baublesCounter;
    }

    public void setBaublesCounter(int liczbaBombek) {
        this.baublesCounter = liczbaBombek;
    }

    public List<Bauble> getBaubles() {
        return baubles;
    }

    public void setBaubles(List<Bauble> baubles) {
        this.baubles = baubles;
    }

    public boolean isElfDone() {
        return isElfDone;
    }

    public void setElfDone(boolean isBoxFull) {
        this.isElfDone = isBoxFull;
    }
}
