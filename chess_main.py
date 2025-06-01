from chess import Chess, ChessAI
from chess_view import ChessView
from threading import Thread, Event
import socket

comm_type = ""
sock = None
host = "localhost"
port = 65535

def connect():
    if comm_type == "server":
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind((host, port))
        server_socket.listen(5)

        client_socket, client_address = server_socket.accept()
        print(f"클라이언트 {client_address}가 연결되었습니다.")

        return client_socket

    elif comm_type == "client":
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((host, port))

        return sock

def getCommType():
    print("Server / client / alone")
    response = input()
    if response == "server":
        comm_type = "server"
    elif response == "client":
        comm_type = "client"
    elif response == "alone":
        comm_type = "alone"
    else:
        exit(0)

    return comm_type

if __name__ == "__main__":
    comm_type = getCommType()
    sock = connect()

    ##################################################
    # Chess Instance
    ##################################################
    if comm_type == "server":
        myChess = Chess("White")
        myView = ChessView(myChess, False)
    elif comm_type == "client":
        myChess = Chess("Black")
        myView = ChessView(myChess, True)
    else:
        myChess = Chess("Black")
        myView = ChessView(myChess, True)
        #myChess = Chess("White")
        #myView = ChessView(myChess, False)
    myChess.turn.comm_type = comm_type
    #myChess.reset(myChess)

    ##################################################
    # AI Instance
    ##################################################
    #black = ChessAI("Black", myChess)
    #white = None

    ##################################################
    # View Instance
    ##################################################
    event = Event()
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
                myChess.clicked(myChess, msg[1])
                myView.draw()
            elif msg[0] == "Left":
                myChess.cursor.changePosByDelta(-1, 0)
                myView.draw()
            elif msg[0] == "Right":
                myChess.cursor.changePosByDelta(1, 0)
                myView.draw()
            elif msg[0] == "Up":
                myChess.cursor.changePosByDelta(0, 1)
                myView.draw()
            elif msg[0] == "Down":
                myChess.cursor.changePosByDelta(0, -1)
                myView.draw()
            elif msg[0] == "Select":
                myChess.clicked(myChess.cursor.posName)
                myView.draw()
            elif msg[0] == "Exit":
                if sock != None:
                    sock.close()
                break

#        if myChess.turn.getThisTurnName() == "White" and white != None:
#            print(f"Get Best Move")
#            mov = white.getBestMove()
#            mov.print()
#            myChess.moveTo( myChess, mov.x, mov.y, mov.newX, mov.newY)
#        elif myChess.turn.getThisTurnName() == "Black" and black != None:
#            print(f"Get Best Move")
#            mov = black.getBestMove()
#            mov.print()
#            myChess.moveTo( myChess, mov.x, mov.y, mov.newX, mov.newY)