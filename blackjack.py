import random
import time

#############
# VARIABLES #
#############

suits = {"Hearts":"♥", "Diamonds":"♦", "Clubs":"♣", "Spades":"♠"} 
ranks = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
values = {"2":2, "3":3, "4":4, "5":5, "6":6, "7":7, "8":8 ,"9": 9, "10": 10, "J":10, "Q":10, "K":10, "A":11}

name = ''
player = ''
dealer = ''
deck = ''
bankroll = ''

active = False
playing = False
show_stats = False



###########
# CLASSES #
###########

class Card():

    def __init__(self, suit, rank):
        self.suit = suits[suit]
        self.rank = rank
        self.value = values[rank]

    def __str__(self):
        return f'{self.rank}{self.suit}'

class Deck():

    def __init__(self):
        self.cards = []
        for suit in suits:
            for rank in ranks:
                self.cards.append(Card(suit,rank))
    
    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        return self.cards.pop()

    def __str__(self):
        deck_string = ''
        for card in self.cards:
            deck_string += f" {card}"
        return deck_string


class Hand():

    def __init__(self,name):
        self.cards = []
        self.value = 0
        self.aces = 0
        self.name = name.upper()
    
    def add_card(self,card):
        self.cards.append(card)
        self.value += card.value
        if card.rank == "A":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1


class Chips():

    def __init__(self):
        self.total = 100
        self.bet = 0
    
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet


#############
# FUNCTIONS #
#############

# Game setup

def setup():
    global name, active, bankroll, show_stats
    new_screen()
    print("\n"*23)
    while name == '':
        name = input("Please enter your name: ").upper()
    
    bankroll = Chips()
    show_stats = True

    new_screen()
    print("\n"*20)
    input(f"Welcome {name}! Press ENTER to start the game...")
    active = True

def initialize():
    global deck, player, dealer, bankroll, playing
    deck = Deck()
    deck.shuffle()

    player = Hand(name)
    dealer = Hand("dealer")
    
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.add_card(deck.deal())
    dealer.add_card(deck.deal())
    player.adjust_for_ace()
    dealer.adjust_for_ace()

    playing = True

# Gameplay

def place_bet(bankroll):
    new_screen()
    print("\n"*20)
    try:
        bankroll.bet = int(input("Please place your bet: $"))
    except ValueError:
        print("Please provide a valid number")
    else:
        while 0 < bankroll.bet > bankroll.total:
            new_screen()
            print("\n"*18)
            print("Your bankroll is insufficient to make this bet.")
            print(f"Your current bankroll is: ${bankroll.total}")
            bankroll.bet = int(input("Please place your bet: $"))
        return bankroll.bet

def hit_or_stand(deck,hand):
    global playing
    if hand.value == 21:
        hit_input = "S"
    elif hand.value > 21:
        return
    else:
        print("If you want another card type H(it), to stand type S(tand)")
        hit_input = input("What do you want to do? ").upper()
    
    while len(hit_input) == 0 or hit_input not in ["H","S"]:
        hit_input = input("Please choose H to hit or S to stand... ").upper()
    
    if hit_input == "H":
        hit(deck, hand)
    else:
        playing = False

def hit(deck,hand):
    global playing
    card = deck.deal()
    hand.add_card(card)
    hand.adjust_for_ace()

    if hand.name == "DEALER": 
        dealers_turn_screen(dealer,player)
        print(f"Dealer draws {card}")
        time.sleep(2)
    else:
        players_turn_screen(dealer,player)

    if hand.value > 21:
        playing = False

def replay():
    global active, playing
    dealers_turn_screen(dealer,player)
    play_again = input("\nDo you want to play another hand? Type Y(es) or N(o): ")[0].upper()
    while len(play_again) == 0 and play_again not in ["Y","N"]:
        play_again = input("Please choose Y for yes or N for no")[0].upper()
    if play_again == "Y":
        active = True
        playing = True
    else:
        dealers_turn_screen(dealer,player)
        confirm_quit = input("\nAre you sure you want to quit? Y/N: ")[0].upper()
        while confirm_quit not in ["Y","N"]:
            confirm_quit = input("Please choose Y for yes or N for no")[0].upper()
        if confirm_quit == "Y":
            active = False
    
