package cornell.debugger;


/**
 * Hello world!
 *
 */
public class App {
    public static void main(String[] args) {
        System.out.println("Starting test application");
        test();
    }

    public static void test() {
        int x = 1;
        int y = 2;
        int z = x + y;
        System.out.println("Result: " + z);
        if(x==1) {
        	System.out.println("Inside if");
        }
        switch(y) {
        case 1: 
        	System.out.println("Odd");
        case 2:
        	System.out.println("Even");
        default:
        	System.out.println("Impossible");
        }
        return;
    }
}