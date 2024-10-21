def curry3[A, B, C, D](f: (A, B, C) => D): A => B => C => D = { a => b => c =>
f(a, b, c)
}

def uncurry3[A, B, C, D](f: A => B => C => D): (A, B, C) => D = { (a, b, c) =>
f(a)(b)(c)
}

def sumProd2(xs: List[Int]): (Int, Int) = {
xs.foldLeft((0, 1))((accumulator, h) =>
    (accumulator._1 + h, accumulator._2 * h)
)
}

// Example usage
val curriedFunction = curry3((a: Int, b: Int, c: Int) => a + b + c)
val uncurriedFunction = uncurry3(curriedFunction)

val result = sumProd2(List(1, 2, 3, 4, 5))
println(s"Sum: ${result._1}, Product: ${result._2}")
