
import itertools as it
class Wedding:
    def __init__(self):
        pass
        self.sol_list = {}
        self.linear_list = {}
        self.list_of_strings_1 = []
        self.list_of_strings_2 = []
    def linear(self, guests):
        orig_guests = guests 
        guest_length = len(guests)
        if guests in self.linear_list:
            copy_of_list = self.linear_list[guest_length]
            return self.linear_list[guest_length] # return the list at that value. 
        if len(guests) == 1:
            self.linear_list[1] = [guests]
            copy_of_list = self.linear_list[1].copy()
            return copy_of_list
        if len(guests) == 2:
            guests_as_list = list(guests)
            self.linear_list[2] = [guests]
            temp_index = guests_as_list[0]
            guests_as_list[0] = guests_as_list[1]
            guests_as_list[1] = temp_index
            guests = ''.join(guests_as_list)
            self.linear_list[2].append(guests)
            copy_of_list = self.linear_list[2].copy()
            return copy_of_list
        elif len(guests) > 2:
            last_char_n1 = guests[-1]
            guests_n1 = guests.rstrip(guests[-1])
            n1_case_list = self.linear(guests_n1) 
            for index, item in enumerate(n1_case_list): 
                item = item + last_char_n1
                n1_case_list[index] = item

            new_guest_n2 = list(guests)
            temp_index = new_guest_n2[-1]
            new_guest_n2[-1] = new_guest_n2[-2]
            new_guest_n2[-2] = temp_index

            last_char_n2 = new_guest_n2[-1]
            second_last_char_n2 = new_guest_n2[-2]
            swapped_chars_n2 = second_last_char_n2 + last_char_n2 

            new_guest_n2 = ''.join(new_guest_n2)
            new_guest_n2 = new_guest_n2.rstrip(new_guest_n2[-1])
            new_guest_n2 = new_guest_n2.rstrip(new_guest_n2[-1])

            n2_case_list = self.linear(new_guest_n2) # will return a list for the n-2 case.
            for index, item in enumerate(n2_case_list):
                item = item + swapped_chars_n2
                n2_case_list[index] = item
            final_list = n1_case_list + n2_case_list

            self.linear_list[guest_length] = final_list

        return final_list

    def shuffle(self, guests):
        orig_guests = guests 
        guest_length = len(guests)
        if any(guests in val for val in self.sol_list.values()):
            copy_of_list = self.sol_list[guest_length]
            return self.sol_list[guest_length] # return the list at that value. 
        if len(guests) == 1:
            self.sol_list[1] = [guests]
            copy_of_list = self.sol_list[1].copy()
            return copy_of_list
        if len(guests) == 2:
            guests_as_list = list(guests)
            self.sol_list[2] = [guests]
            temp_index = guests_as_list[0]
            guests_as_list[0] = guests_as_list[1]
            guests_as_list[1] = temp_index
            guests = ''.join(guests_as_list)
            self.sol_list[2].append(guests)
            copy_of_list = self.sol_list[2].copy()
            return copy_of_list
        elif len(guests) > 2:
            last_char_n1 = guests[-1]
            first_char_n1 = guests[0]
            second_char_n1 = guests[1]
            third_char_n1 = guests[2]
            guests_n1 = guests.rstrip(guests[-1])
            n1_case_list = self.shuffle(guests_n1) 
            new_n1_list = []
            for index, item in enumerate(n1_case_list): 
                item = item + last_char_n1
                n1_case_list[index] = item
                if (item[0] == first_char_n1) or (item[0] == second_char_n1) or (item[0] == last_char_n1):
                    new_n1_list.append(n1_case_list[index])
                
            new_guest_n2 = list(guests)
            temp_index = new_guest_n2[-1]
            new_guest_n2[-1] = new_guest_n2[-2]
            new_guest_n2[-2] = temp_index

            last_char_n2 = new_guest_n2[-1]
            second_last_char_n2 = new_guest_n2[-2]
            swapped_chars_n2 = second_last_char_n2 + last_char_n2
            
            new_guest_n2 = ''.join(new_guest_n2)
            new_guest_n2 = new_guest_n2.rstrip(new_guest_n2[-1])
            new_guest_n2 = new_guest_n2.rstrip(new_guest_n2[-1])
            n2_case_list = self.shuffle(new_guest_n2) # will return a list for the n-2 case.
            new_n2_list = []
            for index, item in enumerate(n2_case_list):
                item = item + swapped_chars_n2
                n2_case_list[index] = item
                if (item[0] == first_char_n1) or (item[0] == second_char_n1) or (item[0] == last_char_n1):
                    new_n2_list.append(n2_case_list[index])
            #swap first and last characters for wrap around case.
            new_guest_n3 = list(guests)
            temp_index = new_guest_n3[-1]
            new_guest_n3[-1] = new_guest_n3[0]
            new_guest_n3[0] = temp_index
            
            last_char_n3 = new_guest_n3[-1]
            first_char_n3 = new_guest_n3[0]
            new_guest_n3 = ''.join(new_guest_n3)
            new_guest_n3 = new_guest_n3.rstrip(new_guest_n3[-1])
            new_guest_n3 = new_guest_n3[1:]

            n3_case_list = self.shuffle(new_guest_n3) # will return a list for the n-2 case.
            new_n3_list = []
            if len(n3_case_list) == 1:
                item = first_char_n3 + n3_case_list[0] + last_char_n3
                new_n3_list.append(item)
                
            elif len(n3_case_list) == 2:
                for index, item in enumerate(n3_case_list):
                    item = first_char_n3 + item + last_char_n3
                    n3_case_list[index] = item
                    if (item[0] == first_char_n1) or (item[0] == second_char_n1) or (item[0] == last_char_n1):
                        new_n3_list.append(n3_case_list[index])
                
            elif len(n3_case_list) > 2:
                for index, item in enumerate(n3_case_list):
                    item = first_char_n3 + item + last_char_n3
                    n3_case_list[index] = item
                    if (item[0] == first_char_n1 and item[-1] == last_char_n1 and (item[1] == second_char_n1 or item[1] == third_char_n1)) or (item[0] == second_char_n1 and item[-1] == last_char_n1 and (item[1] == first_char_n1)) or (item[0] == last_char_n1 and item[-1] == first_char_n1 and (item[1] == second_char_n1 or item[1] == third_char_n1)):
                        new_n3_list.append(n3_case_list[index])
            final_list = new_n1_list + new_n2_list + new_n3_list
            final_list.sort()

            self.sol_list[guest_length] = final_list

        return final_list
    
    def barriers(self, guest, bars):
        pass
        guests_as_list = list(guests)
        first_char = guests_as_list[0]
        last_char= guests_as_list[-1]
        added_barriers = 0
        bars.sort()
        #print(bars)
        new_bar_index = []
        for item in bars:
            #every time an item is inserted into the guests, we need to increment the rest of bars by 1.
            if bars[0] == item:
                guests_as_list.insert(item, '|')
                added_barriers += 1
                new_bar_index.append(item)
            else: 
                item = item + added_barriers
                guests_as_list.insert(item, '|')
                added_barriers += 1
                new_bar_index.append(item)
                
        sep_list = []
        temp_list = []
        for item in guests_as_list:
            if item == '|':
                sep_list.append(temp_list)
                temp_list = []
            else:
                temp_list.append(item)
        sep_list.append(temp_list)
        
        result = []
        if not sep_list[0]:
            del sep_list[0]
        for item in sep_list:
            str_item = ''.join(item)
            new_item = self.shuffle(str_item)
            result.append(new_item)
        new_result = list(it.product(*result))
        new_add = []
        for index, item in enumerate(new_result):
            new_result[index] = '|'.join(item)
            new_item_list = list(new_result[index])
            
            if new_result[index][0] == first_char and new_result[index][-1] == last_char:
                #print(new_item_list)
                new_item_list[0] = last_char
                new_item_list[-1] = first_char
                final_new_add = ''.join(new_item_list)
                new_add.append(final_new_add)
                #print(final_new_add)
        new_result = new_result + new_add

        print(*new_result, sep="\n")


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