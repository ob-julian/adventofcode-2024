package aof_2024_08;

import java.util.ArrayList;
import java.util.Objects;

public class Node {
    private int x;
    private int y;
    private char value;

    public Node(int x, int y, char value) {
        this.x = x;
        this.y = y;
        this.value = value;
    }

    public int getX() {
        return this.x;
    }

    public int getY() {
        return this.y;
    }

    public String toString() {
        return "Node: " + this.value + " at (" + this.x + ", " + this.y + ")";
    }

    private int greatestCommonDivisor(int a, int b) {
        if (b == 0) {
            return a;
        }
        return greatestCommonDivisor(b, a % b);
    }

    public Node[] getAntiNodes(Node otherNode) {
        int xDiff = this.x - otherNode.x;
        int yDiff = this.y - otherNode.y;
        Node[] antiNodes = new Node[2];
        antiNodes[0] = new Node(this.x + xDiff, this.y + yDiff, this.value);
        antiNodes[1] = new Node(otherNode.x - xDiff, otherNode.y - yDiff, this.value);
        return antiNodes;
    }

    public boolean isInBounds(int max_x, int max_y) {
        return this.x >= 0 && this.x < max_x && this.y >= 0 && this.y < max_y;
    }

    public Node[] getAllAntiNodes(Node otherNode, int max_x, int max_y) {
        int xDiff = otherNode.x - this.x;
        int yDiff = otherNode.y - this.y;
        int gcd = greatestCommonDivisor(xDiff, yDiff);
        xDiff = gcd == 0 ? xDiff : xDiff / gcd;
        yDiff = gcd == 0 ? yDiff : yDiff / gcd;
        ArrayList<Node> antiNodes = new ArrayList<>();
        int start_x = this.x;
        int start_y = this.y;
        while (start_x >= 0 && start_x < max_x && start_y >= 0 && start_y < max_y) {
            antiNodes.add(new Node(start_x, start_y, this.value));
            start_x += xDiff;
            start_y += yDiff;
        }
        start_x = this.x - xDiff;
        start_y = this.y - yDiff;
        while (start_x >= 0 && start_x < max_x && start_y >= 0 && start_y < max_y) {
            antiNodes.add(new Node(start_x, start_y, this.value));
            start_x -= xDiff;
            start_y -= yDiff;
        }
        return antiNodes.toArray(new Node[0]);
    }

    // for Set comparison
    @Override
    public boolean equals(Object obj) {
        if (obj == this) {
            return true;
        }
        if (!(obj instanceof Node)) {
            return false;
        }
        Node node = (Node) obj;
        return this.x == node.x && this.y == node.y;
    }

    @Override
    public int hashCode() {
        return Objects.hash(x, y);
    }
}
