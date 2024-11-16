from itertools import product
class Wedding:
    def __init__(self):
        self.seats = []


    def line(self, guests):
        if len(guests) <= 2:
            return [guests] if len(guests) == 1 else [guests, guests[::-1]]

        seat1 = [guests[0] + item for item in self.line(guests[1:])]
        seat2 = [guests[1] + guests[0] + item for item in self.line(guests[2:])]

        return seat1 + seat2

    def shuffle_process(self, guests):
        if len(guests) <= 2:
            return self.line(guests)
        seats = []
        seats.extend(guests[0] + i for i in self.line(guests[1:]))
        seats.extend(guests[1] + guests[0] + i for i in self.line(guests[2:]))
        seats.append(guests[-1] + guests[:-1])
        reversed_middle = ''.join(reversed(guests[1:-1]))
        seats.extend(guests[-1] + ''.join(reversed(i)) + guests[0] for i in self.line(reversed_middle))
        seats.append(guests[1:] + guests[0])
        return seats

    def iteration(self, seats):
        return list(product(*seats))

    def barriers_process(self, guests, bars):
        line_list = []

        start = 0
        for bar in bars:
            if bar != 0:
                line_list.append(guests[start:bar])
                start = bar

        if start != len(guests):
            if bars and bars[0] != 0:
                line_list[0] = guests[start:] + line_list[0]
            else:
                line_list.append(guests[start:])
        barriers = [self.line(item) for item in line_list]

        iteration_rst = self.iteration(barriers)
        ite_results = []

        for ite_rst in iteration_rst:
            ite_str = ''.join(ite_rst)
            if bars[0] != 0:
                temp_str1 = ite_str[:len(guests) - bars[-1]]
                temp_str2 = ite_str[len(guests) - bars[-1]:]
                ite_str = temp_str2 + temp_str1

            for index, bar in enumerate(bars):
                ite_str = ite_str[:bar + index] + '|' + ite_str[bar + index:]
            ite_results.append(ite_str)

        return ite_results

    def shuffle(self, guests):
        seats = self.shuffle_process(guests)
        return seats

    def barriers(self, guests, bars):
        seats = self.barriers_process(guests, bars)
        return seats



def show_result(v, partial=False, ind=None):
    v.sort()
    if not partial:
        print(len(v), "\n".join(v), sep="\n")
    else:
        print(len(v), v[ind], sep="\n")


def standard_tests():
    standard = Wedding()
    res = standard.shuffle("abc")
    show_result(res)

    res = standard.shuffle("WXYZ")
    show_result(res)

    res = standard.barriers("xyz", [0])
    show_result(res)

    res = standard.shuffle("abc")
    show_result(res)

    res = standard.shuffle("abcdefXY")
    show_result(res)

    res = standard.barriers("abcDEFxyz", [2, 5, 7])
    show_result(res)

    res = standard.barriers("ABCDef", [4])
    show_result(res)

    res = standard.barriers("bgywqa", [0, 1, 2, 4, 5])
    show_result(res)

    res = standard.barriers("n", [0])
    show_result(res)
    res = standard.shuffle("hi")
    show_result(res)


def main():
    print("""Type quit to exit.
Commands:
tests
s guests
b guests n barriers
sp guests ind
bp guests n barriers ind
""")
    w = Wedding()
    while True:
        asktype = input().split()
        if not asktype or asktype[0] == "quit":
            break
        elif asktype[0] == "tests":
            standard_tests()
        elif asktype[0] == "s":
            guests = asktype[1]
            r = w.shuffle(guests)
            show_result(r)
        elif asktype[0] == "b":
            guests, nbar, bars = asktype[1], asktype[2], asktype[3:]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r)
        elif asktype[0] == "sp":
            guests, ind = asktype[1:]
            r = w.shuffle(guests)
            show_result(r, True, int(ind))
        elif asktype[0] == "bp":
            guests, nbar, bars, ind = asktype[1], asktype[2], asktype[3:-1], asktype[-1]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r, True, int(ind))


if __name__ == '__main__':
    main()