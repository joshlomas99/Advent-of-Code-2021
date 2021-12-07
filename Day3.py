import shlex
import math
import numpy as np

def bin_to_dec(n):
    """
    Convert a binary (base 2) number to a decimal (base 10) number.

    Parameters
    ----------
    n : int or str
        Binary number to be converted.

    Returns
    -------
    out : int
        Converted base 10 number.

    """
    n, out, power = str(n), 0, 0
    while len(n) > 0:
        curr = int(n[-1])
        out += curr*(2**power)
        n = n[:-1]
        power += 1
    return out

def Day3_Part1(filename='Inputs/Day3_Inputs.txt'):
    """
    Determines the power consumption of the submarine, calculated as the product
    of the gamma and epsilon rates, whose values are determined from a diagnostic report
    containing a list of binary number provided in an input file. Gamma (epsilon) are
    determined by finding the most (least) common bit in each corresponding bit position
    in the diagnostic report.

    Parameters
    ----------
    filename : str, optional
        Input file containing the diagnostic report.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    tuple (str, str)
        (gamma, epsilon) in binary format.
    tuple (int, int)
        (gamma, epsilon) in decimal format.
    power_consumption : int
        Power consumption of submarine (product of gamma and epsilon rates in decimal
        format).

    """
    file = open(filename)
    binary = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            binary.append(line[0])
    file.close()
    
    gamma, epsilon = "", ""
    for i in range(len(binary[0])):
        zero_count, one_count = 0, 0
        for b in binary:
            if b[i] == '0':
                zero_count += 1
            if b[i] == '1':
                one_count += 1
        if zero_count > one_count:
            gamma += '0'
            epsilon += '1'
        else:
            gamma += '1'
            epsilon += '0'
    
    dec_gamma = bin_to_dec(gamma)
    dec_epsilon = bin_to_dec(epsilon)
    power_consumption = dec_gamma*dec_epsilon
    return (gamma, epsilon), (dec_gamma, dec_epsilon), power_consumption

def Day3_Part2(filename='Inputs/Day3_Inputs.txt'):
    """
    Determines the life support rating of the submarine, calculated as the product
    of the oxygen generator rating and the CO2 scrubber rating, which are determined
    from a diagnostic report containing a list of binary number provided in an input
    file. The oxygen (CO2) rating is determined by eliminating numbers from the
    diagnostic report with the least (most) common value of a corresponding bit,
    starting with the first bit.

    Parameters
    ----------
    filename : str, optional
        Input file containing the diagnostic report.
        The default is 'Inputs/Day3_Inputs.txt'.

    Returns
    -------
    tuple (str, str)
        (oxygen, co2) in binary format.
    tuple (int, int)
        (oxygen, co2) in decimal format.
    life_support_rating : int
        Product of oxygen and CO2 ratings in decimal format.

    """
    file = open(filename)
    binary = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            binary.append(line[0])
    file.close()

    # calculate oxygen generator rating
    binary_oxygen, binary_co2 = 1*binary, 1*binary
    oxygen, co2 = False, False
    for i in range(len(binary_oxygen[0])):
        zero_count, one_count = 0, 0
        for b in binary_oxygen:
            if b[i] == '0':
                zero_count += 1
            if b[i] == '1':
                one_count += 1
        if zero_count > one_count:
            most_common = '0'
            least_common = '1'
        else:
            most_common = '1'
            least_common = '0'
        binary_oxygen_keep = []
        if not oxygen:
            for b in binary_oxygen:
                if b[i] == most_common:
                    binary_oxygen_keep.append(b)
            binary_oxygen = 1*binary_oxygen_keep
            if len(binary_oxygen) == 1:
                oxygen = binary_oxygen[0]
        if oxygen:
            break
                
    # calculate C02 scrubber rating
    for i in range(len(binary_co2[0])):
        zero_count, one_count = 0, 0
        for b in binary_co2:
            if b[i] == '0':
                zero_count += 1
            if b[i] == '1':
                one_count += 1
        if zero_count > one_count:
            most_common = '0'
            least_common = '1'
        else:
            most_common = '1'
            least_common = '0'
        binary_co2_keep = []
        if not co2:
            for b in binary_co2:
                if b[i] == least_common:
                    binary_co2_keep.append(b)
            binary_co2 = 1*binary_co2_keep
            if len(binary_co2) == 1:
                    co2 = binary_co2[0]
        if co2:
            break
    
    dec_oxygen = bin_to_dec(oxygen)
    dec_co2 = bin_to_dec(co2)
    life_support_rating = dec_oxygen*dec_co2
    return (oxygen, co2), (dec_oxygen, dec_co2), life_support_rating
                
                
    