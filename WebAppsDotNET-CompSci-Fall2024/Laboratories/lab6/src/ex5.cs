using System;

class Program
{
    static void Main()
    {
        // Example calls to the DrawCard method
        DrawCard("Ryszard", "Rys", 'X', 5, 80, 30);
        //DrawCard("John Doe", "Developer", '#', 3, 25, 10);
    }

    static void DrawCard(string line1, string line2, char borderChar = '*', int borderWidth = 2, int minWidth = 20, int minHeight = 5)
    {
        int numberOfLines = 2; // TODO Refactor
        
        // Calculate the total width of the card
        int cardWidth = Math.Max(minWidth, Math.Max(line1.Length, line2.Length) + borderWidth * 2 + 4);
        string borderLine = new string(borderChar, cardWidth);

        // Calculate the total height of the card
        int cardHeight = Math.Max(minHeight, 4);

        int topPadding = (cardHeight - borderWidth * 2 - numberOfLines) / 2;
        int bottomPadding = topPadding;

        // Print the top border
        for(int i = 0; i < borderWidth; i++)
        {
            Console.WriteLine(borderLine);
        }

        // Print the top padding
        for(int i = 0; i < topPadding; i++)
        {
            Console.WriteLine(new string(borderChar, borderWidth) + new string(' ', cardWidth - borderWidth * 2) + new string(borderChar, borderWidth));
        }

        // Print the first line, centered with spaces
        Console.WriteLine(new string(borderChar, borderWidth) +
                          line1.PadLeft((cardWidth - borderWidth * 2 + line1.Length) / 2).PadRight(cardWidth - borderWidth * 2) +
                          new string(borderChar, borderWidth));

        // Print the second line, centered with spaces
        Console.WriteLine(new string(borderChar, borderWidth) +
                          line2.PadLeft((cardWidth - borderWidth * 2 + line2.Length) / 2).PadRight(cardWidth - borderWidth * 2) +
                          new string(borderChar, borderWidth));
        
        // Print the bottom padding
        for(int i = 0; i < bottomPadding; i++)
        {
            Console.WriteLine(new string(borderChar, borderWidth) + new string(' ', cardWidth - borderWidth * 2) + new string(borderChar, borderWidth));
        }
        
        // Print the bottom border
        for(int i = 0; i < borderWidth; i++)
        {
            Console.WriteLine(borderLine);
        }
    }
}
