(* Signature *)

module type QUEUE_MUT = sig
  type 'a t
  (* The type of queues containing elements of type ['a]. *)
  
  exception Empty of string
  (* Raised when [first q] is applied to an empty queue [q]. *)

  exception Full of string
  (* Raised when [enqueue (x, q)] is applied to a full queue [q]. *)

  val empty: int -> 'a t
  (* [empty n] returns a new queue of length [n], initially empty. *)

  val enqueue: 'a * 'a t -> unit
  (* [enqueue (x, q)] adds the element [x] at the end of a queue [q]. *)

  val dequeue: 'a t -> unit
  (* [dequeue q] removes the first element in queue [q]. *)

  val first: 'a t -> 'a
  (* [first q] returns the first element in queue [q] without removing it from the queue, 
     or raises [Empty] if the queue is empty. *)

  val isEmpty: 'a t -> bool
  (* [isEmpty q] returns [true] if queue [q] is empty, otherwise returns [false]. *)

  val isFull: 'a t -> bool
  (* [isFull q] returns [true] if queue [q] is full, otherwise returns [false]. *)
end
;;

(* Implementation *)
module CircularArrayQueue : QUEUE_MUT = struct
  type 'a t = {
    mutable arr: 'a option array;
    mutable front: int;
    mutable rear: int;
    mutable size: int;
    capacity: int
  }

  exception Empty of string
  exception Full of string

  let empty n = {
    arr = Array.make n None;
    front = 0;
    rear = 0;
    size = 0;
    capacity = n
  }

  let isFull q = q.size = q.capacity
  let isEmpty q = q.size = 0

  let enqueue (x, q) =
    if isFull q then
      raise (Full "Queue is full")
    else begin
      q.arr.(q.rear) <- Some x;
      q.rear <- (q.rear + 1) mod q.capacity;
      q.size <- q.size + 1
    end

  let dequeue q =
    if isEmpty q then
      raise (Empty "Queue is empty")
    else begin
      q.arr.(q.front) <- None;
      q.front <- (q.front + 1) mod q.capacity;
      q.size <- q.size - 1
    end

  let first q =
    if isEmpty q then
      raise (Empty "Queue is empty")
    else match q.arr.(q.front) with
      | Some x -> x
      | None -> failwith "Unexpected: Empty slot at front of queue"
end
;;

(* Example usage *)
(* Zaimportowanie modułu *)
open CircularArrayQueue

let () =
  (* Tworzenie nowej kolejki o pojemności 5 *)
  let queue = empty 5 in

  (* Dodawanie elementów do kolejki *)
  enqueue (1, queue);
  enqueue (2, queue);
  enqueue (3, queue);

  (* Sprawdzenie, czy kolejka jest pełna *)
  Printf.printf "Is the queue full? %b\n" (isFull queue);

  (* Usuwanie elementu z kolejki *)
  dequeue queue;

  (* Sprawdzenie, jaki jest teraz pierwszy element *)
  let first_element = first queue in
  Printf.printf "First element in the queue: %d\n" first_element;

  (* Sprawdzenie, czy kolejka jest pusta *)
  Printf.printf "Is the queue empty? %b\n" (isEmpty queue);

  (* Dodawanie kolejnego elementu *)
  enqueue (4, queue);

  (* Sprawdzenie stanu kolejki *)
  Printf.printf "Is the queue full? %b\n" (isFull queue);
  Printf.printf "Is the queue empty? %b\n" (isEmpty queue);
