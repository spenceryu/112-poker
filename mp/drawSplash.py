import pygame
from loadImages import *

# This file contains the draw function for the splash screen.

def drawTitle(self, screen):
    background = getSplashBG(self.width, self.height)
    screen.blit(background, (0,0))

def drawSplashButtons(self, screen):
    buttons = getTitleButtons()
    self.startButtons = {}
    
    centerSpacing = self.height // (len(buttons)+1); i = 0
    for buttonName in ['15-112-poker', 'start-game', 'help', 'credits']:
        # get dimensions to center the buttons
        button = buttons[buttonName]
        buttonWidth = pygame.Surface.get_width(button)
        buttonHeight = pygame.Surface.get_height(button)
        # draw the buttons
        cx, cy = self.width//2, centerSpacing * (i+1)
        topLX, topLY = cx - buttonWidth//2, cy - buttonHeight//2
        screen.blit(button, (topLX, topLY))
        i += 1
        # button bounds are stored as (x0, y0, x1, y1)
        self.startButtons[buttonName] = (topLX, topLX + buttonWidth, topLY, 
            topLY + buttonHeight)