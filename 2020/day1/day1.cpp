// https://adventofcode.com/2020/day/1
// g++ day1.cpp -o pgm -std=c++11
#include <iostream>
#include <fstream>
#include <vector>

int main(int argc, char *argv[]) {
	std::vector<unsigned> vect;

	std::ifstream infile("in.txt");
	unsigned a;

	while (infile >> a)
		vect.push_back(a);

	for (auto &a: vect) {
		for (auto &b: vect) {
			if ((a + b) == 2020) {
				std::cout << "Part1: Found a:" << a << " and b:" << b << " product:" << a*b << std::endl;
				goto part2;
			}
		}
	}

part2:
	for (auto &a: vect) {
		for (auto &b: vect) {
			for (auto &c: vect) {
				if ((a + b + c) == 2020) {
					std::cout << "Part2: Found a:" << a << " and b:" << b << " and c:" << c
					          << " product:" << a*b*c << std::endl;
					goto end;
				}
			}

		}
	}

end:
	return 0;
}