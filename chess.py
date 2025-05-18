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
turn = "White"

availables = []

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
    print(f"Draw Obj x={x}, y={y}")

    x = x * 49 + 1
    y = y * 49 + 1
    image[y:y+49, x:x+49] = objImages[objName]

def draw_cursor(image, cursor):
    if cursor[0] < 8 and cursor[1] < 8:
        print(f"Draw Cursor x={cursor[0]}, y={cursor[1]}")
        cv2.circle(image, (cursor[0] * 49 + 24, cursor[1] * 49 + 24), 10, (255,255,0), 2)

def draw_availables(image, availables):
    for pos in availables:
        print(f"Draw Available x={pos[0]}, y={pos[1]}")
        cv2.circle(image, (pos[0] * 49 + 24, pos[1] * 49 + 24), 10, (0,0,255), 2)

def updateArea(image, pos):
    if pos[0] >= 8 or pos[1] >= 8:
        return
    
    print(f"Update Area x={pos[0]}, y={pos[1]}")
    draw_object(image, pos[0], pos[1], array[pos[1]][pos[0]])
    draw_rectangle(image, pos[0], pos[1])

def updateWindowAll(image):
    for y in range(8):
        for x in range(8):
            draw_object(image, x, y, array[y][x])
            draw_rectangle(image, x, y)

    cv2.imshow('Chess', image)

##################################################
# Check Movement
##################################################
def getObjName(cursor, deltaX, deltaY):
    x = cursor[0]
    y = cursor[1]
    if x + deltaX < 0 or x + deltaX >= 8:
        return ""
    if y + deltaY < 0 or y + deltaY >= 8:
        return ""
    return str(array[y + deltaY][x + deltaX])

def getMyPrefix():
    return turn

def getEnermyPrefix():
    if turn == "White":
        return "Black"
    return "White"

def checkAvailable_RightAngle(cursor, count):
    dirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    for dir in dirs:
        for i in range(1, count):
            objName = getObjName(cursor, dir[0] * i, dir[1] * i)
            if objName == "" or objName.startswith(getMyPrefix()):
                break
            elif objName.startswith(getEnermyPrefix()):
                availables.append([cursor[0] + dir[0] * i, cursor[1] + dir[1] * i])
                break
            else:
                availables.append([cursor[0] + dir[0] * i, cursor[1] + dir[1] * i])

def checkAvailable_Diagonal(cursor, count):
    dirs = [ [1, 1], [1, -1], [-1, 1], [-1, -1] ]
    for dir in dirs:
        for i in range(1, count):
            objName = getObjName(cursor, dir[0] * i, dir[1] * i)
            if objName == "" or objName.startswith(getMyPrefix()):
                break
            elif objName.startswith(getEnermyPrefix()):
                availables.append([cursor[0] + dir[0] * i, cursor[1] + dir[1] * i])
                break
            else:
                availables.append([cursor[0] + dir[0] * i, cursor[1] + dir[1] * i])

def checkAvailable_Knight(cursor):
    dirs = [ [1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1] ]
    for dir in dirs:
        objName = getObjName(cursor, dir[0], dir[1])
        if objName == "" or objName.startswith(getMyPrefix()):
            continue
        else:
            availables.append([cursor[0] + dir[0], cursor[1] + dir[1]])

def checkAvailable(cursor):
    global availables

    x = cursor[0]
    y = cursor[1]
    objName = str(array[y][x])

    print(f"Check available x={x}, y={y}, objName={objName}")

    if objName == "BlackPawn":
        if getObjName(cursor, 0, 1) == "Empty":
            availables.append([x, y+1])
            if y == 1 and getObjName(cursor, 0, 2) == "Empty":
                availables.append([x, y+2])
        if getObjName(cursor, 1, 1).startswith(getEnermyPrefix()):
            availables.append([x+1, y+1])
        if getObjName(cursor, -1, 1).startswith(getEnermyPrefix()):
            availables.append([x-1, y+1])
    elif objName == "WhitePawn":
        if getObjName(cursor, 0, -1) == "Empty":
            availables.append([x, y-1])
            if y == 6 and getObjName(cursor, 0, -2) == "Empty":
                availables.append([x, y-2])
        if getObjName(cursor, 1, -1).startswith(getEnermyPrefix()):
            availables.append([x+1, y-1])
        if getObjName(cursor, -1, -1).startswith(getEnermyPrefix()):
            availables.append([x-1, y-1])
    elif objName.endswith("King"):
        checkAvailable_RightAngle(cursor, 2)
        checkAvailable_Diagonal(cursor, 2)
    elif objName.endswith("Queen"):
        checkAvailable_RightAngle(cursor, 8)
        checkAvailable_Diagonal(cursor, 8)
    elif objName.endswith("Bishop"):
        checkAvailable_Diagonal(cursor, 8)
    elif objName.endswith("Rook"):
        checkAvailable_RightAngle(cursor, 8)
    elif objName.endswith("Knight"):
        checkAvailable_Knight(cursor)

##################################################
# Mouse Event
##################################################
def selectNew(x, y, cursor):
    global turn

    print(f"Select New x={x}, y={y}")

    objName = array[y][x]
    print(f"ObjName : {objName}")
    if objName.startswith(turn):
        cursor[0] = x
        cursor[1] = y
        updateArea(image, cursor)
        draw_cursor(image, cursor)
        checkAvailable(cursor)
        draw_availables(image, availables)
        cv2.imshow('Chess', image)
    else:
        print(f"Not Turn : turn={turn}")

def cancelCursor(x,y, cursor):
    updateArea(image, cursor)
    cursor[0] = 8
    cursor[1] = 8
    for pt in availables:
        updateArea(image, pt)
    availables.clear()
    cv2.imshow('Chess', image)

def nextTurn():
    global turn
    turn = getEnermyPrefix()

def movement(cursor, newpos):
    array[newpos[1]][newpos[0]] = array[cursor[1]][cursor[0]]
    array[cursor[1]][cursor[0]] = 'Empty'
    updateArea(image, cursor)
    updateArea(image, newpos)
    for pt in availables:
        if pt == newpos:
            continue
        updateArea(image, pt)
    availables.clear()
    cursor[0] = 8
    cursor[1] = 8
    cv2.imshow('Chess', image)

    nextTurn()

def clicked(x,y):
    global cursor
    
    xIdx = int(x / 49)
    yIdx = int(y / 49)

    print(f"Click x={xIdx}, y={yIdx}")
    print(f"Cursor x={cursor[0]}, y={cursor[1]}")

    # Invalid Range
    if cursor[0] >=8 or cursor[1] >= 8:
        selectNew(xIdx, yIdx, cursor)
        return

    # Cancel Cursor
    if cursor[0] == xIdx and cursor[1] == yIdx:
        cancelCursor(xIdx, yIdx, cursor)
        return

    # Move Cursor
    for pt in availables:
        if pt[0] == xIdx and pt[1] == yIdx:
            movement(cursor, pt)

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