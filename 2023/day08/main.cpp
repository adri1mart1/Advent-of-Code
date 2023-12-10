#include <iostream>
#include <string>
#include <fstream>
#include <unordered_map>
#include <vector>
#include <numeric>

/* Quite an interesting day so far ! Very easy for part 1, part2 i run in a infinite loop, like a lot of
 * people who didn't stop the LCM problem here.
 * I got some hints on reddit and saw that all starting points reached their end in a cyclic way so at some
 * point they will all reach the end all together.
 *
 * I ran into an interesting issue, an overflow with std::accumulate().
 * First I used the line:
 * const auto r = accumulate(v.begin(), v.end(), 1, [](ull a, ull b){ return lcm(a, b);
 * and I got a too low answer.
 * The tricky part is you have to replace the third argument with 1ull instead of just 1, if not, your
 * internal accumulator will have an int value and overflow.
 */
using namespace std;

static const string input{"in.txt"};
static string instructions;
static unordered_map<string, unordered_map<char, string>> map;

int main() {
	ifstream ifs{input};
	string line;

	getline(ifs, instructions);
	getline(ifs, line); // empty line

	while (getline(ifs, line)) {
		const auto key = line.substr(0, 3);
		const auto left_value = line.substr(7, 3);
		const auto right_value = line.substr(12, 3);
		const auto l = make_pair('L', left_value);
		const auto r = make_pair('R', right_value);
		map.insert({key, {l, r}});
	}

	unsigned int cnt = 0;
	unsigned int i = 0;

	string now = "AAA";
	while (true) {
		const auto letter = instructions[i];
		cnt++;

		now = map[now][letter];
		if (now == "ZZZ")
			break;

		i++;
		i %= instructions.size()-1;
	}

	cout << "Part1: The number of steps to reach ZZZ is " << cnt << endl;

	// We now have multiple starting points so we need a vector to store all of our current positions
	vector<string> nows;

	// find all starting points
	for (const auto& it: map) {
		if (it.first[2] == 'A')
			nows.push_back(it.first);
	}

	// a vector to hold loop count values for each starting point.
	vector<unsigned long long int> loop_counts;
	loop_counts.resize(nows.size(), 0);

	// run the algo
	i = 0;
	cnt = 0;
	bool finished = false;
	while (!finished) {
		const auto letter = instructions[i];
		cnt++;

		for (unsigned int i=0; i<nows.size(); ++i) {
			nows[i] = map[nows[i]][letter];

			if (nows[i][2] == 'Z') {
				if (loop_counts[i] == 0) {
					loop_counts[i] = cnt;

					// we don't need to go further if all starting points have at least reach their end once.
					if (all_of(loop_counts.begin(), loop_counts.end(), [](unsigned int i){ return i!=0; })) {
						finished = true;
						break;
					}
				}
			}
		}

		i++;
		i %= instructions.size()-1;
	}

	const auto res = accumulate(loop_counts.begin(), loop_counts.end(), 1LL,
		[](const unsigned long long int a, const unsigned long long int b){ return lcm(a, b);
	});

	cout << "Part2: The number of steps to reach xxZ is " << res << endl;
	return 0;
}
