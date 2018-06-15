# LINK TO PDF:   https://www.dropbox.com/s/tn5lg8jbl8ytmrt/Houses%20of%20Cards.docx?dl=0

import random
from termcolor import colored, cprint

# DEV GLOBALS
debug = False  # Autoplay

# META GLOBALS
num_players = None
players = []  # Array of Player objects

# GAME GLOBALS
cur_player = None  # No Player 0
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
        self.affinities = affinities
        self.points = points
        self.hand = hand

    def getName(self):
        print 'Player ' + str(self.p_num) + ' is ' + self.name + '.'

class Card:
    def __init__(self, value, suit):
        self.value = value  # 1-13; where 1 is joker, 2-10 are 2-10, and 11-14 are Jack, Queen, King, Ace respectively
        self.suit = suit

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
            print 'ERROR: something is fucked in the getName() function'

def printPlayers():
    for player in players:
        player.getName()
    return

def createDeck():
    for suit in ('Diamond','Heart','Spade','Club'):
        for num in xrange(2,14):
            card = Card(num, suit)
            deck.append(card)
    joker1 = Card(1, 'Non-Colored')
    joker2 = Card(1, 'Colored')
    deck.append(joker1)
    deck.append(joker2)
    return

def shuffleCards():
    random.shuffle(deck)
    return

def printDeck():
    for card in deck:
        card.getName()
    return

def initGame():
    createDeck()
    shuffleCards()
    return



# START
initGame()



input = raw_input('Enter number of players: ')

if input == '0':
    debug = True
else:
    num_players = int(input)
    for num in xrange(1,num_players+1):
        name = raw_input('Enter name for Player ' + str(num) + ':' )
        player = Player(name, num, [], 0, [])
        players.append(player)



# GAME START
phase = 0

# Game Loop
if debug:
    while True:
        print_red('Debug mode is not implemented currently. Sorry!')
        break

if not debug:
    while True:
        print_grey('yo this is a ' + str(10) + ' sentence')
        print_red('yo this is a ' + str(10) + ' sentence')
        print_green('yo this is a ' + str(10) + ' sentence')
        print_yellow('yo this is a ' + str(10) + ' sentence')
        print_blue('yo this is a ' + str(10) + ' sentence')
        print_magenta('yo this is a ' + str(10) + ' sentence')
        print_cyan('yo this is a ' + str(10) + ' sentence')
        print_white('yo this is a ' + str(10) + ' sentence')

        #Set current player
        #cur_player = 1

        # SETUP PHASE
        if phase == 0:
            #Each player draws 3 cards
            #Each player games +1 affinity to the drawn card suits
            #The player with the highest value card drawn goes first
                #Keep drawing to break ties
            #Empty player hands
            #Shuffle the deck
            #Each player draws 5 cards

        # PLOTTING PHASE
        if phase == 1:
            #Choose 1
                #Current player draws a resource cards
                #Current player offers to trade to the table
                #Current player uses a resource cards ability
                #Current player buys a Usurper's Chance card

        # QUESTING PHASE
        if phase == 2:
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
        if phase == 3:
            #If the calamity was stopped, roll a d100 for new calamity; otherwise pass
            #If the deck is empty and all players hands are empty, the player with the most victory points wins
                #Usurper Chance cards count for 10 victory points
