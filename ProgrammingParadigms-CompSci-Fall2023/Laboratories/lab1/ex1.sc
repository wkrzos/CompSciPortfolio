// Exercise 1
def reverse4(x: Any, y: Any, z: Any, w: Any): (Any, Any, Any, Any) = (w, z, y, x)

def testReverse4(): Unit = {
  // Test 1: Standard element reversal
  val result1 = reverse4(0, 1, 2, 3)
  assert(result1 == (3, 2, 1, 0))

  // Test 2: Reversing elements with values of 0
  val result2 = reverse4(0, 0, 0, 0)
  assert(result2 == (0, 0, 0, 0))

  // Test 3: Reversing elements with negative values
  val result3 = reverse4(-1, -2, -3, -4)
  assert(result3 == (-4, -3, -2, -1))

  // Test 4: Reversing elements with different types
  val result4 = reverse4(1.0, true, 1, "A")
  assert(result4 == ("A", 1, true, 1.0))

  // Test 5: Reversing elements with different types
  val result5 = reverse4(1.5, "Hello", 'c', 42)
  assert(result5 == (42, 'c', "Hello", 1.5))
}

// Exercise 2
def sumRange(start: Int, end_ : Int): Int = {
  def aux(acc: Int, current: Int): Int = {
    if (current > end_ - 1) acc
    else aux(acc + current, current + 1)
  }
  aux(0, start)
}

def prodRange(start: Int, end_ : Int): Int = {
  def aux(acc: Int, current: Int): Int = {
    if (current > end_ - 1) acc
    else if (start == 0) 0
    else aux(acc * current, current + 1)
  }
  if (start == 0) 0
  else aux(1, start)
}

def sumProd(start: Int, end_ : Int): (Int, Int) = {
  val sumOfRange = sumRange(start, end_)
  val prodOfRange = prodRange(start, end_)
  (sumOfRange, prodOfRange)
}

def testSumProd(): Unit = {
  // Test 1: Positive numbers
  val result1 = sumProd(1, 5)
  assert(result1 == (10, 24))

  // Test 2: Only zeros
  val result2 = sumProd(0, 0)
  assert(result2 == (0, 0))

  // Test 3: Negative numbers with an even number of factors
  val result3 = sumProd(-4, 0)
  assert(result3 == (-10, 24))

  // Test 4: Negative numbers with an odd number of factors
  val result4 = sumProd(-4, -1)
  assert(result4 == (-9, -24))

  // Test 5: Range from negative to positive
  val result5 = sumProd(-4, 5)
  assert(result5 == (0, 0))
}

// Exercise 3
def isPerfect(n: Int): Boolean = {
  def isPerfectHelper(i: Int, sum: Int): Boolean = {
    if (i >= n) {
      sum == n
    } else {
      if (n % i == 0) {
        isPerfectHelper(i + 1, sum + i)
      } else {
        isPerfectHelper(i + 1, sum)
      }
    }
  }

  isPerfectHelper(1, 0)
}

// Tests
def testIsPerfect(): Unit = {
  // Test 1: 6 is a perfect number
  val result1 = isPerfect(6)
  assert(result1)

  // Test 2: 28 is a perfect number
  val result2 = isPerfect(28)
  assert(result2)

  // Test 3: 12 is not a perfect number
  val result3 = isPerfect(12)
  assert(!result3)

  // Test 4: 496 is a perfect number
  val result4 = isPerfect(496)
  assert(result4)

  // Test 5: 7 is not a perfect number
  val result5 = isPerfect(7)
  assert(!result5)
}

// Exercise 4
def insert(list: List[Any], node: Any, position: Int): List[Any] = {
  def aux(lst: List[Any], elem: Any, pos: Int): List[Any] = {
    if (pos == 0) {
      elem :: lst
    } else if (lst.isEmpty) {
      List(elem)
    } else if (pos <= 0) {
      elem :: lst
    } else {
      val hd :: tl = lst
      hd :: aux(tl, elem, pos - 1)
    }
  }
  aux(list, node, position)
}

