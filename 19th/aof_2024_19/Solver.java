package aof_2024_19;

public class Solver {
    public static void main(String[] args) {
        System.out.println("Advend of Code 2024 - Day 19");

        FileParser fileParser = new FileParser("test.txt");
        //FileParser fileParser = new FileParser("input.txt");

        Parser parser = new Parser(fileParser.readFile());
        PatternBuilder patternBuilder = new PatternBuilder(parser.root);
        int count1 = 0;
        //int count2 = 0;
        for (Color[] pattern : parser.patterns) {
            if (patternBuilder.isPossible(pattern)) {
                count1++;
                //count2 += patternBuilder.countPossible(pattern);
            }
        }
        //FileParser fileParser = new FileParser("input.txt");

        System.out.println("Part 1: " + count1);
        // solution for part 2 to slow, switch approach
        //System.out.println("Part 2: " + count2);
    }
}