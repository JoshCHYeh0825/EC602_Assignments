
from itertools import product

class Wedding: 
  def __init__(self):
    pass
  # end __init__

  def shuffle(self, guests: list):
    # create Guests
    glen = len(guests)
    if glen == 1:
      return guests
    glst = Guest.str2guests(guests)

    # do the shuffle!
    p = []
    # self.move(glst, glen, p)
    Guest.move(glst, glen, p)
    # remove duplicates
    p = list(set(p))
    return p
    # end shuffle

  def barriers(self, guests, bars):
    if not guests:
      return []
    if not bars:
      self.shuffle(guests)
    if len(guests) == 1:
      return ['|' + guests[0]]
    # create guests
    glst = Guest.str2guests(guests, bars)
    blen = len(bars)

    # split guests into clusters
    clusters = []
    for b in range(blen):
      if b == 0:
        clusters.append(glst[:bars[0]])
      else:
        clusters.append(glst[bars[b-1]:bars[b]])
    # add last cluster
    clusters.append(glst[bars[blen-1]:])

    # do the shuffle/move in individual clusters
    p = []
    barred = 0 in bars # is 0 in bars?

    if barred:
      clusters.pop(0)

    if blen == 1 and barred:
      Guest.move(clusters[0], len(clusters[0]), p, barred=True)
    elif barred:
      for c in clusters:
        parts = []
        Guest.move(c, len(c), parts)
        p.append(parts)
      p = self.combine_clusters(p)
    elif blen == 1:
      # get ends
      first = clusters.pop(0)
      last = clusters.pop()
      # shuffle first and last cluster together
      parts = []
      Guest.move(last+first, len(first)+len(last), parts)
      fEnd = []
      lEnd = []
      for e in parts:
        fEnd.append(e[len(last):])
        lEnd.append(e[:len(last)])
      # combine
      for e in range(len(fEnd)):
        p.append(fEnd[e] + '|' + lEnd[e])
    else:
      # get ends
      first = clusters.pop(0)
      last = clusters.pop()
      # shuffle first and last cluster together
      rawEnds = []
      Guest.move(last+first, len(first)+len(last), rawEnds)
      # split rawEnds into two parts
      fEnd = []
      lEnd = []
      for e in rawEnds:
        fEnd.append(e[len(last):])
        lEnd.append(e[:len(last)])
      # shuffle middle clusters
      middle = []
      for c in clusters:
        m = []
        Guest.move(c, len(c), m)
        middle.append(m)
      middle = self.combine_clusters(middle)
      # combine middle and ends
      for e in range(len(fEnd)):
        for m in middle:
          p.append(fEnd[e] + '|' + m + '|' + lEnd[e])
    
    if barred:
      for i in range(len(p)):
        p[i] = '|' + p[i]
    return p
  # end barriers

  def combine_clusters(self, clusters):
    return ['|'.join(combination) for combination in product(*clusters)]
  # end combine_clusters


