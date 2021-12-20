import shlex

def snail_mag(snail_num):
    """
    Calculates the magnitude of a given snail number pair. The magnitude of a pair is 3 times
    the magnitude of its left element plus 2 times the magnitude of its right element.
    The magnitude of a regular number is just that number. Magnitude calculations are
    recursive if other pairs are nested within the pair.

    Parameters
    ----------
    snail_num : list of (int or lists of int)
        The given snail number pair to calculate the magnitude of.

    Returns
    -------
    magnitude : int
        The magnitude of the snail number pair.

    """

    magnitude = 0
    num = 1*snail_num[0]
    if type(num) == int:
        magnitude += 3*abs(num)
    elif type(num) == list:
        magnitude += 3*snail_mag(num)
    num = 1*snail_num[1]
    if type(num) == int:
        magnitude += 2*abs(num)
    elif type(num) == list:
        magnitude += 2*snail_mag(num)
    return magnitude

def Day18_Part1(filename='Inputs/Day18_Inputs.txt', printout=False):
    """
    Calculates the magnitude of the sum of a series of snail numbers given in an input file.
    A snailfish number is an ordered list of two elements where each element of the pair can
    be either a regular number or another pair. To add two snailfish numbers, form a pair
    from the left and right parameters of the addition operator reduce the result. To reduce
    a snailfish number, you must repeatedly do the first action in this list that applies to
    the snailfish number:
        - If any pair is nested inside four pairs, the leftmost such pair explodes.
        - If any regular number is 10 or greater, the leftmost such regular number splits.
    Once no action in the above list applies, the snailfish number is reduced.

    Parameters
    ----------
    filename : str, optional
        The input file giving the list of snail numbers to be added.
        The default is 'Inputs/Day18_Inputs.txt'.
    printout : bool, optional
        Whether or not to print every steps of the addition and possible reduction.
        The default is False.

    Returns
    -------
    formatted_sum : list of (int or lists of int)
        The reduced snail number resulting from the addition.
    magnitude : int
        The magnitude of the resulting snail number.

    """

    file = open(filename)
    data = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            snail_num, i, level = [], 0, 0
            while i < len(line[0]):
                if line[0][i] == '[':
                    level += 1
                    i += 1
                elif line[0][i] == ']':
                    level -= 1
                    i += 1
                elif line[0][i].isnumeric():
                    reg_num = ''
                    while line[0][i].isnumeric():
                        reg_num += line[0][i]
                        i += 1
                    if line[0][i] == ',':
                        index = 0
                    else:
                        index = 1
                    snail_num.append([level, index, int(reg_num)])
                else:
                    i += 1
            data.append(snail_num)
    file.close()
    
    snail_sum = data[0]
    for snail_num in data[1:]:
        snail_sum_copy = 1*snail_sum
        snail_sum = []
        for num in snail_sum_copy + snail_num:
            snail_sum.append([num[0]+1, num[1], num[2]])
            
        if printout:
            formatted_sum, contr, level = '', 0, 0
            for num in snail_sum:
                if num[1] == 0:
                    formatted_sum += '['*(num[0] - level)
                    contr += 1/(2**num[0])
                    level = 0
                    while contr%(1/2**level) != 0:
                        level += 1
                    formatted_sum += str(num[2]) + ', '
                elif num[1] == 1:
                    formatted_sum += str(num[2])
                    contr += 1/(2**num[0])
                    level = 0
                    while contr%(1/2**level) != 0:
                        level += 1
                    formatted_sum += ']'*(num[0] - level) + ', '
            print(f'After addition: {formatted_sum}')
                
        needs_reducing = True
        while needs_reducing:
            if printout:
                print()
            needs_reducing = False
            for n, place in enumerate(snail_sum):
                if place[0] > 4:
                    needs_reducing = True
                    if place[1] == 0:
                        if n > 0:
                            snail_sum[n-1][2] += place[2]
                            
                        index = sum(prev[0] == 4 for prev in snail_sum[:n])%2
                        snail_sum[n] = [4, index, 0]
                        
                    elif place[1] == 1:
                        if n < len(snail_sum) - 1:
                            snail_sum[n+1][2] += place[2]
                            
                        snail_sum.remove(snail_sum[n])
                        if printout:
                            formatted_sum, contr, level = '', 0, 0
                            for num in snail_sum:
                                if num[1] == 0:
                                    formatted_sum += '['*(num[0] - level)
                                    contr += 1/(2**num[0])
                                    level = 0
                                    while contr%(1/2**level) != 0:
                                        level += 1
                                    formatted_sum += str(num[2]) + ', '
                                elif num[1] == 1:
                                    formatted_sum += str(num[2])
                                    contr += 1/(2**num[0])
                                    level = 0
                                    while contr%(1/2**level) != 0:
                                        level += 1
                                    formatted_sum += ']'*(num[0] - level) + ', '
                            print(f'After explode: {formatted_sum}')
                        break
            if not needs_reducing:
                for n, place in enumerate(snail_sum):
                    if place[2] >= 10:
                        needs_reducing = True
                        snail_sum[n] = [place[0]+1, 0, int(place[2]/2)]
                        snail_sum.insert(n+1, [place[0]+1, 1, place[2]-int(place[2]/2)])
                        if printout:
                            formatted_sum, contr, level = '', 0, 0
                            for num in snail_sum:
                                if num[1] == 0:
                                    formatted_sum += '['*(num[0] - level)
                                    contr += 1/(2**num[0])
                                    level = 0
                                    while contr%(1/2**level) != 0:
                                        level += 1
                                    formatted_sum += str(num[2]) + ', '
                                elif num[1] == 1:
                                    formatted_sum += str(num[2])
                                    contr += 1/(2**num[0])
                                    level = 0
                                    while contr%(1/2**level) != 0:
                                        level += 1
                                    formatted_sum += ']'*(num[0] - level) + ', '
                            print(f'After split: {formatted_sum}')
                        break
                
    formatted_sum, contr, level = '', 0, 0
    for num in snail_sum:
        if num[1] == 0:
            formatted_sum += '['*(num[0] - level)
            contr += 1/(2**num[0])
            level = 0
            while contr%(1/2**level) != 0:
                level += 1
            formatted_sum += str(num[2]) + ', '
        elif num[1] == 1:
            formatted_sum += str(num[2])
            contr += 1/(2**num[0])
            level = 0
            while contr%(1/2**level) != 0:
                level += 1
            formatted_sum += ']'*(num[0] - level) + ', '
    
    formatted_sum = eval(formatted_sum[:-2])
            
    magnitude  = snail_mag(formatted_sum)
    return formatted_sum, magnitude

