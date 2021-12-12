import shlex

def check_paths(first, links, path, paths):
    """
    Calculates the possible paths through a series of caves which are linked according to
    the map 'paths', starting from 'first' and ending at 'end', while visiting big caves
    (whose names are in capitals) an unlimited number of times and small caves (whose
    names are in lower case) only once at maximum.

    Parameters
    ----------
    first : str
        The name of the cave to start at.
    links : dict {str : list of strings}
        Dictionary giving every linked cave to a given cave.
    path : list of strings
        List of the caves visited so far in the current path being generated.
    paths : list of lists of strings
        List of all the different paths from 'start' to 'end' found so far.

    Returns
    -------
    path : list of strings
        List of the caves visited so far in the current path being generated.
    paths : list of lists of strings
        List of all the different paths from 'start' to 'end' found so far.

    """
    path.append(first)
    for second in links[first]:
        path_curr = 1*path
        if (second.islower() and path.count(second) == 0) or second.isupper():
            if second == 'end':
                path_curr.append(second)
                paths.append(path_curr)
                
            else:
                path_curr, paths = check_paths(second, links, path_curr, paths)
        else:
            pass
    
    return path, paths

def Day12_Part1(filename='Inputs/Day12_Inputs.txt', printout=False):
    """
    Calculates the total number of possible paths from 'start' to 'end' through a series
    of caves, which are linked according to an input file giving every link between two
    caves. Big caves (whose names are in capitals) can be visited an unlimited number of
    times and small caves (whose names are in lower case) can be visited only once per
    path.

    Parameters
    ----------
    filename : str
        The input file containing every link between two caves.
        The default is 'Inputs/Day12_Inputs.txt'.
    printout : bool
        Whether or not to print out every path found.
        The default is False.
        
    Returns
    -------
    num_paths : int
        The number of possible paths throught the caves from 'start' to 'end'.

    """
    file = open(filename)
    connections = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            connections.append(line[0])
    file.close()
     
    links = {}
    for connection in connections:
        [first, second] = connection.split('-')
        try:
            links[first].append(second)
            
        except:
            links[first] = [second]
            
        try:
            links[second].append(first)
            
        except:
            links[second] = [first]
    
    paths = check_paths('start', links, [], [])[1]
    if printout:
        print(paths)
        
    num_paths = len(paths)
    return num_paths
    
def check_paths_doublesmall(first, links, path, paths):
    """
    Calculates the possible paths through a series of caves which are linked according to
    the map 'paths', starting from 'first' and ending at 'end', while visiting big caves
    (whose names are in capitals) an unlimited number of times and small caves (whose
    names are in lower case) only once at maximum, except for one small cave which can
    be visited twice at maximum.

    Parameters
    ----------
    first : str
        The name of the cave to start at.
    links : dict {str : list of strings}
        Dictionary giving every linked cave to a given cave.
    path : list of strings
        List of the caves visited so far in the current path being generated.
    paths : list of lists of strings
        List of all the different paths from 'start' to 'end' found so far.

    Returns
    -------
    path : list of strings
        List of the caves visited so far in the current path being generated.
    paths : list of lists of strings
        List of all the different paths from 'start' to 'end' found so far.

    """
    path.append(first)
    for second in links[first]:
        path_curr = 1*path
        if (second.islower() and path_curr.count(second) == 0) or second.isupper():
            if second == 'end':
                path_curr.append(second)
                paths.append(path_curr[1:])
                
            else:
                path_curr, paths = check_paths_doublesmall(second, links, path_curr, paths)
        
        elif not path_curr[0] and path_curr.count(second) == 1 and second != 'start':
            path_curr[0] = True
            path_curr, paths = check_paths_doublesmall(second, links, path_curr, paths)
        
        else:
            pass
    
    return path, paths

def Day12_Part2(filename='Inputs/Day12_Inputs.txt', printout=False):
    """
    Calculates the total number of possible paths from 'start' to 'end' through a series
    of caves, which are linked according to an input file giving every link between two
    caves. Big caves (whose names are in capitals) can be visited an unlimited number of
    times and small caves (whose names are in lower case) can be visited only once per
    path, except for one which can be visited twice.

    Parameters
    ----------
    filename : str
        The input file containing every link between two caves.
        The default is 'Inputs/Day12_Inputs.txt'.
    printout : bool
        Whether or not to print out every path found.
        The default is False.
        
    Returns
    -------
    num_paths : int
        The number of possible paths throught the caves from 'start' to 'end'.

    """
    file = open(filename)
    connections = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            connections.append(line[0])
    file.close()
     
    links = {}
    for connection in connections:
        [first, second] = connection.split('-')
        try:
            links[first].append(second)
            
        except:
            links[first] = [second]
            
        try:
            links[second].append(first)
            
        except:
            links[second] = [first]
    
    paths = check_paths_doublesmall('start', links, [False], [])[1]
    if printout:
        print(paths)
        
    num_paths = len(paths)
    return num_paths
    