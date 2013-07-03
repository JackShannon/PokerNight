"""PokerNight Server.

Usage:
  server.py <noOfPlayers>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from docopt import docopt
from twisted.protocols import amp
from twisted.internet import reactor
from twisted.internet.protocol import Factory
from amp_server import ServerProtocol
from amp_commands import *
import globals

if __name__ == '__main__':
    arguments = docopt(__doc__, version='PokerNight Server 2.0')
    globals.noOfPlayers = int(arguments['<noOfPlayers>'])

    pf = Factory()
    pf.protocol = ServerProtocol
    reactor.listenTCP(1234, pf)

    import socket
    ip = socket.gethostbyname(socket.gethostname())
    print 'Started server @', ip

    reactor.run()