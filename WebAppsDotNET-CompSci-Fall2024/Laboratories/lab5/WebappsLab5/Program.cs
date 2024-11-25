using System;

class Program
{
    static void Main()
    {
        Console.WriteLine("Enter coefficient a:");
        double a = Convert.ToDouble(Console.ReadLine());

        Console.WriteLine("Enter coefficient b:");
        double b = Convert.ToDouble(Console.ReadLine());

        Console.WriteLine("Enter coefficient c:");
        double c = Convert.ToDouble(Console.ReadLine());

        // Solve the quadratic equation
        var result = SolveQuadraticEquation(a, b, c);

        // Display the results
        switch (result.Count)
        {
            case 0:
                Console.WriteLine("No real solutions.");
                break;
            case 1:
                Console.WriteLine($"One solution: x = {result.X1:F2}");
                break;
            case 2:
                Console.WriteLine($"Two solutions: x1 = {result.X1:F2}, x2 = {result.X2:F2}");
                break;
        }
    }

    /// <summary>
    /// Solves a quadratic equation ax^2 + bx + c = 0.
    /// </summary>
    /// <param name="a">Coefficient a.</param>
    /// <param name="b">Coefficient b.</param>
    /// <param name="c">Coefficient c.</param>
    /// <returns>A tuple containing the number of solutions and the solutions (if any).</returns>
    static (int Count, double? X1, double? X2) SolveQuadraticEquation(double a, double b, double c)
    {
        // If a, b, and c are all 0, the equation is invalid
        if (a == 0 && b == 0 && c == 0)
        {
            Console.WriteLine("Invalid equation. Coefficients cannot all be zero.");
            return (0, null, null);
        }

        // If a = 0, the equation is linear: bx + c = 0
        if (a == 0)
        {
            if (b == 0)
            {
                return (0, null, null); // No solutions if b = 0 and c != 0
            }

            // Linear solution: x = -c / b
            return (1, -c / b, null);
        }

        // For quadratic equation: ax^2 + bx + c = 0
        double discriminant = b * b - 4 * a * c;

        if (discriminant < 0)
        {
            // No real solutions
            return (0, null, null);
        }
        else if (discriminant == 0)
        {
            // One real solution
            double x = -b / (2 * a);
            return (1, x, null);
        }
        else
        {
            // Two real solutions
            double x1 = (-b + Math.Sqrt(discriminant)) / (2 * a);
            double x2 = (-b - Math.Sqrt(discriminant)) / (2 * a);
            return (2, x1, x2);
        }
    }
}
