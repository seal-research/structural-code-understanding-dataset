package programas;

import java.math.BigInteger;
import java.util.InputMismatchException;
import java.util.Scanner;

public class IterativeFactorial {

  public BigInteger factorial(BigInteger n) {
    if ( n == null ) {
      throw new IllegalArgumentException();
    }
    else if ( n.signum() == - 1 ) {
      // negative
      throw new IllegalArgumentException("Argument must be a non-negative integer");
    }
    else {
      BigInteger factorial = BigInteger.ONE;
      for ( BigInteger i = BigInteger.ONE; i.compareTo(n) < 1; i = i.add(BigInteger.ONE) ) {
        factorial = factorial.multiply(i);
      }
      return factorial;
    }
  }

  public static void main(String[] args) {
    BigInteger number = new BigInteger("5");
    BigInteger result = new IterativeFactorial().factorial(number);
    System.out.println("Factorial of " + number + ": " + result);
  }

}