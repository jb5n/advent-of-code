
#include <algorithm>
#include <functional>
#include <fstream>
#include <iostream>
#include <set>
#include <string>

#include "AdventOfCodeSolutions.h"

using namespace std;

AdventOfCodeSolutions::AdventOfCodeSolutions() {
	solutions[1] = &AdventOfCodeSolutions::Day1;
	solutions[2] = &AdventOfCodeSolutions::Day2;
	solutions[3] = &AdventOfCodeSolutions::Day3;
	solutions[4] = &AdventOfCodeSolutions::Day4;
	solutions[5] = &AdventOfCodeSolutions::Day5;
	solutions[6] = &AdventOfCodeSolutions::Day6;
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

void AdventOfCodeSolutions::Day2(const vector<string>& lines) {
	int safeReports = 0;

	auto isReportSafe = [](const vector<int>& report) {
		vector<int> sortedReportAsc = report;
		sort(sortedReportAsc.begin(), sortedReportAsc.end());
		vector<int> sortedReportDesc = report;
		sort(sortedReportDesc.begin(), sortedReportDesc.end(), greater<int>());
		if (sortedReportDesc != report && sortedReportAsc != report) {
			return false;
		}
		for (int i = 1; i < report.size(); i++) {
			if (report[i] == report[i - 1] || abs(report[i] - report[i - 1]) > 3) {
				return false;
			}
		}
		return true;
	};

	vector<vector<int>> unsafeReports;
	for (const string& line : lines) {
		const vector<string> splitStrings = SplitString(line, " ");
		vector<int> report(splitStrings.size());
		transform(splitStrings.begin(), splitStrings.end(), report.begin(),
			[](string input) { return stoi(input); });

		if (isReportSafe(report)) {
			safeReports++;
		}
		else {
			unsafeReports.push_back(report);
		}
	}

	cout << "Safe reports: " << safeReports << endl;

	for (const vector<int>& unsafeReport : unsafeReports) {
		for (int i = 0; i < unsafeReport.size(); i++) {
			vector<int> tryReport = unsafeReport;
			tryReport.erase(tryReport.begin() + i);
			if (isReportSafe(tryReport)) {
				safeReports++;
				break;
			}
		}
	}

	cout << "With problem dampener: " << safeReports << endl;
}

void AdventOfCodeSolutions::Day3(const vector<string>& lines) {
	int mulTotalIgnoringDonts = 0;
	int mulTotalWithDonts = 0;
	
	string fullInput;
	for (const string& line : lines) {
		fullInput += line;
	}

	int foundIndex = fullInput.find("mul(");
	while (foundIndex != string::npos) {
		int nextFoundIndex = fullInput.find("mul(", foundIndex + 1);

		int lastDontOccurrence = fullInput.rfind("don't()", foundIndex);
		int lastDoOccurrence = fullInput.rfind("do()", foundIndex);
		bool enabled = lastDontOccurrence == string::npos || lastDoOccurrence > lastDontOccurrence;

		const int searchEnd = nextFoundIndex == string::npos ? fullInput.length() : nextFoundIndex;
		enum SearchStage { FIRST_NUM, SECOND_NUM };
		SearchStage stage = FIRST_NUM;
		string firstNumStr, secondNumStr;
		bool isValidMul = false;
		for (int i = foundIndex + 4; i < searchEnd; i++) {
			if (stage == FIRST_NUM) {
				if (isdigit(fullInput[i])) {
					firstNumStr += fullInput[i];
				}
				else if (fullInput[i] == ',' && !firstNumStr.empty()) {
					stage = SECOND_NUM;
				}
				else {
					break;
				}
			}
			else if (stage == SECOND_NUM) {
				if (isdigit(fullInput[i])) {
					secondNumStr += fullInput[i];
				}
				else if (fullInput[i] == ')' && !secondNumStr.empty()) {
					isValidMul = true;
					break;
				}
				else {
					break;
				}
			}
		}

		if (isValidMul) {
			int num1 = stoi(firstNumStr);
			int num2 = stoi(secondNumStr);
			mulTotalIgnoringDonts += num1 * num2;
			if (enabled) {
				mulTotalWithDonts += num1 * num2;
			}
		}

		foundIndex = nextFoundIndex;
	}

	cout << "Original multiplication total: " << mulTotalIgnoringDonts << endl;
	cout << "Multiplication total avoiding Dont blocks: " << mulTotalWithDonts << endl;
}

void AdventOfCodeSolutions::Day4(const vector<string>& lines) {
	int xmasCounts = 0;

	auto posIsCh = [lines](int row, int col, char testChar) {
		if (row < 0 || col < 0 || row >= lines.size() || col >= lines[row].length()) {
			return false;
		}
		return lines[row][col] == testChar;
	};

	auto evalFunc = [lines, posIsCh](int xRow, int xCol) {
		int evalPositionals[8][3][2] = {
			{ {  0,  1 }, {  0,  2 }, {  0,  3 } }, // horizontal fwd
			{ {  0, -1 }, {  0, -2 }, {  0, -3 } }, // horizontal bwd
			{ {  1,  0 }, {  2,  0 }, {  3,  0 } }, // vertical downward
			{ { -1,  0 }, { -2,  0 }, { -3,  0 } }, // vertical upward
			{ {  1,  1 }, {  2,  2 }, {  3,  3 } }, // pointing SE
			{ { -1,  1 }, { -2,  2 }, { -3,  3 } }, // pointing NE
			{ {  1, -1 }, {  2, -2 }, {  3, -3 } }, // pointing NW
			{ { -1, -1 }, { -2, -2 }, { -3, -3 } } // pointing SW
		};

		int count = 0;
		for (const auto& evalPositional : evalPositionals) {
			if (posIsCh(xRow + evalPositional[0][0], xCol + evalPositional[0][1], 'M') &&
				posIsCh(xRow + evalPositional[1][0], xCol + evalPositional[1][1], 'A') &&
				posIsCh(xRow + evalPositional[2][0], xCol + evalPositional[2][1], 'S')) {
				count++;
			}
		}
		return count;
	};
	
	for (int row = 0; row < lines.size(); row++) {
		for (int col = 0; col < lines[row].length(); col++) {
			if (lines[row][col] == 'X') {
				xmasCounts += evalFunc(row, col);
			}
		}
	}

	cout << "Found XMAS " << xmasCounts << " times\n";

	int xShapedMasCount = 0;

	auto xShapedEvalFunc = [lines, posIsCh](int aRow, int aCol) {
		// NW-SE axis
		bool hasNWSE = false;
		if ((posIsCh(aRow - 1, aCol - 1, 'M') && posIsCh(aRow + 1, aCol + 1, 'S')) ||
			(posIsCh(aRow - 1, aCol - 1, 'S') && posIsCh(aRow + 1, aCol + 1, 'M'))) {
			hasNWSE = true;
		}
		bool hasNESW = false;
		if ((posIsCh(aRow - 1, aCol + 1, 'M') && posIsCh(aRow + 1, aCol - 1, 'S')) ||
			(posIsCh(aRow - 1, aCol + 1, 'S') && posIsCh(aRow + 1, aCol - 1, 'M'))) {
			hasNESW = true;
		}

		return hasNWSE && hasNESW;
	};

	for (int row = 0; row < lines.size(); row++) {
		for (int col = 0; col < lines[row].length(); col++) {
			if (lines[row][col] == 'A') {
				if (xShapedEvalFunc(row, col)) {
					xShapedMasCount++;
				}
			}
		}
	}

	cout << "Found X-MAS (X-shaped MAS) " << xShapedMasCount << " times\n";
}

void AdventOfCodeSolutions::Day5(const vector<string>& lines) {
	map<int, vector<int>> requiredPredecessors;
	auto evaluatePredecessors = [requiredPredecessors](int evalIndex, vector<int> instructions) {

	};

	int middlePageNumTotal = 0;
	bool evaluatingPredecessors = true;
	vector<vector<int>> disorderedInstructions;
	for (const string& line : lines) {
		if (line.empty() && evaluatingPredecessors) {
			evaluatingPredecessors = false;
			continue;
		}
		if (evaluatingPredecessors) {
			vector<string> split = SplitString(line, "|");
			int predecessor = stoi(split[0]);
			int successor = stoi(split[1]);
			requiredPredecessors[successor].push_back(predecessor);
			continue;
		}

		vector<string> instructionStrs = SplitString(line, ",");
		vector<int> instructions(instructionStrs.size());
		transform(instructionStrs.begin(), instructionStrs.end(), instructions.begin(),
			[](const string& st) { return stoi(st); });

		bool isOrdered = true;
		for (int i = 0; i < instructions.size(); i++) {
			vector<int> predecessors = requiredPredecessors[instructions[i]];
			if (predecessors.empty()) {
				continue;
			}
			for (const int& predecessor : predecessors) {
				auto predecessorIt = find(instructions.begin(), instructions.end(), predecessor);
				if (predecessorIt == instructions.end()) {
					continue;
				}
				int indexOfPredecessor = distance(instructions.begin(), predecessorIt);
				if (indexOfPredecessor > i) {
					isOrdered = false;
					break;
				}
			}
			if (!isOrdered) {
				break;
			}
		}

		if (!isOrdered) {
			disorderedInstructions.push_back(instructions);
			continue;
		}
		
		int middleValue = instructions[(instructions.size() - 1) / 2];
		middlePageNumTotal += middleValue;
	}

	cout << "Middle page num total " << middlePageNumTotal << endl;

	auto sortFunc = [&requiredPredecessors](int instA, int instB) {
		// return true if a should go before b
		if (requiredPredecessors.find(instA) != requiredPredecessors.end()) {
			vector<int> predecessorsOfA = requiredPredecessors[instA];
			if (find(predecessorsOfA.begin(), predecessorsOfA.end(), instB) != predecessorsOfA.end()) {
				// B is a predecessor of A, B should be before A
				return false;
			}
		}
		return true;
	};

	int correctedMiddlePageNumTotal = 0;
	for (vector<int> instructions : disorderedInstructions) {
		sort(instructions.begin(), instructions.end(), sortFunc);

		int middleValue = instructions[(instructions.size() - 1) / 2];
		correctedMiddlePageNumTotal += middleValue;
	}

	cout << "Corrected middle page num total " << correctedMiddlePageNumTotal << endl;
}

void AdventOfCodeSolutions::Day6(const vector<string>& lines) {
	pair<int, int> pos(-1, -1);
	for (int y = 0; y < lines.size(); y++) {
		for (int x = 0; x < lines[y].length(); x++) {
			if (lines[y][x] == '^') {
				pos = pair<int, int>(x, y);
				break;
			}
		}
		if (pos.first != -1) {
			break;
		}
	}

	pair<int, int> stepCycle[4] = { pair(0, -1), pair(1, 0), pair(0, 1), pair(-1, 0) };
	int stepCycleIndex = 0;

	auto isOnMap = [lines](const pair<int, int>& evalPos) {
		return evalPos.first >= 0 && evalPos.first < lines[0].length() &&
			evalPos.second >= 0 && evalPos.second < lines.size();
	};

	set<pair<int, int>> stepLocations;
	stepLocations.insert(pos);
	while (isOnMap(pos)) {
		pair<int, int>& stepDir = stepCycle[stepCycleIndex];
		pair<int, int> evalPos(pos.first + stepDir.first, pos.second + stepDir.second);
		if (!isOnMap(evalPos)) {
			break;
		}
		if (lines[evalPos.second][evalPos.first] == '#') {
			stepCycleIndex = (stepCycleIndex + 1) % 4;
		}
		else {
			pos = evalPos;
			stepLocations.insert(pos);
		}
	}

	cout << "Guard stepped in " << stepLocations.size() << " unique positions\n";

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
