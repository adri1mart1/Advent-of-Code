#include <iostream>
#include <string>
#include <fstream>
#include <vector>
#include <map>

/* Not very happy with this solution overall, lots of code, not very efficient to find
 * all possibilities for part2. The get_possibilities() function is the key of the efficiency
 * problem. I'll see in the future if i come back to this problem to improve this.
 * Executing time is about 1min30 on an i7.
 */
using namespace std;

static const string input{"in.txt"};
static const vector<char> cards_p1 = {'2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A'};
static const vector<char> cards_p2 = {'J', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'Q', 'K', 'A'};
static map<char, int> letter_scores_p1, letter_scores_p2;
static vector<string> all_w_possibilities;

class Hand {
public:
    Hand(const string &s) : score_p1_m(0), score_p2_m(0) {
        hand_m = s.substr(0, 5);
        bid_m = atoi(s.substr(6).c_str());
        score_p1_m = get_score(hand_m);
        evaluate_p2();
    }

    [[nodiscard]] int get_index_of_letter(const string& s, const char letter) {
        const auto a = find(s.begin(), s.end(), letter);
        if (a != s.end())
            return a - s.begin();
        return -1;
    }

    void get_possibilities(const string& s) {
        all_w_possibilities.clear();
        all_w_possibilities.push_back(s);

        while (true) {
            bool found_w_with_joker = false;

            for (unsigned int i=0; i<all_w_possibilities.size(); ++i) {
                const auto idx_joker = get_index_of_letter(all_w_possibilities[i], 'J');
                if (idx_joker != -1) {

                    for (unsigned int j=1; j<cards_p2.size(); ++j) {
                        string ns = all_w_possibilities[i];
                        ns[idx_joker] = cards_p2[j];
                        all_w_possibilities.push_back(ns);
                    }

                    found_w_with_joker = true;
                    all_w_possibilities.erase(all_w_possibilities.begin() + i);
                    break;
                }
            }

            if (!found_w_with_joker)
                break;
        }
    }

    void evaluate_p2() {
        get_possibilities(hand_m);

        for (const auto& p: all_w_possibilities) {
            const auto ns = get_score(p);
            score_p2_m = max(ns, score_p2_m);
        }
    }

    [[nodiscard]] bool check_if_n_of_a_kind(map<char, int> mp, const int n) {
        for (const auto m: mp) {
            if (m.second == n)
                return true;
        }
        return false;
    }

    [[nodiscard]] bool check_if_full_house(const map<char, int>& mp) {
        if (mp.size() == 2 && (mp.begin()->second == 3 || mp.begin()->second == 2))
            return true;
        return false;
    }

    [[nodiscard]] bool check_if_three_of_a_kind(const map<char, int>& mp) {
        for (const auto m: mp) {
            if (m.second == 3)
                return true;
        }
        return false;
    }

    [[nodiscard]] bool check_if_n_pairs(const map<char, int>& mp, const int num) {
        int pair_found = 0;
        for (const auto m: mp) {
            if (m.second == 2)
                pair_found++;
        }
        if (pair_found == num)
            return true;
        return false;
    }

    [[nodiscard]] unsigned int get_score(const string &s) {
        map<char, int> letter_count;
        for(unsigned int i=0; i<s.size(); i++)
            letter_count[s[i]]++;

        if (check_if_n_of_a_kind(letter_count, 5)) {
            return 6000;
        } else if (check_if_n_of_a_kind(letter_count, 4)) {
            return 5000;
        } else if (check_if_full_house(letter_count)) {
            return 4000;
        } else if (check_if_three_of_a_kind(letter_count)) {
            return 3000;
        } else if (check_if_n_pairs(letter_count, 2)) {
            return 2000;
        } else if (check_if_n_pairs(letter_count, 1)) {
            return 1000;
        } else {}

        return 0;
    }

    string hand_m;
    unsigned int rank_m;
    unsigned int score_p1_m, score_p2_m;
    unsigned int bid_m;
};


[[nodiscard]] static bool sort_hand_func_p1(const Hand& a, const Hand& b) {
    if (a.score_p1_m == b.score_p1_m) {
        for (unsigned int i=0; i<a.hand_m.size(); ++i) {
            if (a.hand_m[i] == b.hand_m[i])
                continue;
            return letter_scores_p1[a.hand_m[i]] < letter_scores_p1[b.hand_m[i]];
        }
    }
    return a.score_p1_m < b.score_p1_m;
}

[[nodiscard]] static bool sort_hand_func_p2(const Hand& a, const Hand& b) {
    if (a.score_p2_m == b.score_p2_m) {
        for (unsigned int i=0; i<a.hand_m.size(); ++i) {
            if (a.hand_m[i] == b.hand_m[i])
                continue;
            return letter_scores_p2[a.hand_m[i]] < letter_scores_p2[b.hand_m[i]];
        }
    }
    return a.score_p2_m < b.score_p2_m;
}

int main() {

    // init map score to differenciate hands when they are equal
    for (unsigned int i=0; i<cards_p1.size(); ++i) {
        letter_scores_p1[cards_p1[i]] = i;
        letter_scores_p2[cards_p2[i]] = i;
    }

    ifstream ifs{input};
    string line;
    vector<Hand> hands;

    while (getline(ifs, line)) {
        line.erase(line.length()-1); // remove \n
        hands.push_back(Hand(line));
    }

    sort(hands.begin(), hands.end(), sort_hand_func_p1);

    int rank = 1;
    for (auto& h: hands)
        h.rank_m = rank++;

    unsigned int total_p1 = 0;

    for (const auto& h: hands)
        total_p1 += h.rank_m * h.bid_m;

    cout << "Part1: the total winning value is " << total_p1 << endl;


    unsigned int total_p2 = 0;

    sort(hands.begin(), hands.end(), sort_hand_func_p2);

    rank = 1;
    for (auto& h: hands)
        h.rank_m = rank++;

    for (const auto& h: hands)
        total_p2 += h.rank_m * h.bid_m;

    cout << "Part2: the total new winning value is " << total_p2 << endl;

    return 0;
}