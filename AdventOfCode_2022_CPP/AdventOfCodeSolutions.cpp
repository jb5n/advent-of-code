
#include <algorithm>
#include <functional>
#include <fstream>
#include <iostream>
#include <string>

#include "AdventOfCodeSolutions.h"

using namespace std;

AdventOfCodeSolutions::AdventOfCodeSolutions() {
	solutions[1] = &AdventOfCodeSolutions::Day1;
}

void AdventOfCodeSolutions::SolveDay(int day) {
	if (solutions.find(day) == solutions.end()) {
		cout << "ERR: Failed to find solution for day " << day << endl;
		return;
	}

	const string filename = "input/day" + to_string(day) + ".txt";
	ifstream file(filename);
	if (!file.is_open()) {
		cout << "ERR: Failed to open file " << filename << ". Does it exist?" << endl;
		return;
	}
	
	vector<string> readlines;
	string line;
	while (getline(file, line)) {
		readlines.push_back(line);
	}

	solutions[day](*this, readlines);
}

void AdventOfCodeSolutions::Day1(const vector<string>& lines) {
	vector<int> leftNums, rightNums;
	for (const string& line : lines) {
		vector<string> splits = SplitString(line, " ");
		if (splits.size() != 2) {
			cout << "LINE HAS BAD NUMBER OF SPLITS\n";
			continue;
		}
		leftNums.push_back(stoi(splits[0]));
		rightNums.push_back(stoi(splits[1]));
	}
	sort(leftNums.begin(), leftNums.end());
	sort(rightNums.begin(), rightNums.end());

	int totalDistance = 0;
	for (int i = 0; i < leftNums.size(); i++) {
		totalDistance += abs(leftNums[i] - rightNums[i]);
	}
	cout << "Day 1 part 1: " << totalDistance << endl;

	int similarityTotal = 0;
	map<int, int> similarityScores;
	for (const int& leftNum : leftNums) {
		if (similarityScores.find(leftNum) == similarityScores.end()) {
			int scoreForLeftNum = 0;
			for (const int& rightNum : rightNums) {
				if (rightNum == leftNum) {
					scoreForLeftNum++;
				}
			}
			similarityScores[leftNum] = leftNum * scoreForLeftNum;
		}

		similarityTotal += similarityScores[leftNum];
	}

	cout << "Day 1 part 2: " << similarityTotal << endl;
}

vector<string> AdventOfCodeSolutions::SplitString(string input, const string& delimiter, bool removeEmpties) const {
	vector<string> splitStrings;
	string substring;
	int foundIndex = 0;
	while ((foundIndex = input.find(delimiter)) != string::npos) {
		substring = input.substr(0, foundIndex);
		if (!removeEmpties || substring.length() > 0) {
			splitStrings.push_back(substring);
		}
		input.erase(0, foundIndex + delimiter.length());
	}
	splitStrings.push_back(input);
	return splitStrings;
}
