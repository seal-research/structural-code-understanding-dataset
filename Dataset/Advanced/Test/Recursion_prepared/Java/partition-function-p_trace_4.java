import java.math.BigInteger;

public class PartitionFunction {
    public static void main(String[] args) {
        BigInteger result = partitions(20);
        System.out.println("P(20) = " + result);
    }

    private static BigInteger partitions(int n) {
        BigInteger[] p = new BigInteger[n + 1];
        p[0] = BigInteger.ONE;
        for (int i = 1; i <= n; ++i) {
            p[i] = BigInteger.ZERO;
            for (int k = 1; ; ++k) {
                int j = (k * (3 * k - 1))/2;
                if (j > i)
                    break;
                if ((k & 1) != 0)
                    p[i] = p[i].add(p[i - j]);
                else
                    p[i] = p[i].subtract(p[i - j]);
                j += k;
                if (j > i)
                    break;
                if ((k & 1) != 0)
                    p[i] = p[i].add(p[i - j]);
                else
                    p[i] = p[i].subtract(p[i - j]);
            }
        }
        return p[n];
    }
}