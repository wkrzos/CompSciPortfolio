package solution1;
public class BaubleMushroom extends Bauble {
    private int rozmiar;

    public BaubleMushroom(String kolor, String wzor, int rozmiar) {
        super(kolor, wzor);
        this.rozmiar = rozmiar;
    }

    @Override
    public String toString() {
        return "Muschroom Sphere{" + super.toString() + ", Rozmiar=" + rozmiar + "}" + " isBroken=" + isBroken + "}";
    }
}