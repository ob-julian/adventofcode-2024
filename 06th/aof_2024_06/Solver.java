package aof_2024_06;

public class Solver {
    public static void main(String[] args) {
        //FileParser fileParser = new FileParser("test.txt");
        FileParser fileParser = new FileParser("input.txt");
        Map map = new Map(fileParser.readFile());
        Guard guard = map.findInitialGuardPosition();
        while (guard.move());
        System.out.println("Advent of Code 2024 - Day 6");
        System.out.println("Part 1: " + guard.countPath());
        System.out.println("Part 2: " + new ObstacleFinder(map).findAmountOfLoopingObstacles(guard.getPatrollPositions()));

        //AI was used for proper usage and initialisation of Arrays of Linked Lists and Linked Lists of Arrays
    }
}