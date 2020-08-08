from random import random
import pygame

pygame.init()

# Create a window with a backdrop in Pygame

screen_size = width, height = 1400, 800
bgColor = pygame.Color(28, 97, 7)
tbleColor = pygame.Color(84, 42, 7)
tbleBorder = 30
top = (0, 0, width, tbleBorder)
left = (0, 0, tbleBorder, height)
bottom = (0, height-tbleBorder, width, tbleBorder)
right = (width-tbleBorder, 0, tbleBorder, height)
screen = pygame.display.set_mode(screen_size)
screen.fill(bgColor)
pygame.draw.rect(screen, tbleColor, top)
pygame.draw.rect(screen, tbleColor, left)
pygame.draw.rect(screen, tbleColor, bottom)
pygame.draw.rect(screen, tbleColor, right)

# Card variables

cdheight = 200
cdwidth = 130
cdColor = pygame.Color(255, 255, 255)
# Value of the x coordinate for the first and second cards that are initially dealt to the dealer and player
oneCx = 350
twoCx = 510
# Value of the y coordinate of which the dealer and player's hands will be aligned
dcardY = 50
pcardY = 550

# Font type and color variables

font = pygame.font.SysFont(None, 50)
txtColor = pygame.Color(0, 0, 0)
red = pygame.Color(255, 13, 0)

# Writes 'Blackjack' in black and red on the top left of the screen

blck = font.render('Black', True, txtColor)
screen.blit(blck, (40, 40))
jck = font.render('jack', True, red)
screen.blit(jck, (133, 40))

# Draws 'HIT' and 'STAY' rectangles in the bottom left corner of the screen

pygame.draw.rect(screen, red, (55, pcardY + 25, 160, 85))
pygame.draw.rect(screen, red, (55, pcardY + 115, 160, 85))
pygame.draw.rect(screen, txtColor, (60, pcardY + 30, 150, 75))
HIT = font.render('HIT', True, cdColor)
screen.blit(HIT, (105, pcardY + 50))
pygame.draw.rect(screen, txtColor, (60, pcardY + 120, 150, 75))
STAY = font.render('STAY', True, cdColor)
screen.blit(STAY, (91, pcardY + 142))

# Game variables:

# Sum of the values of the cards in the player's hand
hand_total = 0
# Sum of the values of the cards in the dealer's hand
dealer_total = 0
# Lists of the cards in the player and dealer's hands
play_hand = []
deal_hand = []
# Number of times the player/dealer is victorious in a session
play_score = 0
deal_score = 0

# Class for 'Card' objects. Requires two fields: suit and number
class Card():

    def __init__(self, suit, number):
        self.suit = suit
        self.number = number

    def getSuit(self):
        return self.suit

    def getNumber(self):
        if self.number == 'J' or self.number == 'Q' or self.number == 'K':
            return 10
        elif self.number == 'A':
            return 11
        else:
            return self.number

    def getValue(self):
        return str(self.number) + self.suit

    def setNumber(self, n):
        self.number = n

    def draw(self, xpos, ypos):
        pygame.draw.rect(screen, cdColor, (xpos, ypos, cdwidth, cdheight))
        txt = font.render(self.getValue(), True, txtColor)
        screen.blit(txt, (xpos+cdwidth/2-20, ypos+cdheight/2-20))

# Generates a random number between 0 and 3 (inclusive), then returns the corresponding suit as a one letter string
def makeSuit():
    x = int(4*random())
    if x == 0:
        return 'H'
    elif x == 1:
        return 'D'
    elif x == 2:
        return 'S'
    elif x == 3:
        return 'C'

# Generates a random number between 2 and 14 (inclusive), calls makeSuit, and uses the Card class to create a Card object. Returns this Card object.
# Provisions are made for face cards
def genCard():
    rndm = int(13*random()+2)
    if rndm == 11:
        rndm = 'J'
    if rndm == 12:
        rndm = 'Q'
    if rndm == 13:
        rndm = 'K'
    if rndm == 14:
        rndm = 'A'
    suit = makeSuit()
    card = Card(suit, rndm)
    return card

