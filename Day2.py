import shlex

class Submarine:
    """
    Class defining a submarine with associated horizontal (x) and vertical (depth)
    positions and an associated aim parameter controlling the direction of motion
    of the submarine.
    Associated functions allow the submarine to be moved.
    """
    def __init__(self, x, depth, aim):
        """
        Initialise the class with its three components.

        Parameters
        ----------
        x : int
            Horizontal submarine position.
        depth : int
            Vertical submarine depth (higher values mean deeper in the ocean
            i.e. lower vertical position).
        aim : int
            The direction in which the submarine is facing, and the direction
            in which it will move when the forward function is used.

        Returns
        -------
        None.

        """
        self.x = x
        self.depth = depth
        self.aim = aim
    
    def up(self, ddepth):
        """
        Move the submarine up (reduce the depth).

        Parameters
        ----------
        ddepth : int
            The change in depth of the submarine.

        Returns
        -------
        None.

        """
        self.aim -= ddepth
        
    def down(self, ddepth):
        """
        Move the submarine down (increase the depth).

        Parameters
        ----------
        ddepth : int
            The change in depth of the submarine.

        Returns
        -------
        None.

        """
        self.aim += ddepth
        
    def forward(self, dx):
        """
        Move the submarine forward in the direction of 'aim'.

        Parameters
        ----------
        dx : int
            The change in horizontal position of the submarine.

        Returns
        -------
        None.

        """
        self.x += dx
        self.depth += dx*self.aim
        
def Day2_Part1and2(filename='Inputs/Day2_Inputs.txt', submarine=Submarine(0, 0, 0)):
    """
    Move a submarine, starting at a horizontal position of 0 and a depth of 0, according
    to a series of instructions given in an input file.

    Parameters
    ----------
    filename : str, optional
        The input file containing the instructions.
        The default is 'Inputs/Day2_Inputs.txt'.
    submarine : Submarine, optional
        The submarine object which will be moved according to the instructions.
        The default is Submarine(0, 0, 0) (starting at the origin).

    Raises
    ------
    Exception
        If an unknown direction is given.

    Returns
    -------
    tuple (int, int)
        Final horizontal position and depth of the submarine.
    int
        Product of the final horizontal position and depth of the submarine.

    """
    file = open(filename)
    directions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            directions.append(line)
    file.close()

    submarine.x, submarine.depth, submarine.aim = 0, 0, 0
    
    for d in directions:
        if d[0] == 'forward':
            submarine.forward(int(d[1]))
            
        elif d[0] == 'down':
            submarine.down(int(d[1]))
            
        elif d[0] == 'up':
            submarine.up(int(d[1]))
            
        else:
            raise Exception("Unknown direction!")
    
    return (submarine.x, submarine.depth), submarine.x*submarine.depth
        