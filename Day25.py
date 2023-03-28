def get_input(input_file: str='Inputs/Day25_Inputs.txt') -> tuple:
    """
    Parse an input file to extract the coordinates of sea cucumbers in a 2D grid, with one set
    facing east represented as '>', and one set facing south represented as 'v'.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the grid layout.
        The default is 'Inputs/Day25_Inputs.txt'.

    Returns
    -------
    east_facing : set(tuple(int))
        Set of coordinates of east-facing sea cucumbers.
    south_facing : set(tuple(int))
        Set of coordinates of south-facing sea cucumbers.
    cucumbers : set(tuple(int))
        Set of coordinates of all sea cucumbers.
    grid_dim : tuple(int)
        Dimensions of the full grid in the form (height, width).

    """
    # Parse input file
    with open(input_file) as f:
        cucumbers = [line.strip() for line in f.readlines()]
        # Find full grid size
        grid_dim = (len(cucumbers), len(cucumbers[0]))
    # Get east facing cucumbers
    east_facing = {(r, c) for r, row in enumerate(cucumbers) for c, cucumber in enumerate(row) \
                   if cucumber == '>'}
    # Get south facing cucumbers
    south_facing = {(r, c) for r, row in enumerate(cucumbers) for c, cucumber in enumerate(row) \
                    if cucumber == 'v'}
    # Combine both sets to get all cucumbers
    cucumbers = east_facing.union(south_facing)
    return east_facing, south_facing, cucumbers, grid_dim

def move_cucmbers(east_facing: set, south_facing: set, cucumbers: set, grid_dim: tuple) -> tuple:
    """
    Performs a single movement of a set of sea cucumbers in a 2D grid, with some facing east and
    some facing south. Cucumbers can only move if the space in front of them is not currently
    occupied by another cucumber. All east-facing cucumbers attempt to move simulataneously first,
    followed by all south-facing cucumbers. If a cucumber moves of the edge of the grid, they wrap
    around to the other side, facing in the same direction.

    Parameters
    ----------
    east_facing : set(tuple(int))
        Set of coordinates of east-facing sea cucumbers.
    south_facing : set(tuple(int))
        Set of coordinates of south-facing sea cucumbers.
    cucumbers : set(tuple(int))
        Set of coordinates of all sea cucumbers.
    grid_dim : tuple(int)
        Dimensions of the full grid in the form (height, width).

    Returns
    -------
    east_facing : set(tuple(int))
        Set of coordinates of east-facing sea cucumbers after the movement.
    south_facing : set(tuple(int))
        Set of coordinates of south-facing sea cucumbers after the movement.
    cucumbers : set(tuple(int))
        Set of coordinates of all sea cucumbers after the movement.
    changed : bool
        Whether any of the cucumber positions changed during this movement.

    """
    # Construct new set of east-facing cucumbers, checking if next space is occupied or not
    new_east_facing = {c_next if (c_next := (c[0], (c[1]+1)%grid_dim[1])) not in cucumbers else c \
                       for c in east_facing}
    # Update set of all cucumber positions with new east-facing cucumber positions
    cucumbers = new_east_facing.union(south_facing)
    # Construct new set of south-facing cucumbers, checking if next space is occupied or not
    new_south_facing = {c_next if (c_next := ((c[0]+1)%grid_dim[0], c[1])) not in cucumbers else c \
                        for c in south_facing}
    # Update set of all cucumber positions with new south-facing cucumber positions
    cucumbers = new_south_facing.union(new_east_facing)
    # If either set has changed, set changed to True, else False
    changed = not (new_east_facing == east_facing and new_south_facing == south_facing)
    return new_east_facing, new_south_facing, cucumbers, changed

def draw_cucumbers(east_facing: set, south_facing: set, grid_dim: tuple) -> None:
    """
    Draw the full grid layout, with east-facing cucumbers represented as '>', south-facing
    cucumbers represented as 'v' and empty space represented as '.'.

    Parameters
    ----------
    east_facing : set(tuple(int))
        Set of coordinates of east-facing sea cucumbers.
    south_facing : set(tuple(int))
        Set of coordinates of south-facing sea cucumbers.
    grid_dim : tuple(int)
        Dimensions of the full grid in the form (height, width).

    Returns
    -------
    None.

    """
    # Draw each row, checking for cucumbers at each point
    for r in range(grid_dim[0]):
        print(''.join('>' if (r, c) in east_facing else 'v' if (r, c) in south_facing else '.' \
                      for c in range(grid_dim[1])))
    print()

def Day25_Part1(input_file: str='Inputs/Day25_Inputs.txt') -> int:
    """
    Finds the number of movement steps a set of sea cucumbers laid out in a 2D grid can take,
    before no cucumbers are able to move anymore. Some of the sea cucumbers are facing east and
    some are facing south. Cucumbers can only move if the space in front of them is not currently
    occupied by another cucumber. All east-facing cucumbers attempt to move simulataneously first,
    followed by all south-facing cucumbers. If a cucumber moves of the edge of the grid, they wrap
    around to the other side, facing in the same direction.

    Parameters
    ----------
    input_file : str, optional
        Input file giving the initial grid layout.
        The default is 'Inputs/Day25_Inputs.txt'.

    Returns
    -------
    steps : int
        DESCRIPTION.

    """
    # Parse input file to extract cucumber positions
    east_facing, south_facing, cucumbers, grid_dim = get_input(input_file)
    # Track number of steps and if the grid changes in a step
    steps, changed = 0, True
    # While the grid changed in the last step
    while changed:
        # Perform a single (attempted) movement of every cucumber
        east_facing, south_facing, cucumbers, changed = move_cucmbers(east_facing, south_facing,
                                                                      cucumbers, grid_dim)
        steps += 1

    return steps
