package solution1;
public abstract class Bauble {
    protected String kolor;
    protected String wzor;
    protected boolean isBroken;

    public Bauble(String kolor, String wzor) {
        this.kolor = kolor;
        this.wzor = wzor;
        this.isBroken = false;
    }

    @Override
    public String toString() {
        return "Bombka{Kolor='" + kolor + "', Wzór='" + wzor + "'} isBroken=" + isBroken + "}";
    }

    public String getKolor() {
        return kolor;
    }

    public void setKolor(String kolor) {
        this.kolor = kolor;
    }

    public String getWzor() {
        return wzor;
    }

    public void setWzor(String wzor) {
        this.wzor = wzor;
    }

    public boolean isBroken() {
        return isBroken;
    }

    public void setBroken(boolean isBroken) {
        this.isBroken = isBroken;
    }
}
