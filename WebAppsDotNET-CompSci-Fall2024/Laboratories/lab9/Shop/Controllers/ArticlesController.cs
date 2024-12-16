using Microsoft.AspNetCore.Mvc;

public class ArticlesController : Controller
{
    private readonly IArticlesContext _context;

    // Constructor: Injects the IArticlesContext dependency
    public ArticlesController(IArticlesContext context)
    {
        _context = context ?? throw new ArgumentNullException(nameof(context));
    }

    // Displays a list of articles
    public IActionResult Index()
    {
        var articles = _context.GetAll();
        return View(articles);
    }

    // GET: Displays the Create page
    public IActionResult Create()
    {
        return View();
    }

    // POST: Handles the creation of a new article
    [HttpPost]
    [ValidateAntiForgeryToken] // Protects against CSRF attacks
    public IActionResult Create(Article article)
    {
        if (ModelState.IsValid)
        {
            _context.Add(article);
            return RedirectToAction(nameof(Index));
        }
        return View(article);
    }

    public IActionResult Edit(int id)
    {
        var article = _context.GetById(id); // Retrieve the article
        if (article == null)
        {
            return NotFound(); // If not found, return a 404 error
        }
        return View(article); // Pass the article to the view
    }

    // POST: Handles editing an existing article
    [HttpPost]
    [ValidateAntiForgeryToken] // Protects against CSRF attacks
    public IActionResult Edit(Article article)
    {
        if (ModelState.IsValid)
        {
            _context.Update(article);
            return RedirectToAction(nameof(Index));
        }
        return View(article);
    }

    // GET: Displays the Delete confirmation page
    public IActionResult Delete(int id)
    {
        var article = _context.GetById(id);
        if (article == null) return NotFound();
        return View(article);
    }

    // POST: Handles deletion of an article
    [HttpPost, ActionName("Delete")]
    [ValidateAntiForgeryToken] // Protects against CSRF attacks
    public IActionResult DeleteConfirmed(int id)
    {
        _context.Delete(id);
        return RedirectToAction(nameof(Index));
    }
}
