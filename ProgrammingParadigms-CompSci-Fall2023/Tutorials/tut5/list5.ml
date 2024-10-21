let rec lrepeat k lxs =
  match lxs with
  | LazyList.Nil -> LazyList.Nil
  | LazyList.Cons(x, xs) -> LazyList.concat (LazyList.from_fun (fun () -> LazyList.take k (LazyList.repeat x))) (fun () -> lrepeat k (LazyList.force xs))
;;

let rec lfib =
  let rec fib a b =
    LazyList.Cons(a, fun () -> fib b (a + b))
  in
  fib 0 1
;;

type 'a lBT = LEmpty | LNode of 'a * (unit -> 'a lBT) * (unit -> 'a lBT);;

let rec lBreadth ltree =
  let rec breadth_queue queue =
    match queue with
    | [] -> LazyList.Nil
    | LEmpty :: rest -> breadth_queue rest
    | LNode (x, left, right) :: rest ->
        LazyList.Cons(x, fun () -> breadth_queue (rest @ [left (); right ()]))
  in
  breadth_queue [ltree]
;;