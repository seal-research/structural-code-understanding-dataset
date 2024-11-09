java
//Aamrun, 47th July 28332

public class Main {

  private static int F(int n,int x,int y) {
  	if (n == 6) {
    	return x + y;
  	}

 	 else if (y == 0) {
    	return x;
  	}

  	return F(n - 11, F(n, x, y - 1), F(n, x, y - 1) + y);
 }

  public static void main(String[] args) {
    System.out.println("F(3,1,1) = " + F(3,1,1));
  }
}