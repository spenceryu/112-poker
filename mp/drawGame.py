# image sources listed in ~Resources/sources.txt
# This file contains the draw function for the multiplayer game.

import pygame, random, os
from loadImages import *

def drawRedChip(self, screen, r, x, y):
    pos = (x, y); outColor = (255, 50, 50); insColor = (255, 255, 255)
    outR = r; inR = r*2//3
    pygame.draw.circle(screen, (0, 0, 0), pos, outR + 1)
    pygame.draw.circle(screen, outColor, pos, outR)
    pygame.draw.circle(screen, (0, 0, 0), pos, inR + 1)
    pygame.draw.circle(screen, insColor, pos, inR)

def drawBlueChip(self, screen, r, x, y):
    pos = (x, y); outColor = (50, 50, 255); insColor = (255, 255, 255)
    outR = r; inR = r*2//3
    pygame.draw.circle(screen, (0, 0, 0), pos, outR + 1)
    pygame.draw.circle(screen, outColor, pos, outR)
    pygame.draw.circle(screen, (0, 0, 0), pos, inR + 1)
    pygame.draw.circle(screen, insColor, pos, inR)

def drawGreenChip(self, screen, r, x, y):
    pos = (x, y); outColor = (50, 255, 50); insColor = (255, 255, 255)
    outR = r; inR = r*2//3
    pygame.draw.circle(screen, (0, 0, 0), pos, outR + 1)
    pygame.draw.circle(screen, outColor, pos, outR)
    pygame.draw.circle(screen, (0, 0, 0), pos, inR + 1)
    pygame.draw.circle(screen, insColor, pos, inR)

def drawWhiteChip(self, screen, r, x, y):
    pos = (x, y); outColor = (255, 255, 255); insColor = (255, 255, 255)
    outR = r; inR = r*2//3
    pygame.draw.circle(screen, (0, 0, 0), pos, outR + 1)
    pygame.draw.circle(screen, outColor, pos, outR)
    pygame.draw.circle(screen, (0, 0, 0), pos, inR + 1)
    pygame.draw.circle(screen, insColor, pos, inR)

def drawBlackChip(self, screen, r, x, y):
    pos = (x, y); outColor = (100, 100, 100); insColor = (255, 255, 255)
    outR = r; inR = r*2//3
    pygame.draw.circle(screen, (255, 255, 255), pos, outR + 1)
    pygame.draw.circle(screen, outColor, pos, outR)
    pygame.draw.circle(screen, (0, 0, 0), pos, inR + 1)
    pygame.draw.circle(screen, insColor, pos, inR)

def drawThisChip(self, screen, r, x, y, color):
    if color == 'white': drawWhiteChip(self, screen, r, x, y)
    elif color == 'red': drawRedChip(self, screen, r, x, y)
    elif color == 'blue': drawBlueChip(self, screen, r, x, y)
    elif color == 'green': drawGreenChip(self, screen, r, x, y)
    else: drawBlackChip(self, screen, r, x, y)

def drawPokerChips(self, screen):
    for player in self.players: player.getChips()
    playerPositions = getDrawPlayerPositions(self, 4)
    spacing = 20; r = 10
    for (i, player) in enumerate(self.players):
        chipDict = player.chips
        x, y = playerPositions[i]
        if i in [0, 2]: 
            sx = int(x) + spacing * 6
            y += spacing * 5
        else:
            x -= spacing; y -= spacing*2
            x = int(x); y = int(y) + spacing * 12; sx = x
        for chip in ['white', 'red', 'blue', 'green', 'black']:
            chipAmt = chipDict[chip]; sy = y
            if chipAmt != 0: 
                sx += r*2
                for newChip in range(chipAmt):
                    sy -= r//2
                    drawThisChip(self, screen, r, sx, sy, chip)

