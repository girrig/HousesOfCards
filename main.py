# LINK TO PDF:   https://www.dropbox.com/s/tn5lg8jbl8ytmrt/Houses%20of%20Cards.docx?dl=0

import random
from termcolor import cprint
from operator import itemgetter


# Easy color printing functions
# colors = ['grey','red','green','yellow','blue','magenta','cyan','white']
print_grey = lambda x: cprint(x, 'grey')  # Not very visible; DONT USE
print_red = lambda x: cprint(x, 'red')  # ERRORS
print_green = lambda x: cprint(x, 'green')  # Sucessful actions
print_yellow = lambda x: cprint(x, 'yellow')  # Catching edge cases
print_blue = lambda x: cprint(x, 'blue')  # Player actions
print_magenta = lambda x: cprint(x, 'magenta')  # Test output
print_cyan = lambda x: cprint(x, 'cyan')
print_white = lambda x: cprint(x, 'white')  # Normal text


class Game:
    def __init__(self):
        # Dev variables
        self.debug = False  # Autoplay

        # Meta variables
        self.num_players = None
        self.players = []  # Array of Player objects
        self.player_going_first = None

        # Game variables
        self.active_player = None  # Player object
        self.phase = None  # 0=Setup; 1=Plotting; 2=Questing; 3=Cleanup
        self.deck = []  # Array of Card objects
        self.calamity = None  # 1-100
        self.game_over = False

    '''
    PRIMARY FUNCTIONS
    '''

    def run(self):
        # Pre-Game
        self.initGame()
        self.setupPhase()

        # GAME START

        # Game Loop
        if self.debug:
            while True:
                print_yellow('Debug mode is not implemented currently. Sorry!')
                break

        if not self.debug:
            while True:
                """
                print_grey('yo this is a ' + str(10) + ' sentence')
                print_red('yo this is a ' + str(10) + ' sentence')
                print_green('yo this is a ' + str(10) + ' sentence')
                print_yellow('yo this is a ' + str(10) + ' sentence')
                print_blue('yo this is a ' + str(10) + ' sentence')
                print_magenta('yo this is a ' + str(10) + ' sentence')
                print_cyan('yo this is a ' + str(10) + ' sentence')
                print_white('yo this is a ' + str(10) + ' sentence')
                """

                # PLOTTING PHASE
                if self.phase == 1:
                    self.plottingPhase()
                # QUESTING PHASE
                elif self.phase == 2:
                    self.questingPhase()
                # CLEANUP PHASE
                elif self.phase == 3:
                    self.cleanupPhase()
                else:
                    print_red('ERROR: Phase changing is broken!')

                # Set current phase
                if self.phase == 3:
                    self.phase = 1

                    # Set current player
                    if self.active_player.p_num == self.num_players:
                        self.active_player = self.players[0]
                    else:
                        self.active_player = self.players[self.active_player + 1]

                else:
                    self.phase = self.phase + 1

    def initGame(self):
        input = input('Enter number of players: ')

        if input == '0':
            self.debug = True
            self.num_players = 0
        else:
            self.num_players = int(input)
            for num in range(0, self.num_players):
                name = input('Enter name for Player ' + str(num + 1) + ':')
                player = Player(name, num, [0, 0, 0, 0], 0, [])
                self.players.append(player)

        self.dealDeck()
        self.shuffleDeck()

    def setupPhase(self):
        # Each player draws 3 cards
        for player in self.players:
            for i in range(3):
                player.hand.append(self.deck.pop())

        # Check for jokers
        low_num_buf = []
        for player in self.players:
            temp_tuple = (player.p_num, player.getLowestValueCard())
            low_num_buf.append(temp_tuple)
        print_magenta('low_num_buf: ' + str(low_num_buf))

        # Replace jokers
        while min(low_num_buf, key=itemgetter(1))[1] < 2:
            print_yellow('Joker detected!')
            for player in self.players:
                for card in player.hand:
                    if card.value < 2:
                        player.hand.remove(card)
                        player.hand.append(self.deck.pop())
            low_num_buf = []
            for player in self.players:
                temp_tuple = (player.p_num, player.getLowestValueCard())
                low_num_buf.append(temp_tuple)
            print_magenta('low_num_buf: ' + str(low_num_buf))

        # Each player games +1 affinity to the drawn card suits
        for player in self.players:
            for card in player.hand:
                if card.suit == 'Spade':
                    player.affinities[0] = player.affinities[0] + 1
                elif card.suit == 'Heart':
                    player.affinities[1] = player.affinities[1] + 1
                elif card.suit == 'Club':
                    player.affinities[2] = player.affinities[2] + 1
                elif card.suit == 'Diamond':
                    player.affinities[3] = player.affinities[3] + 1
                else:
                    print_red('ERROR: Affinity attribution is broken!')

        # The player with the highest value card drawn goes first
        high_num_buf = []
        for player in self.players:
            temp_tuple = (player.p_num, player.getHighestValueCard())
            high_num_buf.append(temp_tuple)
        print_magenta('high_num_buf: ' + str(high_num_buf))

        # Check for ties
        is_tie = False
        tied_player_buf = []
        for i, j in enumerate(high_num_buf):
            if j[1] == max(high_num_buf, key=itemgetter(1))[1]:
                tied_player_buf.append(j)
        if len(tied_player_buf) > 1:
            print_magenta('tied_player_buf: ' + str(tied_player_buf))
            is_tie = True

        # Keep drawing to break ties
        if is_tie:
            print_yellow('Tie detected!')
            while self.player_going_first is None:
                for player in self.players:
                    player.hand = []

                for i in range(0, len(tied_player_buf)):
                    self.players[tied_player_buf[i][0]].hand.append(self.deck.pop())

                high_num_buf = []
                print_magenta('tied_player_buf loop0: ' + str(tied_player_buf))
                for i in range(0, len(tied_player_buf)):
                    temp_tuple = (tied_player_buf[i][0], self.players[tied_player_buf[i][0]].getHighestValueCard())
                    print_magenta(str(temp_tuple))
                    high_num_buf.append(temp_tuple)
                print_magenta('high_num_buf loop: ' + str(high_num_buf))

                tied_player_buf = []
                for i, j in enumerate(high_num_buf):
                    if j[1] == max(high_num_buf, key=itemgetter(1))[1]:
                        tied_player_buf.append(j)
                print_magenta('tied_player_buf loop: ' + str(tied_player_buf))

                if len(tied_player_buf) > 1:
                    continue
                else:
                    self.player_going_first = tied_player_buf[0][0]
                    self.active_player = self.players[self.player_going_first]
        else:
            self.player_going_first = tied_player_buf[0][0]
            self.active_player = self.players[self.player_going_first]

        # Empty player hands
        for player in self.players:
            player.hand = []

        # Shuffle the deck
        self.deck = []
        self.dealDeck()
        self.shuffleDeck()

        # Each player draws 5 cards
        for player in self.players:
            for i in range(5):
                player.hand.append(self.deck.pop())

        # Set phase
        self.phase = 1

    def plottingPhase(self):
        print_white(self.active_player)
        print_white('Plotting Phase: ' + str(self.active_player.name) + '\'s turn')

        # Current player chooses 1
        while(True):
            print_white('What would you like to do?')
            print_white('1) Draw a resource card')
            print_white('2) Offer a trade to the table')
            print_white('3) Use a resource card\'s special ability')
            print_white('4) Purchase a Usurper\'s Chance card')
            input = input('Choose a number: ')

            # Current player draws a resource cards
            if input == '1':
                self.active_player.hand.append(self.deck.pop())
                break
            # Current player offers to trade to the table
            elif input == '2':
                print_yellow('Currently not implemented!')
                continue
            # Current player uses a resource cards ability
            elif input == '3':
                print_yellow('Currently not implemented!')
                continue
            # Current player buys a Usurper's Chance card
            elif input == '4':
                if self.active_player.points < 7:
                    print_red('You do not have enough victory points to purchase a Usurpers\'s Chance card! Need 7 points; you have ' + str(self.active_player.points) + ' points.')
                else:
                    print_white('Are you sure you want to buy a Usurper\'s Chance card for 7 victory points?')
                    input = input('(y/n): ')
                    if input == 'y':
                        self.active_player.points = self.active_player.points - 7
                        self.active_player.hand.append(Card(15, 'Usurper\'s Chance'))
                    break

    def questingPhase(self):
        print_white(self.active_player)
        print_white('Questing Phase: ' + str(self.active_player.name) + '\'s turn')

        # Current player chooses 1
        while(True):
            print_white('What would you like to do?')
            print_white('1) Spend a resource card and try to stop the calamity')
            print_white('2) Attempt to search for more resource cards')
            print_white('3) Activate a Usurper\'s Chance card and try to take the throne')
            input = input('Choose a number: ')

            # Current player attempts to stop calamity by spending a resource card
            if input == '1':
                card = None
                # Current player can only spend 1 resource card
                while(True):
                    print_white('^^^Your hand^^^')
                    for x in range(0, len(self.active_player.hand)):
                        print_white(str(x + 1) + ') ' + self.active_player.hand[x].getName())
                    input = input('Pick a card to use: ')
                    card = int(input) - 1
                    if self.active_player.hand[card].getSuitNum() == -1:
                        print_red('Please choose a non-joker/non-Usurper\'s Chance card.')
                        pass
                    else:
                        break

                # Current player roll 2d6+affinity for card suit
                print_white('Rolling 2d6 plus your affinity to ' + self.active_player.hand[card].suit + '(+' + str(self.active_player.affinities[self.active_player.hand[card].getSuitNum()]) + ').')
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll = die1 + die2 + self.active_player.affinities[self.active_player.hand[card].getSuitNum()]
                print_magenta(str(roll))

                # 2-6 quest failed
                if roll <= 6:
                    print_yellow('Quest failed! You rolled a ' + str(roll) + '. The calamity lives on')
                    pass
                    # Other players can barter to save the quest from failing
                        # Other player spends a resource card to add resource card value+1 to current players failed roll
                        # Current player can accept, reject, or counteroffer
                        # Player offers are asynchronous
                    # If noone helps
                        # Current player discards the played resource card
                        # End current players turn

                # 7-9 quest success
                elif roll > 6 and roll < 10:
                    while(True):
                        self.calamity_stopped = True
                        print_green('Success! You rolled a ' + str(roll) + ' and stopped the calamity.')
                        print_white('Choose a reward: ')
                        # Current player chooses 1
                        print_white('1) Gain 1 victory point')
                        print_white('2) Draw 2 resource cards')
                        input = input('Which would you like?: ')
                        # Current player gains 1 victory points
                        if input == '1':
                            print_green('You gain 1 victory point.')
                            self.active_player.points = self.active_player.points + 1
                            break
                        # Current player draws 2 resource cards
                        elif input == '2':
                            print_green('You find 2 resource cards.')
                            self.active_player.hand.append(self.deck.pop())
                            self.active_player.hand.append(self.deck.pop())
                            break
                        else:
                            print_red('Please choose reward 1 or reward 2.')

                # 10+ great success
                elif roll >= 10:
                    self.calamity_stopped = True
                    print_green('Great Success!! You rolled a ' + str(roll) + ' and stopped the calamity.')
                    print_white('You gained 1 victory point and found 1 resource card.')
                    # Current player gains 1 victory point and draws 1 resource card
                    self.active_player.points = self.active_player.points + 1
                    self.active_player.hand.append(self.deck.pop())

                del self.active_player.hand[card]
                break

            # Current player attemps to search for more recource cards
            elif input == '2':
                # Current player rolls a 2d6
                print_white('Rolling 2d6.')
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll = die1 + die2
                print_magenta(str(roll))

                # 2-6
                if roll <= 6:
                    print_red('You rolled a ' + str(roll) + ' and failed to find more resource cards.')
                    # Current player draws 0 resource cards
                # 7-9
                elif roll > 6 and roll < 10:
                    print_green('You rolled a ' + str(roll) + ' and found 1 resource card.')
                    # Current player draws 1 resource cards
                    self.active_player.hand.append(self.deck.pop())
                # 10+
                elif roll >= 10:
                    print_green('You rolled a ' + str(roll) + 'and found 2 resource cards!')
                    # Current player draws 2 resource cards
                    self.active_player.hand.append(self.deck.pop())
                    self.active_player.hand.append(self.deck.pop())

                break

            # Activate Usurper's Chance card
            elif input == '3':
                if self.active_player.getHighestValueCard() < 15:
                    print_yellow('You do not have a Usurper\'s Chance card. Please choose a different option.')
                    continue
                print_white('You attempt to take the throne!!')
                # Current player must roll 8+ on 2d6+(Up to 3 victory points)
                print_white('Would you like to wager any victory points to add a bonus to your roll? (up to +3). The victory points wagered will be consumed on use.')
                input = input('(y/n): ')
                wagered_vps = 0
                if input == 'y':
                    input = input('Hpw many victory points would you like to use? (up to 3): ')
                    if input == 1:
                        self.active_player.points = self.active_player.points - 1
                        wagered_vps = wagered_vps + 1
                    elif input == 2:
                        self.active_player.points = self.active_player.points - 2
                        wagered_vps = wagered_vps + 2
                    elif input == 3:
                        self.active_player.points = self.active_player.points - 3
                        wagered_vps = wagered_vps + 3
                    else:
                        print_red('Assigning extra victory points to Usurper\'s Chance is broken!')

                print_white('Rolling 2d6 plus any wagered victory points' + '(+' + str(wagered_vps) + ').')
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll = die1 + die2 + wagered_vps
                print_magenta(str(roll))

                # 2-7
                if roll <= 7:
                    print_red('You failed to take the throne! You rolled a ' + str(roll) + '.')
                    print_white('All other players get to draw one resource card.')
                    # All other players draw 1 resource card
                    for player in self.players:
                        if self.active_player.p_num == player.p_num:
                            pass
                        player.hand.append(self.deck.pop())
                    # Current player discards the played Usurper's Chance card
                    for card in self.active_player.hand:
                        if card.value == 15:
                            player.hand.remove(card)
                # 8+
                elif roll >= 8:
                    print_green('You roll a... ' + str(roll) + '!!!')
                    # Current player wins the game
                    print_green('You have taken the throne and won the game!')
                    self.game_over = True

                break

    def cleanupPhase(self):
        print_white(self.active_player)
        tempy = input('block')
        # Check to see if the game has been won
        # If the calamity was stopped, roll a d100 for new calamity; otherwise pass
        # If the deck is empty and all players hands are empty, the player with the most victory points wins
            # Usurper Chance cards count for 10 victory points


    '''
    UTILITY FUNCTIONS
    '''

    def dealDeck(self):
        for suit in ('Spade', 'Heart', 'Club', 'Diamond'):
            for value in range(2, 15):
                card = Card(value, suit)
                self.deck.append(card)
        joker1 = Card(1, 'Non-Colored')
        joker2 = Card(1, 'Colored')
        self.deck.append(joker1)
        self.deck.append(joker2)
        return

    def shuffleDeck(self):
        random.shuffle(self.deck)
        return

    def printDeck(self):
        for card in self.deck:
            card.getName()
        return

    def printPlayers(self):
        for player in self.players:
            player.getName()
        return


