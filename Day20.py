import shlex

class Coordinates:
    """
    Class to define a set of coordinates (x, y)
    """
    def __init__(self, pos):
        """
        Initialise the class with one parameter.

        Parameters
        ----------
        pos : list of int
            Coordinates in the form [x, y].

        """
        self.pos = pos
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

def Day20_Part1and2(steps, filename='Inputs/Day20_Inputs.txt', display=False,
                    displayresult=False):
    """
    Calculates the number of light pixels (#) in an image after a specified number of
    enhancements of an input file given in an input file, according to an image enhancement
    algorithm given in the same input file. A given pixel in the enhanced image is given
    as the nth character in the image enhancement algorithm, where n in an integer found
    by constructing a 9-bit binary number from the 3x3 square of pixels around the
    corresponding pixel in the input image and, reading left to right and then top to
    bottom, adding a 0 if the pixel is dark (.) or a 1 if it is light (#). The actual image
    is also infinite, and every pixel beyond the given input image start as dark (.).

    Parameters
    ----------
    steps : int
        The number of steps of enhancement to apply to the input image.
    filename : str, optional
        The input file containing the image enhancement algorithm and and the input image.
        The default is 'Inputs/Day20_Inputs.txt'.
    display : bool, optional
        Whether or not to print the image after each step of enhancement.
        The default is False.
    displayresult : bool, optional
        Whether or not to print the image after the final step of enhancement.
        The default is False.

    Returns
    -------
    light_num : int
        The number of light pixels (#) in the final enhanced image.

    """

    file = open(filename)
    data = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data.append(line)
    file.close()

    algorithm = data[0][0]
    input_image = dict()
    for column, line in enumerate(data[1:]):
        for row, char in enumerate(line[0]):
            input_image[Coordinates([row, column])] = char

    for step in range(0, steps):
        print(f'Step {step}')
        xmax = max([coord.x for coord in input_image]) + 1
        xmin = min([coord.x for coord in input_image]) - 1
        ymax = max([coord.y for coord in input_image]) + 1
        ymin = min([coord.y for coord in input_image]) - 1

        if display:
            for y in range(ymin+1, ymax, 1):
                row = ''
                for x in range(xmin+1, xmax, 1):
                    row += input_image[Coordinates([x, y])]
                print(row)
        print()

        enhanced_image = dict()
        for y in range(ymin, ymax+1, 1):
            for x in range(xmin, xmax+1, 1):
                binary = ''
                for y_ext in [y-1, y, y+1]:
                    for x_ext in [x-1, x, x+1]:
                        try:
                            if input_image[Coordinates([x_ext, y_ext])] == '.':
                                binary += '0'
                            elif input_image[Coordinates([x_ext, y_ext])] == '#':
                                binary += '1'
                        except:
                            if algorithm[0] == '.':
                                binary += '0'
                            else:
                                if step%2 == 0:
                                    binary += '0'
                                else:
                                    binary += '1'

                enhanced_image[Coordinates([x, y])] = algorithm[int(binary, base=2)]

        input_image = enhanced_image.copy()

    if displayresult:
        for y in range(ymin, ymax+1, 1):
            row = ''
            for x in range(xmin, xmax+1, 1):
                row += input_image[Coordinates([x, y])]
            print(row)

    light_num = sum([input_image[coords] == '#' for coords in input_image])
    return light_num
