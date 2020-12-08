// https://adventofcode.com/2020/day/6
// g++ day8.cpp -o pgm
#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <ctype.h>
#include <numeric>
#include <sstream>
#include <string>

int run_program(std::vector<std::string> &pgm, bool part1) {
	// if part1 enabled
	//    return acc value when infinite loop is detected
	// else // part2
	//    return -1 if infinite loop, acc value otherwise

	unsigned idx = 0, acc = 0;
	std::vector<int> seen;

	while (1) {

		if (idx >= pgm.size())
			return acc;

		if (std::find(seen.begin(), seen.end(), idx) != seen.end()) {
			if (part1)
				return acc;
			return -1;
		}
		seen.push_back(idx);

		std::stringstream linestream(pgm.at(idx));
		std::string action;
		int value;
		linestream >> action >> value;

		if (action == "nop")
			idx++;

		else if (action == "acc") {
			acc += value;
			idx++;

		} else if (action == "jmp")
			idx += value;
	}
	return -1;
}

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	std::vector<std::string> init_program;

	while (std::getline(infile, line))
		init_program.push_back(line);

	std::cout << "Part1: Accumulator value: " << run_program(init_program, true) << std::endl;

	unsigned idx = 0;

	while (1) {

		std::vector<std::string> program = init_program;

		while (init_program.at(idx).find("acc") != std::string::npos)
			idx++;

		std::stringstream linestream(init_program.at(idx));

		std::string action, new_action;
		int value;
		linestream >> action >> value;

		if (action == "nop")
			new_action = "jmp";
		else
			new_action = "nop";

		program.at(idx) = new_action + " " + std::to_string(value);

		int result = run_program(program, false);
		if (result != -1) {
			std::cout << "Part2: Accumulator value: " << result << std::endl;
			break;
		}

		idx++;
	}

	return 0;
}