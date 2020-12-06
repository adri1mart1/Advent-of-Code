// https://adventofcode.com/2020/day/6
// g++ day6.cpp -o pgm
#include <iostream>
#include <fstream>
#include <algorithm>
#include <vector>
#include <ctype.h>
#include <numeric>
#include <sstream>

void get_sum_of_yeses(std::string &s, int &any, int &every) {

	std::vector<int> alph;
	alph.resize(26);

	std::string word;
	int num_word = 0;
	std::stringstream ss(s);

	while (ss >> word) {
		num_word++;

		for (char &c: word) {
			if (isalpha(c)) {
				alph[(int)c-97]++;
			}
		}
	}

	for (auto &i: alph) {
		if (i == num_word) 
			every++;
		if (i > 0)
			any++;
	}

	s = "";
}

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	std::string group_answer;
	int any = 0, every = 0;

	while (std::getline(infile, line)) {
		if (line.empty())
			get_sum_of_yeses(group_answer, any, every);
		else
			group_answer += line + " ";
	}
	get_sum_of_yeses(group_answer, any, every);

	std::cout << "Part1: Any yeses sum: " << any << std::endl;
	std::cout << "Part2: Every yeses sum: " << every << std::endl;
	
	return 0;
}