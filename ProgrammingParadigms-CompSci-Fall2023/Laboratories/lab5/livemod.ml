(* gen fib number *)
let fibonacci n =
  if n <= 0 then 0
  else if n = 1 || n = 2 then 1
  else
    let a = ref 1 in
    let b = ref 1 in
    let sum = ref 0 in
    for i = 3 to n do
      sum := !a + !b;
      a := !b;
      b := !sum
    done;
    !sum
;;

(* gen fib series with fibbonachi fun *)
let fibonacci_series n =
  let series = Array.make n 0 in
  for i = 0 to n - 1 do
    series.(i) <- fibonacci (i + 1)
  done;
  series
;;

(*  *)
let generate_imperative_skipponachi m n =
  if m = 1 then fibonacci_series n
  else
    let result = Array.make n 0 in
    for i = 0 to n - 1 do
      result.(i) <- fibonacci (2 * i + 2 * m - 1) + fibonacci (2 * i + 2 * m - 2)
    done;
    result
;;

(* Wygenerowac duza tablice, polaczc dwa, potem w tej polaczyc dwa. Obciac tablice. *)

(* Test the function with various inputs *)
let () =
  let print_array arr =
    let strs = Array.map string_of_int arr in
    Printf.printf "Array(%s)\n" (String.concat ", " (Array.to_list strs))
  in
  print_array (generate_imperative_skipponachi 1 0);
  print_array (generate_imperative_skipponachi 1 1);
  print_array (generate_imperative_skipponachi 1 2);
  print_array (generate_imperative_skipponachi 1 3);
  print_array (generate_imperative_skipponachi 2 15);
  print_array (generate_imperative_skipponachi 3 15);
  print_array (generate_imperative_skipponachi 4 15);
  print_array (generate_imperative_skipponachi 5 15)
;;