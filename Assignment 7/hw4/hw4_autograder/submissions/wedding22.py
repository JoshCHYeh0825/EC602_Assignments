
class Wedding:
    def __int__(self):
        pass

    def panel(self, guest):
        arr = [[]] * 2
        
        if len(guest) == 0:
            return guest
        if len(guest) == 1:
            return [[guest[0]]]
        if len(guest) == 2:
            return [[guest[0], guest[1]], [guest[1], guest[0]]]
        
        arr[0] = [[guest[0]]]
        arr[1] = [[guest[0], guest[1]], [guest[1], guest[0]]]

        for j in range (2, len(guest)):

            list = []
            for i in arr[1]:
                temp = i.copy()
                temp = temp + [guest[j]]
                list.append(temp)
            for i in arr[0]:
                temp = i.copy()
                temp = temp + [guest[j]] + [guest[j-1]]
                list.append(temp)
            arr.append(list)
            arr.pop(0)
        return arr[-1]
    
    def shuffle(self, guests):
        guest = list(guests)
        all_left = guest[1:] + [guest[0]]   
        all_right = [guest[-1]] + guest[:-1]
        regular = self.panel(guest)  #head and tail do not switch
        short = guest[1:-1]
        middle = self.panel(short)
        for i in range (0, len(middle)):
            middle[i] = [guest[-1]] + middle[i] + [guest[0]]
        if len(guest)>2:
            result = [all_left] + [all_right] + regular + middle
        else:
            result = regular
        for i in range (0, len(result)):
            result[i] =''.join(result[i])
        return  result
        

    def barriers(self, guests, bars):
        arr = []
        result = []
        if bars == [0]:
            result = [["|"] + i for i in self.panel(guests)]
            for i in range (0, len(result)):
                result[i] =''.join(result[i])
            return result
        if bars == [len(guests)]:
            result =  [i + ["|"] for i in self.panel(guests)]
        if len(bars) == 0:
            return self.shuffle(guests)
        else:
            if 0 in bars or len(guests) in bars:
                result = self.two(guests, bars)
            else:
                arr = self.two(guests, bars)
                arr2 = self.two(guests[1:-1], [i-1 for i in bars])
                for i in range(len(arr2)):
                    arr2[i] = [guests[-1]] + arr2[i] + [guests[0]]
                result = arr2 + arr
        for i in range (0, len(result)):
            result[i] =''.join(result[i])
        return result

    def two(self, guests, bars):
        arr = []
        result = []
        x = 0
        if 0 in bars:
            x = 1
            bars.remove(0)
        if len(guests) in bars:
            x = 2
            bars.remove(len(guests))
        arr.append(guests[0:bars[0]])
        for i in range(0, len(bars) - 1):
            arr.append(guests[bars[i]: bars[i + 1]])
        arr.append(guests[bars[-1]:])
        for j in range(len(arr)):
            result.append(self.panel(arr[j]))
        while len(result) > 1:
            arr1 = []
            for i in result[0]:
                for j in result[1]:
                    a = i + ["|"] + j
                    arr1.append(a)
            result.pop(0)
            result[0] = arr1
        
        if x:
            for i in range (len(result[0])):
                result[0][i] = ["|"] + result[0][i]
        if x == 2:
            result[0] = [i + ['|'] for i in result[0]]
        return result[0]



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