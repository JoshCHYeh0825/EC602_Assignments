
import itertools

class Wedding: 
    def __init__(self): #do nothing on init
      pass

    def panel(self, guests): #create panel function. Note not required part of assignment but used later
      N_guests = len(guests) #number of guests in string
      if N_guests <= 0: # if 0 guests, return empty string
        return [""]
      if N_guests == 1: # if only one guest, return guest
        return [guests]
      if N_guests == 2: # if two guests return guests and guests in opposite order
        return [guests, guests[::-1]]
      start_map = []  # code continues here if nothing returned yet, so for more than 2 guests
      start_map.append(guests[0]) #create a start map that appends the 1 guest and 2 guest solutions
      start_map.append([guests[0:2], (guests[1] + guests[0])])
      for tmp_guest_num in range(2,N_guests): #for each additional number past two guests, go through the following
        start_map.append([]) #append an empty array as a place holder
        for num_to_append in range(0,len(start_map[tmp_guest_num-1])): #case of n-1 with last guest appended on end
          start_map[tmp_guest_num].append(start_map[tmp_guest_num-1][num_to_append] + guests[tmp_guest_num])
        for num_to_append in range(0,len(start_map[tmp_guest_num-2])): #case of n-2 with last two guests switched spots
          start_map[tmp_guest_num].append(start_map[tmp_guest_num-2][num_to_append] + guests[tmp_guest_num] + guests[tmp_guest_num-1])
      val = start_map[-1] #return last value in map
      return val
    
    def shuffle(self, guests): #shuffle code, equivilent to panel but with no barrier between 0 and -1 positions
      N_guests = len(guests) #number of guests
      if N_guests <= 0: #0, 1, 2 guests same as panel
        return [""]
      if N_guests == 1:
        return [guests]
      if N_guests == 2:
        return [guests, guests[::-1]]
      #3+ guests starts here, create starting map
      start_map = []
      start_map.append(guests[0]) 
      start_map.append([guests[0:2], (guests[1] + guests[0])])
      for tmp_guest_num in range(2,N_guests): #for each additonal number past 2 guests, go through the following
        start_map.append([]) #append an array as a placeholder
        last_map = start_map[tmp_guest_num-1] #define the last map as the previous map
        two_last_map = start_map[tmp_guest_num-2] #define the two last map as the second previous map
        for num_to_append in range(0,len(last_map)): #case where last guest is just appended onto all the last map cases
          start_map[tmp_guest_num].append(last_map[num_to_append] + guests[tmp_guest_num]) 
        for num_to_append in range(0,len(two_last_map)): #case where last two guests are swapped and appended onto all the two-last-map cases
          start_map[tmp_guest_num].append(two_last_map[num_to_append] + guests[tmp_guest_num] + guests[tmp_guest_num-1]) 
      tmp_guests = guests[1:-1] #guests 2 through end-1 panelled, with last guest appended to front, first guest appended to last
      tmp_guests_panel = self.panel(tmp_guests)
      for num_to_append in range(0,len(tmp_guests_panel)):
        start_map[tmp_guest_num].append(guests[-1] + tmp_guests_panel[num_to_append] + guests[0]) 
      #add in rotate left and rotate right case
      start_map[tmp_guest_num].append(guests[1:] + guests[0])
      start_map[tmp_guest_num].append(guests[-1] + guests[:-1])
      val = start_map[-1] #return last map
      return val
      
    def barriers(self, guests, bars): #barrier code where define barriers in code
      num_bars = len(bars)
      if num_bars == 0: #if no bars, same as shuffle
        output = self.shuffle(guests)
      elif num_bars == 1: #if one bar, same as panel but have to shift then un-shift
        bar = bars[0]
        guests_modif = guests[bar:] + guests[:bar]
        temp_output = self.panel(guests_modif)
        output = []
        for i in range(0,len(temp_output)):
          val = temp_output[i]
          if bar == 0: 
            output.append('|' + val)
          else: 
            output.append(val[-bar:] + '|' + val[:-bar])
      else: #otherwise inner barrier segments (i.e. seg 0 - seg 1 panel) same as panel, first panel (seg n - seg0) has to be rearanged
        tmp_strs = [] 
        for b in range(0,len(bars)):
          bar = bars[b]
          last_bar = bars[b-1]
          if b == 0: #if panel 0, rearrange to get segment, perform panel
            guest_seg_array = guests[last_bar:] + guests[:bar]
            temp_output = self.panel(guest_seg_array)
            tmp_strs.append(temp_output)         
          else: #if all other bars besides bar 0, do panel on them, store in a temp output
            guest_seg_array = guests[last_bar:bar]
            temp_output = self.panel(guest_seg_array)
            tmp_strs.append(temp_output)
        combos = list(itertools.product(*tmp_strs)) #do a permutation of all the different combos in list
        output = []
        for combo in combos: #for each combo from the permutation, format it appropriately
          combo = list(combo)
          out_str = ""
          this_seg_zero = combo[0]
          bar_zero = bars[0]
          l = len(this_seg_zero)
          combo[0] = this_seg_zero[l-bar_zero:]
          combo.append(this_seg_zero[:l-bar_zero])
          out_str = "|".join(combo)
          output.append(out_str)
      return output #return the output strings
    



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