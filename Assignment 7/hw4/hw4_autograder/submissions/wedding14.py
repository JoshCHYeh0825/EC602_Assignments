from itertools import product

class Wedding: 
    def __init__(self):
      self.results = []

    def panel(self, guests):
        if len(guests) == 1:
            return guests
        if len(guests) == 2:
            results = []
            results.append(guests)
            #results.append(''.join())

            new_list = guests[1] + guests[0]

            #new_list = from itertools import product
            # new_list = ''.join(reversed(guests))
            results.append(new_list)

            return results

        else:
            results = []

            #1 guests[0] stay
            for res in self.panel(guests[1:]):    #there is also to kinds of posibility, so use for to recieve the result
                results.append(guests[0] + res)   #make the list to the string

            #2 guests[0:1] right
            for res in self.panel(guests[2:]):
                results.append(guests[1] + guests[0] + res)

            return results


    def shuffle_process(self, guests):
        results = []

        if len(guests) == 2:
            results.append(guests)
            results.append(''.join(reversed(guests)))
            return results

        #1. guests[0] stay
        for res in self.panel(guests[1:]):      #result
            results.append(guests[0]+res)

        #2. guests[0] right
        #2.1 right_one
        for res in self.panel(guests[2:]):
            results.append(guests[1]+guests[0]+res)
        #2.2 right right
        results.append(guests[-1]+guests[0:-1])

        #3. guest[0] left
        #3.1 left_one
        for res in self.panel(''.join(reversed(guests[1:-1]))):       #
            results.append(guests[-1] + ''.join(reversed(res)) + guests[0])
        #3.2 left left
        results.append(guests[1:] + guests[0])

        return results
    def iteration(self, results):
        return list(product(*results))

    def barriers_process(self, guests, bars):
        panel_list = []           #
        barriers_result = []
        temp = 0
        ite_results = []
        iteration_rst = []

        #对barrier 切片
        for bar in bars:
            if bar==0:
                continue
            panel_list.append(guests[temp:bar])   #
            temp = bar

        if temp!= len(guests) and len(bars) != 0 and bars[0] != 0 :   #to avoid bar=0 get into this loop
            temp_list1 = panel_list[0]
            temp_list2 = []
            temp_list2.append(guests[temp:])
            temp_list2.append(temp_list1)

            panel_list[0] = (''.join(temp_list2))  # panel_list.append(guests)
            #to make the head of the list connect with the tail
            #panel_list.append(guests[temp:])    #panel_list.append(guests)

        elif len(bars) == 1 and bars[0] == 0:
            barriers_result.append(self.panel(guests))
        elif len(bars) >1 and bars[0] == 0:
            panel_list.append(guests[temp:])    #
        #elif bars[0] == 0 and len(bars) > 1 :      #when there is many barrier and the bars[0]=0, so we miss the last one


        #recursion
        for lst in panel_list:
            barriers_result.append(self.panel(lst))   #

        iteration_rst = self.iteration(barriers_result)
        i=0
        for ite_rst in iteration_rst:
            if bars[0]==0:                              #
                ite_str = ''.join(ite_rst)
            else:
                ite_str = ''.join(ite_rst)
                temp_str1 = ite_str[0:(len(guests) - bars[-1])]      #
                temp_str2 = ite_str[(len(guests) - bars[-1]):]
                ite_str = temp_str2 + temp_str1

            j=0   #when i add a '|' i+=1
            for bar in bars:
                ite_str = ite_str[0:bar+j] + '|' + ite_str[bar+j:]
                j+=1

            ite_results.append(ite_str)
            i+=1

        #print(i)
        #return panel_list
        return ite_results

    def shuffle(self, guests):
        result = []
        result = self.shuffle_process(guests)
        #result = "\n".join(shuffle_rst)
        return result

    def barriers(self, guests, bars):
        result = []
        result = self.barriers_process(guests, bars)
        #result = "\n".split(barrier_rst)
        return result


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