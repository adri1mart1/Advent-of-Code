#include <iostream>
#include <fstream>
#include <string>
#include <regex>
#include <unordered_map>
#include <iomanip>
#include <unordered_set>
#include <queue>
#include <bitset>
#include <cassert>

/* Interesting challenge overall but quite difficult for a single day challenge. Probably one of
 * the hardest ever for me. The D-day, I did not even produce any code as I knew I would not
 * provide a performant enough solution to solve it.
 *
 * After months, I decided to come back to this problem and first, get some hints about good
 * algorithm to use, etc.. In the end, there was a lot of different possibilities so I decided
 * to go by myself.
 *
 * I initially wrote a version using a BFS considering all moves (go to here, opened valves,
 * wait, etc..). Even with a lot of pruning, that was not reasonable for part 2.
 *
 * I have seen the hyper-neutrino video on Youtube and his approach was way more interesting,
 * instead of considering all possible moves, just consider all interesting macros moves such
 * as "go open valve AA, go open valve BB, etc" .. with this approach, you have way less states,
 * a queue way smaller and thing are going better.
 *
 * I did not use cache for this problem, but that's almost mandatory I guess. Once I got the
 * example working for part 2, I launch my program for main example, It was working for a while
 * went for dinner and when I came back, I got the answer.
 *
 * Definitely not an optimized approach but this problem cost me a lot of time, I did not
 * took additional time to optimize this.
 */

using namespace std;

class State;

static unordered_map<string, unsigned int> valves_idx{};
static unordered_map<unsigned int, string> valves_names{};


#if 0
// hardcoded official input
static const string input_file{"in.txt"};
static constexpr unsigned int VALVES_NUM = 58;
static constexpr unsigned int VALVES_NUM_TO_BE_OPENED = 15;
#else
// hardcoded training input
static const string input_file{"in2.txt"};
static constexpr unsigned int VALVES_NUM = 10;
static constexpr unsigned int VALVES_NUM_TO_BE_OPENED = 6;
#endif

static constexpr unsigned int TOTAL_MINUTES_PART1 = 30;
static constexpr unsigned int TOTAL_MINUTES_PART2 = 26;

struct Stats {
	unsigned int best_overall_pressure = 0;
	unsigned int best_now_pressure = 0;
};

static array<Stats, TOTAL_MINUTES_PART1> stats;

struct Valve {
	char name[3];
	unsigned int flow_rate = 0;
	unordered_map<unsigned int, unsigned int> direct_neighbours;
	unordered_map<unsigned int, unsigned int> other_neighbours;
};

static array<Valve, VALVES_NUM> valves;

struct State {
	unsigned int minutes = 0;
	unsigned int now_pressure = 0;
	unsigned int overall_pressure = 0;
	unsigned int position = 0;
	// A bitset to save all remaining valves to be opened. We only consider valve that
	// have a positive pressure to be opened.
	// index is the valve index.
	// ex: if AA is at index 0
	// valve_to_be_opened[0] = 0 -> flow_rate is 0 or already opened
	// valve_to_be_opened[0] = 1 -> flow_rate is strictly superior to 0
	bitset<VALVES_NUM> valve_to_be_opened{};
};

static queue<State> states_queue = {};


void dump_state(const State &s) {
	cout << "S: m:" << s.minutes
		 << " np:" << s.now_pressure
		 << " op:" << s.overall_pressure
	     << " n:" << valves_names[s.position]
	     << " vo:" << s.valve_to_be_opened << '\n';
}

void dump_valves() {
	for (unsigned int i=0; i<VALVES_NUM; ++i) {
		cout << "valve " << valves_names[i] << "(" << i << ") fr:" << valves[i].flow_rate
			 << "\n dnb: ";
		for (const auto n: valves[i].direct_neighbours)
			cout << " [" << valves_names[n.first] << "](" << n.second << ")";
		cout << endl;
	}
}

void adding_valve_to_hashmap(const string& v) {
	static unsigned current_valve_idx = 0;
	if (valves_idx.find(v) == valves_idx.end()) {
		valves_idx.insert(make_pair(v, current_valve_idx));
		valves_names.insert(make_pair(current_valve_idx, v));
		current_valve_idx++;
	}
}

void add_relation(const string& v1, const string& v2) {
	// cout << "add relation between " << v1 << " and " << v2 << endl;
	valves[valves_idx[v1]].direct_neighbours.insert(make_pair(valves_idx[v2], 1));
	valves[valves_idx[v2]].direct_neighbours.insert(make_pair(valves_idx[v1], 1));
}

