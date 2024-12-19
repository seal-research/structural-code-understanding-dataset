import java.math.BigInteger;

public static BigInteger ack(BigInteger m, BigInteger n) {
    return m.equals(BigInteger.ZERO)
            ? n.add(BigInteger.ONE)
            : ack(m.subtract(BigInteger.ONE),
                        n.equals(BigInteger.ZERO) ? BigInteger.ONE : ack(m, n.subtract(BigInteger.ONE)));
}

public static void main(String[] args) {
    System.out.println(ack(BigInteger.valueOf(1), BigInteger.valueOf(1)));
}