# This class is used to control the flow of the game (new turns,
# new rounds, best hands, etc.)

import pygame, random, copy
from HandTypes import *

class GameController(object):
    #########################################################
    # Game Flow Functions
    #########################################################
    def __init__(self, players, playerList):
        ############################
        # Defaults
        ############################
        self.defaultMinBet = 2
        self.minBet = self.defaultMinBet
        self.bigBlindValue = self.minBet
        self.smallBlindValue = self.bigBlindValue//2

        ############################
        # Game status information
        ############################
        # players indicated from 0 to n-1
        self.numPlayers = players
        self.currentPlayer = 0
        self.smallBlind = 0
        self.bigBlind = self.smallBlind + 1
        self.dealer = (self.smallBlind - 1) % self.numPlayers
        self.tableHand = []
        self.currentBet = self.minBet
        self.tempBet = self.minBet
        self.betList = [0] * self.numPlayers # sum to get pot value
        # 0 = Fold, 1 = Check, 2 = Raise/Need to Check
        self.betStatus = [2] * self.numPlayers 
        self.roundNum = 1; self.highDesc = ''
        self.lastWon = ''; self.lastWonHand = ''; self.lastWonPlayer = ''
        self.gameOver = False
        GameController.doBlinds(self, playerList)
        testFunctionHands()

    def move(self, moveType, playerID, playerList):
        if self.betStatus.count(0) == 3:
            try: winnerData = (self.betStatus.index(1), -1, -1)
            except: winnerData = (self.betStatus.index(0), -1, '')
            winner = winnerData[0]; self.highDesc = cardToStr(winnerData[2])
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList)
            return
        playerID %= self.numPlayers
        player = playerList[self.currentPlayer]
        if moveType == 'fold':
            player.foldStatus = True
            self.betStatus[self.currentPlayer] = 0
        if moveType == 'check/call' and player.money - self.currentBet >= 0:
            minCall = max(self.betList) - self.betList[playerID]
            if player.money < minCall: minCall = player.money
            player.money -= minCall
            self.betList[playerID] += minCall
            self.betStatus[self.currentPlayer] = 1
        if moveType == 'raise':
            if player.money - self.tempBet < 0: self.tempBet = player.money
            player.money -= self.tempBet
            self.betList[playerID] += self.tempBet
            self.betStatus[self.currentPlayer] = 2
            self.minBet = self.tempBet
            for betID in self.betStatus: 
                if betID == 1: betID = 2 # need to re-check
        print('%s: Player %d | Small: %d | Big: %d | %d\n' % (
        moveType, self.currentPlayer, self.smallBlind, self.bigBlind, 
        self.tempBet))
        GameController.nextPlayer(self, playerList)
        self.currentPlayer %= self.numPlayers

    def isInBounds(self, buttonPositions, command, x, y):
        buttonPos = buttonPositions[command]
        x0, x1, y0, y1 = buttonPos
        if x > x0 and x < x1 and y > y0 and y < y1: return True
        return False

    def nextPlayer(self, playerList):
        # advances the turn to next player's turn
        self.currentPlayer += 1
        # bet statuses: 0 and 1 are good for continuing
        # 2 means that the player needs to re-do their turn
        print(GameController.getPlayingStatus(self, playerList))
        print('self.betStatus', self.betStatus)

        status = GameController.getPlayingStatus(self,playerList)
        if status.count(True) == 1:
            winner = status.index(True)
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList)

        if 2 not in self.betStatus:
            GameController.nextTurn(self, playerList)

    def getPlayingStatus(self, playerList):
        # returns a list of true or false for player can make a move
        # skips bankrupt/folded players
        status = copy.copy(self.betStatus)
        for (i,player) in enumerate(playerList):
            if status[i] != 0 and player.money > 0 and\
            player.foldStatus == False: status[i] = True
            else: status[i] = False
        moneyList = []
        for player in playerList: moneyList.append(player.money)
        if moneyList == [0] * self.numPlayers: 
            self.betStatus = [1] * self.numPlayers
            return [True] * self.numPlayers
        return status

    def nextTurn(self, playerList):

        status = GameController.getPlayingStatus(self,playerList)
        maxCards = 5
        for betID in range(self.numPlayers):
            if playerList[betID].money <= 0 or\
            playerList[betID].foldStatus == True: self.betStatus[betID] = 0
        if status.count(True) == 1:
            winner = status.index(True)
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList)
        if len(self.tableHand) < maxCards: 
            if self.betStatus.count(0) != len(playerList) - 1:
                # draw a new card 
                if len(self.tableHand) == 0:
                    for i in range(2):
                        newCard = GameController.chooseCard(self, playerList)
                        self.tableHand.append(newCard)
                newCard = GameController.chooseCard(self, playerList)
                self.tableHand.append(newCard)
                self.betStatus = [2] * self.numPlayers
                for (i, player) in enumerate(playerList):
                    if player.foldStatus == True: self.betStatus[i] = 0
                    if player.money <= 0: self.betStatus[i] = 0
        else:
            # get the round winner's pID
            winnerData = GameController.getRoundWinner(self, playerList)
            winner = winnerData[0]; self.highDesc = cardToStr(winnerData[2])
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList)

    def nextRound(self, playerList):
        # clears the hands for next round, resets statuses
        print('------Next Round------')
        if GameController.isGameOver(self, playerList):
            self.gameOver = True; return
        self.smallBlind = (self.smallBlind + 1) % self.numPlayers
        self.bigBlind = (self.bigBlind + 1) % self.numPlayers
        self.dealer = (self.dealer + 1) % self.numPlayers
        self.currentPlayer = self.smallBlind
        self.roundNum += 1
        for player in playerList: player.lostGame()
        # reset the betting values
        self.tableHand = []
        self.minBet = self.tempBet = self.currentBet = self.defaultMinBet
        self.betList = [0] * self.numPlayers
        self.betStatus = [2] * self.numPlayers
        for player in playerList: player.hand = []; player.foldStatus = False
        GameController.chooseStartCards(self, playerList)
        for player in playerList:
            if player.money <= 0: player.hand = []; player.foldStatus = True
        GameController.isGameOver(self, playerList)
        if not self.gameOver: GameController.doBlinds(self, playerList)

    def doBlinds(self, playerList):
        # puts big/small blinds into the pot
        self.betList[self.bigBlind] += self.bigBlindValue
        playerList[self.bigBlind].money -= self.bigBlindValue
        self.betList[self.smallBlind] += self.smallBlindValue
        playerList[self.smallBlind].money -= self.smallBlindValue

    def chooseCard(self, playerList):
        self.cardNum = ['2','3','4','5','6','7','8','9','10',
            'jack','queen','king','ace']
        self.cardSuit = ['clubs', 'diamonds', 'spades', 'hearts']
        newSuit = random.choice(self.cardSuit)
        newVal = random.choice(self.cardNum)
        newCard = (newSuit, newVal)
        currCards = []
        for player in playerList:
            for card in player.hand: currCards.append(card)
        for card in self.tableHand: currCards.append(card)
        if newCard in currCards:
            return GameController.chooseCard(self, playerList)
        return newCard

    def getRoundWinner(self, playerList):
        playerHands = []; bestHandCards = '' # tuple of (hand, player)
        for (i, player) in enumerate(playerList):
            if player.foldStatus == False: playerHands.append(player.hand)
            else: playerHands.append([])
        bestHID = -1; bestPID = -1; bestHand = []; highest = 0
        for (i, hand) in enumerate(playerHands):
            if hand != []:
                testHand = hand + self.tableHand
                (tempHID, tempHand, high) = bestPermutation(testHand)
                if tempHID > bestHID: 
                    bestHID = tempHID; bestPID = i
                    bestHand = tempHand; highest = high 
                elif tempHID == bestHID and high > highest:
                    bestPID = i; bestHand = tempHand; highest = high
        for card in bestHand:
            suit, value = card
            bestHandCards += (' ' + suit[0] + '-' + str(value))
        self.lastWon = handIDLookup(bestHID)
        self.lastWonHand = bestHandCards
        self.lastWonPlayer = str(bestPID)
        return (bestPID, bestHID, highest)

    def chooseStartCards(self, playerList):
        # chooses the two starting cards for players
        for player in playerList:
            if player.money >= 0:
                for i in range(2):
                    newCard = GameController.chooseCard(self, playerList)
                    player.hand.append(newCard)

    def isGameOver(self, players):
        status = []
        for player in players:
            status.append(player.lost)
            if player.lost == False: self.winner = player.id
        self.gameOver = (status.count(True) == len(players) - 1)

    def getWinner(self, players):
        # gets game winner
        bestPID = [-1]; bestMoney = -1
        for player in players:
            if player.money > bestMoney:
                bestPID = [player.id]
                bestMoney = player.money
            elif player.money == bestMoney:
                bestPID += [player.id]
        self.winner = bestPID

