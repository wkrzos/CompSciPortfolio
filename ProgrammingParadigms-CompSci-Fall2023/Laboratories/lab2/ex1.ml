let cutOut a b lst =
  let rec helper acc i = function
    | [] -> List.rev acc
    | hd :: tl when i >= a && i <= b ->
      helper (hd :: acc) (i + 1) tl
    | _ :: tl ->
      helper acc (i + 1) tl
  in
  helper [] 0 lst
;;

let cutOut15 = cutOut 1 5;;
cutOut15 [1;2;3;4;5;6;7;8;9;10];;

let cutOut25 = cutOut 2 5;;
cutOut25 [1;2;3;4;5;6;7;8;9;10];;

let cutOut710 = cutOut 7 10;;
cutOut710 [1;2;3;4;5;6;7;8;9;10];;