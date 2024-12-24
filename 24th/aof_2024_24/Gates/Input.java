package aof_2024_24.Gates;

import java.util.HashMap;

public class Input extends Gate {
    private boolean value;

    public Input(boolean value) {
        super(null, null);
        this.value = value;
    }

    public boolean getValue() {
        return this.value;
    }

    protected boolean doOperation() {
        return this.value;
    }

    @Override
    public String toString() {
        return this.value ? "1" : "0";
    }

    @Override
    public void setInputs(String name, HashMap<String, String[]> gateWirering, HashMap<String, Gate> gateObjects) {
        // do nothing
    }
    
}
