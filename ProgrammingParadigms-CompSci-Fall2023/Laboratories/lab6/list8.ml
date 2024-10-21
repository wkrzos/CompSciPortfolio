module type MEMORY = sig
  type t
  val init : int -> t
  val get : t -> int -> int option
  val set : t -> int -> int -> unit
  val dump : t -> (int * int option) list
end
;;

module ArrayMemory : MEMORY = struct
  type t = int option array

  let init size =
    Array.make size None

  let get memory address =
    Array.get memory address

  let set memory address value =
    Array.set memory address (Some value)

  let dump memory =
    Array.mapi (fun index value -> (index, value)) memory |> Array.to_list
end
;;

module ListMemory : MEMORY = struct
  type t = (int option) list ref

  let init size =
    ref (List.init size (fun _ -> None))

  let get memory address =
    List.nth !memory address

  let set memory address value =
    memory := List.mapi (fun i v -> if i = address then Some value else v) !memory

  let dump memory =
    List.mapi (fun index value -> (index, value)) !memory
end
;;

module RAMMachine (M : MEMORY) = struct
  type memory = M.t
  type instruction = Load of int * int | Add of int * int * int | Sub of int * int * int (* further instructions *)

  let initialize size program =
    (* Initialize the memory and load the program *)
    let mem = M.init size in
    mem, program

  let execute_command mem cmd =
    match cmd with
    | Load (addr, value) ->
        M.set mem addr value;
        mem
    | Add (dest, src1, src2) ->
        let value1 = match M.get mem src1 with Some v -> v | None -> 0 in
        let value2 = match M.get mem src2 with Some v -> v | None -> 0 in
        M.set mem dest (value1 + value2);
        mem
    | Sub (dest, src1, src2) ->
        let value1 = match M.get mem src1 with Some v -> v | None -> 0 in
        let value2 = match M.get mem src2 with Some v -> v | None -> 0 in
        M.set mem dest (value1 - value2);
        mem

  let run mem program =
    List.fold_left execute_command mem program

  let dump_memory mem =
    M.dump mem
end
;;

(* Create a RAM machine instance using ArrayMemory *)
(* Switch manually by commenting out one of the variables *)

(*module MyRAMMachine = RAMMachine(ArrayMemory);;*)
module MyRAMMachine = RAMMachine(ListMemory);;

(* Define a program *)
let program = [
  MyRAMMachine.Load (0, 10);         (* Load 10 into memory address 0 *)
  MyRAMMachine.Load (1, 20);         (* Load 20 into memory address 1 *)
  MyRAMMachine.Add (2, 0, 1);        (* Add values at addresses 0 and 1, store result in address 2 *)
  MyRAMMachine.Sub (3, 1, 0);        (* Subtract value at address 0 from value at address 1, store result in address 3 *)
];;

(* Initialize the RAM machine with memory size and the program *)
let memory_size = 10;;
let memory, loaded_program = MyRAMMachine.initialize memory_size program;;

(* Run the program *)
let final_memory = MyRAMMachine.run memory loaded_program;;

(* Dump the memory to see the results *)
let memory_dump = MyRAMMachine.dump_memory final_memory;;

(* Print the memory dump *)
List.iter (fun (addr, value) -> 
  Printf.printf "Address %d: %s\n" addr 
    (match value with 
     | Some v -> string_of_int v 
     | None -> "None")
) memory_dump;;