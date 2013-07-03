class Fold(object):
    pass

class Bet(object):
    def __init__(self, player, amount):
        self.player = player
        self.amount = amount

    # checks if the bet is valid
    def valid(self, toCall):
        # if player has enough
        if (self.player.stackAmount + self.player.betAmount) >= self.amount:
            # if the amount is enough
            if self.amount >= toCall:
                return True
            else:
                print 'Bet amount is not enough'
        else:
            print "Player doesn't have the funds"
        return False

    def moveFunds(self, game):
        # move the funds
        self.player.stackAmount -= (self.amount - self.player.betAmount)
        self.player.betAmount = self.amount
        game.toCall = self.amount