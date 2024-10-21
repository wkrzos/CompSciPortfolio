let rec palindrome list =
  (* Define a recursive function to reverse a list *)
  let rec reverse_list list =
    if list = [] then
      [] (* If the list is empty, return an empty list (base case) *)
    else
      reverse_list (List.tl list) @ [List.hd list] (* Reverse the tail and append the head to it *)
  in
  list = reverse_list list;; (* Check if the input list is equal to its reverse *)

(* Test the palindrome function with some example lists *)
palindrome [1; 2; 3; 2; 1];; (* Should return true, as this list is a palindrome *)
palindrome [1; 2; 3; 4; 5];; (* Should return false, as this list is not a palindrome *)
