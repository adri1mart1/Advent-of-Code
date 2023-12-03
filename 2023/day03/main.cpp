#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <unordered_set>

using namespace std;

static const string input{"in.txt"};
static vector<string> lines;

class Number {
public:
    void compute() {
        string s;
        for (const auto& c: coords)
            s += lines[c.first][c.second];
        number = atoi(s.c_str());
    }

    [[nodiscard]] bool is_adjacent_coord(const pair<int, int>& c) const {
        static const vector<int> values{-1, 0, 1};
        for (auto xx: values) {
            for (auto yy: values) {
                pair<int, int> nv = make_pair(c.first + xx, c.second + yy);
                if (find(coords.begin(), coords.end(), nv) != coords.end())
                    return true;
            }
        }
        return false;
    }

    int number;
    vector<pair<int, int>> coords;
};

int main() {
    ifstream ifs{input};
    string line;
    int total_p1 = 0, total_p2 = 0;

    while (getline(ifs, line)) {
        // remove trailing \n
		line.erase(line.length()-1);
        lines.push_back(line);
    }

    vector<pair<int, int>> all_symbols, gear_symbols;
    vector<Number> all_numbers;

    // Very strange algorithm that pops out of my head but we will loop for
    // all characters from left to right, and from top to bottom. If we meet
    // a digit, that's obviously the first digit of the number. So we create
    // a new static Number instance that will be feed until this is not a
    // digit anymore.
    bool on_going_number = false;
    static Number n;

    for (unsigned int x=0; x<lines.size(); ++x) {
        // in case the digit was the last one on the line
        if (on_going_number) {
            on_going_number = false;
            all_numbers.push_back(n);
        }

        for (unsigned int y=0; y<lines[x].length(); ++y) {

            // getting digit
            if (isdigit(lines[x][y])) {
                // Should we start a new digit ?
                if (!on_going_number) {
                    on_going_number = true;
                    n = Number();
                }
                n.coords.push_back(make_pair(x, y));

            } else {
                // Should we finish an ongoing digit feed ?
                if (on_going_number) {
                    on_going_number = false;
                    all_numbers.push_back(n);
                }

                // getting symbols
                if (!isdigit(lines[x][y]) && lines[x][y] != '.') {
                    all_symbols.push_back(make_pair(x, y));

                    if (lines[x][y] == '*')
                        gear_symbols.push_back(make_pair(x, y));
                }
            }
        }
    }

    // Convert string rep number to integers
    for (auto& n: all_numbers)
        n.compute();

    // Scan all part numbers:
    for (const auto& s: all_symbols) {
        for (const auto& n: all_numbers) {
            if (n.is_adjacent_coord(s))
                total_p1 += n.number;
        }
    }

    // Scan all gearbox:
    for (const auto& g: gear_symbols) {
        vector<Number> v;
        for (const auto& n: all_numbers) {
            if (n.is_adjacent_coord(g))
                v.push_back(n);
        }

        if (v.size() == 2)
            total_p2 += v[0].number * v[1].number;
    }

    cout << "Part1: Sum of all part numbers in the engine schematic: " << total_p1 << endl;
    cout << "Part2: The sum of all gear ratios in the engine schematic is " << total_p2 << endl;
    return 0;
}
