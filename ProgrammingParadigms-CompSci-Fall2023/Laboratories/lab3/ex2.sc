// Solution 1

def composites1(n: Int): List[Int] = {

  def isComposite(num: Int): Boolean = {
    if (num < 2) false
    else (2 until num).exists(num % _ == 0)
  }

  // Generating composite numbers
  (for {
    num <- List.range(2, n + 1)
    if isComposite(num)
  } yield num)
}


val compNum1 = composites1(10)
val compNum2 = composites1(0)
val compNum3 = composites1 (-1)
val compNum4 = composites1(100)
val compNum5 = composites1(1000)

// Solution 2
val composites2 = (n: Int) => {
  def map[A, B](f: A => B, list: List[A]): List[B] =
    list match {
      case Nil => Nil
      case h :: t => f(h) :: map(f, t)
    }

  def filter[A](f: A => Boolean, list: List[A]): List[A] =
    list match {
      case Nil => Nil
      case h :: t if f(h) => h :: filter(f, t)
      case _ :: t => filter(f, t)
    }

  def isComposite(x: Int): Boolean =
    filter((y: Int) => x % y == 0, List.range(2, Math.sqrt(x).ceil.toInt + 1)).nonEmpty

  filter(isComposite, List.range(4, n + 1))
}


composites2(2)
composites2(20)
composites2(50)
composites2(100)
composites2(200)
composites2(9999999)

composites2(-1)
composites2(0)