class Guest:
  def __init__(self, name, position, barriers=[]):
    self.name = name
    self.position = position
    ''' barriers
    0: no barriers                00
    1: barrier to right           01
    2: barrier to left            10
    3: barrier to left and right  11
    '''
    self.barriers = barriers
    self.left = None
    self.right = None
    self.end = False
  # end __init__
    
  def update_left(self, left):
    self.left = left
  # end update_left

  def update_right(self, right):
    self.right = right
  # end update_right

  def get_left(self):
    return self.left
  # end get_left

  def get_right(self):
    return self.right
  # end get_right

  def get_pos(self):
    return self.position
  # end get_pos

  def str2guests(guests, barriers=[]):
    glst = list()
    glen = len(guests)
    blen = len(barriers)
    has_barriers = 0
    for g in range(glen):
      someone = Guest(guests[g], g, 0)
      # check if guest has barriers
      if g in barriers:
        # add barriers
        someone.barriers = 2
        has_barriers += 1
        if has_barriers != blen and barriers[has_barriers] == g+1:
          # has barrier to right
          someone.barriers = 3
          someone.update_right(None)
        if has_barriers == blen:
          someone.end = True
          if g > 0:
            glst[g-1].barriers |= 1
        elif has_barriers == 1:
          if barriers[0] == 0:
            someone.end = True
          else:
            glst[g-1].end = True
            glst[g-1].barriers |= 1
        else:
          glst[g-1].barriers |= 1
        someone.update_left(None)
      else:
        # this guest has no barriers
        if g > 0:
          left = glst[g-1]
          someone.update_left(left)
          left.update_right(someone)
      if g < glen-1 and g:  # is not last guest
        if not someone.barriers & 2:
          left = glst[g-1]
          left.update_right(someone)
        # else:
        #   someone.barriers |= 1
      elif g == glen-1:     # is last guest
        first = glst[0]
        if not first.barriers & 2:
          someone.update_right(first)
          first.update_left(someone)
        else:
          someone.barriers |= 1
          someone.end = True
      glst.append(someone)
    return glst
  # end str2guests

  def get_cluster(glst):
    # get cluster of guests with barriers on both sides
    gn = ""
    for g in glst:
      gn += g.name
    return gn
  # end get_cluster

  def move(glst, glen, ret, swp=[], barred=False):
    # size = len(glst)
    if swp == []:
      # add original guests to ret
      if glen < 4:
        ret.append(Guest.get_cluster(glst))
      swp = []
      # add glen-2 0s to swp
      for i in range(glen-2):
        swp.append(0)
      swp.append(1)
      for i in range(glen-2, -1, -1):
        Guest.move(glst, glen, ret, swp=swp, barred=barred)
        if i:
          swp[i] = 0
          swp[i-1] = 1
      if glst[0].barriers or glen == 2:
        return
      # swap first and last guests
      sglst = glst.copy()
      sglst[0], sglst[glen-1] = glst[glen-1], glst[0]
      ret.append(Guest.get_cluster(sglst))
      # check if it's possible to swap inside guests
      sglst = rmLstIdx(glst, glen-1)
      sglst = rmLstIdx(sglst, 0)
      swp.clear()
      for i in range(glen-4):
        swp.append(0)
      swp.append(1)
      retInt = []
      for i in range(glen-4, -1, -1):
        Guest.move(sglst, glen-2, retInt, swp=swp, barred=True)
        while retInt:
          ret.append(glst[glen-1].name + retInt.pop() + glst[0].name)
        if i:
          swp[i] = 0
          swp[i-1] = 1

      # shift all guests to the right
      sglst = glst.copy()
      sglst.insert(0, sglst.pop())
      ret.append(Guest.get_cluster(sglst))
      # shift all guests to the left
      sglst = glst.copy()
      sglst.append(sglst.pop(0))
      ret.append(Guest.get_cluster(sglst))
    else:
      # add swapped guests to ret
      sglst = glst.copy()
      # get last position of 1 in swp
      idx = swp.index(1)
      sglst[idx], sglst[idx+1] = glst[idx+1], glst[idx]
      gc = Guest.get_cluster(sglst)
      if gc not in ret:
        ret.append(Guest.get_cluster(sglst))
      else:
        return
      # if swp has two 0s in a row
      swap = swp.copy()
      prev = -1
      for s in range(len(swp)-1, -1, -1):
        if swp[s] == 0 and prev == 0:
          sp = swap.copy()
          swap[s+1] = 1
          # remove swp[s] from swap
          swap = rmLstIdx(swap, s)
          Guest.move(sglst, glen, ret, swp=swap, barred=barred)
          swap = sp
        prev = swp[s]
        
  # end move


def rmLstIdx(lst, idx):
  return lst[:idx] + lst[idx+1:]


def show_result(v, partial=False,ind=None):
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
  res = standard.barriers("ab", [0])
  show_result(res)
  # res = standard.shuffle("ABCDEFGHIabcdef")
  # show_result(res)
  # res = standard.shuffle("ABCDEFGHI")
  # show_result(res)
  # res = standard.barriers("ABCDEFGHI", [3, 6])
  # show_result(res)



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
  # standard_tests()