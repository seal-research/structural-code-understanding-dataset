class Solution {

    public List<List<Integer>> combinationSum2(int[] candidates, int target) {
        Arrays.sort(candidates);
        List<List<Integer>> ans = new ArrayList<List<Integer>>();
        List<Integer> ls = new ArrayList<Integer>();
        comb(candidates, target, ans, ls, 0);
        return ans;
    }

    public void comb(
        int[] candidates,
        int target,
        List<List<Integer>> ans,
        List<Integer> ls,
        int index
    ) {
        if (target == 0) {
            ans.add(new ArrayList(ls));
        } else if (target < 0) return; else {
            for (int i = index; i < candidates.length; i++) {
                if (i > index && candidates[i] == candidates[i - 1]) continue;
                ls.add(candidates[i]);
                comb(candidates, target - candidates[i], ans, ls, i + 1);
                ls.remove(ls.get(ls.size() - 1));
            }
        }
    }

    public static void main(String[] args) {
        Solution sol = new Solution();
        int[] candidates = {4, 3, 2, 7, 8, 2, 3, 1};
        int target = 10;
        System.out.println(sol.combinationSum2(candidates, target));
    }
}