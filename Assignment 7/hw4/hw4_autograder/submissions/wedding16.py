





class Wedding:
    def __init__(self):
        self.guests = set()

    def shuffle(self, guests):
        n = len(guests)
        self.res = set()

        def is_valid(seating):
            return len(set(seating)) == n and None not in seating

        def backtrack(seating, guest_index):
            if guest_index == n:
                if is_valid(seating):
                    self.res.add("".join(seating))
                return

            # Try to move to left
            left_index = (guest_index - 1) % n
            new_seating = seating.copy()
            new_seating[left_index] = guests[guest_index]
            backtrack(new_seating, guest_index + 1)

            # Try to stay at the same place
            new_seating = seating.copy()
            new_seating[guest_index] = guests[guest_index]
            backtrack(new_seating, guest_index + 1)

            # Try to move to right
            right_index = (guest_index + 1) % n
            new_seating = seating.copy()
            new_seating[right_index] = guests[guest_index]
            backtrack(new_seating, guest_index + 1)

        # Start backtracking with empty seating and the first guest
        backtrack([None] * n, 0)

        return list(self.res)

    def barriers(self, guests, bars):
        n = len(guests)
        self.res = set()

        def is_valid(seating):
            return len(set(seating)) == n and None not in seating

        def insert_barriers(seating):
            seating_with_bars = []
            for idx, char in enumerate(seating):
                if idx in bars:
                    seating_with_bars.append("|")
                seating_with_bars.append(char)
            return "".join(seating_with_bars)

        def backtrack(seating, guest_index):
            if guest_index == n:
                if is_valid(seating):
                    self.res.add(insert_barriers("".join(seating)))
                return

            # Try to move to left
            left_index = (guest_index - 1) % n
            if guest_index not in bars:  # Ensure there's no barrier on the left
                new_seating = seating.copy()
                new_seating[left_index] = guests[guest_index]
                backtrack(new_seating, guest_index + 1)

            # Try to stay at the same place
            new_seating = seating.copy()
            new_seating[guest_index] = guests[guest_index]
            backtrack(new_seating, guest_index + 1)

            # Try to move to right
            right_index = (guest_index + 1) % n
            if right_index not in bars:  # Ensure there's no barrier on the right
                new_seating = seating.copy()
                new_seating[right_index] = guests[guest_index]
                backtrack(new_seating, guest_index + 1)

        # Start backtracking with empty seating and the first guest
        backtrack([None] * n, 0)

        return list(self.res)


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
    print(
        """Type quit to exit.
Commands:
tests
s guests
b guests n barriers
sp guests ind
bp guests n barriers ind
"""
    )
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


if __name__ == "__main__":
    main()