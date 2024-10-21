// Functional version of modified Pascal's triangle
def modifiedPascalF(n: Int): List[Int] = {

  // Element-wise operation on two lists, used for addition and subtraction
  def elementWiseOperation(a: List[Int], b: List[Int], op: (Int, Int) => Int): List[Int] =
    (a, b) match {
      // If the first list is empty, return the second list.
      case (Nil, _) => b
      // If the second list is empty, return the first list.
      case (_, Nil) => a
      // Apply the operation to the head elements and recursively process the rest of the lists.
      case (x :: xs, y :: ys) => op(x, y) :: elementWiseOperation(xs, ys, op)
    }

  // Recursive function to generate a modified Pascal's triangle row
  def generateRow(row: Int): List[Int] = row match {
    // Base case: Row 0 has a single element, which is 1.
    case 0 => List(1)
    case _ =>
      // Generate the previous row using recursion.
      val previousRow = generateRow(row - 1)
      // Determine the operation (addition or subtraction) based on the row's parity.
      val operation: (Int, Int) => Int = if (row % 2 == 0) _ + _ else _ - _
      // Construct the current row by prepending 1 and performing element-wise operations.
      1 :: elementWiseOperation(previousRow, previousRow.tail, operation)
  }

  // Call the generateRow function to generate the desired row.
  generateRow(n)
}

// Imperative version of modified Pascal's triangle
def modifiedPascalI(n: Int): List[Int] = {
  // Base case: If n is 0, return a list with a single element 1.
  if (n == 0) return List(1)

  // Create arrays to represent the current and previous rows.
  val currentRow = Array.fill(n + 1)(0)
  val previousRow = Array.fill(n + 1)(0)

  // Initialize the first element of both rows to 1.
  currentRow(0) = 1
  previousRow(0) = 1

  // Iterate through each row from 1 to n.
  for (rowIndex <- 1 to n) {
    // Check if the current row is even or odd.
    if (rowIndex % 2 == 0) {
      // Calculate the values in the current row using the values in the previous row.
      for (columnIndex <- 1 to rowIndex) {
        currentRow(columnIndex) = previousRow(columnIndex - 1) + previousRow(columnIndex)
      }
    } else {
      // Calculate the values in the previous row using the values in the current row.
      for (columnIndex <- 1 to rowIndex) {
        previousRow(columnIndex) = currentRow(columnIndex - 1) - currentRow(columnIndex)
      }
    }
  }

  // Check if n is even or odd and return the corresponding row as a list.
  if (n % 2 == 0) {
    currentRow.toList
  } else {
    previousRow.toList
  }
}


modifiedPascalF(0) // Should be (1)
modifiedPascalF(2) // Should be (1, 2, 1)
modifiedPascalF(3) // Should be (1, -1, 1, 1)
modifiedPascalF(4) // Should be (1, 0, 0, 2, 1)
modifiedPascalF(5) // Should be (1, 1, 0, -2, 1, 1)
modifiedPascalF(6) // Should be (1, 2, 1, -2, -1, 2, 1)

modifiedPascalI(0) // Should be (1)
modifiedPascalI(2) // Should be (1, 2, 1)
modifiedPascalI(3) // Should be (1, -1, 1, 1)
modifiedPascalI(4) // Should be (1, 0, 0, 2, 1)
modifiedPascalI(5) // Should be (1, 1, 0, -2, 1, 1)
modifiedPascalI(6) // Should be (1, 2, 1, -2, -1, 2, 1)

