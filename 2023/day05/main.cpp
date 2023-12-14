#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <optional>
#include <array>
#include <limits>

using namespace std;

static const string input{"in.txt"};
static vector<long long int> seed_to_plant_g;
static vector<pair<long long int, long long int>> seed_ranges_to_test_g;

#define MIN_V  0
#define MAX_V  1
#define OFFSET 2

class Mapper {
public:
	void feed(const string& s) {
		stringstream iss(s);
		long long int dest, src, range;
		long long int min_v, max_v, offset;
		iss >> dest >> src >> range;
		min_v = src;
		max_v = src + range - 1;
		offset = dest - src;
		vect.push_back({min_v, max_v, offset});
	}

	[[nodiscard]] long long int convert(long long val) const {
		for (const auto v: vect) {
			if (val >= v[MIN_V] && val <= v[MAX_V]) {
				val += v[OFFSET];
				break;
			}
		}
		return val;
	}

	void optimize() {
		sort(vect.begin(), vect.end(), [](array<long long, 3> &a1, array<long long, 3> &a2) {
			return a1[MIN_V] < a2[MIN_V];
		});
	}

	[[nodiscard]] vector<pair<long long int, long long int>>
	analyze_range(const vector<pair<long long, long long>>& pairs) {
		vector<pair<long long, long long>> nv;

		for (const auto& p: pairs) {
			auto very_first = p.first;
			const auto very_last = p.second;
			auto begin = very_first;
			auto next_end = very_first;

			// check lower band
			if (very_last < vect[0][MIN_V]) {
				nv.push_back(make_pair(very_first, very_last));
				continue;
			}

			for (unsigned int i=0; i<vect.size(); ++i) {
				if (begin > vect[i][MAX_V])
					continue;

				next_end = min(very_last, vect[i][MAX_V]);
				nv.push_back(make_pair(begin, next_end));

				if (next_end < very_last)
					begin = next_end + 1;
				else
					break;
			}

			// check upper band
			if (very_first > vect[vect.size()-1][MAX_V])
				nv.push_back(make_pair(very_first, very_last));
		}

		vector<pair<long long, long long>> fv;
		for (auto p: nv) {
			auto first = convert(p.first);
			auto second = convert(p.second);

			pair<long long, long long> new_pair;
			if (first < second)
				new_pair = make_pair(first, second);
			else
				new_pair = make_pair(second, first);

			fv.push_back(new_pair);
		}

		sort(fv.begin(), fv.end(), [](pair<long long, long long> &p1, pair<long long, long long> &p2) {
			return p1.first < p2.first;
		});

		return fv;
	}

	vector<array<long long, 3>> vect;
};

static vector<Mapper> all_maps_g;

int main() {
	ifstream ifs{input};
	string line;
	long long int total_p1 = numeric_limits<long long int>::max();
	long long int total_p2 = numeric_limits<long long int>::max();

	getline(ifs, line);

	const auto ss = line.substr(line.find(':')+1);
	stringstream iss(ss);
	unsigned int n;
	while (iss >> n)
		seed_to_plant_g.push_back(n);

	static optional<Mapper> mapper;

	while (getline(ifs, line)) {
		// remove trailing \n
		line.erase(line.length()-1);

		if (line.size() == 0)
			continue;

		if (line.find("map") != line.npos) {
			// add to vector and create new one
			if (mapper.has_value())
				all_maps_g.push_back(mapper.value());

			mapper = Mapper();
		} else {
			mapper.value().feed(line);
		}
	}
	// adding last mapper
	all_maps_g.push_back(mapper.value());

	for (auto& m: all_maps_g)
		m.optimize();

	for (auto seed: seed_to_plant_g) {
		auto value = seed;

		for (auto mapp: all_maps_g)
			value = mapp.convert(value);

		total_p1 = min(total_p1, value);
	}

	// compute seed ranges for part 2
	unsigned int i=0;
	while (i < seed_to_plant_g.size()) {
		seed_ranges_to_test_g.push_back(make_pair(seed_to_plant_g[i], seed_to_plant_g[i]+seed_to_plant_g[i+1]-1));
		i+=2;
	}

	vector<pair<long long int, long long int>> all_ranges;

	for (const auto& seed: seed_ranges_to_test_g) {
		vector<pair<long long, long long>> nv;
		nv.push_back(seed);

		for (auto mapp: all_maps_g)
			nv = mapp.analyze_range(nv);

		for (const auto& r: nv)
			all_ranges.push_back(r);

		total_p2 = min(total_p2, nv[0].first);
	}

	sort(all_ranges.begin(), all_ranges.end(), [](const pair<long long int, long long int> &p1,
	                                              const pair<long long int, long long int> &p2) {
		return p1.first < p2.first;
	});

	cout << "Part1: lowest location number that matches the initial seed numbers is " << total_p1 << endl;
	cout << "Part2: lowest location number that matches the initial seed numbers is " << total_p2 << endl;
	return 0;
}
