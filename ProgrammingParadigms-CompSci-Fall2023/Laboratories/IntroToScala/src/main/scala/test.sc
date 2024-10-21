"Hello World"

val x = 7

x == 13

//Learning functions f(x) = x^2 + 1
val f = (x:Double) => x * x + 1
f(15)

def g(x:Double) = x * x + 1
g(15)
//The difference between those two approaches
//will be further explained during the lecture.

//Learning functions

def h(x:Double, y:Double) = {
  val sum = x + y
  if x < y then sum
  else - sum
}

val g = (xy: (Double, Double)) => x

//Polymorphic function
def f[T](x:T) = x
f("Hello")
f(10)

val h = [T] => (x:T) => x
h("Hello")
h(10)

//Loops
//clef fact(n:Int):Int=...