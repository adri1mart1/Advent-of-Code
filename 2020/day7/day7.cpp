// https://adventofcode.com/2020/day/7
// g++ day7.cpp -o pgm
#include <iostream>
#include <iomanip>
#include <fstream>
#include <vector>
#include <sstream>
#include <map>
#include <regex>
#include <iterator>

/*
 * Definitely not the best program I made but did the job, in a dirty way
 *
 * the idea is to build a matrix of number to be able to find how many
 * bags are contained within a bag AND vice versa
 *
 * As an example with the in_ex.txt file, we have the map:
 *
 *    map:
 *   .0.1.2.0.0.0.0.0.0    light red
 *   .0.0.0.0.1.0.0.0.0    bright white
 *   .0.0.0.0.2.9.0.0.0    muted yellow
 *   .0.3.4.0.0.0.0.0.0    dark orange
 *   .0.0.0.0.0.0.1.2.0    shiny gold
 *   .0.0.0.0.0.0.0.0.0    faded blue
 *   .0.0.0.0.0.3.0.0.4    dark olive
 *   .0.0.0.0.0.5.0.0.6    vibrant plum
 *   .0.0.0.0.0.0.0.0.0    dotted black
 *
 * Then, I used 2 recursive functions to find counts of bags within or
 * contained for the target bag.
 *
 * Working well but still, quite a shame :o
 */
std::map<std::string, unsigned> bag_idx;
std::map<unsigned, std::string> idx_bag;
static std::vector<std::string> used_vect;
static unsigned idx = 0;

void add_bag(std::string bag) {
	if (bag_idx.find(bag) == bag_idx.end()) {
		bag_idx.insert(std::pair<std::string, unsigned>(bag, idx));
		idx_bag.insert(std::pair<unsigned, std::string>(idx++, bag));
	}
}

void display_map(std::vector<std::vector<unsigned>> &m) {
	std::cout << "map:" << std::endl;

	for (int i=0; i<m.size(); i++) {
		for (int j=0; j<m[i].size(); j++)
			std::cout << "." << m[i][j];
		std::cout << "    " << idx_bag.at(i) << std::endl;
	}
	std::cout << std::endl;
}

bool if_bag_in_vector(std::vector<std::string> v, std::string bag) {
	if (std::find(v.begin(), v.end(), bag) != v.end())
		return true;
	return false;
}

int get_number_of_bags_containing(std::vector<std::vector<unsigned>> &m, std::string bag) {

	int result = 0;

	if (if_bag_in_vector(used_vect, bag))
		return 0;

	used_vect.push_back(bag);

	for (int i=0; i<idx; i++) {
		if (m[i][bag_idx.at(bag)] > 0 && !if_bag_in_vector(used_vect, idx_bag.at(i)))
			result += get_number_of_bags_containing(m, idx_bag.at(i)) + 1;
	}
	return result;
}

int get_number_of_bags_within(std::vector<std::vector<unsigned>> &m, std::string bag) {
	int result = 0;

	for (int i=0; i<idx; i++) {
		if (m[bag_idx.at(bag)][i] > 0) {
			result += m[bag_idx.at(bag)][i];
			result += get_number_of_bags_within(m, idx_bag.at(i)) * m[bag_idx.at(bag)][i];
		}
	}
	return result;
}

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;

	std::vector<std::vector<int>> vect;
	std::vector<std::string> known_bags;

	// First read all different bags
	while (std::getline(infile, line)) {

		std::regex first_bag_regex(R"(^[a-z]+\s[a-z]+)");
		std::smatch match;
		if (std::regex_search(line, match, first_bag_regex)) {
			add_bag(match.str());
			line = match.suffix();
		}

		std::regex r(R"(\d\s([a-z]+\s[a-z]+))");
		std::smatch sm;
		while (std::regex_search(line, sm, r)) {
		    add_bag(sm.str(1));
		    line = sm.suffix();
		}
	}

	// Init a 2D vector
	std::vector<std::vector<unsigned>> matrix;
	matrix.resize(bag_idx.size());
	for (auto &v: matrix)
		v.resize(bag_idx.size());

	// Re read all file and feed 2D vector
	infile.clear();
	infile.seekg(0, std::ios::beg);

	while (std::getline(infile, line)) {

		std::string main_bag;

		std::regex first_bag_regex(R"(^[a-z]+\s[a-z]+)");
		std::smatch match;
		if (std::regex_search(line, match, first_bag_regex)) {
			main_bag = match.str();
			line = match.suffix();
		}

		std::regex r(R"((\d)\s([a-z]+\s[a-z]+))");
		std::smatch sm;
		while (std::regex_search(line, sm, r)) {
			std::string bag = sm.str(2);
			unsigned quantity = std::stoul(sm.str(1));
			matrix[bag_idx.at(main_bag)][bag_idx.at(bag)] = quantity;
		    line = sm.suffix();
		}
	}

	// display_map(matrix);

	std::cout << "Part1: Number of bags containing shiny gold bags: " << get_number_of_bags_containing(matrix, "shiny gold") << std::endl;
	std::cout << "Part2: Number of bags within a single shiny gold bag: " << get_number_of_bags_within(matrix, "shiny gold") << std::endl;

	return 0;
}