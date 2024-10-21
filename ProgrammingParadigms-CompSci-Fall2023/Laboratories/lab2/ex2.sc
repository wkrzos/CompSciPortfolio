// Define a recursive function 'split3Rec' that takes a list as input and splits it into three lists.
// The base case is an empty list, which returns three empty lists.
// For non-empty lists, it recursively splits the list into groups of three elements.
def split3Rec[A](list: List[A]): (List[A], List[A], List[A]) = {
    list match {
        case Nil => (Nil, Nil, Nil) // Base case: an empty list, return three empty lists
        case elem1 :: elem2 :: elem3 :: tail =>
        val (list1, list2, list3) = split3Rec(tail)
        (elem1 :: list1, elem2 :: list2, elem3 :: list3) // Recursively split the list into three parts
        case _ => (Nil, Nil, Nil) // Incomplete group, return three empty lists
    }
}

// Define a tail-recursive function 'split3Tail' that takes a list as input and splits it into three lists.
// It uses an auxiliary tail-recursive function 'split3TailRec' with accumulators to build the result lists.
def split3Tail[A](list: List[A]): (List[A], List[A], List[A]) = {
    def split3TailRec(list: List[A], list1: List[A], list2: List[A], list3: List[A]): (List[A], List[A], List[A]) = {
        list match {
        case Nil => (list1, list2, list3) // Base case: an empty list, return the accumulated lists
        case elem1 :: elem2 :: elem3 :: tail =>
            split3TailRec(tail, elem1 :: list1, elem2 :: list2, elem3 :: list3) // Accumulate elements into lists
        case _ => (list1, list2, list3) // Incomplete group, return the accumulated lists
        }
    }

    split3TailRec(list, Nil, Nil, Nil) // Start the tail-recursive process with empty accumulators
}


split3Rec List(1, 2, 3, 4, 5, 6, 7, 8, 9)
split3Rec List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
split3Rec List("a", "b", "c", "d", "e", "f", "g", "h", "i")

split3Tail List(1, 2, 3, 4, 5, 6, 7, 8, 9)
split3Tail List(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
split3Tail List("a", "b", "c", "d", "e", "f", "g", "h", "i")
