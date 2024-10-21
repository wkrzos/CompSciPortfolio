def fib(x: Int): Int =
  if x == 0 then
    0
  else if x == 1 then
    1
  else fib (x - 2) + fib (x - 1)

def fibTail(n: Int): Int =
    def fibTailHelper(n: Int, a: Int, b: Int): Int =
        if n == 0 then
            a
        else
            fibTailHelper(n - 1, b, a + b)

    if n <= 1 then
      n
    else
      fibTailHelper(n, 0, 1)

fib(45)
fibTail(45)