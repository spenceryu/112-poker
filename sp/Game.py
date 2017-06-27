# template from Lukas Peraza's pygamegame.py demo
# for 15-112 F15 Pygame Optional Lecture, 11/11/15

# Game wrapper function

import pygame, random
from player import Player
from loadImages import *
from GameController import *
from drawGame import *
from drawSplash import *
from drawHelp import *
from drawCredits import *
from AI import *

class PokerGame(object):

    def init(self, numPlayers=4):
        self.hideCards = True
        self.screen = 'splash' # 'game', 'gameOver', 'help', 'credits'
        # 'help-game'
        self.timerDelay = 0; self.tickSpeed = 10
        self.font = pygame.font.Font(pygame.font.get_default_font(), 12)
        self.players = [Player(i) for i in range(numPlayers)]
        self.boardImage = getBoardImage(self.width, self.height)
        self.statusBoardImage = getStatusBoardImage(self, 4)
        self.cardScale = 30 # changes size of cards
        self.cardImages = getCardImages(self.cardScale)
        self.drawPlayerPositions = getDrawPlayerPositions(self,numPlayers)
        self.buttonImages = getButtonImages()
        self.status = GameController(numPlayers, self.players)
        self.buttonPositions = dict()
        self.status.chooseStartCards(self.players)
        self.aiList = [None] + [AI(i) for i in range(1,numPlayers)]
        self.aiDiff = 'easy'

    def mousePressed(self, x, y):
        # button interactions 
        if self.screen in ['help', 'credits', 'how-to-play-poker']: 
            self.screen = 'splash'
        elif self.screen == 'gameOver': PokerGame.init(self)
        elif self.screen == 'help-game': self.screen = 'game'
        elif self.screen == 'splash':
            if self.status.isInBounds(self.startButtons,'start-game',x,y):
                self.screen = 'game'
            elif self.status.isInBounds(self.startButtons,'help',x,y):
                self.screen = 'help'
            elif self.status.isInBounds(self.startButtons,'credits',x,y):
                self.screen = 'credits'
            elif self.status.isInBounds(self.startButtons,
                'how-to-play-poker',x,y):
                self.screen = 'how-to-play-poker'
        elif self.status.currentPlayer == 0 and self.status.gameOver == False\
        and self.screen == 'game':
            if self.status.isInBounds(self.buttonPositions,'check-call',x,y):
                self.status.move('check/call', self.status.currentPlayer,
                    self.players)
            elif self.status.isInBounds(self.buttonPositions,'fold',x,y):
                self.status.move('fold', self.status.currentPlayer,
                    self.players)
            elif self.status.isInBounds(self.buttonPositions,'raise',x,y):
                self.status.move('raise', self.status.currentPlayer,
                    self.players)
            elif self.status.isInBounds(self.buttonPositions,'home',x,y):
                PokerGame.init(self)
            elif self.status.isInBounds(self.buttonPositions,'end-game',x,y):
                self.screen = 'gameOver'
                self.status.getWinner(self.players)
            elif self.status.isInBounds(self.buttonPositions,
                'help-game',x,y):
                self.screen = 'help-game'


    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        if self.status.gameOver == False and self.screen == 'game':
            # set AI difficulty
            if keyCode == pygame.K_1: self.aiDiff = 'easy'
            if keyCode == pygame.K_2: self.aiDiff = 'medium'

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        for player in self.players: 
            if player.money < 0: player.money = 0
        self.status.currentPlayer %= len(self.players)
        if self.status.gameOver == True: self.screen = 'gameOver'
        elif self.status.gameOver == False:
            # refreshes one of the checkers for folding/advancing
            self.timerDelay += 1
            for betID in self.status.betStatus:
                if self.players[betID].money == 0:
                    if self.players[betID].foldStatus == True:
                        self.status.betStatus[betID] = 0
                    else:
                        self.status.betStatus[betID] = 1
            if self.players[self.status.currentPlayer].foldStatus == True:
                self.status.currentPlayer += 1; return
            # increasing the bet!
            if PokerGame.isKeyPressed(self, pygame.K_UP) and\
                self.status.tempBet < self.players[0].money: 
                self.status.tempBet += 1
            if PokerGame.isKeyPressed(self, pygame.K_DOWN) and\
                self.status.tempBet >= self.status.minBet: 
                self.status.tempBet -= 1
            # delays ai speed
            if self.timerDelay > self.tickSpeed: 
            # ai functions go here!
                self.timerDelay = 0
                if self.status.currentPlayer != 0: # the human player
                    currentAI = self.aiList[self.status.currentPlayer]
                    currentAI.aiMove(self.aiDiff, self.players, self.status)

    def redrawAll(self, screen):

        if self.screen == 'splash':
            drawTitle(self, screen)
            drawSplashButtons(self, screen)

        elif self.screen == 'game':
            drawBackground(self, screen)
            drawTableCards(self, screen)
            drawPlayerStatus(self, screen)
            drawPlayerCards(self, screen)
            drawGameButtons(self, screen)
            drawStatusBoard(self, screen)
            drawPokerChips(self, screen)
            drawTableChips(self, screen)

        elif self.screen == 'gameOver':
            drawTitle(self, screen)
            drawGameOver(self, screen)

        elif self.screen == 'help' or self.screen == 'help-game':
            drawTitle(self, screen)
            drawHelpText(self, screen)

        elif self.screen == 'how-to-play-poker':
            drawTitle(self, screen)
            drawInsText(self, screen)

        elif self.screen == 'credits':
            drawTitle(self, screen)
            drawCreditsText(self, screen)

        pygame.display.flip() # not redrawing entire board every frame

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=800, height=600, fps=60, 
            title="Poker - Single Player Client"):
        self.width = width
        self.height = height
        self.fps = fps
        self.title = title
        self.bgColor = (255, 255, 255)
        pygame.init()

    def run(self):

        clock = pygame.time.Clock()
        screen = pygame.display.set_mode((self.width, self.height))
        # set the title of the window
        pygame.display.set_caption(self.title)

        # stores all the keys currently being held down
        self._keys = dict()

        # call game-specific initialization
        self.init()
        playing = True
        while playing:
            time = clock.tick(self.fps)
            self.timerFired(time)
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    self.mousePressed(*(event.pos))
                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                    self.mouseReleased(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons == (0, 0, 0)):
                    self.mouseMotion(*(event.pos))
                elif (event.type == pygame.MOUSEMOTION and
                      event.buttons[0] == 1):
                    self.mouseDrag(*(event.pos))
                elif event.type == pygame.KEYDOWN:
                    self._keys[event.key] = True
                    self.keyPressed(event.key, event.mod)
                elif event.type == pygame.KEYUP:
                    self._keys[event.key] = False
                    self.keyReleased(event.key, event.mod)
                elif event.type == pygame.QUIT:
                    playing = False
            screen.fill(self.bgColor)
            self.redrawAll(screen)
            
        pygame.quit()

def main():
    game = PokerGame()
    game.run()

if __name__ == '__main__':
    main()
