import Cards
import random

class Deck():

    suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
    ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
    values = {'Two':2, 'Three':3, 'Four':4, 'Five':4, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

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
