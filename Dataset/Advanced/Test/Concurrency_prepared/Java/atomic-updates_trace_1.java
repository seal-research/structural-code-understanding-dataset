import java.util.Arrays;
import java.util.concurrent.ThreadLocalRandom;

public class AtomicUpdates {

    private static final int NUM_BUCKETS = 10;

    public static class Buckets {
        private final int[] data;

        public Buckets(int[] data) {
            this.data = data.clone();
        }

        public int getBucket(int index) {
            synchronized (data) {
                return data[index];
            }
        }

        public int transfer(int srcIndex, int dstIndex, int amount) {
            if (amount < 0)
                throw new IllegalArgumentException("negative amount: " + amount);
            if (amount == 0)
                return 0;

            synchronized (data) {
                if (data[srcIndex] - amount < 0)
                    amount = data[srcIndex];
                if (data[dstIndex] + amount < 0)
                    amount = Integer.MAX_VALUE - data[dstIndex];
                if (amount < 0)
                    throw new IllegalStateException();
                data[srcIndex] -= amount;
                data[dstIndex] += amount;
                return amount;
            }
        }

        public int[] getBuckets() {
            synchronized (data) {
                return data.clone();
            }
        }
    }

    private static long getTotal(int[] values) {
        long total = 0;
        for (int value : values) {
            total += value;
        }
        return total;
    }

    public static void main(String[] args) {
        int[] values = new int[NUM_BUCKETS];
        for (int i = 0; i < values.length; i++)
            values[i] = i * 10;
        Buckets buckets = new Buckets(values);
        buckets.transfer(0, 1, 5);
    }
}