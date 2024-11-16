from itertools import product

class Wedding: 
    # Initialize the Wedding class
    def __init__(self):
      self.results = []

    # Define a function to generate all possible arrangements of a list of guests
    def arrangements(self, guests):
        if len(guests) == 1:
            return guests
        
        elif len(guests) == 2:
            results = []
            results.append(guests)
            results.append(guests[1] + guests[0])
            return results

        else:
            results = []
            for temp in self.arrangements(guests[1:]):    
                results.append(guests[0] + temp)   

            for temp in self.arrangements(guests[2:]):
                results.append(guests[1] + guests[0] + temp)

            return results

    # Define a function to shuffle a list of guests
    def shuffle_procedure(self, guests):
        results = []

        if len(guests) == 2:
            results.append(guests)
            results.append(''.join(reversed(guests)))
            return results

        for temp in self.arrangements(guests[1:]):      
            results.append(guests[0]+temp)

        for temp in self.arrangements(guests[2:]):
            results.append(guests[1]+guests[0]+temp)

        results.append(guests[-1]+guests[0:-1])

        for temp in self.arrangements(''.join(reversed(guests[1:-1]))):       
            results.append(guests[-1] + ''.join(reversed(temp)) + guests[0])
        
        results.append(guests[1:] + guests[0])

        return results
   
    # Define a function to generate all possible arrangements of a list of guests
    def generate(self, results):
        return list(product(*results))
    
    # Define a function to generate all possible arrangements of guests with barriers
    def barriers_procedure(self, guests, bars):
        barriers_result = []
        arrange_list = []           
        temp = 0
        generate_results = []
        gen_rest = []

        for bar in bars:
            if bar==0:
                continue
            arrange_list.append(guests[temp:bar])   
            temp = bar

        if temp!= len(guests) and len(bars) != 0 and bars[0] != 0 :   
            temp_list1 = arrange_list[0]
            temp_list2 = []
            temp_list2.append(guests[temp:])
            temp_list2.append(temp_list1)
            arrange_list[0] = (''.join(temp_list2))  


        elif len(bars) == 1 and bars[0] == 0:
            barriers_result.append(self.arrangements(guests))
        elif len(bars) >1 and bars[0] == 0:
            arrange_list.append(guests[temp:])   

        for lst in arrange_list:
            barriers_result.append(self.arrangements(lst))   

        gen_rest = self.generate(barriers_result)
        for temp_rest in gen_rest:
            if bars[0]==0:                              
                temp_rest = ''.join(temp_rest)
            else:
                temp_rest = ''.join(temp_rest)
                temp_str1 = temp_rest[0:(len(guests) - bars[-1])]      
                temp_str2 = temp_rest[(len(guests) - bars[-1]):]
                temp_rest = temp_str2 + temp_str1

            i=0   
            for bar in bars:
                temp_rest = temp_rest[0:bar+i] + '|' + temp_rest[bar+i:]
                i = i+1

            generate_results.append(temp_rest)
            
        return generate_results

    def shuffle(self, guests):
        result = []
        result = self.shuffle_procedure(guests)
        return result

    def barriers(self, guests, bars):
        result = []
        result = self.barriers_procedure(guests, bars)
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