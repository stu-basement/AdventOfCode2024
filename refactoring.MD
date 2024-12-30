Goals of refactoring:

- correct solutions to all problems (part 1 and part 2)
- improved execution time
- greater than 9/10 pylint score
- Pythonic patterns as far as known to date (*)
- problem-space solutions (**)
- leverage libraries where possible
- no more than one page of code per solution where possible
- modularise and reuse useful code between puzzles where possible

(*) I learned a number of Pythonic approaches during the AdventOfCode period.  This refactoring aims to use the patterns learned.  This does not represent the totally Pythonic way of doing things, just what I know so far.

(**) Example: rather than navigating a maze by moving a robot on a map, transform the maze into a graph representation and solve the problem on nodes/edges.

Day 4 was refactored in this way by using a set to represent the locations of Xs and As and a dictionary for the locations of other letters, then checking set and dictionary membership for word matching

