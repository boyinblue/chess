import cv2

# Chess Object Class
class Object:
    def __init__(self, name, color):
        self.name = name
        self.color = color
        self.move_cnt = 0
        self.score = self.getScore()

    def getFullName(self):
        return f"{self.color}{self.name}"
    
    def getName(self):
        return self.name
    
    def getColor(self):
        return self.color
    
    def getScore(self):
        if self.name == "King":
            return 10
        elif self.name == "Queen":
            return 9
        elif self.name == "Rook":
            return 5
        elif self.name == "Knight" or self.name == "Bishop":
            return 3
        elif self.name == "Pawn":
            return 1
        else:
            assert()
            
    name = ""
    color = ""
    move_cnt = 0
    score = 0

    RightAngleDirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    DiagonalDirs = [ [1, 1], [1, -1], [-1, 1], [-1, -1] ]
    EveryDirs = RightAngleDirs + DiagonalDirs
    KnightDirs = [ [1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1] ]

class Position:
    def set(self, x, y):
        self.x = x
        self.y = y

    def get(self):
        return self.x, self.y
    
    def isPos(self, x, y):
        if self.x == x and self.y == y:
            return True
        return False

class Cursor(Position):
    def reset(self):
        self.x = 0
        self.y = 0

    def left(self):
        self.x = (self.x + 7) % 8

    def right(self):
        self.x = (self.x + 1) % 8
    
    def up(self):
        self.y = (self.y + 7) % 8

    def down(self):
        self.y = (self.y + 1) % 8

    x = 4
    y = 7

class Selector(Position):
    def reset(self):
        self.x = 8
        self.y = 8

    def cancel(self):
        #print("Cancel selector")
        self.reset()
        #self.print()

    def isValid(self):
        if self.x < 8 and self.y < 8:
            return True
        return False
    
    def print(self):
        print(f"Selector : {self.x}, {self.y}")

    x = 8
    y = 8

# Turn Class
class Turn:
    def __init__(self):
        self.turn = "White"
        self.winner = ""
        self.gameover = False

    def reset(self):
        self.__init__()

    def getThisTurnName(self):
        return self.turn
    
    def getNextTurnName(self):
        if self.turn == "White":
            return "Black"
        return "White"
    
    def checkThisTurnObj(self, obj):
        if obj == None:
            return False
        elif obj.color == self.turn:
            return True
        return False
    
    def setTurnName(self, turnName):
        self.turn = turnName

    def nextTurn(self):
        self.turn = self.getNextTurnName()

    def setAI(self, color, user):
        if color == "White":
            self.white = user
        elif color == "Black":
            self.black = user

    color = ""
    turn = ""
    winner = ""
    gameover = False

# Available Class
class Available:
    def __init__(self):
        self.avail.clear()

    def get(self):
        return self.avail
    
    def add(self, posName):
        self.avail.add(posName)

    def isAvaiable(self, posName):
        for pos in self.avail:
            if pos == posName:
                return True
        return False

    def clear(self):
        self.avail.clear()

    avail = set()

# Movement Class
class Movement:
    def __init__(self, x, y, obj, newX, newY, newObj, subSeq = 0):
        self.x = x
        self.y = y
        self.obj = obj
        self.newX = newX
        self.newY = newY
        self.newObj = newObj
        self.subSeq = subSeq
        if self.newObj == None:
            return
        self.score = self.newObj.getScore()

    def print(self):
        objName = self.obj.getFullName()
        newObjName = "Empty"
        if self.newObj != None:
            newObjName = self.newObj.getFullName()
        print(f"Movement : {self.x} {self.y} {objName} {self.newX} {self.newY} {newObjName} (Sub Seq : {self.subSeq}) (score : {self.score})")

    x = 0
    y = 0
    obj = None
    newX = 0
    newY = 0
    newObj = None
    subSeq = 0
    score = 0

# Movement History Class
class History:
    def reset(self):
        self.arrHistory.clear()
        self.arrKilled.clear()

    def append(self, x, y, obj, newX, newY, newObj, subSeq = 0):
        moveInfo = Movement(x, y, obj, newX, newY, newObj, subSeq)
        print(f"Move Info : {moveInfo.print()}")
        self.arrHistory.append(moveInfo)

        if x != newX and y != newY and newObj != None:
            self.arrKilled.append(newObj)

    def rollback(self):
        if len(self.arrHistory) == 0:
            return None

        last = self.arrHistory.pop()
        if last.x != last.newX and last.y != last.newY and last.newObj != None:
            self.arrKilled.pop()
        last.print()

        return last
    
    def print(self):
        print(f"Dump History")
        for mov in self.arrHistory:
            mov.print()

    arrHistory = []
    arrKilled = []

