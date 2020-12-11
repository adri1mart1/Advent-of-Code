// https://adventofcode.com/2020/day/9
// g++ day9.cpp -o pgm -std=c++11
#include <iostream>
#include <fstream>
#include <vector>
#include <algorithm>

static const unsigned preamble_len = 25;

bool xmas_valid(std::vector<unsigned> &v, unsigned to, unsigned from, unsigned value) {
	for (int i=to; i<from; i++) {
		for (int j=to+1; j<from; j++) {
			if (v[i] + v[j] == value)
				return true;
		}
	}
	return false;
}

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::vector<unsigned> digits;
	std::string line;
	unsigned idx = 0;
	unsigned weak_num = 0;

	while (getline(infile, line)) {

		digits.push_back(std::stoul(line));

		if (idx > preamble_len) {
			if (!xmas_valid(digits, idx - preamble_len, idx, digits.back())) {
				std::cout << "Part1: Value: " << digits[idx] << " at idx " << idx << " doesn't respect xmas property" << std::endl;
				weak_num = digits[idx];
				break;
			}
		}
		idx++;
	}

	for (int n=2; n<25; n++) { // sum with Nth digits
		for (int i=0; i<idx; i++) { // loop in all digits

			unsigned sum = std::accumulate(digits.begin()+i, digits.begin()+i+n, 0);

			if (sum > weak_num)
				break;

			if (sum == weak_num) {

				std::vector<unsigned> mini_vect;
				for (int j=0; j<n; j++)
					mini_vect.push_back(digits.at(i+j));

				unsigned min_val = *std::min_element(mini_vect.begin(), mini_vect.end());
				unsigned max_val = *std::max_element(mini_vect.begin(), mini_vect.end());

				std::cout << "Part2: Addition of min: " << min_val << " and max: " << max_val << " is: " << min_val + max_val << std::endl;
				return 0;
			}
		}
	}
	return 0;
}