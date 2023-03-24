# Set up required destinations for each amphipod type, column numbers of corridor-only columns
# (no side room attached) and the costs of moving each amphipod type
DESTINATIONS = {'A': 2, 'B': 4, 'C': 6, 'D': 8}
INTERMEDIATES = [0, 1, 3, 5, 7, 9, 10]
COSTS = {'A': 1, 'B': 10, 'C': 100, 'D': 1000}

def get_input(input_file: str='Inputs/Day23_Inputs.txt', unfolded=False) -> tuple:
    """
    Parse an input file to extract the initial positions of a group of amphipods in burrow formed
    from a series of side rooms connected by a corridor.

    Parameters
    ----------
    input_file : str, optional
        Path to input file.
        The default is 'Inputs/Day23_Inputs.txt'.
    unfolded : bool, optional
        Whether or not to insert the following two additional layers of amphipods between the
        first and last in each side room:
              #D#C#B#A#\n
              #D#B#A#C#
        The default is False.

    Returns
    -------
    columns : list(list(str))
        List of the contents of each column in the burrow, in the form [[amphipod_1, amphipod_2,
        etc...], [amphipod_3], etc...], with the side rooms in columns [2, 4, 6, 8].
    places : dict(str: int)
        Dictionary giving the current column of each amphipod, in the form {amphipod: column_num}.
    not_at_dest : set(str)
        A set of all amphipods not already in their required destination.
    
    """
    # Set up empty outputs
    columns = [[], [], [], [], [], [], [], [], [], [], []]
    places = dict()
    # Track which types have been found once already, to inform what suffix to append
    found_once = set()
    # Parse input file
    with open(input_file) as f:
        lines = f.readlines()

    # Check contents of side room columns (c = column_num + 1 due to outer wall)
    for c in [3, 5, 7, 9]:
        # Check columns from the bottom, up
        for r in [3, 2]:
            # Add suffixes to amphipod types depending on order found, to distinguish different
            # amphipods of the same type
            suffix = '1' if lines[r][c] in found_once else '0'
            # Append to corresponding column_num
            columns[c-1].append(lines[r][c] + suffix)
            # Register this amphipod type as found at least once
            found_once.add(lines[r][c])
            # Add corresponding entry in places
            places[lines[r][c] + suffix] = c - 1

    # If extra layers should be inserted
    if unfolded:
        extra_layers = [['D2', 'D3'], ['B2', 'C2'], ['A2', 'B3'], ['C3', 'A3']]
        for i, c in enumerate([2, 4, 6, 8]):
            # Insert additional layers in each column
            columns[c] = columns[c][:1] + extra_layers[i] + columns[c][1:]
            # Add new amphipods to places
            for extra in extra_layers[i]:\
                places[extra] = c

    # Work out which amphipods are already in their required destinations
    not_at_dest = []
    # For each side room
    for c in [2, 4, 6, 8]:
        for r, amphipod in enumerate(columns[c]):
            # Find first amphipod from the bottom of the corridor is not in the right destination,
            # then this and all higher amphipods are not in the right destination yet
            if DESTINATIONS[amphipod[0]] != c:
                not_at_dest += columns[c][r:]
                break

    return columns, places, set(not_at_dest)

def draw_columns(columns: dict, room_size: int=2, show_amphipod_nums: bool=False) -> None:
    """
    Draw the current layout of the burrow, with the positions of each amphipod marked by their
    types, empty space as '.' and walls as '#'.

    Parameters
    ----------
    columns : list(list(str))
        List of the contents of each column in the burrow, in the form [[amphipod_1, amphipod_2,
        etc...], [amphipod_3], etc...], with the side rooms in columns [2, 4, 6, 8].
    room_size : int, optional
        The capacity of each side room.
        The default is 2.
    show_amphipod_nums : bool
        Whether to show the added numbers for each amphipod to distinguish between amphipods of
        the same type.

    Returns
    -------
    None.

    """
    print('#############' + '###########'*show_amphipod_nums)
    # Print corridor layer
    if show_amphipod_nums:
        print('#' + ''.join('..' if c not in INTERMEDIATES or not columns[c] else columns[c][0] \
                        for c in range(11)) + '#')
    else:
        print('#' + ''.join('.' if c not in INTERMEDIATES or not columns[c] else columns[c][0][0] \
                        for c in range(11)) + '#')
    # Print rooms, filling in the tops with empty space based on room size
    for r in range(room_size)[::-1]:
        if r == room_size - 1:
            pad = '###' + '##'*show_amphipod_nums
        else:
            pad = '  '*show_amphipod_nums + '  #'
        if show_amphipod_nums:
            print(pad + '##'.join('..' if len(columns[c]) - 1 < r else columns[c][r] \
                             for c in [2, 4, 6, 8]) + pad[::-1])
        else:
            print(pad + '#'.join('.' if len(columns[c]) - 1 < r else columns[c][r][0] \
                             for c in [2, 4, 6, 8]) + pad[::-1])
    print('  '*show_amphipod_nums + '  #########' + '#######'*show_amphipod_nums + '  \n')

