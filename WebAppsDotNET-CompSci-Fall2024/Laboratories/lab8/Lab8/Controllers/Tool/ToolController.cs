using Microsoft.AspNetCore.Mvc;

namespace Controllers.Tool
{
    public class ToolController : Controller
    {
        [Route("Tool/Solve/{a}/{b}/{c}")]
        public IActionResult Solve(double a, double b, double c)
        {
            var discriminant = b * b - 4 * a * c;
            string message;
            string cssClass;

            if (a == 0 && b == 0 && c == 0)
            {
                message = "The equation is an identity (infinitely many solutions).";
                cssClass = "identity";
            }
            else if (a == 0 && b == 0)
            {
                message = "The equation is inconsistent (no solutions).";
                cssClass = "no-solution";
            }
            else if (a == 0)
            {
                double singleRoot = -c / b;
                message = $"The equation is linear with a single root: x = {singleRoot}";
                cssClass = "single-root";
            }
            else if (discriminant > 0)
            {
                double root1 = (-b + Math.Sqrt(discriminant)) / (2 * a);
                double root2 = (-b - Math.Sqrt(discriminant)) / (2 * a);
                message = $"The equation has two distinct roots: x1 = {root1}, x2 = {root2}";
                cssClass = "two-roots";
            }
            else if (discriminant == 0)
            {
                double root = -b / (2 * a);
                message = $"The equation has one double root: x = {root}";
                cssClass = "double-root";
            }
            else
            {
                message = "The equation has no real solutions.";
                cssClass = "no-solution";
            }

            ViewData["Message"] = message;
            ViewData["CssClass"] = cssClass;

            return View();
        }
    }
}
