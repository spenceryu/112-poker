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
        self.tableHand = []; self.allTableHand = []
        self.currentBet = self.minBet
        self.tempBet = self.minBet
        self.betList = [0] * self.numPlayers # sum to get pot value
        # 0 = Fold, 1 = Check, 2 = Raise/Need to Check
        self.betStatus = [2] * self.numPlayers 
        self.roundNum = 1; self.highDesc = ''
        self.lastWon = ''; self.lastWonHand = ''; self.lastWonPlayer = ''
        self.gameOver = False
        GameController.doBlinds(self, playerList)

    def move(self, moveType, playerID, playerList, amount=0, whoAmI=0):
        # framework that mp uses for moves
        if self.betStatus.count(0) == 3:
            try: winnerData = (self.betStatus.index(1), -1, -1)
            except: winnerData = (self.betStatus.index(0), -1, '')
            winner = winnerData[0]; self.highDesc = cardToStr(winnerData[2])
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList, whoAmI)
            return
        playerID %= self.numPlayers
        player = playerList[playerID]
        if moveType == 'fold':
            player.foldStatus = True
            self.betStatus[playerID] = 0
        if moveType == 'check/call' and player.money - self.currentBet >= 0:
            minCall = max(self.betList) - self.betList[playerID]
            if player.money < minCall: minCall = player.money
            player.money -= minCall
            self.betList[playerID] += minCall
            self.betStatus[playerID] = 1
        if moveType == 'raise':
            if player.money - amount < 0: amount = player.money
            player.money -= amount
            self.betList[playerID] += amount
            self.betStatus[playerID] = 2
            self.minBet = amount
            for betID in self.betStatus: 
                if betID == 1: betID = 2 # need to re-check
        print('%s: Player %d | Small: %d | Big: %d | %d\n' % (
        moveType, playerID, self.smallBlind, self.bigBlind, 
        self.tempBet))
        GameController.nextPlayer(self, playerList, whoAmI)

    def isInBounds(self, buttonPositions, command, x, y):
        buttonPos = buttonPositions[command]
        x0, x1, y0, y1 = buttonPos
        if x > x0 and x < x1 and y > y0 and y < y1: return True
        return False

    def nextPlayer(self, playerList, whoAmI):
        # advances to next player's turn
        self.currentPlayer += 1
        # bet statuses: 0 and 1 are good for continuing
        # 2 means that the player needs to re-do their turn
        print(GameController.getPlayingStatus(self, playerList))
        print('self.status.betStatus', self.betStatus)

        status = GameController.getPlayingStatus(self,playerList)
        if status.count(True) == 1:
            winner = status.index(True)
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList, whoAmI)

        if 2 not in self.betStatus:
            GameController.nextTurn(self, playerList, whoAmI)

    def getPlayingStatus(self, playerList):
        # returns list of true or false for moving next round
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

    def nextTurn(self, playerList, whoAmI):
        status = GameController.getPlayingStatus(self,playerList)
        maxCards = 5
        for betID in range(self.numPlayers):
            if playerList[betID].money <= 0 or\
            playerList[betID].foldStatus == True: self.betStatus[betID] = 0
        if status.count(True) == 1:
            # drawing new cards is now server-side, not in here
            winner = status.index(True)
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList, whoAmI)
        if len(self.tableHand) < maxCards: 
            if self.betStatus.count(0) != len(playerList) - 1:
                for (i, player) in enumerate(playerList):
                    if player.foldStatus == True: self.betStatus[i] = 0
                    if player.money <= 0: self.betStatus[i] = 0
        else:
            # get the round winner's pID
            winnerData = GameController.getRoundWinner(self, playerList)
            winner = winnerData[0]; self.highDesc = cardToStr(winnerData[2])
            playerList[winner].money += sum(self.betList)
            GameController.nextRound(self, playerList, whoAmI)

    def nextRound(self, playerList, whoAmI):
        # resets hands for next round, statuses as well
        print('------Next Round------')
        if GameController.isGameOver(self, playerList):
            self.gameOver = True; return
        self.firstClick = False
        self.smallBlind = (self.smallBlind + 1) % self.numPlayers
        self.bigBlind = (self.bigBlind + 1) % self.numPlayers
        self.dealer = (self.dealer + 1) % self.numPlayers
        self.currentPlayer = self.smallBlind
        self.roundNum += 1
        for player in playerList: player.lostGame()
        # reset the betting values
        self.tableHand = []; self.allTableHand = []
        self.minBet = self.tempBet = self.currentBet = self.defaultMinBet
        self.betList = [0] * self.numPlayers
        self.betStatus = [2] * self.numPlayers
        for player in playerList: player.hand = []; player.foldStatus = False
        if whoAmI == 0: self.server.send(('newhand' + '\n').encode())
        for player in playerList:
            if player.money <= 0: player.hand = []; player.foldStatus = True
        GameController.isGameOver(self, playerList)
        if not self.gameOver: GameController.doBlinds(self, playerList)

    def doBlinds(self, playerList):
        # puts big/small blind into the pot
        self.betList[self.bigBlind] += self.bigBlindValue
        playerList[self.bigBlind].money -= self.bigBlindValue
        self.betList[self.smallBlind] += self.smallBlindValue
        playerList[self.smallBlind].money -= self.smallBlindValue

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

    def isGameOver(self, players):
        status = []
        for player in players:
            status.append(player.lost)
            if player.lost == False: self.winner = player.id
        self.gameOver = (status.count(True) == len(players) - 1)

    def getWinner(self, players):
        # who is the game's winner?
        bestPID = [-1]; bestMoney = -1
        for player in players:
            if player.money > bestMoney:
                bestPID = [player.id]
                bestMoney = player.money
            elif player.money == bestMoney:
                bestPID += [player.id]
        self.winner = bestPID

