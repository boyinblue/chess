from chess import Chess, ChessAI
from chess_view import ChessView
from threading import Thread, Event
import socket

##################################################
# Connect to server
##################################################
server_address="localhost"
server_port = 65535

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((server_address, server_port))

request = f"login"
client_socket.send(request.encode("utf-8"))

response = client_socket.recv(1024).decode("utf-8")
print(f"Login {response}")

request = f"list"
client_socket.send(request.encode("utf-8"))

response = client_socket.recv(1024).decode("utf-8")
print(f"list : {response}")

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
            client_socket.close()
            break

    if myChess.turn.getThisTurnName() == "White" and white != None:
        print(f"Get Best Move")
        mov = white.getBestMove()
        mov.print()
        myChess.moveTo( myChess, mov.x, mov.y, mov.newX, mov.newY)
    elif myChess.turn.getThisTurnName() == "Black" and black != None:
        print(f"Get Best Move")
        mov = black.getBestMove()
        mov.print()
        myChess.moveTo( myChess, mov.x, mov.y, mov.newX, mov.newY)