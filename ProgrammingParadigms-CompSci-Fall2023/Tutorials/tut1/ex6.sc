// Define a recursive function 'listLength' that takes a list as its argument.
def listLength[A](list: List[A]): Int = {
  // Check if the list is empty. If it is, return 0, indicating the length is 0.
  if (list.isEmpty) {
    0
  } else {
    // If the list is not empty, add 1 to the length of the list obtained by calling 'listLength' recursively on the tail of the list (list.tail).
    1 + listLength(list.tail)
  }
}

// Call the 'listLength' function with the list List(1, 2, 3, 4, 5) to calculate its length.
val result = listLength(List(1, 2, 3, 4, 5)) // This will return the result of the length, which is 5 in this case.
