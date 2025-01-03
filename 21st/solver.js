const path = require('path');
const fs = require('fs');

function readFile(file) {
    const filePath = path.join(__dirname, file);
    return fs.readFileSync(filePath, 'utf8').split('\n').map(line => line.trim());
}

function getPadWrapper(code, start, functionToCall) {
    let current = start;
    let sequence = '';
    for (let i = 0; i < code.length; i++) {
        const sequencesBetween = functionToCall(current, code[i]);
        let bestSequence = "";
        let bestCost = Infinity;
        for (let sequenceBetween of sequencesBetween) {
            const cost = costCalculator(sequenceBetween[0], sequenceBetween[sequenceBetween.length - 1]) + costCalculator(sequenceBetween[sequenceBetween.length - 1], 'A');
            if (cost < bestCost) {
                bestCost = cost;
                bestSequence = sequenceBetween;
            }
        }
        sequence += bestSequence + 'A';
        current = code[i];
   }
   return sequence;
}

function getKeypadSequence(code) {
    return getPadWrapper(code, 'A', getSequenceBetweenNumbers);
}

function getLetterPadSequence(code) {
    return getPadWrapper(code, 'A', getSequenceBetweenLetters);
}

function sequenceWrapper(fromNum, toNum, numToPos, seu1, seu2) {
    if (fromNum === toNum) {
        return '';
    }
    const fromPos = numToPos[fromNum];
    const toPos = numToPos[toNum];

    const sequence1 = 'v'.repeat(Math.max(0, toPos.y - fromPos.y));
    const sequence2 = '^'.repeat(Math.max(0, fromPos.y - toPos.y));
    const sequence3 = '>'.repeat(Math.max(0, toPos.x - fromPos.x));
    const sequence4 = '<'.repeat(Math.max(0, fromPos.x - toPos.x));
    const sequences = new Set();
    sequences.add(sequence1 + sequence2 + sequence3 + sequence4);
    sequences.add(sequence3 + sequence4 + sequence1 + sequence2);

    // dont go over empty space
    if (seu1.includes(fromNum) && seu2.includes(toNum)) {
        sequences.delete(sequence1 + sequence2 + sequence3 + sequence4);
    }
    if (seu2.includes(fromNum) && seu1.includes(toNum)) {
        sequences.delete(sequence3 + sequence4 + sequence1 + sequence2);
    }
    return Array.from(sequences);
}

function getSequenceBetweenNumbers(fromNum, toNum) {
        /*
    +---+---+---+
    | 7 | 8 | 9 |
    +---+---+---+
    | 4 | 5 | 6 |
    +---+---+---+
    | 1 | 2 | 3 |
    +---+---+---+
        | 0 | A |
        +---+---+
    */
    const numToPos = {
        "7": {x: 0, y: 0},
        "8": {x: 1, y: 0},
        "9": {x: 2, y: 0},
        "4": {x: 0, y: 1},
        "5": {x: 1, y: 1},
        "6": {x: 2, y: 1},
        "1": {x: 0, y: 2},
        "2": {x: 1, y: 2},
        "3": {x: 2, y: 2},
        "0": {x: 1, y: 3},
        "A": {x: 2, y: 3}
    };
    const seu1 = ["7", "4", "1"];
    const seu2 = ["0", 'A'];
    return sequenceWrapper(fromNum, toNum, numToPos, seu1, seu2);
}

function getSequenceBetweenLetters(fromLetter, toLetter) {
    /*
        +---+---+
        | ^ | A |
    +---+---+---+
    | < | v | > |
    +---+---+---+
    */
    const toPos = {
        '^': {x: 1, y: 0},
        'A': {x: 2, y: 0},
        '<': {x: 0, y: 1},
        'v': {x: 1, y: 1},
        '>': {x: 2, y: 1}
    };
    const seu1 = ['<'];
    const seu2 = ['^', 'A'];
    return sequenceWrapper(fromLetter, toLetter, toPos, seu1, seu2);
}

function costCalculator(sequenceStart , roboStart) {
    if (sequenceStart === roboStart) {
        return 0;
    }
    const lookup = {
        'A^': 1,
        'A>': 1,
        'Av': 2,
        'A<': 3,

        '^v': 1,
        '^<': 2,
        '^>': 2,

        '>v': 1,
        '><': 2,

        'v<': 1,
    };
    if (lookup[sequenceStart + roboStart] !== undefined) {
        return lookup[sequenceStart + roboStart];
    }
    return lookup[roboStart + sequenceStart];
}


function solve1(data) {
    let sum = 0;
    let repetitions = 3;
    for (let code of data) {
        let keyPadSequence = getKeypadSequence(code);
        for (let i = 0; i < repetitions-1; i++) {
            keyPadSequence = getLetterPadSequence(keyPadSequence);
        }
        sum += keyPadSequence.length * parseInt(code.substring(0, code.length - 1));
    }
    return sum;
}

function solve2(data) {
    let sum = 0;
    let repetitions = 26;
    for (let code of data) {
        console.log("Code: ", code);
        let keyPadSequence = getKeypadSequence(code);
        for (let i = 0; i < repetitions-1; i++) {
            console.log("Iteration: ", i);
            keyPadSequence = getLetterPadSequence(keyPadSequence);
        }
        sum += keyPadSequence.length * parseInt(code.substring(0, code.length - 1));
    }
    return sum;
}


//const data = readFile('test.txt');
const data = readFile('input.txt');

console.log("Advent of Code: 21rd");
console.log("Part 1: ", solve1(data));
console.log("Part 2: ", solve2(data));



function codeToSmaler(code) {
    const positions = [
        [' ', '^', 'A'],
        ['<', 'v', '>']
    ]
    let sequence = '';
    let position = {x:2, y:0};
    for (let letter of code) {
        if (position.x < 0 || position.x > 2 || position.y < 0 || position.y > 1) {
            console.error("Invalid position");
            break;
        }
        if (positions[position.y][position.x] === " ") {
            console.error("Invalid position");
            break;
        }
        if (letter === 'A') {
            sequence += positions[position.y][position.x];
            continue;
        }
        switch (letter) {
            case '<':
                position.x -= 1;
                break;
            case '>':
                position.x += 1;
                break;
            case '^':
                position.y -= 1;
                break;
            case 'v':
                position.y += 1;
                break;
        }
    }
    return sequence;
}
