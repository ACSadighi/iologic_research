The Python Z3 program contained in ioz3.py 
uses SMT to parse I/O logic norms, one conclusion
and any number of premises, from a text file and
determines whether the conclusion is provable
given the premises. This is done by representing
the norms as boolean implications using Z3. If no 
proof can be found, the program prints the norms 
required to complete the proof.

To run the program, ensure that the Z3 Prover is built
and installed in the parent of the current directory.
To do this, visit the following link:
https://github.com/Z3Prover/z3

Once this is done, run the following code:
----
python3 ioz3.py
----


####################
Norm File Notation
####################
Five text files of norms named 'normsk.txt' 
(k being an integer 0-4) are included and can be 
selected for parsing on line 33 of ioz3.py. The
norms in each text file can also be altered 
according to the user.

For parsing purposes, instead of formulating a
norm like 
----
(a, x)
---- 
as in customary I/O logic notation, norms in
the text files are formulated like so:
----
Bool('a') ; Bool('x')
----
There are no parentheses enclosing the entire norm,
a semicolon separates the norm body and head instead
of a comma, and literals are expressed as "Bool('x')"
instead of "x".

To express a conjunctive clause, And() is used. Thus
if "^" is the logical conjunction symbol, the norm
----
(a ^ b, x)
----
is instead formulated as
----
And( Bool('a'), Bool('b') ) ; x
----
Similarly, to express a disjunctive clause, Or() is used. Thus
if "v" is the logical disjunction symbol, the norm
----
(a v b, x)
----
is instead formulated as
----
Or( Bool('a'), Bool('b') ) ; x
----

In these text files, premise norms are entered
directly under the line that says 'Given Premises'
with no lines skipped. below the premise norms, a
blank linke must be preserved before the line with
'Given Conclusion', under which the conclusion norm
is entered.