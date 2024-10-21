package solution1;
public class BaubleSphereBig extends Bauble {
    private int rozmiar;

    public BaubleSphereBig(String kolor, String wzor, int rozmiar) {
        super(kolor, wzor);
        this.rozmiar = rozmiar;
    }

    @Override
    public String toString() {
        return "Big Sphere{" + super.toString() + ", Rozmiar=" + rozmiar + "}" + " isBroken=" + isBroken + "}";
    }
}