def get_input(input_file: str='Inputs/Day24_Inputs.txt') -> list:
    """
    Parse an input file to extract a program consisting of a list of instructions, one per line.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the program.
        The default is 'Inputs/Day24_Inputs.txt'.

    Returns
    -------
    program : list(list(str))
        List of instructions contained in the program.

    """
    # Parse input file, strip and split each line
    with open(input_file) as f:
        program = [line.strip().split() for line in f.readlines()]

    return program

def execute_instruction(instruction: str, variables: list, registers: dict, inputs: str,
                        input_index: int) -> tuple:
    """
    Execute a given instruction on given variables to alter the values of given registers. If the
    inp instruction is used then the value in the input at the given input_index is used.

    Instructions
    ------------
    There are six supported instructions:
        inp a - Read an input value and write it to variable a.

        add a b - Add the value of a to the value of b, then store the result in variable a.

        mul a b - Multiply the value of a by the value of b, then store the result in variable a.

        div a b - Divide the value of a by the value of b, truncate the result to an integer, then
        store the result in variable a. (Here, "truncate" means to round the value toward zero.)

        mod a b - Divide the value of a by the value of b, then store the remainder in variable a.
        (This is also called the modulo operation.)

        eql a b - If the value of a and b are equal, then store the value 1 in variable a.
        Otherwise, store the value 0 in variable a.

    Parameters
    ----------
    instruction : str
        Instruction to execute.
    variables : list(str)
        List of variables to use in instruction.
    registers : dict(str: int)
        Dictionary of registers with their current values, in the form {register: value}.
    inputs : iterable(str)
        Iterable of input values in the form of strings.
    input_index : int
        Current index from which to take a value from the input.

    Raises
    ------
    Exception: Invalid division
        If division by 0 is attempted.
    Exception: Invalid modulus
        If modulus using negative or zero values is attempted.

    Returns
    -------
    registers : dict(str: int)
        Dictionary of registers with their values after the instruction is executed, in the form
        {register: value}.
    input_index : int
        Index from which to take a value from the input, after the instruction is executed.

    """
    # For inp instruction
    if instruction == 'inp':
        # Assign the register corresponding to the given variable, to the current input value,
        # and increment the input_index
        registers[variables[0]] = int(inputs[input_index])
        return registers, input_index + 1
    # For all other instructions, expect two variables
    else:
        # If second variable is a register value, retrieve it
        if variables[1].isalpha():
            b = registers[variables[1]]
        # Else convert to an integer
        else:
            b = int(variables[1])

    # Perform addition
    if instruction == 'add':
        registers[variables[0]] += b
    # Perform multiplication
    elif instruction == 'mul':
        registers[variables[0]] *= b
    # Perform division, handling required exception
    elif instruction == 'div':
        if b == 0:
            raise Exception('Invalid division {registers[variables[0]]} / {b}!')
        registers[variables[0]] //= b
    # Perform modulus, handling required exception
    elif instruction == 'mod':
        if registers[variables[0]] < 0 or b <= 0:
            raise Exception('Invalid modulus {registers[variables[0]]} % {b}!')
        registers[variables[0]] %= b
    # Perform equality
    elif instruction == 'eql':
        registers[variables[0]] = int(registers[variables[0]] == b)
        
    return registers, input_index

def execute_program(registers: dict, program: list, inputs: int) -> dict:
    """
    Execute all the lines of a given program, on registers which start at given values, with a
    given input to increment across.

    Parameters
    ----------
    registers : dict(str: int)
        Dictionary of registers with their initial values, in the form {register: value}.
    program : list(list(str))
        List of instructions contained in the program.
    input : iterable(str)
        Iterable of input values in the form of strings.

    Returns
    -------
    registers : dict(str: int)
        Dictionary of registers with their values after the program is executed, in the form
        {register: value}.

    """
    # Create copy of registers
    registers = registers.copy()
    # Start at the beginning of the input
    input_index = 0

    # Execute each line of the program
    for line in program:
        registers, input_index = execute_instruction(line[0], line[1:], registers, inputs,
                                                     input_index)

    return registers

