/*
Napsiz operator >=<. Ma on przyjmować jedną listę elementów
oraz funkcję.  Ma być on w formie rozwiniętej. Funkcja ma zwrócić listę, taką, że
pierwszy element łączy się z drugim, drugi z trzecim, trzeci z czwartym, itd.
Implementację oprzyj o funkcjonały.

Nie możesz użyć rekurencji, ani rekurencji ogonowej!!!

Funkcjonały to: insert, sigma, map, filter, fold_left, fold_right
*/

// Solution 1
def >=<[A](list: List[A], f: (A, A) => A): List[A] = {
  list.zip(list.tail).map { case (a, b) => f(a, b) }
}

val nums1 = List(1, 2, 3, 4)
val combined1 = >=<(nums1, (a: Int, b: Int) => a + b)

val nums2 = List(0, 1, 2, 3, 4, 5, 6)
val combined2 = >=<(nums2, (a: Int, b: Int) => a - b)

// Solution 2
implicit class ListOps[A](list: List[A]) {
  def >=<(f: (A, A) => A): List[A] = {
    val pairs = list.zip(list.tail)
    pairs.map(pair => f(pair._1, pair._2))
  }
}

// Przykład użycia
val nums3 = List(0, 1, 2, 3)
val combined = nums3 >=< ((a: Int, b: Int) => a + b)