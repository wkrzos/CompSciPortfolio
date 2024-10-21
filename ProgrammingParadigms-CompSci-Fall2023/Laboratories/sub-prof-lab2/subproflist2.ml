(* Stirling with no memoisation *)
let rec stirling = function
  | (0,0) -> 1
  | (_, 1) -> 1
  | (_, 0) -> 0
  | (n,m) when n = m -> 1
  | (n,m) -> stirling(n-1,m-1) + m * stirling(n - 1, m);;

type nm = int * int;;
  
let memoised_stirling =
  let memo = Hashtbl.create 100 in
  let stirling' (arg: nm) =
    if Hashtbl.mem memo arg then Hashtbl.find memo arg else
      let value = stirling arg in
      Hashtbl.add memo arg value;
      value 
  in
  stirling';;

memoised_stirling (40, 9);;

let make_memoise f = 
  let memo = Hashtbl.create 10 in
  let f' args =
  if Hashtbl.mem memo args then Hashtbl.find memo args else
    let value = f args in
    Hashtbl.add memo args value;
    value 
in
f';;

(* test *)
let stirling_value = lazy (stirling (40,9));;
print_int (Lazy.force stirling_value);;