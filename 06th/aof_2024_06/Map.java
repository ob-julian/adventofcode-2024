package aof_2024_06;

public class Map {
    private char[][] map;
    private int[] tmp_obstacle = new int[2];
    private int[] guardPositons;

    public Map(String[] lines) {
        this.map = new char[lines.length][];
        for (int i = 0; i < lines.length; i++) {
            this.map[i] = lines[i].toCharArray();
        }
    }

    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < this.map.length; i++) {
            sb.append(this.map[i]);
            sb.append("\n");
        }
        return sb.toString();
    }

    public int[] find(char c) {
        for (int i = 0; i < this.map.length; i++) {
            for (int j = 0; j < this.map[i].length; j++) {
                if (this.map[i][j] == c) {
                    return new int[] { i, j };
                }
            }
        }
        return null;
    }

    public Guard findInitialGuardPosition() {
        if (this.guardPositons == null) {
            this.guardPositons = find('^');
        }
        return new Guard(this.guardPositons[0], this.guardPositons[1], Direction.UP, this.map);
    }

    public char[][] getMap() {
        return this.map;
    }

    public boolean setObstacle(int row, int col) {
        if (this.map[row][col] == '#' || this.map[row][col] == '^') {
            return false;
        }
        this.map[row][col] = '#';
        this.tmp_obstacle[0] = row;
        this.tmp_obstacle[1] = col;
        return true;
    }

    public boolean removeObstacle() {
        if (this.map[this.tmp_obstacle[0]][this.tmp_obstacle[1]] != '#') {
            return false;
        }
        this.map[this.tmp_obstacle[0]][this.tmp_obstacle[1]] = '.';
        return true;
    }

}