void read_input_file() {
	std::stringstream buffer;
	ifstream ifs(input_file);
	string line;
	regex regex_majuscules("[A-Z]{2}");

	// First read the file once to get all valves and allocate memory
	if (ifs.is_open()) {
		while (getline(ifs, line)) {
			const auto valve_name = line.substr(6, 2);
			adding_valve_to_hashmap(valve_name);
			const auto end_of_str = line.substr(15);

			sregex_iterator it(end_of_str.begin(), end_of_str.end(), regex_majuscules);
		    sregex_iterator it_end;

		    while (it != it_end) {
		        adding_valve_to_hashmap(it->str());
		        ++it;
		    }
		}
	}

	// reset ifstream to be able to read again input file
	ifs.clear();
	ifs.seekg(0, ifs.beg);

	// Add all relations between valves
	if (ifs.is_open()) {
		while (getline(ifs, line)) {
			const auto valve_name = line.substr(6, 2);
			const auto flow_rate = stoi(line.substr(23));
			valves[valves_idx[valve_name]].flow_rate = flow_rate;

			const auto end_of_str = line.substr(15);
			regex regex_majuscules("[A-Z]{2}");

			sregex_iterator it(end_of_str.begin(), end_of_str.end(), regex_majuscules);
		    sregex_iterator it_end;

		    while (it != it_end) {
		        add_relation(valve_name, it->str());
		        ++it;
		    }
		}
	}
}

void init_valves_to_be_opened(State& s) {
	for (unsigned int i=0; i<VALVES_NUM; ++i) {
		if (valves[i].flow_rate > 0) {
			s.valve_to_be_opened[i] = 1;
		}
	}
}

unsigned int get_distance(const unsigned int from, const unsigned int to) {
	// this function returns the shortest distance from one node to
	// another using BFS algorithm.

	unsigned int dist = 0;

	queue<vector<unsigned int>> q; // queue of paths
	unordered_set<unsigned int> visited;

	vector<unsigned int> v;
	v.push_back(from);
	visited.insert(from);
	q.push(v);

	do {
		auto now_path = q.front();
		q.pop();
		auto now = now_path.back();

		if (now == to) {
			dist = now_path.size()-1;
			break;
		}

		for (auto dn: valves[now].direct_neighbours) {
			if (visited.find(dn.first) == visited.end()) {
				visited.insert(dn.first);

				vector<unsigned int> new_vect = now_path;
				new_vect.push_back(dn.first);
				q.push(new_vect);
			}
		}
	} while (!q.empty());

	assert(dist >= 0);
	return dist;
}

void compute_all_distances() {
	// This function compute all distances between all nodes in the graph.
	for (unsigned int i=0; i<VALVES_NUM; ++i) {
		for (unsigned int j=0; j<VALVES_NUM; ++j) {
			if (i == j)
				continue;
			if (i != valves_idx["AA"] && valves[i].flow_rate == 0)
				continue;
			if (j != valves_idx["AA"] && valves[j].flow_rate == 0)
				continue;
			if (valves[i].direct_neighbours.find(j) == valves[i].direct_neighbours.end()) {
				valves[i].other_neighbours.insert(make_pair(j, get_distance(i, j)));
			}
		}
	}
}

void prune_empty_valves() {
	// We remove all valves that have a flow rate of 0
	vector<unsigned int> to_remove;

	for (unsigned int i=0; i<VALVES_NUM; ++i) {
		if (i != valves_idx["AA"] && valves[i].flow_rate == 0) {
			to_remove.push_back(i);
		}
	}

	for (unsigned int i=0; i<VALVES_NUM; ++i) {
		if (find(to_remove.begin(), to_remove.end(), i) != to_remove.end()) {
			valves[i].direct_neighbours.clear();
			valves[i].other_neighbours.clear();

		} else {
			for (const auto j: to_remove) {
				valves[i].direct_neighbours.erase(j);
				valves[i].other_neighbours.erase(j);
			}

			valves[i].direct_neighbours.merge(valves[i].other_neighbours);
		}
	}
}

unsigned int get_pressure_algo(const unsigned int max_min) {
	unsigned int max_val = 0;

	do {
		auto& s = states_queue.front();

		// cout << endl;
/*		if (s.minutes == 3 && s.now_pressure == 20 && s.position == valves_idx["DD"]) {
			dump_state(s);
		}
		if (s.minutes == 18 && s.now_pressure == 76 &&
			s.position == valves_idx["HH"] && s.overall_pressure == 700) {
			dump_state(s);
		}
		if (s.minutes == 22 && s.now_pressure == 79 &&
			s.position == valves_idx["EE"] && s.overall_pressure == 1007) {
			dump_state(s);
		}
		if (s.minutes == 25 && s.now_pressure == 81 && s.overall_pressure == 1246) {
			dump_state(s);
		}
		if (s.minutes == 30 && s.now_pressure == 81 && s.overall_pressure == 1651) {
			dump_state(s);
		}*/

		if (s.minutes == max_min) {
			if (s.overall_pressure > max_val) {
				max_val = s.overall_pressure;
				//cout << "new max_val\n";
				//dump_state(s);
			}
		}

		if (s.minutes < max_min) {

			// check all neighbors
			for (auto n: valves[s.position].direct_neighbours) {
				//cout << " " << n.first << endl;

				if (s.valve_to_be_opened[n.first] == 0)
					continue;

				if ((s.minutes + n.second + 1) > max_min)
					continue;

				State new_state = s;
				new_state.position = n.first;
				new_state.minutes += n.second + 1;
				new_state.overall_pressure += new_state.now_pressure * n.second;
				new_state.now_pressure += valves[n.first].flow_rate;
				new_state.overall_pressure += new_state.now_pressure;
				new_state.valve_to_be_opened[n.first] = 0;
				// cout << "  adding ";
				// dump_state(new_state);
				states_queue.push(new_state);
			}

			// add idle state
			State new_idle_state = s;
			new_idle_state.minutes += 1;
			new_idle_state.overall_pressure += new_idle_state.now_pressure;
			// cout << "  adding ";
			// dump_state(new_state);
			states_queue.push(new_idle_state);
		}

		// we need to pop the element at the end because we are dealing with a reference all above
		states_queue.pop();

	} while (!states_queue.empty());

	return max_val;
}

