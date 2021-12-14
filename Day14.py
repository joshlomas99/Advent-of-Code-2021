import shlex

def Day14_Part1(stepmax, filename='Inputs/Day14_Inputs.txt', printout=False):
    """
     Calculates the difference between the quantity of the most and least common elements in
     a string, after a series of insertions of single characters between corresponding pairs
     of characters are performed as described in an input file, where the initial string is
     given in the same input file.

    Parameters
    ----------
    stepmax : int
        The number of rounds of insertion to perform on the initial string.
    filename : str, optional
        Input files giving the initial string and pair insertion rules.
        The default is 'Inputs/Day14_Inputs.txt'.
    printout : bool, optional
        Whether or not to print the result of each round of insertion.
        The default is False.

    Returns
    -------
    difference : int
         The difference between the quantity of the most and least common elements in
         the initial string after 'stepmax' rounds of insertions.

    """
    file = open(filename)
    instructions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        instructions.append(line)
    file.close()
    
    template = instructions[0][0]
    doubles = [instruction[0] for instruction in instructions[2:]]
    insertions = [instruction[2] for instruction in instructions[2:]]
    
    if printout:
        print('Template:     ' + template)
    
    for step in range(1, stepmax+1):
        template_new = ''
        for i in range(len(template)-1):
            double = template[i:i+2]
            try:
                insert = insertions[doubles.index(double)]
                inserted_double = double[0] + insert + double[1]
                if i < len(template)-2:
                    template_new += inserted_double[:2]
                else:
                    template_new += inserted_double
                
            except:
                if i < len(template)-2:
                    template_new += double[:1]
                else:
                    template_new += double
        
        template = 1*template_new
        if printout:
            print(f'After step {step}: ' + template)
            
    counts = {}
    for char in template:
        try:
            counts[char] += 1
        except:
            counts[char] = 1
    
    difference = max([counts[count] for count in counts]) - min([counts[count] for count in counts])
    return difference

def Day14_Part2(stepmax, filename='Inputs/Day14_Inputs.txt'):
    """
     Calculates the difference between the quantity of the most and least common elements in
     a string, after a series of insertions of single characters between corresponding pairs
     of characters are performed as described in an input file, where the initial string is
     given in the same input file. (Optimised algorithm for larger values of 'stepmax')

    Parameters
    ----------
    stepmax : int
        The number of rounds of insertion to perform on the initial string.
    filename : str, optional
        Input files giving the initial string and pair insertion rules.
        The default is 'Inputs/Day14_Inputs.txt'.

    Returns
    -------
    difference : int
         The difference between the quantity of the most and least common elements in
         the initial string after 'stepmax' rounds of insertions.

    """
    file = open(filename)
    instructions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        instructions.append(line)
    file.close()
    
    template = instructions[0][0]
    doubles = [instruction[0] for instruction in instructions[2:]]
    insertions = [instruction[2] for instruction in instructions[2:]]
    
    counts = {template[0] : 1, template[-1] : 1}
    
    doubles_count = {}
    for i in range(len(template)-1):
        double = template[i:i+2]
        try:
            doubles_count[double] += 1
        
        except:
            doubles_count[double] = 1
            
    
    for step in range(1, stepmax+1):
        doubles_count_new = {}
        for double in doubles_count:
            try:
                insert = insertions[doubles.index(double)]
                try:
                    doubles_count_new[double[0] + insert] += doubles_count[double]
                    
                except:
                    doubles_count_new[double[0] + insert] = doubles_count[double]
                    
                try:
                    doubles_count_new[insert + double[1]] += doubles_count[double]
                    
                except:
                    doubles_count_new[insert + double[1]] = doubles_count[double]
            
            except:
                try:
                    doubles_count_new[double] += doubles_count[double]
                    
                except:
                    doubles_count_new[double] = doubles_count[double]
                    
        doubles_count = doubles_count_new.copy()
                    
    for double in doubles_count:
        try:
            counts[double[0]] += doubles_count[double]
        except:
            counts[double[0]] = doubles_count[double]
            
        try:
            counts[double[1]] += doubles_count[double]
        except:
            counts[double[1]] = doubles_count[double]
            
    for char in counts:
        counts[char] = int(counts[char]/2)
        
    difference = max([counts[count] for count in counts]) - min([counts[count] for count in counts])
    return difference