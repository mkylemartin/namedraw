from random import shuffle
import sys

from namedraw import read_names
from ortools.sat.python import cp_model

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
        receiver_dict[receiver] = model.NewIntVar(0, 1, f'{buyer}\t gives a gift to {receiver}')
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
    """Count all solutions"""

    def __init__(self, variables):
        cp_model.CpSolverSolutionCallback.__init__(self)
        self.__variables = variables
        self.__solution_count = 0


    def on_solution_callback(self):
        self.__solution_count += 1

    def solution_count(self):
        return self.__solution_count

all_variables = []
for name, x in variables.items():
    all_variables += list(x.values())

solver = cp_model.CpSolver()
solutionsstore = AllSolutionsStore(all_variables)
result = solver.SearchForAllSolutions(model, solutionsstore)
print('Number of solutions found: %i' % solutionsstore.solution_count())
print()
solver = cp_model.CpSolver()
result = solver.Solve(model)

if result != cp_model.FEASIBLE:
    for buyer, buyer_vars in variables.items():
        for receiver, var in buyer_vars.items():
            if solver.Value(var):
                print(var)

