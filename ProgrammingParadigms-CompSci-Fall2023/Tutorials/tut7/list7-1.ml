(* Signature *)

module type QUEUE_FUN = sig
  type 'a t
  exception Empty of string
  val empty: unit -> 'a t
  val enqueue: 'a * 'a t -> 'a t
  val dequeue: 'a t -> 'a t
  val first: 'a t -> 'a
  val isEmpty: 'a t -> bool
end
;;

(*
W tym module, kolejka jest reprezentowana 
jako zwykła lista ('a list). 
Do dodawania elementów na końcu listy używamy operatora @, 
co może być nieefektywne dla długich list.   
*)
module QueueList : QUEUE_FUN = struct
  type 'a t = 'a list
  exception Empty of string

  let empty () = []

  let enqueue (x, q) = q @ [x]

  let dequeue = function
    | [] -> raise (Empty "Queue is empty")
    | _ :: t -> t

  let first = function
    | [] -> raise (Empty "Queue is empty")
    | h :: _ -> h

  let isEmpty q = q = []
end
;;

(*
Kolejka jest reprezentowana jako para list, gdzie jedna lista przechowuje 
elementy w kolejności dodawania, a druga w odwrotnej kolejności. 
Funkcja normalize odpowiada za przekształcenie par list w sytuacji, 
gdy pierwsza lista jest pusta.   
*)
module QueuePairList : QUEUE_FUN = struct
  type 'a t = 'a list * 'a list
  exception Empty of string

  let empty () = ([], [])

  let normalize = function
    | [], r -> (List.rev r, [])
    | q -> q

  let enqueue (x, (f, r)) = normalize (f, x :: r)

  let dequeue = function
    | [], _ -> raise (Empty "Queue is empty")
    | _ :: f, r -> normalize (f, r)

  let first = function
    | [], _ -> raise (Empty "Queue is empty")
    | h :: _, _ -> h

  let isEmpty = function
    | [], [] -> true
    | _ -> false
end
;;

(* Użycie QueueList *)
let () =
  let open QueueList in

  (* Tworzenie pustej kolejki *)
  let q = empty () in

  (* Dodawanie elementów *)
  let q = enqueue (1, q) in
  let q = enqueue (2, q) in
  let q = enqueue (3, q) in

  (* Sprawdzanie, czy kolejka jest pusta *)
  let _ = Printf.printf "Is the queue empty? %b\n" (isEmpty q) in

  (* Pobieranie pierwszego elementu *)
  let first_element = first q in
  Printf.printf "First element: %d\n" first_element;

  (* Usuwanie elementu z kolejki *)
  let q = dequeue q in
  let new_first = first q in
  Printf.printf "New first element after dequeue: %d\n" new_first
;;

(* Użycie QueuePairList *)
let () =
  let open QueuePairList in

  (* Tworzenie pustej kolejki *)
  let q = empty () in

  (* Dodawanie elementów *)
  let q = enqueue (1, q) in
  let q = enqueue (2, q) in
  let q = enqueue (3, q) in

  (* Sprawdzanie, czy kolejka jest pusta *)
  let _ = Printf.printf "Is the queue empty? %b\n" (isEmpty q) in

  (* Pobieranie pierwszego elementu *)
  let first_element = first q in
  Printf.printf "First element: %d\n" first_element;

  (* Usuwanie elementu z kolejki *)
  let q = dequeue q in
  let new_first = first q in
  Printf.printf "New first element after dequeue: %d\n" new_first
;;