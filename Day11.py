import shlex
import numpy as np

def Day11_Part1(steps, filename='Inputs/Day11_Inputs.txt'):
    """
    Calculates the total number of flashes which occur in a grid of octupi, given in an
    input file, after a given number of steps. Each octopus has an energy level, starting
    at an initial value given in the input file, which increases by 1 each step. Any
    octupi with an energy level above 9 in a given step flash, decrasing their own energy
    level back to 0 and increasing all adjacent octupi's energy levels by 1, including
    diagonally adjacent octupi. If any of these octupi now have an energy level above 9
    they also flash, and the effect continues until all octupi in the current step have
    energy levels of 9 or below again.

    Parameters
    ----------
    steps : int
        Total number of steps from the initital starting point to simulate.
    filename : str, optional
        Input file containing the initial energy levels of all octupi in the grid of
        octupi.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    flashes : int
        The total number of times an octopus flashes in the given number of steps.

    """
    file = open(filename)
    octupi = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            octupi.append(line[0])
    file.close()
    
    energy = []
    coordinates = []
    for row, octopus_row in enumerate(octupi):
        for column, octopus in enumerate(octopus_row):
            energy.append(int(octopus))
            coordinates.append([row, column])
    
    print('Before any steps:')
    for row in range(10):
        row_str = ''
        for column in range(10):
            row_str += str(energy[coordinates.index([row, column])])
        print(row_str)
    print('')
    
    flashes = 0
    for step in range(steps):
    
        energy = list(np.array(energy) + 1)
        try:
            energy.index(10)
            max_energy = True
            
        except:
            max_energy = False
            
        while max_energy:
            max_coords = coordinates[energy.index(10)]
            energy[coordinates.index(max_coords)] = -1
            for row in range(max_coords[0]-1, max_coords[0]+2):
                for column in range(max_coords[1]-1, max_coords[1]+2):
                    try:
                        energy_here = energy[coordinates.index([row, column])]
                        if energy_here < 10 and energy_here > -1:
                            energy[coordinates.index([row, column])] += 1
                    
                    except:
                        pass
            
            try:
                energy.index(10)
                max_energy = True
            
            except:
                max_energy = False
        
        while True:
            try:
                energy[energy.index(-1)] = 0
            
            except:
                break
        
        flashes += energy.count(0)
        
        print(f'After step {step + 1}:')
        for row in range(10):
            row_str = ''
            for column in range(10):
                row_str += str(energy[coordinates.index([row, column])])
            print(row_str)
        print('')
        
    return flashes

def Day11_Part2(filename='Inputs/Day11_Inputs.txt'):
    """
    Calculates the number of steps required before all octupi in a grid, given in an input
    file, flash simulataneously. Each octopus has an energy level, starting at an initial
    value given in the input file, which increases by 1 each step. Any octupi with an
    energy level above 9 in a given step flash, decrasing their own energy level back to 0
    and increasing all adjacent octupi's energy levels by 1, including diagonally adjacent
    octupi. If any of these octupi now have an energy level above 9 they also flash, and
    the effect continues until all octupi in the current step have energy levels of 9 or
    below again.

    Parameters
    ----------
    filename : str, optional
        Input file containing the initial energy levels of all octupi in the grid of
        octupi.
        The default is 'Inputs/Day11_Inputs.txt'.

    Returns
    -------
    step : int
        The number of steps required before all octupi flash simulataneously.

    """
    file = open(filename)
    octupi = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            octupi.append(line[0])
    file.close()
    
    energy = []
    coordinates = []
    for row, octopus_row in enumerate(octupi):
        for column, octopus in enumerate(octopus_row):
            energy.append(int(octopus))
            coordinates.append([row, column])
    
    print('Before any steps:')
    for row in range(10):
        row_str = ''
        for column in range(10):
            row_str += str(energy[coordinates.index([row, column])])
        print(row_str)
    print('')
    
    step = 0
    while True:
        step += 1
        energy = list(np.array(energy) + 1)
        try:
            energy.index(10)
            max_energy = True
            
        except:
            max_energy = False
            
        while max_energy:
            max_coords = coordinates[energy.index(10)]
            energy[coordinates.index(max_coords)] = -1
            for row in range(max_coords[0]-1, max_coords[0]+2):
                for column in range(max_coords[1]-1, max_coords[1]+2):
                    try:
                        energy_here = energy[coordinates.index([row, column])]
                        if energy_here < 10 and energy_here > -1:
                            energy[coordinates.index([row, column])] += 1
                    
                    except:
                        pass
            
            try:
                energy.index(10)
                max_energy = True
            
            except:
                max_energy = False
        
        while True:
            try:
                energy[energy.index(-1)] = 0
            
            except:
                break
        
        if all(energy_here == 0 for energy_here in energy):
            break
        
    print(f'After step {step}:')
    for row in range(10):
        row_str = ''
        for column in range(10):
            row_str += str(energy[coordinates.index([row, column])])
        print(row_str)
    print('')
        
    return step