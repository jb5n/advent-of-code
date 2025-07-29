package main

import (
	"bufio"
	"os"
	"strconv"
	"strings"
)

type DaySolution interface {
	part1()
	part2()
}

func readLines(path string) ([]string, error) {
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()

	var lines []string
	scanner := bufio.NewScanner(file)
	for scanner.Scan() {
		lines = append(lines, scanner.Text())
	}
	return lines, scanner.Err()
}

func readInputLines(inputFilename string) ([]string, error) {
	return readLines("../input/" + inputFilename + ".txt")
}

func splitToInts(inputStr string, sep string) (splitInts []int, err error) {
	splitStrings := strings.Split(inputStr, sep)
	splitInts = make([]int, len(splitStrings))
	for i, splitStr := range splitStrings {
		asInt64, err := strconv.ParseInt(splitStr, 10, 64)
		if err != nil {
			return nil, err
		}
		splitInts[i] = int(asInt64)
	}
	return splitInts, nil
}

func absInt(x int) int {
	if x < 0 {
		return -x
	}
	return x
}