def testInsert(): Unit = {
  // Test 1: Inserting an element at the beginning of an empty list
  val result1 = insert(Nil, "A", 0)
  assert(result1 == List("A"))

  // Test 2: Inserting an element at the beginning of a non-empty list
  val result2 = insert(List("B", "C"), "A", 0)
  assert(result2 == List("A", "B", "C"))

  // Test 3: Inserting an element at the end of the list
  val result3 = insert(List("A", "B"), "C", 2)
  assert(result3 == List("A", "B", "C"))

  // Test 4: Inserting an element out of the list's range - it should land at the end
  val result4 = insert(List("A", "B"), "C", 10)
  assert(result4 == List("A", "B", "C"))

  // Test 5: Inserting an element at the first position (index 1)
  val result5 = insert(List("A", "B", "C"), "X", 1)
  assert(result5 == List("A", "X", "B", "C"))

  // Test 6: Inserting an element at the middle position (index 2)
  val result6 = insert(List("A", "B", "C"), "Y", 2)
  assert(result6 == List("A", "B", "Y", "C"))

  // Test 7: Inserting an element at the penultimate position (index 2)
  val result7 = insert(List("A", "B", "C"), "Z", 2)
  assert(result7 == List("A", "B", "Z", "C"))

  // Test 8: Inserting an element at the end of the list where the position equals the list's length
  val result8 = insert(List("A", "B", "C"), "D", 3)
  assert(result8 == List("A", "B", "C", "D"))

  // Test 9: Inserting an element at the beginning of the list when the position is negative
  val result9 = insert(List("B", "C"), "A", -1)
  assert(result9 == List("A", "B", "C"))

  // Test 10: Inserting an element at the second position when the position is negative
  val result10 = insert(List("A", "C"), "B", -2)
  assert(result10 == List("B", "A", "C"))

  // Test 11: Inserting an element at the end of the list when the position is highly negative
  val result11 = insert(List("A", "B"), "C", -10)
  assert(result11 == List("C", "A", "B"))
}

// Live Coding 1

def choice(list1: List[Int], list2: List[Int]): List[Int] = {
  if (list1.isEmpty && list2.isEmpty) {
    List.empty
  } else if (list2.isEmpty) {
    list1
  } else if (list1.isEmpty) {
    list2
  } else {
    val (hd1, tl1) = (list1.head, list1.tail)
    val (hd2, tl2) = (list2.head, list2.tail)
    val max_element = if (hd1 > hd2) hd1 else hd2
    max_element :: choice(tl1, tl2)
  }
}

def testChoice(): Unit = {
  // Test 1: Both lists are empty
  val result1 = choice(List.empty, List.empty)
  assert(result1 == List.empty)

  // Test 2: First list is empty
  val result2 = choice(List.empty, List(1, 2, 3))
  assert(result2 == List(1, 2, 3))

  // Test 3: Second list is empty
  val result3 = choice(List(4, 5, 6), List.empty)
  assert(result3 == List(4, 5, 6))

  // Test 4: Lists have the same elements at corresponding positions
  val result4 = choice(List(1, 2, 3), List(4, 5, 6))
  assert(result4 == List(4, 5, 6))

  // Test 5: Lists have different elements at corresponding positions
  val result5 = choice(List(5, 3, 8), List(4, 6, 2))
  assert(result5 == List(5, 6, 8))

  // Test 6: Second list is longer than the first one
  val result6 = choice(List(1, 2), List(3, 4, 5))
  assert(result6 == List(3, 4, 5))

  // Test 7: First list is longer than the second one
  val result7 = choice(List(1, 2, 3, 4, 5), List(6, 7))
  assert(result7 == List(6, 7, 3, 4, 5))

  // Test 8: Lists have the same elements but different lengths
  val result8 = choice(List(1, 2, 3), List(4, 5))
  assert(result8 == List(4, 5, 3))
}

// Live Coding 2

def squash(list: List[List[Int]]): List[Int] = {
  def squishHelper(currList: List[Int], remainingLists: List[List[Int]]): List[Int] = {
    if (currList == Nil) {
      if (remainingLists.isEmpty) {
        Nil
      } else {
        squishHelper(remainingLists.head, remainingLists.tail)
      }
    } else {
      currList.head :: squishHelper(currList.tail, remainingLists)
    }
  }

  if (list == Nil) {
    Nil
  } else {
    squishHelper(list.head, list.tail)
  }
}

def testSquash(): Unit = {
  // Test 1: Empty list
  val result1 = squash(List(List.empty))
  assert(result1 == List.empty)

  // Test 2: List with one element
  val result2 = squash(List(List(1)))
  assert(result2 == List(1))

  // Test 3: List with two different elements
  val result3 = squash(List(List(1), List(2)))
  assert(result3 == List(1, 2))

  // Test 4: List with two equal elements
  val result4 = squash(List(List(1), List(1)))
  assert(result4 == List(1, 1))

  // Test 5: List with three different elements
  val result5 = squash(List(List(1), List(2), List(3)))
  assert(result5 == List(1, 2, 3))

  // Test 6: List with three equal elements
  val result6 = squash(List(List(1), List(1), List(1)))
  assert(result6 == List(1, 1, 1))

  // Test 7: List with three elements, two of which are equal
  val result7 = squash(List(List(1), List(1), List(2)))
  assert(result7 == List(1, 1, 2))

  // Test 8: List with three elements, two of which are equal
  val result8 = squash(List(List(1), List(2), List(2)))
  assert(result8 == List(1, 2, 2))
}

// Running the tests
testReverse4()
println("All tests passed.")

testSumProd()
println("All tests passed.")

testIsPerfect()
println("All tests passed.")

testInsert()
println("All tests passed.")

testChoice()
println("All tests passed.")

testSquash()
println("All tests passed.")