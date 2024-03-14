#!/usr/bin/python3
from z3 import *

"""
Currently, io.py only handles logic with the OR
rule. The other rules can be applied similarly.
"""

# Parser
prems = False
conc = False
prem_list = []
conclusion = None
fd = 'norms2.txt' # Norm file
with open(fd, 'r') as f:
    for line in f:
        if line.strip() == '':
            prems = False
            conc = False
        if prems or conc:
            norm = [x.strip() for x in line.split(';')]
            for expression in norm:
                expression = expression.replace('\n','')
            if prems:   # Adds premise norm to list
                prem_list.append((eval(norm[0]),eval(norm[1])))
            elif conc:  # Adds conclusion norm to list
                conclusion = (eval(norm[0]),eval(norm[1]))
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
    print('Not provable')
    # Adds norms until satisfiable
    new_norms = []
    while str(check) != 'unsat':
        # Gets model
        model = s.model()
        literals = [v for v in model]
        vals = [model[v] for v in model]
        # Looks for norms that satisfy in resolution
        for i in range(len(vals)):
            if vals[i]:
                # Adds premise
                new_lit = literals[i]
                new_norm = Implies(Bool(str(new_lit)),conclusion[1])
                new_norms.append(new_norm)
                s.add(new_norm)
                check = s.check()

    # Prints new norms
    for i in new_norms:
        print('Add norm: ', str(i)[7:])
    check = s.check()