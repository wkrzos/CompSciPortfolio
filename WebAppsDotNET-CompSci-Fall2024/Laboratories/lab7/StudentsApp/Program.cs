using System;
using System.Collections.Generic;
using System.Linq;
using StudentsApp.Models;

public class Program
{
    // ex1
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
            new StudentWithTopics(1, 1001, "Alice", Gender.Female, true, 1, new List<string> { "Math", "Physics" }),
            new StudentWithTopics(2, 1002, "Bob", Gender.Male, true, 1, new List<string> { "Math", "Physics" }),
            new StudentWithTopics(3, 1003, "Alice", Gender.Female, true, 2, new List<string> { "Math", "Geography" }),
            new StudentWithTopics(4, 1004, "Charlie", Gender.Male, false, 1, new List<string> { "Math", "Geography" }),
            new StudentWithTopics(5, 1005, "Dave", Gender.Male, true, 1, new List<string> { "Biology", "Geography" }),
        };

        //ex1
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

        // ex2.1
        // Sorting topics by frequency of occurrence
        var sortedTopics = students
            .SelectMany(s => s.Topics) // Collect all topics from the list of students
            .GroupBy(topic => topic)   // Group by topic name
            .OrderByDescending(group => group.Count()) // Sort in descending order by the number of occurrences
            .Select(group => new { Topic = group.Key, Count = group.Count() });

        Console.WriteLine("Topics sorted by frequency of occurrence:");
        foreach (var topic in sortedTopics)
        {
            Console.WriteLine($"Topic: {topic.Topic}, Count: {topic.Count}");
        }

        // ex2.2
        // Group by gender and then sort topics within each gender group
        var topicsByGender = students
            .GroupBy(s => s.Gender) // Group by gender
            .Select(group => new
            {
                Gender = group.Key,
                Topics = group
                    .SelectMany(s => s.Topics) // Collect topics from students in this gender group
                    .GroupBy(topic => topic)   // Group topics by name
                    .OrderByDescending(group => group.Count()) // Sort by frequency of occurrence
                    .Select(g => new { Topic = g.Key, Count = g.Count() })
            });

        Console.WriteLine("Topics sorted by frequency of occurrence within each gender:");
        foreach (var genderGroup in topicsByGender)
        {
            Console.WriteLine($"Gender: {genderGroup.Gender}");
            foreach (var topic in genderGroup.Topics)
            {
                Console.WriteLine($"  Topic: {topic.Topic}, Count: {topic.Count}");
            }
        }

        // ex3
        // Sample list of StudentWithTopics
        var studentsWithTopics = new List<StudentWithTopics>
        {
            new StudentWithTopics(1, 1001, "Alice", Gender.Female, true, 1, new List<string> { "Math", "Science" }),
            new StudentWithTopics(2, 1002, "Bob", Gender.Male, true, 1, new List<string> { "Science", "History" }),
            new StudentWithTopics(3, 1003, "Charlie", Gender.Male, true, 2, new List<string> { "Math", "History", "Science" }),
            new StudentWithTopics(4, 1004, "Diana", Gender.Female, true, 1, new List<string> { "History" }),
        };

        // Create a unique list of topics
        var uniqueTopics = studentsWithTopics
            .SelectMany(s => s.Topics)
            .Distinct()
            .Select((topic, index) => new Topic(index + 1, topic)) // Assign unique IDs
            .ToList();

        Console.WriteLine("Unique Topics:");
        foreach (var topic in uniqueTopics)
        {
            Console.WriteLine(topic);
        }

        // Transform StudentWithTopics into Student
        var students2 = studentsWithTopics.Select(s => new Student(
            s.Id,
            s.Index,
            s.Name,
            s.Gender,
            s.Active,
            s.DepartmentId,
            s.Topics.Select(topic => uniqueTopics.First(t => t.Name == topic).Id).ToList()
        )).ToList();

        Console.WriteLine("\nTransformed Students:");
        foreach (var student in students2)
        {
            Console.WriteLine(student);
        }
    }
}
