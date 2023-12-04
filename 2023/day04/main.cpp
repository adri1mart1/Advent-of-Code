#include <iostream>
#include <string>
#include <fstream>
#include <regex>
#include <sstream>
#include <optional>

using namespace std;

static const string input{"in.txt"};
// We store in matching_number the number of winning numbers per card idx.
// Ex: if we have [0, 4, 2] --> Card 1 has 4 winning number, Card 2 has 2, etc..
static vector<unsigned int> matching_numbers_g;
// Quite happy with the solution for part2, I just store an array of numbers like so [index]=value
// Starting with array [0, 1, 1, 1, 1, 1, 1, ...]
// Then, we loop for each indexes starting at index 1 (because Card 0 doesn't exists).
// Index 1, so card 1 has a score of 4 so we increment all following indices [2,3,4,5] by 1.
// We will then have: [0, 1, 2, 2, 2, 2, 1, ...].
// We decrement index 1 because we have treated it:
// We will then have: [0, 0, 2, 2, 2, 2, 1, ...].
// If current value is 0, go to next index
// We now manage with index 2, so card 2, with a score of 2 so we increment all 2 following indices [3, 4] by 1
// We will then have: [0, 0, 2, 3, 3, 2, 1, ...].
// And we decrement index 2 by 1 because we have treated it:
// We will then have: [0, 0, 1, 3, 3, 2, 1, ...].
// etc.. etc..
// Quite fast and simple solution in the end.
static vector<unsigned int> tab_g;

class Card {
public:
	Card(const string& s) {
		process_card_num(s);
		process_winning_numbers(s);
		process_my_numbers(s);
	}

	void process_card_num(const string& s) {
		const regex reg{R"(Card (\d+):.*)"};
		smatch matches;
		if (regex_search(s, matches, reg))
			number_m = atoi(matches[1].str().c_str());
	}

	void process_winning_numbers(const string& s) {
		const auto first = s.find(':');
		const auto last = s.find('|');
		const auto ss = s.substr(first+1, last-first);
		stringstream iss(ss);
		unsigned int n;
		while (iss >> n)
			win_numbers_m.push_back(n);
	}

	void process_my_numbers(const string& s) {
		const auto first = s.find('|');
		const auto ss = s.substr(first+1);
		stringstream iss(ss);
		unsigned int n;
		while (iss >> n)
			my_numbers_m.push_back(n);
	}

	[[nodiscard]] unsigned int get_score() {
		if (score_m.has_value())
			return score_m.value();

		my_numbers_size_m = 0;
		for (const auto nm: my_numbers_m) {
			if (find(win_numbers_m.begin(), win_numbers_m.end(), nm) != win_numbers_m.end())
				my_numbers_size_m++;
		}

		score_m = my_numbers_size_m > 0 ? 1 << (my_numbers_size_m-1): 0;
		return score_m.value();
	}

	optional<unsigned int> score_m;
	unsigned int number_m;
	vector<unsigned int> my_numbers_m;
	unsigned int my_numbers_size_m;
	vector<unsigned int> win_numbers_m;
};

int main() {
	ifstream ifs{input};
	string line;
	unsigned int total_p1 = 0;
	unsigned int total_p2 = 1; // p2 score start at 1 because we will always consider the card 1 once.

	// Card 0 does not exists, pushing dump value. It's just to have Card 1 matching with tab_g[1] value
	matching_numbers_g.push_back(0);
	tab_g.push_back(0);

	while (getline(ifs, line)) {
		Card c(line);
		total_p1 += c.get_score();
		matching_numbers_g.push_back(c.my_numbers_size_m);
		tab_g.push_back(1); // init all value to 1 for part 2 (meaning we have to treat it 1 time)
	}

	unsigned int i=1;

	while (true) {
		if (i >= tab_g.size())
			break;

		for (unsigned int a=0; a<matching_numbers_g[i]; ++a)
			tab_g[i+a+1]++;

		tab_g[i]--;
		if (tab_g[i] <= 0) {
			if (i < tab_g.size()-1)
				total_p2 += tab_g[i+1];
			i++;
		}
	}

	cout << "Part1: how many points are they worth in total: " << total_p1 << endl;
	cout << "Part2: how many total scratchcards ends up with: " << total_p2 << endl;
	return 0;
}
