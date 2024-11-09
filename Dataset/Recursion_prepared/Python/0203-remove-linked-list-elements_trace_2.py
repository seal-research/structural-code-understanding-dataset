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
    # Test case 2
    head = ListNode(7, ListNode(7, ListNode(7, ListNode(7))))
    val = 7
    solution = Solution()
    result = solution.removeElements(head, val)
    while result:
        print(result.val, end=" -> ")
        result = result.next
    print("None")