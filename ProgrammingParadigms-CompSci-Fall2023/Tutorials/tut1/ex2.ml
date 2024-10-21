(* Define a recursive function 'count' that takes two arguments: 'element' and 'list'. *)
let rec count (element, list) =
  (* Define an inner recursive function 'count_helper' with three arguments: 'element', 'lst', and 'acc' (accumulator). *)
  let rec count_helper element lst acc =
    (* Check if the input list 'lst' is empty. *)
    if lst = [] then
      acc (* If the list is empty, return the accumulator 'acc'. *)
    else
      (* Extract the head and tail of the list. *)
      let head = List.hd lst in
      let tail = List.tl lst in
      if head = element then
        count_helper element tail (acc + 1) (* If the head of the list is equal to the 'element', recursively call 'count_helper' with the tail of the list and increment the accumulator by 1. *)
      else
        count_helper element tail acc (* If the head is not equal to the 'element', recursively call 'count_helper' with the tail of the list without changing the accumulator. *)
  in
  count_helper element list 0 (* Start the counting process by calling 'count_helper' with 'element', 'list', and an initial accumulator of 0. *)

;;

let result = count (3, [1; 2; 3; 3; 4; 3]);; (* Call the 'count' function with 'element' 3 and a list, and store the result in the 'result' variable. *)
