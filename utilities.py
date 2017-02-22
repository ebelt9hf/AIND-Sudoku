
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
#dia_units = [[rows[i] + cols[i] for i in range(len(cols))], [rows[i] + cols[len(rows) - i - 1] for i in range(len(cols))]]
# As shown in first review:
dia_units = [[r+c for r,c in zip(rows,cols)], [r+c for r,c in zip(rows,cols[::-1])]]

# Add them to a big unit list:
uni_list = row_units + col_units + sqr_units + dia_units
units = dict((s, [u for u in uni_list if s in u]) for s in boxes) # Map boxes to their units
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes) # Map boxes to their peers

assignments = []
def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values
