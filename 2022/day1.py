# Advent of Code 2022 Day 1
# Justin Bostian

with open('day1.txt') as f:
	lines = f.readlines()
	maxCalories = 0
	secondMaxCalories = 0
	thirdMaxCalories = 0
	curCalories = 0
	for line in lines:
		if line == '\n':
			if curCalories > maxCalories:
				thirdMaxCalories = secondMaxCalories
				secondMaxCalories = maxCalories
				maxCalories = curCalories
			elif curCalories > secondMaxCalories:
				thirdMaxCalories = secondMaxCalories
				secondMaxCalories = curCalories
			elif curCalories > thirdMaxCalories:
				thirdMaxCalories = curCalories
			curCalories = 0
		else:
			curCalories += int(line)
	print("Calories from top three elves: " + str(maxCalories + secondMaxCalories + thirdMaxCalories))
