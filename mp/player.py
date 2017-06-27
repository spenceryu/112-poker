# This function creates starting values for new players, modify it to change
# starting values for all players

class Player(object):
    def __init__(self, playerID):
        self.id = playerID
        self.smallBlindStatus = False # half of big blind
        self.bigBlindStatus = False
        self.foldStatus = False # whether to skip player in turns
        self.hand = []
        self.money = 1000 # change this for different starting money
        self.chipValues = {'white': 1, 'red': 5, 'blue': 10, 'green': 25, 
            'black': 100}
        self.chips = Player.getChips(self)
        self.lost = False

    def lostGame(self):
        if self.money <= 0:
            self.lost = True
            print('Player %d lost!!!!!' % self.id)

    def getChips(self):
        # takes money and returns number of chips of each type 
        self.blackChips = self.money // self.chipValues['black']
        tempMoney = self.money - self.blackChips * self.chipValues['black']
        self.greenChips = tempMoney // self.chipValues['green']
        tempMoney -= self.greenChips * self.chipValues['green']
        self.blueChips = tempMoney // self.chipValues['blue']
        tempMoney -= self.blueChips * self.chipValues['blue']
        self.redChips = tempMoney // self.chipValues['red']
        tempMoney -= self.redChips * self.chipValues['red']
        self.whiteChips = tempMoney
        result = {'white': self.whiteChips, 'red': self.redChips, 
            'blue': self.blueChips, 'green': self.greenChips, 
            'black': self.blackChips}
        self.chips = result
        return result