
if __name__ == '__main__':
    
    print("""\n\nWELCOME TO THE SUDOKU SOLVER!\n\n\nInput the sudoku board as a string. It should be 81 characters long and have periods in the place of the empty cells:""")
    diag_sudoku_grid = input()

    print("\n\nIs this a diagonal sudoku? Enter y/n")
    diagonal = input()
    diagonal = diagonal.lower()
    if (diagonal == "y")|(diagonal == "yes"):
        diagonal = True 
    else:
        diagonal = False



    

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a,b):
    """given two strings — a and b,
    return the list formed by all the possible concatenations of a letter s 
    in string a with a letter t in string b."""
    return [s+t for s in a for t in b]



boxes = cross(rows,cols)

row_units = [cross(r, cols) for r in rows]
# Element example:
# row_units[0] = ['A1', 'A2', 'A3', 'A4', 'A5', 'A6', 'A7', 'A8', 'A9']
# This is the top most row.

column_units = [cross(rows, c) for c in cols]
# Element example:
# column_units[0] = ['A1', 'B1', 'C1', 'D1', 'E1', 'F1', 'G1', 'H1', 'I1']
# This is the left most column.

square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
# Element example:
# square_units[0] = ['A1', 'A2', 'A3', 'B1', 'B2', 'B3', 'C1', 'C2', 'C3']
# This is the top left square.

diagonal_units = []

if diagonal:
    diagonal_units = [[a+b for a,b in zip(rows,cols)]] + [[a+b for a,b in zip(rows,"987654321")]]

# Element example:
# diagonal_units[0] = ['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']
# This is the left top to right bottom diagonal.


unitlist = row_units + column_units + square_units +diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
# Dictionary of units to which each box belongs to. Keyed by box.
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)
# Dictionary of boxes from the same unit. Keyed by each box.


def assign_value(values, box, value):
    """
    Please use this function to update your values dictionary!
    Assigns a value to a given box. If it updates the board record it.
    """

    # Don't waste memory appending actions that don't actually change any values
    if values[box] == value:
        return values

    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    """Eliminate values using the naked twins strategy.
    Args:
        values(dict): a dictionary of the form {'box_name': '123456789', ...}

    Returns:
        the values dictionary with the naked twins eliminated from peers.
    """

    # Find all instances of naked twins
    for unit in unitlist:
        
        # list all of the different values in a unit
        unitvals = [values[box] for box in unit]
        
        # take out values that occur the same number of times in a unit as their length (so twins/triplets etc..)
        purgevals = set([value for value in unitvals if ((unitvals.count(value)>1) &
                                                  (len(value)==unitvals.count(value)))])
         
        #purge digits from the other boxes in the same unit
        for vals in purgevals:
            for box in unit:
                if (set(values[box]) != set(vals))&(len(values[box])>1):
                    for digit in vals:
                        assign_value(values,box,values[box].replace(digit,""))
                        
    return values                
    
    
   


def grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    grid_dict = {}
    for box, value in zip(boxes,grid):
        grid_dict[box] = value.replace(".", "123456789")
        
    return grid_dict

def start_grid_values(grid):
    """Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    grid_dict = {}
    for box, value in zip(boxes,grid):
        grid_dict[box] = value.replace(".", " ")
        
    return grid_dict

def display(values):
    """
    Display the values as a 2-D grid.
    Input: The sudoku in dictionary form
    Output: None
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
    solved_values = [box for box in values.keys() if len(values[box]) == 1]
    for box in solved_values:
        digit = values[box]
        for peer in peers[box]:

            assign_value(values, peer,values[peer].replace(digit,''))
            
    return values

def only_choice(values):
    """Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    
    
    for unit in unitlist:
        for digit in '123456789':
            inboxlist=[box for box in unit if digit in values[box]]
            if len(inboxlist) == 1:
                assign_value(values, inboxlist[0], digit)
                
    return values

def reduce_puzzle(values):
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])
        values = eliminate(values)
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

    if values is False:
        return False
    elif all(len(values[box]) == 1 for box in boxes): 
        return values
    # Choose one of the unfilled squares with the fewest possibilities
    
    _,box = min((len(values[box]),box) for box in boxes if len(values[box])>1)    
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!

    for digit in values[box]:
        try_dict = values.copy()
        assign_value(try_dict, box, digit)
        try_result = search(try_dict)
        if try_result:
            return try_result

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """
    print("\n\n Starting board:\n\n")
    display(start_grid_values(diag_sudoku_grid))
    print("\n\n Solved board:\n\n")
    return search(grid_values(grid))

display(solve(diag_sudoku_grid))
