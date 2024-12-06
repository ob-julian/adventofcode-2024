package aof_2024_06;

public class ObstacleFinder {

    private Map map;

    public ObstacleFinder(Map map) {
        this.map = map;
    }

    public int findAmountOfLoopingObstacles(int[][] possibleObstacles) {
        int amountOfLoopingObstacles = 0;
        for (int[] obstacle : possibleObstacles) {
            if (this.map.setObstacle(obstacle[0], obstacle[1])) {
                Guard guard = map.findInitialGuardPosition();
                while (guard.move());
                if (guard.getStatus() == GuardStatus.LOOPING) {
                    amountOfLoopingObstacles++;
                }
                this.map.removeObstacle();
            }
        }
        return amountOfLoopingObstacles;
    }   

}
