import shlex
import itertools

def Day21_Part1(filename='Inputs/Day21_Inputs.txt'):
    """
    Calculates the product of the score of the losing player of a dice game by the number
    of times the dice was rolled during the game. In the game there are two players, who
    take turns moving a pawn around a circular board of 10 spaces, and who start at
    different positions on the board as specified in an input file. On each player's turn,
    the player rolls the die three times and adds up the results. Then, the player moves
    their pawn that many times forward around the track (that is, moving clockwise on
    spaces in order of increasing value, wrapping back around to 1 after 10). After each
    player moves, they increase their score by the value of the space their pawn stopped
    on. Players start the game on a score of 0 and the game immediately ends as a win for
    any player whose score reaches at least 1000. This game uses a 100-sided dice which
    always rolls 1 first, then 2, then 3, and so on up to 100, after which it starts over
    at 1 again.

    Parameters
    ----------
    filename : str, optional
        Input file giving the starting position of each player.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    product : int
        The product of the score of the losing player of a dice game by the number of times
        the dice was rolled during the game.

    """

    file = open(filename)
    positions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            positions.append(int(line[-1]))
    file.close()

    dice, dice_rolls, player, scores = 1, 0, 0, [0, 0]
    while not any(score >= 1000 for score in scores):
        for i in range(3):
            positions[player] = ((positions[player] + dice - 1)%10) + 1
            dice_rolls += 1
            dice = (dice + 1)%100
        scores[player] += positions[player]
        player = (player + 1)%2

    product = min(scores)*dice_rolls
    return product

class GameState:
    def __init__(self, status):
        """
        Initialise the class with one parameter.

        Parameters
        ----------
        status : list of int
            Status of the game in the form [Player 1 position, Player 2 position,
                                            Player 1 score, Player 2 score].

        """
        self.status = status
    
    def __repr__(self):
        """
        Return the representation of a GameState object.

        Returns
        -------
        str
            Representation.

        """
        return f'{self.__class__.__name__}({self.status[0]}, {self.status[1]}, {self.status[2]}, {self.status[3]})'
    
    def __hash__(self):
        """
        Override the hash function for a GameState object.

        Returns
        -------
        int
            The hash of the GameState.

        """
        return hash((self.status[0], self.status[1], self.status[2], self.status[3]))

    def __eq__(self, other):
        """
        Overrides the == operator for a GameState object.

        Parameters
        ----------
        other : GameState
            The GameState object to which we are comparing.

        Returns
        -------
        bool
            Whether the two GameStates are equivalent or not.

        """
        return (self.status) == (other.status)

    def __ne__(self, other):
        """
        Overrides the != operator for a GameState object.

        Parameters
        ----------
        other : GameState
            The GameState object to which we are comparing.

        Returns
        -------
        bool
            Whether the two GameStates are different or not.

        """
        return not(self == other)
    
    def __pos__(self):
        """
        Return a copy of the GameState.
        """
        return self.__class__(self.status)

def Day21_Part2(filename='Inputs/Day21_Inputs.txt'):
    """
    Calculates the number of universes in which the player who wins a dice game in the most
    universes wins the game. In the game there are two players, who take turns moving a
    pawn around a circular board of 10 spaces, and who start at different positions on the
    board as specified in an input file. On each player's turn, the player rolls the die
    three times and adds up the results. Then, the player moves their pawn that many times
    forward around the track (that is, moving clockwise on spaces in order of increasing
    value, wrapping back around to 1 after 10). After each player moves, they increase
    their score by the value of the space their pawn stopped on. Players start the game on
    a score of 0 and the game immediately ends as a win for any player whose score reaches
    at least 21. However, this game now uses a 3-sided Dirac dice. This is a quantum die:
    when you roll it, the universe splits into multiple copies, one copy for each possible
    outcome of the die.

    Parameters
    ----------
    filename : str, optional
        Input file giving the starting position of each player.
        The default is 'Inputs/Day21_Inputs.txt'.

    Returns
    -------
    most_wins : int
        The number of universes in which the player who wins a dice game in the most
        universes wins the game

    """

    file = open(filename)
    positions = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            positions.append(int(line[-1]))
    file.close()

    possible_rolls = dict()
    for rolls in set(itertools.combinations([1, 2, 3]*3, 3)):
        try:
            possible_rolls[sum(rolls)] += 1
        except:
            possible_rolls[sum(rolls)] = 1

    # status = [position1, position2, score1, score2]
    all_states, wins = {GameState([positions[0], positions[1], 0, 0]) : 1}, [0, 0]
    while len(all_states) > 0:
        new_states = dict()
        for state in all_states:
            new_states, wins = possible_outcomes(state, all_states[state], possible_rolls, new_states, wins)
    
        all_states = new_states.copy()

    wins[0] = int(wins[0]/27)
    most_wins = max(wins)
    return most_wins

def possible_outcomes(state, number, possible_rolls, new_states, wins):
    """
    Calculates every possible outcome from both players having a turn each from the given
    game state, and adds the resulting game states to a dictionary, or adds to the number
    of wins if a player's score becomes >= 21.

    Parameters
    ----------
    state : GameState
        The initial state of the game.
    number : int
        The number of universes which have this current state.
    possible_rolls : dict {int : int}
        Dictionary mapping the possible total movements from 3 dice rolls to the number
        of universes in which a given total roll will be obtained.
    new_states : dict {GameState : int}
        Dictionary mapping all the possible game states discovered to the number of
        universes which have this game state.
    wins : list of ints
        The numbers of wins so far by each player, in the form [Player 1 Wins,
                                                                Player 2 Wins].

    Returns
    -------
    new_states : dict {GameState : int}
        Dictionary mapping all the possible game states discovered to the number of
        universes which have this game state.
    wins : list of ints
        The numbers of wins so far by each player, in the form [Player 1 Wins,
                                                                Player 2 Wins].

    """

    total_possibles = []
    for i in range(2):
        possibles = []
        for total_roll in possible_rolls:
            num = possible_rolls[total_roll]
            pos = ((state.status[i] + total_roll - 1)%10) + 1
            score = state.status[i + 2] + pos
            possibles.append([num, pos, score])
        total_possibles.append(possibles)

    for outcome in itertools.product(total_possibles[0], total_possibles[1]):
        if outcome[0][2] >= 21:
            wins[0] += number * outcome[0][0] * outcome[1][0]
        elif outcome[1][2] >= 21:
            wins[1] += number * outcome[0][0] * outcome[1][0]
        else:
            new_state = GameState([outcome[0][1], outcome[1][1], outcome[0][2],
                                   outcome[1][2]])
            try:
                new_states[new_state] += number * outcome[0][0] * outcome[1][0]
            except:
                new_states[new_state] = number * outcome[0][0] * outcome[1][0]

    return new_states, wins
