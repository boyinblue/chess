import cv2
import chess
from chess import Chess, ChessView

##################################################
# Global Variables
##################################################
#myChess = chess.Chess
#myChess.reset(myChess)
myView = ChessView()

##################################################
# Mouse Event
##################################################
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        myView.mouseClicked(myView, x, y)

##################################################
# Main Task
##################################################
while True:
    try:
        cv2.getWindowProperty("Chess", 0)
    except:
        break

    k = cv2.waitKey(0) & 0xFF
    print(f"{k} key pressed")
    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == ord('R'):
        myView.reset(myView, True)
        myView.updateWindowAll(myView)
    elif k == ord('r'):
        myView.reset(myView)
        myView.updateWindowAll(self)