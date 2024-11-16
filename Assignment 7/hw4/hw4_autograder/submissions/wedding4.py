
import itertools

class Wedding:
    
    def __init__(self):
        pass
    
    def wed(self, guest_num, circular=True):
        if guest_num == 0:
            return []
        if guest_num == 1:
            return [[0]]
        if guest_num == 2:
            return [[0,1],[1,0]]
            
        res = []        

        def sub(current, persons):
            if persons == guest_num:         
                res.append(current) 
                return              
            for offset in (-1, 0, +1):          
                if circular:
                    newpos = (persons + offset) % guest_num
                else:
                    newpos = (persons + offset)
                if newpos < 0 or newpos >= guest_num:
                    continue
                if current[newpos] is None:     
                    newcurrent = current[:]     
                    newcurrent[newpos] = persons   
                    sub(newcurrent, persons + 1)   

        sub([None]*guest_num, 0)
        return res
    
    def shuffle(self,guests):
        part_combos = self.wed(len(guests))
        result = []
        for combo in part_combos:
            res = [guests[i] for i in combo]
            res_str = ''.join(res)
            result.append(res_str)
        return result

    def barriers(self, guests, bars = []):
        combos = []
        for i in range(len(bars)):
            if i == 0:
                part = guests[bars[-1]:] + guests[:bars[i]]
            else:
                part = guests[bars[i-1]:bars[i]] 
                
            part_combos = self.wed(len(part), False)
            part_res = []
            
            for combo in part_combos:
                res = [part[i] for i in combo]
                res_str = ''.join(res)
                part_res.append(res_str)
            combos.append(part_res)
    

        permutations = list(itertools.product(*combos))
        final_strings = [''.join(permutation) for permutation in permutations]
        
        for i, string in enumerate(final_strings):
            res = ""
            j = 0
            while j < len(string):
                if j in bars:
                    res += "|"
                res += string[j]
                j += 1
            final_strings[i] = res
            
        
        return final_strings
    

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

