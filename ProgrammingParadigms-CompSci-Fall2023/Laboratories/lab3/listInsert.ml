let isPreceding elem head =
  match (elem, head) with
  | (x, y) when x = y -> true
  | _ -> false
  (*or simply elem = head*)
;;

let rec insert isPreceding elem xs =
  match xs with
    | [] -> [elem]
    | h::t as ys -> 
      if isPreceding elem h then 
        elem::ys
      else
        h::(insert isPreceding elem t);;
;;

insert isPreceding 4 [1;2;3;4;5];;