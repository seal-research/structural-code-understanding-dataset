class Solution {

    public double myPow(double x, int n) {
        if (n == 0) {
            return 1;
        }
        //Make the negative values positive
        else if (n < 0) {
            //whenever even just divide it by 2
            //this will also include Integer.MIN_VALUE
            //We're doing this because if I do -N and N=Integer.MIN_VALUE it'll become a value which is greater than the max value of Integer.MAX_VALUE
            if (n % 2 == 0) {
                n = n / 2;
                n = -n;
                x = (1 / x) * (1 / x);
            } else { //Odds don't need to be divided as their negative is in the positive limit
                n = -n;
                x = 1 / x;
            }
        }
        if (n % 2 == 0) { //even
            return myPow(x * x, n / 2);
        } else { //odd
            return x * myPow(x * x, n / 2);
        }
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        System.out.println(solution.myPow(2.0, 1));
    }
}