package aof_2024_19;

import java.util.ArrayList;

public class Parser {
    public TowelTree root;
    public Color[][] patterns;
    
    public Parser(String[] lines) {
        this.root = new TowelTree(Color.WHITE, false);
        parseTree(lines[0].split(", "));

        ArrayList<Color[]> patterns = new ArrayList<>();
        for (int i = 2; i < lines.length; i++) {
            String[] colors = lines[i].split("");
            Color[] pattern = new Color[colors.length];
            for (int j = 0; j < colors.length; j++) {
                pattern[j] = Color.fromChar(colors[j].charAt(0));
            }
            patterns.add(pattern);
        }
        this.patterns = patterns.toArray(new Color[0][0]);
    }

    public void parseTree(String[] towels) {
        for (String towel : towels) {
            root.generatePattern(towel);
        }
    }
}