# Starts the game by drawing two cards for both the player and the dealer
def deal():
    global hand_total, card1, card2, dealer_total, dcard1

    # Generates the player's two cards
    card1 = genCard()
    card2 = genCard()

    # Ensures that the two cards are different
    while card1.getValue() == card2.getValue():
        card2 = genCard()

    # Scenario if both cards are aces
    if card1.getValue()[0] == 'A' and card2.getValue()[0] == 'A':
        card1.setNumber(11)
        card2.setNumber(1)
        hand_total = card1.getNumber() + card2.getNumber()
        card1.setNumber('A')
        card2.setNumber('A')

    # Scenarios if one of the cards is an ace
    elif card1.getValue()[0] == 'A':
        card1.setNumber(11)
        hand_total = card1.getNumber() + card2.getNumber()
        card1.setNumber('A')

    elif card2.getValue()[0] == 'A':
        card2.setNumber(11)
        hand_total = card1.getNumber() + card2.getNumber()
        card2.setNumber('A')

    # Scenario if neither of the cards is an ace
    else:
        hand_total = card1.getNumber() + card2.getNumber()

    # Add card objects to the play_hand list
    play_hand.append(card1)
    play_hand.append(card2)

    # Generates the dealer's two cards
    dcard1 = genCard()
    dcard2 = genCard()

    # Ensures that are different to each other, and the cards already dealt to the player
    while dcard1.getValue() == card1.getValue() or dcard1.getValue() == card2.getValue() or dcard1.getValue() == dcard2.getValue():
        dcard1 = genCard()
    while dcard2.getValue() == card1.getValue() or dcard2.getValue() == card2.getValue() or dcard2.getValue() == dcard1.getValue():
        dcard2 = genCard()

    # Scenario if both cards are aces
    if dcard1.getValue()[0] == 'A' and dcard2.getValue()[0] == 'A':
        dcard1.setNumber(11)
        dcard2.setNumber(1)
        dealer_total = dcard1.getNumber() + dcard2.getNumber()
        dcard1.setNumber('A')
        dcard2.setNumber('A')

    # Scenarios if one of the cards is an ace
    elif dcard1.getValue()[0] == 'A':
        dcard1.setNumber(11)
        dealer_total = dcard1.getNumber() + dcard2.getNumber()
        dcard1.setNumber('A')

    elif dcard2.getValue()[0] == 'A':
        dcard2.setNumber(11)
        dealer_total = dcard1.getNumber() + dcard2.getNumber()
        dcard2.setNumber('A')

    # Scenario if neither of the cards is an ace
    else:
        dealer_total = dcard1.getNumber() + dcard2.getNumber()

    # Add card objects to the deal_hand list
    deal_hand.append(dcard1)
    deal_hand.append(dcard2)

    # Draws a white rectangle where the dealer's first card should be, simulating a card flipped over
    pygame.draw.rect(screen, cdColor, (oneCx, dcardY, cdwidth, cdheight))

    # Draws the rest of the cards
    dcard2.draw(twoCx, dcardY)
    card1.draw(oneCx, pcardY)
    card2.draw(twoCx, pcardY)

# Simulates the dealer 'hitting' or taking another card
def dHit():
    global dealer_total

    # Generates the new card
    new_card = genCard()

    # Ensures that new_card is different than all the cards in play
    n = 0
    while n < 10:
        for i in play_hand:
            if i.getValue() == new_card.getValue():
                new_card = genCard()
        for j in deal_hand:
            if j.getValue() == new_card.getValue():
                new_card = genCard()
        n += 1

    # Add the card's number to the dealer's sum
    dealer_total += new_card.getNumber()

    # Add the card object to the deal_hand list
    deal_hand.append(new_card)

    # Draw the new card in accordance with the length of the deal_hand list
    new_card.draw(oneCx + ((len(deal_hand) - 1) * cdwidth + 30 * (len(deal_hand) - 1)), dcardY)

    dCheck()

