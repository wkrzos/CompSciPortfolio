public interface IArticlesContext
{
    IEnumerable<Article> GetAll();
    Article GetById(int id);
    void Add(Article article);
    void Update(Article article);
    void Delete(int id);
}
