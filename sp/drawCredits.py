import pygame, os
from loadImages import loadBGBoard

# This file contains the draw function for the credits screen.

def drawCreditsText(self, screen):
    lines = [
    '','',
    '112 Poker Term Project',
    "Texas Hold'em Poker",
    'Made by Spencer Yu',
    'Special thanks to Joseph Kim!!!',
    'Click anywhere to return to title.'
    ]
    xOffset = self.width // 4; yOffset = self.height // 4
    txOffset = tyOffset = 35
    dyOffset = 25
    font = pygame.font.Font(pygame.font.get_default_font(), 18)

    image = loadBGBoard(self, screen, xOffset, yOffset)
    screen.blit(image, (xOffset, yOffset))

    for (i, text) in enumerate(lines):
        textSurface = font.render(text, True, (0,0,0))
        screen.blit(textSurface, (xOffset+txOffset, (i)*dyOffset+yOffset+tyOffset))