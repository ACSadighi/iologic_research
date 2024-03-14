#!/usr/bin/python3
from z3 import *

prems = False
conc = False
prem_list = []      # List of premise norms
conclusion = None
fd = 'norms2.txt'
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

# print(prem_list)
# print(conclusion)

s = Solver()
for p in prem_list:
    print('Premise:', p)
    s.add(Implies(p[0],p[1]))
print('Conclusion:', conclusion)
s.add(Not(Implies(conclusion[0],conclusion[1])))
check = s.check()

if str(check) == 'unsat':
    print('Provable')
else:
    print('Not provable')
    while str(check) != 'unsat':
        model = s.model()
        print(model)
        literals = [v for v in model]
        vals = [model[v] for v in model]
        # print(model)
        # print(literals)
        # print(vals)
        new_norms = []
        for i in range(len(vals)):
            if vals[i]:
                new_lit = literals[i]
                # print(type(Bool(str(new_lit))))
                new_norm = Implies(Bool(str(new_lit)),conclusion[1])
                new_norms.append(new_norm)
                s.add(new_norm)
                check = s.check()

        for i in new_norms:
            print('Add norm: ', str(i)[7:])
        check = s.check()
#"""