def potential_moves(amphipod: str, columns: dict, places: dict) -> list:
    """
    Find every possible move of an amphipod from its current position.

    Movement Rules
    --------------
    Amphipods will never stop on the space immediately outside any room. They can move into that
    space so long as they immediately continue moving. (Specifically, this refers to the four open
    spaces in the hallway that are directly above an amphipod starting position.)

    Amphipods will never move from the hallway into a room unless that room is their destination
    room and that room contains no amphipods which do not also have that room as their own
    destination. If an amphipod's starting room is not its destination room, it can stay in that
    room until it leaves the room.

    Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into
    a room. (That is, once any amphipod starts moving, any other amphipods currently in the
    hallway are locked in place and will not move again until they can move fully into a room.)

    Parameters
    ----------
    amphipod : str
        The ID of the amphipod for which to find valid moves.
    columns : list(list(str))
        List of the contents of each column in the burrow, in the form [[amphipod_1, amphipod_2,
        etc...], [amphipod_3], etc...], with the side rooms in columns [2, 4, 6, 8].
    places : dict(str: int)
        Dictionary giving the current column of each amphipod, in the form {amphipod: column_num}.

    Returns
    -------
    moves : list(int)
        List of every column that the amphipod could move to the top of.

    """
    # If the amphipod is currently in the corridor, it can only move into its destination column,
    # and it can only do this if there are no other types of amphipod already in that corridor
    if places[amphipod] in INTERMEDIATES:
        # If all amphipods are not the required type, this amphipod cannot move anywhere
        if not all(c[0] == amphipod[0] for c in columns[DESTINATIONS[amphipod[0]]]):
            return []
        # Else check that no other amphipods are blocking this amphipod's journey to its
        # destination, depending on the direction
        # If moving to the right
        if places[amphipod] < DESTINATIONS[amphipod[0]]:
            for i in range(INTERMEDIATES.index(places[amphipod]) + 1,
                           INTERMEDIATES.index(DESTINATIONS[amphipod[0]] + 1)):
                # If there are any amphipods in intermediate corridor spots, this amphipod cannot
                # move
                if columns[INTERMEDIATES[i]]:
                    return []
        # If moving to the left
        else:
            for i in range(INTERMEDIATES.index(DESTINATIONS[amphipod[0]] + 1),
                           INTERMEDIATES.index(places[amphipod]))[::-1]:
                # If there are any amphipods in intermediate corridor spots, this amphipod cannot
                # move
                if columns[INTERMEDIATES[i]]:
                    return []
        # If it has passed every check, return the required destination column as the only possible
        # move
        return [DESTINATIONS[amphipod[0]]]
    # Else the amphipod is currently in a side room
    else:
        # It can only move if there are no other amphipods above it in the side room
        if not (curr_col := columns[places[amphipod]]).index(amphipod) == len(curr_col) - 1:
            return []
        moves = []
        # Else check all potential corridor positions, first to the left
        for i in range(INTERMEDIATES.index(places[amphipod] - 1) + 1)[::-1]:
            # If there are no other amphipods blocking the corridor in this direction, add each
            # point to potential moves
            if not columns[INTERMEDIATES[i]]:
                moves.append(INTERMEDIATES[i])
            # Else stop checking this directions, as it can move no further
            else:
                break
        # Then check to the right
        for i in range(INTERMEDIATES.index(places[amphipod] + 1), 7):
            if not columns[INTERMEDIATES[i]]:
                moves.append(INTERMEDIATES[i])
            else:
                break
        # If we can reach the corridor outside the destination of this amphipod, could move there
        if any(DESTINATIONS[amphipod[0]] + dx in moves for dx in [-1, 1]):
            # Check if there are any amphipods of another type in this side room already
            if all(c[0] == amphipod[0] for c in columns[DESTINATIONS[amphipod[0]]]):
                # If not, can move there, so return this as the only move as we always want to
                # move to the destination if we can
                return [DESTINATIONS[amphipod[0]]]
        return moves

