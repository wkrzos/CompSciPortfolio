namespace StudentsApp.Models
{
    public class Topic
    {
        public int Id { get; set; }
        public String Name { get; set; }

        public Topic(int id, string name)
        {
            Id = id;
            Name = name;
        }

        public override string ToString()
        {
            return $"Topic: {Name}";
        }
    }
}