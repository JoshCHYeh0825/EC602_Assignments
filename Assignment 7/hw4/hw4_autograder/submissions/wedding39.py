

import itertools

class Wedding:
    def __init__(self):
        pass

    def shuffle(self, guests):
        guest_list = list(guests)
        arrangements = []

        def generate_permutations(arrangement, remaining_guests):
            if not remaining_guests:
                arrangements.append(''.join(arrangement))
            else:
                for i in range(len(remaining_guests)):
                    new_arrangement = arrangement + [remaining_guests[i]]
                    new_remaining = remaining_guests[:i] + remaining_guests[i+1:]
                    generate_permutations(new_arrangement, new_remaining)

        generate_permutations([], guest_list)
        return arrangements

    def barriers(self, guests, bars):
        guest_list = list(guests)
        arrangements = []

        def generate_combinations(arrangement, remaining_guests):
            if not remaining_guests:
                arrangements.append(''.join(arrangement))
            else:
                for i in range(len(remaining_guests)):
                    new_arrangement = arrangement + [remaining_guests[i]]
                    new_remaining = remaining_guests[:i] + remaining_guests[i+1:]
                    generate_combinations(new_arrangement, new_remaining)

        for combination in itertools.combinations(guest_list, len(bars)):
            arrangement = list(combination)
            remaining_guests = [g for g in guest_list if g not in arrangement]
            for i in range(len(bars)):
                index = guest_list.index(arrangement[i])
                remaining_guests.insert(index, '|')
            generate_combinations([], remaining_guests)
        
        return arrangements

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
            guests, ind = asktype[1], asktype[2]
            r = w.shuffle(guests)
            show_result(r, True, int(ind))
        elif asktype[0] == "bp":
            guests, nbar, bars, ind = asktype[1], asktype[2], asktype[3:-1], asktype[-1]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r, True, int(ind))

if __name__ == '__main__':
    main()
