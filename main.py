# LINK TO PDF:   https://www.dropbox.com/s/tn5lg8jbl8ytmrt/Houses%20of%20Cards.docx?dl=0

import sys
import logging
import random
from operator import itemgetter


# Setting up logger
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')


class Game:
    def __init__(self):
        # Meta variables
        self.num_players = None
        self.players = []  # Array of Player objects
        self.player_going_first = None

        # Game variables
        self.max_players = 6
        self.active_player = None  # Player object
        self.phase = None  # 0=Setup; 1=Plotting; 2=Questing; 3=Upkeep
        self.deck = []  # Array of Card objects
        self.calamity = None  # 1-100
        self.calamity_stopped = False
        self.start_endgame = False
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
        while True:

            # PLOTTING PHASE
            if self.phase == 1:
                self.plottingPhase()
            # QUESTING PHASE
            elif self.phase == 2:
                self.questingPhase()
            # UPKEEP PHASE
            elif self.phase == 3:
                self.upkeepPhase()
            else:
                logging.error('ERROR: Phase changing is broken!')

            # Set current phase
            if self.phase == 3:
                self.phase = 1

                # Set current player
                if self.active_player.p_num == self.num_players - 1:
                    self.active_player = self.players[0]
                else:
                    self.active_player = self.players[self.active_player.p_num + 1]

            else:
                self.phase = self.phase + 1

    def initGame(self):
        num_players = None
        while(True):
            num_players = input('Enter number of players(2-6): ')
            if not num_players.isdigit():
                print('Please enter a number!')
                continue
            if int(num_players) < 2:
                print('Please pick a number greater than 1.')
                continue
            if int(num_players) > self.max_players:
                print('The maximum number of players is 6. Please pick a smaller amount of players.')
                continue

            break

        self.num_players = int(num_players)
        for i in range(0, self.num_players):
            name = input('Enter name for Player ' + str(i + 1) + ':')
            player = Player(name, i, [0, 0, 0, 0], 0, [])
            self.players.append(player)

        self.dealDeck()
        self.shuffleDeck()

    def setupPhase(self):
        print('Setup Phase')
        # Each player draws 3 cards
        for player in self.players:
            for i in range(3):
                player.hand.append(self.deck.pop())

        # Check for jokers
        low_num_buf = []
        for player in self.players:
            temp_tuple = (player.p_num, player.getLowestValueCard())
            low_num_buf.append(temp_tuple)

        # Replace jokers
        while min(low_num_buf, key=itemgetter(1))[1] < 2:
            logging.debug('Joker detected!')
            for player in self.players:
                for card in player.hand:
                    if card.value < 2:
                        player.hand.remove(card)
                        player.hand.append(self.deck.pop())
            low_num_buf = []
            for player in self.players:
                temp_tuple = (player.p_num, player.getLowestValueCard())
                low_num_buf.append(temp_tuple)

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
                    logging.error('ERROR: Affinity attribution is broken!')

        # The player with the highest value card drawn goes first
        high_num_buf = []
        for player in self.players:
            temp_tuple = (player.p_num, player.getHighestValueCard())
            high_num_buf.append(temp_tuple)

        # Check for ties
        is_tie = False
        tied_player_buf = []
        for i, j in enumerate(high_num_buf):
            if j[1] == max(high_num_buf, key=itemgetter(1))[1]:
                tied_player_buf.append(j)
        if len(tied_player_buf) > 1:
            is_tie = True

        # Keep drawing to break ties
        if is_tie:
            logging.debug('Tie detected!')
            while self.player_going_first is None:
                for player in self.players:
                    player.hand = []

                for i in range(0, len(tied_player_buf)):
                    self.players[tied_player_buf[i][0]].hand.append(self.deck.pop())

                high_num_buf = []
                for i in range(0, len(tied_player_buf)):
                    temp_tuple = (tied_player_buf[i][0], self.players[tied_player_buf[i][0]].getHighestValueCard())
                    high_num_buf.append(temp_tuple)

                tied_player_buf = []
                for i, j in enumerate(high_num_buf):
                    if j[1] == max(high_num_buf, key=itemgetter(1))[1]:
                        tied_player_buf.append(j)

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
        print('Plotting Phase: ' + str(self.active_player.name) + '\'s turn')

        # Current player chooses 1
        while(True):
            print('What would you like to do?')
            print('1) Draw a resource card')
            print('2) Offer a trade to the table')
            print('3) Use a resource card\'s special ability')
            print('4) Purchase a Usurper\'s Chance card')
            choice = input('Choose a number: ')

            # Current player draws a resource cards
            if choice == '1':
                if len(self.deck) > 0:
                    self.active_player.hand.append(self.deck.pop())
                    break
                else:
                    print('The deck is empty, sorry. Please choose another option.')
                    continue
            # Current player offers to trade to the table
            elif choice == '2':
                    print('Currently not implemented!')
                    continue
                # Current player uses a resource cards ability
            elif choice == '3':
                    print('Currently not implemented!')
                    continue
                # Current player buys a Usurper's Chance card
            elif choice == '4':
                if self.active_player.points < 7:
                    print('You do not have enough victory points to purchase a Usurpers\'s Chance card! You need 7 points; you have ' + str(self.active_player.points) + ' points.')
                    print('Please choose another option.')
                    continue
                else:
                    print('Are you sure you want to buy a Usurper\'s Chance card for 7 victory points?')
                    choice = input('(y/n): ')
                    if choice == 'y':
                        self.active_player.points = self.active_player.points - 7
                        self.active_player.hand.append(Card(15, 'Usurper\'s Chance'))
                        break
                    else:
                        continue

    def questingPhase(self):
        print('Questing Phase: ' + str(self.active_player.name) + '\'s turn')

        # Current player chooses 1
        while(True):
            print('What would you like to do?')
            print('1) Spend a resource card and try to stop the calamity')
            print('2) Attempt to search for more resource cards')
            print('3) Activate a Usurper\'s Chance card and try to take the throne')
            choice = input('Choose a number: ')

            # Current player attempts to stop calamity by spending a resource card
            if choice == '1':
                card = None
                # Current player can only spend 1 resource card
                while(True):
                    print('^^^Your hand^^^')
                    for i in range(0, len(self.active_player.hand)):
                        print(str(i + 1) + ') ' + self.active_player.hand[i].getName())
                    card_picked = input('Pick a card to use: ')
                    if not card_picked.isdigit():
                        print('Please enter a number!')
                        continue
                    if int(card_picked) < 1:
                        print('Please pick a number greater than 0.')
                        continue
                    if int(card_picked) > len(self.active_player.hand):
                        print('Please pick a number not greater than your hand size.')
                        continue
                    card = int(card_picked) - 1
                    if self.active_player.hand[card].getSuitNum() == -1:
                        print('Please choose a non-joker/non-Usurper\'s Chance card.')
                        continue

                    break

                # Current player roll 2d6+affinity for card suit
                print('Rolling 2d6 plus your affinity to ' + self.active_player.hand[card].suit + '(+' + str(self.active_player.affinities[self.active_player.hand[card].getSuitNum()]) + ').')
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll = die1 + die2 + self.active_player.affinities[self.active_player.hand[card].getSuitNum()]

                # 2-6 quest failed
                if roll <= 6:
                    print('Quest failed! You rolled a ' + str(roll) + '. The calamity lives on.')
                    # Other players can barter to save the quest from failing
                        # Other player spends a resource card to add resource card value+1 to current players failed roll
                        # Current player can accept, reject, or counteroffer
                        # Player offers are asynchronous
                    # If noone helps
                        # Current player discards the played resource card
                        # End current players turn

                # 7-9 quest success
                elif roll > 6 and roll < 10:
                    print('Success! You rolled a ' + str(roll) + ' and stopped the calamity.')
                    self.calamity_stopped = True
                    while(True):
                        print('Choose a reward: ')
                        # Current player chooses 1
                        print('1) Gain 1 victory point')
                        print('2) Draw 2 resource cards')
                        choice = input('Which would you like?: ')
                        # Current player gains 1 victory points
                        if choice == '1':
                            print('You gain 1 victory point.')
                            self.active_player.points = self.active_player.points + 1
                            break
                        # Current player draws 2 resource cards
                        elif choice == '2':
                            if len(self.deck) > 0:
                                print('The deck is empty, sorry. Please choose another option.')
                                continue
                            elif len(self.deck) == 1:
                                print('You only found one card. The deck is now empty.')
                                self.active_player.hand.append(self.deck.pop())
                            else:
                                print('You find 2 resource cards.')
                                for i in range(2):
                                    self.active_player.hand.append(self.deck.pop())
                            break
                        else:
                            print('Please choose a reward.')
                            continue

                # 10+ great success
                elif roll >= 10:
                    self.calamity_stopped = True
                    print('Great Success!! You rolled a ' + str(roll) + ' and stopped the calamity.')
                    # Current player gains 1 victory point and draws 1 resource card
                    if len(self.deck) > 0:
                        print('You gained 1 victory point and found 1 resource card.')
                        self.active_player.points = self.active_player.points + 1
                        self.active_player.hand.append(self.deck.pop())
                    else:
                        print('You gained 1 victory point but could not draw a resource card. The deck is now empty.')
                        self.active_player.points = self.active_player.points + 1

                del self.active_player.hand[card]
                break

            # Current player attempts to search for more recource cards
            elif choice == '2':
                if len(self.deck) <= 0:
                    print('The deck is empty, sorry. Please choose another option.')
                    continue

                # Current player rolls a 2d6
                print('Rolling 2d6.')
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll = die1 + die2

                # 2-6
                if roll <= 6:
                    print('You rolled a ' + str(roll) + ' and failed to find more resource cards.')
                    # Current player draws 0 resource cards
                    pass
                # 7-9
                elif roll > 6 and roll < 10:
                    print('You rolled a ' + str(roll) + ' and found 1 resource card.')
                    # Current player draws 1 resource cards
                    self.active_player.hand.append(self.deck.pop())
                # 10+
                elif roll >= 10:
                    # Current player draws 2 resource cards
                    if len(self.deck) == 1:
                        print('You rolled a ' + str(roll) + ' but could only draw one resource card. The deck is now empty.')
                        self.active_player.hand.append(self.deck.pop())
                    else:
                        print('You rolled a ' + str(roll) + 'and found 2 resource cards!')
                        for i in range(2):
                            self.active_player.hand.append(self.deck.pop())

                break

            # Activate Usurper's Chance card
            elif choice == '3':
                if self.active_player.getHighestValueCard() < 15:
                    print('You do not have a Usurper\'s Chance card. Please choose a different option.')
                    continue

                print('You attempt to take the throne!!')
                # Current player must roll 8+ on 2d6+(Up to 3 victory points)
                wagered_vps = 0
                while(True):
                    print('Would you like to wager any victory points to add a bonus to your roll? (up to +3). Any victory points wagered will be consumed.')
                    print('Current number of victory points: ' + str(self.active_player.points))
                    choice = input('(y/n): ')
                    if choice == 'y':
                        choice = input('How many victory points would you like to wager? (up to 3): ')
                        if choice == 1:
                            if self.active_player.points < 1:
                                print('You do not have at least 1 victory point.')
                                continue
                            else:
                                self.active_player.points = self.active_player.points - 1
                                wagered_vps = wagered_vps + 1
                                break
                        elif choice == 2:
                            if self.active_player.points < 2:
                                print('You do not have at least 2 victory points.')
                                continue
                            else:
                                self.active_player.points = self.active_player.points - 2
                                wagered_vps = wagered_vps + 2
                                break
                        elif choice == 3:
                            if self.active_player.points < 3:
                                print('You do not have at least 3 victory points.')
                                continue
                            else:
                                self.active_player.points = self.active_player.points - 3
                                wagered_vps = wagered_vps + 3
                                break
                        else:
                            print('Please enter a number between 1 and 3 if you would like to wager victory points.')

                    else:
                        print('You wager no victory points.')
                        break

                print('Rolling 2d6 plus any wagered victory points' + '(+' + str(wagered_vps) + ').')
                die1 = random.randint(1, 6)
                die2 = random.randint(1, 6)
                roll = die1 + die2 + wagered_vps

                # 2-7
                if roll <= 7:
                    print('You failed to take the throne! You rolled a ' + str(roll) + '.')
                    print('All other players get to draw 1 resource card.')
                    # If not enough cards for everyone, start endgame
                    if len(self.deck) < self.num_players - 1:
                        print('Not everyone can draw a card. Proceeding to the endgame.')
                        self.start_endgame = True
                    # All other players draw 1 resource card
                    else:
                        for player in self.players:
                            if self.active_player.p_num == player.p_num:
                                continue
                            player.hand.append(self.deck.pop())

                    # Current player discards the played Usurper's Chance card
                    for card in self.active_player.hand:
                        if card.value == 15:
                            player.hand.remove(card)
                # 8+
                elif roll >= 8:
                    print('You roll a... ' + str(roll) + '!!!')
                    # Current player wins the game
                    print('You have taken the throne and won the game!')
                    self.game_over = True

                break

    def upkeepPhase(self):
        print('Upkeep Phase')

        # Check to see if the game has been won
        if self.game_over is True:
            print('Thanks for playing!')
            sys.exit()

        # If the calamity was stopped, roll a d100 for new calamity; otherwise pass
        if self.calamity_stopped is True:
            print('A new calamity arises.')
            num = random.randint(1, 100)
            self.calamity = num
            self.calamity_stopped = False

        # If the deck is empty and all players hands are empty, end the game
        if (len(self.deck) == 0 and len([1 for hand in self.players.hand if len(hand)]) == 0) or (self.start_endgame is True):
            # Start the point tally; winner is determined by the most vicotry points
            final_point_totals = []
            for player in self.players:
                final_points = 0
                # Usurper Chance cards are worth 10 victory points
                while player.getHighestValueCard() == 15:
                    for card in player.hand:
                        if card.value == 15:
                            del self.player.hand[card]
                            final_points = final_points + 10

                final_points = final_points + player.points
                temp = (player.p_num, final_points)
                final_point_totals.append(temp)

            # Determine winner
            winner_buf = []
            for i, j in enumerate(final_point_totals):
                if j[1] == max(final_point_totals, key=itemgetter(1))[1]:
                    winner_buf.append(j)
            if len(winner_buf) == 1:
                print('The winner is ' + str(self.players[winner_buf[0][0]].getName()) + 'with ' + str(winner_buf[0][1]) + ' victory points!')
            elif len(winner_buf) > 1:
                print('There is a tie!')
                print('The winners with ' + str(winner_buf[0][0]) + ' victory points are: ')
                for p_num, points in winner_buf:
                    print(str(self.players[p_num].getName()))
            else:
                logging.error('Winner determination is broken!')

            print('Thanks for playing!')
            sys.exit()

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
            logging.error('ERROR: Something is fucked in the Card Class getName() function')

    # Returns the correct index number for the Player affinity array; if not a suited card, returns -1
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
