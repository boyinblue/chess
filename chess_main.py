from chess import Chess, ChessAI
from chess_view import ChessView
from threading import Thread, Event

##################################################
# Chess Instance
##################################################
myChess = Chess
myChess.reset(myChess)

##################################################
# AI Instance
##################################################
user1 = ChessAI("Black", myChess)
myChess.turn.setAI("Black", user1)
#user2 = chess.ChessHuman("Black", myChess)

##################################################
# View Instance
##################################################
event = Event()
myView = ChessView(myChess)
myView.event = event
myView.draw()
#th1 = Thread(target=myView.main)
#th1.start()

##################################################
# Main Task
##################################################
while True:
    msg = myView.getEvent()
    if msg != None:
        print(msg)
        if msg[0] == "Clicked":
            myChess.clicked(myChess, msg[1], msg[2])
            myView.draw()
        elif msg[0] == "Exit":
            break