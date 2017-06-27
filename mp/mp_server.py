'''
modified framework from 112 optional lecture multiplayer demo

adapted from https://github.com/spenceryu/112-fighter/blob/master/
Multiplayer/sf_server.py
'''

import socket
from _thread import *
from queue import Queue
import random

HOST = '127.0.0.1'
PORT = 51040
BACKLOG = 4

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
server.bind((HOST,PORT))
server.listen(BACKLOG)
print("looking for connection")

class Server(object):

    def __init__(self):
        # cards are stored server-side!
        self.tableHand = [[]]
        self.playerCards = [[] for player in range(4)]
        self.gameOver = False
        self.currPlayer = 0
        self.chooseStartCards()
        self.chooseTableCards()
        print('self.playerCards:', self.playerCards)
        print('self.tableHand:', self.tableHand)

    def chooseCard(self):
        cardNum = ['2','3','4','5','6','7','8','9','10',
            'jack','queen','king','ace']
        cardSuit = ['clubs', 'diamonds', 'spades', 'hearts']
        newSuit = random.choice(cardSuit)
        newVal = random.choice(cardNum)
        newCard = (newSuit, newVal)
        currCards = []
        for hand in self.playerCards:
            for card in hand: currCards.append(card)
        for card in self.tableHand[0]: currCards.append(card)
        if newCard in currCards:
            return Server.chooseCard(self)
        return newCard

    def chooseStartCards(self):
        for (i, hand) in enumerate(self.playerCards):
            for j in range(2):
                card = Server.chooseCard(self)
                self.playerCards[i].append(card)

    def chooseTableCards(self):
        for i in range(5):
            Server.addTableCard(self)

    def encodeHand(self, hands):
        # turns hand into a format that can be sent as string
        result = ''
        for hand in hands:
            for card in hand:
                suit, value = card
                encoded = str(suit[0]) + str(value[0])
                result += encoded + ','
        return result

    def addTableCard(self):
        if self.tableHand[0] == []:
            for i in range(2):
                card = Server.chooseCard(self)
                self.tableHand[0].append(card)
        card = Server.chooseCard(self)
        self.tableHand[0].append(card)

def handleClient(client, serverChannel, cID):
    client.setblocking(1)
    msg = ""
    while True:
        msg += client.recv(10).decode("UTF-8")
        command = msg.split("\n")
        while (len(command) > 1):
            readyMsg = command[0]
            msg = "\n".join(command[1:])
            serverChannel.put(str(cID) + "_" + readyMsg)
            command = msg.split("\n")

def serverThread(clientele, serverChannel, data):
    while True:
        msg = serverChannel.get(True, None)
        senderID = int(msg.split('_')[0])
        msg = "_".join(msg.split("_")[1:])
        if (msg):
            print("msg recv: ", msg)

            if 'newhand' in msg:
                # resets the hands
                data.tableHand = [[]]
                data.playerCards = [[] for player in range(4)]
                data.tableHand = [[]]
                data.chooseStartCards()
                data.chooseTableCards()

            # clientele is dictionary
            for cID in clientele:
                if 'playerhands' in msg or 'newgame' in msg or \
                'newhand' in msg:
                    # send player hands to all players
                    sendMsg = 'playerhands_' +\
                        data.encodeHand(data.playerCards) + '_' + \
                        data.encodeHand(data.tableHand) + '_'
                    print('sending hands to %d from server: %s' % (
                        cID, sendMsg))
                    clientele[cID].send(sendMsg.encode())
                else:
                    # movement commands are sent to all players
                    print('sending message to %d from %d' % (
                        cID,senderID))
                    sendMsg = msg + '_' + str(senderID) + '\n'
                    clientele[cID].send(sendMsg.encode())
                    data.currPlayer = (data.currPlayer + 1) % len(
                        data.playerCards)

        serverChannel.task_done()

data = Server()
clientele = {}
currID = 0

serverChannel = Queue(20)
start_new_thread(serverThread, (clientele, serverChannel, data))

while True:
    client, address = server.accept()
    for cID in clientele:
        clientele[cID].send(("newPlayer_%d\n" % currID).encode())
        client.send(("newPlayer_%d\n" % cID).encode())
        client.send(("myid_%d\n" % currID).encode())
    clientele[currID] = client
    print("connection recieved")
    start_new_thread(handleClient, (client,serverChannel, currID))
    currID += 1


