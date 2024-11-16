class Wedding:
    def __int__(self, index=None):
        if index == None:
            self.index = []

    def shuffle(self, guests):
        guestsa = [char for char in guests]
        result = []
        n = len(guestsa)
        if n>2:
            line_e = self.generate_sequences(n)
        else:
            line_e = [[0,0],[0,1]]
        m = len(line_e)
        for i in range(0, m):
            temp = []
            temp_indices = line_e[i]
            [temp.append(sublist) for sublist in guestsa]
            for j in range(0, n):
                if temp_indices[j] == 1:
                    self.swapper(temp, j)
            result_string = ''.join(temp)
            result.append(result_string)
        if n > 2:
            temp = [guestsa[-1]] + guestsa[:-1]
            result_string = ''.join(temp)
            result.append(result_string)
            temp = guestsa[1:] + [guestsa[0]]
            result_string = ''.join(temp)
            result.append(result_string)
        return result

    def barriers(self, guests, bars):
        guestsa = [char for char in guests]
        result = []
        n = len(guestsa)
        line_e = self.generate_sequences_b(n,bars)
        m = len(line_e)
        for i in range(0, m):
            temp = []
            temp_indices = line_e[i]
            [temp.append(sublist) for sublist in guestsa]
            for j in range(0, n):
                if temp_indices[j] == 1:
                    self.swapper(temp, j)
            l = 0
            for bar in bars:
                temp.insert(bar+l, '|')
                l += 1
            result_string = ''.join(temp)
            result.append(result_string)
        return result

    def swapper(self, index, i):
        if i < len(index) - 1:
            temp = index[i]
            index[i] = index[i + 1]
            index[i + 1] = temp
        elif i == len(index) - 1:
            temp = index[i]
            index[i] = index[0]
            index[0] = temp

    def generate_sequences(self, n):
        sequences = []

        stack = [(0, [])]
        while stack:
            index, sequence = stack.pop()

            if index == n:
                if sequence and sequence[0] * sequence[-1] != 1:
                    sequences.append(sequence)
            else:
                for value in [1, 0]:
                    if not sequence or (sequence[-1] == 0) or (sequence[-1] == 1 and value == 0):
                        stack.append((index + 1, sequence + [value]))

        return sequences

    def generate_sequences_b(self, n, bars=None):
        sequences = []
        if bars!=None:
            bar = [x-1 for x in bars]
        stack = [(0, [])]
        while stack:
            index, sequence = stack.pop()

            if index == n:
                if sequence and sequence[0] * sequence[-1] != 1:
                    valid_sequence = True
                    if bar:
                        for pos in bar:
                            if sequence[pos] == 1:
                                valid_sequence = False
                                break
                    if valid_sequence:
                        sequences.append(sequence)
            else:
                for value in [1, 0]:
                    if not sequence or (sequence[-1] == 0) or (sequence[-1] == 1 and value == 0):
                        stack.append((index + 1, sequence + [value]))

        return sequences

def  show_result(v, partial=False,ind=None):
  v.sort()
  if not partial:
    print(len(v),"\n".join(v),sep="\n")
  else:
    print(len(v),v[ind],sep="\n")


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
            break;
        elif asktype[0] == "tests":
            standard_tests()
        elif asktype[0] == "s":
            guests = asktype[1]
            r = w.shuffle(guests)
            show_result(r);
        elif asktype[0] == "b":
            guests, nbar, bars = asktype[1], asktype[2], asktype[3:]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r)
        elif asktype[0] == "sp":
            guests, ind = asktype[1:]
            r = w.shuffle(guests);
            show_result(r, True, int(ind));
        elif asktype[0] == "bp":
            guests, nbar, bars, ind = asktype[1], asktype[2], asktype[3:-1], asktype[-1]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r, True, int(ind))


if __name__ == '__main__':
    main()