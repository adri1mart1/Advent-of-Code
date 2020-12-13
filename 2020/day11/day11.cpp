// https://adventofcode.com/2020/day/11
// g++ day11.cpp -o pgm -std=c++11
#include <iostream>
#include <vector>
#include <fstream>

#define OCCUPIED '#'
#define EMPTY_SEAT 'L'
#define FLOOR '.'

void display(std::vector<std::vector<char>> &m) {
	for (auto l: m) {
		for (auto c: l)
			std::cout << c;
		std::cout << std::endl;
	}
	std::cout << std::endl;
}

bool spots_are_equal(std::vector<std::vector<char>> &a, std::vector<std::vector<char>> &b) {
	for (int i=0; i<a.size(); i++) {
		for (int j=0; j<a[i].size(); j++) {
			if (a[i][j] != b[i][j])
				return false;
		}
	}
	return true;
}

class Plane {
public:
	Plane() {}

	int count_adjacent_seats(int i, int j, std::vector<std::vector<char>> &map) {
		int cnt = 0;
		if (i > 0) {
			if (j > 0 && map[i-1][j-1] == OCCUPIED) // top left
				cnt++;
			if (map[i-1][j] == OCCUPIED) // top
				cnt++;
			if (j < map[i].size()-1 && map[i-1][j+1] == OCCUPIED) // top right
				cnt++;
		}
		if (i < map.size()-1) {
			if (j > 0 && map[i+1][j-1] == OCCUPIED) // bottom left
				cnt++;
			if (map[i+1][j] == OCCUPIED) // bottom
				cnt++;
			if (j < map[i].size()-1 && map[i+1][j+1] == OCCUPIED) // bottom right
				cnt++;
		}
		if (j > 0 && map[i][j-1] == OCCUPIED) // left
			cnt++;
		if (j < map[i].size()-1 && map[i][j+1] == OCCUPIED) // right
			cnt++;

		return cnt;
	}

	bool has_occupied_seat_adjacent(int i, int j, std::vector<std::vector<char>> &map) {
		if (count_adjacent_seats(i, j, map) > 0)
			return true;
		return false;
	}

	bool has_4plus_adjacent_occupied_seat(int i, int j, std::vector<std::vector<char>> &map) {
		if (count_adjacent_seats(i, j, map) >= 4)
			return true;
		return false;
	}

	int has_visible_occupied_seat(int i, int j, std::vector<std::vector<char>> &map, int x, int y) {
		int times = 1;

		while (1) {
			int x0 = i + times * x;
			int y0 = j + times * y;

			if (x0 < 0 || y0 < 0 || x0 >= map.size() || y0 >= map[i].size()) // out of map 
				return 0;
			if (map[x0][y0] == OCCUPIED)
				return 1;
			if (map[x0][y0] == EMPTY_SEAT)
				return 0;
			times++;
		}
	}

	int get_visible_adjacent_occupied_seat(int i, int j, std::vector<std::vector<char>> &map) {
		int nb_seat = has_visible_occupied_seat(i, j, map, -1, -1);
		nb_seat += has_visible_occupied_seat(i, j, map, -1,  0);
		nb_seat += has_visible_occupied_seat(i, j, map, -1,  1);
		nb_seat += has_visible_occupied_seat(i, j, map,  0, -1);
		nb_seat += has_visible_occupied_seat(i, j, map,  0,  1);
		nb_seat += has_visible_occupied_seat(i, j, map,  1, -1);
		nb_seat += has_visible_occupied_seat(i, j, map,  1,  0);
		nb_seat += has_visible_occupied_seat(i, j, map,  1,  1);
		return nb_seat;
	}
	bool has_5plus_visible_adjacent_occupied_seat(int i, int j, std::vector<std::vector<char>> &map) {
		if (get_visible_adjacent_occupied_seat(i, j, map) >= 5)
			return true;
		return false;
	}

	bool has_a_visible_occupied_seat_arround(int i, int j, std::vector<std::vector<char>> &map) {
		if (get_visible_adjacent_occupied_seat(i, j, map) > 0)
			return true;
		return false;
	}

	char process_spot(int i, int j, std::vector<std::vector<char>> &map) {
		if (map[i][j] == EMPTY_SEAT && !has_occupied_seat_adjacent(i, j, map))
			return OCCUPIED;

		if (map[i][j] == OCCUPIED && has_4plus_adjacent_occupied_seat(i, j, map))
			return EMPTY_SEAT;

		return map[i][j];
	}

	char process_spot_v2(int i, int j, std::vector<std::vector<char>> &map) {
		if (map[i][j] == EMPTY_SEAT && !has_a_visible_occupied_seat_arround(i, j, map))
			return OCCUPIED;

		if (map[i][j] == OCCUPIED && has_5plus_visible_adjacent_occupied_seat(i, j, map))
			return EMPTY_SEAT;

		return map[i][j];
	}

	void process_part2() {
		std::vector<std::vector<char>> copy = spots;

		for (int i=0; i<copy.size(); i++) {
			for (int j=0; j<copy[i].size(); j++)
				spots[i][j] = process_spot_v2(i, j, copy);
		}
	}

	void process() {
		std::vector<std::vector<char>> copy = spots;

		for (int i=0; i<copy.size(); i++) {
			for (int j=0; j<copy[i].size(); j++)
				spots[i][j] = process_spot(i, j, copy);
		}
	}

	int get_occupied_seats_num() {
		int res = 0;
		for (auto &l: spots) {
			for (auto &c: l) {
				if (c == OCCUPIED) 
					res++;
			}
		}
		return res;
	}

	std::vector<std::vector<char>> spots;
};

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	Plane init_plane, plane, plane_previous;

	while (std::getline(infile, line)) {
		std::vector<char> s;
		for (char c: line) 
			s.push_back(c);
		init_plane.spots.push_back(s);
	}

	plane.spots = init_plane.spots;

	while (1) {
		std::vector<std::vector<char>> prev_spots = plane.spots;
		plane.process();
		if (spots_are_equal(prev_spots, plane.spots))
			break;
	}
	std::cout << "Part1: Number of OCCUPIED seats: " << plane.get_occupied_seats_num() << std::endl;

	plane.spots = init_plane.spots;
	
	while (1) {
		std::vector<std::vector<char>> prev_spots = plane.spots;
		plane.process_part2();
		if (spots_are_equal(prev_spots, plane.spots))
			break;
	}

	std::cout << "Part2: Number of visible OCCUPIED seats: " << plane.get_occupied_seats_num() << std::endl;

	return 0;
}