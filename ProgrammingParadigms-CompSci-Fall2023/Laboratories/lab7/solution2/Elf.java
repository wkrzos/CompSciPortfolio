package solution2;

import java.util.ArrayList;
import java.util.List;

public class Elf {
    private final int SIZE_OF_BOXES = 2;
    private int numberOfBoxes = 2;

    private BaubleType type;
    private int baubleCount;
    private List<Bauble> baubles;
    private boolean isBoxFull = false;

    public Elf(BaubleType type, int baubleCount) {
        this.type = type;
        this.baubleCount = baubleCount;
        this.baubles = new ArrayList<>();
    }

    public void addBaubles(Bauble bauble) {
        if (numberOfBoxes == 0) {
            System.out.println("No more boxes available!");
            return;
        }

        if (!czyPasuje(bauble)) {
            System.out.println("Wrong bauble type: " + bauble);
            return;
        }

        baubles.add(bauble);
        baubleCount++;

        System.out.println("Bauble added: " + bauble.toString());

        if (baubleCount == SIZE_OF_BOXES) {
            baubleCount = 0;
            numberOfBoxes--;
            isBoxFull = false; // Reset box status
            System.out.println("Box changed. Remaining boxes: " + numberOfBoxes);
            if (numberOfBoxes == 0) {
                System.out.println("No more boxes left!");
            }
        }
    }

    public String toStringBaublesArrayString() {
        StringBuilder stringBuilder = new StringBuilder();
        for(Bauble bauble : baubles) {
            stringBuilder.append(bauble.toString());
            stringBuilder.append("\n");
        }
        return stringBuilder.toString();
    }

    public boolean czyPasuje(Bauble bauble) {
        if(type == BaubleType.SPHERE_BIG_AND_SMALL) {
            return bauble.getType() == BaubleType.SPHERE_BIG || bauble.getType() == BaubleType.SPHERE_SMALL;
        } else {
            return bauble.getType() == type;
        }
    }

    @Override
    public String toString() {
        return "Elf{" +
                "type=" + type +
                ", baubleCount=" + baubleCount +
                ", baubles=" + "<below>" +
                ", isBoxFull=" + isBoxFull +
                '}';
    }

    public BaubleType getType() {
        return type;
    }

    public void setType(BaubleType type) {
        this.type = type;
    }

    public int getBaubleCount() {
        return baubleCount;
    }

    public void setBaubleCount(int baubleCount) {
        this.baubleCount = baubleCount;
    }

    public int getSIZE_OF_BOXES() {
        return SIZE_OF_BOXES;
    }

    public List<Bauble> getBaubles() {
        return baubles;
    }

    public void setBaubles(List<Bauble> baubles) {
        this.baubles = baubles;
    }

    public boolean isBoxFull() {
        return isBoxFull;
    }

    public void setBoxFull(boolean isBoxFull) {
        this.isBoxFull = isBoxFull;
    }

    public int getNumberOfBoxes() {
        return numberOfBoxes;
    }

    public void setNumberOfBoxes(int numberOfBoxes) {
        this.numberOfBoxes = numberOfBoxes;
    }
}
