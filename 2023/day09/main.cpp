#include <iostream>
#include <string>
#include <vector>
#include <fstream>
#include <sstream>
#include <deque>

using namespace std;

static const string input{"in2.txt"};
static vector<deque<int>> vect;
static unsigned int idx = 0;

void analyze() {
    deque<int> diffs;
    for (unsigned int i=0; i<vect[idx].size()-1; ++i)
        diffs.push_back(vect[idx][i+1] - vect[idx][i]);
    vect.push_back(diffs);
    idx++;

    if (!all_of(vect[idx].begin(), vect[idx].end(), [](int i) { return i==0; }))
        analyze();
}

[[nodiscard]] static int guess_next() {
    vect[idx].push_back(0);
    for (int i = idx-1; i >= 0; --i)
        vect[i].push_back(vect[i].back() + vect[i+1].back());
    return vect[0].back();
}

[[nodiscard]] static int guess_previous() {
    vect[idx].push_front(0);
    for (int i = idx-1; i >= 0; --i)
        vect[i].push_front(vect[i].front() - vect[i+1].front());
    return vect[0].front();
}

int main() {
    ifstream ifs{input};
    string line;
    int total_p1 = 0, total_p2 = 0;

    while (getline(ifs, line)) {
        stringstream iss(line);
        int v;
        deque<int> vv;

        vect.clear();
        while (iss >> v)
            vv.push_back(v);
        vect.push_back(vv);

        idx = 0;
        analyze();
        total_p1 += guess_next();
        total_p2 += guess_previous();
    }

    cout << "Part1: the sum of these extrapolated value is " << total_p1 << endl;
    cout << "Part2: the sum of these extrapolated value is " << total_p2 << endl;
    return 0;
}
