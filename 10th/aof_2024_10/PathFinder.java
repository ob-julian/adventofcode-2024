package aof_2024_10;

import java.util.*;

public class PathFinder {

    private Map map;
    private Queue<Path> queue = new LinkedList<>();
    // why calculate all paths twice?
    private Path[] cachedPaths;

    public PathFinder(Map map) {
        this.map = map;
    }

    public int findAllPathsFor1() {
        Position[] trailHeads = this.map.findAllElevations(0);
        if (this.cachedPaths == null) {
            this.cachedPaths = findAllPaths(trailHeads);
        }
        return scoreTrails(trailHeads, this.cachedPaths);
    }

    public int findAllPathsFor2() {
        Position[] trailHeads = this.map.findAllElevations(0);
        if (this.cachedPaths == null) {
            this.cachedPaths = findAllPaths(trailHeads);
        }
        return this.cachedPaths.length;
    }

    public Path[] findAllPaths(Position[] trailHeads) {
        for (Position trailHead : trailHeads) {
            Path path = new Path(this.map, trailHead);
            this.queue.add(path);
        }

        LinkedList<Path> completePaths = new LinkedList<>();
        while (!this.queue.isEmpty()) {
            Path path = this.queue.poll();
            Path[] nextPaths = path.continuePaths();
            for (Path nextPath : nextPaths) {
                if (nextPath != null) {
                    if (nextPath.isComplete()) {
                        completePaths.add(nextPath);
                    } else {
                        this.queue.add(nextPath);
                    }
                }
            }
        }
        return completePaths.toArray(new Path[0]);
    }

    public int scoreTrails(Position[] trailHeads, Path[] paths) {
        // assert: all path are finished
        HashMap<Position, Set<Position>> pathsByTrailHead = new HashMap<>();
        for (Position trailHead : trailHeads) {
            pathsByTrailHead.put(trailHead, new HashSet<>());
        }
        for (Path path : paths) {
            pathsByTrailHead.get(path.getTrailHead()).add(path.getCurrentPos());
        }
        int score = 0;
        for (Position key : pathsByTrailHead.keySet()) {
            score += pathsByTrailHead.get(key).size();
        }
        return score;
    }

}
