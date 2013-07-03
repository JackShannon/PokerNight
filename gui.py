from amp_commands import *
from Tkinter import *
import Image, ImageTk
import globals

# images directory
dirPath = 'images/'

class GUI(object):
    def connected(self, protocol):
        self.protocol = protocol

    def __init__(self, master):
        master.geometry('985x778+0+0')
        master.resizable(0,0)
        master.title('PokerNight')

        self.canvas = Canvas(master=master, width=985, height=750, borderwidth=0, highlightthickness=0)
        self.canvas.pack()

        self.loadImages()

        # draw background
        self.bgCImage = self.canvas.create_image(0, 0, anchor=NW, image=self.bgImg)

        self.dealerCImage = self.canvas.create_image(-100, -100, anchor=NW, image=self.dealerImg)
        self.focusCImage = self.canvas.create_image(-300, -300, anchor=NW, image=self.focusFrameImg)


        # draw placeholders
        self.drawCanvasLabels()
        self.drawHands()
        self.drawCommunityCards()
        self.drawNotificationBoxes()

        self.btnFold = Button(master, text = "Fold", width=15, state=DISABLED, command=self.clickFold)
        self.btnFold.pack(side=RIGHT)
        self.btnCall = Button(master, text = "Call", width=15, state=DISABLED, command=self.clickCall)
        self.btnCall.pack(side=RIGHT)
        self.btnRaise = Button(master, text = "Raise", width=15, state=DISABLED, command=self.clickRaise)
        self.btnRaise.pack(side=RIGHT)

        self.scale = Scale(master, orient=HORIZONTAL, state=DISABLED, length=284, from_=0, to=250, showvalue=0)
        self.scale.pack(side=RIGHT)
        self.disableControls()

        self.raiseBet = 0

    def clickFold(self):
        self.disableControls()
        self.protocol.callRemote(Fold, name=globals.username)

    def clickCheck(self):
        self.disableControls()
        self.protocol.callRemote(Check, name=globals.username)

    def clickCall(self):
        self.disableControls()
        self.protocol.callRemote(Call, name=globals.username)

    def clickRaise(self):
        self.disableControls()
        self.protocol.callRemote(Raise, name=globals.username, amount=self.raiseBet)

    def disableControls(self):
        self.scale.config(state=DISABLED, command='')
        self.btnRaise.config(state=DISABLED, text='Raise')
        self.btnCall.config(state=DISABLED, text='Check')
        self.btnFold.config(state=DISABLED)

    def changeCallValue(self, value):
        if value == 0:
            self.btnCall.config(text='Check')
            self.btnFold.config(state=NORMAL)
        else:
            self.btnCall.config(text='Call ('+str(value)+')')
        self.callBet = value

    def changeRaiseValue(self, event):
        value = self.scale.get()
        value = int(round(value/5)*5)
        self.btnRaise.config(text='Raise to '+str(value))
        self.raiseBet = value

    def enableControls(self, player, stack, toCall):
        self.scale.config(state=NORMAL, from_=20, to=stack, command=self.changeRaiseValue)
        self.btnRaise.config(state=NORMAL)
        self.btnCall.config(state=NORMAL)
        self.btnFold.config(state=NORMAL)

        self.changeCallValue(toCall)

    def loadImage(self, relativePath):
        return ImageTk.PhotoImage(Image.open(dirPath + relativePath))

    def loadImages(self):
        self.bgImg = self.loadImage('bg.png')
        self.focusFrameImg = self.loadImage('focusFrame.png')
        self.dealerImg = self.loadImage('dealerbtn.png')
        self.notificationImg = self.loadImage('playernotification.png')

        self.smallCardsImgs = []
        for i in range(53): # 53 = back of card
            self.smallCardsImgs.append(self.loadImage('smallcards/'+str(i)+'.gif'))

        self.bigCardsImgs = []
        for i in range(52):
            self.bigCardsImgs.append(self.loadImage('bigcards/'+str(i)+'.gif'))

    # canvas labels - initial drawing
    def drawCanvasLabels(self):
        self.lbPot = self.canvas.create_text(492, 181, text='', fill="#ffff00", anchor=CENTER)

        position = [(301+11, 14+91), (553+11, 14+91), (797+11, 96+91), (797+11, 446+91),
                    (551+11, 528+91), (299+11, 528+91), (56+11, 446+91), (56+11, 96+91)]
        self.lUsers = []
        for i in range(8):
            self.lUsers.append(self.canvas.create_text(position[i][0], position[i][1], text='', fill="#989898", anchor=NW))

        position = [(301+11, 14+106), (553+11, 14+106), (797+11, 96+106), (797+11, 446+106),
                    (551+11, 528+106), (299+11, 528+106), (56+11, 446+106), (56+11, 96+106)]
        self.lStacks = []
        for i in range(8):
            self.lStacks.append(self.canvas.create_text(position[i][0], position[i][1], text='', fill="#f5f5f5", anchor=NW))

        position = [(355, 231), (632, 231), (770, 307), (755, 400),
                    (611, 463), (371, 462), (247, 407), (225, 308)]
        self.lBets = []
        for i in range(8):
            self.lBets.append(self.canvas.create_text(position[i][0], position[i][1], text='', fill="#ffffff", anchor=CENTER))

    # canvas labels - modifications
    def modifyCanvasLabels(self, pot, names, stacks, bets):
        self.canvas.itemconfigure(self.lbPot, text=pot)
        for i in range(8):
            self.canvas.itemconfigure(self.lUsers[i], text='')
            self.canvas.itemconfigure(self.lStacks[i], text='')
            self.canvas.itemconfigure(self.lBets[i], text='')

        for i in range(len(names)):
            self.canvas.itemconfigure(self.lUsers[i], text=names[i])
            self.canvas.itemconfigure(self.lStacks[i], text=stacks[i])
            if not bets[i] == 0:
                self.canvas.itemconfigure(self.lBets[i], text=bets[i])

    def drawHands(self):
        position = [(301+21, 14+15), (553+21, 14+15), (797+21, 96+15), (797+21, 446+15),
                    (551+21, 528+15), (299+21, 528+15), (56+21, 446+15), (56+21, 96+15)]
        self.iHands1 = []
        self.iHands2 = []
        for i in range(8):
            self.iHands1.append(self.canvas.create_image(position[i][0], position[i][1], anchor=NW, image=''))
            self.iHands2.append(self.canvas.create_image(position[i][0]+4+43, position[i][1], anchor=NW, image=''))

    def showHands(self, hands):
        for i in range(len(hands)):
            if len(hands[i]) == 0:
                self.canvas.itemconfigure(self.iHands1[i], image=self.smallCardsImgs[52])
                self.canvas.itemconfigure(self.iHands2[i], image=self.smallCardsImgs[52])
            else:
                self.canvas.itemconfigure(self.iHands1[i], image=self.smallCardsImgs[hands[i][0]])
                self.canvas.itemconfigure(self.iHands2[i], image=self.smallCardsImgs[hands[i][1]])

    def drawCommunityCards(self):
        position = [(313, 272), (313+6+67, 272), (313+6+67+6+67, 272), (313+6+67+6+67+6+67, 272), (313+6+67+6+67+6+67+6+67, 272)]
        self.iCommunityCards = []
        for i in range(5):
            self.iCommunityCards.append(self.canvas.create_image(position[i][0], position[i][1], anchor=NW, image=''))

    def showCommunityCards(self, cards):
        for i in range(5):
            self.canvas.itemconfigure(self.iCommunityCards[i], image='')
        for i in range(len(cards)):
            self.canvas.itemconfigure(self.iCommunityCards[i], image=self.bigCardsImgs[cards[i]])

    def drawNotificationBoxes(self):
        position = [(301+1, 14+126), (553+1, 14+126), (797+1, 96+126), (797+1, 446+126),
                    (551+1, 528+126), (299+1, 528+126), (56+1, 446+126), (56+1, 96+126)]
        self.notificationImgs = []
        self.notificationLabels = []
        for i in range(8):
            self.notificationImgs.append(self.canvas.create_image(position[i][0], position[i][1], anchor=NW, image=''))
            self.notificationLabels.append(self.canvas.create_text(position[i][0]+65, position[i][1]+12, text='', fill="#00ffff", anchor=CENTER))

    def showFoldBoxes(self, playersAlive):
        for i in range(8):
            self.canvas.itemconfigure(self.notificationLabels[i], text='')
            self.canvas.itemconfigure(self.notificationImgs[i], image='')
        for i in range(len(playersAlive)):
            if not playersAlive[i]:
                self.canvas.itemconfigure(self.notificationLabels[i], text='Folded')
                self.canvas.itemconfigure(self.notificationImgs[i], image=self.notificationImg)




    def moveDealerButton(self, dealer):
        position = [(408, 178), (577, 178), (787, 246), (787, 414),
                        (585, 485), (400, 485), (198, 414), (198, 246)]
        self.canvas.coords(self.dealerCImage, position[dealer][0], position[dealer][1])

    def moveFocusFrame(self, player):
        position = [(301, 14), (553, 14), (797, 96), (797, 446),
                    (551, 528), (299, 528), (56, 446), (56, 96)]
        self.canvas.coords(self.focusCImage, position[player][0], position[player][1])

    def update(self, playerNames, playerStacks, playerBets,
                        playersAlive, playerHands, gameDealer, gameActor,
                            gameToCall, gamePot, gameCommunityCards):
        if gameActor == playerNames.index(globals.username):
            self.enableControls(gameActor, playerStacks[gameActor], gameToCall - playerBets[gameActor])

        self.modifyCanvasLabels(gamePot, playerNames, playerStacks, playerBets)
        self.showHands(playerHands)
        self.showCommunityCards(gameCommunityCards)
        self.moveDealerButton(gameDealer)
        self.moveFocusFrame(gameActor)
        self.showFoldBoxes(playersAlive)


