using System;

class Program
{
    static void Main()
    {
        // Example calls to the DrawCard method
        DrawCard("Ryszard", "Rys", 'X', 2, 20);
        DrawCard("John Doe", "Developer", '#', 3, 25);
    }

    static void DrawCard(string line1, string line2, char borderChar = '*', int borderWidth = 2, int minWidth = 20)
    {
        // Calculate the total width of the card
        int cardWidth = Math.Max(minWidth, Math.Max(line1.Length, line2.Length) + borderWidth * 2 + 4);
        string borderLine = new string(borderChar, cardWidth);

        // Print the top border
        Console.WriteLine(borderLine);
        Console.WriteLine(borderLine);

        // Print the first line, centered with spaces
        Console.WriteLine(new string(borderChar, borderWidth) +
                          line1.PadLeft((cardWidth - borderWidth * 2 + line1.Length) / 2).PadRight(cardWidth - borderWidth * 2) +
                          new string(borderChar, borderWidth));

        // Print the second line, centered with spaces
        Console.WriteLine(new string(borderChar, borderWidth) +
                          line2.PadLeft((cardWidth - borderWidth * 2 + line2.Length) / 2).PadRight(cardWidth - borderWidth * 2) +
                          new string(borderChar, borderWidth));

        // Print the bottom border
        Console.WriteLine(borderLine);
        Console.WriteLine(borderLine);
    }
}
