class Wedding:
    def setShuffleGuests(self, guests, low, high, shuffleGuests):
        if low == high:
            shuffleGuests.append(guests)
        else:
            for i in range(low, high+1):
                guests = list(guests)
                guests[low], guests[i] = guests[i], guests[low]
                guests = ''.join(guests)
                self.setShuffleGuests(guests, low+1, high, shuffleGuests)
                guests = list(guests)
                guests[low], guests[i] = guests[i], guests[low]
                guests = ''.join(guests)

    def setShuffleBarriers(self, str, shuffleGuestsWithBarriers, i, temp):
        if i == len(str):
            shuffleGuestsWithBarriers.append(temp[:-1])
        else:
            for j in range(len(str[i])):
                self.setShuffleBarriers(str, shuffleGuestsWithBarriers, i+1, temp+str[i][j]+"|")

    def shuffle(self, guests):
        shuffleGuests = []
        self.setShuffleGuests(guests, 0, len(guests)-1, shuffleGuests)
        return shuffleGuests

    def shuffle_barriers(self, guests, barriers):
        shuffleGuestsWithBarrier = []
        str = []
        subString = []
        barriers.sort()
        subString.append(guests[:barriers[0]])
        for i in range(1, len(barriers)):
            subString.append(guests[barriers[i-1]:barriers[i]])
        subString.append(guests[barriers[-1]:])
        for i in subString:
            temp = []
            self.setShuffleGuests(i, 0, len(i)-1, temp)
            str.append(temp)
        self.setShuffleBarriers(str, shuffleGuestsWithBarrier, 0, "")
        return shuffleGuestsWithBarrier


def show_result(v, partial=False, n=0):
    v.sort()
    print(len(v))
    if partial:
        print(v[n])
    else:
        for c in v:
            for e in c:
                print(e, end="")
            print()


def standard_tests():
    standard = Wedding()
    res = standard.shuffle("abc")
    show_result(res)
    res = standard.shuffle("WXYZ")
    show_result(res)
    res = standard.shuffle_barriers("xyz", [0])
    show_result(res)
    res = standard.shuffle("abc")
    show_result(res)
    res = standard.shuffle("YabcdefX")
    show_result(res)
    res = standard.shuffle_barriers("abcDEFxyz", [2, 5, 7])
    show_result(res)
    res = standard.shuffle_barriers("ABCDef", [4])
    show_result(res)
    res = standard.shuffle_barriers("bgywqa", [0, 1, 2, 4, 5])
    show_result(res)
    res = standard.shuffle_barriers("n", [0])
    show_result(res)
    res = standard.shuffle("hi")
    show_result(res)


if __name__ == "__main__":
    w = Wedding()
    asktype = ""
    guests = ""
    nbar = 0
    ind = 0
    barriers = []
    print("Type quit to exit.")
    print("Commands:")
    print("tests")
    print("s guests")
    print("b guests n barriers")
    print("sp guests ind")
    print("bp guests n barriers ind")
    while True:
        asktype = input()
        if asktype == "quit":
            break
        elif asktype == "tests":
            standard_tests()
        elif asktype == "s":
            guests = input()
            r = w.shuffle(guests)
            show_result(r)
        elif asktype == "b":
            guests = input()
            nbar = int(input())
            barriers = [int(input()) for _ in range(nbar)]
            r = w.shuffle_barriers(guests, barriers)
            show_result(r)
        elif asktype == "sp":
            guests = input()
            ind = int(input())
            r = w.shuffle(guests)
            show_result(r, True, ind)
        elif asktype == "bp":
            guests = input()
            nbar = int(input())
            barriers = [int(input()) for _ in range(nbar)]
            ind = int(input())
            r = w.shuffle_barriers(guests, barriers)
            show_result(r, True, ind)