###################################################################################################
#
# This puzzle can't be solved by just testing every possible value, as there are too many.
# Instead, it can be solved by noticing that the input program is actually an almost perfectly
# repeating sequence of 18 instruction, which repeat 14 times, with each round of 18 instructions
# acting on the next value in the input.
# When the 18 instructions are simplified, they amount to:
#
# x = NOT(z%26 + v1 == w)
# z //= v2
# y = 25x + 1
# z *= y
# y = (w + v3)*x
# z += y
#
# where w is the current input value. Then v1, v2, and v3 are three variables which change between
# the different repetitions of these instructions. Together with w these are the only things that
# change each time. v1 and v3 change between several different values (between -13 and 14 and 0 and
# 16 respectively), while v2 changes between 1 and 26. The key to solving this is noticing how the
# values of x and v2 affect z.
#
# Being boolean, x is always either 0 or 1, depending on how the values of z, v1 and w currently
# relate to each other. When x is 1 the above instructions become:
#
# z //= v2
# z *= 26
# z += w + v3
#
# so clearly whatever the value of v2, z will increase away from zero here, which we want to avoid
# given our target value of zero. However, when x is 0 we instead get:
#
# z //= v2
#
# which either has no effect on z or decreases it by at least a factor of 26, depending on v2.
#
# Therefore, the key to keeping the value of z as low as possible lies in ensuring that x = 0
# whenever possible, particularly when v2 = 26. Therefore we must choose input values w_n such that
# z%26 + v1 == w_n as often as possible.
#
# Starting with registers x, y, z = 0, 0, 0 we can see what happens when applying these
# instructions, using our puzzle input as an example where in round 1 we have
# v1_1, v2_1, v3_1 = 13, 1, 8.
# Since z%26 = 0 here, clearly we cannot have x = 0 since that would required w_1 = 13, when it is
# limited to between 1 and 9. Therefore, after round 1 we have:
#
# x = 1
# z //= v2_1 (1) -> 0
# z *= 26 -> 0
# y = w_1 + v3_1 = w_1 + 8
# z += y -> w_1 + 8
#
# Now in round 2 we have v1_2, v2_2, v3_2 = 12, 1, 16. So now when determining if we can have x = 0
# we consider z%26, which equals (w_1 + v3_1)%26, but since 1 <= w <= 9 and 0 <= v3 <= 16, we have
# 1 <= w + v3 <= 25, i.e. always below 26. Therefore we always now have z%26 = w_1 + v3_1.
# Therefore, for x = 0 we require w_1 + v3_1 + v1_2 == w_2, which in this example means
# w_2 = w_1 + 20, which is clearly impossible since w_2 can be at most 9 and w_1 can be at least 1,
# so we could have at most w_2 = w_1 + 8 to allow for x = 0. So, again we have x = 1, giving after
# round 2 of instructions:
#
# x = 1
# z //= v2_2 (1) -> w_1 + 8
# z *= 26 -> 26*(w_1 + 8)
# y = w_2 + v3_2 = w_2 + 16
# z += y -> 26*(w_1 + 8) + w_2 + 16
#
# so z is beginning to grow larger. Now for round 3 we have v1_3, v2_3, v3_3 = 10, 1, 4 and we have
# z%26 = w_2 + 16 since the component including w_1 is clearly divisible by 26, and w_2 + 16 is
# always < 26 as previously discussed. So for x = 0 we now require w_2 + v3_2 + v1_3 == w_3, which
# in this example means w_3 = w_2 + 26, which again is clearly impossible. So, again we have x = 1,
# giving after round 3 of instructions:
#
# x = 1
# z //= v2_3 (1) -> 26*(w_1 + 8) + w_2 + 16
# z *= 26 -> 26*(26*(w_1 + 8) + w_2 + 16)
# y = w_3 + v3_3 = w_3 + 4
# z += y -> 26*(26*(w_1 + 8) + w_2 + 16) + w_3 + 4
#
# so z continues to grow larger. However, in round 4 we see the key to the solution. Now we have
# v1_4, v2_4, v3_4 = -11, 26, 1 so immediately we have the potential to decrease z since v2 = 26.
# So we have z%26 = w_3 + 4, since again the components containing w_1 and w_2 are clearly divisble
# by 26, and  w_3 + 4 < 26. So for x = 0 we now require w_3 + v3_3 + v1_4 == w_4, which
# in this example means w_4 = w_3 - 7, which is actually possible. So now we can use x = 0 given
# the condition that w_4 = w_3 - 7. So using x = 0 in round 4 we get:
#
# x = 0
# z //= v2_4 (26) -> 26*(w_1 + 8) + w_2 + 16 since w_3 + 4 < 26
# y = 0
#
# so z has finally decreased, with the condition that w_4 = w_3 - 7. When continuing through the
# rest of the instructions, we find that there are 7 rounds with v2 = 26 where x = 0 is possible,
# and 7 rounds where v2 = 1 where x = 0 is impossible. Due to the trade off of z *= 26 and z //= 26
# in these two scenarios, we can therefore achieve z = 0 at the end, given 7 different conditions
# for the seven different rounds allowing x = 0.
#
# We can observe that these conditions all take the form w_n + v3_n + v1_m == w_m, where m is the
# current round number where v2_m = 26, and n is the round number whose corresponding input is
# currently at the surface of z, i.e. added on after the component which is muliplied by 26.
# Therefore, we can construct these conditions easily by going through the rounds and tracking
# which inputs are contained in z on any given round, by adding the current round's input to the
# surface if v2 = 1, and popping the surface input off if v2 = 26. Then on rounds where v2 = 26
# we construct a new condition using the inputs and variables corresponding to the current round,
# and the round whose input forms the surface component of z at that point.
#
# Then, from these 7 conditions, every possible value of the input which gives z = 0 can be
# extracted, and we find that every single input value from w_1 to w_14 appears exactly once in
# these conditions, leaving no free variables.
#
###################################################################################################

