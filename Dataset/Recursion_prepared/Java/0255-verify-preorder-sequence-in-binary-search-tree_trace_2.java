class Solution {
    public boolean verifyPreorder(int[] preorder) {
        int minLimit = Integer.MIN_VALUE;
        Stack<Integer> stack = new Stack<>();
        
        for (int num: preorder) {
            while (!stack.isEmpty() && stack.peek() < num) {
                minLimit = stack.pop();
            }
            
            if (num <= minLimit) {
                return false;
            }
            
            stack.push(num);
        }
        
        return true;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        int[] test2 = {5, 2, 6, 1, 3};
        System.out.println(solution.verifyPreorder(test2));
    }
}