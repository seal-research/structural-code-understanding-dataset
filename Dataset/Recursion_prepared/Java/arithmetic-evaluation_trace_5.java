import java.util.Stack;

public class ArithmeticEvaluation {

    public interface Expression {
        BigRational eval();
    }

    public enum Parentheses {LEFT}

    public enum BinaryOperator {
        ADD('+', 1),
        SUB('-', 1),
        MUL('*', 2),
        DIV('/', 2);

        public final char symbol;
        public final int precedence;

        BinaryOperator(char symbol, int precedence) {
            this.symbol = symbol;
            this.precedence = precedence;
        }

        public BigRational eval(BigRational leftValue, BigRational rightValue) {
            switch (this) {
                case ADD:
                    return leftValue.add(rightValue);
                case SUB:
                    return leftValue.subtract(rightValue);
                case MUL:
                    return leftValue.multiply(rightValue);
                case DIV:
                    return leftValue.divide(rightValue);
            }
            throw new IllegalStateException();
        }

        public static BinaryOperator forSymbol(char symbol) {
            for (BinaryOperator operator : values()) {
                if (operator.symbol == symbol) {
                    return operator;
                }
            }
            throw new IllegalArgumentException(String.valueOf(symbol));
        }
    }

    public static class Number implements Expression {
        private final BigRational number;

        public Number(BigRational number) {
            this.number = number;
        }

        @Override
        public BigRational eval() {
            return number;
        }

        @Override
        public String toString() {
            return number.toString