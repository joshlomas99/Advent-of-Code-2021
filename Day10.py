import shlex

def Day10_Part1(filename='Inputs/Day10_Inputs.txt'):
    """
    Calculates the total syntax error score of all corrupted lines in a set of lines of
    characters given in an input file. Each line contains a series of opening ['(', '[',
    '{', '<'] and closing [')', ']', '}', '>'] brackets, and a corrupted line is one
    where a closing character appears with no matching opening character. The syntax
    error score of such a line depends on the unexpected character which was encountered,
    according to: {')' : 3, ']' : 57, '}' : 1197, '>' : 25137}.

    Parameters
    ----------
    filename : str, optional
        Input file containing the lines of characters.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    syntax_error_score : int
        Total syntax error score of all corrupted lines in the input file.

    """
    file = open(filename)
    lines = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            lines.append(line)
    file.close()
    
    start_chars = ['(', '[', '{', '<']
    end_chars = [')', ']', '}', '>']
    scores = [3, 57, 1197, 25137]
    
    corrupted_chunks, unexpected_chars, syntax_error_score = [], [], 0
    for chunks in lines:
        openers = []
        for char in chunks[0]:            
            if char == '(' or char == '[' or char == '{' or char == '<':
                openers.append(char)
                
            else:
                if len(openers) == 0:
                    corrupted_chunks.append(chunks[0])
                    unexpected_chars.append(char)
                    syntax_error_score += scores[end_chars.index(char)]
                    break
                
                elif end_chars[start_chars.index(openers[-1])] == char:
                    openers.pop(-1)
                    continue
                
                else:
                    corrupted_chunks.append(chunks[0])
                    unexpected_chars.append(char)
                    syntax_error_score += scores[end_chars.index(char)]
                    break
        
    return syntax_error_score

def Day10_Part2(filename='Inputs/Day10_Inputs.txt'):
    """
    Calculates the median autocomplete score of all incomplete lines in a set of lines of
    characters given in an input file. Each line contains a series of opening ['(', '[',
    '{', '<'] and closing [')', ']', '}', '>'] brackets, and an incomplete line is one
    which is not corrupted (wher a closing character appears with no matching opening
    character), but the line ends with some opening characters still not having matching
    closing characters. The autocomplete score is the calculated from the list of closing
    characters required to complete the line, by multiplying the current value of the score
    of a line, starting at 0, by 5, and then adding the value of the next closing character
    required in that line, according to: {')' : 1, ']' : 2, '}' : 3, '>' : 4}.

    Parameters
    ----------
    filename : str, optional
        Input file containing the lines of characters.
        The default is 'Inputs/Day10_Inputs.txt'.

    Returns
    -------
    middle_score : int
        Median autocorrect score of all incomplete lines in the input file.

    """
    file = open(filename)
    lines = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            lines.append(line)
    file.close()
    
    start_chars = ['(', '[', '{', '<']
    end_chars = [')', ']', '}', '>']
    scores = [1, 2, 3, 4]
    
    completion_string_scores = []
    for chunks in lines:
        counts, openers, corrupted = [0, 0, 0, 0], [], False
        for char in chunks[0]:
            if char == '(' or char == '[' or char == '{' or char == '<':
                openers.append(char)
                
            else:
                if len(openers) == 0:
                    corrupted = True
                    break
                
                elif end_chars[start_chars.index(openers[-1])] == char:
                    openers.pop(-1)
                    continue
                
                else:
                    corrupted = True
                    break
                
        if not corrupted and len(openers) > 0:
            completion_string_score = 0
            for remaining_char in openers[::-1]:
                completion_string_score *= 5
                completion_string_score += scores[start_chars.index(remaining_char)]
            completion_string_scores.append(completion_string_score)
    
    completion_string_scores.sort()
    middle_score = completion_string_scores[int((len(completion_string_scores)-1)/2)]
    return middle_score