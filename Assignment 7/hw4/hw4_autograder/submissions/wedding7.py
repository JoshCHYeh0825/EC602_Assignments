
import itertools

class Wedding: 
    def __init__(self, guests = [], bars = []):
        self.guests = guests
        self.bars = bars
        self.allpanelanswers = []
    
    def shuffle(self, guests):
        amountguests = len(guests)
        listguests = list(guests)
        allnumguest = []
        if len(self.allpanelanswers)>amountguests:
            allnumguest = self.allpanelanswers[amountguests]
        else:
            allnumguest = Wedding().panel(amountguests)
        #allnumguest = Wedding().panel(amountguests)
        allletterguest = []
        for numanswer in allnumguest:
            letteranswer = ""
            for numseat in numanswer:
                letterseat = guests[numseat]
                letteranswer += letterseat
            allletterguest.append(letteranswer)
        for answer in allletterguest:
            if (answer[0] == guests[0]) and (answer[amountguests - 1] == guests[amountguests - 1]):
                newanswer = answer[:]
                listnewanswer = list(newanswer)
                listnewanswer[0] = listguests[amountguests - 1]
                listnewanswer[amountguests - 1] = listguests[0]
                newanswer= ''.join(listnewanswer)
                allletterguest.append(newanswer)               
        listguests = list(guests)
        rotatecw = guests[:]
        listrotatecw = list(rotatecw)
        for index, letter in enumerate(listrotatecw):
            if index == 0:
                listrotatecw[0] = listguests[amountguests - 1]
            else:
                listrotatecw[index] = listguests[index - 1]
        rotatecw= ''.join(listrotatecw)
        allletterguest.append(rotatecw)
        
        rotateccw = guests[:]
        listrotateccw = list(rotateccw)
        for index, letter in enumerate(listrotateccw):
            if index == (amountguests - 1):
                listrotateccw[amountguests - 1] = listguests[0]
            else:
                listrotateccw[index] = listguests[index + 1]
        rotateccw= ''.join(listrotateccw)
        allletterguest.append(rotateccw)
        removeddup = set(allletterguest)
        return list(removeddup)

    def panel(self,amountguests):
        if len(self.allpanelanswers)>amountguests:
            return self.allpanelanswers[amountguests - 1]
        else:
            allnumguest = []
            allnumguest = allnumguest 
            lastnum = [(amountguests - 1)]
            secondtolastnum = [(amountguests - 2)]
            lasttwonum = lastnum + secondtolastnum
            if amountguests == 1:
                numguest1 = [[0]]
                allnumguest += numguest1
                self.allpanelanswers += allnumguest
                return allnumguest
            elif amountguests == 2:
                numguest2 = [[0, 1], [1, 0]]
                allnumguest += numguest2
                self.allpanelanswers += allnumguest
                return allnumguest
            elif amountguests > 2:
                panelminus1 = []
                panelminus1 = [Wedding().panel(amountguests-1)]
                for count1, list1 in enumerate(panelminus1):
                    for count2, list2 in enumerate(list1):
                        list2 += lastnum
                        list1[count2] = list2
                    allnumguest += list1      
                panelminus2 = [Wedding().panel(amountguests-2)]
                for count1, list1 in enumerate(panelminus2):
                    for count2, list2 in enumerate(list1):
                        list2 += lasttwonum
                        list1[count2] = list2
                    allnumguest += list1 
                self.allpanelanswers += allnumguest
            #self.allpanelanswers[amountguests - 1] = allnumguest
            return allnumguest

    def barriers(self, guests, bars):
        bars.sort() # causes an issue if you use {} instead of []
        maxbar = max(bars)
        minbar = min(bars)
        numallmiddlestring = []
        letterallmiddlestring = []
        stringpart1 = guests[0:minbar]  # does not include guests[barplace]
        lenstringpart1 = len(stringpart1)
        stringpart2 = guests[maxbar:(len(guests))]
        lenstringpart2 = len(stringpart2)
        section1 = stringpart2 + stringpart1
        allsection1 = [Wedding().panel(len(section1))]
        for barnum, barplace in enumerate(bars):
            if barplace == maxbar:
                pass
            elif barplace != maxbar:
                middlestring = guests[barplace:bars[barnum + 1]]
                numallmiddlestring += [Wedding().panel(len(middlestring))]
                letterallmiddlestring.append(middlestring)
        letterallsolutions = [section1] + letterallmiddlestring
        allsolutions = allsection1 + numallmiddlestring
        solutionsproduct = list(itertools.product(*allsolutions))
        allletterguest = []  
        for solutiongroupnum, eachsolutiongroup in enumerate(solutionsproduct): #([0, 1, 2, 3, 4], [0, 1, 2], [0, 1])
            onesolutionletterguest = ""                
            for solutionnum, eachsolution in enumerate(eachsolutiongroup): #[0, 1, 2, 3, 4]
                sectionguestlist = letterallsolutions[solutionnum]               
                letteranswer = ""
                for numseat in eachsolution: # "0"
                    letterseat = sectionguestlist[numseat]
                    letteranswer += letterseat
                if solutionnum == 0:
                    if minbar == 0:
                        lastpart = letteranswer[0:lenstringpart2]
                        onesolutionletterguest += "|"
                    else:    
                        firstpart = letteranswer[-lenstringpart1:]  #gets last amount of characters from string
                        lastpart = letteranswer[0:lenstringpart2]
                        onesolutionletterguest+= (firstpart + "|")
                else:
                    onesolutionletterguest += (letteranswer + "|")
                
            onesolutionletterguest += lastpart    
            allletterguest.append(onesolutionletterguest)
        removeddup = set(allletterguest)
        return list(removeddup)


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