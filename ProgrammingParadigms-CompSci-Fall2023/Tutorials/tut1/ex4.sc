// Define a recursive function that squares each element of a list
def sqrList(list: List[Int]): List[Int] = {
  // Define a helper function for the recursive process
  def sqrListHelper(list: List[Int]): List[Int] = {
    if (list.isEmpty) {
      List()
    } else {
      // Square the head of the list and add it to the result list,
      // then recursively process the tail of the list
      (list.head * list.head) :: sqrListHelper(list.tail)
    }
  }

  // Call the helper function with the original list
  sqrListHelper(list)
}

// Test the sqrList function with an example list
val result = sqrList(List(1, 2, 3, 4, 5))
