sealed trait Expression
case class Val(value: Double) extends Expression
case class Fun(function: (Double, Double) => Double) extends Expression
case object Sum extends Expression
case object Diff extends Expression
case object Prod extends Expression
case object Div extends Expression

def evaluate(expression: List[Expression]): Option[Double] = {

  def applyOperation(operation: Expression, val1: Double, val2: Double): Double =
    operation match {
      case Sum => val1 + val2
      case Diff => val1 - val2
      case Prod => val1 * val2
      case Div => if (val2 != 0) val1 / val2 else throw new IllegalArgumentException("Division by zero")
      case Fun(function) => function(val1, val2)
    }

  def evaluateHelper(exprList: List[Expression], stack: List[Double]): Option[Double] =
    exprList match {
      case Nil => if (stack.length == 1) Some(stack.head) else None
      case Val(value) :: tail => evaluateHelper(tail, value :: stack)
      case operator :: tail =>

        if (stack.length < 2)
          throw new IllegalArgumentException("Not enough list elements, expression invalid")

        val val1 :: val2 :: t = stack
        val result = applyOperation(operator, val2, val1)

        evaluateHelper(tail, result :: t)
    }

  try {
    evaluateHelper(expression, Nil)
  } catch {
    case _: IllegalArgumentException | _: ArithmeticException => None
  }
}

// Test cases

val list1 = List(Val(1.0), Val(3.5), Sum)
val list2 = List(Val(0.0), Val(1.0), Div)
val list3 = List(Val(1.0), Val(2.0), Val(2.0), Prod, Sum, Val(1.0), Sum)
val list4 = List(Val(1.0), Val(0.0), Prod)
val list5 = List(Val(1.0), Val(0.0), Div)
val list6 = List(Val(2.0), Val(2.0), Sum, Val(3.0), Prod)
val list7 = List(Val(2.0), Val(3.0), Sum, Val(4.0), Prod)
val list8 = List(Val(3.0), Val(7.0), Val(10.0), Prod, Sum)
val list9 = List(Val(3.0), Val(1.0), Sum, Val(3.0), Val(2.0), Sum, Prod)
val list10 = List(Val(3.0), Val(1.0), Sum, Val(4.0), Val(4.0), Sum, Div)

evaluate(list1) // Some 4.5
evaluate(list2) // Some 0.0
evaluate(list3) // Some 6.0 = A + B * C + D
evaluate(list4) // Some 0.0
evaluate(list5) // None (Division by zero)
evaluate(list6) // Some 12.0 = (A + B) * C
evaluate(list7) // Some 20.0 = (A + B) * C
evaluate(list8) // Some 73.0 = A + B * C
evaluate(list9) // Some 20.0 = (A + B) * (C + D)
evaluate(list10) // Some 0.5 = (A + B) / (C + D)

// Tests for the live modification
def veryFunOperationOnNumbers(val1: Double, val2: Double): Double =
  val1 * val1 * val2

def evenMoreFunOperationOnNumbers(val1: Double, val2: Double): Double =
  val1 * val1 - val2 + val1

def notSoFunOperationOnNumbers(val1: Double, val2: Double): Double =
  val1 / val2

def thisOneIsSoFunILiterallyCantRN(val1: Double, val2: Double): Double =
  0

val modList1 = List(Val(1.0), Val(2.0), Fun(veryFunOperationOnNumbers))
val modList2 = List(Val(1.0), Val(2.0), Fun(evenMoreFunOperationOnNumbers))
val modList3 = List(Val(1.0), Val(0.0), Fun(notSoFunOperationOnNumbers))

evaluate(modList1) // Some 2.0
evaluate(modList2) // Some 0.0
evaluate(modList3) // None (Division by zero)
