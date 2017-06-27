'''
https://goo.gl/zXAmXz odds of poker hands
http://www.thepokerbank.com/strategy/mathematics/ math for ai
'''

import math, random, copy
from HandTypes import *

class AI(object):
    def __init__(self, pID):
        self.id = pID
        self.moveList = ['fold', 'raise', 'check/call']
        self.totalHandStr = 0
        self.totalHands = 0
        self.alreadyRaised = False

    def avgHandStr(self):
        if self.totalHands == 0: return 0
        return self.totalHandStr/self.totalHands

    def aiMove(self, aiDiff, playerList, status):
        # this function is a wrapper for all ai moves
        aggression = 1 # lower is more aggressive
        trials = 3
        if aiDiff == 'easy': turn = AI.easyMove(self, status, playerList)
        elif aiDiff == 'medium': 
            turn = AI.medMove(self, status, aggression, playerList, trials)
        thisMove, number = turn
        print('aiDiff:', aiDiff)
        status.move(thisMove, self.id, playerList)

    def easyMove(self, status, playerList):
        # randomly chooses to check or call if above threshold
        hand = thisHand = playerList[status.currentPlayer].hand
        try:
            if AI.startHandStr(self, hand) > 4:
                checkOdds = 50; raiseOdds = 5; foldOdds = 1
                easyOdds = ['check/call']*checkOdds + ['raise']*raiseOdds +\
                    ['fold']*foldOdds
                thisMove = random.choice(easyOdds)
                if thisMove != 'raise': number = 0
                else: number = random.randint(0, 10)
                return (thisMove, number)
            else: return ('fold', 0)
        except:
            return ('fold', 0)

    def medMove(self, status, aggression, playerList, trials):
        # for starting move, take the handStr and use high prob of taking
        # does not choose moves based on what other people's actions/hands
        # runs a monte carlo simulation w/thresholds to get strength
        thisHand = playerList[status.currentPlayer].hand

        if len(status.tableHand) == 0:
            raiseThreshold = 10; checkThreshold = 4
            strength = AI.startHandStr(self, thisHand)
            print('Starting Hand Strength:', strength, thisHand)
            if strength == None: return ('fold', 0)
            if strength > raiseThreshold and self.alreadyRaised == False:
                self.alreadyRaised = True 
                return ('raise', random.randint(0, 50)) 
            elif strength > checkThreshold: return ('check/call', 0)
            else: return ('fold', 0)

        def monteCarlo(cpuHand, status, trials):
            # Calculating the winning probability for the player's hand
            totalHands = 10**trials; totalWins = 0; handSize = 5
            def chooseStartCards(self, playerList):
                for playerHand in playerList:
                    for i in range(2):
                        newCard = GameController.chooseCard(self, playerList)
                        playerHand.append(newCard)
            for hands in range(totalHands):
                playerList = []; self.totalHands += 1
                trialHand = copy.deepcopy(cpuHand)
                # this loop feeds a 7 card hand into bestPermutation
                status.chooseStartCards(playerList)
                trialHand.append(playerList)
                tableHand = [copy.deepcopy(status.tableHand)]
                testHand = drawNRandomCards(5)
                strPlayer, handPlayer, plHigh = bestPermutation(
                    trialHand[:-1]+tableHand[0]) 
                strOther, handOther, otHigh = bestPermutation(
                    tableHand[0]+testHand)
                self.totalHandStr += strOther
                if strPlayer > strOther: totalWins += 1
                if strPlayer == strOther and plHigh > otHigh: totalWins += 1
            return totalWins/totalHands * 100
        currentHand = playerList[status.currentPlayer].hand
        handStr = monteCarlo(currentHand, status, trials)

        print('handStr: ', handStr)

        def chooseMove(self, handStr, aggression):
            scaleFactor = 42; thresh = AI.avgHandStr(self)*scaleFactor
            raiseThreshold = thresh + aggression
            checkThreshold = thresh - aggression
            currentPlayer = playerList[status.currentPlayer]
            currentHand = currentPlayer.hand
            print('raiseThreshold', raiseThreshold, '| checkThreshold', 
                checkThreshold, '| avgHandStr', AI.avgHandStr(self))
            print('self.alreadyRaised', self.alreadyRaised)
            if handStr > raiseThreshold and self.alreadyRaised == False:
                money = max(currentPlayer.money, 1)
                self.alreadyRaised = True
                return ('raise', random.randint(1, money))
            elif handStr > checkThreshold: return ('check/call', 0)
            else: 
                return ('fold', 0)

        return chooseMove(self, handStr, aggression)

    def startHandStr(self, hand):
        # Chen formula: https://goo.gl/G7VT6d

        def getCardValues(hand):
            cardValues = []
            for card in hand:
                suit, value = card
                try: cardValues.append(int(value))
                except:
                    if value == 'ace': add = 10
                    if value == 'jack': add = 6
                    if value == 'queen': add = 7
                    if value == 'king': add = 8
                    cardValues.append(add)
            return cardValues

        def scoreHighestCard(hand):
            cards = []; suits = set(); total = 0
            for card in hand:
                suit, value = card
                cards.append(value); suits.add(suit)
            if len(set(cards)) == 1:
                total = max(int(cards[0]) * 2, 5)
            elif len(set(cards)) > 1:
                cardValues = getCardValues(hand)
                total = max(cardValues)
            if len(set(suits)) == 1: total += 2
            return total
        
        def subtractGap(hand, score):
            cards = []; suits = set(); total = 0
            for card in hand:
                suit, value = card
                cards.append(value); suits.add(suit)
            if len(set(cards)) > 1:
                cardValues = getCardValues(hand)
                diff = abs(cardValues[0] - cardValues[1])
                if diff in [0, 1]:
                    if 'queen' not in cards and 'king' not in cards and\
                        'ace' not in cards: score += 1
                    return score - diff
                if diff == 2: return score - diff
                if diff == 3: return score - diff - 1
                if diff >  3: return score - 5

        # actually computing the hand score
        thisHand = getIntHand(hand)
        score = scoreHighestCard(thisHand)
        score = subtractGap(thisHand, score)
        return score