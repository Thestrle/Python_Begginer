import random
#import Deck

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':4, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

isPlaying = True


###################################
class Cards():

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank +" of "+self.suit


###################################
class Deck():

    def __init__(self):
        self.deck =[]
        for suit in suits:
            for rank in ranks:
                self.deck.append(Cards(suit,rank))

    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n'+card.__str__()
        return "The Deck has "+ deck_comp

# In place shuffle. Will not return any thing but shuffle the existing deck
    def shuffle(self):
        random.shuffle(self.deck)

# To get a single card for hit
    def deal(self):
        single_card = self.deck.pop()
        return single_card
##################
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0

    def add_card(self,card):
        #card passed in from Deck.deal() --> Single Card(suit, rank)
        self.cards.append(card)
        self.value += values[card.rank]
      # Track Aces
        if card.rank == 'Ace':
            self.aces += 1

    # If total Value > 21 and I still have an Ace
    # Then change my Ace  to be 1 instead of 11
    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

##################
class Chips:

    def __init__(self,total=100):
        self.total = total # This can be set to a default value or supplied by a user player_input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet
##################
def take_bet(chips):

    while True:
        try:
            chips.bet = int(input("How many chips would you like to bet?: "))

        except:
            print("Please provide an Integer number")
        else:
            if chips.bet > chips.total:
                print("Sorry! You dont have enough chips. You have {} chips".format(chips.total))
            else:
                break

def hit(deck,hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global isPlaying

    while True:
        x = input("Hit or Stand? Press h or s: " )

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() == 's':
            print("Player stands, Dealer's Turn")
            isPlaying = False
        else:
            print("Sorry I did not understand. Please enter h or s only.")
            continue
        break
def show_some(player,dealer):
    print("\n Dealer's Hand:\n")
    print(" <card hidden> ")
    print('\n',dealer.cards[1])
    print("\n Player's Hand:", *player.cards, sep='\n ')

def show_all(player,dealer):
    print("\n Dealer's Hand:", *dealer.cards, sep='\n ')
    print("Dealer's Hand =\n",dealer.value)
    print("\n Dealer's Hand:", *player.cards, sep='\n ')
    print("Dealer's Hand =\n",player.value)


def player_busts(player,dealer,chips):
    print("Bust Player!")
    chips.lose_bet()

def platyer_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Player wins! Dealer Busted")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and player tie. PUSH!")


##################
#Game Logic
while True:
    print("Welcome to BlackJack Game!!!")

    # Create the Deck shuffle it and give two cards to player and dealer each.
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # setup player's chip
    player_chips = Chips()
    #Prompt the player for their bet
    take_bet(player_chips)

    # show Cards but keep one dealer card hidden
    show_some(player_hand,dealer_hand)

    #If playervExceeds 21 , run player busts anf break out of Loop
    if player_hand.value > 21:
        player_busts(player_hand,dealer_hand,chips)
        break

    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        #show all Cards(suit, rank)
        show_all(player_hand,dealer_hand)

        #Run different winning Scenarios:
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            platyer_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)

    #Inform player of their chis total
    print("\n Player's total chips are at : {}".format(player_chips.total))
    #Ask player if he wants to play again
    new_game = input("Would you like to play another hand? y/n?: ")

    if new_game[0].lower() == 'y':
        isPlaying = True
        continue

    else:
        print("Thank you for playing.:)")
        break
