# LINK TO PDF:   https://www.dropbox.com/s/tn5lg8jbl8ytmrt/Houses%20of%20Cards.docx?dl=0

import random
from termcolor import colored, cprint
from operator import itemgetter

# DEV GLOBALS
debug = False  # Autoplay

# META GLOBALS
num_players = None
players = []  # Array of Player objects
player_going_first = None

# GAME GLOBALS
cur_player = None  # Starts at 0
phase = None  # 0=Setup; 1=Plotting; 2=Questing; 3=Cleanup
deck = []  # Array of Card objects
calamity = None  # 1-100

# Easy color printing functions
#colors = ['grey','red','green','yellow','blue','magenta','cyan','white']
print_grey = lambda x: cprint(x, 'grey')  # Does not work well
print_red = lambda x: cprint(x, 'red')
print_green = lambda x: cprint(x, 'green')
print_yellow = lambda x: cprint(x, 'yellow')
print_blue = lambda x: cprint(x, 'blue')
print_magenta = lambda x: cprint(x, 'magenta')
print_cyan = lambda x: cprint(x, 'cyan')
print_white = lambda x: cprint(x, 'white')



class Player:
    def __init__(self, name, p_num, affinities, points, hand):
        self.name = name
        self.p_num = p_num
        self.affinities = affinities  #Array of ints; Ordering is: Spade, Heart, Club, Diamond
        self.points = points
        self.hand = hand

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def getName(self):
        print 'Player ' + str(self.p_num) + ' is ' + self.name + '.'

    def getHighestValueCard(self):
        current_highest = 0
        for card in self.hand:
            if card.value > current_highest:
                current_highest = card.value
        return current_highest

class Card:
    def __init__(self, value, suit):
        self.value = value  # 1-13; where 1 is Joker, 2-10 are 2-10, and 11-14 are Jack, Queen, King, Ace respectively
        self.suit = suit

    def __str__(self):
        return str(self.__dict__)

    def __repr__(self):
        return self.__str__()

    def getName(self):
        if 1 < self.value < 11:
            print 'The card is the ' + str(self.value) + ' of ' + self.suit + 's.'
        elif self.value == 11:
            print 'The card is the Jack of ' + self.suit + 's.'
        elif self.value == 12:
            print 'The card is the Queen of ' + self.suit + 's.'
        elif self.value == 13:
            print 'The card is the King of ' + self.suit + 's.'
        elif self.value == 14:
            print 'The card is the Ace of ' + self.suit + 's.'
        elif self.value == 1:
            print 'The card is the ' + self.suit + ' Joker.'
        else:
            print 'ERROR: Something is fucked in the Card Class getName() function'

def printPlayers():
    for player in players:
        player.getName()
    return

def dealDeck():
    for suit in ('Spade','Heart','Club','Diamond'):
        for value in xrange(2,14):
            card = Card(value, suit)
            deck.append(card)
    joker1 = Card(1, 'Non-Colored')
    joker2 = Card(1, 'Colored')
    deck.append(joker1)
    deck.append(joker2)
    return

def shuffleDeck():
    random.shuffle(deck)
    return

def printDeck():
    for card in deck:
        card.getName()
    return

def initGame():
    dealDeck()
    shuffleDeck()
    return



# START
initGame()



input = raw_input('Enter number of players: ')

if input == '0':
    debug = True
    num_players = 0
else:
    num_players = int(input)
    for num in xrange(0,num_players):
        name = raw_input('Enter name for Player ' + str(num+1) + ':' )
        player = Player(name, num, [0,0,0,0], 0, [])
        players.append(player)



# GAME START

# Game Loop
if debug:
    while True:
        print_red('Debug mode is not implemented currently. Sorry!')
        break

