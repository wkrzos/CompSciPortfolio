// Define a recursive function 'count' that takes two arguments: 'element' and 'list'.
def count[A](element: A, list: List[A]): Int = {
  // Define an inner recursive function 'countHelper' with three arguments: 'element', 'lst', and 'acc' (accumulator).
  def countHelper(element: A, lst: List[A], acc: Int): Int = {
    // Check if the input list 'lst' is empty.
    if (lst.isEmpty) {
      acc // If the list is empty, return the accumulator 'acc'.
    } else {
      // Extract the head and tail of the list.
      val head = lst.head
      val tail = lst.tail
      if (head == element) {
        countHelper(element, tail, acc + 1) // If the head of the list is equal to the 'element', recursively call 'countHelper' with the tail of the list and increment the accumulator by 1.
      } else {
        countHelper(element, tail, acc) // If the head is not equal to the 'element', recursively call 'countHelper' with the tail of the list without changing the accumulator.
      }
    }
  }

  // Start the counting process by calling 'countHelper' with 'element', 'list', and an initial accumulator of 0.
  countHelper(element, list, 0)
}

val result = count(3, List(1, 2, 3, 3, 4, 3)) // Call the 'count' function with 'element' 3 and a list, and store the result in the 'result' variable.
