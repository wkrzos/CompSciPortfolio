// Ex 1

def whileLoop(condition: => Boolean)(body: => Unit): Unit = {
  if (condition) {
    body
    whileLoop(condition)(body)
  }
}

var count = 0

whileLoop(count < 3) {
  println(count)
  count += 1
}

// Ex 2
def swap(tab: Array[Int], i: Int, j: Int): Unit =
  val aux = tab(i)
  tab(i) = tab(j)
  tab(j) = aux

def choosePivot[A](tab: Array[A], m: Int, n: Int): A = tab((m + n) / 2)

def partition[A](tab: Array[Int], l: Int, r: Int): (Int, Int) = {
  var i = l
  var j = r
  val pivot = choosePivot(tab, l, r)
  
  while (i <= j) {
    while (tab(i) < pivot) i += 1
    while (pivot < tab(j)) j -= 1
    if (i <= j) {
      val temp = tab(i)
      tab(i) = tab(j)
      tab(j) = temp
      i += 1
      j -= 1
    }
  }
  
  (i, j)
}

def quickSort(tab: Array[Int], l: Int, r: Int): Unit = {
  if (l < r) {
    val (i, j) = partition(tab, l, r)
    if (j - l < r - i) {
      quickSort(tab, l, j)
      quickSort(tab, i, r)
    } else {
      quickSort(tab, i, r)
      quickSort(tab, l, j)
    }
  }
}

def quicksort(tab: Array[Int]): Unit = {
  quickSort(tab, 0, tab.length - 1)
}

// Test with an array of integers
val arr1 = Array(5, 2, 9, 1, 5, 6)
quicksort(arr1)
println(arr1.mkString(", ")) // Should print: 1, 2, 5, 5, 6, 9

// Test with an empty array
val arr3 = Array.empty[Int]
quicksort(arr3)
println(arr3.mkString(", ")) // Should print nothing (empty array)

// Test with an array containing a single element
val arr4 = Array(42)
quicksort(arr4)
println(arr4.mkString(", ")) // Should print: 42

// Test with an array in descending order
val arr5 = Array(9, 8, 7, 6, 5, 4, 3, 2, 1)
quicksort(arr5)
println(arr5.mkString(", ")) // Should print: 1, 2, 3, 4, 5, 6, 7, 8, 9
