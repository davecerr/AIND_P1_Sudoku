
# coding: utf-8

# In[6]:

# %load solution.py

from utils import *
import itertools

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC','DEF','GHI') for cs in ('123','456','789')]
unitlist = row_units + column_units + square_units 

# TODO: Update the unit list to add the new diagonal units
diagonal1 = [[a[0]+a[1] for a in zip(rows,cols)]]
diagonal2 = [[a[0]+a[1] for a in zip(rows,cols[::-1])]]
diagonal_units = diagonal1 + diagonal2
unitlist = unitlist + diagonal_units

units = dict((s, [u for u in unitlist if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s],[]))-set([s])) for s in boxes)


def naked_twins(values):
    """Eliminate values using the naked twins strategy.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the naked twins eliminated from peers

    Notes
    -----
    Your solution can either process all pairs of naked twins from the input once,
    or it can continue processing pairs of naked twins until there are no such
    pairs remaining -- the project assistant test suite will accept either
    convention. However, it will not accept code that does not process all pairs
    of naked twins from the original input. (For example, if you start processing
    pairs of twins and eliminate another pair of twins before the second pair
    is processed then your code will fail the PA test suite.)

    The first convention is preferred for consistency with the other strategies,
    and because it is simpler (since the reduce_puzzle function already calls this
    strategy repeatedly).
    """
    # TODO: Implement this function!
    
    
    for unit in unitlist:
        # Identify potential remaining twins as boxes with two possibilities
        two_element_boxes = [box for box in unit if len(values[box]) == 2]
    
        # Create a list of pairings of all possible twins
        potential_twins = [list(pairing) for pairing in itertools.combinations(two_element_boxes, 2)]
    
        # For each potential pair of naked twins, remove these values from all peers 
        for twin in potential_twins:
            box1 = twin[0]
            box2 = twin[1]
            # Identify if they are genuinely naked twins
            if values[box1] == values[box2]:
                for box in unit:
                    if box != box1 and box != box2:
                        # Since offending digits may not be consecutive, we should address them individually rather than as a pair
                        for box_value in values[box1]:
                            assign_value(values, box, values[box].replace(box_value, ''))
                     
                        
    return values
    


def eliminate(values):
    """Apply the eliminate strategy to a Sudoku puzzle

    The eliminate strategy says that if a box has a value assigned, then none
    of the peers of that box can have the same value.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with the assigned values eliminated from peers
    """
    # TODO: Copy your code from the classroom to complete this function
    
    single_elements = [box for box in values.keys() if len(values[box]) == 1]
    for s in single_elements:
        for p in peers[s]:
            assign_value(values, p, values[p].replace(values[s], ''))
    return values


def only_choice(values):
    """Apply the only choice strategy to a Sudoku puzzle

    The only choice strategy says that if only one box in a unit allows a certain
    digit, then that box must be assigned that digit.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict
        The values dictionary with all single-valued boxes assigned

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    """
    # TODO: Copy your code from the classroom to complete this function
    
    for unit in unitlist:
        for digit in '123456789':
            # Below we use in rather than == to build a list of boxes for which that digit is an option 
            box_occurences = [box for box in unit if digit in values[box]]
            if len(box_occurences) == 1:
                assign_value(values, box_occurences[0], digit)
    return values


def reduce_puzzle(values):
    """Reduce a Sudoku puzzle by repeatedly applying all constraint strategies

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary after continued application of the constraint strategies
        no longer produces any changes, or False if the puzzle is unsolvable 
    """
    # TODO: Copy your code from the classroom and modify it to complete this function
    
    stalled = False
    while not stalled:
        # Check how many boxes have a determined value
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        # Use the Eliminate Strategy
        eliminate(values)

        # Use the Naked Twins Strategy
        naked_twins(values)
        
        # Use the Only Choice Strategy
        only_choice(values)
        
        # Check how many boxes have a determined value, to compare
        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        # If no new values were added, stop the loop.
        stalled = solved_values_before == solved_values_after
        # Sanity check, return False if there is a box with zero available values:
        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values



def search(values):
    """Apply depth first search to solve Sudoku puzzles in order to solve puzzles
    that cannot be solved by repeated reduction alone.

    Parameters
    ----------
    values(dict)
        a dictionary of the form {'box_name': '123456789', ...}

    Returns
    -------
    dict or False
        The values dictionary with all boxes assigned or False

    Notes
    -----
    You should be able to complete this function by copying your code from the classroom
    and extending it to call the naked twins strategy.
    """
    # TODO: Copy your code from the classroom to complete this function
    
    # First, reduce the puzzle using the previous function
    values = reduce_puzzle(values)
    if values is False:
        return False ## Failed earlier
    if all(len(values[s]) == 1 for s in boxes): 
        return values ## Solved!
    # Choose one of the unfilled squares with the fewest possibilities
    n,s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)
    
    # Now use recursion to solve each one of the resulting sudokus, and if one returns a value (not False), return that answer!
    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt


def solve(grid):
    """Find the solution to a Sudoku puzzle using search and constraint propagation

    Parameters
    ----------
    grid(string)
        a string representing a sudoku grid.
        
        Ex. '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'

    Returns
    -------
    dict or False
        The dictionary representation of the final sudoku grid or False if no solution exists.
    """
    values = grid2values(grid)
    values = search(values)
    return values


if __name__ == "__main__":
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    
    # Further testing from http://www.conceptispuzzles.com/index.aspx?uri=puzzle/sudoku/diagonal
    easy_diag_sudoku_grid = '.45...63.2...1...59..8.5..7..9...3...3.....7...8...5..8..5.3..15...2...3.26...95.'
    med_diag_sudoku_grid = '.5.......6.3..24...7.1....38.4.....7.........3.....2.97....1.2...96..7.1.......4.'
    hard_diag_sudoku_grid = '...1.6...3...5...1....7....4...9...5.157.239.7...3...2....8....6...1...7...9.7...'

    
    puzzle = med_diag_sudoku_grid
    
    display(grid2values(puzzle))
    result = solve(puzzle)
    display(result)

    try:
        import PySudoku
        PySudoku.play(grid2values(puzzle), result, history)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')


# In[ ]:



