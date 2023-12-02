#include <iostream>
#include <string>
#include <fstream>
#include <regex>
#include <map>
#include <unordered_map>
#include <vector>

using namespace std;

static const string input{"in.txt"};

static const map<string, unsigned int> min_qty_required {
	{ "red", 12 },
	{ "green", 13 },
	{ "blue", 14 }
};

class Game {
public:
	Game(unsigned int id) : id_m(id) {}

	void add_groups(const string& s) {
		const regex group_reg{R"(([\d\w ,]*)[;]?)"};
		smatch group_matches;
		string remaining{s};

		while (regex_search(remaining, group_matches, group_reg)) {
			string group = group_matches[1].str();
			remaining = group_matches.suffix();

			const regex cube_reg{R"((\d+) (\w+))"};
			smatch cube_matches;
			unordered_map<string, unsigned int> cube_subset_map;

			while (regex_search(group, cube_matches, cube_reg)) {
				unsigned int qty = atoi(cube_matches[1].str().c_str());
				const string color = cube_matches[2].str();
				cube_subset_map.insert({color, qty});
				group = cube_matches.suffix();
			}

			games_m.push_back(cube_subset_map);

			if (remaining.size() == 0)
				break;
		}
	}

	[[nodiscard]] bool is_p1_game_possible() {
		for (const auto& game: games_m) {
			for (const auto& color: game) {
				if (color.second > min_qty_required.at(color.first))
					return false;
			}
		}
		return true;
	}

	[[nodiscard]] unsigned int get_power_num() {
		unsigned int min_blue = 0, min_red = 0, min_green = 0;

		for (const auto& game: games_m) {
			for (const auto& color: game) {
				if (color.first == "red")
					min_red = max(color.second, min_red);
				else if (color.first == "green")
					min_green = max(color.second, min_green);
				else if (color.first == "blue")
					min_blue = max(color.second, min_blue);
			}
		}
		return min_blue * min_red * min_green;
	}

	vector<unordered_map<string, unsigned int>> games_m;
	unsigned int id_m;
};

int main() {
	unsigned int total_p1 = 0, total_p2 = 0;
	ifstream ifs{input};
	string line;

	while (getline(ifs, line)) {

		// remove trailing \n
		line.erase(line.length()-1);

		const regex game_reg{R"(Game (\d+):(.*))"};
		smatch game_matches;

		if (regex_search(line, game_matches, game_reg)) {
			const unsigned int game_num = atoi(game_matches[1].str().c_str());
			const string remaining = game_matches[2].str();

			Game game(game_num);
			game.add_groups(remaining);

			if (game.is_p1_game_possible())
				total_p1 += game.id_m;

			total_p2 += game.get_power_num();
		}
	}

	cout << "Part1: Sum of the possible game IDs:" << total_p1 << endl;
	cout << "Part2: Sum of the power of these sets:" << total_p2 << endl;
	return 0;
}