def move_amphipod(amphipod: str, new_col: int, columns: dict, places: dict, not_at_dest: set,
                  energy_spent: int=0, room_size: int=2) -> tuple:
    """
    Move an amphipod from its current position to the top of a given column, updating the burrow
    column contents, amphipod positions and set of amphipods not at their required destination
    accordingly. It is assumed that the move is valid.

    Parameters
    ----------
    amphipod : str
        The ID of the amphipod to move.
    new_col : int
        The column to move the amphipod into.
    columns : list(list(str))
        List of the contents of each column in the burrow, in the form [[amphipod_1, amphipod_2,
        etc...], [amphipod_3], etc...], with the side rooms in columns [2, 4, 6, 8].
    places : dict(str: int)
        Dictionary giving the current column of each amphipod, in the form {amphipod: column_num}.
    not_at_dest : set(str)
        A set of all amphipods not already in their required destination.
    energy_spent : int, optional
        The energy spent before the move has occured.
        The default is 0.
    room_size : int, optional
        The capacity of each side room.
        The default is 2.

    Returns
    -------
    new_columns : list(list(str))
        Burrow column contents after the movement has occured.
    new_places : dict(str: int)
        Amphipod places after the movement has occured.
    new_not_at_dest : set(str)
        A set of all amphipods not already in their required destination after the movement has
        occured.

    """
    # Calculate the energy cost of moving through the corridor from the current column to the new
    new_energy_spent = energy_spent + abs(places[amphipod] - new_col)*COSTS[amphipod[0]]
    # If the amphipod does not start in the corridor, calculate the energy to move into the
    # corridor from the top of the current column
    if places[amphipod] not in INTERMEDIATES:
        new_energy_spent += (room_size - len(columns[places[amphipod]]) + 1)*COSTS[amphipod[0]]
    # If the new column is not in the corridor, calculate the energy to move to the top of the
    # corresponding side room from the corridor
    if new_col not in INTERMEDIATES:
        new_energy_spent += (room_size - len(columns[new_col]))*COSTS[amphipod[0]]
    # Build new columns dictionary with changed column for moving amphipod
    new_columns = [c[:-1] if i == places[amphipod] else  c + [amphipod] if i == new_col else \
                   c for i, c in enumerate(columns)]
    # Build new places dictionary with new place for moving amphipod
    new_places = {i: new_col if i == amphipod else p for i, p in places.items()}
    new_not_at_dest = not_at_dest.copy()
    # If it has moved to its required destination, remove current amphipod from not_at_dest
    if new_col == DESTINATIONS[amphipod[0]]:
        new_not_at_dest.discard(amphipod)

    return new_columns, new_places, new_not_at_dest, new_energy_spent

