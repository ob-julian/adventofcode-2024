package aof_2024_11;

import java.math.BigInteger;

public class Stone {
    BigInteger number; // AI was used to switch from int to BigInteger

    public Stone(int number) {
        this.number = BigInteger.valueOf(number);
    }

    public Stone(BigInteger number) {
        this.number = number;
    }

    public Stone[] applyRule() {
        if (this.number.equals(BigInteger.ZERO)) {
            this.number = BigInteger.ONE;
            return new Stone[]{this};
        }
        int numberLength = this.number.toString().length();
        if (numberLength % 2 == 0) {
            BigInteger oldNumber = this.number;
            BigInteger shift = BigInteger.TEN.pow(numberLength / 2);
            this.number = this.number.divide(shift);
            return new Stone[]{this, new Stone(oldNumber.subtract(this.number.multiply(shift)))};
        }
        this.number = this.number.multiply(BigInteger.valueOf(2024));
        return new Stone[]{this};
    }

    @Override
    public String toString() {
        return this.number.toString();
    }

}