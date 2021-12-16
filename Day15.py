import shlex
import numpy as np

class Coordinates:
    """
    Class to define a pair of coordinates (x, y)
    """
    def __init__(self, pos):
        """
        Initialise the class with one parameter.

        Parameters
        ----------
        pos : list of int
            Coordinates in the form [x, y].
            
        Returns
        -------
        None.

        """
        self.x = pos[0]
        self.y = pos[1]
    
    def __repr__(self):
        """
        Return the representation of a Coordinates object.

        Returns
        -------
        str
            Representation.

        """
        return f'{self.__class__.__name__}({self.x}, {self.y})'
    
    def __hash__(self):
        """
        Override the hash function for a Coordinates object.

        Returns
        -------
        int
            The hash of the Coordinates.

        """
        return hash((self.x, self.y))

    def __eq__(self, other):
        """
        Overrides the == operator for a Coordinates object.

        Parameters
        ----------
        other : Coordinates
            The Coordinates object to which we are comparing.

        Returns
        -------
        bool
            Whether the two Coordinates are equivalent or not.

        """
        return (self.x, self.y) == (other.x, other.y)

    def __ne__(self, other):
        """
        Overrides the != operator for a Coordinates object.

        Parameters
        ----------
        other : Coordinates
            The Coordinates object to which we are comparing.

        Returns
        -------
        bool
            Whether the two Coordinates are different or not.

        """
        return not(self == other)
    
    def __pos__(self):
        """
        Return a copy of the Coordinates.
        """
        return self.__class__([self.x, self.y])
    
def Day15_Part1(filename='Inputs/Day15_Inputs.txt'):
    """
    Uses Dijkstra's algorithm to calculate the minimum total risk of any path from the top
    left to the bottom right of a square grid of points, where each point has a risk level
    as given in an input file.

    Parameters
    ----------
    filename : str, optional
        Input file giving the risk level of every point.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    min_risk : int
        The minimum total risk of any path from the top left to the bottom right of the
        grid.

    """
    file = open(filename)
    unvisited, points, tentatives, line_num = {}, [], [], 0
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            for n, risk in enumerate(line[0]):
                unvisited[Coordinates([n, line_num])] = [int(risk), 9e99]
                xmax = n
            line_num += 1
    ymax = line_num - 1
    file.close()
    
    points = [point for point in unvisited]
    tentatives = [9e99 for point in unvisited]
    
    current = Coordinates([0, 0])
    unvisited[current][1] = 0
    tentatives[points.index(current)] = 0
    while current != Coordinates([xmax, ymax]):
        for neighbour in adjacent(current):
            try:
                dist_curr = unvisited[current][1] + unvisited[neighbour][0]
                if dist_curr < unvisited[neighbour][1]:
                    unvisited[neighbour][1] = dist_curr
                    tentatives[points.index(neighbour)] = dist_curr
            except:
                continue
            
        unvisited.pop(current)
        index = points.index(current)
        points.pop(index)
        tentatives.pop(index)
        current = +points[np.argmin(tentatives)]
    
    min_risk = unvisited[current][1]
    return min_risk
    
    
def adjacent(point):
    """
    Calculates the four Coordinates immediately adjacent to a given pair of Coordinates.

    Parameters
    ----------
    point : Coordinates
        The initial Coordinates.

    Returns
    -------
    next_points : list of Coordinates
        The four adjacent Coordinates.

    """
    x, y = point.x, point.y
    next_points = []
    for x_next in [x-1, x+1]:
        next_points.append(Coordinates([x_next, y]))
    for y_next in [y-1, y+1]:
        next_points.append(Coordinates([x, y_next]))
    return next_points

def Day15_Part2(filename='Inputs/Day15_Inputs.txt'):
    """
    Uses Dijkstra's algorithm to calculate the minimum total risk of any path from the top
    left to the bottom right of an extended square grid of points. The extended grid is
    generated from an initial grid where each point has a risk level as given in an input
    file.
    The initial grid forms the top left tile in a 5x5 tile area that forms the full map,
    with the original map tile repeating to the right and downward. Each time the tile
    repeats to the right or downward, all of its risk levels are 1 higher than the tile
    immediately up or left of it. However, risk levels above 9 wrap back around to 1.

    Parameters
    ----------
    filename : str, optional
        Input file giving the risk level of every point in the initial grid.
        The default is 'Inputs/Day15_Inputs.txt'.

    Returns
    -------
    min_risk : int
        The minimum total risk of any path from the top left to the bottom right of the
        extended grid.

    """
    file = open(filename)
    unvisited, points, tentatives, line_num = {}, [], [], 0
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            for n, risk in enumerate(line[0]):
                unvisited[Coordinates([n, line_num])] = [int(risk), 9e99]
                xmax = n
            line_num += 1
    ymax = line_num - 1
    file.close()
    
    unvisited = extend_grid(unvisited, xmax, ymax)    
    points = [point for point in unvisited]
    tentatives = [9e99 for point in unvisited]
    
    current = Coordinates([0, 0])
    unvisited[current][1] = 0
    tentatives[points.index(current)] = 0
    while current != Coordinates([(5*(xmax+1))-1, (5*(ymax+1))-1]):
        for neighbour in adjacent(current):
            try:
                dist_curr = unvisited[current][1] + unvisited[neighbour][0]
                if dist_curr < unvisited[neighbour][1]:
                    unvisited[neighbour][1] = dist_curr
                    tentatives[points.index(neighbour)] = dist_curr
            except:
                continue
            
        unvisited.pop(current)
        index = points.index(current)
        points.pop(index)
        tentatives.pop(index)
        current = +points[np.argmin(tentatives)]
    
    return unvisited[current][1]

def extend_grid(unvisited, xmax, ymax):
    """
    Calculates an extended grid from an initial grid, where the initial grid forms the top
    left tile in a 5x5 tile area that forms the full map, with the original map tile
    repeating to the right and downward. Each time the tile repeats to the right or
    downward, all of its risk levels are 1 higher than the tile immediately up or left of
    it. However, risk levels above 9 wrap back around to 1.

    Parameters
    ----------
    unvisited : dict {Coordinates : [int, int]}
        Map of every point on the initial grid to its assigned risk level and current
        tentative distance to the starting point (as in Dijkstra's algorithm).
    xmax : int
        The maximum x-coordinate of the initial grid.
    ymax : int
        The maximum y-coordinate of the initial grid.

    Returns
    -------
    unvisited_new : dict {Coordinates : [int, int]}
        Map of every point on the extended grid to its assigned risk level and current
        tentative distance to the starting point (as in Dijkstra's algorithm).

    """
    unvisited_new = dict()
    for point in unvisited:
        for n_x, x in enumerate(range(point.x, point.x + (5*(xmax+1)), xmax+1)):
            for n_y, y in enumerate(range(point.y, point.y + (5*(ymax+1)), ymax+1)):
                risk = unvisited[point][0] + n_x + n_y
                if risk > 9:
                    risk %= 9
                unvisited_new[Coordinates([x, y])] = [risk, 9e99]
                
    return unvisited_new
