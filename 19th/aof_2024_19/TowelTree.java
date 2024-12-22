package aof_2024_19;

import java.util.*;

public class TowelTree {
    private HashMap<Color, TowelTree> branches;
    private Color color;
    private boolean isTowel;

    public TowelTree(Color color, boolean isTowel) {
        this.color = color;
        this.branches = new HashMap<>();
        this.isTowel = isTowel;
    }

    public boolean isTowel() {
        return isTowel;
    }

    public void addBranch(Color color, TowelTree branch) {
        this.branches.put(color, branch);
    }

    public void generatePattern(String pattern) {
        generatePattern(pattern, 0);
    }

    private void generatePattern(String pattern, int index) {
        if (index == pattern.length()) { // skip root
            this.isTowel = true;
            return;
        }

        Color color = Color.fromChar(pattern.charAt(index));
        if (this.branches.containsKey(color)) {
            this.branches.get(color).generatePattern(pattern, index + 1);
        } else {
            TowelTree branch = new TowelTree(color, false);
            this.branches.put(color, branch);
            branch.generatePattern(pattern, index + 1);
        }
    }


    public int[] findPatternPart(Color[] pattern, int index) {
        return findPatternPart(pattern, index, 0);
    }

    private int[] findPatternPart(Color[] pattern, int index, int depth) {
        if (index == pattern.length) {
            if (this.isTowel) {
                return new int[] {depth};
            } else {
                return new int[] {};
            }
        }
        Color nColor = pattern[index];
        ArrayList<Integer> results = new ArrayList<>();
        if (this.isTowel && depth != 0) {
            results.add(depth);
        }
        if (this.branches.containsKey(nColor)) {
            int[] res = this.branches.get(nColor).findPatternPart(pattern, index + 1, depth + 1);
            for (int r : res) {
                results.add(r);
            }
        }
        // Integer to int
        return results.stream().mapToInt(i -> i).toArray();
    }

    @Override
    public String toString() {
        return "TowelTree{\n" + toString(0) + "}";
    }

    public String toString(int level) {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < level; i++) {
            sb.append("  ");
        }
        if (level == 0) {
            sb.append("root");
        } else {
            sb.append(color);
        }
        if (isTowel) {
            sb.append(" (towel)");
        }
        sb.append("\n");
        for (TowelTree branch : branches.values()) {
            sb.append(branch.toString(level + 1));
        }
        return sb.toString();
    }
}
