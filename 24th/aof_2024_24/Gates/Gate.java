package aof_2024_24.Gates;

import java.util.HashMap;

public abstract class Gate {
    protected Gate input1;
    protected Gate input2;
    protected boolean isSet;
    protected boolean value;

    public Gate(Gate input1, Gate input2) {
        this.input1 = input1;
        this.input2 = input2;
    }

    protected abstract boolean doOperation();

    public boolean getValue() {
        if (!this.isSet) {
            // do operation will get the value of the input gates if necessary
            this.value = this.doOperation();
            this.isSet = true;
        }
        return this.value;
    }

    public void setInputs(String name, HashMap<String, String[]> gateWirering, HashMap<String, Gate> gateObjects) {
        if (this.input1 != null) {
            // was already set
            return;
        }
        String[] wiring = gateWirering.get(name);
        this.input1 = gateObjects.get(wiring[0]);
        this.input2 = gateObjects.get(wiring[1]);
        this.input1.setInputs(wiring[0], gateWirering, gateObjects);
        this.input2.setInputs(wiring[1], gateWirering, gateObjects);
    }

    @Override
    public String toString() {
        if (this.input1 != null && this.input2 != null) {
            return this.input1.toString() + " " + this.getClass().getSimpleName() + " " + this.input2.toString();
        }
        return this.getClass().getSimpleName();
    }
}
