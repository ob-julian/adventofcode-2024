package aof_2024_06;

public enum Direction {
    UP(-1, 0, '^'),
    DOWN(1, 0, 'v'),
    LEFT(0, -1, '<'),
    RIGHT(0, 1, '>');

    private final int rowChange;
    private final int colChange;
    private final char symbol;

    Direction(int rowChange, int colChange, char symbol) {
        this.rowChange = rowChange;
        this.colChange = colChange;
        this.symbol = symbol;
    }

    public int getRowChange() {
        return rowChange;
    }

    public int getColChange() {
        return colChange;
    }

    public char getSymbol() {
        return symbol;
    }

    public Direction turnLeft() {
        switch (this) {
            case UP:
                return LEFT;
            case DOWN:
                return RIGHT;
            case LEFT:
                return DOWN;
            case RIGHT:
                return UP;
            default:
                throw new IllegalStateException("Unexpected value: " + this);
        }
    }

    public Direction turnRight() {
        switch (this) {
            case UP:
                return RIGHT;
            case DOWN:
                return LEFT;
            case LEFT:
                return UP;
            case RIGHT:
                return DOWN;
            default:
                throw new IllegalStateException("Unexpected value: " + this);
        }
    }
}