class Player:
    def __init__(self, name, p_num, affinities, points, hand):
        self.name = name
        self.p_num = p_num
        self.affinities = affinities  # Array of ints; Ordering is: Spade, Heart, Club, Diamond
        self.points = points
        self.hand = hand

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def getName(self):
        print('Player ' + str(self.p_num) + ' is ' + self.name + '.')

    def getHighestValueCard(self):
        current_highest = 0
        for card in self.hand:
            if card.value > current_highest:
                current_highest = card.value
        return current_highest

    def getLowestValueCard(self):
        current_lowest = 15  # Picked a number higher than the highest
        for card in self.hand:
            if card.value < current_lowest:
                current_lowest = card.value
        return current_lowest


class Card:
    def __init__(self, value, suit):
        self.value = value  # 1-15; where 1 is Joker, 2-10 are 2-10, and 11-14 are Jack, Queen, King, Ace respectively; 15 is the Usurper's Chance card
        self.suit = suit  # Spade, Heart, Club, Diamond for normal cards; Non-Colored, Colored for jokers; Usurper's Chance

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    # Returns a human readable string of the card
    def getName(self):
        if 1 < self.value < 11:
            return '' + str(self.value) + ' of ' + self.suit + 's'
        elif self.value == 11:
            return 'Jack of ' + self.suit + 's'
        elif self.value == 12:
            return 'Queen of ' + self.suit + 's'
        elif self.value == 13:
            return 'King of ' + self.suit + 's'
        elif self.value == 14:
            return 'Ace of ' + self.suit + 's'
        elif self.value == 1:
            return '' + self.suit + ' Joker'
        elif self.value == 15:
            return 'Usurper\'s Chance'
        else:
            print('ERROR: Something is fucked in the Card Class getName() function')

    # Returns the correct index number for the Player affinity array; if not a normal card, returns -1
    def getSuitNum(self):
        if self.suit == 'Spade':
            return 0
        elif self.suit == 'Heart':
            return 1
        elif self.suit == 'Club':
            return 2
        elif self.suit == 'Diamond':
            return 3
        else:
            return -1


if __name__ == '__main__':
    game = Game()
    game.run()
