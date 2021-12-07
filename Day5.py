import shlex
import numpy as np

def Day5_Part1(filename='Inputs/Day5_Inputs.txt'):
    """
    Determine the number of dangerous points in a field of hydrothermal vents, where
    dangerous points are defined as points where at least 2 lines of vents intersect.
    The lines of vents are defined by start and end coordinates (inclusive) which are
    provided in an input file. Only horizontal (y1 == y2) and vertical (x1 == x2) lines
    are considered here.

    Parameters
    ----------
    filename : str, optional
        Input file containing the start and end coordinates of the lines of vents.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    dangerous : int
        The number of dangerous points, where at least 2 lines of vents intersect.

    """
    file = open(filename)
    coords = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            coords.append(line)
    file.close()
    
    formatted_coords = []
    for line in coords:
        i = line[0].find(',')
        start = [int(line[0][:i]), int(line[0][i+1:])]
        j = line[2].find(',')
        end = [int(line[2][:j]), int(line[2][j+1:])]
        formatted_coords.append([start, end])
    
    x_coords, y_coords = [], []
    for coords in formatted_coords:
        x_coords.append(coords[0][0])
        x_coords.append(coords[1][0])
        y_coords.append(coords[0][1])
        y_coords.append(coords[1][1])
    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)
    
    whole_map = []
    for y in range(ymin, ymax+1):
        whole_map.append(np.zeros((xmax-xmin)+1))
            
    for n, coords in enumerate(formatted_coords):
        x1, x2 = coords[0][0], coords[1][0]
        y1, y2 = coords[0][1], coords[1][1]
        if x1 == x2 or y1 == y2:
            all_points = []
            if x1 != x2:
                gradient = (y2 - y1)/(x2 - x1)
                intercept = y1 - (gradient*x1)
                for x in np.arange(x1, x2+(-1)**(x1>x2), (-1)**(x1>x2)):
                    all_points.append([int(x), int((gradient*x)+intercept)])
            else:
                for y in np.arange(y1, y2+(-1)**(y1>y2), (-1)**(y1>y2)):
                    all_points.append([int(x1), int(y)])
            for point in all_points:
                whole_map[point[1]-ymin][point[0]-xmin] += 1
                
    dangerous = 0
    for y_line in whole_map:
        dangerous += sum(x >= 2 for x in y_line)
        
    return dangerous

def Day5_Part2(filename='Inputs/Day5_Inputs.txt'):
    """
    Determine the number of dangerous points in a field of hydrothermal vents, where
    dangerous points are defined as points where at least 2 lines of vents intersect.
    The lines of vents are defined by start and end coordinates (inclusive) which are
    provided in an input file. Horizontal (y1 == y2), vertical (x1 == x2) and diagonal
    (at 45 degrees) lines are all considered here.

    Parameters
    ----------
    filename : str, optional
        Input file containing the start and end coordinates of the lines of vents.
        The default is 'Inputs/Day5_Inputs.txt'.

    Returns
    -------
    dangerous : int
        The number of dangerous points, where at least 2 lines of vents intersect.

    """
    file = open(filename)
    coords = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            coords.append(line)
    file.close()
    
    formatted_coords = []
    for line in coords:
        i = line[0].find(',')
        start = [int(line[0][:i]), int(line[0][i+1:])]
        j = line[2].find(',')
        end = [int(line[2][:j]), int(line[2][j+1:])]
        formatted_coords.append([start, end])
    
    x_coords, y_coords = [], []
    for coords in formatted_coords:
        x_coords.append(coords[0][0])
        x_coords.append(coords[1][0])
        y_coords.append(coords[0][1])
        y_coords.append(coords[1][1])
    xmin, xmax = min(x_coords), max(x_coords)
    ymin, ymax = min(y_coords), max(y_coords)
    
    whole_map = []
    for y in range(ymin, ymax+1):
        whole_map.append(np.zeros((xmax-xmin)+1))
            
    for n, coords in enumerate(formatted_coords):
        x1, x2 = coords[0][0], coords[1][0]
        y1, y2 = coords[0][1], coords[1][1]
        all_points = []
        if x1 != x2:
            gradient = (y2 - y1)/(x2 - x1)
            intercept = y1 - (gradient*x1)
            for x in np.arange(x1, x2+(-1)**(x1>x2), (-1)**(x1>x2)):
                all_points.append([int(x), int((gradient*x)+intercept)])
        else:
            for y in np.arange(y1, y2+(-1)**(y1>y2), (-1)**(y1>y2)):
                all_points.append([int(x1), int(y)])
        for point in all_points:
            whole_map[point[1]-ymin][point[0]-xmin] += 1
                
    dangerous = 0
    for y_line in whole_map:
        dangerous += sum(x >= 2 for x in y_line)
        
    return dangerous
