
#include <algorithm>
#include <functional>
#include <fstream>
#include <iostream>
#include <string>

#include "AdventOfCodeSolutions.h"

using namespace std;

AdventOfCodeSolutions::AdventOfCodeSolutions() {
	solutions[1] = &AdventOfCodeSolutions::Day1;
	solutions[2] = &AdventOfCodeSolutions::Day2;
	solutions[3] = &AdventOfCodeSolutions::Day3;
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
