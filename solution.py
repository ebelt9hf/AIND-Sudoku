assignments = []

rows = "ABCDEFGHI"
cols = "123456789"

def cross(A, B):
    "Cross product of elements in A and elements in B"
    return[s + t for s in A for t in B]

boxes = cross(rows,cols)
# Define the different units: rows, columns, squares and diagonals
row_units = [cross(r, cols) for r in rows]
col_units = [cross(rows, c) for c in cols]
sqr_units = [cross(r, c) for r in ('ABC', 'DEF', 'GHI') for c in ('123', '456', '789')]
dia_units = [[rows[i] + cols[i] for i in range(len(cols))], [rows[i] + cols[len(rows) - i - 1] for i in range(len(cols))]]
# Add them to a big unit list:
uni_list = row_units + col_units + sqr_units + dia_units
units = dict((s, [u for u in uni_list if s in u]) for s in boxes) # Map boxes to their units
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # Map boxes to their peers

def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def duplDig(unit_dic):
    """Enumerate returning the naked twin's digits and the boxes which:
            * do not contain the twin
            * are not solved
            --> The boxes were the twin's digits should be removed
        Args:
            unit in the format: dict(box:digit)
        Returns:
            (digit, [boxes matching above conditions])
    """
    digits = list(unit_dic.values())
    for value in [d for d in set(digits) if len(d) == 2 and digits.count(d) > 1]:
        nduplBoxes = [b for (b, v) in unit_dic.items() if v != value and len(v) > 1]
        if len(nduplBoxes) > 0:# yield a value
            yield value, nduplBoxes

def naked_twins(values):
    """Eliminates values using the naked twins strategy, thus eliminates the
        naked twins as possibilities for their peers. Uses the currently defined uni_list variable which contains the possible
        units defined.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """
    # As it not clear which unit space should be used
    #uni_list = row_units + col_units + sqr_units
    for unit in uni_list: # Iterate through the peers
        # Map the unit boxes to their digits
        unitDig = {box:values[box] for box in unit}
        for (value, nDuplBoxes) in duplDig(unitDig):
            for nduplBox in nDuplBoxes:
                oldVal = values[nduplBox]
                # Remove the naked twin's digits
                newVal = ''.join([d for d in oldVal if d not in value])
                assign_value(values, nduplBox, newVal)
    return(values)

def grid_values(grid):
    """
    Convert grid into a dict of {square: char} with '123456789' for empties.
    Args:
        grid(string) - A grid in string form.
    Returns:
        A grid in dictionary form
            Keys: The boxes, e.g., 'A1'
            Values: The value in each box, e.g., '8'. If the box has no value, then the value will be '123456789'.
    """
    lst = ['123456789' if v == '.' else v for v in grid] # subtitude . with 123...
    return dict(zip(boxes, lst))

def display(values):
    """
    Display the values as a 2-D grid.
    Args:
        values(dict): The sudoku in dictionary form
    """
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '')
                      for c in cols))
        if r in 'CF': print(line)
    return

def eliminate(values):
    """Eliminate values from peers of each box with a single value.

    Go through all the boxes, and whenever there is a box with a single value,
    eliminate this value from the set of values of all its peers.

    Args:
        values: Sudoku in dictionary form.
    Returns:
        Resulting Sudoku in dictionary form after eliminating values.
    """
    # Get the solved boxes and iterate
    for solved in [k for (k,v) in values.items() if len(v) == 1]:
        valueSolved = values[solved]
        for peer in peers[solved]:
            # replace works here because valueSolved has length one :)
            assign_value(values, peer, values[peer].replace(valueSolved, ''))

    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in uni_list:
        for digit in '123456789':
            # For each digit get canditates and only canditate
            # --> Solved with curr digit
            cand = [box for box in unit if digit in values[box]]
            if len(cand) == 1:
                assign_value(values, cand[0], str(digit))
    return values

def reduce_puzzle(values):
    """Repeat both methods until no change or board has mistake (possible values == 0)

        Input: Soduko in dictionary form
        Output: False if sodoku has no solution
                Sodoku in dictionary form, solved until no change possible.
    """
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        # Your code here: Use the Eliminate Strategy
        values = eliminate(values)
        # Your code here: Use the Only Choice Strategy
        values = only_choice(values)
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False
    return values

def search(values):
    "Using depth-first search and propagation, create a search tree and solve the sudoku."
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values == False: # values could also be a dictionary!!
        return False # This is so ugly, this cannot be considered the python way
    # Get the unsolved boxes and their digits
    unsolvedBoxes = [(box, digit) for (box, digit) in values.items() if len(digit) > 1]
    if len(unsolvedBoxes) == 0: # Puzzle is solved
        return values
    # Choose one of the unsolved boxes with the fewest possibilities
    currNode , currDig = min(unsolvedBoxes, key = lambda x : len(x[1]))
    # Use currNode as node and begin to branch for the different possible digits.
    # Apply search on the resulting sodokus (the currNode is solved).
    # If false:     no solution was found in the current branch.
    # If not false: solution was found in the current branch (stop recursion)
    for dig in currDig:
        cValues = copy(values)
        assign_value(cValues, currNode, dig)
        cValues = search(cValues)
        if cValues != False:
            return cValues
    return False

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    # Convert to dictionary
    values = grid_values(grid)
    # Start search on function and return return.
    return search(values)

if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