# Simulates the player 'hitting' or taking another card
def hit():
    global hand_total

    # Generates the new card
    new_card = genCard()

    # Ensures that new_card is different than all the cards in play
    n = 0
    while n < 10:
        for i in play_hand:
            if i.getValue() == new_card.getValue():
                new_card = genCard()
        for j in deal_hand:
            if j.getValue() == new_card.getValue():
                new_card = genCard()
        n += 1

    # Add the card's number to the player's sum
    hand_total += new_card.getNumber()

    # Add the card object to the play_hand list
    play_hand.append(new_card)

    # Draw the new card in accordance with the length of the play_hand list
    new_card.draw(oneCx+((len(play_hand)-1)*130 + 30*(len(play_hand)-1)), pcardY)

    check()

# Checks a busted dealer hand for aces and changes their values to 1
def dCheck():
    global dealer_total

    if dealer_total > 21:
        for card in deal_hand:
            if card.getValue()[0] == 'A':
                card.setNumber(1)
                dealer_total = 0
                for c in deal_hand:
                    dealer_total += c.getNumber()
                card.setNumber('A')

# Checks a busted player hand for aces and changes their values to 1
def check():
    global hand_total

    if hand_total > 21:
        for card in play_hand:
            if card.getValue()[0] == 'A':
                card.setNumber(1)
                hand_total = 0
                for c in play_hand:
                    hand_total += c.getNumber()
                card.setNumber('A')

