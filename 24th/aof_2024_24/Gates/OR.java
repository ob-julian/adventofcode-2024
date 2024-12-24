package aof_2024_24.Gates;

public class OR extends Gate {
    public OR(Gate input1, Gate input2) {
        super(input1, input2);
    }

    protected boolean doOperation() {
        return this.input1.getValue() | this.input2.getValue();
    }
    
}
