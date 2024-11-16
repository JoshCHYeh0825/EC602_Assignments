"""
Homework 4 for BU EC602
"""

import itertools


class Wedding:
    """Class that solves the wedding table musical chairs problem"""

    def __init__(self):
        pass

    def shuffle(self, guests):
        """Function performing a circular suffle"""
        # Really, this is just 2 cases of 1 barrier case
        # Thus more efficient to call that twice
        all_seatings = self.meta_shuffle(guests, wrap=True)
        return all_seatings

    def barriers(self, guests, bars):
        """Function performing suffle with barries preventing guests
        from moving past them."""
        if len(bars) == 0:
            self.shuffle(guests)

        if not all(x >= 0 for x in bars):
            raise ValueError

        panels = []
        panels.append(guests[bars[-1]:] + guests[:bars[0]])
        for baridx in range(1, len(bars)):
            panels.append(guests[bars[baridx-1]:bars[baridx]])

        subseatings = []
        for subguests in panels:
            sublist = self.meta_shuffle(subguests, False)
            subseatings.append(sublist)

        fullseatings = []
        for pair in itertools.product(*subseatings):
            if bars[0] == 0:
                startstr = '|'
                laststr = pair[0]
            else:
                startstr = pair[0][-bars[0]:] + '|'
                laststr = pair[0][:(len(guests) - bars[-1])]
            for group in pair[1:]:
                startstr += group
                startstr += '|'
            startstr += laststr
            fullseatings.append(startstr)
            # print(''.join(pair))

        # Finally, need to go through and make all the possible
        # permutations of the sub seatings
        return fullseatings

    def meta_shuffle(self, guests, wrap=True):
        """Top level of the suffling, This will work for a generic case
        of sequential guests.
        Wrapping can be true or false (false for barrier case subgroup)"""
        lineup = [None]*len(guests)
        return self.next_guest(guests, 0, lineup, wrap=wrap)

    def next_guest(self, guests, seat, lineup, *, wrap=False):
        """Recursive suffling, goes through each guest in order and
        attempts to shuffle
        1. no shuffle
        2. shuffle left
        3. shuffle right"""
        # If seat has reached the end of the line, we've finished the lineup
        if seat >= len(lineup):
            return [''.join(lineup)]
        # Otherwise, continue in the recursion...
        seatings = []
        if lineup[seat] is None:
            new_lineup = lineup.copy()
            new_lineup[seat] = guests[seat]
            new_set = self.next_guest(guests, seat+1, new_lineup, wrap=wrap)
            seatings.extend(new_set)
        # Try moving left:
        if seat-1 >= 0 and lineup[seat-1] is None:
            new_lineup = lineup.copy()
            new_lineup[seat-1] = guests[seat]
            new_set = self.next_guest(guests, seat+1, new_lineup, wrap=wrap)
            seatings.extend(new_set)
        elif seat-1 < 0 and wrap and lineup[len(lineup)-1] is None \
                and len(lineup) > 2:
            new_lineup = lineup.copy()
            new_lineup[len(lineup)-1] = guests[seat]
            new_set = self.next_guest(guests, seat+1, new_lineup, wrap=wrap)
            seatings.extend(new_set)

        # Try moving right
        if seat + 1 < len(lineup) and lineup[seat+1] is None:
            new_lineup = lineup.copy()
            new_lineup[seat+1] = guests[seat]
            new_set = self.next_guest(guests, seat+1, new_lineup, wrap=wrap)
            seatings.extend(new_set)
        elif seat + 1 >= len(lineup) and wrap and lineup[0] is None \
                and len(lineup) > 2:
            new_lineup = lineup.copy()
            new_lineup[0] = guests[seat]
            new_set = self.next_guest(guests, seat+1, new_lineup, wrap=wrap)
            seatings.extend(new_set)
        return seatings


def show_result(v, partial=False, ind=None):
    """show_result - predefined function to display result"""
    v.sort()
    if not partial:
        print(len(v), "\n".join(v), sep="\n")
    else:
        print(len(v), v[ind], sep="\n")


def standard_tests():
    """standard_tests - predefined function to run a standard test"""
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
    """main execution function. Asks for user input for commands"""
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
        if asktype[0] == "tests":
            standard_tests()
        elif asktype[0] == "s":
            guests = asktype[1]
            r = w.shuffle(guests)
            show_result(r)
        elif asktype[0] == "b":
            guests, nbar, bars = asktype[1], asktype[2], asktype[3:]
            if nbar != len(bars):
                pass
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r)
        elif asktype[0] == "sp":
            guests, ind = asktype[1:]
            r = w.shuffle(guests)
            show_result(r, True, int(ind))
        elif asktype[0] == "bp":
            guests, nbar, bars, ind = asktype[1], asktype[2], asktype[3:-1], \
                asktype[-1]
            if nbar != len(bars):
                pass
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r, True, int(ind))


if __name__ == '__main__':
    main()