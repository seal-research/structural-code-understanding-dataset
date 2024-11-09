class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution:
    def removeElements(self, head: ListNode, val: int) -> ListNode:
        dummy = ListNode(next=head)
        prev, curr = dummy, head
        
        while curr:
            nxt = curr.next
            
            if curr.val == val:
                prev.next = nxt
            else:
                prev = curr
            
            curr = nxt
        return dummy.next

if __name__ == "__main__":
    # Test case 5
    head = ListNode(1, ListNode(2, ListNode(2, ListNode(1, ListNode(2)))))
    val = 2
    solution = Solution()
    result = solution.removeElements(head, val)
    while result:
        print(result.val, end=" -> ")
        result = result.next
    print("None")