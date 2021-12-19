import shlex

def Day17_Part1(filename='Inputs/Day17_Inputs.txt'):
    """
    Calculates the maximum y position that can be reached by a projectile starting at
    [0, 0] such that it passes through a target area specified in an input file. The
    projectile moves in distinct steps according to a velocity [vx, vy], where in each
    step the x and y coordinates are incremented by vx and vy respectively and then vx
    moves 1 unit closer to 0 and vy decreases by 1.

    Parameters
    ----------
    filename : str, optional
        Input file giving the target area.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    max_y : int
        Maximum y position that can be reached by the projectile while still passing
        through the target area.

    """
    file = open(filename)
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data = line
    file.close()
    x_data = data[2].split('..')
    y_data = data[3].split('..')
    limits = [[int(x_data[0][2:]), int(x_data[1][:-1])], [int(y_data[0][2:]), int(y_data[1])]]
    
    success = []
    for v_y in range((-1*min(limits[1]))+1):
        y = 0
        v_ynow = -1*(v_y + 1)
        while y > limits[1][1]:
            y += v_ynow
            v_ynow -= 1
        if y >= limits[1][0]:
            success.append(v_y)            
    
    max_y = sum(i for i in range(success[-1]+1))
    return max_y
                    
    
def steps(limits, curr_v, curr_pos=[0, 0]):
    """
    Calculates the coordinates of a projectile starting at curr_pos with an initial
    velocity of curr_v for a number of steps until the projectile has entered or passed
    the target area specified by the input limits. The projectile moves in distinct steps
    according to a velocity [vx, vy], where in each step the x and y coordinates are
    incremented by vx and vy respectively and then vx moves 1 unit closer to 0 and vy
    decreases by 1.

    Parameters
    ----------
    limits : list of lists of ints
        Limits of the target area in the form [[xmin, xmax], [ymin, ymax]].
    curr_v : list of ints
        Initial velocity [vx, vy] of the projectile.
    curr_pos : TYPE, optional
        Initial position [x, y] of the projectile.
        The default is [0, 0].

    Returns
    -------
    positions : list of lists of ints
        List of the coordinates of the projectile at every step calculated.

    """
    positions = [1*curr_pos]
    while curr_pos[0] < limits[0][0] or curr_pos[1] > limits[1][1]:
        curr_pos[0] += curr_v[0]
        curr_pos[1] += curr_v[1]
        curr_v[0] += 1*(curr_v[0] < 0) + 0*(curr_v[0] == 0) - 1*(curr_v[0] > 0)
        curr_v[1] += -1
        positions.append(1*curr_pos)
        
    return positions

def draw_steps(limits, vinitial, curr_pos=[0, 0]):
    """
    Draws the path of a projectile starting at curr_pos with an initial velocity of
    vinitial for a number of steps until the projectile has entered or passed the target
    area specified by the input limits. The projectile moves in distinct steps according
    to a velocity [vx, vy], where in each step the x and y coordinates are incremented by
    vx and vy respectively and then vx moves 1 unit closer to 0 and vy decreases by 1.

    Parameters
    ----------
    limits : list of lists of ints
        Limits of the target area in the form [[xmin, xmax], [ymin, ymax]].
    curr_v : list of ints
        Initial velocity [vx, vy] of the projectile.
    curr_pos : TYPE, optional
        Initial position [x, y] of the projectile.
        The default is [0, 0].

    """
    positions = steps(limits, 1*vinitial, 1*curr_pos)
    x_pos = [pos[0] for pos in positions] + limits[0]
    y_pos = [pos[1] for pos in positions] + limits[1]
    xmin, xmax = min(x_pos), max(x_pos)
    ymin, ymax = min(y_pos), max(y_pos)
    for y in range(ymin, ymax+1)[::-1]:
        out = ''
        for x in range(xmin, xmax+1):
            try:
                if positions.index([x, y]) == 0:
                    out += 'S'
                else:
                    out += '#'
            except:
                if x >= limits[0][0] and x <= limits[0][1] and y >= limits[1][0] and y <= limits[1][1]:
                    out += 'T'
                else:
                    out += '.'
        print(out)

def Day17_Part2(filename='Inputs/Day17_Inputs.txt'):
    """
    Calculates the total number of different initial velocities a projectile starting at
    [0, 0] can have such that it passes through a target area specified in an input file.
    The projectile moves in distinct steps according to a velocity [vx, vy], where in each
    step the x and y coordinates are incremented by vx and vy respectively and then vx
    moves 1 unit closer to 0 and vy decreases by 1.

    Parameters
    ----------
    filename : str, optional
        Input file giving the target area.
        The default is 'Inputs/Day17_Inputs.txt'.

    Returns
    -------
    success_num : int
        Total number of different initial velocities the projectile can have and still
        pass through the target area.

    """
    file = open(filename)
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data = line
    file.close()
    x_data = data[2].split('..')
    y_data = data[3].split('..')
    limits = [[int(x_data[0][2:]), int(x_data[1][:-1])], [int(y_data[0][2:]), int(y_data[1])]]
    
    v_xmax = limits[0][1]
    v_ymin = limits[1][0]
    
    v_xmin = 1
    while sum(i for i in range(v_xmin+1)) < limits[0][0]:
        v_xmin += 1
    
    success = []
    for v_y in range((-1*min(limits[1]))+1):
        y = 0
        v_ynow = -1*(v_y + 1)
        while y > limits[1][1]:
            y += v_ynow
            v_ynow -= 1
        if y >= limits[1][0]:
            v_ymax = v_y
            
    for v_y in range(v_ymin, v_ymax+1):
        for v_x in range(v_xmin, v_xmax+1):
            final = steps(limits, [v_x, v_y], [0, 0])[-1]
            if final[0] <= limits[0][1] and final[1] >= limits[1][0]:
                success.append([v_x, v_y])

    success_num = len(success)
    return success_num