package aof_2024_08;

public class Solver {
    public static void main(String[] args) {
        //FileParser fileParser = new FileParser("test.txt");
        FileParser fileParser = new FileParser("input.txt");
        Nodes nodes = new Nodes(fileParser.readFile());

        System.out.println("Advent of Code 2024 - Day 08");
        System.out.println("Part 1: " + nodes.getAllUniqueAntiNodes().length);
        System.out.println("Part 2: " + nodes.getAllUniqueAntiNodesWithInterference().length);
    }
}