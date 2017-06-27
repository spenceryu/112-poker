import random

#########################################################
# Hand Classifying Functions
#########################################################

def getHandType(intHand):
    # returning numbers makes comparison easier between types of hands
    highCard = getHighCard(intHand)
    if isRoyalFlush(intHand): ace = 14; return (9, ace)
    elif isStraightFlush(intHand): return (8, highCard)
    elif isFourOfAKind(intHand): 
        fourCard = getNCard(intHand, 4); return (7, fourCard)
    elif isFullHouse(intHand): 
        threeCard = getNCard(intHand, 3); return (6, threeCard)
    elif isFlush(intHand): return (5, highCard)
    elif isStraight(intHand): return (4, highCard)
    elif isThreeOfAKind(intHand): 
        threeCard = getNCard(intHand, 3); return (3, threeCard)
    elif isTwoPair(intHand): 
        highPair = getPair(intHand); return (2, highPair)
    elif isPair(intHand): 
        pairCard = getPair(intHand); return (1, pairCard)
    elif isHighCard(intHand): return (0, highCard)

def handIDLookup(value):
    # decodes hand into status board
    if value == -1: return 'Fold'
    if value == 0: return 'High Card'
    if value == 1: return 'Pair'
    if value == 2: return 'Two Pair'
    if value == 3: return 'Three of a Kind'
    if value == 4: return 'Straight'
    if value == 5: return 'Flush'
    if value == 6: return 'Full House'
    if value == 7: return 'Four of a Kind'
    if value == 8: return 'Straight Flush'
    if value == 9: return 'Royal Flush'

def cardToStr(value):
    # decodes hand as strs
    if value == 1 or value == 14: return 'Ace'
    if value == 13: return 'King'
    if value == 12: return 'Queen'
    if value == 11: return 'Jack'
    return str(value)

def getIntHand(hand):
    # encodes hand as ints
    result = []
    for card in hand:
        suit, value = card
        if value in '23456789' or value in '10': value = int(value)
        if value == 'jack': value = 11
        if value == 'queen': value = 12
        if value == 'king': value = 13
        if value == 'ace': value = 14
        result.append((suit, value))
    return result

def bestPermutation(hand):
    # determines best 5 for hand of 2 + table of 5 (total len 7)
    bestStr = -1; bestHand = []; highCard = 0
    cHand = getIntHand(hand)
    for rm1 in range(len(cHand)): # index of card to remove
        for rm2 in range(len(cHand)): # always make rm2 more than rm1
            if rm1 != rm2:
                if rm1 > rm2: rm1, rm2 = rm2, rm1
                testHand = cHand[:rm1] + cHand[rm1+1:rm2] + cHand[rm2+1:]
                handStr, descCard = getHandType(testHand)
                if handStr > bestStr:
                    bestStr = handStr
                    bestHand = testHand
                    highCard = descCard
    return (bestStr, bestHand, highCard)

def makeCardList():
    # makes a deck of cards to draw from
    cardNum = ['2','3','4','5','6','7','8','9','10',
        'jack','queen','king','ace']
    cardSuit = ['clubs', 'diamonds', 'spades', 'hearts']
    result = []
    for num in cardNum:
        for suit in cardSuit:
            result.append((suit, num))
    return result

def drawNRandomCards(n):
    deck = makeCardList()
    chosen = []
    for i in range(n):
        cardIndex = random.randint(0, len(deck) - 1)
        chosenCard = deck.pop(cardIndex)
        chosen.append(chosenCard)
    return chosen

#########################################################
# Hands in descending order
#########################################################

def isRoyalFlush(hand):
    if not isFlush(hand): return False
    cardValues = set()
    for card in hand:
        suit, value = card
        cardValues.add(value)
    return set([10,11,12,13,14]) == cardValues

def isStraightFlush(hand):
    return isFlush(hand) and isStraight(hand)

def isNOfAKind(hand, count):
    cardValueCount = dict()
    for card in hand:
        suit, value = card
        cardValueCount[value] = cardValueCount.get(value, 0) + 1
    for value in cardValueCount:
        if cardValueCount[value] == count: return True
    return False

def isFourOfAKind(hand):
    return isNOfAKind(hand, 4)

def isFullHouse(hand):
    return isNOfAKind(hand, 2) and isNOfAKind(hand, 3)

def isFlush(hand):
    # flush is five of the same suit
    cardSuits = set()
    for card in hand:
        suit, value = card
        cardSuits.add(suit)
    if len(cardSuits) > 1: return False
    return True

def isStraight(hand):
    cardValues = set()
    for card in hand:
        suit, value = card
        if value == 14: cardValues.add(1)
        cardValues.add(value)
    minVal = min(cardValues)
    setRange = 5 # for a straight
    return cardValues == set(range(minVal, minVal + setRange))

def isThreeOfAKind(hand):
    return isNOfAKind(hand, 3)

def isTwoPair(hand):
    return isNPairs(hand, 2)

def isPair(hand):
    return isNPairs(hand, 1)

def isNPairs(hand, n):
    # determines if this is a n-pair hand
    cardValueCount = dict()
    for card in hand:
        suit, value = card
        cardValueCount[value] = cardValueCount.get(value, 0) + 1
    count = 0
    for cardValue in cardValueCount:
        if cardValueCount[cardValue] == 2:
            # this is a pair
            count += 1
    return count == n
    
def isHighCard(hand):
    # there is always a high card
    return True

def getHighCard(hand):
    # comparison card when high card needed
    values = []
    for card in hand:
        suit, value = card
        values.append(value)
    return max(values)

def getNCard(hand, n):
    # determines the comparison card in a n card hand
    values = []
    for card in hand:
        suit, value = card
        values.append(value)
    for value in values:
        if values.count(value) == n:
            return value

def getPair(hand):
    # gets highest pair value
    values = []; highestPair = 0
    for card in hand:
        suit, value = card
        values.append(value)
    for value in values:
        if values.count(value) == 2 and value > highestPair:
            highestPair = value
    assert(highestPair > 0)
    return highestPair

######################## TEST FUNCTION ########################

def testFunctionHands():
    # appropriate test function for the critical algorithm!
    print('Testing handEvaluators...')
    hand1 = [('spades', 2), ('spades', 3), ('spades', 4),
    ('spades', 5), ('hearts', 6)]
    assert(isStraight(hand1) == True)
    hand2 = [('spades', 2), ('spades', 9), ('spades', 4),
    ('spades', 5), ('spades', 7)]
    assert(isFlush(hand2) == True)
    print('Passed!')