import shlex

def Day16_Part1(filename='Inputs/Day16_Inputs.txt'):
    """
    Calculates the sum of the version numbers in all packets of a hexadecimal-encoded BITS
    transmission, as given in an input file, once it is decoded.

    Parameters
    ----------
    filename : str, optional
        Input file giving the encoded transmission.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    version_total : int
        The sum of the version numbers in all packets.

    """
    file = open(filename)
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data = line[0]
    file.close()
    binary_data = ''
    for hexa in data:
        binary = bin(int(hexa, base=16))[2:]
        if len(binary)%4 != 0:
            binary = '0'*(4-(len(binary)%4)) + binary
        binary_data += binary
    version_total = 0
    while '1' in binary_data:
        packet_version = int(binary_data[:3], base=2)
        version_total += packet_version
        type_id = int(binary_data[3:6], base=2)
        if type_id == 4:
            binary_data = binary_data[6:]
            while binary_data[0] == '1':
                binary_data = binary_data[5:]
            binary_data = binary_data[5:]
        else:
            length_id = int(binary_data[6])
            if length_id == 0:
                binary_data = binary_data[22:]
            elif length_id == 1:
                binary_data = binary_data[18:]
    
    return version_total

def Day16_Part2(filename='Inputs/Day16_Inputs.txt'):
    """
    Calculates the result of evaluating the expression represented by a hexadecimal-encoded
    BITS transmission, as given in an input file, once it is decoded.

    Parameters
    ----------
    filename : str, optional
        Input file giving the encoded transmission.
        The default is 'Inputs/Day16_Inputs.txt'.

    Returns
    -------
    result : int
        The result of evaluating the decoded expression.

    """
    file = open(filename)
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            data = line[0]
    file.close()
    binary_data = ''
    for hexa in data:
        binary = bin(int(hexa, base=16))[2:]
        if len(binary)%4 != 0:
            binary = '0'*(4-(len(binary)%4)) + binary
        binary_data += binary
    level = 0
    type_id = int(binary_data[3:6], base=2)
    packet = [type_id]
    length_id = int(binary_data[6])
    if length_id == 0:
        length = int(binary_data[7:22], base=2)
        binary_data = binary_data[22:]
        binary_data, sub_length, sub_packet = process_set_len(binary_data, length, level+1)
        packet += sub_packet
    elif length_id == 1:
        number = int(binary_data[7:18], base=2)
        binary_data = binary_data[18:]
        binary_data, sub_length, sub_packet = process_set_num(binary_data, number, level+1)
        packet += sub_packet
        
    if packet[0] == 0: #sum
        packet = '(' + ' + '.join(packet[1:]) + ')'
        
    elif packet[0] == 1: #product
        packet = '(' + ' * '.join(packet[1:]) + ')'
        
    elif packet[0] == 2: #min
        packet = 'min([' + ', '.join(packet[1:]) + '])'
        
    elif packet[0] == 3: #max
        packet = 'max([' + ', '.join(packet[1:]) + '])'
        
    elif packet[0] == 5: #>
        packet = '(' + ' > '.join(packet[1:]) + ')'
        
    elif packet[0] == 6: #<
        packet = '(' + ' < '.join(packet[1:]) + ')'
        
    elif packet[0] == 7: #==
            packet = '(' + ' == '.join(packet[1:]) + ')'
            
    result = int(eval(packet))
    return result

