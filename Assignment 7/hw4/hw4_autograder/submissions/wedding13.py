
class Wedding:
    def __init__(self):
        pass

    def shuffle(self, guests):
        def backstep(first = 0):
            if first == n:
                res.append(nums[:])
                return
            i = first+1
            if first<(n-1):
                if nums[first] == guests[first]:
                    nums[first], nums[i] = nums[i], nums[first]
                    backstep(first + 1)
                    nums[first], nums[i] = nums[i], nums[first]
                    backstep(first + 1)
                else:
                    backstep(first + 1)
            else:
                if(nums[0]==guests[0]) and (nums[first]==guests[n-1]) and first>1:
                    nums[first], nums[0] = nums[0], nums[first]
                    backstep(first + 1)
                    nums[first], nums[0] = nums[0], nums[first]
                    backstep(first + 1)
                else:
                    backstep(first + 1)
        nums = list(guests)
        nums1 = list(guests)
        n = len(nums)
        if n == 0:
            return ['']
        res = []
        backstep()
        if n>2:
            s1 = nums1[1:]
            s1.append(nums1[0])
            res.append(s1)
            s2 = [nums1[-1]]
            s2 += nums1[0:-1]
            res.append(s2)
        ans = []
        for ele in res:
            ans.append(''.join(ele))
        return ans

    def barriers(self, guests, bars):
        def back(n, first=0, temp=''):
            if first == n:
                temp = temp[:-1]
                res.append(temp)
            else:
                strs = ans[first]
                for i in strs:
                    back(n, first=first + 1, temp=temp + i + '|')

        bars.sort()
        n = len(bars)
        str1 = []
        str1.append(guests[0:bars[0]])
        for i in range(1, len(bars)):
            str1.append(guests[bars[i - 1]:bars[i]])
        str1.append(guests[bars[n - 1]:])
        ans = []
        for s in str1:
            ss = self.shuffle_another(guests=s)
            ans.append(ss)
        # print(ans)
        res = []
        n1 = len(ans)
        back(n=n1, first=0, temp='')
        for str in res:
            if str[0]==guests[0] and str[-1]==guests[-1]:
                ss=(guests[-1])
                ss += str[1:-1]
                ss += guests[0]
                res.append(ss)
        return res

    def shuffle_another(self, guests):
        def backstep(first=0):
            if first == n:
                res.append(nums[:])
                return
            i = first+1
            if first<(n-1):
                if nums[first] == guests[first]:
                    nums[first], nums[i] = nums[i], nums[first]
                    backstep(first + 1)
                    nums[first], nums[i] = nums[i], nums[first]
                    backstep(first + 1)
                else:
                    backstep(first + 1)
            else:
                backstep(first + 1)
        nums = list(guests)
        nums1 = list(guests)
        n = len(nums)
        if n == 0:
            return ['']
        res = []
        backstep()
        ans = []
        for ele in res:
            ans.append(''.join(ele))
        return ans


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