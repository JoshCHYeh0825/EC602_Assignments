
class Wedding:
    "Wedding() - a model for wedding guests seated at a ciruclar table"
    
    building_arr = []
    
    #constructor
    def __init__(self):
        self.building_arr = [["0", "1"], ["00", "01", "10"], ["000", "001", "010", "100"]]
    
    #returns all possible arragements following a single shuffle
    def shuffle(self, guests):
        #screen for trivial cases
        N = len(guests)
        
        #no guests
        if N <= 0:
            return [""]
        #only one guest
        if N == 1:
            return [guests]
        #exactly two guests
        if N == 2:
            return [guests, guests[::-1]]
        
        #calculate relevant map_arr
        map_arr = self.get_swap_map_arr(N)
        
        #determine seating results; add left/right shifts
        seat_arr = self.swap_seats(guests, map_arr)
        seat_arr.append(guests[1:]+guests[0])
        seat_arr.append(guests[N-1]+guests[0:N-1])
        return seat_arr
    
    #returns all possible arragements following a single shuffle with barriers
    def barriers(self, guests, bars):
        #screen for trivial cases
        if not len(bars):
            return self.shuffle(guests)
        
        N = len(guests)
        #no guests
        if N <= 0:
            return [""]
        
        #calculate relevant map_arr w/o barriers
        map_arr = self.get_swap_map_arr(N)
        
        #barrier[y] sits before seat[y] ∴ swap_map[x] = barrier[y-1]
        #identify invalid swap maps
        valid_maps = []
        for swap_map in map_arr:
            valid = True
            for b in bars:
                if swap_map[b-1] == "1":
                    valid = False
            if valid:
                valid_maps.append(swap_map)
        
        #determine seating results; no left/right shifts if at least one barrier
        seat_arr = self.swap_seats(guests, valid_maps)
        
        #add barrier characters
        seat_arr_bars = []
        for seating in seat_arr:
            seat_bars = ""
            offset = 0
            for guest in seating:
                if len(seat_bars)-offset in bars:
                    seat_bars += "|"
                    offset += 1
                seat_bars += guest
            seat_arr_bars.append(seat_bars)
        
        return seat_arr_bars
    
    #determines circular swap_map possiblities for N guests
    def get_swap_map_arr(self, N):
        #if already calculated, return answer
        if N <= len(self.building_arr):
            return self.building_arr[N-1]
        
        #lay out recursive linear (non-circular) base cases
        building_arr = [["0", "1"], ["00", "01", "10"], ["000", "001", "010", "100"]]
        
        #iteratively builds up to swap_maps_arr[N]
        for n in range(3,N):
            building_arr.append([])
            #add swap maps if leading swap is off
            for linear_long in building_arr[n-1]:
                building_arr[n].append("0" + linear_long)
                #add case where loop prevented swap, but now good
                if linear_long[0] == "1" and linear_long[-1] == "0" and linear_long[-2] == "0":
                    building_arr[n].append("0" + linear_long[:-1] + "1")
            #add swap maps if leading swap is on
            for linear_short in building_arr[n-3]:
                building_arr[n].append("10" + linear_short + "0")
                #add case where loop prevented swap, but now good
                if linear_short[0] == "1" and linear_short[-1] == "0" and linear_short[-2] == "0":
                    building_arr[n].append("10" + linear_short[:-1] + "10")
        
        #update array & determine swapping results
        self.building_arr = building_arr
        return building_arr[N-1]
    
    #converts each swap_map in map_arr to seating string in seats_arr
    def swap_seats(self, guests, map_arr):
        N = len(guests)
        seats_arr = []
        #build seating string for each valid swap map
        for swap_map in map_arr:
            seating = ""
            #swap_map[x] sits between seat[x] & seat[x+1]
            for i in range(N):
                if swap_map[i] == "1":
                    seating += guests[(i+1)%N]
                elif swap_map[i-1] == "1":
                    seating += guests[i-1]
                else:
                    seating += guests[i]
            seats_arr.append(seating)
        return seats_arr














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