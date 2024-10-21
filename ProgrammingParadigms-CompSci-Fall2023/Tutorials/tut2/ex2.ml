let rec fib n =
  if n = 0 then 0
  else if n = 1 then 1
  else fib (n - 1) + fib (n - 2)
;;

let fibTail n =
  let rec fibTail' n a b =
    if n = 0 then
      a
    else
      fibTail' (n - 1) b (a + b)
  in fibTail' n 0 1
;;

fib 45;;

fibTail 45;;

(*
fib (Standard Recursive):
This implementation uses a simple recursive approach to calculate Fibonacci numbers. It has exponential time complexity, O(2^n), because it repeatedly calls the fib function twice for each value of n, resulting in a large number of redundant calculations. The space complexity is O(n) because it requires a call stack of depth n.

fibTail (Tail Recursive):
This implementation is a tail-recursive version of the Fibonacci function. It uses an accumulator (a) and a current Fibonacci value (b) to avoid redundant calculations. The time complexity of this function is linear, O(n), as it iterates through the numbers from 0 to n with a single tail-recursive call. The space complexity is O(1) because it doesn't require a call stack of significant depth; it uses constant space due to the tail-recursive optimization.   
*)