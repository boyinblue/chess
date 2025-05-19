import cv2
import chess

##################################################
# Global Variables
##################################################
objImages = {}

objs = [
        'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackPawn',
        'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhitePawn',
        'Empty'
]

myChess = chess.Chess

##################################################
# Drawing Functions
##################################################
def loadObjImages(objImages):
    for obj in objs:
        img = cv2.imread(f"img/{obj}.png")
        objImages[obj] = img

def draw_object(image, x, y, objName):
    print(f"Draw Obj x={x}, y={y}")

    # Draw Object
    pX = x * 49 + 1
    pY = y * 49 + 1
    image[pY:pY+49, pX:pX+49] = objImages[objName]

    # Draw Rectangle
    pt1 = ( x * 49 + 1, y * 49 + 1 )
    pt2 = ( x * 49 + 49, y * 49 + 49 )
    cv2.rectangle(image, pt1, pt2, (0, 0, 0), 1)

def draw_cursor(image):
    # Draw Cursor
    cursor = myChess.cursor
    if cursor[0] >= 8 or cursor[1] >= 8:
        return
    print(f"Draw Cursor")
    cv2.circle(image, (cursor[0] * 49 + 24, cursor[1] * 49 + 24), 10, (255,255,0), 2)

def draw_availables(image):
    for pos in myChess.availables:
        x, y = myChess.getXY(myChess, pos)
        cv2.circle(image, (x * 49 + 24, y * 49 + 24), 10, (0,0,255), 2)

def delete_info_background(image):
    pt1 = ( 400, 0 )
    pt2 = ( 800, 400 )
    cv2.rectangle(image, pt1, pt2, (255,255,255), -1)

def draw_info(image):
    delete_info_background(image)

    turn = myChess.getThisTurnName(myChess)
    if turn == "White":
        textPos = [ 400, 375 ]
    else:
        textPos = [ 400, 25 ]
    cv2.putText(image, f"< {turn}", textPos, 1, 1, (0, 0, 0), 2)

    cv2.putText(image, "ESC : Exit", [ 500, 25 ], 1, 1, (255, 255, 0))
    cv2.putText(image, "R : Reset", [ 500, 50 ], 1, 1, (255, 255, 0))

def redraw(image):
    newPos = myChess.need_to_redraw
    for posName in newPos:
        if posName == []:
            continue
        try:
            x, y = myChess.getXY(myChess, posName)
        except:
            print(f"Error {posName} to XY")
        objName = myChess.getObjectName(myChess, x, y)
        draw_object(image, x, y, objName)

    draw_cursor(image)
    draw_availables(image)
    draw_info(image)

    myChess.need_to_redraw.clear()
    cv2.imshow('Chess', image)

def updateWindowAll(image):
    for y in range(8):
        for x in range(8):
            objName = myChess.getObjectName(myChess, x, y)
            draw_object(image, x, y, objName)

    draw_cursor(image)
    draw_availables(image)
    draw_info(image)

    myChess.need_to_redraw.clear()
    cv2.imshow('Chess', image)

##################################################
# Mouse Event
##################################################
def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        myChess.clicked(myChess, int(x / 49), int(y / 49))
        redraw(image)

##################################################
# Initialization
##################################################
loadObjImages(objImages)

image = cv2.imread('background.png')
updateWindowAll(image)
cv2.setMouseCallback("Chess", mouse_event, image)

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
    elif k == ord('R') or k == ord('r'):
        myChess.reset(myChess)
        updateWindowAll(image)
