
class Wedding:
    def __init(self):
        pass

    def shuffle(self, guests):
        if len(guests) == 2:
            # Special case for only two guests
            arrangements = [guests, guests[::-1]]
        else:
            arrangement = [None] * len(guests)
            available_positions = self.create_available_positions_dict(len(guests))
            arrangements = self.generate_arrangements(guests, arrangement, available_positions, 0)
    
        return arrangements

    def create_available_positions_dict(self, num_guests):
        available_positions = {}
        for i in range(num_guests):
            available_positions[i] = [i, (i + 1) % num_guests, (i - 1) % num_guests]
        return available_positions

    def generate_arrangements(self, guests, arrangement, available_positions, index):

        if index == len(guests):
            return [''.join(arrangement)]  

        possible_arrangements = []

        guest = guests[index]
        positions = available_positions[index]

        for position in positions:
            if arrangement[position] is None:
                arrangement[position] = guest
                possible_arrangements.extend(self.generate_arrangements(guests, arrangement, available_positions, index + 1))
                arrangement[position] = None  

        return possible_arrangements

    def barriers(self, guests, barrier_positions):
        if len(guests) == 0:
            arrangement = []
        elif len(guests) == 1:
            for barrier in barrier_positions: 
                if barrier == 0:
                    inserted_text = "|"
                    arrangements = [ inserted_text + guests]
                if barrier == 1:
                    inserted_text = "|"
                    arrangements = [guests+ inserted_text]
        else:
          arrangement = [None] * len(guests)
          available_positions = self.create_available_positions_dict_barr(len(guests), barrier_positions)
          ##print(available_positions)
          arrangements = self.generate_arrangements(guests, arrangement, available_positions, 0)
          sorted_barriers = sorted(barrier_positions)
          j = 0
          for barrier in sorted_barriers:
              for i in range(len(arrangements)):
                  adjusted = barrier + j
                  inserted_text = "|"
                  arrangement = arrangements[i]
                  arrangement = arrangement[:adjusted] + inserted_text + arrangement[adjusted:]
                  arrangements[i] = arrangement
              j = j + 1  
        return arrangements

    def create_available_positions_dict_barr(self, num_guests, barrier_positions):
        available_positions = {}
        for i in range(num_guests):
            available_positions[i] = [i, (i + 1) % num_guests, (i - 1) % num_guests]
        #print(available_positions)
        
        for key in barrier_positions:
            for dic_key, positions in available_positions.items():
                ##print(key)
                ##print(available_positions)
                if key == 0 and dic_key == 0:
                    if num_guests - 1 in positions:
                        positions.remove(num_guests - 1)
                elif key == 0  and dic_key == num_guests - 1:
                    if 0 in positions:
                        positions.remove(0)
                elif key == num_guests and dic_key == 0:
                    if num_guests - 1 in positions:
                        positions.remove(num_guests - 1)
                elif key == num_guests and dic_key == num_guests - 1:
                    if 0 in positions:
                        positions.remove(0)
                elif dic_key == key:
                    if key-1 in positions:
                        positions.remove(key-1)
                elif dic_key == key - 1:
                    if key in positions:
                        positions.remove(key)
        return available_positions



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
      r = w.barriers(guests, [int(x) for x in bars])
      show_result(r)
    elif asktype[0] == "sp":
      guests,ind = asktype[1:]
      r = w.shuffle(guests)
      show_result(r, True, int(ind))
    elif asktype[0] == "bp":
      guests,nbar,bars,ind  = asktype[1],asktype[2],asktype[3:-1],asktype[-1]
      r = w.barriers(guests, [int(x) for x in bars])
      show_result(r, True, int(ind))
    

if __name__ == '__main__':
  main()