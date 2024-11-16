
import itertools
class Wedding:

    def __init__(self):
        self.memo = {}

    def is_valid_swap(self, original, perm):
        n = len(original)
       
        if all(original[(idx + 1) % n] == perm[idx] for idx in range(n)) or \
        all(original[idx] == perm[(idx + 1) % n] for idx in range(n)):
            return True

        for idx, guest in enumerate(perm):
            original_idx = original.index(guest)
            
            if abs(original_idx - idx) > 1:
                # Allow for end-to-end swap
                if not ((original_idx == 0 and idx == n - 1) or
                        (original_idx == n - 1 and idx == 0)):
                    return False
        return True



    def shuffle(self, guests):
        original = guests
        return sorted(set(self.generate_swaps(list(guests), original, 0)))

    def generate_swaps(self, current, original, start):
        memo_key = ''.join(current)
        if memo_key in self.memo:
            return self.memo[memo_key]

        valid_swaps = [memo_key]

        for i in range(start, len(original)):
            for j in range(i + 1, len(original)):
               
                new_current = current[:]
                new_current[i], new_current[j] = new_current[j], new_current[i]
                
                if self.is_valid_swap(original, new_current):
                  
                    further_swaps = self.generate_swaps(new_current, original, i + 1)
                    
                  
                    for swap in further_swaps:
                        if swap not in valid_swaps:
                            valid_swaps.append(swap)

        left_shift = original[1:] + original[:1]
        right_shift = original[-1:] + original[:-1]
        if ''.join(left_shift) not in valid_swaps:
            valid_swaps.append(''.join(left_shift))
        if ''.join(right_shift) not in valid_swaps:
            valid_swaps.append(''.join(right_shift))
       
        self.memo[memo_key] = valid_swaps
        return valid_swaps
    

    def valid_perm(self, segment, perm):
        
        for i, guest in enumerate(perm):
            original_idx = segment.index(guest)
            
            if abs(original_idx - i) > 1:
                return False
        return True

    def linear_shuffle(self, segment):
       
        all_perms = itertools.permutations(segment)
        # Filter out permutations where a guest moves more than one position
        valid_perms = [''.join(perm) for perm in all_perms if self.valid_perm(segment, perm)]
        return valid_perms

    def barriers(self, guests, n_bars, barrier_locations):
      
        segments = []
        last_index = 0
        for index in barrier_locations:
            segments.append(guests[last_index:index])
            last_index = index
        segments.append(guests[last_index:])

       
        all_combinations = set()
        for combination in itertools.product(*[self.shuffle(segment) for segment in segments]):
            all_combinations.add('|'.join(combination))

      
        all_combinations = self.add_end_swaps(all_combinations, segments)

        return sorted(all_combinations)
    
    def add_end_swaps(self, combinations, segments):
       
        end_swaps_set = set()
        first_segment, last_segment = segments[0], segments[-1]
        
        if first_segment and last_segment:
            # Check if the end swap is valid
            if self.is_valid_end_swap(first_segment, last_segment):
                # Perform the swap
                swapped_first, swapped_last = self.swap_ends(first_segment, last_segment)

                for combo in combinations:
                    parts = combo.split('|')
                    new_combo = '|'.join([swapped_first] + parts[1:-1] + [swapped_last])
                    end_swaps_set.add(new_combo)

        return combinations.union(end_swaps_set)

    def is_valid_end_swap(self, first_segment, last_segment):
        return len(first_segment) > 1 and len(last_segment) > 1
    
    def swap_ends(self, first_segment, last_segment):
      first_list = list(first_segment)
      last_list = list(last_segment)

      first_list[0], last_list[-1] = last_list[-1], first_list[0]

      return ''.join(first_list), ''.join(last_list)

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
    asktype=input().split()
    if not asktype or asktype[0] == "quit":
      break
    elif asktype[0] == "tests":
      standard_tests()
    elif asktype[0] == "s":
      guests = asktype[1]
      r = w.shuffle(guests)
      show_result(r)
    elif asktype[0] == "b":
      guests,nbar,bars = asktype[1],asktype[2],asktype[3:]
      nbar = int(nbar)
      r = w.barriers(guests, nbar, [int(x) for x in bars])
      show_result(r)
    elif asktype[0] == "sp":
      guests,ind = asktype[1:]
      r = w.shuffle(guests)
      show_result(r, True, int(ind))
    elif asktype[0] == "bp":
      guests,nbar,bars,ind  = asktype[1],asktype[2],asktype[3:-1],asktype[-1]
      nbar = int(nbar)
      r = w.barriers(guests, nbar, [int(x) for x in bars])
      show_result(r, True, int(ind))
    

if __name__ == '__main__':
  main()