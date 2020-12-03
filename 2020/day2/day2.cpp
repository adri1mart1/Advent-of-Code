// https://adventofcode.com/2020/day/2
// g++ day2.cpp -o pgm
#include <iostream>
#include <fstream>
#include <sstream>

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	int part1_total = 0;
	int part2_total = 0;

	while (std::getline(infile, line)) {

		std::stringstream linestream(line);
		int min, max;
		char unused, letter;
		std::string password;

		linestream >> min >> unused >> max >> letter >> unused >> password;

		int cnt = 0;
		for (char &c: password) {
			if (c == letter)
				cnt++;
		}

		if (min <= cnt && cnt <= max)
			part1_total++;

		if ((password[min-1] == letter && password[max-1] != letter) ||
			(password[min-1] != letter && password[max-1] == letter))
			part2_total++;
	}

	std::cout << "part 1 total answer is: " << part1_total << std::endl;
	std::cout << "part 2 total answer is: " << part2_total << std::endl;

	return 0;
}