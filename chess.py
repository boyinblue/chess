import cv2

class Object:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.move_cnt = 0

    def getFullName(self):
        return f"{self.color}{self.name}"

    name = ""
    color = ""
    move_cnt = 0

class Movement:
    def __init__(self, x, y, obj, newX, newY, newObj):
        self.x = x
        self.y = y
        self.obj = obj
        self.newX = newX
        self.newY = newY
        self.newObj = newObj

    def print(self):
        objName = self.obj.getFullName()
        newObjName = "Empty"
        if self.newObj != None:
            newObjName = self.newObj.getFullName()
        print(f"Movement : {self.x} {self.y} {objName} {self.newX} {self.newY} {newObjName}")

    x = 0
    y = 0
    obj = None
    newX = 0
    newY = 0
    newObj = None

class History:
    def reset(self):
        self.arrHistory.clear()
        self.arrKilled.clear()

    def append(self, x, y, obj, newX, newY, newObj):
        moveInfo = Movement(x, y, obj, newX, newY, newObj)
        print(f"Move Info : {moveInfo}")
        self.arrHistory.append(moveInfo)

        if newObj != None:
            self.arrKilled.append(newObj)

    def rollback(self):
        if len(self.arrHistory) == 0:
            return None

        last = self.arrHistory.pop()
        if last == None:
            return last
        last.print()

        return last

    arrHistory = []
    arrKilled = []

