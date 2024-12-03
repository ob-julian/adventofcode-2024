const path = require('path');
const fs = require('fs');

function readFile(file) {
    const filePath = path.join(__dirname, file);
    return fs.readFileSync(filePath, 'utf8');
}

function uncorupt(data) {
    return data.match(/mul\(\d+,\d+\)/g);
}

function executeInstructions(instructionSets) {
    sum = 0;
    for (let i = 0; i < correct.length; i++) {
        values = correct[i].match(/\d+/g);
        sum += parseInt(values[0]) * parseInt(values[1]);
    }
    return sum;
}

function splitInDoAndDont(data) {
    // For correctly using Lookahead, thx Copilot
    return data.match(/(do(n't)?\(\))?.*?(?=((do(n't)?\(\))|$))/g);
}

function solve1(data) {
    correct = uncorupt(data);
    if (correct === null) {
        return 0;
    }
    return executeInstructions(correct);
}

function solve2(data) {
    let sum = 0;
    const instructionSets = splitInDoAndDont(data);
    sum = solve1(instructionSets[0]);
    if (instructionSets.length > 1) {
        for (let i = 1; i < instructionSets.length; i++) {
            if (instructionSets[i].startsWith("do()")) {
                sum += solve1(instructionSets[i]);
            }
        }
    }
    return sum;
}


//const data = readFile('test_1.txt');
//const data = readFile('test_2.txt');
const data = readFile('input.txt');

console.log("Advent of Code: 03rd");
console.log("Part 1: ", solve1(data));
console.log("Part 2: ", solve2(data));