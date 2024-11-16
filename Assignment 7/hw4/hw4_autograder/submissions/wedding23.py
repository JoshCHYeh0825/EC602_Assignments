
class Wedding:
    def __init__(self):
        pass

    def shuffle(self, guests):
        arrangements = []
        right_guests = ""
        left_guests  = ""
        arrangements.append(guests)
        if len(guests) > 2:
        	self.generate_shuffle_arrangements(list(guests),list(guests),arrangements,index=0)
        	for i in range(len(guests)):
        			right_guests += guests[i-1]
        			if i < len(guests)-1:
        				left_guests  += guests[i+1]
        			else:
        				left_guests  += guests[0]
        	arrangements.append(right_guests)
        	arrangements.append(left_guests)
        elif len(guests) > 1:
        	char_guests = [char for char in guests]
        	char_guests[0], char_guests[1] = char_guests[1], char_guests[0]
        	arrangements.append(''.join(char_guests))
        arrangements.sort()
        return arrangements

	#shuffle_version_2
    def generate_shuffle_arrangements(self, guests,ori_guests, arrangement,index):
        i = index
        while i < len(guests):
        	if i < len(guests)-1:
        		guests[i], guests[i+1] = guests[i+1], guests[i]
        		arrangement.append(''.join(guests))
        		guests[i], guests[i+1] = guests[i+1], guests[i]
        	elif i == len(guests)-1 and guests[0] == ori_guests[0]:
        		guests[i], guests[0] = guests[0], guests[i]
        		arrangement.append(''.join(guests))
        		guests[i], guests[0] = guests[0], guests[i]
        	i += 1
        if index < len(guests)-1:
        	j = index
	        while j < len(guests):
	        	if j < len(guests)-1:
	        		guests[j], guests[j+1] = guests[j+1], guests[j]
	        		self.generate_shuffle_arrangements(guests,ori_guests,arrangement,j+2)
	        		guests[j], guests[j+1] = guests[j+1], guests[j]
	        	elif j == len(guests)-1:
	        		guests[j], guests[0] = guests[0], guests[j]
	        		self.generate_shuffle_arrangements(guests,ori_guests,arrangement,j+2)
	        		guests[j], guests[0] = guests[0], guests[j]
	        	j = j + 1


    def barriers(self, guests, bars):
        arrangements = []
        guests_barriers = guests
        for index,item in enumerate(bars):
        	guests_barriers = guests_barriers[:(item+index)] + '|' + guests_barriers[(item+index):]
        arrangements.append(guests_barriers)
        self.generate_barrier_arrangements(list(guests_barriers),list(guests_barriers),arrangements,index=0)
        arrangements.sort()
        return arrangements

    def generate_barrier_arrangements(self, guests,ori_guests, arrangement,index):
        i = index
        while i < len(guests):
        	if i < len(guests)-1 and guests[i] != '|' and guests[i+1] != '|':
        		guests[i], guests[i+1] = guests[i+1], guests[i]
        		arrangement.append(''.join(guests))
        		guests[i], guests[i+1] = guests[i+1], guests[i]
        	elif i == len(guests)-1 and guests[0] == ori_guests[0] and guests[i] != '|' and guests[0] != '|':
        		guests[i], guests[0] = guests[0], guests[i]
        		arrangement.append(''.join(guests))
        		guests[i], guests[0] = guests[0], guests[i]
        	i += 1
        if index < len(guests)-1:
        	j = index
	        while j < len(guests):
	        	if j < len(guests)-1 and guests[j] != '|' and guests[j+1] != '|':
	        		guests[j], guests[j+1] = guests[j+1], guests[j]
	        		self.generate_barrier_arrangements(guests,ori_guests,arrangement,j+2)
	        		guests[j], guests[j+1] = guests[j+1], guests[j]
	        	elif j == len(guests)-1 and guests[0] == ori_guests[0] and guests[j] != '|' and guests[0] != '|':
	        		guests[j], guests[0] = guests[0], guests[j]
	        		self.generate_barrier_arrangements(guests,ori_guests,arrangement,j+2)
	        		guests[j], guests[0] = guests[0], guests[j]
	        	j = j + 1

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

