// https://adventofcode.com/2020/day/4
// g++ day4.cpp -o pgm
#include <iostream>
#include <vector>
#include <fstream>
#include <regex>

bool get_value(std::string in, std::string needle, std::string &v) {
	std::size_t found_needle = in.find(needle);
	if (found_needle != std::string::npos) {
		std::string str1 = in.substr(found_needle);
		std::size_t found_value = str1.find_first_of(":");
		if (found_value != std::string::npos) {
			std::size_t space = str1.substr(found_value+1).find(" ");
			if (space != std::string::npos) {
				v = str1.substr(found_value+1, space);
				return true;
			}
		}
	}
	return false;
}

class Passport {
public:
	Passport(std::string &in) :
		ppt(in) {}

	bool check_if_int_in_range(int v, int min, int max, std::string var) {
		if (v >= min && v <= max) 
			return true;
		return false;
	}

	bool check_eye_color(std::string ecl) {
		const std::vector<std::string> vect = { "amb", "blu", "brn", "gry", "grn", "hzl", "oth" };
		for (auto &v: vect) {
			if (v == ecl) 
				return true;
		}
		return false;
	}

	bool check_height() {
		unsigned height = std::stoi(hgt);
		if (hgt.find("cm") != std::string::npos && height >= 150 && height <= 193)
			return true;
		if (hgt.find("in") != std::string::npos && height >= 59 && height <= 76)
			return true;
		return false;
	}

	bool check_passport_id() {
		if (pid.size() == 9) {
			for (char &c: pid) {
				if (!isdigit(c) && c != '_')
					return false;
			}
			return true;
		}
		return false;
	}

	bool check_hair_color() {
		if (std::regex_match(hcl, std::regex("#[0-9a-f]{6}")))
			return true;
		return false;
	}

	bool has_enough_info() {
		if (get_value(ppt, "byr", byr) &&
			get_value(ppt, "iyr", iyr) &&
			get_value(ppt, "eyr", eyr) &&
			get_value(ppt, "hgt", hgt) &&
			get_value(ppt, "hcl", hcl) &&
			get_value(ppt, "ecl", ecl) &&
			get_value(ppt, "pid", pid))

			return true;
		return false;
	}

	bool is_valid() {
		if (check_if_int_in_range(std::stoi(byr), 1920, 2002, "byr") &&
			check_if_int_in_range(std::stoi(iyr), 2010, 2020, "iyr") &&
			check_if_int_in_range(std::stoi(eyr), 2020, 2030, "eyr") &&
			check_height() &&
			check_hair_color() &&
			check_passport_id() && 
			check_eye_color(ecl))
			
			return true;
		return false;
	}

	std::string ppt;
	std::string byr, iyr, eyr, hgt, cid;
	std::string hcl, ecl, pid;
};

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::vector<Passport> passeports;
	std::string line;
	std::string in;

	while (std::getline(infile, line)) {
		if (line.empty()) {
			passeports.push_back(Passport(in));
			in = "";
		} else {
			in += line + " ";
		}
	}
	passeports.push_back(Passport(in));


	unsigned cnt1 = 0, cnt2 = 0;
	for (auto &p: passeports) {
		if (p.has_enough_info()) {
			cnt1++;
			if (p.is_valid())
				cnt2++;
		}
	}

	std::cout << "Part1: total number of passports with enough information: " << cnt1 << std::endl;
	std::cout << "Part2: total number of valid passports: " << cnt2 << std::endl;

	return 0;
}