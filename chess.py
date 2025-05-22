# Check Class

import copy

class Object:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.moved = False

    def getFullName(self):
        return f"{self.color}{self.name}"

    name = ""
    color = ""
    moved = False

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
        self.arrKilled.clear()

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

    def addRedraw(self, x, y):
        posName = self.getPosName(self, x, y)
        self.addRedrawByPosName(self, posName)

    def addRedrawByPosName(self, posName):
        print(f"Add Redraw {posName}")
        self.need_to_redraw.add(posName)
    
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
        if self.array[y][x].moved == True:
            return False
        if self.array[y][x+1] == None and self.array[y][x+2] == None and self.array[y][x+3] != None and self.array[y][x+3].moved == False:
            self.addAvailable(self, x + 2, y)
        if self.array[y][x-1] == None and self.array[y][x-2] == None and self.array[y][x-3] == None and self.array[y][x-4] != None and self.array[y][x-4].moved == False:
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

    def swap(self, x, y, x2, y2):
        # Make swap
        tmp = self.array[x][y]
        self.array[x][y] = self.array[x2][y2]
        self.array[x2][y2] = tmp

        self.array[x][y].moved = True
        self.array[x2][y2].moved = True

    def movement(self, x, y, newX, newY):
        print(f"Move({x}, {y} => {newX}, {newY})")

        # Add Killed List
        if self.isEnermy(self, newX, newY):
            self.arrKilled.append(self.array[newY][newX].getFullName())

        # Moved Flag On
        self.array[y][x].moved = True

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

    arrKilled = []

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