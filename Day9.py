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


def Day9_Part1(filename='Inputs/Day9_Inputs.txt'):
    """
    Calculates the number of points on a map, as given in an input file, which have a lower
    height than all adjacent points (not including diagonally adjacent points).

    Parameters
    ----------
    filename : str, optional
        Input file giving the heights of all points on the map.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    risk_sum : int
        The sum of the risk factors of all the minimum points of the map, where the risk
        factor is 1 more than the height of a point.

    """
    file = open(filename)
    points, line_num = {}, 0
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            for n, height in enumerate(line[0]):
                points[Coordinates([n, line_num])] = int(height)
            line_num += 1
    file.close()
    
    risk_sum = 0
    for point in points:
        x, y = point.x, point.y
        lowest = True
        for pos in [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]:
            try:
                if points[Coordinates(pos)] <= points[point]:
                    lowest = False
            except:
                pass
        
        if lowest:
            risk_sum += points[point] + 1
    
    return risk_sum

def check_adjacent(point, points, basin=0):
    """
    Recursive function to calculate the number of points on a map which are in a basin
    containing the given point, where a basin is a group of points with heights less than
    9, surrounded by points with a height of 9, or the edge of the map. Points exist on a
    map.

    Parameters
    ----------
    point : Coordinates
        Starting point for the search for all points in the current basin.
    points : map {Coordinates : int}
        Map of all points, with the Coordinates of a point as the key and the height of a
        point as the value.
    basin : int, optional
        The number of points in the basin. The default is 0 as this is the starting value
        of basin.

    Returns
    -------
    basin : int
        The total number of points in the current basin.
    points : map {Coordinates : int}
        The map of points with the heights of all counted points for the given basin
        changed to 10 (required to avoid double counting).

    """
    x, y = point.x, point.y
    if basin == 0:
        basin += 1
    points[point] = 10
    for pos in [[x-1, y], [x+1, y], [x, y-1], [x, y+1]]:
        try:
            if points[Coordinates(pos)] >= 9:
                pass
            else:
                basin += 1
                basin, points = check_adjacent(Coordinates(pos), points, basin)
        except:
            pass
    
    return basin, points

def Day9_Part2(filename='Inputs/Day9_Inputs.txt'):
    """
    Calculates the product of the sizes of the three largest basins of points on a map,
    as given in an input file, where a basin is a group of points with heights less than
    9, surrounded by points with a height of 9, or the edge of the map.

    Parameters
    ----------
    filename : str, optional
        Input file giving the heights of all points on the map.
        The default is 'Inputs/Day9_Inputs.txt'.

    Returns
    -------
    basin_product : int
        The product of the sizes of the three largest basins on the map.

    """
    file = open(filename)
    points, line_num = {}, 0
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            for n, height in enumerate(line[0]):
                points[Coordinates([n, line_num])] = int(height)
            line_num += 1
    file.close()
    
    basins = []
    for point in points:
        if points[point] < 9:
            basin_next, points = check_adjacent(point, points)
            basins.append(basin_next)
            
    basin_product = 1
    for i in range(3):
        basin_product *= basins.pop(np.argmax(basins))
            
    return basin_product