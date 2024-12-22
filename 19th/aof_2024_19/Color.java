package aof_2024_19;

public enum Color {
    WHITE, BLUE, BLACK, RED, GREEN;

    public static Color fromChar(char color) {
        switch (color) {
            case 'w':
                return WHITE;
            case 'u':
                return BLUE;
            case 'b':
                return BLACK;
            case 'r':
                return RED;
            case 'g':
                return GREEN;
            default:
                throw new IllegalArgumentException("Unknown color: " + color);
        }
    }

    public static int numColors() {
        return Color.values().length;
    }
}
