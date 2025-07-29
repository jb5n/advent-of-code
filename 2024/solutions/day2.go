package main

import "fmt"

type Day2Solution struct{}

func (s Day2Solution) part1() {
	input, err := readInputLines("day2")
	if err != nil {
		panic(err)
	}

	var safeReports int
	for _, line := range input {
		levels, err := splitToInts(line, " ")
		if err != nil {
			panic(err)
		}
		if len(levels) < 2 {
			continue
		}
		startedIncreasing := levels[1] > levels[0]
		isSafe := true
		for i := 1; i < len(levels); i++ {
			isIncreasing := levels[i] > levels[i-1]
			levelChange := absInt(levels[i] - levels[i-1])
			if isIncreasing != startedIncreasing || levelChange == 0 || levelChange > 3 {
				isSafe = false
				break
			}
		}
		if isSafe {
			safeReports++
		}
	}
	fmt.Printf("Safe report count: %d\n", safeReports)
}

func (s Day2Solution) part2() {

}