def find_cheapest_route(columns: dict, places: dict, not_at_dest: set, energy_spent: int=0,
                        curr_min: int=100000, room_size: int=2, route: list=[], min_route: list=[],
                        columns_cache: dict={}) -> tuple:
    """
    Performs a recursive depth-first search to find the method for organising a given layout of
    amphipods in a burrow into their required destinations which uses the least energy. The burrow
    consists of a corridor connecting 4 side rooms of a given length, and there are 4 types of
    amphipod: A, B, C, D; which need to reach the first, second, third and fourth side rooms
    respectively, with per-movement energy costs of 1, 10, 100 and 1000 respectively.

    Parameters
    ----------
    columns : list(list(str))
        List of the contents of each column in the burrow, in the form [[amphipod_1, amphipod_2,
        etc...], [amphipod_3], etc...], with the side rooms in columns [2, 4, 6, 8].
    places : dict(str: int)
        Dictionary giving the current column of each amphipod, in the form {amphipod: column_num}.
    not_at_dest : set(str)
        A set of all amphipods not already in their required destination.
    energy_spent : int, optional
        The energy spent so far in the current route.
        The default is 0.
    curr_min : int, optional
        The current minimum energy cost found in all routes tested so far.
        The default is 100000.
    room_size : int, optional
        The capacity of each side room.
        The default is 2.
    route : list(tuple(str, int)), optional
        The route taken so far in the current branch, with each move listed in the form
        (amphipod_that_moved, column_moved_to).
        The default is [].
    min_route : list(tuple(str, int)), optional
        The route requiring the least energy found so far, with each move listed in the form
        (amphipod_that_moved, column_moved_to).
        The default is [].
    columns_cache : dict(tuple(tuple(str)): int) optional
        A cache of the minimum cost to reach every burrow layout found so far, in the form
        {columns: min_cost}. Columns are converted from lists to strings to allow for hashing.
        The default is {}.

    Returns
    -------
    curr_min : int
        The minimum possible energy cost for reorganising the amphipods in the required way.
    min_route : list(tuple(str, int))
        The route correpsonding to the minimum possible energy cost, with each move listed in the
        form (amphipod_that_moved, column_moved_to).

    """
    # Group relevant parameters for tidiness
    params = (columns, places, not_at_dest, energy_spent)

    # If there are no amphipods still not at their required destinations, we are finished
    if not not_at_dest:
        # If the current energy spend is below the minimum found so far, return this
        if energy_spent < curr_min:
            return energy_spent, route
        # Else return the current minimum
        return curr_min, min_route

    # Find absolute minimum possible energy cost from current point, assuming each amphipod can
    # move straight to its destination. If this doesn't beat the current minimum, no point
    # continuing
    abs_min = energy_spent
    # Count amphipods of given type which aren't at destination yet, to determine the position in
    # their side room they must reach
    counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0}
    # For each amphipod not at its destination yet
    for a in not_at_dest:
        # Calculate cost to move into corridor (if not there already) + cost to move to destination
        # column + cost to move to top of corresponding side room
        abs_min += ((places[a] not in INTERMEDIATES)*(room_size - columns[places[a]].index(a)) \
            + abs(DESTINATIONS[a[0]] - places[a]) + counts[a[0]] + 1)*COSTS[a[0]]
        counts[a[0]] += 1
    # If this best case scenario doesn't beat current minimum, stop here and return curr_min
    if abs_min >= curr_min:
        return curr_min, min_route

    # Find all possible moves for every amphipod not at its destination yet
    all_pot_moves = {a: moves for a in places \
                     if a in not_at_dest and (moves := potential_moves(a, columns, places))}

    # Find all amphipods which are able to move to their destinations
    can_move_to_dest = [a for a, m in all_pot_moves.items() if DESTINATIONS[a[0]] in m]

    # If there are any, only consider doing this, as this is always the most efficient choice
    if can_move_to_dest:
        # Just take the first amphipod which can move straight to its destination, as the order
        # if there are multiple is irrelevant
        new_params = move_amphipod(can_move_to_dest[0], DESTINATIONS[can_move_to_dest[0][0]],
                                   *params, room_size)

        # Update cache for this burrow layout, if this layout isn't already cached or if this
        # current cost beats the cached one
        if (tuple_columns := tuple(tuple(c) for c in new_params[0])) not in columns_cache \
            or new_params[3] < columns_cache[tuple_columns]:
            columns_cache[tuple_columns] = new_params[3]
        # Else stop here, as we already found a cheaper way of reaching this point
        else:
            return curr_min, min_route

        # Find cheapest possible route from this point and return
        return find_cheapest_route(*new_params, curr_min, room_size,
                                   route + [(can_move_to_dest[0],
                                             DESTINATIONS[can_move_to_dest[0][0]])],
                                   min_route, columns_cache)

    # Else if there are no amphipods which can move straight to their destinations
    else:
        # Go through each possible move for each amphipod
        for amphipod, pot_moves in all_pot_moves.items():

            for move in pot_moves:
                # Perform the movement
                new_params = move_amphipod(amphipod, move, *params, room_size)

                # Update cache for this burrow layout, if this layout isn't already cached or if
                # this current cost beats the cached one
                if (tuple_columns := tuple(tuple(c) for c in new_params[0])) not in columns_cache \
                    or new_params[3] < columns_cache[tuple_columns]:
                    columns_cache[tuple_columns] = new_params[3]
                # Else stop here, as we already found a cheaper way of reaching this point
                else:
                    continue

                # Find cheapest possible route from this point and assign to curr_min, which will
                # not change if no cheaper route is found
                curr_min, min_route = find_cheapest_route(*new_params, curr_min, room_size,
                                                          route + [(amphipod, move)], min_route,
                                                          columns_cache)

    return curr_min, min_route

from time import perf_counter

def time_function(func):
    """
    Decorator function to measure runtime of given function.

    Parameters
    ----------
    func : func
        Function to time.

    """
    def wrapper(*args, **kwargs):
        t1 = perf_counter()
        out = func(*args, **kwargs)
        t2 = perf_counter() - t1
        print(f'{func.__name__} ran in {t2:.7f} seconds')
        return out
    return wrapper

