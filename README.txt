The Python Z3 program contained in ioz3.py 
uses SMT to parse I/O logic norms, one conclusion
and any number of premises, from a text file and
determines whether the conclusion is provable
given the premises. This is done by representing
the norms as boolean implications using Z3. If no 
proof can be found, the program prints the norms 
required to complete the proof.

To run the program, run the following code:
----
python3 ioz3.py
----
Five text files of norms are included and can be
selected for parsing on line 33 of ioz3.py. The
norms in each text file can also be altered 
according to the user.