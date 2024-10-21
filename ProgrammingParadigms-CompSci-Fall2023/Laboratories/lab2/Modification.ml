(*Modification*)
(*mod: napisz funkcję reverseDelete. Dochodzę do ntej pozycji i ją usuwam. Reszta listy ma być odwrócona, początek bez zmian idzie na koniec. Dopasowanie do wzorca, rekurencja, może ogonowa. Napisane tak jak cutOut, że można np. cutOut15.*)

(* Solution 1 *)
let reverseDelete n list =
  let rec helper lst i = 
    match (lst, i) with 
    | (hd :: tl, i ) when i < n ->
        let (acc_ret, result) = helper (tl) (i+1) in
        if acc_ret = [] then ([], result) else (List.tl acc_ret, List.hd acc_ret :: result)
    | (lst, i) when i = n -> (list, List.tl lst)
    | (lst, _) -> (list, lst)
    | _ -> (list, []) in
  let (_, res) = helper list 0 in
  res
;;

let result = reverseDelete 3 [0; 1; 2; 3; 4; 5; 6];;

let reverseDelete4 = reverseDelete 4;;
reverseDelete4 [0; 1;2;3;4;5;6];;

(* Solution 2 *)
let reverseDelete n input_list =
  let rec accumulate_and_reverse acc count = function
    | [] -> acc
    | hd :: tl when count < n -> accumulate_and_reverse (hd :: acc) (count + 1) tl
    | hd :: tl -> hd :: accumulate_and_reverse acc (count + 1) tl
  in

  let reversed_list = accumulate_and_reverse [] 0 input_list in

  let rec delete_nth count acc = function
    | [] -> acc
    | _ :: tl when count = n -> List.rev_append acc tl
    | hd :: tl -> delete_nth (count + 1) (hd :: acc) tl
  in

  delete_nth 0 [] reversed_list
;;

let result = reverseDelete 3 [1; 2; 3; 4; 5; 6];;
let result2 = reverseDelete 3 [1; 2; 3; 4; 5; 6; 7; 8; 9; 10];;
let result3 = reverseDelete 3 [6;5;4;3;2;1]

(* Solution 2 *)

(*Delete*)
let _Delete n lst =
  let rec helper acc i = function
    | [] -> List.rev acc
    | hd :: tl when i < n - 1 -> List.rev  (* Accumulate elements before the deletion point *)
    | hd :: tl when i = n - 1 -> helper acc (i + 1) tl          (* Skip the element at the deletion point *)
    | hd :: tl when i > n - 1 -> helper (hd :: acc) (i + 1) tl  (* Accumulate elements after the deletion point *)
  in
  helper [] 0 lst
;;

(* Example usage: *)
let result = _Delete 3 [1; 2; 3; 4; 5];;


let _Delete3 = _Delete 3;;
_Delete3 [1;2;3;4;5;6;7;8;9;10];;

(*Reverse list*)
let reverse_list lst =
  let rec aux acc lst =
    match lst with
    | [] -> acc
    | head :: tail -> aux (head :: acc) tail
  in
  aux [] lst
;;

let my_list = [1; 2; 3; 4; 5];;
let reversed_list = reverse_list my_list;;

(* Both, bug fixes needed *)
let reverseDelete2 n lst =
  let rec reverse acc = function
    | [] -> acc
    | hd :: tl -> reverse (hd :: acc) tl
  in
  let rec helper acc i = function
    | [] -> List.rev acc
    | hd :: tl when i = n - 1 -> helper acc (i + 1) tl
    | hd :: tl -> helper (reverse [] (hd :: acc)) (i + 1) tl
  in
  match helper [] 0 lst with
  | [] -> []
  | _ :: tl -> tl
;;

let reverseDelete3 = reverseDelete2 3;;
let result = reverseDelete3 [1; 2; 3; 4; 5; 6; 7; 8; 9; 10];;
