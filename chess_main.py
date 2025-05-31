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
black = ChessAI("Black", myChess)
white = None

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

    if myChess.turn.getThisTurnName() == "White" and white != None:
        mov = white.getBestMove()
        myChess.moveTo( myChess, mov.x, mov.y, mov.newX, mov.newY)
    elif myChess.turn.getThisTurnName() == "Black" and black != None:
        mov = black.getBestMove()
        myChess.moveTo( myChess, mov.x, mov.y, mov.newX, mov.newY)