package aof_2024_24;

public class Solver {
    public static void main(String[] args) {
        //FileParser fileParser = new FileParser("test.txt");
        FileParser fileParser = new FileParser("input.txt");
        fileParser.readFile().parseFile();
        System.out.println("Advent of Code 2024 - Day 24");
        System.out.println("Part 1: " + fileParser.endGatesToInt());
        // Caching to difficult/ time intensive to implement, switch to Python
    }
}