def reverseDelete(n: Int, list: List[Int]): List[Int] = {

  def helper(lst: List[Int], i: Int): (List[Int], List[Int]) = (lst, i) match {
    case (hd :: tl, i) if i < n =>
      val (accRet, result) = helper(tl, i + 1)
      if (accRet == Nil) (Nil, result) else (accRet.tail, accRet.head :: result)
    case (lst, i) if i == n => (list, lst.tail)
    case (lst, _) => (list, lst)
  }

  val (_, res) = helper(list, 0)
  res
}


val result = reverseDelete(3, List(1, 2, 3, 4, 5, 6))
println(result)

