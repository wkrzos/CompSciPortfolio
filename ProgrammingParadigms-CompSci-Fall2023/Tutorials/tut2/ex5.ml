let rec initSegment (list1, list2) =
  match (list1, list2) with
  | ([], _) -> true  (* If 'list1' is empty, it's an initial segment of any list. *)
  | (_, []) -> false  (* If 'list2' is empty, it's not an initial segment of 'list1'. *)
  | (x :: xs, y :: ys) when x = y -> initSegment (xs, ys)
  | _ -> false
;;

(*
The function operates by pattern matching on the two input lists, list1 and list2. In the best case, if list1 is empty, it immediately returns true, which is an O(1) operation. In the worst case, the function needs to traverse both lists until it reaches the end of either list or finds a mismatch. This can take O(min(N, M)) time, where N is the length of list1, and M is the length of list2   
*)

(* Test cases *)

initSegment ([], [1; 2; 3]);;  (* Expect: true, an empty list is an initial segment of any list. *)
initSegment ([1; 2; 3], []);;  (* Expect: false, an empty list cannot be an initial segment of a non-empty list. *)
initSegment ([1], [1; 2; 3]);;  (* Expect: true, [1] is an initial segment of [1; 2; 3]. *)
initSegment ([1; 2; 3], [1]);;  (* Expect: false, [1; 2; 3] is not an initial segment of [1]. *)
initSegment ([1; 2], [1; 2; 3; 4]);;  (* Expect: true, [1; 2] is an initial segment of [1; 2; 3; 4]. *)
initSegment ([1; 2; 4], [1; 2; 3; 4]);;  (* Expect: false, [1; 2; 4] is not an initial segment of [1; 2; 3; 4]. *)
initSegment (["a"; "b"], ["a"; "b"; "c"]);;  (* Expect: true, ["a"; "b"] is an initial segment of ["a"; "b"; "c"]. *)
initSegment (["a"; "b"; "d"], ["a"; "b"; "c"]);;  (* Expect: false, ["a"; "b"; "d"] is not an initial segment of ["a"; "b"; "c"]. *)
initSegment (["x"; "y"; "z"], ["x"; "y"; "z"]);;  (* Expect: true, ["x"; "y"; "z"] is an initial segment of itself. *)
initSegment ([1; 2; 3; 4], [1; 2; 3; 4]);;  (* Expect: true, [1; 2; 3; 4] is an initial segment of itself. *)
initSegment ([1; 2; 3; 4], [1; 2; 3]);;  (* Expect: false, [1; 2; 3; 4] is not an initial segment

(* 

Expected O() complexity 

The time complexity of the `initSegment` function can be analyzed as follows:

1. The function is a recursive function that takes two lists, `list1` and `list2`, as input.

2. In each recursive call, the function pattern matches on the two input lists, which involves checking the length and comparing the first elements.

3. There are four cases in the pattern matching:
   a. If `list1` is empty, the function returns `true`.
   b. If `list2` is empty, the function returns `false`.
   c. If the first elements of `list1` and `list2` are equal, the function makes a recursive call with the tails of both lists (i.e., `initSegment (xs, ys)`).
   d. In all other cases, the function returns `false`.

4. In the worst case, the function will have to traverse both lists completely to determine if one is an initial segment of the other.

The time complexity of this function can be analyzed as O(min(n, m)), where "n" is the length of `list1` and "m" is the length of `list2`. This is because the function will need to check a minimum of the length of the shorter list. In the worst case, if one list is a prefix of the other, it will have to traverse both lists, but it will not have to examine elements beyond the length of the shorter list.

In big O notation, O(min(n, m)) simplifies to O(min(n, m)).

So, the time complexity of the `initSegment` function is O(min(n, m)), where "n" is the length of `list1` and "m" is the length of `list2`.

*)