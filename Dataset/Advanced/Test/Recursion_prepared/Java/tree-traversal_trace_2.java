import java.util.*;

public class TreeTraversal {

    static class Node<T> {
        T value;
        Node<T> left;
        Node<T> right;

        Node(T value) {
            this.value = value;
        }

        void visit() {
            System.out.print(this.value + " ");
        }
    }

    static enum ORDER {
        PREORDER, INORDER, POSTORDER, LEVEL
    }

    static <T> void traverse(Node<T> node, ORDER order) {
        if (node == null) {
            return;
        }
        switch (order) {
            case PREORDER:
                node.visit();
                traverse(node.left, order);
                traverse(node.right, order);
                break;
            case INORDER:
                traverse(node.left, order);
                node.visit();
                traverse(node.right, order);
                break;
            case POSTORDER:
                traverse(node.left, order);
                traverse(node.right, order);
                node.visit();
                break;
            case LEVEL:
                Queue<Node<T>> queue = new LinkedList<>();
                queue.add(node);
                while (!queue.isEmpty()) {
                    Node<T> next = queue.remove();
                    next.visit();
                    if (next.left != null)
                        queue.add(next.left);
                    if (next.right != null)
                        queue.add(next.right);
                }
        }
    }

    public static void main(String[] args) {
        Node<Integer> root = new Node<>(20);
        Node<Integer> left = new Node<>(10);
        Node<Integer> right = new Node<>(30);
        root.left = left;
        root.right = right;
        left.left = new Node<>(5);
        left.right = new Node<>(15);
        right.left = new Node<>(25);
        right.right = new Node<>(35);

        traverse(root, ORDER.INORDER);
    }
}