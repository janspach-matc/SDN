##Name: card_game_week_4.py
##Author: Josh Anspach
##Date finished: 2/14/2023
##
##Script Function: Gets a shuffled deck of cards from an API and uses the deck_id along with input from the user,
##to draw a number of cards between 1-5. The script validates the selection is a number 1-5. Selecting 0 will end the script.
##Once the cards are drawn, The values of any face cards are converted to integers and the values are added up for both the player
##and the CPU. The script then compares the scores and declares a winner.

import requests

payload = {}
headers = {}


#Return a deck_id from the API
def getNewDeck():
    url = "https://deckofcardsapi.com/api/deck/new/shuffle/?deck_count=1"
    response = requests.request("GET", url, headers=headers, data=payload)
    deck_id = response.json()["deck_id"]
    return deck_id #string

#A fuction that simply prints the rules of the game
def printRules():
    print("Choose a number of cards between 1 and 5 for you and the CPU to draw. Face cards are worth 10. Highest score wins!")

#A function that asks the player for a number of cards to draw and then validates the user input
def getNumberOfCards():
    isValidNum = False #Setting a variable to manipulate the while loop
    while isValidNum == False:
        num_cards = input("How many cards will be drawn? Choose a number between 1-5. Choose 0 to exit: ")
        
        if num_cards.isdigit() and int(num_cards) <= 5 and int(num_cards) >= 0: #validates the user input
            isValidNum = True #Changes the value of isValidNum so the while loop deosn't repeat  
            
        else:
            print("Please enter a number between 1-5 or 0 to exit") #prints an error message and continues the loop
        #print("this always prints")
        
    return num_cards #string
    
#Function that uses variables deck_id and num_cards to make an api call that
#draws the requested number of cards and returns a dictionary
def drawCards(d_id,card_num):
    url = "https://deckofcardsapi.com/api/deck/"+d_id+"/draw/?count="+card_num
    response = requests.request("GET", url, headers=headers, data=payload)
    cards_drawn = response.json()
    return cards_drawn #dictionary


def printcards(cards_drawn):
    #print(type(cards_drawn))
    #print(type(cards_drawn["cards"]))
    for card in cards_drawn["cards"]: #This is a list we are looping through
        #print(type(card)) # This is a dictionary that we use to call keys to 
                           # access their current value
        print(card["value"]+" of "+card["suit"])

# This function uses the returned dictionary cards_drawn and loops through adding
# each value in the dict to the variable score
def calc_score(cards_drawn):
    score = 0
    for card in cards_drawn["cards"]:
        if card["value"] == "JACK":
            score += 10
        elif card["value"] == "KING":
            score += 10
        elif card["value"] == "QUEEN":
            score += 10
        elif card["value"] == "ACE":
            score += 1
        else:
            score += int(card["value"])
    return score #integer


# Calling the printRules function and getting string variables assigned by calling
# the getNewDeck() and getNumberOfCards() functions
printRules()
#Josh P explained how to get the return statement to actually return a variable by creating a variable = function()
deck_id = getNewDeck()
num_cards = getNumberOfCards()
#print(type(num_cards))

# If statement that continues the game if the string "0" is not selected
if num_cards != "0":
    
# If a valid number is selected varables are assigned a returned dictionary
# from the drawCards function
    cpu_cards_drawn = drawCards(deck_id, num_cards)
    player_cards_drawn = drawCards(deck_id, num_cards)

    print("Your cards are:")
    printcards(player_cards_drawn)
    player_score = calc_score(player_cards_drawn) #integer
    #print(type(player_score))
    print(f"Your score is {player_score} points")

    print("My cards are:")
    printcards(cpu_cards_drawn)
    cpu_score = calc_score(cpu_cards_drawn) #integer
    print(f"My score is {cpu_score} points")
# If statements that compare the integers assigned to the variables and
# prints who won out of the 3 possible outcomes.
    if player_score > cpu_score:
        print("You win!")
    if cpu_score > player_score:
        print("I win!")
    if player_score == cpu_score:
        print("It's a tie!")
    
    
# else statement that ends the game if 0 is selected     
else:
    
    print("GAME OVER")
