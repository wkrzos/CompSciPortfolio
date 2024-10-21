(* Exercise 1 *)

let reverse4 = function (x, y, z, w) -> (w, z, y, x);;

let test_reverse4 () =
  (* Test 1: Standard element reversal *)
  let result1 = reverse4 (0, 1, 2, 3) in
  assert (result1 = (3, 2, 1, 0));;

  (* Test 2: Reversing elements with values of 0 *)
  let result2 = reverse4 (0, 0, 0, 0) in
  assert (result2 = (0, 0, 0, 0));;

  (* Test 3: Reversing elements with negative values *)
  let result3 = reverse4 (-1, -2, -3, -4) in
  assert (result3 = (-4, -3, -2, -1));;

  (* Test 4: Reversing elements with different types *)
  let result4 = reverse4 (1.0, true, 1, "A") in
  assert (result4 = ("A", 1, true, 1.0));;

  (* Test 5: Reversing elements with different types *)
  let result5 = reverse4 (1.5, "Hello", 'c', 42) in
  assert (result5 = (42, 'c', "Hello", 1.5));;

(* Running the tests *)
let () =
  test_reverse4 ();
  print_endline "All tests passed.";;

(* Exercise 2 *)

let sumRange = fun (start, end_) ->
  let rec aux acc current =
    if current > end_ - 1 then acc
    else aux (acc + current) (current + 1)
  in aux 0 start
;;

let prodRange = fun (start, end_) ->
  let rec aux acc current =
    if current > end_ - 1 then acc
    else if start = 0 then 0
    else aux (acc * current) (current + 1)
  in
  if start = 0 then 0
  else aux 1 start
;;

let sumProd = fun (start, end_) ->
  let sumOfRange = sumRange (start, end_) in
  let prodOfRange = prodRange (start, end_) in
  (sumOfRange, prodOfRange)
;;

let test_sumProd() = 
  (* Test 1: Positive numbers *)
  let result1 = sumProd (1, 5) in
  assert (result1 = (10, 24));;

  (* Test 2: Only zeros *)
  let result2 = sumProd (0, 0) in
  assert (result2 = (0, 0));;

  (* Test 3: Negative numbers with an even number of factors *)
  let result3 = sumProd (-4, 0) in
  assert (result3 = (-10, 24));;

  (* Test 4: Negative numbers with an odd number of factors *)
  let result4 = sumProd (-4, -1) in
  assert (result4 = (-9, -24));;

  (* Test 5: Range from negative to positive *)
  let result5 = sumProd (-4, 5) in
  assert (result5 = (0, 0));;

(* Run the tests *)
let () =
  test_sumProd ();
  print_endline "All tests passed.";;

(* Exercise 3 *)

  let isPerfect n =
    let rec sum_divisors i sum =
      if i = 0 then
        sum (* If we have checked all divisors, return the sum. *)
      else if n mod i = 0 then
        sum_divisors (i - 1) (sum + i) (* If 'i' is a divisor, add it to the sum. *)
      else
        sum_divisors (i - 1) sum (* If 'i' is not a divisor, continue without adding it to the sum. *)
    in
    let sum = sum_divisors (n - 1) 0 in (* Start checking divisors from n - 1 and initialize sum to 0. *)
    sum = n (* Check if the computed sum is equal to 'n' to determine if 'n' is a perfect number. *)
  ;;
  

(* Tests *)

let test_isPerfect () =
  (* Test 1: 6 is a perfect number *)
  let result1 = isPerfect 6 in
  assert (result1 = true);;

  (* Test 2: 28 is a perfect number *)
  let result2 = isPerfect 28 in
  assert (result2 = true);;

  (* Test 3: 12 is not a perfect number *)
  let result3 = isPerfect 12 in
  assert (result3 = false);;

  (* Test 4: 496 is a perfect number *)
  let result4 = isPerfect 496 in
  assert (result4 = true);;

  (* Test 5: 7 is not a perfect number *)
  let result5 = isPerfect 7 in
  assert (result5 = false);;

(* Run the tests *)
let () =
  test_isPerfect ();;
  print_endline "All tests passed.";;

(* Exercise 4 *)

let insert list node position =
  let rec aux lst elem pos =
    if pos = 0 then
      elem :: lst  (* If 'pos' is 0, insert 'elem' at the beginning of the list. *)
    else if lst = [] then
      [elem]  (* If 'lst' is empty, create a new list with just 'elem'. *)
    else if pos <= 0 then
      elem :: lst  (* If 'pos' is less than or equal to 0, insert 'elem' at the beginning of the list. *)
    else
      if lst <> [] then
        let hd, tl = List.hd lst, List.tl lst in
        hd :: (aux tl elem (pos - 1))  (* If none of the above conditions match, recursively insert 'elem' in the tail of the list. *)
      else
        []  (* If 'lst' is empty (an edge case), return an empty list. *)
  in aux list node position  (* Call the 'aux' function with the input 'list', 'node', and 'position'. *)
;;


