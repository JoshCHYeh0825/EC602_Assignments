class Wedding:
    def __init__(self):
        pass
    def shuffle(self, guests):
        def backtrack(num=0):
            if num == n:
                res.append(nums[:])
                return
            i = num + 1
            if num < (n - 1):
                if nums[num] == guests[num]:
                    nums[num], nums[i] = nums[i], nums[num]
                    backtrack(num + 1)
                    nums[num], nums[i] = nums[i], nums[num]
                    backtrack(num + 1)
                else:
                    backtrack(num + 1)
            else:
                if (nums[0] == guests[0]) and (nums[num] == guests[n - 1]) and num > 1:
                    nums[num], nums[0] = nums[0], nums[num]
                    backtrack(num + 1)
                    nums[num], nums[0] = nums[0], nums[num]
                    backtrack(num + 1)
                else:
                    backtrack(num + 1)
        nums = []
        nums1 = []
        for j in guests:
            nums.append(j)
            nums1.append(j)
        n = len(nums)
        if n == 0:
            return ['']
        res = []
        backtrack()
        if n > 2:
            s1 = nums1[1:]
            s1.append(nums1[0])
            res.append(s1)
            s2 = [nums1[-1]]
            s2 += nums1[0:-1]
            res.append(s2)
        ans = []
        len1 = len(res)
        for i in range(len1):
            s1 = res[i]
            ans.append(''.join(s1))
        return ans

    def barriers(self, guests, bars):
        def change(guests):
            def backtrack(num=0):
                if num == n:
                    res.append(nums[:])
                    return
                i = num + 1
                if num < (n - 1):
                    if nums[num] == guests[num]:
                        nums[num], nums[i] = nums[i], nums[num]
                        backtrack(num + 1)
                        nums[num], nums[i] = nums[i], nums[num]
                        backtrack(num + 1)
                    else:
                        backtrack(num + 1)
                else:
                    backtrack(num + 1)

            nums = list(guests)
            n = len(nums)
            if n == 0:
                return ['']
            res = []
            backtrack()
            ans = [''.join(s) for s in res]
            return ans

        def back(n, num=0, temp=''):
            if num == n:
                temp = temp[:-1]
                res.append(temp)
            else:
                strs = ans[num]
                for i in strs:
                    back(n, num=num + 1, temp=temp + i + '|')

        bars.sort()
        n = len(bars)
        str1 = [guests[0:bars[0]]]
        for i in range(1, len(bars)):
            str1.append(guests[bars[i - 1]:bars[i]])
        str1.append(guests[bars[n - 1]:])
        ans = [change(guests=s) for s in str1]
        res = []
        n1 = len(ans)
        back(n=n1, num=0, temp='')
        for str in res:
            if str[0] == guests[0] and str[-1] == guests[-1]:
                ss = guests[-1] + str[1:-1] + guests[0]
                res.append(ss)
        return res


def show_result(v, partial=False, ind=None):
    v.sort()
    if not partial:
        print(len(v), "\n".join(v), sep="\n")
    else:
        print(len(v), v[ind], sep="\n")


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
        asktype = input().split()
        if not asktype or asktype[0] == "quit":
            break
        elif asktype[0] == "tests":
            standard_tests()
        elif asktype[0] == "s":
            guests = asktype[1]
            r = w.shuffle(guests)
            show_result(r)
        elif asktype[0] == "b":
            guests, nbar, bars = asktype[1], asktype[2], asktype[3:]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r)
        elif asktype[0] == "sp":
            guests, ind = asktype[1:]
            r = w.shuffle(guests)
            show_result(r, True, int(ind))
        elif asktype[0] == "bp":
            guests, nbar, bars, ind = asktype[1], asktype[2], asktype[3:-1], asktype[-1]
            r = w.barriers(guests, [int(x) for x in bars])
            show_result(r, True, int(ind))


if __name__ == '__main__':
    main()