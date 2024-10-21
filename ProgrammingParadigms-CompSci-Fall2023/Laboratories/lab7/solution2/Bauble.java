package solution2;

public class Bauble {
    private BaubleType type;
    private String colour;
    private String pattern;
    private boolean isBroken;

    public Bauble(BaubleType type, String colour, String pattern){
        this.type = type;
        this.colour = colour;
        this.pattern = pattern;
        this.isBroken = false;
    }

    public BaubleType getType() {
        return type;
    }

    public void setType(BaubleType type) {
        this.type = type;
    }

    public String getColour() {
        return colour;
    }

    public void setColour(String colour) {
        this.colour = colour;
    }

    public String getPattern() {
        return pattern;
    }

    public void setPattern(String pattern) {
        this.pattern = pattern;
    }

    public boolean getIsBroken() {
        return isBroken;
    }

    public void setIsBroken(boolean isBroken) {
        this.isBroken = isBroken;
    }

    @Override
    public String toString() {
        return "Bombka{" +
        "rodzaj=" + type +
        ", kolor='" + colour + '\'' +
        ", wzor='" + pattern + '\'' +
        ", isBroken=" + isBroken +
        '}';
    }
}
