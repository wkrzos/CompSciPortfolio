// Define a recursive function 'flatten1' that takes a list as its argument.
def flatten1[A](list: List[List[A]]): List[A] = {
  // Check if the input list is empty. If it is, return an empty list (base case of recursion).
  if (list.isEmpty)
    List()
  else {
    // If the list is not empty, then:
    val head = list.head
    // Extract the head (the first element) of the list.
    val tail = list.tail
    // Extract the tail (the rest of the list) after removing the head.
    head ::: flatten1(tail)
    // Concatenate the head with the recursive result on the tail.
  }
}

// Call the 'flatten1' function with a list of lists.
val result = flatten1(List(List(5, 6), List(1, 2, 3), List(6, 5)))
