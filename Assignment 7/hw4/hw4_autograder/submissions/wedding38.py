
class Wedding: 
    def __init__(self):
      self.results_list = []
      self.guests_segments_list = []
    
    #recusion, 1, 2, more
    #right only
    def panel(self, guests):

      if len(guests) == 1:
        #results_list = []
        #results_list.append(guests)
        #return results_list
        return guests

      elif len(guests) == 2:
        results_list = []
        reverse_guests = reversed(guests)

        results_list.append(guests)
        results_list.append(''.join(reverse_guests))
        return results_list

      else:
        #length at least is 3
        results_list = []
        #stay
        list1 = self.panel(guests[1:])
        #exchange with right
        list2 = self.panel(guests[2:])

        for item in list1:
          results_list.append(guests[0] + item)

        #start_guests = reversed(guests[0:2])
        #print(start_guests)

        for item in list2:
          #results_list.append(''.join(start_guests) + item)
          results_list.append(guests[1] + guests[0] + item)
        return results_list

        
    #guest is input list
    #recursion start with the first guest name
    def shuffle(self, guests):
      results_list = []

      if len(guests) == 2:
        #not reset!
        list0 = self.panel(guests)
        for item in list0:
          results_list.append(item)
        return results_list

      else:
        #first guest not move
        list1 = self.panel(guests[1:])

        for item in list1:
          results_list.append(guests[0] + item)

        #first guest move right
        list2 = self.panel(guests[2:])

        #start_guests = reversed(guests[0:2])

        for item in list2:
          #results_list.append(''.join(start_guests) + item)
          results_list.append(guests[1] + guests[0] + item)

        #first guest move left
        list3 = self.panel(guests[1:-1])

        for item in list3:
          results_list.append(guests[-1] + item + guests[0])

        #right circular
        results_list.append(guests[len(guests) - 1] + guests[0:len(guests) - 1])
        #left circular
        results_list.append(guests[1:] + guests[0])

        return results_list
    #list barrier first
    #stay, segment more
    def barriers(self, guests, bars):
      results_list = []
      guests_segments_list = []
      last_bar_location = 0

      shuffle_result_segment_list = []

      #special case first, first item is barrrier
      if len(bars) == 1 and bars[0] == 0:
        list0 = self.panel(guests)

        for item in list0:
          results_list.append('|' + item)

        return results_list

      #does not move
      #result_stay = ''

      #move first barrier to last
      if bars[0] == 0:
        bars.append(len(guests) - 1)

      for bar_location in bars:
        if bar_location == 0:
          continue

        guests_segments_list.append(guests[last_bar_location:bar_location])

        last_bar_location = bar_location

      

      return results_list


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