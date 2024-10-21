package src;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import util.Stack;

public class PostfixEvaluator {

    public String readPostfixExpressionFromFile(String fileName) {

        StringBuilder sb = new StringBuilder();

        try (BufferedReader br = new BufferedReader(new FileReader(fileName))) {
            String lineOfEquation;

            while ((lineOfEquation = br.readLine()) != null) {
                sb.append(lineOfEquation);
            }

        } catch (IOException e) {
            e.printStackTrace();
        }

        return sb.toString();
    }

    public int evaluatePostfixExpression(String postfixExpression) {

        Stack<Integer> stack = new Stack<>();

        String[] tokens = postfixExpression.split(" ");

        for (String token : tokens) {

            // \d is a digit (a character in the range [0-9]), and + means one or more
            // times. Thus, \d+ means match one or more digits.
            if (token.matches("\\d+")) {
                stack.push(Integer.parseInt(token));
                
            } else {
                int operand2 = stack.pop();
                int operand1 = stack.pop();
                int result = evaluateExpression(operand1, operand2, token);
                stack.push(result);
            }
        }

        if (stack.isEmpty()) {
            throw new IllegalArgumentException("Invalid postfix expression: " + postfixExpression);
        }

        return stack.pop();
    }

    public int evaluateExpression(int operand1, int operand2, String operator) {
        switch (operator) {
            case "+":
                return operand1 + operand2;
            case "-":
                return operand1 - operand2;
            case "*":
                return operand1 * operand2;
            case "/":
                return operand1 / operand2;
            default:
                throw new IllegalArgumentException("Invalid operator: " + operator);
        }
    }
}
