class Wedding:
    """
    Class to generate all combinations of seating arrangements for a wedding.
    Includes an additional barrier method for specific constraints.
    """

    def __init__(self, index=None):
        """
        Initialize the Wedding instance.

        Args:
            index (list, optional): List of indices for predefined operations.
                                    Defaults to None.
        """
        if index is None:
            self.index = []

    def shuffle(self, guests: str) -> list:
        """
        Generates all possible combinations of seating arrangements for guests.

        Args:
            guests (str): A string of individual guests as characters.

        Returns:
            list: A list of shuffled guest arrangements.
        """
        guestsa = list(guests)
        result = []
        n = len(guestsa)

        if n > 2:
            line_e = self.generate_sequences(n)
        else:
            line_e = [[0, 0], [0, 1]]

        m = len(line_e)

        for i in range(m):
            temp = guestsa[:]
            temp_indices = line_e[i]

            for j in range(n):
                if temp_indices[j] == 1:
                    self.swapper(temp, j)

            result.append("".join(temp))

        if n > 2:
            result.append("".join([guestsa[-1]] + guestsa[:-1]))
            result.append("".join(guestsa[1:] + [guestsa[0]]))

        return result

    def barriers(self, guests: str, bars: list) -> list:
        """
        Generates guest arrangements with barriers.

        Args:
            guests (str): A string of individual guests as characters.
            bars (list): List of barrier positions.

        Returns:
            list: A list of guest arrangements with barriers.
        """
        guestsa = list(guests)
        result = []
        n = len(guestsa)
        line_e = self.generate_sequences_b(n, bars)
        m = len(line_e)

        for i in range(m):
            temp = guestsa[:]
            temp_indices = line_e[i]

            for j in range(n):
                if temp_indices[j] == 1:
                    self.swapper(temp, j)

            bar_pos = 0
            for bar in bars:
                temp.insert(bar + bar_pos, "|")
                bar_pos += 1

            result.append("".join(temp))

        return result

    def swapper(self, index: list, i: int):
        """
        Swaps adjacent elements in a list.

        Args:
            index (list): The list of elements.
            i (int): The index of the element to swap with the next.
        """
        if i < len(index) - 1:
            index[i], index[i + 1] = index[i + 1], index[i]
        elif i == len(index) - 1:
            index[i], index[0] = index[0], index[i]

    def generate_sequences(self, n: int) -> list:
        """
        Generates valid sequences for shuffling.

        Args:
            n (int): The length of the sequence.

        Returns:
            list: A list of valid binary sequences.
        """
        sequences = []
        stack = [(0, [])]

        while stack:
            index, sequence = stack.pop()
            if index == n:
                if sequence and sequence[0] * sequence[-1] != 1:
                    sequences.append(sequence)
            else:
                for value in [1, 0]:
                    if (not sequence or sequence[-1] == 0 or
                            (sequence[-1] == 1 and value == 0)):
                        stack.append((index + 1, sequence + [value]))

        return sequences

    def generate_sequences_b(self, n: int, bars: list = None) -> list:
        """
        Generates valid sequences for shuffling with barriers.

        Args:
            n (int): The length of the sequence.
            bars (list, optional): List of barrier positions. Defaults to None.

        Returns:
            list: A list of valid binary sequences with barrier constraints.
        """
        sequences = []
        bar = [x - 1 for x in bars] if bars is not None else []
        stack = [(0, [])]

        while stack:
            index, sequence = stack.pop()
            if index == n:
                if sequence and sequence[0] * sequence[-1] != 1:
                    if all(sequence[pos] == 0 for pos in bar):
                        sequences.append(sequence)
            else:
                for value in [1, 0]:
                    if (not sequence or sequence[-1] == 0 or
                            (sequence[-1] == 1 and value == 0)):
                        stack.append((index + 1, sequence + [value]))

        return sequences


def show_result(v: list, partial: bool = False, ind: int = None):
    """
    Displays the results.

    Args:
        v (list): The list of results.
        partial (bool, optional): Shows only a specific result if True.
                                  Defaults to False.
        ind (int, optional): Index of the result to display if partial is True.
                             Defaults to None.
    """
    v.sort()

    if not partial:
        print(len(v), "\n".join(v), sep="\n")
    else:
        print(len(v), v[ind], sep="\n")


def standard_tests():
    """
    Runs a set of standard tests for the Wedding class.
    """
    standard = Wedding()
    show_result(standard.shuffle("abc"))
    show_result(standard.shuffle("WXYZ"))
    show_result(standard.barriers("xyz", [0]))
    show_result(standard.shuffle("abcdefXY"))
    show_result(standard.barriers("abcDEFxyz", [2, 5, 7]))
    show_result(standard.barriers("ABCDef", [4]))
    show_result(standard.barriers("bgywqa", [0, 1, 2, 4, 5]))
    show_result(standard.barriers("n", [0]))
    show_result(standard.shuffle("hi"))


def main():
    """
    Interactive function for running commands.
    """
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
            show_result(w.shuffle(guests))

        elif asktype[0] == "b":
            guests = asktype[1]
            bars = [int(x) for x in asktype[2:]]
            show_result(w.barriers(guests, bars))

        elif asktype[0] == "sp":
            guests, ind = asktype[1], int(asktype[2])
            show_result(w.shuffle(guests), True, ind)

        elif asktype[0] == "bp":
            guests = asktype[1]
            bars = [int(x) for x in asktype[2:-1]]
            ind = int(asktype[-1])
            show_result(w.barriers(guests, bars), True, ind)


if __name__ == "__main__":
    main()
