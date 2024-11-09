class Solution {
    int res = 0;
    HashMap<Integer, List<Integer>> graph = new HashMap<>();
    HashSet<String> oldEdges = new HashSet<>();

    public int minReorder(int n, int[][] connections) {
        HashSet<Integer> visited = new HashSet<>();
        for (int[] edges : connections){
            int a = edges[0], b = edges[1];
            String s = a + "->" + b;
            oldEdges.add(s);
            graph.computeIfAbsent(a, val -> new ArrayList<>()).add(b);
            graph.computeIfAbsent(b, val -> new ArrayList<>()).add(a);
        }
        dfs(0, -1, visited);
        return res-1;
    }

    private void dfs(int curr, int parent, HashSet<Integer> visited) {
        if (visited.contains(curr))
            return;
        visited.add(curr);
        String s = curr + "->" + parent;
        if (!oldEdges.contains(s))
            res++;
        for (int child : graph.get(curr)){
            dfs(child, curr, visited);
        }
    }

    public static void main(String[] args) {
        Solution sol = new Solution();
        int[][] connections = {{0, 1}, {1, 2}, {2, 3}, {3, 0}, {4, 5}};
        System.out.println(sol.minReorder(6, connections));
    }
}