from twisted.protocols import amp
from amp_commands import *
import globals

class ClientProtocol(amp.AMP):
    def updateClient(self, playerNames, playerStacks, playerBets,
                        playersAlive, playerHands, gameDealer, gameActor,
                            gameToCall, gamePot, gameCommunityCards):
        globals.gui.update(playerNames, playerStacks, playerBets,
                        playersAlive, playerHands, gameDealer, gameActor,
                            gameToCall, gamePot, gameCommunityCards)
        return {}
    UpdateClient.responder(updateClient)