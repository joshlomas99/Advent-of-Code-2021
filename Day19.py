import shlex
import numpy as np

# define the 24 rotation matices in 3D with 0 determinant
rotations = [np.array([[1, 0, 0], [0, 1, 0], [0, 0, 1]]),
             np.array([[-1, 0, 0], [0, -1, 0], [0, 0, 1]]),
             np.array([[-1, 0, 0], [0, 1, 0], [0, 0, -1]]),
             np.array([[1, 0, 0], [0, -1, 0], [0, 0, -1]]),
             np.array([[-1, 0, 0], [0, 0, 1], [0, 1, 0]]),
             np.array([[1, 0, 0], [0, 0, -1], [0, 1, 0]]),
             np.array([[1, 0, 0], [0, 0, 1], [0, -1, 0]]),
             np.array([[-1, 0, 0], [0, 0, -1], [0, -1, 0]]),
             np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1]]),
             np.array([[0, 1, 0], [-1, 0, 0], [0, 0, 1]]),
             np.array([[0, 1, 0], [1, 0, 0], [0, 0, -1]]),
             np.array([[0, -1, 0], [-1, 0, 0], [0, 0, -1]]),
             np.array([[0, 1, 0], [0, 0, 1], [1, 0, 0]]),
             np.array([[0, -1, 0], [0, 0, -1], [1, 0, 0]]),
             np.array([[0, -1, 0], [0, 0, 1], [-1, 0, 0]]),
             np.array([[0, 1, 0], [0, 0, -1], [-1, 0, 0]]),
             np.array([[0, 0, 1], [1, 0, 0], [0, 1, 0]]),
             np.array([[0, 0, -1], [-1, 0, 0], [0, 1, 0]]),
             np.array([[0, 0, -1], [1, 0, 0], [0, -1, 0]]),
             np.array([[0, 0, 1], [-1, 0, 0], [0, -1, 0]]),
             np.array([[0, 0, 1], [0, 1, 0], [-1, 0, 0]]),
             np.array([[0, 0, 1], [0, -1, 0], [1, 0, 0]]),
             np.array([[0, 0, -1], [0, 1, 0], [1, 0, 0]]),
             np.array([[0, 0, -1], [0, -1, 0], [-1, 0, 0]])]

class Coordinates:
    """
    Class to define a set of coordinates (x, y, z)
    """
    def __init__(self, pos):
        """
        Initialise the class with one parameter.

        Parameters
        ----------
        pos : list of int
            Coordinates in the form [x, y, z].

        """
        self.pos = pos
        self.x = pos[0]
        self.y = pos[1]
        self.z = pos[2]
    
    def __repr__(self):
        """
        Return the representation of a Coordinates object.

        Returns
        -------
        str
            Representation.

        """
        return f'{self.__class__.__name__}({self.x}, {self.y}, {self.z})'
    
    def __hash__(self):
        """
        Override the hash function for a Coordinates object.

        Returns
        -------
        int
            The hash of the Coordinates.

        """
        return hash((self.x, self.y, self.z))

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
        return (self.x, self.y, self.z) == (other.x, other.y, other.z)

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
        return self.__class__([self.x, self.y, self.z])

