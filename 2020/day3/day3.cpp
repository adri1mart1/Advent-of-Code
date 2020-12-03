// https://adventofcode.com/2020/day/3
// g++ day3.cpp -o pgm
#include <iostream>
#include <vector>
#include <fstream>

static const unsigned map_pattern_len = 31;

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::vector<std::string> map;
	std::string line;

	std::vector<std::pair<unsigned, unsigned>> slopes;
	slopes.push_back({1,1});
	slopes.push_back({3,1});
	slopes.push_back({5,1});
	slopes.push_back({7,1});
	slopes.push_back({1,2});

	unsigned res = 1;

	while (std::getline(infile, line))
		map.push_back(line);

	for (auto &s: slopes) {
		std::pair<unsigned, unsigned> coord = {0,0};
		unsigned trees = 0;

		while (coord.second < map.size()-s.second) {
			coord.first += s.first;
			coord.first %= map_pattern_len;
			coord.second += s.second;

			if (map.at(coord.second)[coord.first] == '#')
				trees++;
		}

		std::cout << "slope (" << s.first << ";" << s.second << ") has " << trees << " trees" << std::endl;
		res *= trees;
	}

	std::cout << "Product of all trees found: " << res << std::endl;	
	return 0;
}