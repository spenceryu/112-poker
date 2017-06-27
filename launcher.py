# template from Lukas Peraza's pygamegame.py demo
# for 15-112 F15 Pygame Optional Lecture, 11/11/15

# Game launcher function
# A separate instance of the launcher needs to be run to create the mp server

import pygame, os

class Launcher(object):

    def init(self):
        self.screen = 'main' # mp # host
        self.buttonPositions = {}

    def mousePressed(self, x, y):
            
        def isInBounds(buttonPositions, command, x, y):
            buttonPos = buttonPositions[command]
            x0, x1, y0, y1 = buttonPos
            if x > x0 and x < x1 and y > y0 and y < y1: return True
            return False

        if self.screen == 'main':
            if isInBounds(self.buttonPositions,'play-single-player',x,y):
                print('sp_client launched')
                os.system('python3 sp/Game.py')
            elif isInBounds(self.buttonPositions,'play-multiplayer',x,y):
                self.screen = 'mp'
        elif self.screen == 'mp':
            if isInBounds(self.buttonPositions,'home',x,y):
                self.screen = 'main'
            elif isInBounds(self.buttonPositions,'multiplayer-client',x,y):
                print('mp_client launched')
                os.system('python3 mp/mp_client.py')
            elif isInBounds(self.buttonPositions,'multiplayer-server',x,y):
                print('mp_server launched')
                self.screen = 'host'
                os.system('python3 mp/mp_server.py')

    def mouseReleased(self, x, y):
        pass

    def mouseMotion(self, x, y):
        pass

    def mouseDrag(self, x, y):
        pass

    def keyPressed(self, keyCode, modifier):
        pass

    def keyReleased(self, keyCode, modifier):
        pass

    def timerFired(self, dt):
        pass

    def redrawAll(self, screen):

        def getBGImage(self):
            filepath = os.path.join('sp', 'Resources', 'splash-bg.jpg')
            image = pygame.transform.scale(pygame.image.load(filepath).\
                convert_alpha(),(self.width, self.height))
            return image

        def getButton(self, name):
            name = 'button_' + name + '.png'
            filepath = os.path.join('Resources', name) 
            image = pygame.image.load(filepath)
            return image

        def drawSplashButtons(self, screen):
            if self.screen == 'main':
                buttonNames = ['15-112-poker', 'play-single-player', 
                    'play-multiplayer']
            elif self.screen == 'mp':
                buttonNames = ['multiplayer-client', 'multiplayer-server', 
                    'home']
            if self.screen == 'main' or self.screen == 'mp':
                buttons = {name: getButton(self, name) for name in buttonNames}
                centerSpacing = self.height // (len(buttons)+1); i = 0
                for buttonName in buttonNames:
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
                    self.buttonPositions[buttonName] = (topLX,
                        topLX + buttonWidth, topLY, topLY + buttonHeight)   

        def loadBGBoard(self, screen, xOffset, yOffset):
            filepath = os.path.join('sp', 'Resources', 'status-board.jpg')
            image = pygame.transform.scale(pygame.image.load(filepath).convert_alpha(),
                (int(self.width) - 2 * xOffset, int(self.height) - 2 * yOffset))
            return image

        def drawHostText(self, screen):
            # This screen only appears if the port is taken or
            # the game crashes due to an error.
            lines = [
            '',
            'This port is already in use.',
            'Please change the port in', 'mp_client.py and mp_server.py!',
            ''
            ]
            if self.screen == 'host':
                xOffset = self.width // 4; yOffset = self.height // 4
                txOffset = tyOffset = 35
                dyOffset = 25
                font = pygame.font.Font(pygame.font.get_default_font(), 12)

                image = loadBGBoard(self, screen, xOffset, yOffset)
                screen.blit(image, (xOffset, yOffset))

                for (i, text) in enumerate(lines):
                    textSurface = font.render(text, True, (0,0,0))
                    screen.blit(textSurface, (xOffset+txOffset, 
                        (i)*dyOffset+yOffset+tyOffset))

        screen.blit(getBGImage(self), (0,0))
        drawSplashButtons(self, screen)
        drawHostText(self, screen)

        pygame.display.flip() # not redrawing entire board every frame

    def isKeyPressed(self, key):
        ''' return whether a specific key is being held '''
        return self._keys.get(key, False)

    def __init__(self, width=600, height=400, fps=60, title="Launcher"):
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
    game = Launcher()
    game.run()

if __name__ == '__main__':
    main()