using System;

class Program
{
    static void Main()
    {
        int[] array = { 1, 2, 3, 4, 5 };

        // 1. Sort the array
        Array.Sort(array);
        Console.WriteLine("Sorted array: " + string.Join(", ", array));

        // 2. Reverse the array
        Array.Reverse(array);
        Console.WriteLine("Reversed array: " + string.Join(", ", array));

        // 3. Find an element greater than 3
        int found = Array.Find(array, x => x > 3);
        Console.WriteLine("First element greater than 3: " + found);

        // 4. Find the index of an element
        int index = Array.IndexOf(array, 3);
        Console.WriteLine("Index of 3: " + index);

        // 5. Resize the array
        Array.Resize(ref array, 10);
        Console.WriteLine("Resized array: " + string.Join(", ", array));
    }
}
