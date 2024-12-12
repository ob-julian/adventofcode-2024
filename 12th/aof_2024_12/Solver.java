package aof_2024_12;

public class Solver {
    public static void main(String[] args) {
        System.out.println("Advend of Code 2024 - Day 12");

        //FileParser fileParser = new FileParser("test.txt");
        FileParser fileParser = new FileParser("input.txt");
        Field field = new Field(fileParser.readFile());
        field.joinAllRegions();
        System.out.println("Part 1: " + field.calculateCost());
        System.out.println("Part 2: " + field.calculateDiscountCost());
    }
}