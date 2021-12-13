import shlex

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
        self.pos = pos
        self.x = 1*pos[0]
        self.y = 1*pos[1]
    
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
    
    def __getitem__(self, i):
        """
        Return the 'x' component of the Coordinates if 0 and the 'y' component if 1.

        Parameters
        ----------
        i : int
            Index of Coordinates [x, y].

        Returns
        -------
        int
            'i' component of Coordinates.

        """
        return self.pos[i]
    
    def __setitem__(self, i, s):
        """
        Set the 'i' component of the Coordinates with the integer 's'.

        Parameters
        ----------
        i : int
            Index of Coordinates [x, y].
        s : int
            Integer to which to set the 'i' Coordinates.

        Returns
        -------
        None.

        """
        self.pos[i] = s
        
        if s == 0:
            self.x = s
        if s == 1:
            self.y = s
    
def Day13_Part1(filename='Inputs/Day13_Inputs.txt', printout=False):
    """
    Calculates the number of dots visible on a piece of transparent paper after only the
    first fold according to instructions given in an input file has been applied, where
    the initial positions of every dot on a grid on the paper is given in the input file.
    
    Parameters
    ----------
    filename : str, optional
        Input files containing the initial dot positions and the folding instructions.
        The default is 'Inputs/Day13_Inputs.txt'.
    printout : bool, optional
        Whether or not to print out the grid before and after the fold.
        The default is False.

    Returns
    -------
    num_dots : int
        The number of dots visible after the first fold.

    """
    file = open(filename)
    instructions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        instructions.append(line)
    file.close()
    
    split = instructions.index([])
    dots = {Coordinates([int(coord) for coord in dot[0].split(',')]) for dot in instructions[:split]}
    
    convert_fold = lambda coord : int(coord) if coord.isnumeric() else coord
    
    folds = [[convert_fold(coord) for coord in fold[2].split('=')] for fold in instructions[split+1:]]
    
    if printout:
        for row in range(max([dot.y for dot in dots])+1):
            row_curr = ''
            for column in range(max([dot.x for dot in dots])+1):
                if Coordinates([column, row]) in dots:
                    row_curr += '#'
                else:
                    row_curr += '.'
            print(row_curr)
    
    fold = folds[0]
    dots_new = set()
    for n, dot in enumerate(dots):
        if fold[0] == 'x' and dot.x > fold[1]:
            dot_new = Coordinates([2*fold[1] - dot.x, dot.y])
            dots_new.add(dot_new)
        
        elif fold[0] == 'y' and dot[1] > fold[1]:
            dot_new = Coordinates([dot.x, 2*fold[1] - dot.y])
            dots_new.add(dot_new)
            
        else:
            dots_new.add(dot)
            
    dots = dots_new.copy()
            
    if printout:
        for row in range(max([dot.y for dot in dots])+1):
            row_curr = ''
            for column in range(max([dot.x for dot in dots])+1):
                if Coordinates([column, row]) in dots:
                    row_curr += '#'
                else:
                    row_curr += '.'
    
    num_dots = len(dots)
    return num_dots
    
def Day13_Part2(filename='Inputs/Day13_Inputs.txt'):
    """
    Prints the grid of dots and empty space visible on a piece of transparent paper after
    every fold has been applied according to instructions given in an input file, where the
    initial positions of every dot on a grid on the paper is given in the input file.
    
    Parameters
    ----------
    filename : str, optional
        Input files containing the initial dot positions and the folding instructions.
        The default is 'Inputs/Day13_Inputs.txt'.

    """
    file = open(filename)
    instructions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        instructions.append(line)
    file.close()
    
    split = instructions.index([])
    dots = {Coordinates([int(coord) for coord in dot[0].split(',')]) for dot in instructions[:split]}
    
    convert_fold = lambda coord : int(coord) if coord.isnumeric() else coord
    
    folds = [[convert_fold(coord) for coord in fold[2].split('=')] for fold in instructions[split+1:]]
    
    fold = folds[0]
    for fold in folds:
        dots_new = set()
        for n, dot in enumerate(dots):
            if fold[0] == 'x' and dot.x > fold[1]:
                dot_new = Coordinates([2*fold[1] - dot.x, dot.y])
                dots_new.add(dot_new)
            
            elif fold[0] == 'y' and dot[1] > fold[1]:
                dot_new = Coordinates([dot.x, 2*fold[1] - dot.y])
                dots_new.add(dot_new)
                
            else:
                dots_new.add(dot)
                
        dots = dots_new.copy()
            
    for row in range(max([dot.y for dot in dots])+1):
        row_curr = ''
        for column in range(max([dot.x for dot in dots])+1):
            if Coordinates([column, row]) in dots:
                row_curr += '#'
            else:
                row_curr += '.'
        print(row_curr)
    