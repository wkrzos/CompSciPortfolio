import scala.math.sqrt

// Exercise 1

type Point2D = (Float, Float)

def distance(point: Point2D): Float = {
  val (x, y) = point
  math.sqrt(x * x + y * y).toFloat
}

println(distance((5, 5)))

// Exercise 2

// Part 1

type PersonTuple = (String, String, Int, String, Int)
type PartnershipTuple = (PersonTuple, PersonTuple)

val person1: PersonTuple = ("Maciej", "Kradziej", 32, "Male", 42)
val person2: PersonTuple = ("Rysiu", "Pysiu", 35, "Male", 39)

def biggerShoeSize(partnership: PartnershipTuple): PersonTuple = {
  val (_, _, _, _, shoeSize1) = partnership._1
  val (_, _, _, _, shoeSize2) = partnership._2
  if (shoeSize1 > shoeSize2) partnership._1 else partnership._2
}

println(biggerShoeSize((person1, person2)))

// Part 2

case class PersonClassType(name: String, surname: String, age: Int, sex: String, shoeSize: Int)
case class PartnershipClassType(partner1: PersonClassType, partner2: PersonClassType)

val person3 = PersonClassType("John", "Doe", 25, "Male", 44)
val person4 = PersonClassType("Jane", "Doe", 28, "Female", 38)

def biggerShoeSize(partnership: PartnershipClassType): PersonClassType = {
  if (partnership.partner1.shoeSize > partnership.partner2.shoeSize) partnership.partner1
  else partnership.partner2
}

val partnership34 = PartnershipClassType(person3, person4)
println(biggerShoeSize(partnership34))

// Exercise 3

sealed trait WeekDay
case object Monday extends WeekDay
case object Tuesday extends WeekDay
case object Wednesday extends WeekDay
case object Thursday extends WeekDay
case object Friday extends WeekDay
case object Saturday extends WeekDay
case object Sunday extends WeekDay

def weekDayToString(day: WeekDay): String = day match {
  case Monday => "Pon"
  case Tuesday => "Wt"
  case Wednesday => "Sr"
  case Thursday => "Czw"
  case Friday => "Pt"
  case Saturday => "Sob"
  case Sunday => "Nd"
}

def nextDay(day: WeekDay): WeekDay = day match {
  case Monday => Tuesday
  case Tuesday => Wednesday
  case Wednesday => Thursday
  case Thursday => Friday
  case Friday => Saturday
  case Saturday => Sunday
  case Sunday => Monday
}

println(weekDayToString(Monday))
println(nextDay(Monday))

// Exercise 4

sealed trait Maybe[+A]
case class Just[A](value: A) extends Maybe[A]
case object Nothing extends Maybe[Nothing]

def safeHead[A](list: List[A]): Maybe[A] = list match {
  case Nil => Nothing
  case head :: _ => Just(head)
}

println(safeHead(List.empty))
println(safeHead(List(1)))
println(safeHead(List("Cause")))

// Exercise 5

sealed trait Solid
case class Cuboid(length: Float, width: Float, height: Float) extends Solid
case class Cone(radius: Float, height: Float) extends Solid
case class Sphere(radius: Float) extends Solid
case class Cylinder(radius: Float, height: Float) extends Solid
case class Torus(majorRadius: Float, minorRadius: Float) extends Solid

type SolidFigure = Option[Solid]

def volume(figure: SolidFigure): Float = figure match {
  case Some(Cuboid(length, width, height)) => length * width * height
  case Some(Cone(radius, height)) => (1/ 3) * math.Pi.toFloat * radius * radius * height
  case Some(Sphere(radius)) => (4 / 3) * math.Pi.toFloat * radius * radius * radius
  case Some(Cylinder(radius, height)) => math.Pi.toFloat * radius * radius * height
  case Some(Torus(majorRadius, minorRadius)) => 2 * math.Pi.toFloat * minorRadius * minorRadius * majorRadius
  case None => 0.0
}

val cuboidExample: SolidFigure = Some(Cuboid(2.0, 3.0, 4.0))
val coneExample: SolidFigure = Some(Cone(1.5, 5.0))
val sphereExample: SolidFigure = Some(Sphere(2.0))
val cylinderExample: SolidFigure = Some(Cylinder(1.0, 3.0))
val torusExample: SolidFigure = Some(Torus(3.0, 1.0))
val noSolidExample: SolidFigure = None

val cuboidVolume = volume(cuboidExample)
val coneVolume = volume(coneExample)
val sphereVolume = volume(sphereExample)
val cylinderVolume = volume(cylinderExample)
val torusVolume = volume(torusExample)
val noSolidVolume = volume(noSolidExample)
