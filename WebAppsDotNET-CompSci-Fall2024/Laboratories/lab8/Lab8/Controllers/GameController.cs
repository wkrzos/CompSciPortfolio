using Microsoft.AspNetCore.Mvc;
using System;

namespace Lab8.Controllers
{
    public class GameController : Controller
    {
        private static int range = 10;
        private static int lowerRange = 0;
        
        private static int randValue;
        private static int attempts;
        private static Random random = new Random();

        static GameController()
        {
            DrawNewNumber();
        }

        [Route("Set/{n}/{m}")]
        public IActionResult Set(int n, int m)
        {
            if (n <= 0)
            {
                ViewData["Message"] = "The range must be a positive integer.";
                ViewData["CssClass"] = "error";
                return View("Result");
            }

            if (n <= m)
            {
                ViewData["Message"] = "The upper range must be greater than the lower range.";
                ViewData["CssClass"] = "error";
                return View("Result");
            }

            range = n;
            lowerRange = m;
            DrawNewNumber();
            ViewData["Message"] = $"Range set to {lowerRange} - {range}. A new number has been drawn.";
            ViewData["CssClass"] = "info";
            return View("Result");
        }

        [Route("Set/{n}")]
        public IActionResult Set(int n)
        {
            if (n <= 0)
            {
                ViewData["Message"] = "The range must be a positive integer.";
                ViewData["CssClass"] = "error";
                return View("Result");
            }

            if (n <= lowerRange)
            {
                ViewData["Message"] = "The upper range must be greater than the lower range.";
                ViewData["CssClass"] = "error";
                return View("Result");
            }

            range = n;
            DrawNewNumber();
            ViewData["Message"] = $"Range set to {lowerRange} - {range}. A new number has been drawn.";
            ViewData["CssClass"] = "info";
            return View("Result");
        }

        [Route("Draw")]
        public IActionResult Draw()
        {
            DrawNewNumber();
            ViewData["Message"] = "A new number has been drawn.";
            ViewData["CssClass"] = "info";
            return View("Result");
        }

        [Route("Guess/{guess}")]
        public IActionResult Guess(int guess)
        {
            attempts++;

            if (guess < randValue)
            {
                ViewData["Message"] = $"Attempt {attempts}: {guess} is too low.";
                ViewData["CssClass"] = "low";
            }
            else if (guess > randValue)
            {
                ViewData["Message"] = $"Attempt {attempts}: {guess} is too high.";
                ViewData["CssClass"] = "high";
            }
            else
            {
                ViewData["Message"] = $"Congratulations! {guess} is correct. It took you {attempts} attempts.";
                ViewData["CssClass"] = "success";
                DrawNewNumber();
            }

            return View("Result");
        }

        private static void DrawNewNumber()
        {
            randValue = random.Next(lowerRange, range);
            attempts = 0;
        }
    }
}
