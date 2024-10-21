// Define a recursive function 'replicate' that takes an element and the number of times to replicate it
def replicate[A](element: A, times: Int): List[A] = {
  // Define a helper function 'replicateHelper' that replicates the element 'times' times and accumulates the result in 'table'
  def replicateHelper(element: A, times: Int, table: List[A]): List[A] = {
    if (times == 0) {
      table // If 'times' is zero, return the accumulated 'table' as the result (base case)
    } else {
      replicateHelper(element, times - 1, element :: table) // Recursively call 'replicateHelper' with one less 'times' and add 'element' to 'table'
    }
  }

  replicateHelper(element, times, List.empty[A]) // Initialize the helper function with 'element', 'times', and an empty 'table'
}

// Test the replicate function by replicating the element "Ha" five times
val result = replicate("Ha", 5)
