

class Wedding:
    def __init__(self):
        pass
    
    def shuffle(self, guests):
        n = len(guests)
        result = []
        
        def dfs(path, visited):
            # dfs algorithm
            if len(path) == n:
                result.append("".join(path))
                return
            for i in range(n):
                if not visited[i]:
                    if guests[i] == guests[len(path)] or guests[i] == guests[(len(path) - 1) % n] or guests[i] == guests[(len(path) + 1) % n]:
                        visited[i] = True
                        dfs(path + [guests[i]], visited)
                        visited[i] = False

        dfs([], [False] * n)
        return result
    
    
    def barriers(self, guests, bars):
        n = len(guests)
        guests_with_bars = ""
        new_bars_position = bars.copy()
        bars_cnt = 0
        for i in range(n):
            if i in bars:
                guests_with_bars += "|"
                new_bars_position[bars_cnt] += bars_cnt
                bars_cnt += 1
            guests_with_bars += guests[i]
        guests = guests_with_bars
        n = len(guests)
        result = set()

        def valid_move(path):
            # filter the wrong arrangements
            for idx in new_bars_position:
                if path[idx] != '|':
                    return False
            return True

        def dfs(path, visited):
            # dfs algorithm
            if len(path) == n and valid_move(path):
                result.add("".join(path))
                return
            for i in range(n):
                if not visited[i]:
                    if guests[i] == guests[len(path)] or guests[i] == guests[(len(path) - 1) % n] or guests[i] == guests[(len(path) + 1) % n]:
                        visited[i] = True
                        dfs(path + [guests[i]], visited)
                        visited[i] = False

        dfs([], [False] * n)
        return list(result)


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
    # wedding = Wedding()
    # res_shuffle = wedding.shuffle("WXYZ")
    # print(res_shuffle)
    # res_barriers = wedding.barriers("ABxy", [2])
    # print(res_barriers)