import java.util.HashMap;
import java.util.Map;

public class MutualRecursion {

    private static Map<Integer,Integer> F_MAP = new HashMap<>();

    private static int f(final int n) {
        if ( F_MAP.containsKey(n) ) {
            return F_MAP.get(n);
        }
        int fn = n == 0 ? 1 : n - m(f(n - 1));
        F_MAP.put(n, fn);
        return fn;
    }

    private static Map<Integer,Integer> M_MAP = new HashMap<>();

    private static int m(final int n) {
        if ( M_MAP.containsKey(n) ) {
            return M_MAP.get(n);
        }
        int mn = n == 0 ? 0 : n - f(m(n - 1));
        M_MAP.put(n, mn);
        return mn;
    }

    public static void main(final String args[]) {
        System.out.printf("f(25) = %d%n", f(25));
    }
}