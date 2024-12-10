package aof_2024_10;

public class Path {
    private Map map;
    private Position trailHead;
    private Position currentPos;
    private int expectedElevation;
    private boolean isComplete;

    public Path(Map map, Position trailHead, Position currentPos, int elevation) {
        this.map = map;
        this.trailHead = trailHead;
        this.currentPos = currentPos;
        this.expectedElevation = elevation;
        this.isComplete = this.expectedElevation == 9;
    }

    public Path(Map map, Position trailHead) {
        this(map, trailHead, trailHead, 0);
    }

    public int getExpectedElevation() {
        return this.expectedElevation;
    }

    public boolean isComplete() {
        return this.isComplete;
    }

    public Position getTrailHead() {
        return this.trailHead;
    }

    public Position getCurrentPos() {
        return this.currentPos;
    }

    public Path nextStep(int x, int y) {
        Position newPos = new Position(this.currentPos.x + x, this.currentPos.y + y);
        if (this.map.isValid(newPos) && this.map.get(newPos) == this.expectedElevation + 1) {
            return new Path(this.map, this.trailHead, newPos, this.expectedElevation + 1);
        }
        return null;
    }

    public Path[] continuePaths() {
        Path[] paths = new Path[4];
        paths[0] = nextStep(0, 1);
        paths[1] = nextStep(1, 0);
        paths[2] = nextStep(0, -1);
        paths[3] = nextStep(-1, 0);
        return paths;
    }
}
