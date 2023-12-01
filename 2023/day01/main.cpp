#include <iostream>
#include <string>
#include <fstream>
#include <algorithm>
#include <cassert>

using namespace std;

static const string input{"in.txt"};

int get_num(const string &s, const bool consider_letters = false) {
	static const array<string, 10> numbers{
		"zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine"
	};

	if (isdigit(s[0])) {
		return s[0] - 48;
	} else {
		if (consider_letters) {
			for (const auto& number: numbers) {
				if (string_view(s).starts_with(number)) {
					const auto it = find(numbers.begin(), numbers.end(), number);
					return  it - numbers.begin();
				}
			}
		}
	}
	return -1;
}

int get_first_num(const string& s, const bool consider_letters = false) {
	for (unsigned int i=0; i<s.size(); ++i) {
		if (const auto res = get_num(s.substr(i), consider_letters); res != -1)
			return res;
	}
	return -1;
}

int get_last_num(const string& s, const bool consider_letters = false) {
	for (unsigned int i=s.size()-1;;--i) {
		if (const auto res = get_num(s.substr(i), consider_letters); res != -1)
			return res;
	}
	return -1;
}

int main() {
	ifstream ifs{input};
	string line;
	unsigned int total_p1, total_p2 = 0;

	while (getline(ifs, line)) {

		// remove trailing \n
		line.erase(line.length()-1);

		const auto p1_n1 = get_first_num(line);
		const auto p1_n2 = get_last_num(line);

		const auto p2_n1 = get_first_num(line, true);
		const auto p2_n2 = get_last_num(line, true);

		assert (p1_n1 != -1 && p1_n2 != -1 && p2_n1 != -1 && p2_n2 != -1);

		total_p1 += p1_n1 * 10 + p1_n2;
		total_p2 += p2_n1 * 10 + p2_n2;
	}

	cout << "Part1: sum of all of the calibration values: " << total_p1 << endl;
	cout << "Part2: sum of all of the calibration values: " << total_p2 << endl;

	return 0;
}
