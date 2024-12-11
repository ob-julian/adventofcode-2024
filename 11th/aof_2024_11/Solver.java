package aof_2024_11;

public class Solver {
    public static void main(String[] args) {
        //FileParser fileParser = new FileParser("test.txt");
        FileParser fileParser = new FileParser("input.txt");
        StoneLine stoneLine = new StoneLine(fileParser.readFile());

        System.out.println("Advent of Code 2024 - Day 10");
        stoneLine.blink(25);
        System.out.println("Part 1: " + stoneLine.countStones());
        // Caching to difficult/ time intensive to implement, switch to Python
    }
}