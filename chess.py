# Check Class

import copy

class Chess:
    def __init__(self):
        turn = "White"
        self.array = copy.deepcopy(self.array_org)

        self.availables.clear()
        self.need_to_redraw.clear()

        self.cursor[0] = 8
        self.cursor[1] = 8

    def reset(self):
        self.__init__(self)

    # Basic I/O functions
    def getObjectName(self, x, y):
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return ""
        return str(self.array[y][x])
    
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
        posName = f"{y}{self.ColName[x]}"
        return posName
    
    def getXY(self, posName):
        y = ord(posName[0])-ord('0')
        x = ord(posName[1])-ord('A')
        return x, y
    
    # Check Movement functions
    def addAvailable(self, x, y):
        posName = self.getPosName(self, x, y)
        print(f"Add Available {posName}")
        self.availables.append(posName)

    def addRedraw(self, x, y):
        posName = self.getPosName(self, x, y)
        self.addRedrawByPosName(self, posName)

    def addRedrawByPosName(self, posName):
        self.need_to_redraw.append(posName)
    
    def checkUnitAvailable(self, x, y):
        objectName = str( self.getObjectName(self, x, y) )
        if objectName == "" or objectName.startswith(self.getThisTurnName(self)):
            return False
        self.addAvailable(self, x, y)
        if objectName.startswith(self.getNextTurnName(self)):
            return False
        return True
        
    def checkAvailableByDirList(self, x, y, dirs, count):
        for dir in dirs:
            for i in range(0, count):
                if False == self.checkUnitAvailable(self, x + dir[0] * (i+1), y + dir[1] * (i+1)):
                    break

    def checkAvailable_Pawn(self):
        y_offset = 1
        y_org_pos = 1
        objName = str( self.getObjectName(self, self.cursor[0], self.cursor[1]) )
        if( objName.startswith("White") ):
            y_offset = -1
            y_org_pos = 6

        if self.getObjectName(self, self.cursor[0], self.cursor[1] + y_offset) == "Empty":
            self.addAvailable(self, self.cursor[0], self.cursor[1] + y_offset)
            if self.cursor[1] == y_org_pos and self.getObjectName(self, self.cursor[0], self.cursor[1] + y_offset * 2) == "Empty":
                self.addAvailable(self, self.cursor[0], self.cursor[1] + y_offset * 2)
        if self.getObjectName(self, self.cursor[0] + 1, self.cursor[1] + y_offset).startswith(self.getNextTurnName(self)):
            self.addAvailable(self, self.cursor[0] + 1, self.cursor[1] + y_offset)
        if self.getObjectName(self, self.cursor[0] - 1, self.cursor[1] + y_offset).startswith(self.getNextTurnName(self)):
            self.addAvailable(self, self.cursor[0] - 1, self.cursor[1] + y_offset)

    def checkAvailable(self, x, y):
        objName = self.getObjectName(self, x, y)

        print(f"Check available x={x}, y={y}, objName={objName}")

        if objName.endswith("King"):
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.EveryDirs, 1)
        elif objName.endswith("Queen"):
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.EveryDirs, 7)
        elif objName.endswith("Bishop"):
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.DiagonalDirs, 7)
        elif objName.endswith("Rook"):
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.RightAngleDirs, 7)
        elif objName.endswith("Knight"):
            self.checkAvailableByDirList(self, self.cursor[0], self.cursor[1], self.KnightDirs, 1)
        elif objName.endswith("Pawn"):
            self.checkAvailable_Pawn(self)

    # Mouse Event
    def selectObject(self, x, y):
        objName = str( self.getObjectName(self, x, y))
        if objName.startswith(self.getThisTurnName(self)):
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

    def movement(self, newX, newY):
        self.array[newY][newX] = self.array[self.cursor[1]][self.cursor[0]]
        self.array[self.cursor[1]][self.cursor[0]] = 'Empty'
        self.cancelCursor(self, self.cursor[0], self.cursor[1])
        self.nextTurn(self)

    def clicked(self, x, y):
        print(f"")
        print(f"Clicked x={x}, y={y}")

        # Invalid Range
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
                self.movement(self, x, y)

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
        [ 'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackBishop',  'BlackKnight',  'BlackRook' ],
        [ 'BlackPawn',  'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn',    'BlackPawn' ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'Empty',      'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty',        'Empty'     ],
        [ 'WhitePawn',  'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn',    'WhitePawn' ],
        [ 'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhiteBishop',  'WhiteKnight',  'WhiteRook' ]
    ]
    
    ColName = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]

    RightAngleDirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    DiagonalDirs = [ [1, 1], [1, -1], [-1, 1], [-1, -1] ]
    EveryDirs = RightAngleDirs + DiagonalDirs
    KnightDirs = [ [1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1] ]

    cursor = [8, 8]
    turn = "White"

    availables = []
    need_to_redraw = []