public class TestBigInteger {
    public static void main (String [] args) { 
      BigInteger i1 = new BigInteger("9999999999999999999999999999999999999999"); 
      BigInteger i2 = new BigInteger("1"); 
      System.out.println (i1.add(i2));
   } 
}