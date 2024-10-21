(* Define a recursive function that squares each element of a list *)
let rec sqrList list =
  (* Define a helper function for the recursive process *)
  let rec sqrList_helper list =
    if list = [] then
      []
    else
      (* Square the head of the list and add it to the result list,
         then recursively process the tail of the list *)
      (List.hd list) * (List.hd list) :: sqrList_helper (List.tl list)
  in
  (* Call the helper function with the original list *)
  sqrList_helper list

(* Test the sqrList function with an example list *)
sqrList [1; 2; 3; 4; 5;]
