"""
Calculates how many unique years of Secret Santa draws remain before
all valid assignments have been used up.

Usage:
    python namedraw_capacity.py input_names.txt
    python namedraw_capacity.py input_names.txt --history history.txt

History file format (one year per blank-line-separated block):
    kyle -> april
    curt -> jared
    ...

    kyle -> eliza
    curt -> courtney
    ...
"""

import argparse
import sys

from namedraw import read_names
from ortools.sat.python import cp_model
from tqdm import tqdm


def build_model(persons, forbidden):
    model = cp_model.CpModel()
    variables = {}
    for buyer in persons:
        receiver_dict = {}
        for receiver in persons:
            receiver_dict[receiver] = model.NewIntVar(0, 1, f'{buyer}->{receiver}')
        variables[buyer] = receiver_dict

    for buyer, buyer_vars in variables.items():
        model.Add(sum(buyer_vars.values()) == 1)

    for person in persons:
        model.Add(sum(receivers[person] for receivers in variables.values()) == 1)

    for person in persons:
        model.Add(variables[person][person] == 0)

    for name_1, name_2 in forbidden:
        model.Add(variables[name_1][name_2] == 0)
        model.Add(variables[name_2][name_1] == 0)

    return model, variables


class SolutionCollector(cp_model.CpSolverSolutionCallback):
    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solutions = set()
        self.__pbar = tqdm(desc='Enumerating solutions', unit=' solutions', dynamic_ncols=True)

    def on_solution_callback(self):
        assignment = frozenset(
            (buyer, receiver)
            for buyer, buyer_vars in self.__variables.items()
            for receiver, var in buyer_vars.items()
            if self.Value(var)
        )
        self.__solutions.add(assignment)
        self.__pbar.update(1)

    def close(self):
        self.__pbar.close()

    def solutions(self):
        return self.__solutions


def load_history(path):
    """Parse history file into a set of frozenset assignments."""
    used = set()
    with open(path) as f:
        raw = f.read()

    for block in raw.strip().split('\n\n'):
        pairs = set()
        for line in block.strip().splitlines():
            line = line.strip()
            if not line:
                continue
            parts = [p.strip() for p in line.split('->')]
            if len(parts) == 2:
                pairs.add((parts[0], parts[1]))
        if pairs:
            used.add(frozenset(pairs))
    return used


def main():
    parser = argparse.ArgumentParser(description='Calculate remaining unique Secret Santa draws.')
    parser.add_argument('input_names', help='Constraint file (same format as namedraw_constraint.py)')
    parser.add_argument('--history', help='Optional history file of past assignments', default=None)
    args = parser.parse_args()

    family, persons = read_names(args.input_names)
    forbidden = [p for p in family if len(p) > 1]

    model, variables = build_model(persons, forbidden)

    solver = cp_model.CpSolver()
    solver.parameters.enumerate_all_solutions = True
    collector = SolutionCollector(variables)
    solver.Solve(model, collector)
    collector.close()

    all_solutions = collector.solutions()
    total = len(all_solutions)

    print()
    print(f'Total unique assignments: {total}')

    if args.history:
        used = load_history(args.history)
        known_used = used & all_solutions
        remaining = total - len(known_used)
        print(f'Used so far (from history): {len(known_used)}')
        print(f'Remaining unique draws:     {remaining}')
        print()
        if remaining == 0:
            print('All unique assignments have been used — time to reset!')
        else:
            print(f'You have {remaining} year(s) of unique draws remaining before needing to reset.')
    else:
        print()
        print(f'You have {total} year(s) of unique draws before any assignment repeats.')


if __name__ == '__main__':
    main()
