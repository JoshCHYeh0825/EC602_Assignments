
class Wedding: 
    def __init__(self):
        pass
    def shuffle(self, guests):
        
        if len(guests) == 1:
            return [guests]
        if len(guests) == 2:
            return [guests, guests[::-1]]
        self.guests = guests
        self.results = []
        self.__dfs_shuffle(0, [None for _ in range(len(self.guests))])
        return self.results
    
    
    
    def __dfs_shuffle(self, index, positions):
        if index == len(positions):
            self.results.append(''.join(positions))
            return 
        length = len(self.guests)
        for offset in range(-1, 2):   
            new_index = (index + offset) % length
            if positions[new_index] is None:
                positions[new_index] = self.guests[index]
                self.__dfs_shuffle(index + 1, positions)
                positions[new_index] = None

    def barriers(self, guests, bars):
        self.guests = guests
        self.bars = bars
        self.results = []
        self.__dfs_barriers(0, [None for _ in range(len(self.guests))])
        
        return self.results

    def __dfs_barriers(self, index, positions):
        if index == len(positions):
            s = ""
            for idx, p in enumerate(positions):
                if idx in self.bars:
                    s += "|"
                s += p
            self.results.append(s)
            return 
        length = len(self.guests)
        for offset, barrier_offset in zip(range(-1, 2), [0, None, 1]):   
            new_index = (index + offset) % length
            if (barrier_offset is None or (index + barrier_offset) % length not in self.bars) and \
                positions[new_index] is None:
                positions[new_index] = self.guests[index]
                self.__dfs_barriers(index + 1, positions)
                positions[new_index] = None

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