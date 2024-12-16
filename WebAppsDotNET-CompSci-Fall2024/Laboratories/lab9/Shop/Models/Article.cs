public enum Category
{
    Electronics,
    Food,
    Clothing,
    Household,
    Other
}

public class Article
{
    public int Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public decimal Price { get; set; }
    public DateTime ExpiryDate { get; set; }
    public Category Category { get; set; }
}
