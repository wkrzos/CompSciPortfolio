"Hello World";;

"Hello" ^ "World";;

let x = 7;;

x = 13;; 
(** We get a boolean*)

let x = 13;;

x + 7;;

2.5 +. 1.4;;

float_of_int x +. 2.5;;
(* x +. 2.5;;*) 
(** We get an exception, one of the vars is an int, the other is a double*)

(** ===== LEARNING FUNCTIONS =====*)
let f = function  x -> x *. x +. 1.0;;
f 15.;;

(*Two arguments fucntions*)
let g = function pair -> 
  let x = fst pair
  and y = snd pair
in x *. x +. y *. y;; 

g (10. , 10.);;

let h = function (x, y) -> x *. x +. y *. y;;

h (10. , 10.);;

(* ===== LEARNING LOOPS =====*)
let rec factorial n = 
  if n = 0 then 1 else n * factorial (n - 1);;

let rec fact = function n -> if n<=1 then 1 else n * fact (n-1);;