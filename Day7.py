import shlex
import numpy as np

def Day7_Part1(filename='Inputs/Day7_Inputs.txt'):
    """
    Calculates the minimum possible fuel spent to move every crab submarine to a common
    position, where the initial positions of each submarine are given in an input file,
    and each movement of a submarine by 1 position costs 1 fuel.

    Parameters
    ----------
    filename : str, optional
        Input file giving the initial positions of every crab submarine.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    minimum_fuel_spent : int
        The minimum possible fuel spent to get every submarine to a common position.

    """
    file = open(filename)
    positions_input = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            positions_input.append(line)
    file.close()
    
    positions, i = [], 0
    while i < len(positions_input[0][0]):
        curr_pos = ''
        while i < len(positions_input[0][0]) and positions_input[0][0][i] != ',':
            curr_pos += positions_input[0][0][i]
            i += 1
        positions.append(int(curr_pos))
        i += 1
    
    positions = np.array(positions)
    fuel_spent, end_points = [], np.arange(min(positions), max(positions)+1, 1)
    for end_point in end_points:
        fuel_spent.append(sum(abs(positions - end_point)))
    
    minimum_fuel_spent = min(fuel_spent)
    return minimum_fuel_spent

def cumulative_fuel(dx_max):
    """
    Calculates the total fuel used to move a crab submarine 'dx_max' positions given that
    each movement of a given submarine by 1 position costs 1 more fuel than the
    previous movement of that submarine, starting at 1 fuel for the first movement.

    Parameters
    ----------
    dx_max : int
        The total movement in position of a submarine.

    Returns
    -------
    fuel_used : int
        Total fuel used to move 'dx_max' positions.

    """
    fuel_used = [0]
    for i in range(1, dx_max):
        fuel_used.append(fuel_used[-1] + i)
    return fuel_used
    
def Day7_Part2(filename='Inputs/Day7_Inputs.txt'):
    """
    Calculates the minimum possible fuel spent to move every crab submarine to a common
    position, where the initial positions of each submarine are given in an input file,
    and each movement of a given submarine by 1 position costs 1 more fuel than the
    previous movement of that submarine, starting at 1 fuel for the first movement.

    Parameters
    ----------
    filename : str, optional
        Input file giving the initial positions of every crab submarine.
        The default is 'Inputs/Day7_Inputs.txt'.

    Returns
    -------
    minimum_fuel_spent : int
        The minimum possible fuel spent to get every submarine to a common position.

    """
    file = open(filename)
    positions_input = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            positions_input.append(line)
    file.close()
    
    positions, i = [], 0
    while i < len(positions_input[0][0]):
        curr_pos = ''
        while i < len(positions_input[0][0]) and positions_input[0][0][i] != ',':
            curr_pos += positions_input[0][0][i]
            i += 1
        positions.append(int(curr_pos))
        i += 1
    
    positions = np.array(positions)
    fuel_spent, end_points = [], np.arange(min(positions), max(positions)+1, 1)
    cum_fuel = cumulative_fuel(max(positions)+1 - min(positions))
    for end_point in end_points:
        fuel_used = 0
        for position in positions:
            fuel_used += cum_fuel[abs(position - end_point)]
        fuel_spent.append(fuel_used)
    
    minimum_fuel_spent = min(fuel_spent)
    return minimum_fuel_spent
