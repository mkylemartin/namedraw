# namedraw
draw names for gift exchanges with simple constraints

## Usage:

```
python namedraw_constraint.py input_names.txt
```

## format of `input_names.txt`

```
kyle april
curt eliza
jared courtney
katie
```

Couples are on the same line, individuals can be on a single line. Being on the same line introduces the constraint of not giving/receiving a gift from that person; this allows past years to be taken into account. 

My attempt at solving the problem by hand is in `namedraw.py`. I use the constraint-based code from [here](https://gist.github.com/bartaelterman/3954eff5e5249e52cd473eec724f544e) to solve the problem and generate a total number of solutions found. 