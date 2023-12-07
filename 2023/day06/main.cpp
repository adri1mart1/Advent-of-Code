#include <iostream>
#include <string>
#include <fstream>
#include <sstream>
#include <vector>
#include <algorithm>

using namespace std;

static const string input{"in.txt"};

int main() {
	ifstream ifs{input};
	string line0, line1;
	unsigned int total_p1 = 1, total_p2 = 0;

	getline(ifs, line0);
	getline(ifs, line1);

	line0 = line0.substr(line0.find(':')+1);
	line1 = line1.substr(line1.find(':')+1);
	stringstream iss1(line0);
	stringstream iss2(line1);

	vector<unsigned int> times;
	unsigned int time;
	while (iss1 >> time)
		times.push_back(time);

	vector<unsigned int> distances_to_beat;
	int distance_to_beat;
	while (iss2 >> distance_to_beat)
		distances_to_beat.push_back(distance_to_beat);

	auto get_number_of_ways = [](const unsigned long long time, const unsigned long long dist) {
		unsigned int res = 0;
		for (unsigned long long int speed=0; speed<time; ++speed) {
			const unsigned long long int remaining_time = time - speed;
			const unsigned long long int d = remaining_time * speed;
			if (d > dist)
				res++;
		}
		return res;
	};

	for (unsigned int i=0; i<times.size(); ++i)
		total_p1 *= get_number_of_ways(times[i], distances_to_beat[i]);

	// preparing part2
	line0.erase(remove(line0.begin(), line0.end(), ' '), line0.end());
	line1.erase(remove(line1.begin(), line1.end(), ' '), line1.end());

	const auto time_p2 = atoll(line0.c_str());
	const auto distance_to_beat_p2 = atoll(line1.c_str());

	total_p2 = get_number_of_ways(time_p2, distance_to_beat_p2);

	cout << "Part1: the record can be beaten " << total_p1 << " times" << endl;
	cout << "Part2: the record can be beaten " << total_p2 << " times" << endl;
	return 0;
}