# Check Class
class Chess:
    def __init__(self):
        self.reset(self)

    def reset(self, bug = False):
        self.turn = "White"
        self.winner = ""
        self.gameover = False
        for x in range(8):
            for y in range(8):
                obj_name = self.array_org[y][x]
                print(f"Generate Object x={x}, y={y}, {obj_name}")
                if obj_name != "Empty":
                    self.array[y][x] = Object(obj_name[5:], obj_name[0:5])
                elif bug == False:
                    self.array[y][x] = None
        self.history.reset()

        self.availables.clear()
        self.need_to_redraw.clear()

        self.cursor[0] = 8
        self.cursor[1] = 8

    # Basic I/O functions
    def getObject(self, x, y):
        if not self.isValidPos(self, x, y):
            return None
        return self.array[y][x]
    
    def getObjectName(self, x, y):
        obj = self.getObject(self, x, y)
        if obj == None:
            return ""
        return obj.name
    
    def getObjectFullName(self, x, y):
        obj = self.getObject(self, x, y)
        if obj == None:
            return "Empty"
        return obj.getFullName()
    
    def getObjectColor(self, x, y):
        obj = self.getObject(self, x, y)
        if obj == None:
            return ""
        return obj.color
    
    def isValidPos(self, x, y):
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        return True
    
    def isEmpty(self, x, y):
        if self.isValidPos(self, x, y) and self.array[y][x] == None:
            return True
        return False
    
    def isEnermy(self, x, y):
        if self.isValidPos(self, x, y) and self.array[y][x] != None and self.array[y][x].color == self.getNextTurnName(self):
            return True
        return False
    
    def isAlly(self, x, y):
        if self.isValidPos(self, x, y) and self.array[y][x] != None and self.array[y][x].color == self.getThisTurnName(self):
            return True
        return False
    
    # Basic I/O functions
    def getThisTurnName(self):
        return self.turn
    
    def getNextTurnName(self):
        if self.turn == "White":
            return "Black"
        return "White"

    def nextTurn(self):
        self.turn = self.getNextTurnName(self)

    def getPosName(self, x, y):
        ColName = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
        posName = f"{y}{ColName[x]}"
        return posName
    
    def getXY(self, posName):
        y = ord(posName[0])-ord('0')
        x = ord(posName[1])-ord('A')
        return x, y
    
    # Check Movement functions
    def addAvailable(self, x, y):
        posName = self.getPosName(self, x, y)
        print(f"Add Available {posName}")
        self.availables.add(posName)

    def checkUnitAvailable(self, x, y):
        if not self.isValidPos(self, x, y):
            return False
        elif self.isAlly(self, x, y):
            return False
        
        self.addAvailable(self, x, y)
        if self.isEnermy(self, x, y):
            return False
        return True #Continue Checking
        
    def checkAvailableByDirList(self, x, y, dirs, count):
        for dir in dirs:
            for i in range(0, count):
                if False == self.checkUnitAvailable(self, x + dir[0] * (i+1), y + dir[1] * (i+1)):
                    break

    def checkCastling(self, x, y):
        if self.array[y][x].move_cnt != 0:
            return False
        if self.array[y][x+1] == None and self.array[y][x+2] == None and self.array[y][x+3] != None and self.array[y][x+3].move_cnt == 0:
            self.addAvailable(self, x + 2, y)
        if self.array[y][x-1] == None and self.array[y][x-2] == None and self.array[y][x-3] == None and self.array[y][x-4] != None and self.array[y][x-4].move_cnt == 0:
            self.addAvailable(self, x - 2, y)

    def checkAvailable_Pawn(self):
        y_offset = 1
        y_org_pos = 1
        obj = self.getObject(self, self.cursor[0], self.cursor[1])
        if( obj.color == "White" ):
            y_offset = -1
            y_org_pos = 6

        if self.isEmpty(self, self.cursor[0], self.cursor[1] + y_offset):
            self.addAvailable(self, self.cursor[0], self.cursor[1] + y_offset)
            if self.cursor[1] == y_org_pos and self.isEmpty(self, self.cursor[0], self.cursor[1] + y_offset * 2):
                self.addAvailable(self, self.cursor[0], self.cursor[1] + y_offset * 2)
        if self.isEnermy(self, self.cursor[0] + 1, self.cursor[1] + y_offset):
            self.addAvailable(self, self.cursor[0] + 1, self.cursor[1] + y_offset)
        if self.isEnermy(self, self.cursor[0] - 1, self.cursor[1] + y_offset):
            self.addAvailable(self, self.cursor[0] - 1, self.cursor[1] + y_offset)

    def checkAvailable(self, x, y):
        objName = self.getObjectName(self, x, y)

        print(f"Check available x={x}, y={y}, objName={objName}")

        if objName == "King":
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.EveryDirs, 1)
            self.checkCastling(self, self.cursor[0], self.cursor[1])
        elif objName == "Queen":
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.EveryDirs, 7)
        elif objName == "Bishop":
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.DiagonalDirs, 7)
        elif objName == "Rook":
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.RightAngleDirs, 7)
        elif objName == "Knight":
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.KnightDirs, 1)
        elif objName == "Pawn":
            self.checkAvailable_Pawn(self)

    # Redraw Data Functions
    def addRedraw(self, x, y):
        posName = self.getPosName(self, x, y)
        self.addRedrawByPosName(self, posName)

    def addRedrawByPosName(self, posName):
        print(f"Add Redraw {posName}")
        self.need_to_redraw.add(posName)

    # Mouse Event
    def selectObject(self, x, y):
        obj = self.getObject(self, x, y)
        if obj != None and obj.color == self.getThisTurnName(self):
            self.cursor[0] = x
            self.cursor[1] = y
            self.checkAvailable(self, x, y)
            self.addRedraw(self, x, y)
            for posName in self.availables:
                self.addRedrawByPosName(self, posName)
        else:
            print(f"Not Turn : turn={self.getThisTurnName(self)}")

    def cancelCursor(self, x,y):
        self.cursor[0] = 8
        self.cursor[1] = 8
        self.addRedraw(self, x, y)
        for posName in self.availables:
            self.addRedrawByPosName(self, posName)
        self.availables.clear()

    def clicked(self, x, y):
        if self.gameover == True:
            return

        print(f"")
        print(f"Clicked x={x}, y={y}")

        # Nothing selected
        if self.cursor[0] >= 8 or self.cursor[1] >= 8:
            self.selectObject(self, x, y)
            return

        # Cancel Cursor
        if self.cursor[0] == x and self.cursor[1] == y:
            self.cancelCursor(self, x, y)
            return

        # Move Cursor
        for pt in self.availables:
            posX, posY = self.getXY(self, pt)
            if posX == x and posY == y:
                self.moveTo(self, self.cursor[0], self.cursor[1], posX, posY)
                self.cancelCursor(self, self.cursor[0], self.cursor[1])
                break

    # Actual Movement Functions
    def swap(self, x, y, x2, y2):
        # Make swap
        tmp = self.array[x][y]
        self.array[x][y] = self.array[x2][y2]
        self.array[x2][y2] = tmp

        self.array[x][y].move_cnt += 1
        self.array[x2][y2].move_cnt += 1

    def movement(self, x, y, newX, newY):
        print(f"Move({x}, {y} => {newX}, {newY})")

        # Move Count
        self.array[y][x].move_cnt += 1

        # Write History
        self.history.append(x, y, self.array[y][x], newX, newY, self.array[newY][newX])

        # Check Game Over
        obj = self.array[newY][newX]
        if obj is not None and obj.name == "King":
            self.gameover = True
            self.winner = self.getThisTurnName(self)

        # Make movement
        self.array[newY][newX] = self.array[y][x]
        self.array[y][x] = None
        self.addRedraw(self, x, y)
        self.addRedraw(self, newX, newY)

        # Pawn Upgrade
        obj = self.array[newY][newX]
        if obj is not None and obj.name == "Pawn" and obj.color == "White" and newY == 0:
            self.array[newY][newX].name = "Queen"
        elif obj is not None and obj.name == "Pawn" and obj.color == "Black" and newY == 7:
            obj = self.array[newY][newX].name = "Queen"

    def moveTo(self, x, y, newX, newY):
        # Castling
        obj = self.array[y][x]
        if obj is not None and obj.name == "King" and newX - x == 2:
            # Kingside castling
            self.movement(self, x, y, x + 2, y)
            self.movement(self, x + 3, y, x + 1, y)
        elif obj is not None and obj.name == "King" and  x - newX == 2:
            # Queenside castling
            self.movement(self, x, y, x - 2, y)
            self.movement(self, x - 4, y, x - 1, y)
        else:
            # Make Movement
            self.movement(self, x, y, newX, newY)

        # Next Turn
        if self.gameover != True:
            self.nextTurn(self)

    def rollback(self):
        mov = self.history.rollback()
        if mov == None:
            print(f"Nothing in history")
            return

        if mov.newObj == None:
            print(f"Set {mov.newX}, {mov.newY} : Empty")
            self.array[mov.newY][mov.newX] = None
        else:
            print(f"Set {mov.newX}, {mov.newY} : {mov.newObj.getFullName()}")
            self.array[mov.newY][mov.newX] = mov.newObj

        print(f"Set {mov.x}, {mov.y} : {mov.obj.getFullName()}")
        self.array[mov.y][mov.x] = mov.obj

        self.addRedraw(self, mov.x, mov.y)
        self.addRedraw(self, mov.newX, mov.newY)

        self.nextTurn(self)

    array_org = [
        [ 'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackBishop',  'BlackKnight',  'BlackRook' ],
        [ 'BlackPawn',  'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn' ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'WhitePawn',  'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn' ],
        [ 'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhiteBishop',  'WhiteKnight',  'WhiteRook' ]
    ]

    array = [
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ],
        [ None, None, None, None, None, None, None, None ]
    ]

    history = History()

    RightAngleDirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    DiagonalDirs = [ [1, 1], [1, -1], [-1, 1], [-1, -1] ]
    EveryDirs = RightAngleDirs + DiagonalDirs
    KnightDirs = [ [1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1] ]

    cursor = [8, 8]
    turn = "White"
    winner = ""
    gameover = False
    AI = True

    availables = set()
    need_to_redraw = set()

