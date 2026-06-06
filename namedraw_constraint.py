from random import shuffle
import sys

from namedraw import read_names
from ortools.sat.python import cp_model
from tqdm import tqdm

"""
    Usage:
        namedraw_constraint.py input_names.txt

"""

input_names = sys.argv[1]

family, persons = read_names(input_names)

# filter out singletons (e.g. Katie)
forbidden = [p for p in family if len(p) > 1]
shuffle(persons)

model = cp_model.CpModel()

variables = {}

for buyer in persons:
    receiver_dict = {}
    for receiver in persons:
        receiver_dict[receiver] = model.NewIntVar(0, 1, f'{buyer} gives a gift to {receiver}')
    variables[buyer] = receiver_dict

for name, buyer in variables.items():
    model.Add(sum(buyer.values()) == 1)

for name in persons:
    model.Add(sum([receivers[name] for buyer_name, receivers in variables.items()]) == 1)

for name in persons:
    model.Add(variables[name][name] == 0)

for name_1, name_2 in forbidden:
    model.Add(variables[name_1][name_2] == 0)
    model.Add(variables[name_2][name_1] == 0)


class AllSolutionsStore(cp_model.CpSolverSolutionCallback):
    """Enumerate all solutions and capture the first one as an example."""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0
        self.__first_solution = []
        self.__pbar = tqdm(desc='Enumerating solutions', unit=' solutions', dynamic_ncols=True)

    def on_solution_callback(self):
        self.__solution_count += 1
        self.__pbar.update(1)
        if self.__solution_count == 1:
            for buyer, buyer_vars in self.__variables.items():
                for receiver, var in buyer_vars.items():
                    if self.Value(var):
                        self.__first_solution.append((buyer, receiver))

    def close(self):
        self.__pbar.close()

    def solution_count(self):
        return self.__solution_count

    def first_solution(self):
        return self.__first_solution


solver = cp_model.CpSolver()
solver.parameters.enumerate_all_solutions = True
solutionsstore = AllSolutionsStore(variables)
result = solver.Solve(model, solutionsstore)
solutionsstore.close()

col_w = max(len(p) for p in persons)

print()
print(f'Total unique assignments: {solutionsstore.solution_count()}')
print()

if result in (cp_model.OPTIMAL, cp_model.FEASIBLE):
    print('Example assignment:')
    print()
    for buyer, receiver in solutionsstore.first_solution():
        print(f'  {buyer:<{col_w}}  →  {receiver}')
    print()
