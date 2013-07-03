from player import Player
from cards import Cards
from actions import Fold, Bet
from SevenEval import SevenEval

class Game(object):
    def __init__(self, stackSize = 2000, littleBlind = 10):
        self.players = []
        self.stackSize = stackSize
        self.started = False

        # amount needed to call in active betting round
        self.toCall = 0

        # blinds
        self.littleBlind = littleBlind
        self.bigBlind = littleBlind * 2

        self.dealer = None
        self.actingPlayer = None
        self.alivePlayers = []

        self.communityCards = []

        self.pot = 0

    def addPlayer(self, name):
        player = None
        if not self.started:
            player = Player(self, name, self.stackSize)
            self.players.append(player)
        else:
            print 'Game has started, cannot add Player ' + name
        return player

    def start(self):
        self.started = True
        self.dealer = self.players[0]
        self.deal()

    def update(self):
        # if the acting player is done then update things
        actor = self.actingPlayer
        folded = False
        if actor.act == False:
            # perform the players action
            a = actor.action
            if a.__class__ == Fold:
                self.nextPlayer()
                actor.hadTurn = True
                self.alivePlayers.remove(actor)
                folded = True

            if a.__class__ == Bet:
                if a.valid(self.toCall):
                    # move the funds
                    a.moveFunds(self)
                    actor.hadTurn = True
                else:
                    actor.act = True
                    return

            actor.action = None

            roundIsOver = self.roundOver()
            if roundIsOver:
                self.bettingRound += 1

            # check for winner
            winner = self.getWinner(roundIsOver)
            if winner:
                self.transferWinnings(winner)
                self.deal()
                return

            # check if betting round is over
            if roundIsOver:
                self.newRound()
                return

            # next players turn
            if not folded:
                self.nextPlayer()

    def deal(self):
        # copy list of players
        self.alivePlayers = list(self.players)

        # create new deck
        cards = Cards(len(self.players))
        # store the chosen community cards
        self.communityCards = cards.communityCards
        # give each hand to a player
        for index, player in enumerate(self.players):
            player.hand = cards.hands[index]

        # move the dealer button
        self.dealer = self.players[(self.players.index(self.dealer) + 1) % len(self.players)]

        # take blinds
        l = self.players[(self.players.index(self.dealer) + 1) % len(self.players)]
        b = self.players[(self.players.index(self.dealer) + 2) % len(self.players)]
        lBet = Bet(l, self.littleBlind)
        bBet = Bet(b, self.littleBlind * 2)
        if lBet.valid(0):
            lBet.moveFunds(self)
        if bBet.valid(0):
            bBet.moveFunds(self)

        # set the acting player
        self.actingPlayer = self.players[(self.players.index(self.dealer) + 3) % len(self.players)]
        self.actingPlayer.act = True

        for p in self.players:
            p.hadTurn = False

        self.bettingRound = 0

    def getWinner(self, roundIsOver):
        # if only one person hasn't folded
        if len(self.alivePlayers) == 1:
            print 'Winner: ' + self.alivePlayers[0].name
            return self.alivePlayers[0]

        # else if all betting rounds are over (round 4)
        if self.bettingRound == 4:
            # rank the hands of all alive players (players that haven't folded)
            eval = SevenEval()
            ranks = []
            for p in self.alivePlayers:
                hand  = list(self.communityCards)
                for c in p.hand:
                    hand.append(c)
                ranks.append(eval.getRankOfSeven(*hand))

            # winner has highest ranked hand
            maxValue = max(ranks)
            indexes = [i for i, v in enumerate(ranks) if v == maxValue]
            print 'Winner is ' + self.alivePlayers[indexes[0]].name + '!'
            return self.alivePlayers[indexes[0]]
        return None

    def transferWinnings(self, winner):
        self.collectPot()
        winner.stackAmount += self.pot
        self.pot = 0

    def newRound(self):
        self.collectPot()

        # community cards are all visible server side for time being

        # if round 1 deal flop

        # if round 2 deal turn

        # if round 3 deal river

        # next player left of dealer
        self.actingPlayer = self.alivePlayers[(self.alivePlayers.index(self.dealer) + 1) % len(self.alivePlayers)]
        self.actingPlayer.act = True
        self.toCall = 0

        for p in self.players:
            p.hadTurn = False


    def roundOver(self):
        a = self.alivePlayers[0].betAmount
        for p in self.alivePlayers:
            if (not (p.betAmount == a)) or (not p.hadTurn):
                return False
        return True

    def nextPlayer(self):
        self.actingPlayer = self.alivePlayers[(self.alivePlayers.index(self.actingPlayer) + 1) % len(self.alivePlayers)]
        self.actingPlayer.act = True

    def collectPot(self):
        for p in self.players:
            self.pot += p.betAmount
            p.betAmount = 0
            p.action = None