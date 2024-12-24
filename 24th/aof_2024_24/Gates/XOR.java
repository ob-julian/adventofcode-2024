package aof_2024_24.Gates;

public class XOR extends Gate {
    public XOR(Gate input1, Gate input2) {
        super(input1, input2);
    }

    protected boolean doOperation() {
        return this.input1.getValue() ^ this.input2.getValue();
    }
}
