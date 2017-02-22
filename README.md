# Artificial Intelligence Nanodegree
## Introductory Project: Diagonal Sudoku Solver

# Question 1 (Naked Twins)
Q: How do we use constraint propagation to solve the naked twins problem?  
A: A naked twin is given if a unit, e.g. row, square, contains two boxes having
the same two digits as candidates, as this implies that these two digits must be
in these boxes, thus that they are no candidates for the remaining boxes.
Obviously this can be generalized to N-tuples (N \in 1:8). We already implemented
the N = 1 generalizations, as so called elimination technique. One could Furthermore
generalize to overlapping digits, e.g., {A1: 12, A2:23, A3:13, ...}. However, this
could be difficult to check with acceptable computer speed.

A naked twin, as elaborated above, is an additional technique to detect implications
of the simple 1:9 uniqueness in a unit constraint. Thus, we can solve a Sudoku
faster, as we have an additional constraint detection method.

# Question 2 (Diagonal Sudoku)
Q: How do we use constraint propagation to solve the diagonal Sudoku problem?  
A: In Sudoku the constraints are defined on units of size 9, e.g. rows, squares.
The constraint is the uniqueness of the digits 1:9 and additionally that all boxes
are filled. Thus, adding the diagonal to the units reduces the number of possible
Sudokus and should thus increase the speed at which a Sudoku can be solved
(as we have more constraints).

To answer the question directly, we solve the Sudoku by reducing the number of
candidates in each box. This is done by extracting information from the peer boxes'
candidates as we know that each digit is unique in its peers (and thus not a candidates
in another peer box.)

### Install

This project requires **Python 3**.

We recommend students install [Anaconda](https://www.continuum.io/downloads), a pre-packaged Python distribution that contains all of the necessary libraries and software for this project.
Please try using the environment we provided in the Anaconda lesson of the Nanodegree.

##### Optional: Pygame

Optionally, you can also install pygame if you want to see your visualization. If you've followed our instructions for setting up our conda environment, you should be all set.

If not, please see how to download pygame [here](http://www.pygame.org/download.shtml).

### Code

* `solutions.py` - You'll fill this in as part of your solution.
* `solution_test.py` - Do not modify this. You can test your solution by running `python solution_test.py`.
* `PySudoku.py` - Do not modify this. This is code for visualizing your solution.
* `visualize.py` - Do not modify this. This is code for visualizing your solution.

### Visualizing

To visualize your solution, please only assign values to the values_dict using the ```assign_values``` function provided in solution.py

### Data

The data consists of a text file of diagonal sudokus for you to solve.
