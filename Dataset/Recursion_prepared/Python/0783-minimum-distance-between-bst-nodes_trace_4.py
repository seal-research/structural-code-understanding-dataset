class TreeNode:
     def __init__(self, val=0, left=None, right=None):
         self.val = val
         self.left = left
         self.right = right
class Solution:
    def minDiffInBST(self, root: Optional[TreeNode]) -> int:
        curr_smallest, prev = float("inf"), None
        
        def inorder(node):
            nonlocal curr_smallest, prev
            if node is None:
                return
            
            inorder(node.left)
            if prev is not None:
                curr_smallest = min(curr_smallest, node.val-prev.val)
            prev = node
            inorder(node.right)

        inorder(root)
        return curr_smallest

if __name__ == "__main__":
    root = TreeNode(15)
    root.left = TreeNode(10)
    root.right = TreeNode(20)
    root.left.left = TreeNode(8)
    root.left.right = TreeNode(12)
    root.right.left = TreeNode(17)
    root.right.right = TreeNode(25)
    solution = Solution()
    print(solution.minDiffInBST(root))