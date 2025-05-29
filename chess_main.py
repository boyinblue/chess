import cv2
import chess

##################################################
# Global Variables
##################################################
objImages = {}
objImages_small = {}
obj_width = 0
obj_height = 0
scale = 1.5

myChess = chess.Chess
myChess.reset(myChess)
user1 = chess.ChessAI("White", myChess)
#user2 = chess.ChessHuman("Black", myChess)

##################################################
# Drawing Functions
##################################################
def loadObjImages(objImages):
    global obj_width, obj_height

    objs = [
        'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackPawn',
        'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhitePawn',
        'Empty'
    ]

    for obj in objs:
        img = cv2.imread(f"img/{obj}.png")
        objImages[obj] = cv2.resize(img, (int(img.shape[1] * scale), int(img.shape[0] * scale)))
        objImages_small[obj] = cv2.resize(img, (int(img.shape[0] * scale / 2), int(img.shape[1] * scale / 2)))
        obj_width = objImages[obj].shape[1]
        obj_height = objImages[obj].shape[0]

    #print(f"Object Size : {obj_width} x {obj_height}")

def draw_border(image, x, y, color, width):
    pt1 = ( x * obj_width + width, y * obj_height + width )
    pt2 = ( x * obj_width + obj_width - width, y * obj_height + obj_height - width )
    cv2.rectangle(image, pt1, pt2, color, width)

def draw_object(image, x, y):
    objName = myChess.getObjectFullName(myChess, x, y)

    # Draw Object
    pX = x * obj_width + 1
    pY = y * obj_height + 1
    image[pY:pY+obj_height, pX:pX+obj_width] = objImages[objName]

    # Draw Border
    posName = myChess.getPosName(myChess, x, y)
    if x != myChess.cursor[0] or y != myChess.cursor[1]:
        draw_border(image, x, y, (0, 0, 0), 1)
    elif myChess.availables.isAvaiable(posName):
        draw_border(image, x, y, (255, 0, 0), 3)
    elif myChess.array[y][x] != None and myChess.array[y][x].getColor() == myChess.turn.getThisTurnName():
        draw_border(image, x, y, (255, 0, 0), 3)
    else:
        draw_border(image, x, y, (0, 0, 255), 3)

def drawKilledObject(image, x, y, objName):
    global obj_width, obj_height
    print(f"Draw Killed Obj x={x}, y={y}")

    # Draw Object
    pX = int(500 * scale + x * obj_width / 2 + 1)
    pY = int(50 * scale + y * obj_height / 2 + 1)
    image[pY:int(pY + obj_height / 2), pX:int(pX + obj_width / 2)] = objImages_small[objName]

def draw_selected(image):
    # Draw selected
    selected = myChess.selected
    if selected[0] >= 8 or selected[1] >= 8:
        return
    print(f"Draw selected")
    cv2.circle(image, (int(selected[0] * obj_width + obj_width / 2), int(selected[1] * obj_height + obj_height / 2)), int(obj_width / 3), (255,255,0), 2)

def draw_availables(image):
    for pos in myChess.availables.get():
        print(f"Draw Availables {pos}")
        x, y = myChess.getXY(myChess, pos)
        cv2.circle(image, (int(x * obj_width + obj_width / 2), int(y * obj_height + obj_height / 2)), int(obj_width / 3), (0,0,255), 2)

def delete_info_background(image):
    pt1 = ( int(400 * scale), 0 )
    pt2 = ( int(800 * scale), int(400 * scale) )
    cv2.rectangle(image, pt1, pt2, (255,255,255), -1)

def draw_info(image):
    delete_info_background(image)

    turn = myChess.turn.getThisTurnName()
    if turn == "White":
        textPos = [ int(400 * scale), int(375 * scale) ]
    else:
        textPos = [ int(400 * scale), int(25 * scale) ]
    cv2.putText(image, f"< {turn}", textPos, 1, 1, (0, 0, 0), 2)

    cv2.putText(image, "ESC : Exit", [ int(500 * scale), 25 ], 1, 1, (255, 255, 0), 2)
    cv2.putText(image, "R : Reset", [ int(500 * scale), 50 ], 1, 1, (255, 255, 0), 2)

    if myChess.turn.gameover:
        cv2.putText(image, "GAME OVER!", [ int(400 * scale), int(50 * scale) ], 1, 1, (0, 0, 255), 2)

    i = 0
    for killedObj in myChess.history.arrKilled:
        if killedObj == None:
            break
        drawKilledObject(image, int(i % 4), int(1 + i / 4), killedObj.getFullName())
        i = i + 1

def draw():
    image_org = cv2.imread('img/background.png')
    image = cv2.resize(image_org, (int(image_org.shape[1] * scale), int(image_org.shape[0] * scale)))
    cv2.imshow('Chess', image)
    cv2.setMouseCallback("Chess", mouse_event, image)
    #print(f"Image Size({image.shape[1]} x {image.shape[0]} x {image.shape[2]})")
    loadObjImages(objImages)

    for x in range(8):
        for y in range(8):
            draw_object(image, x, y)

    draw_selected(image)
    draw_availables(image)
    draw_info(image)

    cv2.imshow('Chess', image)
##################################################
# Mouse Event
##################################################
def mouse_event(event, x, y, flags, param):
    global obj_width, obj_height

    if event == cv2.EVENT_FLAG_LBUTTON:
        myChess.clicked(myChess, int(x / obj_width), int(y / obj_height))
        draw()

##################################################
# Initialization
##################################################
draw()

##################################################
# Main Task
##################################################
while True:
    try:
        cv2.getWindowProperty("Chess", 0)
    except:
        break

    k = cv2.waitKeyEx(0)
    print(f"{k} key pressed")
    if k == 27:
        cv2.destroyAllWindows()
        break
    elif k == ord('R'):
        myChess.reset(myChess, True)
        draw()
    elif k == ord('r'):
        myChess.reset(myChess)
        draw()
    elif k == ord('b'):
        myChess.cancelselected(myChess)
        if myChess.rollback(myChess):
            # Castling rollback takes 2 actions.
            myChess.rollback(myChess)
        draw()
    # Arrow Keys (8BitDo Gamepad)
    elif k == ord('e') or k == 0x250000:
        myChess.cursor[0] = (myChess.cursor[0] + 7) % 8
        draw()
    elif k == ord('f') or k == 0x270000:
        myChess.cursor[0] = (myChess.cursor[0] + 1) % 8
        draw()
    elif k == ord('c') or k == 0x260000:
        myChess.cursor[1] = (myChess.cursor[1] + 7) % 8
        draw()
    elif k == ord('d') or k == 0x280000:
        myChess.cursor[1] = (myChess.cursor[1] + 1) % 8
        draw()
    elif k == ord('g') or k == ord(' '):
        myChess.clicked(myChess, myChess.cursor[0], myChess.cursor[1])
        draw()

    elif k == ord('+'):
        scale += 0.1
        draw()
    elif k == ord('-'):
        scale -= 0.1
        draw()