class ChessView(Chess):
    def __init__(self):
        print(f"ChessView Initialize")
        super().__init__()

        self.scale = 1.5
        self.loadObjImages()

        self.image_org = cv2.imread('img/background.png', cv2.IMREAD_UNCHANGED)
        self.image = cv2.resize(self.image_org, (int(self.image_org.shape[1] * self.scale), int(self.image_org.shape[0] * self.scale)))
        print(f"Image Size({self.image.shape[1]} x {self.image.shape[0]} x {self.image.shape[2]})")
        #cv2.imshow('Chess', self.image)

        self.updateWindowAll()
        #cv2.setMouseCallback("Chess", mouse_event, self.image)

    def loadObjImages(self):
        objs = [
            'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackPawn',
            'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhitePawn',
            'Empty'
        ]

        for obj in objs:
            img = cv2.imread(f"img/{obj}.png", cv2.IMREAD_UNCHANGED)
            self.objImages[obj] = cv2.resize(img, (int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)))
            self.objImages_small[obj] = cv2.resize(img, (int(img.shape[0] * self.scale / 2), int(img.shape[1] * self.scale / 2)))
            obj_width = self.objImages[obj].shape[1]
            obj_height = self.objImages[obj].shape[0]
            print(f"Loading Obj Image : {obj_width} x {obj_height}")

        print(f"Object Size : {obj_width} x {obj_height}")

    def draw_object(self, x, y):
        obj = self.array[y][x]
        if obj == None:
            return
        objName = obj.getFullName()

        # Draw Object
        print(f"Draw Obj x={x}, y={y}, name={objName}")
        pX = x * self.obj_width + 1
        pY = y * self.obj_height + 1
        cv2.seamlessClone(self.objImages[objName], self.image, (self.obj_width, self.obj_height), (pX, pY), cv2.NORMAL_CLONE)
        #self.image[pY:pY+self.obj_height, pX:pX+self.obj_width] = self.objImages[objName]
        #mask = objImages[objName][:,:,3]
        #bit = objImages[objName][:,:,0:2]

        # Draw Rectangle
        pt1 = ( x * self.obj_width + 1, y * self.obj_height + 1 )
        pt2 = ( x * self.obj_width + self.obj_width, y * self.obj_height + self.obj_height )
        cv2.rectangle(self.image, pt1, pt2, (0, 0, 0), 1)

    def drawKilledObject(self, x, y, obj):
        print(f"Draw Killed Obj x={x}, y={y}")
        objName = obj.getFullName()

        # Draw Object
        pX = int(500 * self.scale + x * self.obj_width / 2 + 1)
        pY = int(50 * self.scale + y * self.obj_height / 2 + 1)
        self.image[pY:int(pY + self.obj_height / 2), pX:int(pX + self.obj_width / 2)] = self.objImages_small[objName]

    def draw_cursor(self):
        # Draw Cursor
        cursor = self.cursor
        if cursor[0] >= 8 or cursor[1] >= 8:
            return
        print(f"Draw Cursor")
        cv2.circle(self.image, (int(cursor[0] * self.obj_width + self.obj_width / 2), int(cursor[1] * self.obj_height + self.obj_height / 2)), int(self.obj_width / 3), (255,255,0), 2)

    def draw_availables(self):
        for pos in self.availables:
            print(f"Draw Availables {pos}")
            x, y = self.getXY(self, pos)
            cv2.circle(self.image, (int(x * self.obj_width + self.obj_width / 2), int(y * self.obj_height + self.obj_height / 2)), int(self.obj_width / 3), (0,0,255), 2)

    def delete_info_background(self):
        pt1 = ( int(400 * self.scale), 0 )
        pt2 = ( int(800 * self.scale), int(400 * self.scale) )
        cv2.rectangle(self.image, pt1, pt2, (255,255,255), -1)

    def draw_info(self):
        self.delete_info_background()

        turn = self.getThisTurnName()
        if self.turn == "White":
            textPos = [ int(400 * self.scale), int(375 * self.scale) ]
        else:
            textPos = [ int(400 * self.scale), int(25 * self.scale) ]
        cv2.putText(self.image, f"< {turn}", textPos, 1, 1, (0, 0, 0), 2)

        cv2.putText(self.image, "ESC : Exit", [ int(500 * self.scale), 25 ], 1, 1, (255, 255, 0), 2)
        cv2.putText(self.image, "R : Reset", [ int(500 * self.scale), 50 ], 1, 1, (255, 255, 0), 2)

        if self.gameover:
            cv2.putText(self.image, "GAME OVER!", [ int(400 * self.scale), int(50 * self.scale) ], 1, 1, (0, 0, 255), 2)

        i = 0
        for killedObj in self.history.arrKilled:
            if killedObj == None:
                break
            self.drawKilledObject(self.image, int(i % 4), int(1 + i / 4), killedObj)
            i = i + 1

    def redraw(self):
        newPos = self.need_to_redraw
        for posName in newPos:
            print(f"Redraw {posName}")
            if posName == []:
                continue
            x, y = self.getXY(self, posName)
            self.draw_object(self, x, y)

        self.draw_cursor(self)
        self.draw_availables(self)
        self.draw_info(self)

        self.need_to_redraw.clear()
        cv2.imshow('Chess', self.image)

    def updateWindowAll(self):
        for y in range(8):
            for x in range(8):
                self.draw_object(x, y)

        self.draw_cursor()
        self.draw_availables()
        self.draw_info()

        self.need_to_redraw.clear()
        cv2.imshow('Chess', self.image)

    def mouseClicked(self, x, y):
        self.clicked(self, int(x / self.obj_width), int(y / self.obj_height))
        self.redraw(self)

    ##################################################
    # Initialization
    ##################################################
    objImages = {}
    objImages_small = {}
    obj_width = 0
    obj_height = 0
    scale = 1.5
    image = None
    image_org = None