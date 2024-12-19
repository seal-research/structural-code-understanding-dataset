class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None

class Solution:
    def reverseList(self, head: ListNode) -> ListNode:
        prev, curr = None, head

        while curr:
            temp = curr.next
            curr.next = prev
            prev = curr
            curr = temp
        return prev

if __name__ == "__main__":
    # Test case 2: List with a single element
    node1 = ListNode(1)
    solution = Solution()
    reversed_list = solution.reverseList(node1)
    while reversed_list:
        print(reversed_list.val, end=" -> ")
        reversed_list = reversed_list.next
    print("None")