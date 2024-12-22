#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <cmath>

using namespace std;

// file reader
vector<string> read_file(string filename) {
    vector<string> lines;
    ifstream file(filename);
    if (file.is_open()) {
        string line;
        while (getline(file, line)) {
            lines.push_back(line);
        }
        file.close();
    }
    return lines;
}

unsigned long long mix(unsigned long long a, unsigned long long b) {
    return a ^ b; // bitwise XOR
}

unsigned long long prune(unsigned long long a) {
    return a % 16777216; // modulo x
}

unsigned long long step1(unsigned long long secretNumber) {
    return prune(mix(secretNumber, secretNumber * 64));
}

unsigned long long step2(unsigned long long secretNumber) {
    return prune(mix(secretNumber, floor(secretNumber / 32)));
}

unsigned long long step3(unsigned long long secretNumber) {
    return prune(mix(secretNumber, secretNumber * 2048));
}

unsigned long long nextSecretNumber(unsigned long long secretNumber) {
    return step3(step2(step1(secretNumber)));
}

unsigned long long solve1(vector<string> data) {
    int iterations = 2000;
    unsigned long long accumulator = 0;
    for (string line : data) {
        unsigned long long secretNumber = stoull(line);
        for (int i = 0; i < iterations; i++) {
            secretNumber = nextSecretNumber(secretNumber);
        }
        accumulator += secretNumber;
    }
    return accumulator;
}

int getPrice(unsigned long long secretNumber, int changeSequence, int signsSequence) {
    int iterations = 2000;
    int changes = 0; // base 10
    int signs = 0; // base 10, base 2 would suffice, but converting is a hassle
    int lastPrice = secretNumber % 10;

    for (int i = 0; i < iterations; i++) {
        secretNumber = nextSecretNumber(secretNumber);
        int newPrice = secretNumber % 10;
        int diff = newPrice - lastPrice;
        lastPrice = newPrice;
        // prepare free right shift
        changes = (changes * 10) % 10000;
        signs = (signs * 10) % 10000;

        // update changes and signs
        changes += abs(diff);
        if (diff < 0) {
            signs += 1;
        }

        if (i >= 3) {
            // check if we found a sequence
            if (changes == changeSequence && signs == signsSequence) {
                return newPrice;
            }
        }
    }
    return 0;
}

bool checkIfNotValid(int sequence[]) {
    int sums[10] = {0, 1, 2, 3, 4, 5, 6, 7, 8, 9};
    bool vailds[10] = {true, true, true, true, true, true, true, true, true, true};
    for (int i = 0; i < 4; i++) {
        for (int j = 0; j < 10; j++) {
            sums[j] += sequence[i];
            if (sums[j] < 0 || sums[j] > 9) {
                vailds[j] = false;
            }
        }
        bool allFalse = true;
        for (int j = 0; j < 10; j++) {
            allFalse = allFalse && !vailds[j];
        }
        if (allFalse) {
            return true;
        }
    }
    return false;
}

int getPrice(unsigned long long secretNumber, int sequence[]) {
    int singsSequence = 0;
    int changeSequence = 0;
    for (int i = 0; i < 4; i++) {
        changeSequence *= 10; // will be ignored for the first iteration -> times 0
        singsSequence *= 10;
        changeSequence += abs(sequence[i]);
        if (sequence[i] < 0) {
            singsSequence += 1;
        }
    }
    return getPrice(secretNumber, changeSequence, singsSequence);
}

bool increaseSequence(int sequence[]) {
    for (int i = 0; i < 4; i++) {
        if (sequence[i] == 9) {
            sequence[i] = -9;
        } else {
            sequence[i]++;
            return true;
        }
    }
    // sequence is full
    return false;
}

int findPattern(const string& str, const string& pattern) {
    size_t index = str.find(pattern);

    if (index != string::npos) {
        return static_cast<int>(index);
    } else {
        return -1;
    }
}

// optimized via regex and and precalculations
int solve2(vector<string> data) {
    int iterations = 2000;
    int amountTrader = data.size();

    //char differenceChars[amountTrader][2*iterations+1]; //  sign + number and null terminator
    //int prices[amountTrader][iterations];

    // after stack is too small, use heap
    vector<vector<char>> differenceChars(amountTrader, vector<char>(2 * iterations + 1));
    vector<vector<int>> prices(amountTrader, vector<int>(iterations));

    for (int i = 0; i < amountTrader; i++) {
        int secretNumber = stoi(data[i]);
        prices[i][0] = secretNumber % 10;
        differenceChars[i][0] = 'a'; // dummy value, because no difference for the first price, dummy to ensure it does not interfere with the later algorithm
        differenceChars[i][1] = 'a';
        differenceChars[i][2*iterations] = '\0';
        for (int j = 1; j < iterations; j++) {
            secretNumber = nextSecretNumber(secretNumber);
            prices[i][j] = secretNumber % 10;

            differenceChars[i][2*j] = prices[i][j] < prices[i][j-1] ? '-' : '+';
            differenceChars[i][2*j + 1] = '0' + abs(prices[i][j] - prices[i][j-1]);
        }
    }
    vector<string> difference(amountTrader);
    for (int i = 0; i < amountTrader; i++) {
        difference[i] = string(differenceChars[i].begin(), differenceChars[i].end());
    }
    // free memory
    differenceChars.clear();

    // precalculations done
    int max = 0;
    int sequence[] = {-9, -9, -9, -9};
    do {
        if (checkIfNotValid(sequence)) {
            continue;
        }
        int aquired = 0;
        char charSequence[9];
        for (int i = 0; i < 4; i++) {
            charSequence[2*i] = sequence[i] < 0 ? '-' : '+';
            charSequence[2*i + 1] = '0' + abs(sequence[i]);
        }
        charSequence[8] = '\0';
        string stringSequence = charSequence;

        for (int i = 0; i < amountTrader; i++) {
            int index = findPattern(difference[i], stringSequence);
            if (index != -1) {
                aquired += prices[i][(index + 6) / 2];
            }
        }

        if (aquired > max) {
            max = aquired;
        }
        
    } while (increaseSequence(sequence));
    return max;
        
}

// brute force way
int solve2_tooSlow(vector<string> data) {
    vector<unsigned long long> secretNumbers;
    for (string line : data) {
        secretNumbers.push_back(stoull(line));
    }
    int max = 0;
    int sequence[] = {-9, -9, -9, -9};
    do  {
        if (checkIfNotValid(sequence)) {
            continue;
        }
        int aquired = 0;
        for (unsigned long long secretNumber : secretNumbers) {
            unsigned long long price = getPrice(secretNumber, sequence);
            aquired += price;
        }
        if (aquired > max) {
            max = aquired;
        }
    } while (increaseSequence(sequence));
    return max;
}

int main() {
    cout << "Advent of Code 2024 - Day 22" << endl;
    vector<string> data = read_file("input.txt");
    //vector<string> data = read_file("test.txt");
    //cout << "Part 1: " << solve1(data) << endl;
    //cout << "Part 2: " << solve2_tooSlow(data) << endl; // test needs 8.7 secs, real input too long
    cout << "Part 2: " << solve2(data) << endl; // test needs 2.5 secs, real input 35 mins, could be /8 if parallelized
    return 0;
}