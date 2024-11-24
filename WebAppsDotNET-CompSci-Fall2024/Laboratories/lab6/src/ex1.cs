using System;

class Program
{
    static void Main()
    {
        var person = ("John", "Doe", 30, 5000.50);

        PrintPersonInfo(person);

        Console.WriteLine($"Name: {person.Item1}, Surname: {person.Item2}, Age: {person.Item3}, Salary: {person.Item4}");
        Console.WriteLine(string.Join(", ", person));
        Console.WriteLine($"Tuple contents: {person}");
    }

    static void PrintPersonInfo((string FirstName, string LastName, int Age, double Salary) person)
    {
        Console.WriteLine($"Name: {person.FirstName}, Surname: {person.LastName}, Age: {person.Age}, Salary: {person.Salary}");
    }
}
