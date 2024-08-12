#!/usr/bin/python3
from z3 import *

def get_boolean_variables(expr):
    """
    Helper function for the parser to incorporate
    literals from norm heads/tails in their
    respective sets.
    """
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


"""
Variables for norms/literals involved in proof are initialized
"""
body_literals = set()   # Set of variables that appear in norm bodies
head_literals = set()   # Set of variables that appear in norm heads
prem_list = []          # Set of premise norms
conclusion = None       # Conclusion norm

"""
Parser reads text files to populate norm/literal variables
"""
prems = False
conc = False
fd = 'norms3.txt' # Norm file to be read
with open(fd, 'r') as f:
    for line in f:
        if line.strip() == '':  # Stops parsing norms
            prems = False
            conc = False
        if prems or conc:   # Norm is parsed
            # Processes strings
            norm = [x.strip() for x in line.split(';')]
            for expression in norm: #
                expression = expression.replace('\n','')
            # Converts strings to Z3 expressions
            body = eval(norm[0])
            head = eval(norm[1])
            # Adds literals to body/head sets
            body_literals.update(get_boolean_variables(body))
            head_literals.update(get_boolean_variables(head))
            # Stores norms as tuples
            if prems:   # Adds premise norm to list
                prem_list.append((body,head))
            elif conc:  # Sets conclusion norm
                conclusion = ((body,head))

        if 'Given Premises' in line:
            prems = True    # Prepares to parse premise norms
        elif 'Given Conclusion' in  line:
            conc = True     # Prepares to parse conclusion norm



"""
Resolution is applied to the to the premise and
conclusion norms using the Z3 proof solver. 
Norms are added to the solver as Z3 'Implies' 
expressions (i.e. conditional expressions).
"""
# Initializes Z3 solver
solver = Solver()
# Adds premise norms from list to solver
for p in prem_list: 
    solver.add(Implies(p[0],p[1]))
    print('Premise:', p) # Displays premise norm
# Adds negated conclusion norm to solver
solver.add(Not(Implies(conclusion[0],conclusion[1])))
print('Conclusion:', conclusion) # Displays conslusion norm

"""
Norms in the solver are checked for satisfiability.
"""
check = solver.check()

"""
If the solver returns 'unsat', a proof exists for the
given conclusion and premise norms.

If the solver returns 'sat', a proof does not exist.
The model from the solver that returns 'sat' is used
to construct a premise norm to add to the solver.
Premise norms are added to the solver until a 
proof exists and the solver returns 'unsat'.
"""
if str(check) == 'unsat':
    # Displays that proof exists
    print('Provable')
else:
    # Not provable if 'sat'
    print('Not provable\n')

    new_norms = [] # Initializes list of norms to be added
    # New norms are found and added until solver returns 'unsat'
    while str(check) != 'unsat':
        # Gets model that satisfies norms
        model = solver.model()
        literals = [v for v in model]    # List of literals
        vals = [model[v] for v in model] # Truth values of literals

        # Uncomment print statement below to view model
        # print('Model:', model)

        # # #
        # Constructs a new norm using the model, iterating
        # through all literals in all norms. If a literal
        # is a body literal and true in the model, or a head
        # literal and false in the mode, the literal is 
        # included in the new norm.
        # # #
        new_body = Or()
        new_head = And()
        # Checks all literals that appear in all norms
        for lit, val in zip(literals, vals):
            # Adds body literal to new norm if it is true in the model
            if val and str(lit) in body_literals:
                new_body = Or(new_body, Bool(str(lit)))
            # Adds head literal to new norm if it is false in the model
            elif not val and str(lit) in head_literals:
                new_head = And(new_head, Bool(str(lit)))
            else:
                continue
        new_norm = Implies(simplify(new_body), simplify(new_head))
        new_norms.append(new_norm)
        # Uncomment print statement below to see new norm
        # print('New norm: ', str(new_norm)[7:], '\n')
        
        # Adds new norm to solver, checks if 'sat'
        solver.add(new_norm)
        check = solver.check()

    # Prints new norms
    for i in new_norms:
        print('Add norm: ', str(i)[7:])
