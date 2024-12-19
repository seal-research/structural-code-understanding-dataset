class Solution:
    def minReorder(self, n: int, connections: List[List[int]]) -> int:
        edges = {(a,b) for a, b in connections}
        neighbors = defaultdict(list)
        visit = set()
        changes = 0

        for a, b in connections:
            neighbors[a].append(b)
            neighbors[b].append(a)
        
        def dfs(city):
            nonlocal changes

            for neighbor in neighbors[city]:
                if neighbor in visit:
                    continue
                # check if this neighbor can reach city 0
                if (neighbor, city) not in edges:
                    changes += 1
                visit.add(neighbor)
                dfs(neighbor)
        visit.add(0)
        dfs(0)
        return changes

if __name__ == "__main__":
    solution = Solution()
    n = 4
    connections = [[0,1],[2,0],[3,2]]
    print(solution.minReorder(n, connections))