if not debug:
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

        #Set current player
        if cur_player == None:
            cur_player = 0
        elif cur_player == num_players:
            cur_player = 0
        else:
            cur_player = cur_player + 1

        #Set current phase
        if phase == None:
            phase = 0
        elif phase == 3:
            phase = 1
        else:
            phase = phase + 1

        # SETUP PHASE
        if phase == 0:
            #Each player draws 3 cards
            for player in players:
                for i in xrange(3):
                    player.hand.append(deck.pop())

            #Each player games +1 affinity to the drawn card suits
            for player in players:
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

            #The player with the highest value card drawn goes first
            high_num_buf = []
            for player in players:
                temp_tuple = (player.p_num, player.getHighestValueCard())
                high_num_buf.append(temp_tuple)
            for num in xrange(len(high_num_buf)):
                max(high_num_buf,key=itemgetter(1))
            is_tie = False
            tied_player_buf = []
            for i,j in enumerate(high_num_buf):
                if j[1] == max(high_num_buf,key=itemgetter(1))[1]:
                    tied_player_buf.append(j)
            if len(tied_player_buf) > 1:
                is_tie = True

            #Keep drawing to break ties
            if is_tie:
                while player_going_first == None:
                    for player in players:
                        player.hand = []

                    for i in xrange(0,len(tied_player_buf)-1):
                        players[tied_player_buf[i][0]].hand.append(deck.pop())

                    high_num_buf = []
                    for player in players:
                        temp_tuple = (player.p_num, player.getHighestValueCard())
                        high_num_buf.append(temp_tuple)
                    for num in xrange(len(high_num_buf)):
                        max(high_num_buf,key=itemgetter(1))
                    tied_player_buf = []
                    for i,j in enumerate(high_num_buf):
                        if j[1] == max(high_num_buf,key=itemgetter(1))[1]:
                            tied_player_buf.append(j)

                    if len(tied_player_buf) > 1:
                        pass
                    else:
                        player_going_first = tied_player_buf[0][0]

            #Empty player hands
            for player in players:
                player.hand = []

            #Shuffle the deck
            deck = []
            dealDeck()
            shuffleDeck()

            #Each player draws 5 cards
            for player in players:
                for i in xrange(5):
                    player.hand.append(deck.pop())

        # PLOTTING PHASE
        elif phase == 1:
            print_green('Got to phase 1')
            print_white(players[0])
            print_white(players[1])
            pass
            #Choose 1
                #Current player draws a resource cards
                #Current player offers to trade to the table
                #Current player uses a resource cards ability
                #Current player buys a Usurper's Chance card

        # QUESTING PHASE
        elif phase == 2:
            pass
            #Current player chooses 1
                #Current player attempts to stop calamity by spending a resource card
                    #Current player can only spend 1 resource card
                    #Current player roll 2d6+affinity for card suit
                        #2-6 quest failed
                            #Other players can barter to save the quest from failing
                                #Other player spends a resource card to add resource card value+1 to current players failed roll
                                #Current player can accept, reject, or counteroffer
                                #Player offers are asynchronous
                            #If noone helps
                                #Current player discards the played resource card
                                #End current players turn
                        #7-9 quest success
                            #Current player chooses 1
                                #Current player gains 1 victory points
                                #Current player draws 2 resource cards
                        #10+
                            #Current player gains 1 victory point and draws 1 resource card
                #Current player attemps to search for more recource cards
                    # Current player rolls a 2d6
                        #2-6
                            #Current player draws 0 resource cards
                        #7-9
                            #Current player draws 1 resource cards
                        #10+
                            #Current player draws 2 resource cards
                #Activate Usurper's Chance card
                    #Current player must roll 8+ on 2d6+(Up to 3 victory points)
                        #2-7
                            #All other players draw 1 resource card
                            #Current player discards the played Usurper's Chance card
                        #8+
                            #Current player wins the game

        # CLEANUP PHASE
        elif phase == 3:
            tempy = input('block')
            #If the calamity was stopped, roll a d100 for new calamity; otherwise pass
            #If the deck is empty and all players hands are empty, the player with the most victory points wins
                #Usurper Chance cards count for 10 victory points

        else:
            print_red('ERROR: Phase changing is broken!')
