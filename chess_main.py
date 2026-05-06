from chess import Chess, ChessAI
from chess_view import ChessView
from chess_wizard import run_wizard
from threading import Thread, Event
import socket
import sys
import time
import cv2
import os
import tkinter as tk
from tkinter import filedialog

ICON_PATH = os.path.join(os.path.dirname(__file__), "img", "chess_icon.ico")

fo = None

if os.environ.get("CHESS_LOG", "0") == "1":
    fo = open("log.txt", "w")
    sys.stdout = fo

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
    if len(sys.argv) >= 2:
        response = sys.argv[1].strip().lower()
        if response not in ["server", "client", "alone"]:
            response = "alone"
        return response, "White"

    result = run_wizard()
    if result is None:
        sys.exit(0)
    return result["comm_type"], result["my_color"]


def ask_save_record_path(default_path):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected = filedialog.asksaveasfilename(
        title="기보 저장",
        initialfile=os.path.basename(default_path),
        initialdir=os.path.dirname(os.path.abspath(default_path)),
        defaultextension=".json",
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
    )
    root.destroy()
    return selected


def ask_open_record_path(default_path):
    root = tk.Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    selected = filedialog.askopenfilename(
        title="기보 불러오기",
        initialdir=os.path.dirname(os.path.abspath(default_path)),
        filetypes=[("JSON Files", "*.json"), ("All Files", "*.*")],
    )
    root.destroy()
    return selected


def setup_process_icon(icon_path):
    if not os.path.isfile(icon_path):
        return
    try:
        import ctypes
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("boyinblue.chess")
    except Exception:
        pass

    try:
        import win32gui
        import win32con
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, icon_flags)
        hwnd = 0
        try:
            import ctypes
            hwnd = ctypes.windll.kernel32.GetConsoleWindow()
        except Exception:
            hwnd = 0
        if hwnd:
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
            win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)
    except Exception:
        pass

if __name__ == "__main__":
    setup_process_icon(ICON_PATH)
    comm_type, my_color = getCommType()
    sock = connect()

    ##################################################
    # Chess Instance
    ##################################################
    if comm_type == "server":
        myChess = Chess(my_color)
        myView = ChessView(myChess, my_color == "Black", "Chess")
    elif comm_type == "client":
        myChess = Chess("Black")
        myView = ChessView(myChess, True, "Chess")
    else:
        myChess = Chess(my_color)
        myView = ChessView(myChess, my_color == "Black", "Chess")

    myChess.turn.comm_type = comm_type

    ##################################################
    # AI Instance
    ##################################################
    if myChess.turn.comm_type == "alone":
        ai_color = "Black" if my_color == "White" else "White"
        black = ChessAI(ai_color, myChess)
        white = None

    ##################################################
    # View Instance
    ##################################################
    event = Event()
    myView.event = event
    myView.draw()
    next_ai_move_time = 0.0
    record_path = "game_record.json"
    replay_mode = False
    replay_moves = []
    replay_index = 0
    #th1 = Thread(target=myView.main)
    #th1.start()

    ##################################################
    # Main Task
    ##################################################
    try:
        while True:
            msg = myView.getEvent()
            if msg != None:
                print(msg)
                if msg[0] == "Clicked":
                    if replay_mode:
                        continue
                    hist_len_before = len(myChess.history.arrHistory)
                    myChess.clicked(msg[1])
                    new_moves = myChess.history.arrHistory[hist_len_before:]
                    if len(new_moves) > 0:
                        myView.animateMoves(new_moves)
                        if black != None and myChess.turn.getThisTurnName() == black.color:
                            next_ai_move_time = time.time() + 1.0
                            myView.hideCursor = True
                    myView.draw()
                elif msg[0] == "Left":
                    if replay_mode:
                        continue
                    myChess.cursor.changePosByDelta(-1, 0)
                    myView.draw()
                elif msg[0] == "Right":
                    if replay_mode:
                        if replay_index < len(replay_moves):
                            rec = replay_moves[replay_index]
                            src = rec.get("from", "")
                            dst = rec.get("to", "")
                            if myChess.isValidPos(src) and myChess.isValidPos(dst) and dst in myChess.getLegalMoves(src):
                                hist_len_before = len(myChess.history.arrHistory)
                                myChess.moveTo(src, dst)
                                myView.animateMoves(myChess.history.arrHistory[hist_len_before:])
                                replay_index += 1
                            else:
                                print(f"Stop replay on illegal move: {src} -> {dst}")
                                replay_index = len(replay_moves)

                            if replay_index >= len(replay_moves):
                                replay_mode = False
                                myView.hideCursor = False
                                print("Replay finished")
                            myView.draw()
                        continue

                    myChess.cursor.changePosByDelta(1, 0)
                    myView.draw()
                elif msg[0] == "Up":
                    if replay_mode:
                        continue
                    myChess.cursor.changePosByDelta(0, 1)
                    myView.draw()
                elif msg[0] == "Down":
                    if replay_mode:
                        continue
                    myChess.cursor.changePosByDelta(0, -1)
                    myView.draw()
                elif msg[0] == "Select":
                    if replay_mode:
                        continue
                    myChess.clicked(myChess.cursor.posName)
                    myView.draw()
                elif msg[0] == "Reset":
                    replay_mode = False
                    replay_moves = []
                    replay_index = 0
                    myChess.reset()
                    myChess.turn.comm_type = comm_type
                    myView.hideCursor = False
                    myView.draw()
                elif msg[0] == "Rollback":
                    if replay_mode:
                        continue
                    myChess.cancelselected()
                    if myChess.rollback():
                        myChess.rollback()
                    myView.hideCursor = False
                    myView.draw()
                elif msg[0] == "Exit":
                    break
                elif msg[0] == "SaveRecord":
                    try:
                        selected = ask_save_record_path(record_path)
                        if selected:
                            record_path = selected
                            count = myChess.saveRecord(record_path)
                            print(f"Saved {count} moves to {os.path.abspath(record_path)}")
                    except Exception as e:
                        print(f"Failed to save record: {e}")
                elif msg[0] == "ReplayRecord":
                    try:
                        selected = ask_open_record_path(record_path)
                        if not selected:
                            continue
                        record_path = selected
                        moves = myChess.loadRecord(record_path)
                        myChess.reset()
                        myChess.turn.comm_type = comm_type
                        myView.hideCursor = True
                        myView.draw()
                        replay_mode = True
                        replay_moves = moves
                        replay_index = 0
                        print(f"Replay ready ({len(moves)} moves). Press Right Arrow to step.")
                    except Exception as e:
                        print(f"Failed to replay record: {e}")

            if replay_mode:
                continue

            if myChess.turn.gameover:
                continue

            if black != None and myChess.turn.getThisTurnName() == black.color:
                if time.time() < next_ai_move_time:
                    continue
                print(f"Get Best Move For {black.color}")
                mov = black.getBestMove()
                if mov is None:
                    myChess.updateGameStatus()
                    myView.draw()
                    continue
                mov.print()
                hist_len_before = len(myChess.history.arrHistory)
                myChess.moveTo(mov.posName, mov.newPosName)
                myView.animateMoves(myChess.history.arrHistory[hist_len_before:])
                myView.hideCursor = False
                myView.draw()
    finally:
        if sock != None:
            sock.close()
        cv2.destroyAllWindows()
        if fo is not None:
            fo.close()