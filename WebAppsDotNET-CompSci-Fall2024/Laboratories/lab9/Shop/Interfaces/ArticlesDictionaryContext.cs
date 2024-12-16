public class ArticlesDictionaryContext : IArticlesContext
{
    private readonly Dictionary<int, Article> _articles = new();
    private int _currentId = 1;

    public IEnumerable<Article> GetAll() => _articles.Values;

    public Article GetById(int id) => _articles.ContainsKey(id) ? _articles[id] : null;

    public void Add(Article article)
    {
        article.Id = _currentId++;
        _articles[article.Id] = article;
    }

    public void Update(Article article)
    {
        if (_articles.ContainsKey(article.Id))
        {
            _articles[article.Id] = article;
        }
    }

    public void Delete(int id) => _articles.Remove(id);
}
