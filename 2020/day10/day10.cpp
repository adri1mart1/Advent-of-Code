// https://adventofcode.com/2020/day/10
// g++ day10.cpp -o pgm -std=c++11
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	std::vector<unsigned> vect;

	while (getline(infile, line))
		vect.push_back(std::stoul(line));

	std::sort(vect.begin(), vect.end());

	unsigned diff1 = 1, diff3 = 1;

	for (int i=0; i<vect.size()-1; i++) {
		if (vect.at(i+1) - vect.at(i) == 1)
			diff1++;
		else
			diff3++;
	}
	std::cout << "Part1: diff1: " << diff1 << " x diff3: " << diff3 << " = " << diff3 * diff1  << std::endl;

	vect.insert(vect.begin(), 0);
	vect.push_back(vect.back() + 3); // built in

	std::vector<unsigned long> path;
	path.push_back(1);

	for (int i=1; i<vect.size(); ++i) {
		int j=i-1;
		unsigned long p = path[j];
		while (--j >= 0) {
			if (vect[i]-vect[j] <= 3)
				p += path[j];
		}
		path.push_back(p);
	}
	std::cout << "Part2: Number of possible paths is " << path.back() << std::endl;

	return 0;
}