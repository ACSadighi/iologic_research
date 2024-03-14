#!/usr/bin/python3
from z3 import *

s = Solver()

# AND
s.add(Implies(Bool('a'),Bool('x')))
s.add(Implies(Bool('a'),Bool('y')))
#
s.add(Not (Implies(Bool('a'),And(Bool('x'),Bool('y')))))
#
check = s.check()
print(check)

# WO
s = Solver()
s.add(Implies(Bool('a'),Bool('x')))
#
s.add(Not (Implies(Bool('a'),Or(Bool('x'),Bool('y')))))
#
check = s.check()
print(check)

# SI
s = Solver()
s.add(Implies(Bool('a'),Bool('x')))
#
s.add(Not (Implies(And(Bool('a'),Bool('b')),Bool('x'))))
#
check = s.check()
print(check)


