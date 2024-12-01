using System;
using System.Collections.Generic;
using System.Linq;
using GroupStudentsApp.Models;

public class Program
{
    public static IEnumerable<List<StudentWithTopics>> GroupStudents(List<StudentWithTopics> students, int groupSize)
    {
        // Validate group size
        if (groupSize <= 0) throw new ArgumentException("Group size must be greater than 0.");

        // Sort students by name and index
        var sortedStudents = students
            .OrderBy(s => s.Name)
            .ThenBy(s => s.Index)
            .ToList();

        // Group students into chunks of n
        return sortedStudents
            .Select((student, index) => new { student, index })
            .GroupBy(x => x.index / groupSize)
            .Select(group => group.Select(x => x.student).ToList());
    }

    public static void Main(string[] args)
    {
        var students = new List<StudentWithTopics>
        {
            new StudentWithTopics(1, 1001, "Alice", Gender.Female, true, 1),
            new StudentWithTopics(2, 1002, "Bob", Gender.Male, true, 1),
            new StudentWithTopics(3, 1003, "Alice", Gender.Female, true, 2),
            new StudentWithTopics(4, 1004, "Charlie", Gender.Male, false, 1),
            new StudentWithTopics(5, 1005, "Dave", Gender.Male, true, 1),
        };

        int groupSize = 2;

        var groupedStudents = GroupStudents(students, groupSize);

        foreach (var group in groupedStudents)
        {
            Console.WriteLine("Group:");
            foreach (var student in group)
            {
                Console.WriteLine(student);
            }
            Console.WriteLine();
        }
    }
}
