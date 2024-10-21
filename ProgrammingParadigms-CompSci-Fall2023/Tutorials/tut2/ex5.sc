def initSegment(list1: List[Any], list2: List[Any]): Boolean = {
  (list1, list2) match {
    case (Nil, _) => true // If 'list1' is empty, it's an initial segment of any list.
    case (_, Nil) => false // If 'list2' is empty, it's not an initial segment of 'list1'.
    case (x :: xs, y :: ys) if x == y => initSegment(xs, ys)
    case _ => false
  }
}

// Test cases
val test1 = initSegment(Nil, List(1, 2, 3)) // Expect: true
val test2 = initSegment(List(1, 2, 3), Nil) // Expect: false
val test3 = initSegment(List(1), List(1, 2, 3)) // Expect: true
val test4 = initSegment(List(1, 2, 3), List(1)) // Expect: false
val test5 = initSegment(List(1, 2), List(1, 2, 3, 4)) // Expect: true
val test6 = initSegment(List(1, 2, 4), List(1, 2, 3, 4)) // Expect: false
val test7 = initSegment(List("a", "b"), List("a", "b", "c")) // Expect: true
val test8 = initSegment(List("a", "b", "d"), List("a", "b", "c")) // Expect: false
val test9 = initSegment(List("x", "y", "z"), List("x", "y", "z")) // Expect: true
val test10 = initSegment(List(1, 2, 3, 4), List(1, 2, 3, 4)) // Expect: true
val test11 = initSegment(List(1, 2, 3, 4), List(1, 2, 3)) // Expect: false
