(* Exercise 1 *)

type point2d = float * float;;

let distance ((x, y):point2d) =
   sqrt(x*.x +. y*.y)
;;

distance(5., 5.);;


(* Exercise 2 *)
(* Part1: Record type *)

type personTuple = string * string * int * string * int;; (*"name * surname * age * sex * shoeSize"*)
type partnershipTuple = personTuple * personTuple;;

let person1: personTuple = ("Maciej", "Kradziej", 32, "Male", 42);;
let person2: personTuple = ("Rysiu", "Pysiu", 35, "Male", 39);;

let biggerShoeSize((person1, person2): partnershipTuple) =
  let (_, _, _, _, shoeSize1) = person1 in
  let (_, _, _, _, shoeSize2) = person2 in
  if shoeSize1 > shoeSize2 then
    person1
  else 
    person2
;;

biggerShoeSize(person1, person2);;

(*Part: class 2*)

type personRecordType = {
  name: string;
  surname: string;
  age: int;
  sex: string;
  shoeSize: int;
}

type partnershipRecordType = {
  partner1: personRecordType;
  partner2: personRecordType;
}

let person3 = {name = "John"; surname = "Doe"; age = 25; sex = "Male"; shoeSize = 44};;
let person4 = {name = "Jane"; surname = "Doe"; age = 28; sex = "Female"; shoeSize = 38};;

let biggerShoeSize(par2 : partnershipRecordType) =
  if par2.partner1.shoeSize > par2.partner2.shoeSize then
    par2.partner1
  else
    par2.partner2
;;

let partnership34 = {partner1 = person3; partner2 = person4};;

biggerShoeSize(partnership34);;


(* Excersice 3 *)

type weekDay =
|Monday
|Tuesday
|Wednesday
|Thursday
|Friday
|Saturday
|Sunday
;;

let weekDayToString day =
  match day with
  |Monday     -> "Pon"
  |Tuesday    -> "Wt"
  |Wednesday  -> "Sr"
  |Thursday   -> "Czw"
  |Friday     -> "Pt"
  |Saturday   -> "Sob"
  |Sunday     -> "Nd"
;;

let nextDay day =
  match day with
  |Monday     -> Tuesday
  |Tuesday    -> Wednesday
  |Wednesday  -> Thursday
  |Thursday   -> Friday
  |Friday     -> Saturday
  |Saturday   -> Sunday
  |Sunday     -> Monday
;;

weekDayToString Monday;;

nextDay Monday;;


(* Exercise 4 *)

(* Polymorphic type able to hold values of any type. It consists
   of two constructors: 
   1. Just of 'a: value is present
   2. Nothing: no value
*)
type 'a maybe =
  | Just of 'a
  | Nothing
;;

let safeHead list =
  match list with
  |[]     ->  Nothing
  |hd::tl ->  Just hd
;;

safeHead [];;
safeHead [1];; (* Just 1 :D *)
safeHead ["Cause"];; (* Just Cause B) *)


(* Exercise 5 *)

type solid =
  | Cuboid of float * float * float  (* dimensions: length, width, height *)
  | Cone of float * float            (* dimensions: radius, height *)
  | Sphere of float                  (* dimension: radius *)
  | Cylinder of float * float         (* dimensions: radius, height *)
  | Torus of float * float            (* dimensions: major_radius, minor_radius *)

type solidFigure = solid option

let volume (figure : solidFigure) : float =
  match figure with
  | Some (Cuboid (length, width, height)) -> length *. width *. height
  | Some (Cone (radius, height)) -> (1. /. 3.) *. 3.14159 *. radius *. radius *. height
  | Some (Sphere radius) -> (4. /. 3.) *. 3.14159 *. radius *. radius *. radius
  | Some (Cylinder (radius, height)) -> 3.14159 *. radius *. radius *. height
  | Some (Torus (major_radius, minor_radius)) -> 2. *. 3.14159 *. minor_radius *. minor_radius *. major_radius
  | None -> 0.0
;;

let cuboid_example : solidFigure = Some (Cuboid (2.0, 3.0, 4.0))
let cone_example : solidFigure = Some (Cone (1.5, 5.0))
let sphere_example : solidFigure = Some (Sphere 2.0)
let cylinder_example : solidFigure = Some (Cylinder (1.0, 3.0))
let torus_example : solidFigure = Some (Torus (3.0, 1.0))
let no_solid_example : solidFigure = None

let cuboid_volume = volume cuboid_example
let cone_volume = volume cone_example
let sphere_volume = volume sphere_example
let cylinder_volume = volume cylinder_example
let torus_volume = volume torus_example
let no_solid_volume = volume no_solid_example


