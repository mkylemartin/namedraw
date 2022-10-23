#python3
"""
    Purpose:
        for each person draw a name at random 
        from the remaining names
        that arent a couple

    Usage:
        python3 namedraw.py input_names.txt
"""

from random import choice
import sys


input_names = sys.argv[1]

def read_names(input_file):
    """ 
        args:
            input file
        returns:
            data structure of names representing couples and people
    """

    with open(input_file, 'r') as f:
        name_lines = f.read().split('\n')
        family = []
        names = []
        for raw_line in name_lines:
            line = raw_line.split()
            # build families
            family.append(line)
            # build all names
            [names.append(name) for name in line]
    return family, names


def draw_matches(family, names):
        if len(names) % 2 == 1:
            print('oh no, odd number!')
        
        hat = names
        picked = []

        while hat:
            giver = choice(hat)
            hat.remove(giver)
            
            # giver's family
            givers_fam = [fam for fam in family if giver in fam][0]
            # print(givers_fam)
            getter = choice(hat)
            while (getter in givers_fam) or (getter in picked):
                # chose again
                getter = choice(hat)

            picked.append(getter)
            
            print(f'{giver: <10} -> {getter}')

        
       
if __name__ == "__main__":
    family, names = read_names(input_names)
    draw_matches(family, names)