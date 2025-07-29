package main

import (
	"fmt"
	"sort"
	"strconv"
	"strings"
)

type Day1Solution struct{}

func (s Day1Solution) part1() {
	input, err := readInputLines("day1")
	if err != nil {
		panic(err)
	}

	listA, listB := make([]int, len(input)), make([]int, len(input))
	for i, line := range input {
		splitLine := strings.Split(line, "   ")
		lineA, err := strconv.ParseInt(splitLine[0], 10, 64)
		if err != nil {
			panic(err)
		}
		lineB, err := strconv.ParseInt(splitLine[1], 10, 64)
		if err != nil {
			panic(err)
		}
		listA[i] = int(lineA)
		listB[i] = int(lineB)
	}
	sort.Ints(listA)
	sort.Ints(listB)
	var distance int
	for i := range len(input) {
		distance += max(listA[i], listB[i]) - min(listA[i], listB[i])
	}
	fmt.Printf("Part 1 total distance: %d\n", distance)
}

func (s Day1Solution) part2() {
	input, err := readLines("../input/day1.txt")
	if err != nil {
		panic(err)
	}

	leftList := make([]int, len(input))
	numInstancesMap := make(map[int]int)
	for i, line := range input {
		splitLine := strings.Split(line, "   ")
		lineA, err := strconv.ParseInt(splitLine[0], 10, 64)
		if err != nil {
			panic(err)
		}
		lineB, err := strconv.ParseInt(splitLine[1], 10, 64)
		if err != nil {
			panic(err)
		}
		leftList[i] = int(lineA)
		if _, ok := numInstancesMap[int(lineB)]; ok {
			numInstancesMap[int(lineB)]++
		} else {
			numInstancesMap[int(lineB)] = 1
		}
	}

	var similarityScore int
	for _, element := range leftList {
		if count, ok := numInstancesMap[element]; ok {
			similarityScore += count * element
		}
	}
	fmt.Printf("Part 2 similarity score: %d\n", similarityScore)
}
