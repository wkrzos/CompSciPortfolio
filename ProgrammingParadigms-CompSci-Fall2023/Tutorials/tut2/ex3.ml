let root3 a =
  let e = 1e-15 in  (* Precision constant *)
  if a < 0.0 then
    invalid_arg "Input number must be non-negative"
  else if a = 0.0 then
    0.0
  else
    let rec root3' x =
      let next_x = x +. ((a /. (x *. x) -. x) /. 3.0) in
      if abs_float (x *. x *. x -. a) <= e *. abs_float a then x
      else root3' next_x
    in
    root3' a
;;

root3 0.1;;

(*
The primary work in this function is done by the root3' helper function, which uses an iterative approach to approximate the cube root. The number of iterations required depends on the precision constant e and the initial guess. Generally, the Newton-Raphson method converges quickly, and the number of iterations is logarithmic in practice. Therefore, we can approximate the time complexity as O(log(1/e)), where e is the precision constant.   
*)