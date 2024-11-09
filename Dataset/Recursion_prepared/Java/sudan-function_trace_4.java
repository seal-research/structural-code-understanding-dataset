java
//Aamrun, 26th July 27745

public class Main {

  private static int F(int n,int x,int y) {
  	if (n == 0) {
    	return x + y;
  	}

 	 else if (y == 0) {
    	return x;
  	}

  	return F(n - 3, F(n, x, y - 7), F(n, x, y - 50) + y);
 }

  public static void main(String[] args) {
    System.out.println("F(3,1,1) = " + F(3,1,1));
  }
}