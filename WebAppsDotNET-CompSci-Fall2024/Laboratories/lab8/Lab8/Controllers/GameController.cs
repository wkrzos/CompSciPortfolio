using Microsoft.AspNetCore.Mvc;
using Microsoft.AspNetCore.Http;
using System;

namespace Lab8.Controllers
{
    public class GameController : Controller
    {
        private const string SessionKeyRange = "Range";
        private const string SessionKeyLowerRange = "LowerRange";
        private const string SessionKeyRandValue = "RandValue";
        private const string SessionKeyAttempts = "Attempts";

        private Random _random = new Random();

        private int Range
        {
            get => HttpContext.Session.GetInt32(SessionKeyRange) ?? 10;
            set => HttpContext.Session.SetInt32(SessionKeyRange, value);
        }

        private int LowerRange
        {
            get => HttpContext.Session.GetInt32(SessionKeyLowerRange) ?? 0;
            set => HttpContext.Session.SetInt32(SessionKeyLowerRange, value);
        }

        private int RandValue
        {
            get => HttpContext.Session.GetInt32(SessionKeyRandValue) ?? DrawNewNumber();
            set => HttpContext.Session.SetInt32(SessionKeyRandValue, value);
        }

        private int Attempts
        {
            get => HttpContext.Session.GetInt32(SessionKeyAttempts) ?? 0;
            set => HttpContext.Session.SetInt32(SessionKeyAttempts, value);
        }

        [Route("Set/{n}/{m}")]
        public IActionResult Set(int n, int m)
        {
            if (n <= 0 || n <= m)
            {
                ViewData["Message"] = n <= 0
                    ? "The range must be a positive integer."
                    : "The upper range must be greater than the lower range.";
                ViewData["CssClass"] = "error";
                return View("Result");
            }

            Range = n;
            LowerRange = m;
            DrawNewNumber();
            ViewData["Message"] = $"Range set to {LowerRange} - {Range}. A new number has been drawn.";
            ViewData["CssClass"] = "info";
            return View("Result");
        }

        [Route("Set/{n}")]
        public IActionResult Set(int n)
        {
            if (n <= 0 || n <= LowerRange)
            {
                ViewData["Message"] = n <= 0
                    ? "The range must be a positive integer."
                    : "The upper range must be greater than the lower range.";
                ViewData["CssClass"] = "error";
                return View("Result");
            }

            Range = n;
            DrawNewNumber();
            ViewData["Message"] = $"Range set to {LowerRange} - {Range}. A new number has been drawn.";
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
            Attempts++;

            if (guess < RandValue)
            {
                ViewData["Message"] = $"Attempt {Attempts}: {guess} is too low.";
                ViewData["CssClass"] = "low";
            }
            else if (guess > RandValue)
            {
                ViewData["Message"] = $"Attempt {Attempts}: {guess} is too high.";
                ViewData["CssClass"] = "high";
            }
            else
            {
                ViewData["Message"] = $"Congratulations! {guess} is correct. It took you {Attempts} attempts.";
                ViewData["CssClass"] = "success";
                DrawNewNumber();
            }

            return View("Result");
        }

        private int DrawNewNumber()
        {
            int newNumber = _random.Next(LowerRange, Range);
            RandValue = newNumber;
            Attempts = 0;
            return newNumber;
        }
    }
}
