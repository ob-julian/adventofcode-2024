package aof_2024_10;

public class Solver {
    public static void main(String[] args) {
        //FileParser fileParser = new FileParser("test.txt");
        FileParser fileParser = new FileParser("input.txt");
        Map map = new Map(fileParser.readFile());
        PathFinder pathFinder = new PathFinder(map);

        System.out.println("Advent of Code 2024 - Day 10");
        System.out.println("Part 1: " + pathFinder.findAllPathsFor1());
        System.out.println("Part 2: " + pathFinder.findAllPathsFor2());
    }
}