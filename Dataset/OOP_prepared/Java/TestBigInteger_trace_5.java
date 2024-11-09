public class TestBigInteger {
    public static void main (String [] args) { 
      BigInteger i1 = new BigInteger("5555555555555555555555555555555555555555"); 
      BigInteger i2 = new BigInteger("4444444444444444444444444444444444444444"); 
      System.out.println (i1.add(i2));
   } 
}