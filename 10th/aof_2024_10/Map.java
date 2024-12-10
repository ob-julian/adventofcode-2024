package aof_2024_10;

import java.util.ArrayList;

public class Map {

    private int[][] map;
    private int maxX;
    private int maxY;

    public Map(String[] lines) {
        this.map = new int[lines.length][lines[0].length()];
        for (int i = 0; i < lines.length; i++) {
            for (int j = 0; j < lines[i].length(); j++) {
                this.map[i][j] = Character.getNumericValue(lines[i].charAt(j));
            }
        }
        this.maxX = this.map.length;
        this.maxY = this.map[0].length;
    }

    public int get(int x, int y) {
        return this.map[x][y];
    }

    public int get(Position pos) {
        return get(pos.x, pos.y);
    }

    public boolean isValid(int x, int y) {
        return x >= 0 && x < this.maxX && y >= 0 && y < this.maxY;
    }

    public boolean isValid(Position pos) {
        return isValid(pos.x, pos.y);
    }

    public Position[] findAllElevations(int elevation) {
        ArrayList<Position> positions = new ArrayList<>();
        for (int i = 0; i < this.map.length; i++) {
            for (int j = 0; j < this.map[i].length; j++) {
                if (this.map[i][j] == elevation) {
                    positions.add(new Position(i, j));
                }
            }
        }
        return positions.toArray(new Position[0]);
    }
        
    @Override
    public String toString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < this.map.length; i++) {
            for (int j = 0; j < this.map[i].length; j++) {
                sb.append(this.map[i][j]);
            }
            sb.append("\n");
        }
        return sb.toString();
    }

}
