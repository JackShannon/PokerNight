class Cards(object):
    def __init__(self, playerCount):
        from random import shuffle
        deck = self.makeDeck()
        shuffle(deck)
        self.hands = self.dealPlayerHands(deck, playerCount)
        self.communityCards = self.dealHand(deck, 5)

    def makeDeck(self):
        deck = range(52)
        return deck

    def dealHand(self, deck, handSize=2):
        hand = []
        for i in range(handSize):
            hand.append(deck.pop())
        return hand

    def dealPlayerHands(self, deck, playerCount):
        hands = []
        for i in range(playerCount):
            hands.append(self.dealHand(deck))
        return hands