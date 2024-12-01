using StudentsApp.Models;

namespace StudentsApp.Models{
    public class Student
    {
        public int Id { get; set; }
        public int Index { get; set; }
        public string Name { get; set; }
        public Gender Gender {get; set; }
        public bool Active { get; set; }
        public int DepartmentId { get; set; }

        public List<int> TopicIds { get; set; }

        public Student(int id, int index, string name, Gender gender, bool active, int departmentId, List<int> topicIds)
        {
            Id = id;
            Index = index;
            Name = name;
            Gender = gender;
            Active = active;
            DepartmentId = departmentId;
            TopicIds = topicIds;
        }

        public override string ToString()
        {
            return $"Student: {Name} Topics: {string.Join(", ", TopicIds)}";
        } 
    }
}
