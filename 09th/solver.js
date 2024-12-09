const path = require('path');
const fs = require('fs');
const LinkedList = require('./linkedList.js');
const Data = require('./data.js');

function readFile(file) {
    const filePath = path.join(__dirname, file);
    return fs.readFileSync(filePath, 'utf8');
}

function generateHash(data) {
    let hash = 0;
    for(let i = 0; i < data.length; i++) {
        hash += i * data[i]
    }
    return hash;
}

function generateHashFromDataList(dataList) {
    let hash = 0;
    for(let i = 0; i < dataList.length; i++) {
        let position = dataList[i].position;
        for (let j = 0; j < dataList[i].size; j++) {
            hash += position * dataList[i].id;
            position++;
        }
    }
    return hash;
}

function toStringFromDataList(dataList) {
    let size = 0;
    for (let data of dataList) {
         size = Math.max(size, data.position + data.size);
    }
    let result = new Array(size).fill('.');
    for (let data of dataList) {
        let position = data.position;
        for (let i = 0; i < data.size; i++) {
            result[position] = data.id;
            position++;
        }
    }
    return result.join('');
}

function solve1(data) {
    let id = 0;
    let frontIndex = 0;
    let backIndex = data.length - 1;
    let remainingSymbols = parseInt(data[backIndex]);
    let backId = Math.floor(backIndex / 2);

    let result = [];

    let isData = true;
    let isDone = false;
    while (!isDone) {
        const symbol = parseInt(data[frontIndex]);
        frontIndex++;
        if (isData) {
            for(let _ = 0; _ < symbol; _++) {
                result.push(id);
            }
            id++;
        } else {
            for(let _ = 0; _ < symbol; _++) {
                if (remainingSymbols <= 0) {
                    backId--;
                    backIndex -= 2;
                    if (backId <= id) {
                        isDone = true;
                        break;
                    }
                    remainingSymbols = parseInt(data[backIndex]);
                }
                if (remainingSymbols > 0) {
                    result.push(backId);
                    remainingSymbols--;
                }
            }
                
        }
        isData = !isData;
        if (frontIndex >= backIndex) {
            isDone = true;
            break;
        }
    }
    for (let i = 0; i < remainingSymbols; i++) {
        result.push(backId);
    }
    return generateHash(result);
}



function solve2(data) {
    let isData = true;
    let freeList = new LinkedList(0, 0);
    let root = freeList;
    let dataList = [];
    let position = 0;
    let id = 0;
    for (let i = 0; i < data.length; i++) {
        const size = parseInt(data[i]);

        if (isData) {
            const data = new Data(id, size, position);
            dataList.push(data);
            id++;
        } else {
            freeList = freeList.addNode(size, position);
        }
        position += size;
        isData = !isData;
    }
    // remove first dummy node and set freeList to List start
    freeList = root.next;

    for (let i = dataList.length - 1; i >= 0; i--) {
        const dataObj = dataList[i];
        const freeNode = freeList.findBigEnoughNode(dataObj.size);
        if (freeNode !== null && freeNode.position < dataObj.position) {
            const oldPosition = dataObj.position;
            dataObj.position = freeNode.position;
            const newFreeSize = freeNode.size - dataObj.size;
            if (newFreeSize > 0) {
                freeNode.size = newFreeSize;
                freeNode.position += dataObj.size;
            } else {
                freeNode.removeThisNode();
                if (freeNode === freeList) {
                    // root case
                    freeList = freeNode.next;
                }
            }
            freeList.addNodeInOrder(dataObj.size, oldPosition);
        }
    }
    //console.log(toStringFromDataList(dataList));
    return generateHashFromDataList(dataList);
}


//const data = readFile('test.txt');
const data = readFile('input.txt');

console.log("Advent of Code: 03rd");
console.log("Part 1: ", solve1(data));
console.log("Part 2: ", solve2(data));