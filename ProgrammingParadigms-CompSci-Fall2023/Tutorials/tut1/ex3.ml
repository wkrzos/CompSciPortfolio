(* Define a recursive function 'replicate' that takes an element and the number of times to replicate it *)
let rec replicate (element, times) =
  (* Define a helper function 'replicate_helper' that replicates the element 'times' times and accumulates the result in 'table' *)
  let rec replicate_helper element times table =
    if times = 0 then
      table  (* If 'times' is zero, return the accumulated 'table' as the result (base case) *)
    else
      replicate_helper element (times - 1) (element :: table)  (* Recursively call 'replicate_helper' with one less 'times' and add 'element' to 'table' *)
  in
  replicate_helper element times []  (* Initialize the helper function with 'element', 'times', and an empty 'table' *)

(* Test the replicate function by replicating the element "Ha" five times *)
replicate ("Ha", 5);;
