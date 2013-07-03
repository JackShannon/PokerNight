from twisted.protocols import amp
from amp_commands import *
from game import Game
import player
import globals

class ServerProtocol(amp.AMP):
    def join(self, name):
        globals.users[name] = self
        self.player = globals.game.addPlayer(name)
        if self.player:
            print name + ' joined the game'
            if len(globals.game.players) == globals.noOfPlayers:
                globals.game.start()
                self.updateClient()
            return {'result' : True}
        return {'result' : False}
    Join.responder(join)

    def fold(self, name):
        self.getPlayer(name).fold()
        self.updateClient()
        return {}
    Fold.responder(fold)

    def check(self, name):
        self.getPlayer(name).check()
        self.updateClient()
        return {}
    Check.responder(check)

    def call(self, name):
        self.getPlayer(name).call()
        self.updateClient()
        return {}
    Call.responder(call)

    def raise_(self, name, amount):
        self.getPlayer(name).raise_(amount)
        self.updateClient()
        return {}
    Raise.responder(raise_)

    def getPlayer(self, name):
        for p in globals.game.players:
            if p.name == name:
                return p

    def updateClient(self):
        globals.game.update()
        pNames = []
        pStacks = []
        pBets = []
        pAlive = []
        pHands = []
        for p in globals.game.players:
            pNames.append(p.name)
            pStacks.append(p.stackAmount)
            pBets.append(p.betAmount)
            pAlive.append(p in globals.game.alivePlayers)
            #pHands.append(p.hand)
        gDealer = globals.game.players.index(globals.game.dealer)
        gActor = globals.game.players.index(globals.game.actingPlayer)
        gToCall = globals.game.toCall
        gPot = globals.game.pot

        # send the right number of cards each round
        round = globals.game.bettingRound
        cCards = globals.game.communityCards
        if round == 0:
            gCommunityCards = []
        elif round == 1:
            gCommunityCards = cCards[:3]
        elif round == 2:
            gCommunityCards = cCards[:4]
        elif round == 3:
            gCommunityCards = cCards
        else:
            gCommunityCards = []

        for name, protocol in globals.users.iteritems():
            p1 = self.getPlayer(name)
            pHands = []
            for p2 in globals.game.players:
                if p1 == p2:
                    pHands.append(p1.hand)
                else:
                    pHands.append([])

            protocol.callRemote(UpdateClient,
                                playerNames = pNames,
                                playerStacks = pStacks,
                                playerBets = pBets,
                                playersAlive = pAlive,
                                playerHands = pHands,
                                gameDealer = gDealer,
                                gameActor = gActor,
                                gameToCall = gToCall,
                                gamePot = gPot,
                                gameCommunityCards = gCommunityCards)