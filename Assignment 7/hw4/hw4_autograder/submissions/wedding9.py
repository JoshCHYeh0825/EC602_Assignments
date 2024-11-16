def countem(c):
    a=[0]* len(c)
    while True:
        yield a
        j=0
        a[j] += 1
        while a[j]==c[j]:
            a[j]=0
            j += 1
            if j == len(c):
              return
            a[j]+=1


class Wedding: 
    def __init__(self):
      self.panels =  [ ( tuple(), ), ( (0,), ) ]
      self.circles = [ ( tuple(), ), ( (0,), ), ((0,1), (1,0)) ]

    def linear(self,n,guests=None):
      i = len(self.panels)
      while i <= n:
          stay = tuple( ans + (i-1,)     for ans in self.panels[i-1] )
          swap = tuple( ans + (i-1,i-2)  for ans in self.panels[i-2] )
          self.panels.append(stay + swap)
          i += 1

      if guests:
        N=len(guests)
        res = []
        for t in self.panels[n]:
          res.append("".join(guests[t[i]] for i in range(N)))
        return res

    def shuffle(self, guests):
      N = len(guests)
      self.linear(N-1)

      i = len(self.circles)
      while i <= N:
        #stay at end
        stay = tuple( ans + (i-1,) for ans in self.panels[i-1])
        #swap with end
        swapZ = tuple( ans + (i-1,i-2) for ans in self.panels[i-2])
        #swap with start
        swapA = tuple( (i-1,) + tuple(x+1 for x in ans) + (0,) 
                              for ans in self.panels[i-2])
        # 0123 -> 3012
        rotL = ( (i-1,) + tuple(x for x in range(i-1)) ),
        # 0123 -> 1230
        rotR = ( tuple(x for x in range(1,i)) + (0,) ),

        self.circles.append( stay + swapA + swapZ + rotL + rotR)

        i += 1


      return ["".join(guests[t[i]] for i in range(N))  \
                 for t in self.circles[N] ]

    def barriers(self, guests, bars):
      if not bars:
        return self.shuffle(guests)

      N=len(guests)
      bars.sort()
      B=len(bars)

      OFF = bars[0]
      doubleguests = guests + guests
      bars.append(OFF+N)
      res = []
      count = 1
      counter = []
      for i in range(B):
        g = doubleguests[bars[i]:bars[i+1]]
        
        res.append(self.linear(len(g),g))
        Gcount= len(res[-1])

        counter.append(Gcount)
        count *= Gcount
      
      ans = []
      for x in countem(counter):
        v = "|".join(res[i][x[i]] for i in range(B))
        if OFF:
          ans.append(v[-OFF:]+"|"+v[:-OFF])
        else:
          ans.append("|"+v)
      return ans



def  show_result(v, partial=False,ind=None):
  v.sort()
  if not partial:
    print("",len(v),"\n".join(v),sep="\n")
  else:
    print("",len(v),v[ind],sep="\n")




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
    if asktype[0] == "quit":
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
