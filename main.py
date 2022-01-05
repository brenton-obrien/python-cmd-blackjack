# Command line Blackjack - Created by Brenton O'Brien

# Imports
import random
import os
import time

# Global Variables
chips = 100
bet_amount = 0
user_hand = []
dealer_hand = []
deck = []
has_hit = False
has_sat = False
got_bet = False


# Create and shuffle a deck of cards
def create_deck():
    global deck
    suits = ["Hearts", "Diamonds", "Spades", "Clubs"]
    values = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
    deck = [f"{value} of {suit}" for value in values for suit in suits]  # Creates a list of 52 un-shuffled cards
    random.shuffle(deck)  # Shuffles the deck


# Create value system for cards
def calculate_card_value(card):
    value_dict = {"Ace": 11, "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10, "Jack": 10, "Queen": 10, "King": 10}
    for item in value_dict:  # Loops through the 'keys' of the dictionary
        if item in card:  # Checks to see if the 'key' is in the name of the card (i.e. if '2' is in '2 of Hearts')
            return value_dict[item]  # Returns the 'Key's corresponding 'Value' integer


# Count the value of a players hand, will also convert aces from 11 to 1 if the hand value is larger than 21
def count_hand_value(player_hand):
    current_value = 0  # Starts from zero each time the players hand needs to be counted
    for card in player_hand:
        current_value += calculate_card_value(card)  # Adds up the value of each card in the players hand

    # The following code will track the amount of aces in a players hand so that it can be converted from 11 to 1 if the hand value is larger than 21
    ace_count = 0
    for card in player_hand:  # Adds the amount of aces up
        if "Ace" in card:
            ace_count += 1

    while current_value > 21 and ace_count > 1:  # If the value is larger than 21, convert the available aces from 11 to 1 until the value is under 21
        if ace_count >= 1: #  Only run if aces are in the hand
            current_value -= 10  # Minus 10 from the value
            ace_count -= 1 #  Remove the ace

    return current_value


# Removes card from the deck and adds it the dealer or user hand
def deal_card(player):  # The player parameter can be used to deal cards to either the user or the dealer
    global deck
    player.append(deck.pop())


# Ask user for bet (Minimum $5), also controls user
def get_bet():
    global bet_amount, chips
    print("\n******************** BLACKJACK ********************")
    print(f"\nCurrent chips: ${chips}")

    try:
        bet_amount = int(input('\n\n\n\n\n\n\n\n\n***************************************************'
                               '\nPlease Enter an amount to bet (Minimum bet is $5)\n\n> $')) #This strange formatting is used to keep the look consistent

        if bet_amount > chips:  # Stops bet being higher than the current amount of user chips
            print(f"Bet is too high, you only have ${chips}")
            time.sleep(2)  # Keeps the message up for two seconds before clearing it and rerunning the function
            cls()
            get_bet()

        elif bet_amount < 5:  # Ensures bet is higher than the minimum bet
            print(f"Bet is too low, minimum bet is $5")
            time.sleep(2)
            cls()
            get_bet()

        elif 5 <= bet_amount <= chips:  # If valid bet, subtract it from the total bet and continue main_game_loop()
            chips = chips - bet_amount

    except ValueError:
        print(f"Incorrect input, please enter a valid number")  # Only allows valid integers to be typed
        time.sleep(2)
        cls()
        get_bet()


# Displays the main board, (cards, hand value, current chips and current bet) can also control when to show the dealers second card
def display_game_board():
    global bet_amount, has_sat

    print("\n******************** BLACKJACK ********************")
    print(f"\nCurrent Chips: ${chips}")
    print(f"\nBet Amount: ${bet_amount}")

    if has_sat: #  If the user has sat, then allow the second dealer card to be showed
        print(f"\nDealer Hand: {', '.join(dealer_hand)}")
        print(f"Dealer Amount: {count_hand_value(dealer_hand)}")

    else: #  If the user hasn't sat yet, then only show the first card, and get the value of that first card only
        print(f"\nDealer Hand: {dealer_hand[0]}")
        print(f"Dealer Amount: {calculate_card_value(dealer_hand[0])}")

    print(f"\nUser Hand: {', '.join(user_hand)}")
    print(f"User Amount: {count_hand_value(user_hand)}\n")
    print("***************************************************")


# Clears the terminal screen
def cls():
    os.system('cls')


def reset_variables(): #  Used to reset all the required variables prior to each new hand being played
    global bet_amount, user_hand, dealer_hand, deck, has_sat, has_hit, got_bet

    bet_amount = 0
    user_hand = []
    dealer_hand = []
    deck = []
    has_hit = False
    has_sat = False
    got_bet = False


# Check for blackjack when cards are first dealt, will also pay out chips if required, and gives reset prompt
def check_for_blackjack(userhand, dealerhand):
    global chips, bet_amount, has_sat, has_hit

    if count_hand_value(dealerhand) == 21 and count_hand_value(userhand) == 21: #  Accounts for if both players hit blackjack
        has_sat = True #  This variable is set to true so that the dealers second card is revealed in display_board() after cls()
        cls()
        display_game_board()
        chips += bet_amount #  Gives the bet back to the user
        reset_prompt('Draw! Both Players Have Blackjack')

    elif count_hand_value(dealerhand) == 21:  # Accounts for if only dealer hits blackjack
        has_sat = True
        cls()
        display_game_board()
        reset_prompt('Dealer has Blackjack! User loses')

    elif count_hand_value(userhand) == 21:  # Accounts for if only the dealer hits blackjack
        has_sat = True
        cls()
        display_game_board()
        if has_hit:  # This accounts for if the user has hit already (therefore it is not technically blackjack)
            chips += bet_amount * 2
        else:
            chips += (bet_amount * 3)  # Pays out if it is blackjack
        reset_prompt('User has Blackjack! User wins')


# Ask player to hit or sit, runs the respective function
def hit_or_sit_prompt():
    answer = ''
    while answer not in ['1', '2']:
        answer = input('Would you like to hit or sit?\n\n1) Hit\n2) Sit\n>')

        if answer == '1':
            hit()

        elif answer == '2':
            sit()

        else:
            cls()
            display_game_board()


def reset_prompt(message): # This message will ask if the user wants to play again and also have a custom message to describe the result of the last hand
    replay_input = input(f'{message}!\n\n1) Bet again\n2) EXIT\n>')

    while replay_input not in ["1", "2"]:
        cls()
        display_game_board()
        replay_input = input('Would you like to bet again?\n1) Bet again\n2) EXIT\n>')

    if replay_input == "1":
        cls()
        reset_variables()
        main_game_loop()

    elif replay_input == "2":
        exit()


def hit():  # Runs when the player hits, will track if the player busts, if not, asks the play to hit or sit
    global user_hand, has_hit

    has_hit = True

    deal_card(user_hand)
    cls()
    display_game_board()

    if count_hand_value(user_hand) > 21:
        replay_input = input('User Busts!\n\n1) Bet again\n2) EXIT\n>')

        while replay_input not in ["1", "2"]:
            cls()
            display_game_board()
            replay_input = input('Would you like to bet again?\n1) Bet again\n2) EXIT\n>')

        if replay_input == "1":
            cls()
            reset_variables()
            main_game_loop()

        elif replay_input == "2":
            exit()

    else:
        hit_or_sit_prompt()


def sit():  # Continues to add cards to the dealers hand until they hit at least 16
    global has_sat, chips
    has_sat = True

    while count_hand_value(dealer_hand) < 16:
        deal_card(dealer_hand)
        cls()
        display_game_board()
        time.sleep(1)

    cls()  # These two lines are used to display the dealers second card after has_sat = True
    display_game_board()

    if count_hand_value(dealer_hand) > 21:  # Dealer busts and user gets paid their winning chips
        chips += (bet_amount * 2)
        reset_prompt('Dealer Busts')

    elif count_hand_value(user_hand) == count_hand_value(dealer_hand):  # Handles the draw
        chips += bet_amount
        reset_prompt('Draw')

    elif count_hand_value(user_hand) > count_hand_value(dealer_hand):  # Handles if player is closer to 21
        chips += (bet_amount * 2)
        reset_prompt('User Wins')

    elif count_hand_value(user_hand) < count_hand_value(dealer_hand):  # Handles if dealer is closer to 21
        reset_prompt('Dealer Wins')


# Create Main loop - Gets a bet, then creates a deck and deals cards, shows the board, checks for blackjack, then asks the hit/sit prompt
def main_game_loop():
    global got_bet, has_sat, chips

    if chips > 0:  # Checks to see if there is at least 1 chip to bet

        if not got_bet:  # Gets the initial bet
            get_bet()
            got_bet = True

            # Clears the screen
            cls()

            # Creates and shuffles a deck
            create_deck()

            # Deal Cards to dealer and user
            deal_card(dealer_hand)
            deal_card(dealer_hand)
            deal_card(user_hand)
            deal_card(user_hand)

            # Displays All cards, the current bet, and remaining chips
            display_game_board()

            # Checks to see if the user or player has hit blackjack
            check_for_blackjack(user_hand, dealer_hand)

            # Asks the user to hit or sit
            hit_or_sit_prompt()

    else:  # If out of chips ask if the player wants to play again or quit
        cls()

        print("\n******************** BLACKJACK ********************")
        replay_prompt = input('\nYou are out of chips!\n\nWould you like to restart with $100 chips or quit the game\n1) RESTART\n2) QUIT\n>')

        if replay_prompt == '1':
            cls()
            chips = 100
            main_game_loop()

        elif replay_prompt == '2':
            exit()


main_game_loop()  # Runs the game when first booting the program