def game_over():
    global bankroll, active

    dealers_turn_screen(dealer,player)
    play_again = input("\nGAME OVER! Do you want to play again? Type Y(es) or N(o): ")[0].upper()

    while play_again not in ["Y","N"]:
        play_again = input("Please choose Y for yes or N for no")[0].upper()

    if play_again == "Y":
        bankroll.total = 100
    else:
        active = False

# End results

def player_busts():
    global bankroll, playing
    bankroll.lose_bet()
    bet =  bankroll.bet
    bankroll.bet = 0
    dealers_turn_screen(dealer,player)
    input(f"\nBUST! ${bet} was deducted from your bankroll. Press ENTER to continue... ")
    playing = False
    

def player_wins():
    global bankroll
    bankroll.win_bet()
    bet =  bankroll.bet
    bankroll.bet = 0
    dealers_turn_screen(dealer,player)
    input(f"\nYOU WIN! ${bet} was added to your bankroll. Press ENTER to continue... ")
    

def dealer_busts():
    global bankroll
    bankroll.win_bet()
    bet =  bankroll.bet
    bankroll.bet = 0
    dealers_turn_screen(dealer,player)
    input(f"\nDEALER BUSTS! ${bet} was added to your bankroll. Press ENTER to continue... ")
    
def dealer_wins():
    global bankroll, playing
    bankroll.lose_bet()
    bet =  bankroll.bet
    bankroll.bet = 0
    dealers_turn_screen(dealer,player)
    input(f"\nDEALER WINS! ${bet} was deducted from your bankroll. Press ENTER to continue... ")
    playing = False
    
def push():
    global playing
    bankroll.bet = 0
    dealers_turn_screen(dealer,player)
    input(f"\nPUSH! Nobody wins. Press ENTER to continue... ")
    playing = False
    


###########
# VISUALS #
###########

def welcome_screen():
    print("\n"*100)
    print("♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ WELCOME TO: ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")
    print("╔═════════════════════════════════════════════════════════╗")
    print("║ ┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐ ║")
    print("║ │B    │     │L    │     │A    │     │C    │     │K    │ ║")  
    print("║ │  ♥  │     │  ♣  │     │  ♠  │     │  ♣  │     │  ♥  │ ║") 
    print("║ │    J│     │    A│     │    C│     │    K│     │    !│ ║")
    print("║ └─────┘     └─────┘     └─────┘     └─────┘     └─────┘ ║")
    print("╚═════════════════════════════════════════════════════════╝")
    print("♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦ PLAY RESPONSIBLY! ♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")
    print("\n"*10)
    input("                   PRESS ENTER TO BEGIN!" + "\n" * 13)

def new_screen():
    print("\n"*100)
    print("♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")
    print("╔═════════════════════════════════════════════════════════╗")
    print("║ ┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐     ┌─────┐ ║")
    print("║ │B    │     │L    │     │A    │     │C    │     │K    │ ║")  
    print("║ │  ♥  │     │  ♣  │     │  ♠  │     │  ♣  │     │  ♥  │ ║") 
    print("║ │    J│     │    A│     │    C│     │    K│     │    !│ ║")
    print("║ └─────┘     └─────┘     └─────┘     └─────┘     └─────┘ ║")
    print("╚═════════════════════════════════════════════════════════╝")
    print("♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")
    if show_stats == True:
        print(f" PLAYER NAME:    {name}") 
        print(f" BANKROLL:       ${bankroll.total}")
        if bankroll.bet > 0:
            print(f" YOUR BET:       ${bankroll.bet}")
        print("♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦♦")

