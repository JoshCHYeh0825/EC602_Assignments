
def countem(coll):
    val = [0] * len(coll)
    while True:
        yield val
        j = 0
        val[j] += 1
        while val[j] == coll[j]:
            val[j] = 0
            j += 1
            if j == len(coll):
                return
            val[j] += 1


class Wedding:

    def __init__(self):
        self.panels = [(tuple(), ), ((0,), )]
        self.circles = [(tuple(), ), ((0,), ), ((0, 1), (1, 0))]

    def linear(self, tablesize, guests=None):
        i = len(self.panels)
        while i <= tablesize:
            stay = tuple(ans + (i-1,) for ans in self.panels[i-1])
            swap = tuple(ans + (i-1, i-2) for ans in self.panels[i-2])
            self.panels.append(stay + swap)
            i += 1

        if guests:
            res = []
            for tab in self.panels[tablesize]:
                res.append("".join(guests[tab[i]] for i in range(len(guests))))
            return res

    def shuffle(self, guests):
        gnum = len(guests)
        self.linear(gnum-1)

        i = len(self.circles)
        while i <= gnum:
            # stay at end
            stay = tuple(ans + (i-1,) for ans in self.panels[i-1])
            # swap with end
            swapz = tuple(ans + (i-1, i-2) for ans in self.panels[i-2])
            # swap with start
            swapa = tuple((i-1,) + tuple(x+1 for x in ans) + (0,)
                          for ans in self.panels[i-2])
            # 0123 -> 3012
            rotl = ((i-1,) + tuple(x for x in range(i-1))),
            # 0123 -> 1230
            rotr = (tuple(x for x in range(1, i)) + (0,)),

            self.circles.append(stay + swapa + swapz + rotl + rotr)

            i += 1

        return ["".join(guests[t[i]] for i in range(gnum))
                for t in self.circles[gnum]]

    def barriers(self, guests, bars):
        if not bars:
            return self.shuffle(guests)

        gnum = len(guests)
        bars.sort()
        bnum = len(bars)

        offset = bars[0]
        doubleguests = guests + guests
        bars.append(offset+gnum)
        res = []
        count = 1
        counter = []
        for i in range(bnum):
            guestslice = doubleguests[bars[i]:bars[i+1]]

            res.append(self.linear(len(guestslice), guestslice))
            gcount = len(res[-1])

            counter.append(gcount)
            count *= gcount

        ans = []
        for clock in countem(counter):
            barres = "|".join(res[i][clock[i]] for i in range(bnum))
            if offset:
                ans.append(barres[-offset:]+"|"+barres[:-offset])
            else:
                ans.append("|"+barres)
        return ans


def show_result(results, partial=False, ind=None):
    results.sort()
    if not partial:
        print(len(results), "\n".join(results), sep="\n")
    else:
        print(len(results), results[ind], sep="\n")


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
    "interactive session for wedding"

    print("""Type quit to exit.
Commands:
tests
s guests
b guests n barriers
sp guests ind
bp guests n barriers ind
""")
    wed = Wedding()
    while True:
        asktype = input().split()
        if not asktype or asktype[0] == "quit":
            break

        if asktype[0] == "tests":
            standard_tests()
        elif asktype[0] == "s":
            guests = asktype[1]
            ans = wed.shuffle(guests)
            show_result(ans)
        elif asktype[0] == "b":
            guests, _, bars = asktype[1], asktype[2], asktype[3:]
            ans = wed.barriers(guests, [int(x) for x in bars])
            show_result(ans)
        elif asktype[0] == "sp":
            guests, ind = asktype[1:]
            ans = wed.shuffle(guests)
            show_result(ans, True, int(ind))
        elif asktype[0] == "bp":
            guests, _, bars, ind = \
                asktype[1], asktype[2], asktype[3:-1], asktype[-1]
            ans = wed.barriers(guests, [int(x) for x in bars])
            show_result(ans, True, int(ind))


if __name__ == '__main__':
    main()
