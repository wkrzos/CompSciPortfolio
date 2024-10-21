def lrepeat[A](k: Int)(lxs: LazyList[A]): LazyList[A] = {
  lxs.flatMap(x => LazyList.fill(k)(x))
}

lazy val lfib: LazyList[Int] = {
  def fib(a: Int, b: Int): LazyList[Int] =
    LazyList.cons(a, fib(b, a + b))

  fib(0, 1)
}

sealed trait lBT[+A]
case object LEmpty extends lBT[Nothing]
case class LNode[+A](elem: A, left: () => lBT[A], right: () => lBT[A]) extends lBT[A]

def lBreadth[A](ltree: lBT[A]): LazyList[A] = {
  def breadthQueue(queue: List[lBT[A]]): LazyList[A] = {
    queue match {
      case Nil => LazyList.empty
      case LEmpty :: rest => breadthQueue(rest)
      case LNode(x, left, right) :: rest =>
        LazyList.cons(x, breadthQueue(rest ++ List(left(), right())))
    }
  }

  breadthQueue(List(ltree))
}

def lTree(n: Int): lBT[Int] = LNode(n, () => lTree(2 * n), () => lTree(2 * n + 1))
