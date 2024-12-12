package aof_2024_12;

import java.util.*;

public class Region {
    public RegionProperties properties;
    private List<Region> neighbours;
    private int x;
    private int y;

    public Region (int size, int perimiter, char cropType, int id, int x, int y) {
        // using complex data structure to allow pointer manipulation
        this.properties = new RegionProperties(size, perimiter, cropType, id);
        this.neighbours = new ArrayList<Region>();
        neighbours.add(this);
        this.x = x;
        this.y = y;
    }

    @Override
    public boolean equals(Object obj) {
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        final Region other = (Region) obj;
        if (this.properties.id != other.properties.id) {
            return false;
        }
        return true;
    }

    @Override
    public int hashCode() {
        return this.properties.id;
    }

    public void combine(Region other) {
        if (this.neighbours.size() >= other.neighbours.size()) {
            this.properties.combine(other.properties);
            for (Region neighbour : other.neighbours) {
                neighbour.override(this);
                this.neighbours.add(neighbour);
            }
        } else {
            other.combine(this);
            this.override(other);
        }
    }

    public boolean sameCropType(Region other) {
        return this.properties.cropType == other.properties.cropType;
    }

    public int getPerimeter() {
        return this.properties.perimeter;
    }

    public void removeFence() {
        this.properties.perimeter -= 2;
    }

    public int getSize() {
        return this.properties.size;
    }

    public char getCropType() {
        return this.properties.cropType;
    }

    public int getId() {
        return this.properties.id;
    }

    public void override(Region other) {
        this.properties = other.properties;
        this.neighbours = other.neighbours;
    }

    public int getindividualRegionBorders() {
        int minX = (int) Float.POSITIVE_INFINITY;
        int maxX = 0;
        int minY = (int) Float.POSITIVE_INFINITY;
        int maxY = 0;
        for (Region neighbour : this.neighbours) {
            minX = Math.min(minX, neighbour.x);
            maxX = Math.max(maxX, neighbour.x);
            minY = Math.min(minY, neighbour.y);
            maxY = Math.max(maxY, neighbour.y);
        }
        int size = 3;
        int[][] regionCopy = new int[(maxX - minX + 3)*size][(maxY - minY + 3)*size];
        for (Region neighbour : this.neighbours) {
            fillRegion(regionCopy, (neighbour.x - minX + 1)*size, (neighbour.y - minY + 1)*3, size);
        }
        for (int i = 0; i < regionCopy.length; i++) {
            for (int j = 0; j < regionCopy[i].length; j++) {
                paintBorder(i, j, regionCopy);
            }
        }
        return getAllUniqueBorders(regionCopy);
    }

    private void fillRegion(int[][] region, int x, int y, int size) {
        for (int i = 0; i < size; i++) {
            for (int j = 0; j < size; j++) {
                region[x + i][y + j] = 1;
            }
        }
    }

    private void paintBorder(int x, int y, int[][] region) {
        if (region[x][y] != 1) {
            return;
        }
        paintBorderIter(x + 1, y, region);
        paintBorderIter(x - 1, y, region);
        paintBorderIter(x, y + 1, region);
        paintBorderIter(x, y - 1, region);
        paintBorderIter(x + 1, y + 1, region);
        paintBorderIter(x + 1, y - 1, region);
        paintBorderIter(x - 1, y + 1, region);
        paintBorderIter(x - 1, y - 1, region);
    }

    private void paintBorderIter(int x, int y, int[][] region) {
        if (x < 0 || x >= region.length || y < 0 || y >= region[0].length) {
            return;
        }
        if (region[x][y] == 1) {
            return;
        }
        region[x][y] = 2;
    }

    private int getAllUniqueBorders(int[][] region) {
        int borders = 0;
        boolean done = false;
        while (!done) {
            
            boolean found = false;
            for (int i = 0; i < region.length; i++) {
                for (int j = 0; j < region[i].length; j++) {
                    if (region[i][j] == 2) {
                        borders += traiceBorder(i, j, region, 1, 0);
                        borders += traiceBorder(i, j, region, -1, 0);
                        borders += traiceBorder(i, j, region, 0, 1);
                        borders += traiceBorder(i, j, region, 0, -1);
                        found = true;
                        break;
                    }
                }
                if (found) {
                    break;
                }
            }
            if (!found) {
                // didnt find a border to scan -> exit
                done = true;
            }
        }
        return borders;
    }

    private int traiceBorder(int x, int y, int[][] region, int direX, int dirY) {
        if (x < 0 || x >= region.length || y < 0 || y >= region[0].length || x + direX < 0 || x + direX >= region.length || y + dirY < 0 || y + dirY >= region[0].length) {
            return 0;
        }
        // end condition
        if (region[x][y] != 2) {
            return 0;
        }
        region[x][y] = 3;
        if (region[x + direX][y + dirY] == 2) {
            return traiceBorder(x + direX, y + dirY, region, direX, dirY);
        }
        int count = 1;
        count += traiceBorder(x + 1, y, region, 1, 0);
        count += traiceBorder(x - 1, y, region, -1, 0);
        count += traiceBorder(x, y + 1, region, 0, 1);
        count += traiceBorder(x, y - 1, region, 0, -1);
        return count;
    }


    private class RegionProperties {
        public int size;
        public int perimeter;
        public char cropType;
        public int id;

        public RegionProperties(int size, int perimiter, char cropType, int id) {
            this.size = size;
            this.perimeter = perimiter;
            this.cropType = cropType;
            this.id = id;
        }

        public void combine(RegionProperties other) {
            this.size += other.size;
            this.perimeter += other.perimeter - 2;
        }
    }

}