def process_set_len(binary_data, max_len, level):
    """
    Decodes the sub-packets given in a packet with a length type ID of 0, meaning that the
    sub-packets contained in the packet have a set total length in bits.

    Parameters
    ----------
    binary_data : str
        The remaining binary data from the outermost packet that is still to be parsed.
    max_len : int
        The total length in bits of the sub-packets in this packet.
    level : int
        The current level of recursion into the sub-packets.

    Returns
    -------
    binary_data : str
        The remaining binary data from the outermost packet that is still to be parsed.
    curr_length : int
        The total length in bits contained in this sub-packet.
    packet : list of strings
        List of the objects contained in the current sub-packet.

    """
    curr_length, packet = 0, []
    while curr_length < max_len:
        type_id = int(binary_data[3:6], base=2)
        curr_length += 6
        if type_id == 4:
            binary_data, literal = binary_data[6:], ''
            while binary_data[0] == '1':
                literal += binary_data[1:5]
                binary_data = binary_data[5:]
                curr_length += 5
            literal += binary_data[1:5]
            binary_data = binary_data[5:]
            curr_length += 5
            packet.append(str(int(literal, base=2)))
        else:
            sub_packet = [type_id]
            length_id = int(binary_data[6])
            curr_length += 1
            if length_id == 0:
                length = int(binary_data[7:22], base=2)
                binary_data = binary_data[22:]
                curr_length += 15
                binary_data, sub_length, sub_packet_contents = process_set_len(binary_data, length, level+1)
                sub_packet += sub_packet_contents
                curr_length += sub_length
                if sub_packet[0] == 0: #sum
                    sub_packet = '(' + ' + '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 1: #product
                    sub_packet = '(' + ' * '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 2: #min
                    sub_packet = 'min([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 3: #max
                    sub_packet = 'max([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 5: #>
                    sub_packet = '(' + ' > '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 6: #<
                    sub_packet = '(' + ' < '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 7: #==
                    sub_packet = '(' + ' == '.join(sub_packet[1:]) + ')'
            
                packet.append(sub_packet)
    
            elif length_id == 1:
                number = int(binary_data[7:18], base=2)
                binary_data = binary_data[18:]
                curr_length += 11
                binary_data, sub_length, sub_packet_contents = process_set_num(binary_data, number, level+1)
                sub_packet += sub_packet_contents
                curr_length += sub_length
                if sub_packet[0] == 0: #sum
                    sub_packet = '(' + ' + '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 1: #product
                    sub_packet = '(' + ' * '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 2: #min
                    sub_packet = 'min([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 3: #max
                    sub_packet = 'max([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 5: #>
                    sub_packet = '(' + ' > '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 6: #<
                    sub_packet = '(' + ' < '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 7: #==
                    sub_packet = '(' + ' == '.join(sub_packet[1:]) + ')'
            
                packet.append(sub_packet)
                
    return binary_data, curr_length, packet

def process_set_num(binary_data, max_num, level):
    """
    Decodes the sub-packets given in a packet with a length type ID of 1, meaning that there
    are a set number of sub-packets contained in the packet.

    Parameters
    ----------
    binary_data : str
        The remaining binary data from the outermost packet that is still to be parsed.
    max_num : int
        The total number of sub-packets in this packet.
    level : int
        The current level of recursion into the sub-packets.

    Returns
    -------
    binary_data : str
        The remaining binary data from the outermost packet that is still to be parsed.
    curr_length : int
        The total length in bits contained in this sub-packet.
    packet : list of strings
        List of the objects contained in the current sub-packet.

    """
    curr_number, curr_length, packet = 0, 0, []
    while curr_number < max_num:
        type_id = int(binary_data[3:6], base=2)
        curr_length += 6
        if type_id == 4:
            binary_data, literal = binary_data[6:], ''
            while binary_data[0] == '1':
                literal += binary_data[1:5]
                binary_data = binary_data[5:]
                curr_length += 5
            literal += binary_data[1:5]
            binary_data = binary_data[5:]
            curr_length += 5
            packet.append(str(int(literal, base=2)))
        else:
            sub_packet = [type_id]
            length_id = int(binary_data[6])
            curr_length += 1
            if length_id == 0:
                length = int(binary_data[7:22], base=2)
                binary_data = binary_data[22:]
                curr_length += 15
                binary_data, sub_length, sub_packet_contents = process_set_len(binary_data, length, level+1)
                sub_packet += sub_packet_contents
                curr_length += sub_length
                if sub_packet[0] == 0: #sum
                    sub_packet = '(' + ' + '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 1: #product
                    sub_packet = '(' + ' * '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 2: #min
                    sub_packet = 'min([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 3: #max
                    sub_packet = 'max([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 5: #>
                    sub_packet = '(' + ' > '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 6: #<
                    sub_packet = '(' + ' < '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 7: #==
                    sub_packet = '(' + ' == '.join(sub_packet[1:]) + ')'
            
                packet.append(sub_packet)
    
            elif length_id == 1:
                number = int(binary_data[7:18], base=2)
                binary_data = binary_data[18:]
                curr_length += 11
                binary_data, sub_length, sub_packet_contents = process_set_num(binary_data, number, level+1)
                sub_packet += sub_packet_contents
                curr_length += sub_length
                if sub_packet[0] == 0: #sum
                    sub_packet = '(' + ' + '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 1: #product
                    sub_packet = '(' + ' * '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 2: #min
                    sub_packet = 'min([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 3: #max
                    sub_packet = 'max([' + ', '.join(sub_packet[1:]) + '])'
                    
                elif sub_packet[0] == 5: #>
                    sub_packet = '(' + ' > '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 6: #<
                    sub_packet = '(' + ' < '.join(sub_packet[1:]) + ')'
                    
                elif sub_packet[0] == 7: #==
                    sub_packet = '(' + ' == '.join(sub_packet[1:]) + ')'
            
                packet.append(sub_packet)
        curr_number += 1
                
    return binary_data, curr_length, packet
