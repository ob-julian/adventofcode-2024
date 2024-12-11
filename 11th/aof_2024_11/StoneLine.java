package aof_2024_11;

import java.util.*;
import java.math.BigInteger;

public class StoneLine {

    private LinkedList<Stone> stones;

    public StoneLine(String[] lines) {
        this.stones = new LinkedList<>();
        if (lines.length != 1) {
            throw new IllegalArgumentException("Invalid input");
        }
        String[] numbers = lines[0].split(" ");
        for (String number : numbers) {
            this.stones.add(new Stone(BigInteger.valueOf(Integer.parseInt(number))));
        }
    }

    @Override
    public String toString() {
        return Arrays.toString(stones.toArray());
    }

    public void blink(int times) {
        for (int i = 0; i < times; i++) {
            ListIterator<Stone> iterator = stones.listIterator();
            while (iterator.hasNext()) {
                Stone stone = iterator.next();
                Stone[] newStone = stone.applyRule();
                if (newStone.length == 2) {
                    iterator.add(newStone[1]);
                }
            }
        }
    }

    public BigInteger blink_optimised(int times) {
        // better than blink, but still not good enough for 75 iterations
        BigInteger count = BigInteger.ZERO;
        for (Stone stone : this.stones) {
            count = count.add(blink_optimised_iter(times, stone));
        }
        return count;
    }

    public BigInteger blink_optimised_iter(int times, Stone stone) {
        if (times == 0) {
            return BigInteger.ONE;
        }
        Stone[] newStones = stone.applyRule();
        BigInteger count = BigInteger.ZERO;
        for (Stone newStone : newStones) {
            count = count.add(blink_optimised_iter(times - 1, newStone));
        }
        return count;
    }
        

    public int countStones() {
        return this.stones.size();
    }
}
