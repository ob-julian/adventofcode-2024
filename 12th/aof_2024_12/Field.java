package aof_2024_12;

import java.util.Set;
import java.math.BigInteger;

public class Field {
    private Region[][] regions;

    public Field(String[] lines) {
        this.regions = new Region[lines.length][lines[0].length()];
        int id = 0;
        for (int i = 0; i < lines.length; i++) {
            for (int j = 0; j < lines[i].length(); j++) {
                this.regions[i][j] = new Region(1, 4, lines[i].charAt(j), id, i, j);
                id++;
            }
        }
    }

    public void joinRegionsHorizontally() {
        for (int y = 0; y < this.regions.length; y++) {
            for (int x = 0; x < this.regions[y].length - 1; x++) {
                joinRegions(y, x, y, x + 1);
            }
        }
    }

    public void joinRegionsVertically() {
        for (int y = 0; y < this.regions.length - 1; y++) {
            for (int x = 0; x < this.regions[y].length; x++) {
                joinRegions(y, x, y + 1, x);
            }
        }
    }

    private void joinRegions(int y1, int x1, int y2, int x2) {
        if (this.regions[y1][x1].getCropType() == this.regions[y2][x2].getCropType()) {
            if (this.regions[y1][x1].equals(this.regions[y2][x2])) {
                // same region, just remove fence between them
                this.regions[y1][x1].removeFence();
            } else {
                this.regions[y1][x1].combine(this.regions[y2][x2]);

            }
        }
    }

    public void joinAllRegions() {
        joinRegionsHorizontally();
        joinRegionsVertically();
    }

    public BigInteger calculateCost() {
        Set<Region> regions = new java.util.HashSet<Region>();
        for (int i = 0; i < this.regions.length; i++) {
            for (int j = 0; j < this.regions[i].length; j++) {
                regions.add(this.regions[i][j]);
            }
        }
        BigInteger cost = BigInteger.ZERO;

        for(Region region : regions) {
            cost = cost.add(BigInteger.valueOf(region.getSize()).multiply(BigInteger.valueOf(region.getPerimeter())));
        }
        return cost;
    }

    public BigInteger calculateDiscountCost() {
        Set<Region> regions = new java.util.HashSet<Region>();
        for (int i = 0; i < this.regions.length; i++) {
            for (int j = 0; j < this.regions[i].length; j++) {
                regions.add(this.regions[i][j]);
            }
        }
        BigInteger cost = BigInteger.ZERO;

        for(Region region : regions) {
            cost = cost.add(BigInteger.valueOf(region.getSize()).multiply(BigInteger.valueOf(region.getindividualRegionBorders())));
        }
        return cost;
    }

    public String regionsToString() {
        StringBuilder sb = new StringBuilder();
        for (int i = 0; i < this.regions.length; i++) {
            for (int j = 0; j < this.regions[i].length; j++) {
                sb.append(this.regions[i][j].getCropType() + "/" + this.regions[i][j].getId() + " ");
            }
            sb.append("\n");
        }
        return sb.toString();
    }
}
