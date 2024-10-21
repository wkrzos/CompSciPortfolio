package solution1;
public class BaubleIcecycle extends Bauble {
    private int rozmiar;

    public BaubleIcecycle(String kolor, String wzor, int rozmiar) {
        super(kolor, wzor);
        this.rozmiar = rozmiar;
    }

    @Override
    public String toString() {
        return "Icecycle Sphere{" + super.toString() + ", Rozmiar=" + rozmiar + "}" + " isBroken=" + isBroken + "}";
    }
}