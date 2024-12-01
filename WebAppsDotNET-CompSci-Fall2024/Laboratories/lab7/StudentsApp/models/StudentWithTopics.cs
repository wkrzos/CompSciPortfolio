namespace GroupStudentsApp.Models{

    public enum Gender
    {
        Female,
        Male
    }

    public class StudentWithTopics
    {
        public int Id { get; set; }
        public int Index { get; set; }
        public string Name { get; set; }
        public Gender Gender {get; set; }
        public bool Active { get; set; }
        public int DepartmentId { get; set; }

        public List<string> Topics { get; set; }

        public StudentWithTopics(int id, int index, string name, Gender gender, bool active, int departmentId)
        {
            Id = id;
            Index = index;
            Name = name;
            Gender = gender;
            Active = active;
        }

        public override string ToString()
        {
            return $"Student: {Name}";
        } 
    }
}
