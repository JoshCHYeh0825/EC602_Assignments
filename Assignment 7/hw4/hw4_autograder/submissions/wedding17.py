

class Wedding:
    def __init__(self):
        self.shuffle_guests_with_barrier = []
        self.sub_strings = []
        self.shuffled_guests=[]
        self.print_str=[]
        self.bar=0
        self.temp_guest_str=''
        self.arrangements=[]
        

    def set_shuffle_guests(self, guests):
        if guests=='':
          return
        shuffle_guests=[]
        self.arrangements=[]
        self.temp_guest_str=''
        if len(guests) <=1:
          temp=[guests]
        elif len(guests) <=2:
          temp=[guests,guests[::-1]]
        else:
          self.shuffle_rec(guests)
          temp=self.arrangements
        for i in temp:
          shuffle_guests.append(i)
        return shuffle_guests

    def set_shuffle_barriers(self,temp_shuffled_guests_list):
        guest_grp=temp_shuffled_guests_list[0]
        for seat_arrangement in guest_grp:
            if len(temp_shuffled_guests_list) > 1:
                self.print_str.append(seat_arrangement)
                self.set_shuffle_barriers(temp_shuffled_guests_list[1:])
                self.print_str.remove(seat_arrangement)
            else:
                printstr=""
                for p_str in self.print_str:
                    printstr+='|'+p_str
                temp_str=(printstr+'|'+seat_arrangement)
                #print(temp_str)
                if self.bar != 0:
                    temp= -abs(self.bar_size - self.bar)-1
                    self.shuffle_guests_with_barrier.append(temp_str[-temp:]+temp_str[:-temp])
                else:
                    self.shuffle_guests_with_barrier.append(temp_str)
        #print(self.shuffle_guests_with_barrier)
        #print(temp_shuffled_guests_list)
        return self.shuffle_guests_with_barrier
    
    def shuffle(self, guests):
      if len(guests) <=1:
         return guests
      elif len(guests) <=2:
         return [guests,guests[::-1]]
      self.arrangements=[]
      self.temp_guest_str=''
      self.shuffle_rec(guests)
      #print(self.arrangements)
      temp_guests=guests[1:-1]
      self.shuffle_rec(temp_guests)
      for idx,strg in enumerate(self.arrangements):
        if len(strg) is not len(guests):
          self.arrangements[idx]= guests[-1:]+self.arrangements[idx]+guests[:1]
      #print(self.arrangements)
      temp=guests[1:]+guests[:1]
      if temp not in self.arrangements:
        self.arrangements.append(temp)

      temp=guests[-1:]+guests[:-1]
      if temp not in self.arrangements:
        self.arrangements.append(temp)
                  
      #print(self.arrangements)
      return self.arrangements
       

    def shuffle_rec(self, guests):
        #case1 stays the same
        self.temp_guest_str=self.temp_guest_str+guests[0:1]
        #print(guests[0:1])
        if len(guests) > 1:
            self.shuffle_rec(guests[1:])
        else:
            #print(self.temp_guest_str)
            #print(guests)
            self.arrangements.append(self.temp_guest_str)
            self.temp_guest_str=self.temp_guest_str[:-1]
            return
        self.temp_guest_str=self.temp_guest_str[:-1]

        #case2 swap with right
        self.temp_guest_str+=guests[1:2]+guests[:1]
        
        if len(guests) > 2:
            self.shuffle_rec(guests[2:])
        else:
            self.arrangements.append(self.temp_guest_str)
            self.temp_guest_str=self.temp_guest_str[:-2]
            return
        self.temp_guest_str=self.temp_guest_str[:-2]

        #case3 swap with left
        '''self.temp_guest_str+=guests[1:2]+guests[:1]+guests[2:3]
        
        if len(guests) > 3:
            self.shuffle_rec(guests[3:])
        else:
            if self.temp_guest_str not in self.arrangements:
              self.arrangements.append(self.temp_guest_str)
            self.temp_guest_str=self.temp_guest_str[:-3]
            return
        self.temp_guest_str=self.temp_guest_str[:-3]
'''
        return 

    def barriers(self, guests, bars):
        self.shuffle_guests_with_barrier = []
        self.sub_strings = []
        self.shuffled_guests=[]
        self.bar=0
        bars.sort()

        if bars[0]!=0:
          self.sub_strings.append(guests[bars[-1]:]+guests[:bars[0]])
          self.bar=bars[0]
          self.bar_size=len(guests[bars[-1]:]+guests[:bars[0]])
        for i in range(1, len(bars)):
            self.sub_strings.append(guests[bars[i - 1]:bars[i]])
        if bars[0]==0 :
          self.sub_strings.append(guests[bars[-1]:])
        for i in self.sub_strings:
            temp = self.set_shuffle_guests(i)
            self.shuffled_guests.append(temp)
        self.print_str=[]
        shuffle_guests_with_barrier = self.set_shuffle_barriers(self.shuffled_guests)
        return shuffle_guests_with_barrier


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