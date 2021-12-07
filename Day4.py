import shlex

class Bingo:
    """
    Class defining a n x m bingo card, initialised with a list of m rows containing
    n numbers each. Methods are provided to determine if bingo (a full row or column
    of numbers) has been achieved for a given list of called numbers, and to determine
    the sum of the unmarked numbers on the card for a given list of called numbers.
    """
    def __init__(self, bingo_card):
        """
        Initialise the class with one parameter.

        Parameters
        ----------
        bingo_card : list of lists of int
            list of m rows containing n integers defining an n x m bingo card.

        Returns
        -------
        None.

        """
        self.rows = bingo_card
        self.columns = [[bingo_card[j][i] for j in range(len(bingo_card))] for i in range(len(bingo_card[0]))]
    
    def check_bingo(self, numbers_called):
        """
        Determine whether bingo (a full row or column of numbers) has been achieved
        for a given list of called numbers.

        Parameters
        ----------
        numbers_called : list of int
            List of numbers which have been called and should be marked off the bingo
            card.

        Returns
        -------
        Bingo? : bool
            Whether bingo has been achieved or not.

        """
        for row in self.rows:
            bingo = True
            for num in row:
                if numbers_called.count(num) == 0:
                    bingo = False
                    break
            if bingo:
                return True
        for column in self.columns:
            bingo = True
            for num in column:
                if numbers_called.count(num) == 0:
                    bingo = False
                    break
            if bingo:
                return True
        return False
    
    def check_unmarked(self, numbers_called):
        """
        Determine the sum of the unmarked numbers on the card for a given list of
        called numbers.

        Parameters
        ----------
        numbers_called : list of int
            List of numbers which have been called and should be marked off the bingo
            card.

        Returns
        -------
        uncalled_sum : int
            Sum of the unmarked numbers on the card.

        """
        uncalled_sum = 0
        for row in self.rows:
            for num in row:
                if numbers_called.count(num) == 0:
                    uncalled_sum += num
        return uncalled_sum
        

def Day4_Part1(filename='Inputs/Day4_Inputs.txt'):
    """
    Determine the score of the first bingo card to achieve bingo out of a set given in
    an input file, for called numbers as given in the same input file. The score of a
    bingo card is the last number called for this card to achieve bingo, multiplied by
    the sum of the unmarked numbers on the card at this point.

    Parameters
    ----------
    filename : str, optional
        Input file containing the numbers called and the bingo cards.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    score : int
        The score of the first card to achieve bingo, where the score is the last number
        called for this card to achieve bingo, multiplied by the sum of the unmarked
        numbers on the card at this point.

    """
    file = open(filename)
    bingo = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            bingo.append(line)
    file.close()
    
    numbers_called, i = [], 0
    while i < len(bingo[0][0]):
        curr_num = ''
        while i < len(bingo[0][0]) and bingo[0][0][i] != ',':
            curr_num += bingo[0][0][i]
            i += 1
        numbers_called.append(int(curr_num))
        i += 1
        
    bingo_cards = []
    for n, row in enumerate(bingo[1:]):
        int_row = []
        for i in row:
            int_row.append(int(i))
        if n%5 == 0:
            bingo_cards.append([int_row])
        else:
            bingo_cards[-1].append(int_row)
    for n, card in enumerate(bingo_cards):
        bingo_cards[n] = Bingo(card)
    
    called = []
    for call in numbers_called:
        called.append(call)
        for card_num, card in enumerate(bingo_cards):
            if card.check_bingo(called):
                score = call*card.check_unmarked(called)
                return score
                
def Day4_Part2(filename='Inputs/Day4_Inputs.txt'):
    """
    Determine the score of the last bingo card to achieve bingo out of a set given in
    an input file, for called numbers as given in the same input file. The score of a
    bingo card is the last number called for this card to achieve bingo, multiplied by
    the sum of the unmarked numbers on the card at this point.

    Parameters
    ----------
    filename : str, optional
        Input file containing the numbers called and the bingo cards.
        The default is 'Inputs/Day4_Inputs.txt'.

    Returns
    -------
    score : int
        The score of the last card to achieve bingo, where the score is the last number
        called for this card to achieve bingo, multiplied by the sum of the unmarked
        numbers on the card at this point.

    """
    file = open(filename)
    bingo = []
    for line in file:
        line = line.strip()
        line = shlex.split(line)
        if len(line) > 0:
            bingo.append(line)
    file.close()
    
    numbers_called, i = [], 0
    while i < len(bingo[0][0]):
        curr_num = ''
        while i < len(bingo[0][0]) and bingo[0][0][i] != ',':
            curr_num += bingo[0][0][i]
            i += 1
        numbers_called.append(int(curr_num))
        i += 1
        
    bingo_cards = []
    for n, row in enumerate(bingo[1:]):
        int_row = []
        for i in row:
            int_row.append(int(i))
        if n%5 == 0:
            bingo_cards.append([int_row])
        else:
            bingo_cards[-1].append(int_row)
    for n, card in enumerate(bingo_cards):
        bingo_cards[n] = Bingo(card)
    
    i, called, completed = 0, [], []
    while len(bingo_cards) > 0 and i < len(numbers_called):
        called.append(numbers_called[i])
        for card_num, card in enumerate(bingo_cards):
            if card.check_bingo(called):
                bingo_cards.remove(card)
                completed.append(card)
        i += 1
    score = called[-1]*completed[-1].check_unmarked(called)
    return score
                