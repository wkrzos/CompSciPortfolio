(* Define a recursive function 'listLength' that takes a list as its argument. *)
let rec listLength list =
  (* Check if the list is empty. If it is, return 0, indicating the length is 0. *)
  if list = [] then
    0
  else
    (* If the list is not empty, add 1 to the length of the list obtained by calling 'listLength' recursively on the tail of the list (List.tl list). *)
    1 + listLength (List.tl list)
  ;;

(* Call the 'listLength' function with the list [1;2;3;4;5] to calculate its length. *)
listLength [1;2;3;4;5];;  (* This will return the result of the length, which is 5 in this case. *)
