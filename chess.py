import cv2

##################################################
# Global Variables
##################################################

array = [
    [ 'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackBishop',  'BlackKnight',  'BlackRook' ],
    [ 'BlackPawn',  'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn' ],
    [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
    [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
    [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
    [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
    [ 'WhitePawn',  'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn' ],
    [ 'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhiteBishop',  'WhiteKnight',  'WhiteRook' ]
]

objImages = {}

cursor = [8, 8]
turn = "Black"

##################################################
# Drawing Functions
##################################################
def loadObjImages(objImages):
    for y in range(8):
        for x in range(8):
            obj_name = array[y][x]
            img = cv2.imread(f"img/{obj_name}.png")
            objImages[obj_name] = img

def draw_rectangle(image, x, y):
    pt1 = ( x * 49 + 1, y * 49 + 1 )
    pt2 = ( x * 49 + 49, y * 49 + 49 )
    cv2.rectangle(image, pt1, pt2, (0, 0, 0), 1)

def draw_object(image, x, y, objName):
    print(f"Draw Obj x={x}, y={y})")

    x = x * 49 + 1
    y = y * 49 + 1
    image[y:y+49, x:x+49] = objImages[objName]

def draw_cursor(image, cur):
    if cursor[0] < 8 and cursor[1] < 8:
        print(f"Draw Cursor x={cursor[0]}, y={cursor[1]}")
        cv2.circle(image, (cursor[0] * 49 + 24, cursor[1] * 49 + 24), 10, (255,255,0), 2)

def updateArea(image, pos):
    if pos[0] >= 8 or pos[1] >= 8:
        return
    
    print(f"Update Area x={pos[0]}, y={pos[1]})")
    draw_object(image, pos[0], pos[1], array[pos[1]][pos[0]])
    draw_rectangle(image, pos[0], pos[1])

def updateWindowAll(image):
    for y in range(8):
        for x in range(8):
            draw_object(image, x, y, array[y][x])
            draw_rectangle(image, x, y)

    cv2.imshow('Chess', image)

##################################################
# Mouse Event
##################################################
def selectNew(x, y, cursor):
    global turn

    print(f"Select New x={x}, y={y}")

    objName = array[y][x]
    print(f"ObjName : {objName}")
    if objName.startswith(turn):
        cursor = [x, y]
        updateArea(image, cursor)
        draw_cursor(image, cursor)
        cv2.imshow('Chess', image)

def cancelCursor(x,y):
    updateArea(image, cursor)
    cursor = [8, 8]
    cv2.imshow('Chess', image)

def clicked(x,y):
    global cursor
    
    xIdx = int(x / 50)
    yIdx = int(y / 50)

    print(f"Click x={xIdx}, y={yIdx}")

    # Invalid Range
    if cursor[0] >=8 or cursor[1] >= 8:
        selectNew(xIdx, yIdx, cursor)
        return

    # Cancel Cursor
    if cursor[0] == xIdx and cursor[1] == yIdx:
        cancelCursor(xIdx, yIdx)
        return

    # New Select
    if cursor[0] >= 8 or cursor[1] >= 8:
        selectNew(image, array, cursor)
    # Move To
    else:
        
            cursor = [xIdx, yIdx]
            updateArea(image, cursor)
            draw_cursor(image, cursor)
        

def mouse_event(event, x, y, flags, param):
    if event == cv2.EVENT_FLAG_LBUTTON:
        clicked(x,y)

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
    k = cv2.waitKey(0) & 0xFF
    if k == 27:
        cv2.destroyAllWindows()
        break