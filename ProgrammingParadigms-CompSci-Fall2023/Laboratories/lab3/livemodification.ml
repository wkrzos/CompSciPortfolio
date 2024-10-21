(* 
Napsiz operator >=<. Ma on przyjmować jedną listę elementów 
oraz funkcję.  Ma być on w formie rozwiniętej. Funkcja ma zwrócić listę, taką, że
pierwszy element łączy się z drugim, drugi z trzecim, trzeci z czwartym, itd.
Implementację oprzyj o funkcjonały, bez rekurencji. 

insert, sigma, map, filter, fold_left, fold_right

tak, że funkcja bierze pierwszy element z drugim, 
drugi z trzecim, trzci z czwartym, funkcja ma być w formie rozwiniętej, 
oprzyj implementację bez rekurencji, wykrozystaj funkcjonały
*)

(* Solution 1 *)
let ( >=< ) list f =
  let pairs = List.combine list (List.tl list) in
  List.map (fun (a, b) -> f a b) pairs;;

let nums1 = [1; 2; 3; 4];;
let combined1 = nums1 >=< (fun a b -> a + b);;

let nums2 = [0; 1; 2; 3; 4; 5; 6];;
let combined2 = nums2 >=< (fun a b -> a - b);;