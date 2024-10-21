package main;

import java.lang.Comparable;
import java.util.Comparator;

public class Car implements Comparable<Car> {

    String brand;
    String colour;
    int yearOfProduction;

    public Car(String brand, String colour, int yearOfProduction) {
        this.brand = brand;
        this.colour = colour;
        this.yearOfProduction = yearOfProduction;
    }

    public String getBrand() {
        return brand;
    }

    public void setBrand(String brand) {
        this.brand = brand;
    }

    public String getColour() {
        return colour;
    }

    public void setColour(String colour) {
        this.colour = colour;
    }

    public int getYearOfProduction() {
        return yearOfProduction;
    }

    public void setYearOfProduction(int yearOfProduction) {
        this.yearOfProduction = yearOfProduction;
    }

    @Override
    public String toString() {
        return brand + " " + colour + " " + yearOfProduction;
    }

    /*
     * @Override
     * public int compareTo(Car o) {
     * return brand.compareTo(o.brand);
     * }
     */

    @Override
    public int compareTo(Car o) {
        return Comparator.comparing(Car::getBrand)
                .thenComparing(Car::getColour)
                .thenComparingInt(Car::getYearOfProduction)
                .compare(this, o);
    }
}