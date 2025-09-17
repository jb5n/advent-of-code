#pragma once

#include <functional>
#include <map>
#include <string>
#include <vector>

using namespace std;

class AdventOfCodeSolutions;
typedef function<void(AdventOfCodeSolutions&, const vector<string>&)> SolutionFunction;

class AdventOfCodeSolutions
{
public:
	AdventOfCodeSolutions();

	void SolveDay(int index);

private:
	// Day solutions
	void Day1(const vector<string>& lines);
	void Day2(const vector<string>& lines);
	void Day3(const vector<string>& lines);

	// Utilities
	vector<string> SplitString(string input, const string& delimiter, bool removeEmpties = true) const;

	// Member variables
	map<int, SolutionFunction> solutions;
};
