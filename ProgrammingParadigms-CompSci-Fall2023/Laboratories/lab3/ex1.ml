let (><) list1 list2 f =
  let rec map2 xs ys =
    match (xs, ys) with
      | [], [] -> []
      | _, [] -> []
      | [], _ -> []
      | x::xs, y::ys -> (f (x, y)) :: (map2 xs ys)
  in
  map2 list1 list2
;;

let add (x, y) = x + y;;
let subtract (x, y) = x - y;;
let multiply (x, y) = x * y;;

(* Test Cases *)

(* Test Case 1: Empty lists *)
let result_a = [] >< [];;
result_a add;;

(* Test Case 2: Lists with the same elements *)
let result_b = [1; 2; 3] >< [1; 2; 3];;
result_b add;;

(* Test Case 3: Lists with different elements *)
let result_c = [1; 2; 3] >< [4; 5; 6];;
result_c subtract;;

(* Test Case 4: Lists with mixed operations *)
let result_d = [1; 2; 3] >< [4; 5; 6];;
result_d multiply;;

(* Test Case 5: Lists with one empty list *)
let result_e = [] >< [4; 5; 6];;
result_e add;;

(* Test Case 6: Lists with one empty list *)
let result_f = [4; 5; 6] >< [];;
result_f add;;

(* Test Case 7: Lists with different lengths *)
let result_g = [1; 2; 3] >< [4; 5];;
result_g add;;