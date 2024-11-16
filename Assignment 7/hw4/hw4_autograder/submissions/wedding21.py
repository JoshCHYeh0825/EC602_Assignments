
class Wedding:
    def __init__(self) -> None:
        pass
    
    def shuffle(self, guests):
        a = [[""]] * len(guests)
        n = len(guests)
        if n == 1:
            return [guests]
        for i in range(n - 2, -1, -1):
            b = a.copy()
            for j in range(i, n):
                if i == j:
                    a[j] = [guests[j]]
                elif j - i == 1:
                    a[j] = [guests[j] + guests[i], guests[i] + guests[j]]
                else:
                    a[j] = []
                    for item in a[j - 1]:
                        a[j].append(item + guests[j])
                    if j - i >= 2:
                        for item in a[j - 2]:
                            a[j].append(item + guests[j] + guests[j - 1])
                        if i == 0 and j == n - 1:
                            for item in b[j - 1]:
                                a[j].append(guests[j] + item + guests[i])
        res = a[n - 1]
        if n >= 3:
            res.append(guests[1:] + guests[0])
            res.append(guests[-1] + guests[0:-1])
        return res

    def barriers(self, guests, bars):
        a = [[""]] * len(guests)
        n = len(guests)
        if n == 1:
            if len(bars) != 0:
                return ["|" + guests]
            else:
                return [guests]
        for i in range(n - 2, -1, -1):
            b = a.copy()
            for j in range(i, n):
                cur = ""
                prev = ""
                if j in bars:
                    cur = "|"
                if j - 1 in bars:
                    prev = "|"
                if i == j:
                    a[j] = [cur + guests[j]]
                elif j - i == 1:
                    if cur!="|":
                        a[j] = [prev + guests[j - 1] + cur + guests[j], prev + guests[j] + cur + guests[j - 1]]
                    else:
                        a[j]=[prev + guests[j - 1] + cur + guests[j]]
                else:
                    a[j] = []
                    for item in a[j - 1]:
                        a[j].append(item + cur + guests[j])
                    if j - i >= 2:
                        if j not in bars:
                            for item in a[j - 2]:
                                a[j].append(item + prev + guests[j] + cur + guests[j - 1])
                        if i == 0 and j == n - 1:
                            if  0 not in bars:
                                for item in b[j - 1]:
                                    a[j].append(guests[j] + item + cur+guests[i])
        res = a[n - 1]
        if len(bars) == 0:
            res.append(guests[1:] + guests[0])
            res.append(guests[-1] + guests[0:-1])
        return res
    


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