# Check Class
class Chess:
    def __init__(self, color):
        self.reset(self)
        self.turn.color = color
        print(f"Set {color} color")

    def reset(self, bug = False):
        for x in range(8):
            for y in range(8):
                obj_name = self.array_org[y][x]
                print(f"Generate Object x={x}, y={y}, {obj_name}")
                if obj_name != "Empty":
                    self.array[y][x] = Object(obj_name[5:], obj_name[0:5])
                elif bug == False:
                    self.array[y][x] = None
        
        self.turn.reset()
        self.availables.clear()
        self.history.reset()
        self.cursor.reset()

    # Dump
    def print(self):
        print(f"Dump Chess")
        for y in range(8):
            print(f"")
            for x in range(8):
                if self.array[y][x] == None:
                    print(f"Empty ", end="")
                else:
                    print(f"{self.array[y][x].getName()} ", end="")
        print(f"Dump Chess - Completed")

    # Basic I/O functions
    def getObject(self, x, y):
        if not Chess.isValidPos(self, x, y):
            return None
        return self.array[y][x]
    
    def getObjectName(self, x, y):
        obj = Chess.getObject(self, x, y)
        if obj == None:
            return ""
        return obj.name
    
    def getObjectFullName(self, x, y):
        obj = Chess.getObject(self, x, y)
        if obj == None:
            return "Empty"
        return obj.getFullName()
    
    def getObjectColor(self, x, y):
        obj = Chess.getObject(self, x, y)
        if obj == None:
            return ""
        return obj.color
    
    def isValidPos(self, x, y):
        if x < 0 or x >= 8 or y < 0 or y >= 8:
            return False
        return True
    
    def isEmpty(self, x, y):
        if Chess.isValidPos(self, x, y) and self.array[y][x] == None:
            return True
        return False
    
    def isEnermy(self, x, y):
        if Chess.isValidPos(self, x, y) and self.array[y][x] != None and self.array[y][x].color == self.turn.getNextTurnName():
            return True
        return False
    
    def isAlly(self, x, y):
        if Chess.isValidPos(self, x, y) and self.array[y][x] != None and self.array[y][x].color == self.turn.getThisTurnName():
            return True
        return False
    
    # Basic I/O functions
    def getPosName(self, x, y):
        ColName = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
        posName = f"{y}{ColName[x]}"
        return posName
    
    def getXY(self, posName):
        y = ord(posName[0])-ord('0')
        x = ord(posName[1])-ord('A')
        return x, y
    
    # Check Movement functions
    def addAvailable(self, x, y, newX, newY):
        posName = Chess.getPosName(self, newX, newY)
        #print(f"Add Available {posName}")
        self.availables.add(posName)
        mov = Movement(x, y, self.array[y][x], newX, newY, self.array[newY][newX])
        self.moveables.append(mov)

    def checkUnitAvailable(self, x, y, newX, newY):
        if not Chess.isValidPos(self, newX, newY):
            return False
        elif Chess.isAlly(self, newX, newY):
            return False
        
        Chess.addAvailable(self, x, y, newX, newY)
        if Chess.isEnermy(self, newX, newY):
            return False
        return True #Continue Checking
        
    def checkAvailableByDirList(self, x, y, dirs, count):
        for dir in dirs:
            for i in range(0, count):
                if False == Chess.checkUnitAvailable(self, x, y, x + dir[0] * (i+1), y + dir[1] * (i+1)):
                    break

    def checkCastling(self, x, y):
        if self.array[y][x].move_cnt != 0:
            return False
        if self.array[y][x+1] == None and self.array[y][x+2] == None and self.array[y][x+3] != None and self.array[y][x+3].move_cnt == 0:
            self.addAvailable(self, x, y, x + 2, y)
        if self.array[y][x-1] == None and self.array[y][x-2] == None and self.array[y][x-3] == None and self.array[y][x-4] != None and self.array[y][x-4].move_cnt == 0:
            self.addAvailable(self, x, y, x - 2, y)

    def checkAvailable_Pawn(self, x, y):
        y_offset = 1
        y_org_pos = 1
        obj = Chess.getObject(self, x, y)
        if( obj.color == "White" ):
            y_offset = -1
            y_org_pos = 6

        if Chess.isEmpty(self, x, y + y_offset):
            Chess.addAvailable(self, x, y, x, y + y_offset)
            if y == y_org_pos and Chess.isEmpty(self, x, y + y_offset * 2):
                Chess.addAvailable(self, x, y, x, y + y_offset * 2)
        if Chess.isEnermy(self, x + 1, y + y_offset):
            Chess.addAvailable(self, x, y, x + 1, y + y_offset)
        if Chess.isEnermy(self, x - 1, y + y_offset):
            Chess.addAvailable(self, x, y,  x - 1, y + y_offset)

    def checkAvailable(self, x, y):
        obj = self.array[y][x]
        objName = obj.name

        #print(f"Check available x={x}, y={y}, objName={objName}")

        if objName == "King":
            Chess.checkAvailableByDirList(self, x, y, obj.EveryDirs, 1)
            Chess.checkCastling(self, x, y)
        elif objName == "Queen":
            Chess.checkAvailableByDirList(self, x, y, obj.EveryDirs, 7)
        elif objName == "Bishop":
            Chess.checkAvailableByDirList(self, x, y, obj.DiagonalDirs, 7)
        elif objName == "Rook":
            Chess.checkAvailableByDirList(self, x, y, obj.RightAngleDirs, 7)
        elif objName == "Knight":
            Chess.checkAvailableByDirList(self, x, y, obj.KnightDirs, 1)
        elif objName == "Pawn":
            Chess.checkAvailable_Pawn(self, x, y)

    # Mouse Event
    def selectObject(self, x, y):
        obj = Chess.getObject(self, x, y)
        turn = self.turn.getThisTurnName()
        if obj != None and obj.color == turn:
            self.selector.set(x, y)
            Chess.checkAvailable(self, x, y)
        else:
            print(f"Not Turn : turn={turn}")

    def cancelselected(self):
        self.selector.cancel()
        self.availables.clear()

    def clicked(self, x, y):
        if self.turn.gameover == True:
            return

        print(f"")
        print(f"Clicked x={x}, y={y}")

        # Check This Turn Object
        if x >= 8 or y >= 8:
            return

        self.cursor.set(x,y)
        if self.array[y][x] != None and self.turn.checkThisTurnObj(self.array[y][x]):
            # Cancel previsou selected
            if self.selector.isPos(x, y):
                self.cancelselected()
            else:
                self.cancelselected()
                self.selectObject(x, y)
            return

        # Move selected
        for pt in self.availables.get():
            posX, posY = self.getXY(pt)
            if posX == x and posY == y:
                self.moveTo(self.selector.x, self.selector.y, posX, posY)
                break

        # Cancel selected
        self.cancelselected()

    # Actual Movement Functions
    def swap(self, x, y, x2, y2):
        # Make swap
        tmp = self.array[x][y]
        self.array[x][y] = self.array[x2][y2]
        self.array[x2][y2] = tmp

        self.array[x][y].move_cnt += 1
        self.array[x2][y2].move_cnt += 1

    def movement(self, x, y, newX, newY, subSeq = 0):
        print(f"Move({x}, {y} => {newX}, {newY})")

        # Move Count
        self.array[y][x].move_cnt += 1

        # Write History
        self.history.append(x, y, self.array[y][x], newX, newY, self.array[newY][newX], subSeq)

        # Check Game Over
        obj = self.array[newY][newX]
        if obj is not None and obj.name == "King":
            self.turn.gameover = True
            self.turn.winner = self.turn.getThisTurnName()

        # Make movement
        self.array[newY][newX] = self.array[y][x]
        self.array[y][x] = None

    def pawnUpgrade(self, x, y):
        print(f"Pawn Upgrade({x}, {y}")

        # Write History
        self.history.append(x, y, self.array[y][x], x, y, self.array[x][y], 2)

        # Change pawn to queen
        self.array[y][x].name = "Queen"

    def moveTo(self, x, y, newX, newY):
        # Castling
        obj = self.array[y][x]
        if obj is not None and obj.name == "King" and newX - x == 2:
            # Kingside castling
            Chess.movement(self, x, y, x + 2, y, 1)
            Chess.movement(self, x + 3, y, x + 1, y, 2)
        elif obj is not None and obj.name == "King" and  x - newX == 2:
            # Queenside castling
            Chess.movement(self, x, y, x - 2, y, 1)
            Chess.movement(self, x - 4, y, x - 1, y, 2)
        else:
            # Make Movement
            Chess.movement(self, x, y, newX, newY)

            # Check Pawn Upgrade
            obj = self.array[newY][newX]
            if obj is not None and obj.name == "Pawn" and obj.color == "White" and newY == 0:
                Chess.pawnUpgrade(self, newX, newY)
            elif obj is not None and obj.name == "Pawn" and obj.color == "Black" and newY == 7:
                Chess.pawnUpgrade(self, newX, newY)

        # Next Turn
        if self.turn.gameover != True:
            self.turn.nextTurn()

    def rollback(self):
        mov = self.history.rollback()
        if mov == None:
            print(f"Nothing in history")
            return False

        # Rollback for pawn upgrade
        if mov.x == mov.newX and mov.y == mov.newY:
            self.array[mov.newY][mov.newX].name = "Pawn"
            print(f"Pawn Upgrade Rollback")
            return True
        elif mov.newObj == None:
            print(f"Set {mov.newX}, {mov.newY} : Empty")
            self.array[mov.newY][mov.newX] = None
        else:
            print(f"Set {mov.newX}, {mov.newY} : {mov.newObj.getFullName()}")
            self.array[mov.newY][mov.newX] = mov.newObj

        print(f"Set {mov.x}, {mov.y} : {mov.obj.getFullName()}")
        self.array[mov.y][mov.x] = mov.obj
        self.array[mov.y][mov.x].move_cnt -= 1

        self.turn.setTurnName(mov.obj.getColor())
        self.turn.gameover = False

        if mov.subSeq == 2:
            return True

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

    turn = Turn()

    availables = Available()
    moveables = []

    history = History()

    cursor = Cursor()
    selector = Selector()