def get_variables(program: list, round_index: int) -> list:
    """
    Extract from the given program, the values of the free variables v1, v2 and v3 for the current
    round of instructions.

    Parameters
    ----------
    program : list(list(str))
        List of instructions contained in the program.
    round_index : int
        The index of the current round.

    Returns
    -------
    variables : list(int)
        List of the free variables for the current round in the form [v1, v2, v3] as discussed
        above.

    """
    # Extract variables in required order
    variables = [int(program[18*round_index + i][2]) for i in [5, 4, 15]]
    return variables

def get_links(program: list) -> list:
    """
    Use the logic described above to parse the given program and extract the 7 conditions which
    give z = 0 after the program has been run.

    Parameters
    ----------
    program : list(list(str))
        List of instructions contained in the program.

    Raises
    ------
    Exception: Unexpected variable value
        If v2 has a value that isn't 1 or 26.

    Returns
    -------
    links : list(tuple(int))
        List of the conditions in the form (n, dw, m), such that the correponding condition is
        w_n + dw = w_m (where here n and m go from 0-13, unlike in the above explanation where they
        go from 1-14).

    """
    # Track the different components of z in each round
    z_components = []
    links = []
    # For each round of instructions
    for i in range(14):
        # Get the free variables for the current round
        variables = get_variables(program, i)
        # If v2 == 1 then add the input for this round and the corresponding value of v3 to the
        # surface of z
        if variables[1] == 1:
            z_components.append((i, variables[2]))
        # Else if v2 == 26 then remove the surface component of z, and use it along with the
        # current input and value of v1 to construct a new condition
        elif variables[1] == 26:
            popped = z_components.pop(-1)
            dw = popped[1] + variables[0]
            # Add the new condition to the list
            links.append((popped[0], dw, i))
        else:
            raise Exception(f'Unexpected variable value {variables[1]}')

    # We expect 7 different conditions
    assert len(links) == 7
    # We expect every input to appear once
    assert set(links[i][j] for j in [0, 2] for i in range(7)) == set(range(14))

    return links

def Day24_Part1(input_file: str='Inputs/Day24_Inputs.txt') -> int:
    """
    Finds the largest 14-digit model number accepted by the MOdel Number Automatic Detector
    program (MONAD), as given in an input file. The number should be given as input to MONAD, with
    registers w, x, y and z, all starting at 0, and the number is valid if register z ends at 0.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the MONAD program.
        The default is 'Inputs/Day24_Inputs.txt'.

    Returns
    -------
    max_model_number : int
        The largest 14-digit model number accepted by MONAD.

    """
    # Parse the input file to extract the program
    program = get_input(input_file)

    # Use the logic described above to extract the 7 conditions constraining the input values
    links = get_links(program)
    
    mod_num_components = [0]*14
    # For each link we have two input numbers and a value dw between them. Therefore, to maximise
    # the number we take the higher of these two numbers and set that to 9, and then calculate the
    # other number from the condition
    for link in links:
        if link[1] < 0:
            mod_num_components[link[0]] = 9
            mod_num_components[link[2]] = 9 + link[1]
        else:
            mod_num_components[link[2]] = 9
            mod_num_components[link[0]] = 9 - link[1]

    # Join the inputs to form the full model number and run it through the MONAD program,
    # requiring z == 0 at the end
    max_model_number = ''.join([str(i) for i in mod_num_components])
    registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    assert execute_program(registers, program, max_model_number)['z'] == 0

    # Convert to integer and return
    return int(max_model_number)

def Day24_Part2(input_file: str='Inputs/Day24_Inputs.txt') -> int:
    """
    Finds the smallest 14-digit model number accepted by the MOdel Number Automatic Detector
    program (MONAD), as given in an input file. The number should be given as input to MONAD, with
    registers w, x, y and z, all starting at 0, and the number is valid if register z ends at 0.

    Parameters
    ----------
    input_file : str, optional
        Input file containing the MONAD program.
        The default is 'Inputs/Day24_Inputs.txt'.

    Returns
    -------
    min_model_number : int
        The smallest 14-digit model number accepted by MONAD.

    """
    # Parse the input file to extract the program
    program = get_input(input_file)
    
    # Use the logic described above to extract the 7 conditions constraining the input values
    links = get_links(program)
    
    mod_num_components = [0]*14
    # For each link we have two input numbers and a value dw between them. Therefore, to minimise
    # the number we take the lower of these two numbers and set that to 1, and then calculate the
    # other number from the condition
    for link in links:
        if link[1] < 0:
            mod_num_components[link[2]] = 1
            mod_num_components[link[0]] = 1 - link[1]
        else:
            mod_num_components[link[0]] = 1
            mod_num_components[link[2]] = 1 + link[1]
    
    # Join the inputs to form the full model number and run it through the MONAD program,
    # requiring z == 0 at the end
    min_model_number = ''.join([str(i) for i in mod_num_components])
    registers = {'w': 0, 'x': 0, 'y': 0, 'z': 0}
    assert execute_program(registers, program, min_model_number)['z'] == 0
    
    # Convert to integer and return
    return int(min_model_number)