void part2() {
	read_input_file();
	compute_all_distances();
	prune_empty_valves();
	// dump_valves();

	State init;
	init.minutes = 1;
	init.now_pressure = 0;
	init.overall_pressure = 0;
	init.position = valves_idx["AA"];
	init_valves_to_be_opened(init);

	// At this point, this is where the fun begins.
	// To test all possibilities, we are going to consider all valves to
	// be opened in a bitset. (exactly like part 1).
	// With the example, the bitset of valves to be opened is: 1100111010
	// Each index is the valve index.
	// Then we will split is in two parts, one bitset for me, one bitset for
	// the elephant. The bitset will mark all valves to be opened by each one.
	// Ex: considering the initial bitset 1100111010
	//                      Me:           0000011010
	//                      The elephant: 1100100000
	// Then, we try to get the most pressure we can get for these bitsets for
	// each one of the characters, we add these 2 values and keep the max
	// overall value.
	// A small optimisation done is to only keep bitsets that are well balanced.
	// Again, if we have the initial bitset 1100111010 and the following division:
	//                      Me:             1000000000
	//                      The elephant:   0100111010
	// It does not really makes sense as the most pressure solution is probably
	// a solution where each one of the characters is a close number to num of valves
	// divided by 2.

	const auto init_bitset_value = init.valve_to_be_opened;
	vector<unsigned int> init_bitset_indices;

	for (unsigned int i=0; i<VALVES_NUM; i++) {
		if (init_bitset_value[i] == 1)
			init_bitset_indices.push_back(i);
	}

	auto total_bit_set = init.valve_to_be_opened.count();
	unsigned int min_v = 0;
	unsigned int max_v = 0;

	if (total_bit_set%2 != 0) {
		min_v = total_bit_set/2;
		max_v = total_bit_set/2+1;
	} else {
		min_v = max_v = total_bit_set/2;
	}

	bitset<VALVES_NUM_TO_BE_OPENED> bs;
	bs.set();
	const auto max_valve_value = init.valve_to_be_opened.to_ulong();

	// vector of me and elephant valves to be opened bitsets.
	vector<pair<bitset<VALVES_NUM_TO_BE_OPENED>, bitset<VALVES_NUM_TO_BE_OPENED>>> possibilities;

	for (unsigned int i=0; i<(bs.to_ulong()/2); i++) {
		auto j = bs.to_ulong() - i;
		bitset<VALVES_NUM_TO_BE_OPENED> bi = i;
		bitset<VALVES_NUM_TO_BE_OPENED> bj = j;
		if ((bi.count() >= min_v && bi.count() <= max_v) &&
			(bj.count() >= min_v && bj.count() <= max_v)) {

			possibilities.push_back(make_pair(bi, bj));
		}
	}

	// Making all possibilties
	vector<pair<bitset<VALVES_NUM>, bitset<VALVES_NUM>>> bitset_possibilities;

	for (auto p: possibilities) {
		bitset<VALVES_NUM> b1, b2;

		for (unsigned int i=0; i<VALVES_NUM_TO_BE_OPENED; ++i) {
			if (p.first[i] == 1)
				b1.set(init_bitset_indices[i]);

			if (p.second[i] == 1)
				b2.set(init_bitset_indices[i]);

			bitset_possibilities.push_back(make_pair(b1, b2));
		}
	}

	// Run algorithm with all values
	unsigned int max_overall = 0;

	for (auto p: bitset_possibilities) {
		assert(states_queue.size() == 0);
		init.valve_to_be_opened = p.first;
		states_queue.push(init);
		const auto first = get_pressure_algo(TOTAL_MINUTES_PART2);

		assert(states_queue.size() == 0);
		init.valve_to_be_opened = p.second;
		states_queue.push(init);
		const auto second = get_pressure_algo(TOTAL_MINUTES_PART2);

		max_overall = max(max_overall, first + second);
	}

	cout << "Part2: Me and an elephant, max pressure we can release: " << max_overall << endl;
}

void part1() {
	read_input_file();
	compute_all_distances();
	prune_empty_valves();
	// dump_valves();

	State init;
	init.minutes = 1;
	init.now_pressure = 0;
	init.overall_pressure = 0;
	init.position = valves_idx["AA"];
	init_valves_to_be_opened(init);

	states_queue.push(init);

	cout << "Part1: max pressure I can release alone: " << get_pressure_algo(TOTAL_MINUTES_PART1) << endl;
}

int main() {
	part1();
	part2();
	return 0;
}
