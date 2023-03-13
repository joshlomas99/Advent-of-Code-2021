from functools import reduce
import operator

class RangeException(Exception):
    """
    Exception for invalid cuboid limit ranges.
    """
    pass

class Cuboid:
    """
    Class describing a cuboid, with the ranges on each axis defined.
    """
    def __init__(self, ranges: list) -> None:
        """
        Initialise the class with one parameter, the ranges in each axis. Ranges are considered
        inclusively, so limits of e.g. (1, 2) on one axis would give a side length of 2.

        Parameters
        ----------
        ranges : list
            Range in each axis of the cuboid, in the form [xmin, xmax, ymin, ymax, zmin, zmax] or
            [(xmin, xmax), (ymin, ymax), (zmin, zmax)].

        Raises
        ------
        RangeException
            If ranges are given in an invalid format.

        Returns
        -------
        None.

        """
        # Parse both possible forms of input ranges into common format
        if len(ranges) == 3 and isinstance(ranges[0], tuple):
            self.ranges = ranges
        elif len(ranges) == 6 and isinstance(ranges[0], int):
            self.ranges = [(ranges[2*i], ranges[2*i+1]) for i in range(3)]
        else:
            raise RangeException(f'Unknown cuboid format {ranges}')

    def __repr__(self) -> str:
        """
        Return the representation of a Cuboid object.

        Returns
        -------
        repr : str
            Representation.

        """
        return '{}(x={}..{}, y={}..{}, z={}..{})'.format(self.__class__.__name__,
                                                        *self.ranges[0], *self.ranges[1],
                                                        *self.ranges[2])

    def volume(self) -> int:
        """
        Returns the volume of the cuboid, where ranges are considered inclusively.

        Returns
        -------
        volume : int
            Volume of the cuboid.

        """
        # Volume is dx*dy*dz
        return reduce(operator.mul, [(r[1]-r[0])+1 for r in self.ranges])

    def find_overlap(self, cuboid):
        """
        Find the overlap of this cuboid with another.

        Parameters
        ----------
        cuboid : Cuboid
            The cuboid to compare to this one for overlap.

        Returns
        -------
        overlap : Cuboid or None
            The cuboid covering the volume overlapping between the two cuboids. Or None if there is
            no overlap.

        """
        overlap_ranges = []
        # For each axis
        for axis in range(3):
            if (lower := max(self.ranges[axis][0], cuboid.ranges[axis][0])) > \
                (higher := min(self.ranges[axis][1], cuboid.ranges[axis][1])):
                # If the ranges of any axis do not overlap, there is no overlap between the cuboids
                return None
            # Else build new Cuboid with overlapping ranges
            overlap_ranges.append((lower, higher))

        return Cuboid(overlap_ranges)

    def unique_volume(self, following_cuboids: list) -> int:
        """
        Finds the unique volume covered by this Cuboid when compared to a list of other Cuboids.

        Parameters
        ----------
        following_cuboids : list(Cuboid)
            List of cuboids to compare this one to.

        Returns
        -------
        volume : int
            The unique volume covered only by this cuboid.

        """
        # Find the overlaps with all cuboids in the list which do overlap
        overlaps = [overlap for cuboid in following_cuboids if (overlap := self.find_overlap(cuboid))]

        # Start with the whole volume of this cuboid
        volume = self.volume()
        # Remove the unique volume covered by each cuboid in the list, when compared to every
        # cuboid after it in the list, calculated recursively to avoid overcounting
        volume -= sum(cuboid.unique_volume(overlaps[i+1:]) for i, cuboid in enumerate(overlaps))

        return volume

import re

def get_input(input_file: str='Inputs/Day22_Inputs.txt', limited_volume=None) -> list:
    """
    Parse an input file to extract a set of reboot steps required to reboot a reactor core. Each
    step describes a cuboidal section of the reactor and whether this section is turns 'on' or
    'off' in that step. Additional option to only consider cuboids in a limited volume of the
    reactor.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the reboot steps.
        The default is 'Inputs/Day22_Inputs.txt'.
    limited_volume : Cuboid or None, optional
        If not None then the Cuboid describing the limited volume to consider, ignoring the rest
        of the volume.
        The default is None.

    Returns
    -------
    cuboids : list(tuple(str, Cuboid))
        List of reboot steps in the form (instruction, Cuboid).

    """
    # Parse input file
    with open(input_file) as f:
        cuboids = []
        for line in f.readlines():
            line = line.strip().split()
            # Extract axis ranges and build corresponding Cuboid
            cuboid = Cuboid([int(i) for i in re.findall('[-\d]+', line[1])])
            # If a limited volume is defined, only consider the overlap with this volume
            if limited_volume:
                cuboid = cuboid.find_overlap(limited_volume)
                if cuboid is None:
                    continue
            cuboids.append((line[0], cuboid))

    return cuboids

def Day22_Part1(input_file: str='Inputs/Day22_Inputs.txt') -> int:
    """
    Finds the number of cubes in a reactor core which are on after executing a set of reboot steps
    given in an input file, considering only the initialization procedure area in the region
    x=-50..50, y=-50..50, z=-50..50. Each step describes a cuboidal section of the reactor and
    whether this section is turns 'on' or 'off' in that step. All cubes start as 'off'.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the reboot steps.
        The default is 'Inputs/Day22_Inputs.txt'.

    Returns
    -------
    volume_on : int
        The number of cubes in the initialization procedure area which are on after the reboot
        steps have been executed.

    """
    # Define the initialization procedure area
    limited_volume = Cuboid([(-50, 50), (-50, 50), (-50, 50)])
    # Extract the reboot steps from the input file, considering only overlaps with the
    # initialization procedure area
    cuboids = get_input(input_file, limited_volume)

    # Starting with all cubes off
    volume_on = 0
    # For every step
    for i, (state, cuboid) in enumerate(cuboids):
        # Ignore steps which turn cubes off, as these will be accounted for in the next step
        if state == 'off':
            continue
        # Count the unique volume turned on by this step, which is the volume not covered by any
        # future steps. This must therefore be the final instruction for this unique volume,
        # so it fill finish as 'on'.
        volume_on += cuboid.unique_volume([cuboid2 for state2, cuboid2 in cuboids[i+1:]])
    
    return volume_on

def Day22_Part2(input_file: str='Inputs/Day22_Inputs.txt') -> None:
    """
    Finds the number of cubes in a reactor core which are on after executing a set of reboot steps
    given in an input file, considering the entire reactor volume. Each step describes a cuboidal
    section of the reactor and whether this section is turns 'on' or 'off' in that step. All cubes
    start as 'off'.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the reboot steps.
        The default is 'Inputs/Day22_Inputs.txt'.

    Returns
    -------
    volume_on : int
        The number of cubes in the whole reactor which are on after the reboot steps have been
        executed.

    """
    # Extract the reboot steps from the input file
    cuboids = get_input(input_file)

    # Starting with all cubes off
    volume_on = 0
    # For every step
    for i, (state, cuboid) in enumerate(cuboids):
        # Ignore steps which turn cubes off, as these will be accounted for in the next step
        if state == 'off':
            continue
        # Count the unique volume turned on by this step, which is the volume not covered by any
        # future steps. This must therefore be the final instruction for this unique volume,
        # so it fill finish as 'on'.
        volume_on += cuboid.unique_volume([cuboid2 for state2, cuboid2 in cuboids[i+1:]])
    
    return volume_on
