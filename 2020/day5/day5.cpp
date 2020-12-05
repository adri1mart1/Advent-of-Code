// https://adventofcode.com/2020/day/5
// g++ day5.cpp -o pgm
#include <iostream>
#include <fstream>
#include <math.h>
#include <vector>
#include <algorithm>

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	unsigned max_seat_id = 0;
	std::vector<int> ids;

	while (std::getline(infile, line)) {

		unsigned row_min = 0, row_max = 127;

		for (int i=0; i<7; i++) {
			char &c = line[i];
			double d = ceil((double)(row_max - row_min) / 2);
			if (c == 'F')
				row_max -= d;
			else
				row_min += d;
		}

		unsigned col_min = 0, col_max = 7;

		for (int i=7; i<10; i++) {
			char &c = line[i];
			double d = ceil((double)(col_max - col_min) / 2);
			if (c == 'R')
				col_min += d;
			else
				col_max -= d;
		}

		unsigned seat_id = row_min * 8 + col_max;
		if (seat_id > max_seat_id)
			max_seat_id = seat_id;

		ids.push_back(seat_id);
	}

	std::cout << "Part1: max seat id: " << max_seat_id << std::endl;

	std::sort(ids.begin(), ids.end());

	for (int i=0; i<ids.size()-1; i++) {
		if (ids[i]+1 != ids[i+1])
			std::cout << "Part2: found empty seat with id: " << ids[i]+1 << std::endl;
	}

	return 0;
}