def Day19_Part1(filename='Inputs/Day19_Inputs.txt'):
    """
    Calculates the total number of unique beacons in a 3D area of water, given the
    coordinates of every beacon detected by a series of scanners at unknown relative
    coordinates, as given in an input file. Each scanner is capable of detecting all
    beacons that are at most 1000 units away from the scanner in each of the three axes
    (x, y, and z). Every scanner will detect at least 12 beacons which are also detected
    by a single other scanner, allowing the absolute positions of every scanner and beacon
    to be determined.

    Parameters
    ----------
    filename : str, optional
        Input file giving every scanner and the relative coordinates of the beacons it
        detects.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    beacon_num : int
        The total number of unique beacons.

    """

    file = open(filename)
    data = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data.append(line)
    file.close()

    scanners = []
    for line in data:
        if 'scanner' in line:
            scanners.append(['Scanner ' + line[2]])
        else:
            scanners[-1].append(np.array([int(i) for i in line[0].split(',')]))

    corrected_scanners = [scanners.pop(0)]
    beacons = {Coordinates(beacon) for beacon in corrected_scanners[0][1:]}
    searched_scanners = dict()
    while len(scanners) > 0:
        print(len(corrected_scanners))
        match_found = False
        for n, scanner in enumerate(scanners):
            for corrected_scanner in corrected_scanners:
                if scanner[0] not in searched_scanners or corrected_scanner[0] not in searched_scanners[scanner[0]]:
                    for rotation in rotations:
                        offsets = dict()
                        rotated_scanner = []
                        for coord in scanner[1:]:
                            rotated_scanner.append(rotation.dot(coord))
                        for coord in rotated_scanner:
                            for corrected_coord in corrected_scanner[1:]:
                                offset = Coordinates(corrected_coord - coord)
                                try:
                                    offsets[offset] += 1
                                    if offsets[offset] >= 12:
                                        match_found = True
                                        break
                                except:
                                    offsets[offset] = 1
                            if match_found:
                                break
                        if match_found:
                            break
                    if match_found:
                        break
                    else:
                        try:
                            searched_scanners[scanner[0]].append(corrected_scanner[0])
                        except:
                            searched_scanners[scanner[0]] = [corrected_scanner[0]]
            if match_found:
                new_corrected_scanner = [scanner[0]]
                for beacon in rotated_scanner:
                    new_corrected_scanner.append(beacon + np.array(offset.pos))
                    beacons.add(Coordinates(new_corrected_scanner[-1]))
                corrected_scanners.append(new_corrected_scanner)
                scanners.pop(n)
                break
    beacon_num = len(beacons)
    return beacon_num

def Day19_Part2(filename='Inputs/Day19_Inputs.txt'):
    """
    Calculates the largest Manhattan distance between any two scanners once their relative
    positions are determined, given the coordinates of every beacon detected by a series
    of scanners at unknown relative coordinates, as given in an input file. Each scanner is
    capable of detecting all beacons that are at most 1000 units away from the scanner in
    each of the three axes (x, y, and z). Every scanner will detect at least 12 beacons
    which are also detected by a single other scanner, allowing the absolute positions of
    every scanner and beacon to be determined.

    Parameters
    ----------
    filename : str, optional
        Input file giving every scanner and the relative coordinates of the beacons it
        detects.
        The default is 'Inputs/Day19_Inputs.txt'.

    Returns
    -------
    max_distance : int
        The largest Manhattan distance between any two scanners.

    """
    file = open(filename)
    data = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data.append(line)
    file.close()

    scanners = []
    for line in data:
        if 'scanner' in line:
            scanners.append(['Scanner ' + line[2]])
        else:
            scanners[-1].append(np.array([int(i) for i in line[0].split(',')]))

    corrected_scanners = [scanners.pop(0)]
    beacons = {Coordinates(beacon) for beacon in corrected_scanners[0][1:]}
    scanner_positions = [[0, 0, 0]]
    searched_scanners = dict()
    while len(scanners) > 0:
        print(len(corrected_scanners))
        match_found = False
        for n, scanner in enumerate(scanners):
            for corrected_scanner in corrected_scanners:
                if scanner[0] not in searched_scanners or corrected_scanner[0] not in searched_scanners[scanner[0]]:
                    for rotation in rotations:
                        offsets = dict()
                        rotated_scanner = []
                        for coord in scanner[1:]:
                            rotated_scanner.append(rotation.dot(coord))
                        for coord in rotated_scanner:
                            for corrected_coord in corrected_scanner[1:]:
                                offset = Coordinates(corrected_coord - coord)
                                try:
                                    offsets[offset] += 1
                                    if offsets[offset] >= 12:
                                        match_found = True
                                        break
                                except:
                                    offsets[offset] = 1
                            if match_found:
                                break
                        if match_found:
                            break
                    if match_found:
                        break
                    else:
                        try:
                            searched_scanners[scanner[0]].append(corrected_scanner[0])
                        except:
                            searched_scanners[scanner[0]] = [corrected_scanner[0]]
            if match_found:
                new_corrected_scanner = [scanner[0]]
                for beacon in rotated_scanner:
                    scanner_positions.append([-1*pos for pos in offset.pos])
                    new_corrected_scanner.append(beacon + np.array(offset.pos))
                    beacons.add(Coordinates(new_corrected_scanner[-1]))
                corrected_scanners.append(new_corrected_scanner)
                scanners.pop(n)
                break

    max_distance = 0
    for scanner in scanner_positions:
        scanner_positions.remove(scanner)
        scanner_positions_copy = 1*scanner_positions
        for second_scanner in scanner_positions_copy:
            distance = sum([abs(scanner[i] - second_scanner[i]) for i in range(3)])
            if distance > max_distance:
                max_distance = distance

    return max_distance