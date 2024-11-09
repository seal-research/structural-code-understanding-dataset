# Definition for a binary tree node.
# class TreeNode(object):
#     def __init__(self, x):
#         self.val = x
#         self.left = None
#         self.right = None

class Codec:
    def serialize(self, root):
        res = []

        def dfs(node):
            if not node:
                res.append("N")
                return
            res.append(str(node.val))
            dfs(node.left)
            dfs(node.right)

        dfs(root)
        return ",".join(res)

    def deserialize(self, data):
        vals = data.split(",")
        self.i = 0

        def dfs():
            if vals[self.i] == "N":
                self.i += 1
                return None
            node = TreeNode(int(vals[self.i]))
            self.i += 1
            node.left = dfs()
            node.right = dfs()
            return node

        return dfs()

if __name__ == "__main__":
    codec = Codec()
    root = TreeNode(50)
    root.left = TreeNode(25)
    root.right = TreeNode(75)
    root.left.left = TreeNode(12)
    root.left.right = TreeNode(37)
    root.right.left = TreeNode(62)
    root.right.right = TreeNode(87)
    serialized = codec.serialize(root)
    deserialized = codec.deserialize(serialized)
    print(serialized)