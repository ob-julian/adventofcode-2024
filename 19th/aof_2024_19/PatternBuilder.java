package aof_2024_19;

import java.util.Arrays;

public class PatternBuilder {

    private TowelTree root;
    
    public PatternBuilder(TowelTree root) {
        this.root = root;
    }

    public boolean isPossible(Color[] pattern) {
        return isPossible(pattern, 0);
    }

    private boolean isPossible(Color[] pattern, int index) {
        if (index == pattern.length) {
            return true;
        }

        int[] possiblePatterns = root.findPatternPart(pattern, index);
        //System.out.println("possiblePatterns: " + Arrays.toString(possiblePatterns));
        for (int i : possiblePatterns) {
            if (isPossible(pattern, index + i)) {
                return true;
            }
            //System.out.println("not possible at index: " + index + " with i: " + i);
        }
        return false;
    }

    public int countPossible(Color[] pattern) {
        return countPossible(pattern, 0);
    }

    private int countPossible(Color[] pattern, int index) {
        if (index == pattern.length) {
            return 1;
        }

        int[] possiblePatterns = root.findPatternPart(pattern, index);
        int count = 0;
        for (int i : possiblePatterns) {
            count += countPossible(pattern, index + i);
        }
        return count;
    }
}
