package aof_2024_24;

import java.io.BufferedReader;
import java.io.FileReader;
import java.io.IOException;
import java.util.*;

import aof_2024_24.Gates.*;

public class FileParser {
    private String filename;
    private String[] lines;
    private HashMap<String, Boolean> startingWire;
    private HashMap<String, String[]> gateWirering;
    private HashMap<String, Gate> gateObjects;
    private HashMap<String, Gate> endGates;

    public FileParser(String filename) {
        this.filename = filename;
    }

    public FileParser readFile() {
        List<String> lines = new ArrayList<>();
        try (BufferedReader br = new BufferedReader(new FileReader(this.filename))) {
            String line;
            while ((line = br.readLine()) != null) {
                lines.add(line);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        this.lines = lines.toArray(new String[0]);
        return this;
    }

    public FileParser parseFile() {
        boolean isStarting = true;
        startingWire = new HashMap<>();
        gateWirering = new HashMap<>();
        gateObjects = new HashMap<>();
        endGates = new HashMap<>();

        for (String line : this.lines) {
            if (line.isEmpty()) {
                isStarting = false;
                continue;
            }
            if (isStarting) {
                String[] parts = line.split(": ");
                startingWire.put(parts[0], parts[1].equals("1"));
            } else {
                String[] parts = line.split(" ");
                String input1 = parts[0];
                String input2 = parts[2];
                String output = parts[4];
                String type = parts[1];
                Gate gate = getGate(type);
                gateObjects.put(output, gate);
                gateWirering.put(output, new String[]{input1, input2});
                if (output.startsWith("z")) {
                    endGates.put(output, gate);
                }
            }
        }
        for (Map.Entry<String, Boolean> entry : startingWire.entrySet()) {
            String name = entry.getKey();
            boolean value = entry.getValue();
            gateObjects.put(name, new Input(value));
        }
        for (Map.Entry<String, Gate> entry : endGates.entrySet()) {
            String name = entry.getKey();
            Gate gate = entry.getValue();
            gate.setInputs(name, gateWirering, gateObjects);
        }

        return this;
    }

    private Gate getGate(String type) {
        switch (type) {
            case "AND":
                return new AND(null, null);
            case "OR":
                return new OR(null, null);
            case "XOR":
                return new XOR(null, null);
            default:
                return null;
        }
    }

    public long endGatesToInt() {
        // let ai do the sorting part, could not be bothered to look up the correct way to do this
        long result = 0;
        // sorted endGates, desending order
        List<String> sortedEndGates = new ArrayList<>(endGates.keySet());
        sortedEndGates.sort(Comparator.reverseOrder());
        for (String name : sortedEndGates) {
            Gate gate = endGates.get(name);
            result = (result << 1) | (gate.getValue() ? 1 : 0);
        }
        return result;
    }
}