from twisted.protocols import amp


# Client to Server
class Join(amp.Command):
    arguments = [('name', amp.String())]
    response = [('result', amp.Boolean())]

class Fold(amp.Command):
    arguments = [('name', amp.String())]
    response = []

class Check(amp.Command):
    arguments = [('name', amp.String())]
    response = []

class Call(amp.Command):
    arguments = [('name', amp.String())]
    response = []

class Raise(amp.Command):
    arguments = [('name', amp.String()), ('amount', amp.Integer())]
    response = []

# Server to Client
class UpdateClient(amp.Command):
    arguments = [   ('playerNames', amp.ListOf(amp.String())),
                    ('playerStacks', amp.ListOf(amp.Integer())),
                    ('playerBets', amp.ListOf(amp.Integer())),
                    ('playersAlive', amp.ListOf(amp.Boolean())),
                    ('playerHands', amp.ListOf(amp.ListOf(amp.Integer()))),
                    ('gameDealer', amp.Integer()),
                    ('gameActor', amp.Integer()),
                    ('gameToCall', amp.Integer()),
                    ('gamePot', amp.Integer()),
                    ('gameCommunityCards', amp.ListOf(amp.Integer()))
                ]
    response = []
