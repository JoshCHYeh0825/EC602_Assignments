from itertools import product

class Wedding:
    def __init__(self):
        pass

    def panel(self, guests):
        n = len(guests)
        if n == 1:
            return [guests]
        elif n == 2:
            return [guests, guests[1] + guests[0]]
        else:
            return [guests[0] + res for res in self.panel(guests[1:])] + [guests[1] + guests[0] + res for res in self.panel(guests[2:])]

    def shuffle_process(self, guests):
        results = []

        if len(guests) == 2:
            results.append(guests)
            results.append(''.join(reversed(guests)))
            return results

        for res in self.panel(guests[1:]):      
            results.append(guests[0]+res)

        for res in self.panel(guests[2:]):
            results.append(guests[1]+guests[0]+res)
     
        results.append(guests[-1]+guests[0:-1])

        for res in self.panel(''.join(reversed(guests[1:-1]))):       #
            results.append(guests[-1] + ''.join(reversed(res)) + guests[0])
    
        results.append(guests[1:] + guests[0])

        return results

    def iteration(self, results):
        return list(product(*results))

    def barriers_process(self, guests, bars):
        panel_list = []           
        barriers_result = []
        temp = 0
        ite_results = []
        iteration_rst = []

        for bar in bars:
            if bar==0:
                continue
            panel_list.append(guests[temp:bar])   
            temp = bar

        if temp!= len(guests) and len(bars) != 0 and bars[0] != 0 :   
            temp_list1 = panel_list[0]
            temp_list2 = []
            temp_list2.append(guests[temp:])
            temp_list2.append(temp_list1)

            panel_list[0] = (''.join(temp_list2))  

        elif len(bars) == 1 and bars[0] == 0:
            barriers_result.append(self.panel(guests))
        elif len(bars) >1 and bars[0] == 0:
            panel_list.append(guests[temp:])   

        for lst in panel_list:
            barriers_result.append(self.panel(lst))   

        iteration_rst = self.iteration(barriers_result)
        i=0
        for ite_rst in iteration_rst:
            if bars[0]==0:                              
                ite_str = ''.join(ite_rst)
            else:
                ite_str = ''.join(ite_rst)
                temp_str1 = ite_str[0:(len(guests) - bars[-1])]      
                temp_str2 = ite_str[(len(guests) - bars[-1]):]
                ite_str = temp_str2 + temp_str1

            j=0  
            for bar in bars:
                ite_str = ite_str[0:bar+j] + '|' + ite_str[bar+j:]
                j+=1

            ite_results.append(ite_str)
            i+=1

        return ite_results

    def shuffle(self, guests):
        return self.shuffle_process(guests)

    def barriers(self, guests, bars):
        return self.barriers_process(guests, bars)



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