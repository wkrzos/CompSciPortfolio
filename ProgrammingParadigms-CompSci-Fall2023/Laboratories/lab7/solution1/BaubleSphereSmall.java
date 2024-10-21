package solution1;
public class BaubleSphereSmall extends Bauble {
    private int rozmiar;

    public BaubleSphereSmall(String kolor, String wzor, int rozmiar) {
        super(kolor, wzor);
        this.rozmiar = rozmiar;
    }

    @Override
    public String toString() {
        return "Small Sphere{" + super.toString() + ", Rozmiar=" + rozmiar + "}" + " isBroken=" + isBroken + "}";
    }
}