def display_cards(hand):
    row1 = []
    row2 = []
    row3 = []
    row4 = []
    row5 = []
    display = [row1, row2, row3, row4, row5]
    for card in hand.cards:
        if card.rank != "10":
            row1.append(" ┌─────┐ ")
            row2.append(f" │{card.rank}    │ ")
            row3.append(f" │  {card.suit}  │ ")
            row4.append(f" │    {card.rank}│ ")
            row5.append(" └─────┘ ")
        else:
            row1.append(" ┌─────┐ ")
            row2.append(f" │{card.rank}   │ ")
            row3.append(f" │  {card.suit}  │ ")
            row4.append(f" │   {card.rank}│ ")
            row5.append(" └─────┘ ")
    print(f"{hand.name}'S HAND:")
    for row in display:
        print("".join(row))
    print(f"HAND TOTAL: {hand.value}")

def display_one_card(hand):
    print(f"{hand.name}'S HAND:")
    for card in hand.cards[0:1]:
        if card.rank != "10":
            print(" ┌─────┐  ┌─────┐ ")
            print(f" │{card.rank}    │  │+ + +│ ")
            print(f" │  {card.suit}  │  │ + + │ ")
            print(f" │    {card.rank}│  │+ + +│ ")
            print(" └─────┘  └─────┘ ")
        else:
            print(" ┌─────┐  ┌─────┐ ")
            print(f" │{card.rank}   │  │+ + +│ ")
            print(f" │  {card.suit}  │  │ + + │ ")
            print(f" │   {card.rank}│  │+ + +│ ")
            print(" └─────┘  └─────┘ ")

def players_turn_screen(dealer,player):
    new_screen()
    display_one_card(dealer)
    print("\n"*5)
    display_cards(player)

def dealers_turn_screen(dealer,player):
    new_screen()
    display_cards(dealer)
    print("\n"*5)
    display_cards(player)

def thanks():
    global show_stats
    show_stats = False
    new_screen()
    print("\n")
    print("         ████████ ██    ██   ████   ███   ██ ██    ██")
    print("            ██    ██    ██  ██  ██  ████  ██ ██   ██")
    print("            ██    ████████ ████████ ██ ██ ██ ██████")
    print("            ██    ██    ██ ██    ██ ██  ████ ██   ██")
    print("            ██    ██    ██ ██    ██ ██   ███ ██    ██")
    print("\n")
    print("██    ██  ██████  ██    ██          ████████  ██████  ███████ ")
    print(" ██  ██  ██    ██ ██    ██          ██       ██    ██ ██    ██")
    print("  ████   ██    ██ ██    ██          ██████   ██    ██ ███████ ")
    print("   ██    ██    ██ ██    ██          ██       ██    ██ ██    ██")
    print("   ██     ██████   ██████           ██        ██████  ██    ██")
    print("\n")
    print("███████  ██         ████   ██    ██    ██    ███   ██  ██████ ")
    print("██    ██ ██        ██  ██   ██  ██     ██    ████  ██ ██      ")
    print("███████  ██       ████████   ████      ██    ██ ██ ██ ██  ████")
    print("██       ██       ██    ██    ██       ██    ██  ████ ██    ██")
    print("██       ████████ ██    ██    ██       ██    ██   ███  ██████ ")
    print("\n")


########
# GAME #
########

welcome_screen()

print("\n"*17)

if active == False:
    setup()

while active == True:
    new_screen()
    initialize()
    
    place_bet(bankroll)

    while playing == True:
        players_turn_screen(dealer,player)
        hit_or_stand(deck,player)

    if player.value <= 21: 
        while dealer.value < 17 or dealer.value < player.value:
            dealers_turn_screen(dealer,player)
            time.sleep(2)
            hit(deck,dealer)

        if dealer.value > 21:
            dealer_busts()
        elif dealer.value > player.value:
            dealer_wins()
        elif dealer.value < player.value:
            player_wins()
        else:
            push()
    else:
        player_busts()

    if bankroll.total == 0:
        game_over()
    else:
        replay()

thanks()