def Day18_Part2(filename='Inputs/Day18_Inputs.txt'):
    """
    Calculates the maximum possible magnitude from adding a pair of snail numbers out of
    a list of snail numbers given in an input file. A snailfish number is an ordered list
    of two elements where each element of the pair can be either a regular number or another
    pair. To add two snailfish numbers, form a pair from the left and right parameters of
    the addition operator reduce the result. To reduce a snailfish number, you must
    repeatedly do the first action in this list that applies to the snailfish number:
        - If any pair is nested inside four pairs, the leftmost such pair explodes.
        - If any regular number is 10 or greater, the leftmost such regular number splits.
    Once no action in the above list applies, the snailfish number is reduced.

    Parameters
    ----------
    filename : str, optional
        The input file giving the list of snail numbers to be added.
        The default is 'Inputs/Day18_Inputs.txt'.

    Returns
    -------
    max_magnitude : int
        The maximum possible magnitude of the resulting snail number from adding two out of
        the input snail numbers.

    """
    file = open(filename)
    data = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            snail_num, i, level = [], 0, 0
            while i < len(line[0]):
                if line[0][i] == '[':
                    level += 1
                    i += 1
                elif line[0][i] == ']':
                    level -= 1
                    i += 1
                elif line[0][i].isnumeric():
                    reg_num = ''
                    while line[0][i].isnumeric():
                        reg_num += line[0][i]
                        i += 1
                    if line[0][i] == ',':
                        index = 0
                    else:
                        index = 1
                    snail_num.append([level, index, int(reg_num)])
                else:
                    i += 1
            data.append(snail_num)
    file.close()
    
    max_magnitude = 0
    for snail_sum in data:
        data_copy = 1*data
        data_copy.remove(snail_sum)
        for snail_num in data_copy:
            double_sum = []
            for num in snail_sum + snail_num:
                double_sum.append([num[0]+1, num[1], num[2]])
                
            needs_reducing = True
            while needs_reducing:
                needs_reducing = False
                for n, place in enumerate(double_sum):
                    if place[0] > 4:
                        needs_reducing = True
                        if place[1] == 0:
                            if n > 0:
                                double_sum[n-1][2] += place[2]
                                
                            index = sum(prev[0] == 4 for prev in double_sum[:n])%2
                            double_sum[n] = [4, index, 0]
                            
                        elif place[1] == 1:
                            if n < len(double_sum) - 1:
                                double_sum[n+1][2] += place[2]
                                
                            double_sum.remove(double_sum[n])
                            break
                if not needs_reducing:
                    for n, place in enumerate(double_sum):
                        if place[2] >= 10:
                            needs_reducing = True
                            double_sum[n] = [place[0]+1, 0, int(place[2]/2)]
                            double_sum.insert(n+1, [place[0]+1, 1, place[2]-int(place[2]/2)])
                            break
                    
            formatted_sum, contr, level = '', 0, 0
            for num in double_sum:
                if num[1] == 0:
                    formatted_sum += '['*(num[0] - level)
                    contr += 1/(2**num[0])
                    level = 0
                    while contr%(1/2**level) != 0:
                        level += 1
                    formatted_sum += str(num[2]) + ', '
                elif num[1] == 1:
                    formatted_sum += str(num[2])
                    contr += 1/(2**num[0])
                    level = 0
                    while contr%(1/2**level) != 0:
                        level += 1
                    formatted_sum += ']'*(num[0] - level) + ', '
            
            formatted_sum = eval(formatted_sum[:-2])
                    
            magnitude  = snail_mag(formatted_sum)
            if magnitude > max_magnitude:
                max_magnitude = 1*magnitude
                
    return max_magnitude