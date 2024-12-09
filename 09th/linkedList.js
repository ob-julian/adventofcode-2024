class LinkedList {
    constructor(size, position) {
        this.size = size;
        this.position = position;
        this.next = null;
        this.prev = null; // needed for Node removal
        // maybe optimise with a bigger pointer
    }

    addNode(size, position) {
        if (size <= 0) {
            return this;
        }
        if (this.next === null) {
        this.next = new LinkedList(size, position);
        this.next.prev = this;
        return this.next;
        }
        
        // in case we dont append to the end of list
        console.log("List Element is not last, appending to end");
        let current = this.next;
        while (current.next !== null) {
            current = current.next;
        }
    
        current.next = new LinkedList(size, position);
        current.next.prev = current;
        return current.next;
    }

    addNodeInOrder(size, position) {
        if (size <= 0) {
            return;
        }
        let current = this;
        let smaller = null;
        while ( current !== null && current.position < position) {
            smaller = current;
            current = current.next;
        }
        if (smaller === null) {
            //could happen in last move but correct list is irrelevant then so we just skip
            return;
        }
        // add up free space if possible
        let wasSizeAdded = false;
        // add up left
        if (smaller !== null && smaller.position + smaller.size === position) {
            smaller.size += size;
            wasSizeAdded = true;
        }
        
        // add up right
        if (smaller.next !== null && smaller.next.position === position + size) {
            if (wasSizeAdded) {
                smaller.size += smaller.next.size;
                smaller.next.removeThisNode();
            } else {
                smaller.next.position = position;
                smaller.next.size += size;
            }
            return;
        }
        // else
        if (smaller.next === null) {
            smaller.addNode(size, position);
            return;
        }
        const newNode = new LinkedList(size, position);
        newNode.prev = smaller;
        newNode.next = smaller.next;
        smaller.next.prev = newNode;
        smaller.next = newNode;
    }
                

    findBigEnoughNode(value) {
        let current = this;
        while (current !== null) {
            if (current.size >= value) {
                return current;
            }
            current = current.next;
        }
        return null;
    }

    removeThisNode() {
        if (this.prev !== null) {
            this.prev.next = this.next;
        }
        if (this.next !== null) {
            this.next.prev = this.prev;
        }
    }

    toString() {
        let current = this;
        let result = "";
        while (current !== null) {
            result += `Size: ${current.size}, Position: ${current.position} -> `;
            current = current.next;
        }
        return result;
    }
}

module.exports = LinkedList;