# Uses the values stored in hand_total and dealer_total to determine a winner, prints result to middle of the screen
# Updates play_score and deal_score appropriately
def decide():
    global play_score, deal_score

    if hand_total == 21 and dealer_total == 21:
        if len(play_hand) == 2 and len(deal_hand) == 2:
            one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
            screen.blit(one1, (oneCx, height / 2 - 100))

            one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
            screen.blit(one2, (oneCx, height / 2 - 50))

            one3 = font.render('Both players have two-card blackjack. Tie!', True, txtColor)
            screen.blit(one3, (oneCx, height / 2 + 40))

        elif len(play_hand) == 2 and len(deal_hand) > 2:
            one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
            screen.blit(one1, (oneCx, height / 2 - 100))

            one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
            screen.blit(one2, (oneCx, height / 2 - 50))

            one3 = font.render('You win by two-card blackjack!', True, txtColor)
            screen.blit(one3, (oneCx, height / 2 + 40))

            play_score += 1

        elif len(play_hand) > 2 and len(deal_hand) == 2:
            one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
            screen.blit(one1, (oneCx, height / 2 - 100))

            one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
            screen.blit(one2, (oneCx, height / 2 - 50))

            one3 = font.render('Dealer wins by two-card blackjack!', True, txtColor)
            screen.blit(one3, (oneCx, height / 2 + 40))

            deal_score += 1

        else:
            one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
            screen.blit(one1, (oneCx, height / 2 - 100))

            one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
            screen.blit(one2, (oneCx, height / 2 - 50))

            one3 = font.render('Both players have 3+ card blackjack. Tie!', True, txtColor)
            screen.blit(one3, (oneCx, height / 2 + 40))

    elif dealer_total == 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('Dealer has blackjack. You lose!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        deal_score += 1

    elif hand_total == 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('You have blackjack. You win!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        play_score += 1

    elif dealer_total > 21 and hand_total <= 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('You win!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        play_score += 1

    elif hand_total > 21 and dealer_total <= 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('Dealer wins!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        deal_score += 1

    elif hand_total > dealer_total and hand_total <= 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('You win!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        play_score += 1

    elif dealer_total > hand_total and dealer_total <= 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('Dealer wins!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        deal_score += 1

    elif dealer_total > 21 and hand_total > 21:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('Everyone busts. Dealer wins!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

        deal_score += 1

    else:
        one1 = font.render('Your total: ' + str(hand_total), True, txtColor)
        screen.blit(one1, (oneCx, height / 2 - 100))

        one2 = font.render('Dealer\'s total: ' + str(dealer_total), True, txtColor)
        screen.blit(one2, (oneCx, height / 2 - 50))

        one3 = font.render('Tie!', True, txtColor)
        screen.blit(one3, (oneCx, height / 2 + 40))

# Resets the table, updates the score on screen
def play_again():
    global hand_total, dealer_total, play_hand, deal_hand

    # Reset game variables
    hand_total = 0
    dealer_total = 0
    play_hand = []
    deal_hand = []

    # Draws rectangles the color of the background over the previous hands, result text, and scores.
    pygame.draw.rect(screen, bgColor, (50, 190, 200, 150))
    pygame.draw.rect(screen, bgColor, (oneCx, height / 2 - 130, width - 30 - oneCx, 260))
    pygame.draw.rect(screen, bgColor, (oneCx + 290, dcardY, 530, cdheight))
    pygame.draw.rect(screen, bgColor, (oneCx + 290, pcardY, 530, cdheight))
    pygame.display.flip()

    # Draws an updated version of the score
    score = font.render('--------SCORE--------', True, txtColor)
    screen.blit(score, (40, 130))
    score1 = font.render('You: ' + str(play_score), True, txtColor)
    screen.blit(score1, (50, 190))
    score2 = font.render('Dealer: ' + str(deal_score), True, txtColor)
    screen.blit(score2, (50, 230))

    deal()
    pygame.display.flip()

def main2():
    global hand_total, dealer_total, play_hand, deal_hand

    # Update display
    pygame.display.flip()

    # Determine if the mouse clicks on the 'HIT' rectangle
    if (pygame.mouse.get_pos()[0] >= 55 and pygame.mouse.get_pos()[0] <= 215) and (pygame.mouse.get_pos()[1] >= pcardY+25 and pygame.mouse.get_pos()[1] <= pcardY+25+85):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                hit()

                # Force the dealer to also hit if dealer_total is below 17
                if dealer_total <= 16:
                    dHit()

                # Determine if either hand is busted
                if hand_total > 21 or dealer_total > 21:
                    # Draws the value of the dealer's first card that was previously 'flipped over'
                    dcd1 = font.render(deal_hand[0].getValue(), True, txtColor)
                    screen.blit(dcd1, (oneCx + cdwidth / 2 - 20, dcardY + cdheight / 2 - 20))

                    decide()

                    # Draw a 'PLAY AGAIN' rectangle
                    pygame.draw.rect(screen, red, (oneCx + 450, pcardY - 250, 315, 85))
                    pygame.draw.rect(screen, txtColor, (oneCx + 455, pcardY - 245, 305, 75))
                    PLAY_AGAIN = font.render('PLAY AGAIN', True, cdColor)
                    screen.blit(PLAY_AGAIN, (oneCx + 500, pcardY - 245 + 20))
                    pygame.display.flip()


    # Determine if the mouse clicks on the 'STAY' rectangle
    if (pygame.mouse.get_pos()[0] >= 55 and pygame.mouse.get_pos()[0] <= 215) and (pygame.mouse.get_pos()[1] >= pcardY+115 and pygame.mouse.get_pos()[1] <= pcardY+115+85):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:

                # Force the dealer to continuously hit until dealer_total is above 16
                while dealer_total <= 16:
                    dHit()

                # Draws the value of the dealer's first card that was previously 'flipped over'
                dcd1 = font.render(deal_hand[0].getValue(), True, txtColor)
                screen.blit(dcd1, (oneCx+cdwidth/2-20, dcardY+cdheight/2-20))

                decide()

                # Draw a 'PLAY AGAIN' rectangle
                pygame.draw.rect(screen, red, (oneCx + 450, pcardY - 250, 315, 85))
                pygame.draw.rect(screen, txtColor, (oneCx + 455, pcardY - 245, 305, 75))
                PLAY_AGAIN = font.render('PLAY AGAIN', True, cdColor)
                screen.blit(PLAY_AGAIN, (oneCx + 500, pcardY - 245 + 20))
                pygame.display.flip()

    # Determine if the mouse clicks on the 'PLAY AGAIN' rectangle
    if (pygame.mouse.get_pos()[0] >= oneCx + 450 and pygame.mouse.get_pos()[0] <= oneCx + 765) and (pygame.mouse.get_pos()[1] >= pcardY - 250 and pygame.mouse.get_pos()[1] <= pcardY - 250 + 85):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                play_again()
                pygame.display.flip()




if __name__ == '__main__':
    deal()

    while True:

        # Breaks loop if 'X' button is clicked
        e = pygame.event.poll()
        if e.type == pygame.QUIT:
            break

        main2()



