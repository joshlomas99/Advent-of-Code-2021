import numpy as np
import shlex

def Day1_Part1(filename='Inputs/Day1_Inputs.txt'):
    """
    Determine where the depth of a submarine, taken from an input file, increases
    or decreases at each measurement, and calculate how many times it increases.
    
    Parameters
    ----------
    filename : str
        Input file containing a list of depths.
        
    Returns
    -------
    increased : int
        The number of times the depth increased over the previous measurement.
        
    """
    file = open(filename)
    depths = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            depths.append(int(line[0]))
    file.close()

    increased = 0
    print(f'{depths[0]} (N/A - no previous measurement)')
    for n, d in enumerate(depths):
        if n == 0:
            continue
        if d > depths[n-1]:
            print(f'{d} (increased)')
            increased += 1
        elif d == depths[n-1]:
            print(f'{d} (no change)')
        else:
            print(f'{d} (decreased)')
    
    return increased

def Day1_Part2(filename='Inputs/Day1_Inputs.txt'):
    """
    Determine where the sum of a three-measurement sliding window of depths of a
    submarine, taken from an input file, increases or decreases at each measurement,
    and calculate how many times it increases.
    
    Parameters
    ----------
    filename : str
        Input file containing a list of depths.
        
    Returns
    -------
    increased : int
        The number of times the sum of a three-measurement sliding window of depths
        increased over the previous measurement.
        
    """
    file = open(filename)
    depths = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            depths.append(int(line[0]))
    file.close()
    
    combined_depths = []
    for n in range(len(depths)-2):
        combined_depths.append(np.sum(depths[n:n+3]))
        
    increased = 0
    print(f'{combined_depths[0]} (N/A - no previous sum)')
    for m, c in enumerate(combined_depths):
        if m == 0:
            continue
        if c > combined_depths[m-1]:
            print(f'{c} (increased)')
            increased += 1
        elif c == combined_depths[m-1]:
            print(f'{c} (no change)')
        else:
            print(f'{c} (decreased)')
    
    return increased