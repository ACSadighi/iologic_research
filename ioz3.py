#!/usr/bin/python3
from z3 import *

"""
Change the norm file on line 32 to see how different
rules are handled. Add, remove, or alter the norms
as needed.
"""


def get_boolean_variables(expr):
    variables = set()

    def collect_variables(e):
        if is_const(e):
            if e.sort() == BoolSort():
                variables.add(str(e))
        else:
            for arg in e.children():
                collect_variables(arg)

    collect_variables(expr)
    return variables


# Parser
input_literals = set()
output_literals = set()
prems = False
conc = False
prem_list = []
conclusion = None
fd = 'norms3.txt' # Norm file
with open(fd, 'r') as f:
    for line in f:
        if line.strip() == '':
            prems = False
            conc = False
        if prems or conc:
            norm = [x.strip() for x in line.split(';')]
            for expression in norm:
                expression = expression.replace('\n','')
            tail = eval(norm[0])
            head = eval(norm[1])
            input_literals.update(get_boolean_variables(tail))
            output_literals.update(get_boolean_variables(head))
            if prems:   # Adds premise norm to list
                prem_list.append((tail,head))
            elif conc:  # Adds conclusion norm to list
                conclusion = ((tail,head))
        if 'Given Premises' in line:
            prems = True
        elif 'Given Conclusion' in  line:
            conc = True



# Applies resolution in solver s
s = Solver()
for p in prem_list: # Adds premises to solver
    print('Premise:', p)
    s.add(Implies(p[0],p[1]))
# Adds conclusion to solver
s.add(Not(Implies(conclusion[0],conclusion[1])))
print('Conclusion:', conclusion)
check = s.check() # Checks for satisfiability

# Provable if unsat
if str(check) == 'unsat':
    print('Provable')
else:
    # Not provable if sat
    print('Not provable\n')
    # Adds norms until satisfiable
    new_norms = []
    while str(check) != 'unsat':
        # Gets model
        model = s.model()
        literals = [v for v in model]
        vals = [model[v] for v in model]
        print('Model:', model)

        # Looks for norms that satisfy in resolution
        new_tail = Or()
        new_head = And()
        for lit, val in zip(literals, vals):
            if val and str(lit) in input_literals:
                new_tail = Or(new_tail, Bool(str(lit)))
            elif not val and str(lit) in output_literals:
                new_head = And(new_head, Bool(str(lit)))
            else:
                continue
        
        new_norm = Implies(simplify(new_tail), simplify(new_head))
        print('New norm: ', str(new_norm)[7:], '\n')
        new_norms.append(new_norm)
        s.add(new_norm)
        check = s.check()

    # Prints new norms
    print()
    for i in new_norms:
        print('Add norm: ', str(i)[7:])
    check = s.check()