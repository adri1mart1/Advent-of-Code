#
# This day16 wasn't the best puzzle I tried to solve.
# My original code was passing tests successfully and
# gave me a result for part 2 slightly above expected.
#
# I ended checking code of IanFindlay to understand
# and correct my initial code to solve this
# problem ->
# https://github.com/IanFindlay/advent-of-code/blob/master/2021/day_16.py
#

class Packet:

    def __init__(self, line):
        self.line = line
        self.version = int(self.line[0:3], 2)
        self.packetTypeID = int(self.line[3:6], 2)
        self.sub_packets = []
        self.decode_packet()

    def decode_packet(self):
        if self.packetTypeID == 4:
            self.value = self.get_literal_value()
        else:
            self.sub_packets = self.get_operators()
            self.value = self.get_calc_result()
        self.version_sum = self.sum_versions()

    def get_literal_value(self):
        v = ''
        i = 6
        while True:
            ind = self.line[i]
            v += self.line[i+1:i+5]
            i += 5
            if ind == '0':
                break

        self.length = i
        return int(v, 2)

    def get_operators(self):
        sp = []

        length_type = self.line[6]
        if length_type == '0':
            index = 22
            subpacket_length = int(self.line[7: index], 2)
            self.length = subpacket_length + index
            to_process = self.line[index: self.length]

            while True:
                sp.append(Packet(to_process))
                index = sp[-1].length
                if index == len(to_process):
                    break
                to_process = to_process[index:]
        else:
            index = 18
            subpacket_count = int(self.line[7:index], 2)

            self.length = index
            to_process = self.line[index:]
            while len(sp) != subpacket_count:
                sp.append(Packet(to_process))
                self.length += sp[-1].length
                index = sp[-1].length
                to_process = to_process[index:]
        return sp

    def sum_versions(self):
        version_sum = self.version
        for subpacket in self.sub_packets:
            version_sum += subpacket.sum_versions()
        return version_sum

    def get_calc_result(self):
        res = 0
        if self.packetTypeID == 0: # sum
            for p in self.sub_packets:
                res += p.get_calc_result()

        elif self.packetTypeID == 1: # product
            res = 1
            for p in self.sub_packets:
                res *= p.get_calc_result()

        elif self.packetTypeID == 2: # min
            m = 999999
            for p in self.sub_packets:
                if p.get_calc_result() < m:
                    m = p.get_calc_result()
            res = m

        elif self.packetTypeID == 3: # max
            m = 0
            for p in self.sub_packets:
                if p.get_calc_result() > m:
                    m = p.get_calc_result()
            res = m

        elif self.packetTypeID == 4:
            return self.value

        elif self.packetTypeID == 5: # greater than
            assert(len(self.sub_packets) == 2)
            if self.sub_packets[0].value > self.sub_packets[1].value:
                res = 1
            else:
                res = 0

        elif self.packetTypeID == 6: # less than
            assert(len(self.sub_packets) == 2)
            if self.sub_packets[0].value < self.sub_packets[1].value:
                res = 1
            else:
                res = 0

        elif self.packetTypeID == 7: # equals to
            assert(len(self.sub_packets) == 2)
            if self.sub_packets[0].value == self.sub_packets[1].value:
                res = 1
            else:
                res = 0

        else:
            assert(False)
        return res

with open("in.txt") as f:
    msg = f.readline().rstrip()
    binary = bin(int(msg, 16))[2:].zfill(len(msg)*4)

p = Packet(binary)

print("part1: version additionned: {}".format(p.version_sum))
print("part2: hex encoded result: {}".format(p.value))