def drawTableChips(self, screen):
    (sx, sy) = (self.width//4, self.height//3)
    spacing = 20; r = 10
    money = sum(self.status.betList)
    
    def getChips(money):
        # takes money and returns number of chips of each type 
        chipValues = {'white': 1, 'red': 5, 'blue': 10, 'green': 25, 
            'black': 100}
        blackChips = money // chipValues['black']
        tempMoney = money - blackChips * chipValues['black']
        greenChips = tempMoney // chipValues['green']
        tempMoney -= greenChips * chipValues['green']
        blueChips = tempMoney // chipValues['blue']
        tempMoney -= blueChips * chipValues['blue']
        redChips = tempMoney // chipValues['red']
        tempMoney -= redChips * chipValues['red']
        whiteChips = tempMoney
        result = {'white': whiteChips, 'red': redChips, 'blue': blueChips, 
            'green': greenChips, 'black': blackChips}
        return result

    chipDict = getChips(money)
    for chip in ['white', 'red', 'blue', 'green', 'black']:
        chipAmt = chipDict[chip]
        if chipAmt != 0: 
            sx += r*2
            for newChip in range(chipAmt):
                sy -= r//2
                drawThisChip(self, screen, r, sx, sy, chip)
                
def drawBackground(self, screen):
    screen.blit(self.boardImage, (0,0))

def drawStatusBoard(self, screen):
    screen.blit(self.statusBoardImage, (0,0))
    
    if self.whoAmI == self.status.currentPlayer and\
    not self.status.firstClick:
        lines = ['', '', 'Press the', 'Check/Call', 'button to', 'begin!!!']
        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        xOffset = 20; yOffset = 15
    else:
        line1 = 'Pot: %d | Raise: %d' % (sum(self.status.betList),
            self.status.tempBet)
        line2 = 'Winner: %s' % (self.status.lastWon)
        line3 = ''; line4 = ''; line5 = ''
        if self.status.highDesc != '': line4 += '%s High ' % (
            self.status.highDesc)
        if self.status.lastWonPlayer != '': line3 += 'Player %s' % (
            self.status.lastWonPlayer)
        if self.status.lastWonHand != '':
            line5 += self.status.lastWonHand
        lines = [line1, line2, line3, line4, line5]
        font = pygame.font.Font(pygame.font.get_default_font(), 15)
        xOffset = 17; yOffset = 22
    
    for (i, text) in enumerate(lines):
        textSurface = font.render(text, True, (0,0,0))
        screen.blit(textSurface, (xOffset, (i+1)*yOffset))

# draws cards that everyone can see
def drawTableCards(self, screen):
    cards = self.status.tableHand
    xScale, yScale = 2, 3 
    width, height = self.cardScale*xScale, self.cardScale*yScale 
    maxCards = 5
    startX = self.width/2 - maxCards/2 * width
    if len(cards) != 0:
        for (i, card) in enumerate(cards):
            if i < maxCards:
                suit, value = card
                x = startX + i * width
                y = self.height/2 - height
                screen.blit(self.cardImages[suit][value], (x, y))

def drawHomeButton(self, screen):
    button = getHomeButton()
    buttonHeight = pygame.Surface.get_height(button)
    buttonWidth = pygame.Surface.get_width(button)
    (x0, y0) = (self.width - buttonWidth, 0)
    (x1, y1) = (x0 + buttonWidth, y0 + buttonHeight)
    self.buttonPositions['home'] = (x0, x1, y0, y1)
    screen.blit(button, (x0, y0))

def drawEndGameButton(self, screen):
    button = getEndGameButton()
    space = 5
    buttonHeight = pygame.Surface.get_height(button)
    buttonWidth = pygame.Surface.get_width(button)
    (x0, y0) = (self.width - buttonWidth, buttonHeight + space)
    (x1, y1) = (x0 + buttonWidth, y0 + buttonHeight)
    self.buttonPositions['end-game'] = (x0, x1, y0, y1)
    screen.blit(button, (x0, y0))

def drawGameHelp(self, screen):
    button = getGameHelpButton()
    space = 5
    buttonHeight = pygame.Surface.get_height(button)
    buttonWidth = pygame.Surface.get_width(button)
    (x0, y0) = (self.width - buttonWidth, 2*(buttonHeight + space))
    (x1, y1) = (x0 + buttonWidth, y0 + buttonHeight)
    self.buttonPositions['help-game'] = (x0, x1, y0, y1)
    screen.blit(button, (x0, y0))

def drawGameButtons(self, screen):
    totalWidth = 0; space = 5
    bottomRow = ['raise', 'check-call', 'fold']
    
    # get dimensions to center the buttons
    for buttonName in bottomRow:
        button = self.buttonImages[buttonName]
        buttonWidth = pygame.Surface.get_width(button)
        totalWidth += buttonWidth + space
    mid = self.width / 2
    startX = mid - totalWidth/2

    # draw the buttons
    for buttonName in bottomRow:
        button = self.buttonImages[buttonName]
        buttonHeight = pygame.Surface.get_height(button)
        buttonWidth = pygame.Surface.get_width(button)
        startY = self.height - buttonHeight
        screen.blit(button, (startX, startY))
        startX += buttonWidth + space
        (x0, x1, y0, y1) = (startX - buttonWidth, startX, 
            startY, startY + buttonHeight)
        self.buttonPositions[buttonName] = (x0, x1, y0, y1)
        
    # draw raise instruction button
    def drawRaiseInstructions(self, screen, height, space):
        ins = self.buttonImages['raise-instructions']
        x = self.width/2 - pygame.Surface.get_width(ins)/2
        y = self.height - height*2 - space
        screen.blit(ins, (x,y))
    drawRaiseInstructions(self, screen, buttonHeight, space)
    drawHomeButton(self, screen)
    drawEndGameButton(self, screen)
    drawGameHelp(self, screen)

def getDrawPlayerPositions(self, numPlayers):
    # returns in format [(x,y)], at where cards are drawn
    # for code clarity
    playerList = self.players
    offset = 20 # to show both cards for player hand
    cardWidth = pygame.Surface.get_width(self.cardImages['hearts']['ace'])
    cardHeight = pygame.Surface.get_height(self.cardImages['hearts']['ace'])
    botDY = 260; topDY = 80; leftDX = 50; rightDX = 50 # margins from image
    result = []

    for i in range(len(playerList)):
        if i % 2 == 0: # players on top/bottom of screen
            x = self.width / 2 - cardWidth # to center cards
            if i == 0: y = self.height - botDY
            else: y = topDY
        else: # players on left/right of screen
             y = self.height / 2 - 3*offset
             if i == 1: x = leftDX
             else: x = self.width - rightDX - cardWidth # to center cards
        result.append((x,y))
    return result

def drawPlayerCards(self, screen):
    # draw function is assuming 4 players total, clockwise
    playerList = self.players
    offset = 20 # to show both cards for player hand
    cardWidth = pygame.Surface.get_width(self.cardImages['hearts']['ace'])
    cardHeight = pygame.Surface.get_height(self.cardImages['hearts']['ace'])
    botDY = 260; topDY = 80; leftDX = 50; rightDX = 50 # margins from image
    cardPos = getDrawPlayerPositions(self, len(playerList))

    for (i, player) in enumerate(playerList):
        for (j, card) in enumerate(player.hand[:2]): # only show 2 cards
            (x,y) = cardPos[i]
            if self.whoAmI == i: suit, value = card
            else: suit, value = 'back', 'back'
            screen.blit(self.cardImages[suit][value], (x+offset*j, 
                y+offset*j//3))         

def drawPlayerStatus(self, screen):
    playerList = self.players
    offset = 20; offsetFromCard = 10 # to show cards + text
    cardWidth = pygame.Surface.get_width(self.cardImages['hearts']['ace'])
    cardHeight = pygame.Surface.get_height(self.cardImages['hearts']['ace'])
    botDY = 260; topDY = 80; leftDX = 50; rightDX = 50 # margins from image
    cardPos = getDrawPlayerPositions(self, len(playerList))

    for (i, player) in enumerate(playerList):
        money = self.players[i].money
        text = 'Player %d: $%d' % (i, money)
        if i == self.status.currentPlayer and i == self.whoAmI and\
        not playerList[i].foldStatus: 
            r, g, b = (0, 255, 0)
        elif i == self.status.currentPlayer and not playerList[i].foldStatus: 
            r, g, b = (255, 0, 0)
        else: r, g, b = (0, 100, 255)
        textSurface = self.font.render(text, True, (255, 255, 255))
        (x,y) = cardPos[i]
        rectArea = (x-offset,y-offset,cardWidth+3*offset,cardHeight+2*offset)
        pygame.draw.rect(screen, (r, g, b), rectArea)
        screen.blit(textSurface, (int(x), int(y)-offset))

def drawGameOver(self, screen):
    lines = [
    '','','','','',''
    ]

    def multiWinnerText(winners):
        result = '     Players'
        for player in winners[:-1]:
            result += ' ' + str(player) + ' and '
        result += str(winners[-1]) + ' win!!!'
        return result
    singleWinner = '         Player %s wins!!!' % str(self.status.winner[0])
    multiWinner = multiWinnerText(self.status.winner)

    if len(self.status.winner) > 1: lines[-2] += multiWinner
    else: lines[-2] += singleWinner

    xOffset = self.width // 4; yOffset = self.height // 4
    txOffset = tyOffset = 35
    dyOffset = 25
    font = pygame.font.Font(pygame.font.get_default_font(), 25)

    image = loadBGBoard(self, screen, xOffset, yOffset)
    screen.blit(image, (xOffset, yOffset))

    for (i, text) in enumerate(lines):
        textSurface = font.render(text, True, (0,0,0))
        screen.blit(textSurface, (xOffset+txOffset, 
            (i)*dyOffset+yOffset+tyOffset))