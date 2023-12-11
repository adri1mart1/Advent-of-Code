#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <algorithm>

using namespace std;

static const string input{"in.txt"};
static vector<vector<char>> map;
// Holds the coordinates (pairs) of all galaxies
static vector<pair<unsigned int, unsigned int>> galaxies;
// Holds all x or y space expansions
static vector<unsigned int> x_expansions, y_expansions;

void get_galaxy_coords() {
	for (unsigned int y=0; y<map.size(); ++y) {
		for (unsigned int x=0; x<map[0].size(); ++x) {
			if (map[y][x] == '#')
				galaxies.push_back(make_pair(x, y));
		}
	}
}

[[nodiscard]] unsigned long long int compute(const unsigned long long factor) {
	unsigned long long int total = 0ull;
	const auto fact = max(1ull, factor - 1);

	for (unsigned int i=0; i<galaxies.size(); ++i) {
		for (unsigned int j=0; j<galaxies.size(); ++j) {
			if (i >= j)
				continue;

			const auto min_x = min(galaxies[i].first, galaxies[j].first);
			const auto max_x = max(galaxies[i].first, galaxies[j].first);
			const auto min_y = min(galaxies[i].second, galaxies[j].second);
			const auto max_y = max(galaxies[i].second, galaxies[j].second);

			const auto x_cnt = ranges::count_if(x_expansions, [&](const unsigned int x){
				return x >= min_x && x <= max_x;
			});
			const auto y_cnt = ranges::count_if(y_expansions, [&](const unsigned int y){
				return y >= min_y && y <= max_y;
			});

			const auto dist = max_x - min_x + x_cnt * fact + max_y - min_y + y_cnt * fact;
			total += dist;
		}
	}
	return total;
}

void get_space_expansions() {
	for (unsigned int y=0; y<map.size(); ++y) {
		bool found_galaxy = false;
		for (unsigned int x=0; x<map[0].size(); ++x) {
			if (map[y][x] == '#') {
				found_galaxy = true;
				break;
			}
		}
		if (!found_galaxy)
			y_expansions.push_back(y);
	}

	for (unsigned int x=0; x<map[0].size(); ++x) {
		bool found_galaxy = false;
		for (unsigned int y=0; y<map.size(); ++y) {
			if (map[y][x] == '#') {
				found_galaxy = true;
				break;
			}
		}
		if (!found_galaxy)
			x_expansions.push_back(x);
	}
}

int main() {
	ifstream ifs{input};
	string line;

	while (getline(ifs, line)) {
		line.erase(line.length()-1); // remove \n
		vector<char> v;
		for (const auto c: line)
			v.push_back(c);
		map.push_back(v);
	}

	get_galaxy_coords();
	get_space_expansions();

	cout << "Part1: the sum of these length is " << compute(1) << endl;
	cout << "Part2: the sum of these length is " << compute(1e6) << endl;
	return 0;
}
