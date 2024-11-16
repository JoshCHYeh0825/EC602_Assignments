
from itertools import product



class Wedding:
    

    def __init__(self):
        pass

    #The master of ceremonies asks all the guests to stand, 
    # and sit back down either one seat to the left, 
    # one seat to the right, or in the same chair.
    
    def circular_table(self, chars, num_chars, direction='right'):
        if direction == 'right':
            return chars[-num_chars:] + chars[:-num_chars]
        else:
            direction == 'left'
            return chars[num_chars:] + chars[:num_chars]
       
    
    # add new guests to the circular table. make rearrangements
    # to ensure that no guests is seated next to the same person twice.
    
    def add_guests(self, initial: str, final: str) -> list:
        if len(initial) == 0:
            return [final]

        arrangements = []
        for i in range(len(initial)):
            new_arrangements = self.circular_table(initial, i+1) + final
            ri = self.circular_table(new_arrangements, 1, direction='right')
            le = self.circular_table(new_arrangements, 1, direction='left')
            ri_c = self.circular_table(ri, 1, direction='right')
            le_c = self.circular_table(le, 1, direction='left')
            possible_arrangement = [new_arrangements, ri, le, ri_c, le_c]
            for j in possible_arrangement:
                if all(j[k] != j[k+1] for k in range(len(j)-1)):
                    arrangements.append(j)

        return arrangements    

    # find all the possible arrangments  of the guests specified as a list of strings
    def possible_arrangements(self, guests: str) -> list:
        if len(guests) == 1:
            return [guests[0]]
        if len(guests) == 0:
            return None

        possible_arrangement = [guests[0]]

        for i in range(1, len(guests)):
            sets = []
            initial = guests[0:i] + guests[i]

            for j in possible_arrangement:
                new_arrangements = self.add_guests(j, guests[i])

                for k in new_arrangements:
                    for n in initial:
                        if abs(initial.index(n) - k.index(n)) > 1:

                            # disc
                            break
                    else:
                        sets.append(k)

            possible_arrangement = list(set(sets))
        return sorted(possible_arrangement)

 


    
    def shuffle(self, guests: str) -> list:
        if len(guests) == 1:
            return [guests[0]]
        if len(guests) == 0:
            return None
        if len(guests) == 2:
            return [guests, guests[1] + guests[0]]

        arrangement = set()
        possible_arrangement = self.possible_arrangements(guests[0:len(guests) - 1])

        initial = list(guests)
        initial_indices = {guest: index for index, guest in enumerate(initial)}

        for j in possible_arrangement:
            new_arrangement = self.add_guests(j, guests[len(guests) - 1])

            for k in new_arrangement:
                final = list(k)
                for i in initial:
                    index_diff = abs(initial_indices[i] - final.index(i))
                    if index_diff > 1 and index_diff != (len(initial) - 1):
                        break
                else:
                    arrangement.add(k)

        return sorted(list(arrangement))

    def barriers(self, guests: str, bars: list) -> list:
        lists = [self.possible_arrangements(guests[v:bars[i+1]]) if i != len(bars) - 1 else self.possible_arrangements(guests[v:] + guests[:bars[0]]) for i, v in enumerate(bars)]
        combinations = [''.join(i) for i in product(*lists)]
        possible_arrangement = []

        for i in combinations:
            i = self.circular_table(i, bars[0], direction='right')
            arr = 0
            for j in bars:
                parts = [i[:j+arr], '|', i[j+arr:]]
                i = ''.join(parts)
                arr += 1
            possible_arrangement.append(i)
        # Remove duplicates
        possible_arrangement = list(set(possible_arrangement))

        return possible_arrangement


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


