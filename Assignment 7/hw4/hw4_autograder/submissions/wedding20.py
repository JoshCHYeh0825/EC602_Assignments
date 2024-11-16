
import itertools as it

class Wedding: 
    def __init__(self):
        pass
    
    def panel(self, word):    #panel method (assume boundary at start) ex: abc
        if len(word)>1:
            nminus2 = word[0]   #first letter ex: a
            nminus1 = [word[:2], word[1] + word[0]]    # first 2 letter combination ex. ['ab','ba']
            nm1_calc = []
            nm2_calc = []
        
            for i in range(2,len(word)): # calculate n-1 and n2 from 3rd letter and on
                nm1_calc = [x+word[i] for x in nminus1]   
                nm2_calc = [x+word[i]+word[i-1] for x in nminus2]
                nminus2 = nminus1   # new n-2 is previous n-1
                nminus1 = nm1_calc + nm2_calc     # new n-1 is newly calulated n-1 and n-2
        else:     # if it's one letter or empty word return the word itself
            nminus1=[word]
       
        return(nminus1)   # n-1 contains final list
    
    def shuffle(self, word):  # method has no boundaries
        if len(word)>2:    # example 'abcd'
            comb_stay = self.panel(word[1:])   # assume a doesn't swap, -> a + panel('bcd') 
            comb_shiftrt = self.panel(word[2:]) # assume a swaps with b -> ba + panel('cd')
            comb_shiftlt = self.panel(word[1:len(word)-1])  # assume a swaps with d -> d+panel('bc')+a
            comb_stay_form = [word[0]+i for i in comb_stay]  # adds a to combinations
            comb_shiftrt_form = [word[1]+word[0]+i for i in comb_shiftrt]  # adds ba to the combinations
            comb_shiftlt_form = [word[-1]+i+word[0] for i in comb_shiftlt] # adds da based on location to the combinations
            rotate_rt = [word[-1]+word[:len(word)-1]]   # shift all letters one right
            rotate_lt = [word[1:]+word[0]]    # shift all letters one left
            comb_final = comb_stay_form + comb_shiftrt_form + comb_shiftlt_form + rotate_rt + rotate_lt  # add all combinations together
        else:     # if 2 letter word or less, return word combination using panel method
            comb_final = self.panel(word)
        return comb_final
        
    
    def barriers(self, word, block): # methods has more than boudaries at any location
        new_word = []
        comb = []
        combf_join = []
    
        if len(block)<1:  # if block is not provided then trat it like word with no boundaries
            comb_format = self.shuffle(word)
        else:
            for i in range(len(block)):  # example: 'A|bc|d|EF'
                if i <len(block)-1:  # separate word based on the location of the block -> new_word = ['bc','d']
                    new_word += [word[block[i]:block[i+1]]]
                else:    # when you reach last block, include remaining letter -> new_word = ['EFA']
                    new_word += [word[block[i]:] + word[:block[0]]]
                comb = [self.panel(i) for i in new_word]   # perform panel on all of the new words
                # rem1 = comb
                for i in range(len(comb)-1):   # multiply two word combinations together aand then multiply that with the next word combination
                    comb[i+1] = list(it.product(comb[i],comb[i+1]))   # use itertools product method to multiply each words' combinations with each other and store combination at the same location
                    comb[i+1] = [j[0]+'|'+j[1] for j in comb[i+1]]    # for each combinations join parts together and include '|' to identify the wall; the final multiplied combina
                if 0 in block:     # if there is a boundary at 0th position include '|' at the start 
                    comb_format = ['|'+i[:len(i)-block[0]] for i in comb[-1]]
                else:       # otherwise shift the word back to it's original position based and add '|' at teh first block location -> 'bc|d|EFA' changes to 'A|bc|d|EF'
                    comb_format = [i[-1*block[0]:]+'|'+i[:len(i)-block[0]] for i in comb[-1]]
        return comb_format

    
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