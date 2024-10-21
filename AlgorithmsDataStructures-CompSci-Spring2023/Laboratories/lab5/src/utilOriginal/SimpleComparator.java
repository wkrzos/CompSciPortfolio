package utilOriginal;

import java.util.Comparator;

import main.Car;

public class SimpleComparator implements Comparator<Car> {
    private final String fieldName;
    
    public SimpleComparator(String fieldName) {
        this.fieldName = fieldName;
    }
    
    @Override
    public int compare(Car p1, Car p2) {
        switch (fieldName) {
            case "brand":
                return p1.getBrand().compareTo(p2.getBrand());
            case "colour":
                return p1.getColour().compareTo(p2.getColour());
            case "yearOfProduction":
                return Integer.compare(p1.getYearOfProduction(), p2.getYearOfProduction());
            default:
                throw new IllegalArgumentException("Invalid field name: " + fieldName);
        }
    }
}
