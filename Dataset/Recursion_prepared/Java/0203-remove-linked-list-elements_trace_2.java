class Solution {
    public ListNode removeElements(ListNode head, int val) {
        ListNode dummy = new ListNode(0, head);
        ListNode prev = dummy, curr = head;
        while(curr != null) {
            ListNode nxt = curr.next;
            
            if(curr.val == val)
                prev.next = nxt;
            else
                prev = curr;
            
            curr = nxt;
        }
        return dummy.next;
    }

    public static void main(String[] args) {
        Solution solution = new Solution();
        ListNode head = new ListNode(7, new ListNode(7, new ListNode(7, new ListNode(7, new ListNode(7)))));
        solution.removeElements(head, 7);
    }
}

class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
    ListNode(int val, ListNode next) { this.val = val; this.next = next; }
}