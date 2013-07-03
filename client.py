"""PokerNight Client.

Usage:
  client.py <yourName> <serverAddress>

Options:
  -h --help     Show this screen.
  --version     Show version.

"""

from docopt import docopt
from amp_client import ClientProtocol
from gui import GUI
from twisted.internet.protocol import ClientCreator
from twisted.internet import tksupport, reactor
from amp_commands import *
from Tkinter import *
import globals

class Player(object):
    def __init__(self, name):
        self.name = name

    def connected(self, protocol):
        self._protocol = protocol
        self._protocol.callRemote(Join, name = self.name).addCallback(self.joined)

    def joined(self, results):
        if results['result']:
            print 'Successfully joined game!'

if __name__ == '__main__':
    arguments = docopt(__doc__, version='PokerNight Client 2.0')

    globals.username = arguments['<yourName>']
    server = arguments['<serverAddress>']

    root = Tk()
    tksupport.install(root)

    p = Player(globals.username)
    globals.gui = GUI(root)

    client = ClientCreator(reactor, ClientProtocol).connectTCP(server, 1234)
    client.addCallback(p.connected)
    client = ClientCreator(reactor, ClientProtocol).connectTCP(server, 1234)
    client.addCallback(globals.gui.connected)

    reactor.run()