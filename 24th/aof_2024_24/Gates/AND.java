package aof_2024_24.Gates;

public class AND extends Gate {
    public AND(Gate input1, Gate input2) {
        super(input1, input2);
    }

    protected boolean doOperation() {
        return this.input1.getValue() & this.input2.getValue();
    }
}
