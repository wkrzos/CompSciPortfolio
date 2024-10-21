(* Define a recursive function 'flatten1' that takes a list as its argument. *)
let rec flatten1 list =
  (* Check if the input list is empty. If it is, return an empty list (base case of recursion). *)
  if list = [] then
    []
  else
    (* If the list is not empty, then: *)
    let head = List.hd list in
    (* Extract the head (the first element) of the list. *)
    let tail = List.tl list in
    (* Extract the tail (the rest of the list) after removing the head. *)
    head @ flatten1 tail
    (* Concatenate the head with the recursive result on the tail. *)

(* Call the 'flatten1' function with a list of lists. *)
let result = flatten1 [[5; 6]; [1; 2; 3]; [6; 5]];;
