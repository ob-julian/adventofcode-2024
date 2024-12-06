package aof_2024_06;

import java.util.ArrayList;

public class Guard {
    private int row;
    private int col;
    private Direction direction;
    private ArrayList<Direction>[][] patrollMap;
    private char[][] obstacleMap;

    private GuardStatus status;

    public Guard(int row, int col, Direction direction, char[][] map) {
        this.row = row;
        this.col = col;
        this.direction = direction;
        this.status = GuardStatus.PATROLLING;
        this.obstacleMap = map;
        int map_length = map.length;
        int map_width = map[0].length;
        this.patrollMap = new ArrayList[map_length][map_width];
        for (int i = 0; i < map_length; i++) {
            for (int j = 0; j < map_width; j++) {
                this.patrollMap[i][j] = new ArrayList<>();
            }
        }
    }

    public int getRow() { return row; }

    public int getCol() { return col; }

    public Direction getDirection() { return direction; }

    public GuardStatus getStatus() { return status; }


    public boolean move() {
        // mark path with 'X'
        if (this.patrollMap[this.row][this.col].contains(this.direction)) {
            this.status = GuardStatus.LOOPING;
            return false;
        }
        this.patrollMap[this.row][this.col].add(this.direction);

        int newRow = this.row + this.direction.getRowChange();
        int newCol = this.col + this.direction.getColChange();
        if (newRow < 0 || newRow >= this.obstacleMap.length || newCol < 0 || newCol >= this.obstacleMap[0].length) {
            this.status = GuardStatus.OUT_OF_BOUNDS;
            return false;
        }
        if (this.obstacleMap[newRow][newCol] == '#') {
            this.direction = this.direction.turnRight();
            this.status = GuardStatus.PATROLLING;
            return true;
        }
        this.row = newRow;
        this.col = newCol;
        this.status = GuardStatus.PATROLLING;
        return true;
    }

    public int countPath() {
        int count = 0;
        for (int i = 0; i < this.patrollMap.length; i++) {
            for (int j = 0; j < this.patrollMap[i].length; j++) {
                if (!this.patrollMap[i][j].isEmpty()) {
                    count++;
                }
            }
        }
        return count;
    }

    public int[][] getPatrollPositions() {
        ArrayList<int[]> positions = new ArrayList<>();
        for (int i = 0; i < this.patrollMap.length; i++) {
            for (int j = 0; j < this.patrollMap[i].length; j++) {
                if (!this.patrollMap[i][j].isEmpty()) {
                    positions.add(new int[] { i, j });
                }
            }
        }
        return positions.toArray(new int[positions.size()][]);
    }

    public String toMapString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < this.patrollMap.length; i++) {
            for (int j = 0; j < this.patrollMap[i].length; j++) {
                if (this.patrollMap[i][j].isEmpty()) {
                    sb.append('.');
                } else if (this.patrollMap[i][j].size() == 1) {
                    sb.append(this.patrollMap[i][j].get(0).getSymbol());
                } else {
                    sb.append('X');
                }
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}
