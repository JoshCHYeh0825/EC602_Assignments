import itertools
def panel(guests):
    match len(guests):
        case 0 | 1:
            return [guests]
        case 2:
            return [guests, guests[1]+guests[0]]
        case _:
            results = []
            # guests[0] S
            for s in panel(guests[1:]):
                results.append(guests[0]+s)
            # guests[0] R
            for s in panel(guests[2:]):
                results.append(guests[1]+guests[0]+s)
            return results



class Wedding: 
    def __init__(self):
      pass
    def shuffle(self, guests):
        match len(guests):
            case 0 | 1 :
                return [guests]
            case 2 :
                return [guests,guests[1]+guests[0]]
            case _ : #_ means rest 
                results=[]
            # guests[0] still 
                for s in panel(guests[1:]):
                    results.append(guests[0]+s)
            # guests[0] left
            # a. guests[-1] swap
                for s in panel(guests[1:-1]): #-1 represents last
                    results.append(guests[-1]+s+guests[0])
            # b. guests[-1] left
                results.append(guests[1:]+guests[0])
            # guests[0] right
            # a. guests[1] swap
                for s in panel(guests[2:]):
                    results.append(guests[1]+guests[0]+s)
            # b. guests[1] right
                results.append(guests[-1]+guests[:-1])
                return results

    def barriers(self, guests, bars):
        match len(bars):
            case 0 :
                return self.shuffle(guests)
            case _:
                segments = []
                for seg in itertools.pairwise(bars+[bars[0]]):
                #print("start-end", seg[0], seg[1])
                    if seg[0]<seg[1]:
                        people_on_table= guests[seg[0]:seg[1]]
                    else :
                        people_on_table= guests[bars[-1]:]+guests[:bars[0]]
                    people_order = panel(people_on_table)
                    segments.append(people_order) #小桌子可能的情況>segment
                results = []
                for s in itertools.product(*segments): 
                    t = "|".join(s)
                    n = len(t)
                    t = t[n-bars[0]:]+"|"+t[:n-bars[0]]
                    results.append(t)
                return results



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