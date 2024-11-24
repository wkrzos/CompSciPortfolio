using System;

class Program
{
    static void Main()
    {
        // Call CountMyTypes with a variety of elements
        var counts = CountMyTypes(2, 4.5, "Hello", 10, 12.34, "World!", 5, 6, 'A', 7.89, "ABCDE");
        Console.WriteLine($"Even integers: {counts.evenInts}");
        Console.WriteLine($"Positive doubles: {counts.positiveDoubles}");
        Console.WriteLine($"Strings with 5+ characters: {counts.longStrings}");
        Console.WriteLine($"Other types: {counts.otherTypes}");
    }

    static (int evenInts, int positiveDoubles, int longStrings, int otherTypes) CountMyTypes(params object[] elements)
    {
        int evenInts = 0, positiveDoubles = 0, longStrings = 0, otherTypes = 0;

        // Iterate through each element
        foreach (var element in elements)
        {
            switch (element)
            {
                case int i when i % 2 == 0:
                    evenInts++;
                    break;
                case double d when d > 0:
                    positiveDoubles++;
                    break;
                case string s when s.Length >= 5:
                    longStrings++;
                    break;
                default:
                    otherTypes++;
                    break;
            }
        }

        // Return the counts as a tuple
        return (evenInts, positiveDoubles, longStrings, otherTypes);
    }
}
