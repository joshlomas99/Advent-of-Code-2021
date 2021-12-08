import shlex

def Day8_Part1(filename='Inputs/Day8_Inputs.txt'):
    """
    Calculates the number of times the digits 1, 4, 7, or 8 appear in a list of output
    values given in an input file, where each digit is represented by up to 7 letters,
    each of which represent a segment on a seven-segment display, but the position of
    each letter on the display is not known.

    Parameters
    ----------
    filename : str, optional
        Input file giving the letters which correspond to each of the ten possible
        numbers on the seven segment display, followed by letters specifying four
        output numbers.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    unique_length_digits : int
        The number of times 1, 4, 7 or 8 appear in the output numbers.

    """
    file = open(filename)
    digits = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            digits.append(line)
    file.close()
    
    all_digits, output = [], []
    for digit_set in digits:
        for i in range(len(digit_set)):
            if digit_set[i] == '|':
                all_digits.append(digit_set[:i])
                output.append(digit_set[i+1:])
                
    unique_length_digits = 0
    for output_set in output:
        for output_digit in output_set:
            if len(output_digit) <= 4 or len(output_digit) == 7:
                unique_length_digits += 1
            
    return unique_length_digits

def Day8_Part2(filename='Inputs/Day8_Inputs.txt'):
    """
    Calculates the sum of the output values given in an input file, where each digit in
    each value is represented by up to 7 letters, each of which represent a segment on
    a seven-segment display, but the position of each letter on the display is not known.

    Parameters
    ----------
    filename : str, optional
        Input file giving the letters which correspond to each of the ten possible
        numbers on the seven segment display, followed by letters specifying four
        output numbers.
        The default is 'Inputs/Day8_Inputs.txt'.

    Returns
    -------
    output_sum : int
        The sum of the output values.

    """
    file = open(filename)
    digits = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            digits.append(line)
    file.close()
    
    all_digits, output = [], []
    for digit_set in digits:
        for i in range(len(digit_set)):
            if digit_set[i] == '|':
                all_digits.append(digit_set[:i])
                output.append(digit_set[i+1:])
    
    output_sum = 0
    for index, digit_set in enumerate(all_digits):
        possible_digits = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        digit_nums = [0, 0, 0, 0, 0, 0, 0]
        for n, digit in enumerate(digit_set):
            for char in digit:
                digit_nums[possible_digits.index(char)] += 1
            if len(digit) == 2:
                one = n
            if len(digit) == 3:
                seven = n
            if len(digit) == 4:
                four = n
            if len(digit) == 7:
                eight = n  
                
        top_left = possible_digits[digit_nums.index(6)]
        possible_digits.pop(digit_nums.index(6))
        digit_nums.pop(digit_nums.index(6))
        bottom_left = possible_digits[digit_nums.index(4)]
        possible_digits.pop(digit_nums.index(4))
        digit_nums.pop(digit_nums.index(4))
        bottom_right = possible_digits[digit_nums.index(9)]
        possible_digits.pop(digit_nums.index(9))
        digit_nums.pop(digit_nums.index(9))
        
        for char in digit_set[seven]:
            if digit_set[one].find(char) < 0:
                top = char
                digit_nums.pop(possible_digits.index(top))
                possible_digits.pop(possible_digits.index(top))
        
        top_right = possible_digits[digit_nums.index(8)]
        possible_digits.pop(digit_nums.index(8))
        digit_nums.pop(digit_nums.index(8))
        
        for char in digit_set[four]:
            if digit_set[one].find(char) < 0:
                try:
                    middle = possible_digits.pop(possible_digits.index(char))
                    break
                except:
                    continue
        
        bottom = possible_digits[0]
        
        possible_numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        number_segments = []
        #0
        zero = top + top_right + bottom_right + bottom + bottom_left + top_left
        number_segments.append(''.join(sorted(zero)))
        #1
        one = top_right + bottom_right
        number_segments.append(''.join(sorted(one)))
        #2
        two = top + top_right + middle + bottom_left + bottom
        number_segments.append(''.join(sorted(two)))
        #3
        three = top + top_right + middle + bottom_right + bottom
        number_segments.append(''.join(sorted(three)))
        #4
        four = top_left + middle + top_right + bottom_right
        number_segments.append(''.join(sorted(four)))
        #5
        five = top + top_left + middle + bottom_right + bottom
        number_segments.append(''.join(sorted(five)))
        #6
        six = top + top_left + bottom_left + bottom + bottom_right + middle
        number_segments.append(''.join(sorted(six)))
        #7
        seven = top + top_right + bottom_right
        number_segments.append(''.join(sorted(seven)))
        #8
        eight = top + top_right + bottom_right + bottom + bottom_left + top_left + middle
        number_segments.append(''.join(sorted(eight)))
        #9
        nine = top + top_left + middle + top_right + bottom_right + bottom
        number_segments.append(''.join(sorted(nine)))
        
        output_number = ''
        for output_digit in output[index]:
            output_number += possible_numbers[number_segments.index(''.join(sorted(output_digit)))]
        
        output_sum += int(output_number)
        
    return output_sum