let test_insert() =
  (* Test 1: Inserting an element at the beginning of an empty list *)
  let result1 = insert [] "A" 0 in
  assert (result1 = ["A"]);;

  (* Test 2: Inserting an element at the beginning of a non-empty list *)
  let result2 = insert ["B"; "C"] "A" 0 in
  assert (result2 = ["A"; "B"; "C"]);;

  (* Test 3: Inserting an element at the end of the list *)
  let result3 = insert ["A"; "B"] "C" 2 in
  assert (result3 = ["A"; "B"; "C"]);;

  (* Test 4: Inserting an element out of the list's range - it should land at the end *)
  let result4 = insert ["A"; "B"] "C" 10 in
  assert (result4 = ["A"; "B"; "C"]);;

  (* Test 5: Inserting an element at the first position (index 1) *)
  let result5 = insert ["A"; "B"; "C"] "X" 1 in
  assert (result5 = ["A"; "X"; "B"; "C"]);;

  (* Test 6: Inserting an element at the middle position (index 2) *)
  let result6 = insert ["A"; "B"; "C"] "Y" 2 in
  assert (result6 = ["A"; "B"; "Y"; "C"]);;

  (* Test 7: Inserting an element at the penultimate position (index 2) *)
  let result7 = insert ["A"; "B"; "C"] "Z" 2 in
  assert (result7 = ["A"; "B"; "Z"; "C"]);;

  (* Test 8: Inserting an element at the end of the list where the position equals the list's length *)
  let result8 = insert ["A"; "B"; "C"] "D" 3 in
  assert (result8 = ["A"; "B"; "C"; "D"]);;

  (* Test 9: Inserting an element at the beginning of the list when the position is negative *)
  let result9 = insert ["B"; "C"] "A" (-1) in
  assert (result9 = ["A"; "B"; "C"]);;

  (* Test 10: Inserting an element at the second position when the position is negative *)
  let result10 = insert ["A"; "C"] "B" (-2) in
  assert (result10 = ["B"; "A"; "C"]);;

  (* Test 11: Inserting an element at the end of the list when the position is highly negative *)
  let result11 = insert ["A"; "B"] "C" (-10) in
  assert (result11 = ["C"; "A"; "B"]);;

(* Run the tests *)
let () =
  test_insert ();;
  print_endline "All tests passed.";;

(* Live Coding 1 *)

let rec choice list1 list2 =
  if list1 = [] && list2 = [] then
    []
  else if list2 = [] then
    list1
  else if list1 = [] then
    list2
  else
    let hd1, tl1 = List.hd list1, List.tl list1 in
    let hd2, tl2 = List.hd list2, List.tl list2 in
    let max_element = if hd1 > hd2 then hd1 else hd2 in
    max_element :: choice tl1 tl2
;;

let test_choice () =
  (* Test 1: Both lists are empty *)
  let result1 = choice [] [] in
  assert (result1 = []);

  (* Test 2: First list is empty *)
  let result2 = choice [] [1; 2; 3] in
  assert (result2 = [1; 2; 3]);

  (* Test 3: Second list is empty *)
  let result3 = choice [4; 5; 6] [] in
  assert (result3 = [4; 5; 6]);

  (* Test 4: Lists have the same elements at corresponding positions *)
  let result4 = choice [1; 2; 3] [4; 5; 6] in
  assert (result4 = [4; 5; 6]);

  (* Test 5: Lists have different elements at corresponding positions *)
  let result5 = choice [5; 3; 8] [4; 6; 2] in
  assert (result5 = [5; 6; 8]);

  (* Test 6: Second list is longer than the first one *)
  let result6 = choice [1; 2] [3; 4; 5] in
  assert (result6 = [3; 4; 5]);

  (* Test 7: First list is longer than the second one *)
  let result7 = choice [1; 2; 3; 4; 5] [6; 7] in
  assert (result7 = [6; 7; 3; 4; 5]);

  (* Test 8: Lists have the same elements but different lengths *)
  let result8 = choice [1; 2; 3] [4; 5] in
  assert (result8 = [4; 5; 3]);

;;

(* Run the tests *)
let () =
  test_choice ();;
  print_endline "All tests passed.";;

(* Live Coding 2 *)

(*Napisać funkcję squish przyjmującą listę list i zwracającą listę składającą się z elementów 
tychże list, w kolejności występowania. (OCaml i Scala)*)

let squash list =
  let rec squash_helper currList remainingLists =
    if currList = [] then
      if remainingLists = [] then
        []  (* If currList is empty and no remainingLists, return an empty list. *)
      else
        squash_helper (List.hd remainingLists) (List.tl remainingLists) (* Recursively call squash_helper with the head of remainingLists. *)
    else
      List.hd currList :: squash_helper (List.tl currList) remainingLists
      (* If currList is not empty, take the head of currList and recursively call squash_helper with the tail of currList. *)
  in

  if list = [] then
    []
  else
    squash_helper (List.hd list) (List.tl list) (* Call squash_helper with the head of the input list and its tail. *)
;;

let test_squash() =
  (* Test 1: Squashing an empty list *)
  let result1 = squash [] in
  assert (result1 = []);

  (* Test 2: Squashing a list with one element *)
  let result2 = squash [[1]] in
  assert (result2 = [1]);

  (* Test 3: Squashing a list with two elements *)
  let result3 = squash [[1]; [2]] in
  assert (result3 = [1; 2]);

  (* Test 4: Squashing a list with three elements *)
  let result4 = squash [[1]; [2]; [3]] in
  assert (result4 = [1; 2; 3]);

  (* Test 5: Squashing a list with three elements *)
  let result5 = squash [[1; 2]; [3; 4]; [5; 6]] in
  assert (result5 = [1; 2; 3; 4; 5; 6]);

  ;;

(* Run the tests *)
let () =
  test_squash ();;
  print_endline "All tests passed.";;