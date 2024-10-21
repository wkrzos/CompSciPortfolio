(* Define a recursive function 'split3Rec' that takes a list as input and splits it into three lists.
The base case is an empty list, which returns three empty lists.
For non-empty lists, it recursively splits the list into groups of three elements. *)
let rec split3Rec list =
  match list with
  | [] -> ([], [], [])  (* Base case: an empty list, return three empty lists *)
  | elem1 :: elem2 :: elem3 :: tail -> 
    let (list1, list2, list3) = split3Rec tail in
    (elem1 :: list1, elem2 :: list2, elem3 :: list3)  (* Recursively split the list into three parts *)
  | _ -> ([], [], [])  (* Incomplete group, return three empty lists *)
;;
  
(* Define a tail-recursive function 'split3Tail' that takes a list as input and splits it into three lists.
It uses an auxiliary tail-recursive function 'split3TailRec' with accumulators to build the result lists. *)
let split3Tail list =
  let rec split3TailRec (list, list1, list2, list3) =

    match list with
    | [] -> (list1, list2, list3)  (* Base case: an empty list, return the accumulated lists *)
    | elem1 :: elem2 :: elem3 :: tail ->
      split3TailRec (tail, elem1 :: list1, elem2 :: list2, elem3 :: list3)  (* Accumulate elements into lists *)
    | _ -> (list1, list2, list3)  (* Incomplete group, return the accumulated lists *)
    in

  split3TailRec (list, [], [], [])  (* Start the tail-recursive process with empty accumulators *)
;;
  


split3Rec [1; 2; 3; 4; 5; 6; 7; 8; 9];;
split3Rec [1; 2; 3; 4; 5; 6; 7; 8; 9; 10];;
split3Rec ["a"; "b"; "c"; "d"; "e"; "f"; "g"; "h"; "i"];;
split3Rec [];;

split3Tail [1; 2; 3; 4; 5; 6; 7; 8; 9];;
split3Tail [1; 2; 3; 4; 5; 6; 7; 8; 9; 10];;
split3Tail ["a"; "b"; "c"; "d"; "e"; "f"; "g"; "h"; "i"];;
split3Tail [];;