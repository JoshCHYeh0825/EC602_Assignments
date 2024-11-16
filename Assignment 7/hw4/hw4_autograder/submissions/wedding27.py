"""hw4

Returns:
    Shuffle and barrier
"""
class Wedding:
    """_summary_
    """
    def __init__(self):
        self.results = set()  # To store unique seating configurations

    def shuffle(self, guests):
        """_summary_

        Args:
            guests (list): list of guests

        Returns:
            list: list of possible positions
        """
        self.results.clear()  # Clear the results set before starting
        self._dfs(
            list(
                range(
                    len(guests))),
            [None] *
            len(guests),
            0, #bitmask
            circular=False,
            barrier_pos=None)
        return ["".join(guests[i] for i in config) for config in self.results]

    def seg_shuffle(self, segment):
        """_summary_

        Args:
            segment (list): list of guests in segment

        Returns:
            list: list of possible positions
        """
        self.results.clear()
        self._dfs(
            list(range(len(segment))),
            [None] * len(segment),
            0, #bitmask
            circular=False,
            barrier_pos=0,
            is_circular_segment=False
        )
        return ["".join(segment[i] for i in config) for config in self.results]


    def circular_shuffle(self, segment, barrier_pos):
        """_summary_

        Args:
            segment (list): list of guests in segment
            barrier_pos (int): barrier position

        Returns:
            list: list of possible positions
        """
        self.results.clear()
        self._dfs(
            list(
                range(
                    len(segment))),
            [None] *
            len(segment),
            0, #bitmask
            circular=True,
            barrier_pos=barrier_pos)
        return ["".join(segment[i] for i in config) for config in self.results]

    def combine_circular(self, head_segment_configs, middle_segments_configs, tail_segment, bars):
        """_summary_

        Args:
            head_segment_configs (_type_): _description_
            middle_segments_configs (_type_): _description_
            tail_segment (_type_): _description_
            bars (_type_): _description_

        Returns:
            _type_: _description_
        """
        # This function combines the configurations with correct circular handling
        def recursive_combine(middle_configs, current_config, head_config, tail_config):
            if not middle_configs:
                # Combine the current configuration with the head and tail segments
                combined_config = head_config + current_config + "|" + tail_config  # Add the last barrier
                for bar in reversed(bars[:-1]):  # Skip the last barrier
                    combined_config = combined_config[:bar] + "|" + combined_config[bar:]
                combined_results.add(combined_config)
                return

            for config in middle_configs[0]:
                # Continue combining the configurations
                recursive_combine(middle_configs[1:], current_config + config, head_config, tail_config)

        # Generate all combinations of head and tail configurations
        combined_results = set()
        for head_config, tail_config in head_segment_configs:
            # Combine middle segments configurations with each valid head-tail pair
            recursive_combine(middle_segments_configs, "", head_config, tail_config)

        return list(combined_results)

    def barriers(self, guests, bars):
        """_summary_

        Args:
            guests (_type_): _description_
            bars (_type_): _description_

        Returns:
            _type_: _description_
        """
        # Separate the guests into head, middle, and tail segments
        head_segment = guests[:bars[0]]
        tail_segment = guests[bars[-1]:]
        middle_segments = [guests[bars[i]:bars[i + 1]] for i in range(len(bars) - 1)]

        # Compute configurations for the circular head and tail segments
        circular_configs = self.circular_shuffle(head_segment + tail_segment, len(head_segment))
        circular_segment_configurations = [(config[:len(head_segment)], config[len(head_segment):]) for config in circular_configs]

        # Compute configurations for each non-circular middle segment
        middle_segments_configs = [self.seg_shuffle(segment) for segment in middle_segments]

        # Combine configurations with proper circular segment handling
        combined_configurations = self.combine_circular(circular_segment_configurations, middle_segments_configs, tail_segment, bars)
        return combined_configurations


    def _dfs(self, remaining_guests, current_seating, occupied_seats, circular, barrier_pos, is_circular_segment=True):
        # Base case: All guests are seated
        if not remaining_guests:
            self.results.add(tuple(current_seating))
            return

        guest_index = remaining_guests[0]
        original_position = guest_index  # The original position of the guest in the segment
        n = bin(occupied_seats).count('1')  # Count the number of occupied seats

        # Helper functions are the same as before, so we won't redefine them here

        # Try seating the guest in the current seat
        if not occupied_seats & (1 << n) and self.within_one_step(n, original_position) or self.allow_circular_swap(n, is_circular_segment, guest_index, len(current_seating)):
            current_seating[n] = guest_index
            self._dfs(remaining_guests[1:], current_seating, occupied_seats | (1 << n), circular, barrier_pos, is_circular_segment)
            current_seating[n] = None  # Backtrack

        # Try seating the guest to the left
        left_seat = (n - 1) % len(current_seating)
        if not occupied_seats & (1 << left_seat) and (self.within_one_step(left_seat, original_position) or self.allow_circular_swap(left_seat, is_circular_segment, guest_index, len(current_seating))) and (
                not circular or guest_index != barrier_pos or left_seat != (barrier_pos - 1) % len(current_seating)):
            current_seating[left_seat] = guest_index
            self._dfs(remaining_guests[1:], current_seating, occupied_seats | (1 << left_seat), circular, barrier_pos, is_circular_segment)
            current_seating[left_seat] = None  # Backtrack

        # Try seating the guest to the right
        right_seat = (n + 1) % len(current_seating)
        if not occupied_seats & (1 << right_seat) and (self.within_one_step(right_seat, original_position) or self.allow_circular_swap(right_seat, is_circular_segment, guest_index, len(current_seating))) and (
                not circular or guest_index != (barrier_pos - 1) % len(current_seating) or right_seat != barrier_pos):
            current_seating[right_seat] = guest_index
            self._dfs(remaining_guests[1:], current_seating, occupied_seats | (1 << right_seat), circular, barrier_pos, is_circular_segment)
            current_seating[right_seat] = None  # Backtrack

    # Extracted the helper functions to avoid redefining them inside _dfs
    @staticmethod
    def within_one_step(position, original_position):
        """_summary_

        Args:
            position (_type_): _description_
            original_position (_type_): _description_

        Returns:
            _type_: _description_
        """
        return abs(original_position - position) <= 1

    @staticmethod
    def allow_circular_swap(position, is_circular_segment, guest_index, seating_length):
        """_summary_

        Args:
            position (_type_): _description_
            is_circular_segment (bool): _description_
            guest_index (_type_): _description_
            seating_length (_type_): _description_

        Returns:
            _type_: _description_
        """
        return is_circular_segment and ((position == 0 and guest_index == seating_length - 1) or \
                (position == seating_length - 1 and guest_index == 0))



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