class ChessUser:
    def __init__(self, color, chess):
        self.color = color
        self.chess = chess

    color = ""
    chess = None

#class ChessHuman(ChessUser):

class ChessAI(ChessUser):
    def getSelectable(self):
        selectable = []
        for x in range(8):
            for y in range(8):
                posName = Chess.getPosName(Chess, x, y)
                obj = self.board.array[y][x]
                if obj == None:
                    continue
                elif obj.color == self.board.turn.getThisTurnName():
                    selectable.append(posName)

        return selectable
    
    def getMoveable(self, selectable):
        print(f"selectables {selectable}")
        for select in selectable:
            #print(f"Sel {select}")
            x, y = Chess.getXY(select)
            Chess.checkAvailable(self.chess, x, y)

        return self.board.moveables

    def getRandomMove(self):
        print(f"Random Move")
        self.board.moveables.clear()
        selectable = ChessAI.getSelectable(self)
        moveables = ChessAI.getMoveable(self, selectable)
        for mov in self.board.moveables:
            mov.print()

        import random
        randMov = random.choice(self.chess.moveables)

        return randMov

    def getBestMove_Recursive(self, cnt):
        print(f"Do Best Move : Level-{cnt}")
        if cnt == 0:
            return None
        max_score = 0
        max_move = None

        moveables_old = self.board.moveables
        self.board.moveables.clear()

        selectable = ChessAI.getSelectable(self)
        moveables = ChessAI.getMoveable(self, selectable)
        for mov in moveables:
            if mov.score > max_score:
                print(f"Set Max Score")
                mov.print()
                max_score = mov.score
                max_move = mov
            Chess.moveTo(self.chess, mov.x, mov.y, mov.newX, mov.newY)
            self.chess.history.print()
            mov = ChessAI.getBestMove_Recursive(self, cnt - 1)
            Chess.rollback(self.board)
            self.chess.history.print()

        self.board.moveables = moveables_old

        return max_move

    def getBestMove(self):
        print(f"Do Best Move")
        import copy
        self.board = copy.deepcopy(self.chess)
        max_move = ChessAI.getBestMove_Recursive(self, 1)

        if max_move == None:
            max_move = ChessAI.getRandomMove(self)
        else:
            max_move.print()

        return max_move