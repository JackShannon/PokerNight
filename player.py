from actions import Fold, Bet

class Player(object):
    def __init__(self, game, name, stackSize):
        self.game = game
        self.name = name
        self.stackAmount = stackSize
        self.betAmount = 0
        self.hand = []

        # whether it's the players turn to act
        self.act = False

        self.action = None

        self.hadTurn = False

    def fold(self):
        if self.act:
            self.action = Fold()
            self.done()

    def raise_(self, amount):
        if self.act:
            self.action = Bet(self, amount)
            self.done()

    def call(self):
        if self.act:
            self.action = Bet(self, self.game.toCall)
            self.done()

    def check(self):
        if self.act:
            self.action = Bet(self, 0)
            done()

    def done(self):
        self.act = False