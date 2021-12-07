import shlex

def Day6_Part1and2(daymax, filename='Inputs/Day6_Inputs.txt'):
    """
    Calculates the number of fish in a population after a specified nunmber of days,
    with the initial population at Day 0 given in an input file. Each fish contains an
    internal timer which goes down by 1 each day, they reproduce at 0 and then reset to
    6, newborn fish spawn with an internal timer of 8.

    Parameters
    ----------
    daymax : int
        The number of days after which we want to known the resulting fish population.
    filename : str, optional
        Input file containing the internal timers of the initial population of fish at
        Day 0.
        The default is 'Inputs/Day6_Inputs.txt'.

    Returns
    -------
    population_size : int
        The number of fish in the population after 'daymax' days have passed.

    """
    file = open(filename)
    ages = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            ages.append(line)
    file.close()
    
    fish_ages, i = [0]*9, 0
    while i < len(ages[0][0]):
        curr_age = ''
        while i < len(ages[0][0]) and ages[0][0][i] != ',':
            curr_age += ages[0][0][i]
            i += 1
        fish_ages[int(curr_age)] += 1
        i += 1
    
    day = 0
    while day < daymax:
        day += 1
        reproducing = fish_ages[0]
        fish_ages.pop(0)
        fish_ages.append(reproducing)
        fish_ages[6] += reproducing
    
    population_size = sum(fish_ages)
    return population_size
        
