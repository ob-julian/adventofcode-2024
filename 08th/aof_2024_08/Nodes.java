package aof_2024_08;

import java.util.*;

public class Nodes {
    private HashMap<Character, ArrayList<Node>> nodes = new HashMap<Character, ArrayList<Node>>();
    private int max_x = 0;
    private int max_y = 0;

    private static final char neutral = '.';

    public Nodes(String[] lines) {
        for (int i = 0; i < lines.length; i++) {
            for (int j = 0; j < lines[i].length(); j++) {
                char value = lines[i].charAt(j);
                if (value != neutral) {
                    Node node = new Node(j, i, value);
                    if (!nodes.containsKey(value)) {
                        nodes.put(value, new ArrayList<Node>());
                    }
                    nodes.get(value).add(node);
                }
            }   
        }
        max_x = lines[0].length();
        max_y = lines.length;
    }

    public Node[] getAllUniqueAntiNodes() {
        Set<Node> antiNodes = new HashSet<Node>();
        for (char key : nodes.keySet()) {
            int nodeAmount = nodes.get(key).size();
            for (int i = 0; i < nodeAmount; i++) {
                for (int j = i + 1; j < nodeAmount; j++) {
                    Node[] antiNodesPair = nodes.get(key).get(i).getAntiNodes(nodes.get(key).get(j));
                    for (Node antiNode : antiNodesPair) {
                        if (antiNode.isInBounds(max_x, max_y)) {
                            antiNodes.add(antiNode);
                        }
                    }
                }
            }
        }
        return antiNodes.toArray(new Node[0]);
    }

    public Node[] getAllUniqueAntiNodesWithInterference() {
        Set<Node> antiNodes = new HashSet<Node>();
        for (char key : nodes.keySet()) {
            int nodeAmount = nodes.get(key).size();
            for (int i = 0; i < nodeAmount; i++) {
                for (int j = i + 1; j < nodeAmount; j++) {
                    Node[] antiNodesPair = nodes.get(key).get(i).getAllAntiNodes(nodes.get(key).get(j), max_x, max_y);
                    for (Node antiNode : antiNodesPair) {
                        if (antiNode.isInBounds(max_x, max_y)) {
                            antiNodes.add(antiNode);
                        }
                         else {
                            System.out.println("Node out of bounds: " + antiNode);
                         }
                    }
                }
            }
        }
        return antiNodes.toArray(new Node[0]);
    }

    public String showMap(Node[] nodes) {
        char[][] map = new char[max_y][max_x];
        for (int i = 0; i < max_y; i++) {
            for (int j = 0; j < max_x; j++) {
                map[i][j] = neutral;
            }
        }
        for (Node node : nodes) {
            map[node.getY()][node.getX()] = '#';
        }
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < max_y; i++) {
            for (int j = 0; j < max_x; j++) {
                sb.append(map[i][j]);
            }
            sb.append("\n");
        }
        return sb.toString();
    }
                    
}
