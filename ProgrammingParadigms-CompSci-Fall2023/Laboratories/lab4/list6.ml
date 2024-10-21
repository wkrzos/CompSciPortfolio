(* Solution 1 
type 'a lazyBinaryTree1 =
  | LEmpty
  | LNode of 'a * (unit -> 'a lazyBinaryTree1) * (unit -> 'a lazyBinaryTree1)
;;

let rec treeFoldL1 f acc tree =
  match tree with
  | LEmpty -> acc
  | LNode (value, leftThunk, rightThunk) ->
    let newAcc = treeFoldL1 f acc (leftThunk ()) in
    let finalAcc = f newAcc value in
    treeFoldL1 f finalAcc (rightThunk ())
;;

let lazyTreeExample =
  LNode (1,
         (fun () -> LNode (2, (fun () -> LEmpty), (fun () -> LEmpty))),
         (fun () -> LNode (3, (fun () -> LEmpty), (fun () -> LEmpty))))
;;

let sumResult = treeFoldL1 (fun acc value -> acc + value) 0 lazyTreeExample;;

*)

(* Solution 2 *)

type 'a lazyBinaryTree =
  | Empty
  | Node of 'a * 'a lazyBinaryTree Lazy.t * 'a lazyBinaryTree Lazy.t
;;

let rec treeFoldL f acc tree =
  match tree with
  | Empty -> acc
  | Node (value, left, right) ->
      let acc' = treeFoldL f acc (Lazy.force left) in
      let acc'' = f acc' value in
      treeFoldL f acc'' (Lazy.force right)
;;
       
 
(* Example 1: summation of all node values *) 

let tree1 =
  Node (1,
        lazy (Node (2, lazy Empty, lazy Empty)),
        lazy (Node (3, lazy Empty, lazy Empty))
       ) 
;;

let sum = treeFoldL (fun acc x -> acc + x) 0 tree1;; (* Expected: 6 *)
    
                                                           
(* Example 2: Counter of the number of nodes in a tree *)

let countNodes acc _ = acc + 1;;

let tree2 =
  Node (1,
        lazy (Node (2, lazy Empty, lazy Empty)),
        lazy (Node (3, lazy Empty, lazy Empty))
       )
;;

let nodeCount1 = treeFoldL countNodes 0 tree2;; (* Expected: 3 *) 
                                                

(* Example 3: Joining all Nodes into a string  *)

let concatenateValues acc x = acc ^ " " ^ string_of_int x;;

let tree3 =
  Node (1,
        lazy (Node (2, lazy Empty, lazy Empty)),
        lazy (Node (3, lazy Empty, lazy Empty))
       )
;;

let concatenatedValues2 = treeFoldL concatenateValues "" tree3;; (* Expected: " 2 1 3 " *)


