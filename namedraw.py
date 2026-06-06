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


def parse_constraint_file(input_file):
    """Parse the constraint file into persons, couple pairs, and year constraints.

    Lines that introduce at least one new name define the family structure:
      - 1 name  → singleton participant
      - 2 names → couple (bidirectional: neither can give to the other)

    Lines where all names are already known are past-year pairing records:
      - 2 names → directional (giver gave to receiver last year; giver can't repeat)

    Returns:
        persons         – ordered list of unique participants
        couples         – list of (name1, name2) bidirectional constraint pairs
        year_constraints – list of (giver, receiver) directional constraint pairs
    """
    with open(input_file) as f:
        lines = [l.split() for l in f.read().splitlines() if l.strip()]

    seen = set()
    persons = []
    couples = []
    year_constraints = []

    for names in lines:
        has_new = any(n not in seen for n in names)
        if has_new:
            for n in names:
                if n not in seen:
                    seen.add(n)
                    persons.append(n)
            if len(names) == 2:
                couples.append((names[0], names[1]))
        else:
            if len(names) == 2:
                year_constraints.append((names[0], names[1]))

    return persons, couples, year_constraints


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