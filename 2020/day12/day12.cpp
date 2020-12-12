// https://adventofcode.com/2020/day/12
// g++ day12.cpp -o pgm -std=c++11
#include <iostream>
#include <vector>
#include <fstream>
#include <regex>
#include <map>
#include <cmath>

#define NORTH 0
#define EAST  90
#define SOUTH 180
#define WEST  270

#define PI 3.14159265
#define TO_RADIAN(a) (a*PI/180.0)

class Ship {
public:
	Ship() :
		cap(EAST), x(0), y(0) {}

	void feed(std::string s) {
		int v;
		std::regex r(R"(\d+$)");
		std::smatch m;
		if (std::regex_search(s, m, r))
			v = std::stoi(m.str());

		switch (s[0]) {
			case 'N':
				y += v;
			break;
			case 'S':
				y -= v;
			break;
			case 'E':
				x += v;
			break;
			case 'W':
				x -= v;
			break;
			case 'L':
				cap -= v;
				cap += 360;
				cap %= 360;
			break;
			case 'R':
				cap += v;
				cap %= 360;
			break;
			case 'F':
				switch (cap) {
					case NORTH:
						y += v;
					break;
					case EAST:
						x += v;
					break;
					case SOUTH:
						y -= v;
					break;
					case WEST:
						x -= v;
					break;
				}
			break;
		}
	}

	void feedwp(std::string s) {
		int v;
		std::regex r(R"(\d+$)");
		std::smatch m;
		if (std::regex_search(s, m, r))
			v = std::stoi(m.str());

		switch (s[0]) {
			case 'N':
				wayp_y += v;
			break;
			case 'S':
				wayp_y -= v;
			break;
			case 'E':
				wayp_x += v;
			break;
			case 'W':
				wayp_x -= v;
			break;
			case 'L':
			case 'R': {
				int sign = 1;
				if (s[0] == 'R')
					sign = -1;

				int c = (int)cos(sign * TO_RADIAN(v));
				int s = (int)sin(sign * TO_RADIAN(v));
				int oldx = wayp_x;
				int oldy = wayp_y;

				wayp_x = oldx * c - oldy * s;
				wayp_y = oldx * s + oldy * c;
			}
			break;
			case 'F':
				x += (v * wayp_x);
				y += (v * wayp_y);
			break;
		}
	}

	int manhattan_dist() {
		return std::abs(x) + std::abs(y);
	}

	std::string pos() {
		return "x:" + std::to_string(x) + " y:" + std::to_string(y);
	}

	int x, y;
	int wayp_x, wayp_y;
	int cap;
};

int main(int argc, char *argv[]) {

	std::ifstream infile("in.txt");
	std::string line;
	Ship ship;

	while (std::getline(infile, line))
		ship.feed(line);

	std::cout << "Part1: Ship final pos: " << ship.pos() << " manhattan distance: " << ship.manhattan_dist() << std::endl;

	Ship wpship;
	wpship.wayp_x = 10;
	wpship.wayp_y = 1;

	infile.clear();
	infile.seekg(0, std::ios::beg);

	while (std::getline(infile, line))
		wpship.feedwp(line);

	std::cout << "Part2: Ship final pos: " << wpship.pos() << " manhattan distance: " << wpship.manhattan_dist() << std::endl;

	return 0;
}