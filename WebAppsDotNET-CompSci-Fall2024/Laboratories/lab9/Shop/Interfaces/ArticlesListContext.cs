public class ArticlesListContext : IArticlesContext
{
    private readonly List<Article> _articles = new();

    public Article? GetById(int id) => _articles.FirstOrDefault(a => a.Id == id);

    public void Update(Article article)
    {
        var existing = GetById(article.Id);
        if (existing != null)
        {
            existing.Name = article.Name;
            existing.Price = article.Price;
            existing.ExpiryDate = article.ExpiryDate;
            existing.Category = article.Category;
        }
    }

    public void Delete(int id)
    {
        var article = GetById(id);
        if (article != null)
        {
            _articles.Remove(article);
        }
    }

    public IEnumerable<Article> GetAll()
    {
        Console.WriteLine($"GetAll called. Current articles: {string.Join(", ", _articles.Select(a => a.Name))}");
        return _articles;
    }

    public void Add(Article article)
    {
        article.Id = _articles.Any() ? _articles.Max(a => a.Id) + 1 : 1;
        _articles.Add(article);
        Console.WriteLine($"Added: {article.Name}. Current articles: {string.Join(", ", _articles.Select(a => a.Name))}");
    }


    public ArticlesListContext()
    {
        Console.WriteLine($"New ArticlesListContext instance created: {GetHashCode()}");
        _articles.Add(new Article
        {
            Id = 1,
            Name = "Test Article",
            Price = 19.99M,
            ExpiryDate = DateTime.Now.AddMonths(1),
            Category = Category.Food
        });
    }
}
