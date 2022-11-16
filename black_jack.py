# %%
## Black Jack Card Game, play against computer 'Dealer'

import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 
        'Jack':10,'Queen':10, 'King':10, 'Ace':11}

playing = True

# %%
# CARD

class Card:

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return self.rank + " of " + self.suit



# %%
class Deck:

    def __init__(self):

        self.deck = []

        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit,rank))
    
    def __str__(self):
        deck_comp = ''
        for card in self.deck:
            deck_comp += '\n ' + card.__str__()
        return 'The deck has:' + deck_comp

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        
        single_card = self.deck.pop()
        return single_card


# %%
class Hand:
    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        # 0 is treated as False, integers not 0 are treated as True (truthiness)

    def add_card(self,card):
        self.cards.append(card)
        self.value += values[card.rank]

        # track aces
        if card.rank == "Ace":
            self.aces += 1 # add to self.aces

    def adjust_for_ace(self):
        # if hand is > 21, ace becomes 1
        # self.aces is the same thing as saying self.aces > 0
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

# %%
class Chips():

    def __init__(self):
        self.total = 100 # default value or supplied by user input
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

# %%
def take_bet(chips):

    while True:
        try:
            chips.bet = int(input('Place your bet:'))
        except:
            print("That is not a number!")
            continue
        else:
            if chips.bet > chips.total:
                    print('Sorry, your bet cannot exceed', chips.total)
            else:
                break
        

# %%
def hit(deck,hand):

    hand.add_card(deck.deal())
    hand.adjust_for_ace()

# %%
def hit_or_stand(deck,hand):
    global playing

    while True:
        player_choice = input('Hit or stand? Choose H for Hit and S for Stand.').lower()
        if player_choice[0] == 'h':
            hit(deck,hand)

        elif player_choice[0] == 's':
            print('Player stands. Dealer is playing')
            playing = False

        else:
            print('Sorry please try again.')
            continue
        break

# %%
# function to display cards

def show_some(player,dealer):
    print("Dealer has card hidden and:\n")
    for card in dealer.cards[1:]:
        print(card,"\n")

    print("Player's hand:\n")
    # print("Player's hand:", *player.cards, sep='\n')
    for card in player.cards:
        print(card,"\n")

def show_all(player,dealer):
    print("Dealer has:\n")
    for card in dealer.cards:
        print(card,"\n")
    print("Dealer's hand:",dealer.value)

    print("\nPlayer's hand:\n")
    for card in player.cards:
        print(card,"\n")
    print("Player's hand:",player.value)
    

# %%
# end of game scenarios
def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Player Wins! Dealer busts!")
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()

def push(player,dealer):
    print("Dealer and Player tie! It's a push")

# %%
while True:
    # Print an opening statement
    print("Welcome to Black Jack! Let's play!")
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()
    
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
        
    # Set up the Player's chips
    player_chips = Chips()
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck,dealer_hand)

        # Show all cards
        show_all(player_hand,dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)
            
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
            
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
            
        
        else:
            push(player_hand,dealer_hand)
            

    
    # Inform Player of their chips total 
    print(f'\nPlayer chip total: {player_chips.total}')

    # Ask to play again
    new_game = input("Play again? Enter y or n")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('Thank you for playing!')
        break


