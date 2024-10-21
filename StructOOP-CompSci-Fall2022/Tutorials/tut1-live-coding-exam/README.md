Implement a class that will have a public static main method. The name of the class should be your first and last name, e.g. MaciejWalczynski. In this class, inside the main method, you will create objects of the classes implemented next, and call their methods.  
Good luck!

1.Implement the Morse class, which will have two fields letter and code. The fields should be private and have appropriate getters and setters.

2.Implement a Morse function that will convert the text given as an argument into a string of dashes and dots (letters should be separated by spaces). The function should return this string.
E.g. SOS -> ... --- ...

3.Implement the function OnlyDashes, which will print those of the letters that consist of only dashes. The function should take as an argument an array of objects of the Morse class, having two fields: letter and code.

4.Implement the class RoadRunner, which will have private fields age and name. Add getters and setters and a constructor with age and name parameters.

5.Create an ArrayList called myRoadRunners, containing 5 RoadRunners with parameter values of your choice.  

6.Sort the list from the task by the names of the RoadRunners.

7.Find the oldest roadRunner. In case two roadRunners are the same age, give the one with the first name in alphabetical order.

8.Create a class Coyote, which contains a private field eatenAnimals (which is of type ArrayList<RoadRunner>) in addition to the age and name (also private) fields. In addition to the constructor and getters and setters, the Coyote class should contain an eat method that takes an object of the RoadRunner class as an argument and, as a result of the action, puts the eaten bird at the end of the eatenAnimals array.

9.Test the method implemented in step 8 on the array myRoadRunners and eat first two RoadRunners.

10.Has your myRoadRunners ArrayList been depleted by birds eaten by a coyote? If not, suggest a solution to this problem.