@time_function
def Day23_Part1(input_file: str='Inputs/Day23_Inputs.txt') -> tuple:
    """
    Uses a recursive depth-first search to find the most energy efficient way to reorganise a group
    of amphipods in a burrow into their required destinations. Four types of amphipods live there:
    Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a
    hallway and four side rooms. The side rooms are initially full of amphipods, and the hallway
    is initially empty. Amphipod types A, B, C and D need to reach the first, second, third and
    fourth side rooms respectively, with per-movement energy costs of 1, 10, 100 and 1000
    respectively. Each side room holds 2 amphipods. 

    Movement Rules
    --------------
    Amphipods will never stop on the space immediately outside any room. They can move into that
    space so long as they immediately continue moving. (Specifically, this refers to the four open
    spaces in the hallway that are directly above an amphipod starting position.)

    Amphipods will never move from the hallway into a room unless that room is their destination
    room and that room contains no amphipods which do not also have that room as their own
    destination. If an amphipod's starting room is not its destination room, it can stay in that
    room until it leaves the room.

    Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into
    a room. (That is, once any amphipod starts moving, any other amphipods currently in the
    hallway are locked in place and will not move again until they can move fully into a room.)

    Parameters
    ----------
    input_file : str, optional
        Inupt file giving the initial layout of the amphipods in the burrow.
        The default is 'Inputs/Day23_Inputs.txt'.

    Returns
    -------
    min_energy : int
        The minimum possible energy cost for reorganising the amphipods in the required way.
    min_route : list(tuple(str, int))
        The route correpsonding to the minimum possible energy cost, with each move listed in the
        form (amphipod_that_moved, column_moved_to).

    """
    # Parse input file to extract amphipod position information, including which are not already
    # in their destinations
    columns, places, not_at_dest = get_input(input_file)

    # Draw the initial burrow layout
    draw_columns(columns, 2, True)

    # Perform a recursive depth-first search through potential routes to find the minimum possible
    # energy cost, and corresponding route
    min_energy, min_route = find_cheapest_route(columns, places, not_at_dest, 0, 100000,
                                                2, [], [], {})

    return min_energy, min_route

@time_function
def Day23_Part2(input_file: str='Inputs/Day23_Inputs.txt') -> tuple:
    """
    Uses a recursive depth-first search to find the most energy efficient way to reorganise a group
    of amphipods in a burrow into their required destinations. Four types of amphipods live there:
    Amber (A), Bronze (B), Copper (C), and Desert (D). They live in a burrow that consists of a
    hallway and four side rooms. The side rooms are initially full of amphipods, and the hallway
    is initially empty. Amphipod types A, B, C and D need to reach the first, second, third and
    fourth side rooms respectively, with per-movement energy costs of 1, 10, 100 and 1000
    respectively. However, now each side room holds 4 amphipods, and the following additional two
    layers of amphipods are inserted between the original first and second layers in the initial
    layout:
        #D#C#B#A#\n
        #D#B#A#C#

    Movement Rules
    --------------
    Amphipods will never stop on the space immediately outside any room. They can move into that
    space so long as they immediately continue moving. (Specifically, this refers to the four open
    spaces in the hallway that are directly above an amphipod starting position.)

    Amphipods will never move from the hallway into a room unless that room is their destination
    room and that room contains no amphipods which do not also have that room as their own
    destination. If an amphipod's starting room is not its destination room, it can stay in that
    room until it leaves the room.

    Once an amphipod stops moving in the hallway, it will stay in that spot until it can move into
    a room. (That is, once any amphipod starts moving, any other amphipods currently in the
    hallway are locked in place and will not move again until they can move fully into a room.)

    Parameters
    ----------
    input_file : str, optional
        Inupt file giving the initial layout of the amphipods in the burrow.
        The default is 'Inputs/Day23_Inputs.txt'.

    Returns
    -------
    min_energy : int
        The minimum possible energy cost for reorganising the amphipods in the required way.
    min_route : list(tuple(str, int))
        The route correpsonding to the minimum possible energy cost, with each move listed in the
        form (amphipod_that_moved, column_moved_to).

    """
    # Parse input file to extract amphipod position information, including which are not already
    # in their destinations
    columns, places, not_at_dest = get_input(input_file, unfolded=True)

    # Draw the initial burrow layout, now with 4 amphipods per side room
    draw_columns(columns, 4, True)

    # Perform a recursive depth-first search through potential routes to find the minimum possible
    # energy cost, and corresponding route
    min_energy, min_route = find_cheapest_route(columns, places, not_at_dest, 0, 100000,
                                                4, [], [], {})

    return min_energy, min_route
