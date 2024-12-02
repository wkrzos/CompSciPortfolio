using System;
using System.Collections.Generic;
using System.Linq;
using System.Reflection;
using StudentsApp.Models;

public class Program
{
    public static void Main(string[] args)
    {
        // Example 1: Group Students
        Ex1GroupStudents();

        // Example 2.1: Sort Topics by Frequency
        Ex21SortTopicsByFrequency();

        // Example 2.2: Sort Topics by FirstLetterOfName and Frequency
        Ex22SortTopicsByGenderAndFrequency();

        // Example 3: Transform StudentsWithTopics into Students
        Ex3TransformStudents();

        // Example 4: Use Reflection to Invoke Methods
        Ex4ReflectionExample();
    }

    // Example 1: Group Students
    public static void Ex1GroupStudents()
    {
        var students = new List<StudentWithTopics>
        {
            new StudentWithTopics(1, 1001, "Alice", Gender.Female, true, 1, new List<string> { "Math", "Physics" }),
            new StudentWithTopics(2, 1002, "Bob", Gender.Male, true, 1, new List<string> { "Math", "Physics" }),
            new StudentWithTopics(3, 1003, "Alice", Gender.Female, true, 2, new List<string> { "Math", "Geography" }),
            new StudentWithTopics(4, 1004, "Charlie", Gender.Male, false, 1, new List<string> { "Math", "Geography" }),
            new StudentWithTopics(5, 1005, "Dave", Gender.Male, true, 1, new List<string> { "Biology", "Geography" }),
        };

        int groupSize = 2;

        var groupedStudents = GroupStudents(students, groupSize);

        Console.WriteLine("\nExample 1: Group Students");
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

    public static IEnumerable<List<StudentWithTopics>> GroupStudents(List<StudentWithTopics> students, int groupSize)
    {
        if (groupSize <= 0) throw new ArgumentException("Group size must be greater than 0.");

        return students
            .OrderBy(s => s.Name)
            .ThenBy(s => s.Index)
            .Select((student, index) => new { student, index })
            .GroupBy(x => x.index / groupSize)
            .Select(group => group.Select(x => x.student).ToList());
    }

    // Example 2.1: Sort Topics by Frequency
    public static void Ex21SortTopicsByFrequency()
    {
        var students = CreateSampleStudents();

        var sortedTopics = students
            .SelectMany(s => s.Topics)
            .GroupBy(topic => topic)
            .OrderByDescending(group => group.Count())
            .Select(group => new { Topic = group.Key, Count = group.Count() });

        Console.WriteLine("\nExample 2.1: Topics Sorted by Frequency");
        foreach (var topic in sortedTopics)
        {
            Console.WriteLine($"Topic: {topic.Topic}, Count: {topic.Count}");
        }
    }

    // Example 2.2: Sort Topics by the first letter of a student's name and Frequency
    public static void Ex22SortTopicsByGenderAndFrequency()
    {
        var students = CreateSampleStudents();

        var topicsByFirstLetterOfName = students
            .GroupBy(s => s.Name[0])
            .Select(group => new
            {
                FirstLetterOfName = group.Key,
                Topics = group
                    .SelectMany(s => s.Topics)
                    .GroupBy(topic => topic)
                    .OrderByDescending(group => group.Count())
                    .Select(g => new { Topic = g.Key, Count = g.Count() })
            });

        Console.WriteLine("\nExample 2.2: Topics Sorted by FirstLetterOfName and Frequency");
        foreach (var firstLetterGroup in topicsByFirstLetterOfName)
        {
            Console.WriteLine($"FirstLetterOfName: {firstLetterGroup.FirstLetterOfName}");
            foreach (var topic in firstLetterGroup.Topics)
            {
                Console.WriteLine($"  Topic: {topic.Topic}, Count: {topic.Count}");
            }
        }
    }

    // Example 3: Transform StudentsWithTopics into Students
    public static void Ex3TransformStudents()
    {
        var studentsWithTopics = CreateSampleStudents();

        var uniqueTopics = studentsWithTopics
            .SelectMany(s => s.Topics)
            .Distinct()
            .Select((topic, index) => new Topic(index + 1, topic))
            .ToList();

        Console.WriteLine("\nExample 3: Unique Topics");
        foreach (var topic in uniqueTopics)
        {
            Console.WriteLine(topic);
        }

        var students = studentsWithTopics.Select(s => new Student(
            s.Id,
            s.Index,
            s.Name,
            s.Gender,
            s.Active,
            s.DepartmentId,
            s.Topics.Select(topic => uniqueTopics.First(t => t.Name == topic).Id).ToList()
        )).ToList();

        Console.WriteLine("\nTransformed Students:");
        foreach (var student in students)
        {
            Console.WriteLine(student);
        }
    }

    // Example 4: Use Reflection to Invoke Methods
    public static void Ex4ReflectionExample()
    {
        object calculator = new Calculator();

        Type calculatorType = typeof(Calculator);

        MethodInfo addMethod = calculatorType.GetMethod("Add");
        MethodInfo multiplyMethod = calculatorType.GetMethod("Multiply");

        Console.WriteLine("\nExample 4: Use Reflection to Invoke Methods");

        object resultAdd = addMethod.Invoke(calculator, new object[] { 5, 3 });
        Console.WriteLine($"Result of Add: {resultAdd}");

        object resultMultiply = multiplyMethod.Invoke(calculator, new object[] { 4, 7 });
        Console.WriteLine($"Result of Multiply: {resultMultiply}");
    }

    // Helper to Create Sample Students
    public static List<StudentWithTopics> CreateSampleStudents()
    {
        return new List<StudentWithTopics>
        {
            new StudentWithTopics(1, 1001, "Alice", Gender.Female, true, 1, new List<string> { "Math", "Science" }),
            new StudentWithTopics(2, 1002, "Bob", Gender.Male, true, 1, new List<string> { "Science", "History" }),
            new StudentWithTopics(3, 1003, "Charlie", Gender.Male, true, 2, new List<string> { "Math", "History", "Science" }),
            new StudentWithTopics(4, 1004, "Diana", Gender.Female, true, 1, new List<string> { "History" }),
        };
    }
}
