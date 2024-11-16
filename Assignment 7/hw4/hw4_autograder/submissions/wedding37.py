from itertools import permutations

class Wedding:
    def __init__(self):
        # self.guests = guests
        pass

    def shuffle(self, guests):
        def is_valid(permutation):
            for i, guest in enumerate(permutation):
                if guest not in {guests[i], guests[i - 1], guests[(i + 1) % len(guests)]}:
                    return False
            return True

        return sorted(''.join(p) for p in set(permutations(guests)) if is_valid(p))

    def barriers(self, guests, bars):
        def insert_barriers(perm):
            perm_list = list(perm)
            for bar in sorted(bars, reverse=True):
                perm_list.insert(bar, '|')
            return ''.join(perm_list)

        def is_valid(perm):
            for i in range(len(guests)):
                if guests[i] != perm[i] and guests[i-1] != perm[i] and guests[(i+1) % len(guests)] != perm[i]:
                    return False
                if i in bars:
                    if guests[i] == perm[i-1] and guests[i-1] == perm[i]:
                        return False
                    if guests[i] == perm[i-1] and guests[(i+1) % len(guests)] == perm[i]:
                        return False
                    if guests[i] == perm[(i+1) % len(guests)] and guests[i-1] == perm[i]:
                        return False
            if len(guests) in bars:
                if guests[0] == perm[-1] and guests[-1] == perm[0]:
                    return False
                if guests[0] == perm[-1] and guests[(0+1) % len(guests)] == perm[0]:
                    return False
                if guests[0] == perm[(0+1) % len(guests)] and guests[-1] == perm[0]:
                    return False
            return True

        results = set()
        if len(guests)<=1:
            results.add(insert_barriers(guests))
        elif len(guests)==2:
            if (0 in bars or 2 in bars) and 1 in bars:
                results.add(insert_barriers(guests))
            else:
                results.add(insert_barriers(guests))
                results.add(insert_barriers(reversed(guests)))
        else:
            for perm in permutations(guests):
                if is_valid(perm):
                    results.add(insert_barriers(perm))

        return sorted(results)

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