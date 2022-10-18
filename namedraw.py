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
            if len(line) > 1:
                family.append(line)
            # build all names
            [names.append(name) for name in line]
    return family, names


def draw_matches(family, names):
        givers = names
        receivers = names

        chosen = []

        for giver in givers:
            # giver's family
            givers_family = [fam for fam in family if giver in fam]
            # chose a recipient
            receiver = choice(receivers)
            # match found
            print(f'{giver: >10} -> {receiver}')
            




family, names = read_names(input_names)
draw_matches(family, names)