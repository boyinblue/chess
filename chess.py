# Define Classes For Chess

class Position:
    def __init__(self, posName):
        self.set(posName)

    def set(self, posName):
        self.posName = posName

    def get(self):
        return self.posName
    
    def getDeltaPos(self, dX, dY):
        newPosName = self.getDeltaPosName(dX, dY)
        if newPosName != "":
            return Position(newPosName)
        return None

    def getDeltaPosName(self, dX, dY):
        #print(f"GetDeltaPosName {self.posName} {dX} {dY}")
        x = self.Col2Id[self.posName[1]] + dX
        y = self.Row2Id[self.posName[0]] - dY
        if x >= 0 and x < 8 and y >= 0 and y < 8:
            return f"{self.Id2Row[y]}{self.Id2Col[x]}"
        #print(f"Invalid Delta Pos {x} {y}")
        return ""
    
    def isPos(self, posName):
        if self.posName == posName:
            return True
        return False
    
    def getAllPosNames(self):
        return self.allPosNames
    
    def changePosByDelta(self, dX, dY):
        newPos = self.getDeltaPosName(dX, dY)
        if newPos != "":
            self.posName = newPos
        return newPos

    posName = ""
    allPosNames = [
        "1A", "1B", "1C", "1D", "1E", "1F", "1G", "1H",
        "2A", "2B", "2C", "2D", "2E", "2F", "2G", "2H",
        "3A", "3B", "3C", "3D", "3E", "3F", "3G", "3H",
        "4A", "4B", "4C", "4D", "4E", "4F", "4G", "4H",
        "5A", "5B", "5C", "5D", "5E", "5F", "5G", "5H",
        "6A", "6B", "6C", "6D", "6E", "6F", "6G", "6H",
        "7A", "7B", "7C", "7D", "7E", "7F", "7G", "7H",
        "8A", "8B", "8C", "8D", "8E", "8F", "8G", "8H",
    ]
    Id2Col = [ 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H' ]
    Id2Row = [ '8', '7', '6', '5', '4', '3', '2', '1' ]
    Col2Id = {
        "A" : 0,
        "B" : 1,
        "C" : 2,
        "D" : 3,
        "E" : 4,
        "F" : 5,
        "G" : 6,
        "H" : 7
    }
    Row2Id = {
        "8" : 0,
        "7" : 1,
        "6" : 2,
        "5" : 3,
        "4" : 4,
        "3" : 5,
        "2" : 6,
        "1" : 7
    }

class Cursor(Position):
    def reset(self):
        print(f"Cursor reset")
        self.set("1A")

class Selector(Position):
    def reset(self):
        self.posName = ""

    def cancel(self):
        #print("Cancel selector")
        self.reset()
        #self.print()

    def isValid(self):
        if self.posName in self.allPosNames:
            return True
        return False
    
    def print(self):
        print(f"Selector : {posName}")

# Available Class
class Available:
    def __init__(self):
        self.avail.clear()

    def get(self):
        return self.avail
    
    def add(self, posName):
        #print(f"Add Avail {posName}")
        self.avail.add(posName)

    def isAvaiable(self, posName):
        for pos in self.avail:
            if pos == posName:
                return True
        return False

    def clear(self):
        self.avail.clear()

    avail = set()

# Chess Object Class
class Object:
    def __init__(self, name, color, posName, move_cnt = 0):
        self.name = name
        self.color = color
        self.move_cnt = move_cnt
        self.score = self.getScore()
        self.pos = Position(posName)
        self.originPosName = posName

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
    pos = None
    originPosName = ""
    move_cnt = 0
    score = 0
    avails = None

    RightAngleDirs = [ [0, 1], [0, -1], [1, 0], [-1, 0] ]
    DiagonalDirs = [ [1, 1], [1, -1], [-1, 1], [-1, -1] ]
    EveryDirs = RightAngleDirs + DiagonalDirs
    KnightDirs = [ [1, 2], [1, -2], [-1, 2], [-1, -2], [2, 1], [2, -1], [-2, 1], [-2, -1] ]

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
        #print(f"New Turn : {self.turn} {self} By Rollback")

    def nextTurn(self):
        self.turn = self.getNextTurnName()
        #print(f"New Turn : {self.turn} {self}")

    def setAI(self, color, user):
        if color == "White":
            self.white = user
        elif color == "Black":
            self.black = user

    comm_type = ""
    color = ""
    turn = ""
    winner = ""
    gameover = False

# Movement Class
class Movement:
    def __init__(self, posName, obj, newPosName, newObj, subSeq = 0):
        self.posName = posName
        self.obj = obj
        self.newPosName = newPosName
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
        print(f"Movement : {self.posName} {objName} {self.newPosName} {newObjName} (Sub Seq : {self.subSeq}) (score : {self.score})")

    posName = ""
    obj = None
    newPosName = ""
    newObj = None
    subSeq = 0
    score = 0

# Movement History Class
class History:
    def reset(self):
        self.arrHistory.clear()
        self.arrKilled.clear()

    def append(self, posName, obj, newPosName, newObj, subSeq = 0):
        moveInfo = Movement(posName, obj, newPosName, newObj, subSeq)
        #print(f"Move Info")
        #moveInfo.print()
        self.arrHistory.append(moveInfo)

        if posName != newPosName and newObj != None:
            self.arrKilled.append(newObj)

    def rollback(self):
        #print(f"History Rollback")
        if len(self.arrHistory) == 0:
            return None

        last = self.arrHistory.pop()
        if last.posName != last.newPosName and last.newObj != None:
            self.arrKilled.pop()
        #last.print()

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
        self.turn = Turn()
        self.turn.color = color
        print(f"Set {color} color")

        self.history = History()
        self.cursor = Cursor("1A")
        self.array = {}
        self.reset(self)

    def reset(self, bug = False):
        self.turn.reset()
        self.history.reset()
        self.cursor.reset()

        posNames = self.cursor.getAllPosNames()
        for posName in posNames:
            if posName in self.array_org:
                objName = self.array_org[posName]
                self.array[posName] = Object(objName[5:], objName[0:5], posName)
                self.array[posName].pos.set(posName)
            else:
                self.array[posName] = None
            #print(f"Generate Object posName : {objName}")

    # Dump
    def print(self):
        print(f"Dump Chess {self}")
        for posName in self.cursor.getAllPosNames():
            if self.array[posName] == None:
                print(f"{posName} : Empty")
            else:
                print(f"{posName} : {self.array[posName].getName()} {self.array[posName]} {self.array[posName].originPosName}")
        print(f"Dump Chess - Completed")

    # Basic I/O functions
    def getObject(self, posName):
        if posName in self.array:
            return self.array[posName]
        return None
    
    def getObjectName(self, posName):
        obj = self.getObject(self, posName)
        if obj == None:
            return ""
        return obj.name
    
    def getObjectFullName(self, posName):
        obj = self.getObject(self, posName)
        if obj == None:
            return "Empty"
        return obj.getFullName()
    
    def getObjectColor(self, posName):
        obj = self.getObject(self, posName)
        if obj == None:
            return ""
        return obj.color
    
    def isValidPos(self, posName):
        pos = Position(posName)
        #print(f"Check Valid Pos {posName}")
        if posName in pos.getAllPosNames():
            return True
        return False

    def isEmpty(self, posName):
        if self.array[posName] == None:
            return True
        return False
    
    def isEnermy(self, posName):
        if self.isValidPos(posName) and self.array[posName] != None and self.array[posName].color == self.turn.getNextTurnName():
            return True
        return False
    
    def isAlly(self, posName):
        #print(self.turn)
        #print(f"Check Ally {posName} Turn : {self.turn.getThisTurnName()}")
        if self.isValidPos(posName) and self.array[posName] != None and self.array[posName].color == self.turn.getThisTurnName():
            return True
        return False
    
    def getAvails(self):
        if not self.selector.isValid():
            return None
        obj = self.getObject(self.selector.posName)
        if obj == None:
            return None
        return obj.avails
    
    # Check Movement functions
    def checkUnitAvailable(self, obj, newPos):
        if not self.isValidPos(newPos):
            return False
        elif self.isAlly(newPos):
            return False
        
        obj.avails.add(newPos)
        if self.isEnermy(newPos):
            return False
        return True #Continue Checking
        
    def checkAvailableByDirList(self, obj, dirs, count):
        #print(f"Check Availables {obj.name} {obj.pos.get()}")
        for dir in dirs:
            for i in range(0, count):
                newPosName = obj.pos.getDeltaPosName(dir[0] * (i+1), dir[1] * (i+1))
                if False == self.checkUnitAvailable(obj, newPosName):
                    break

    def checkCastling(self, obj):
        if obj.move_cnt != 0:
            return False
        
        posName = obj.pos.get()
        if posName[0] != "1" and posName[0] != "8":
            return False
        elif posName[1] != "E":
            return False
        
        if posName == "1E":
            if self.array["1F"] == None and self.array["1G"] == None and self.array["1H"] != None and self.array["1H"].move_cnt == 0:
                obj.avails.add("1G")
            if self.array["1D"] == None and self.array["1C"] == None and self.array["1B"] == None and self.array["1A"] != None and self.array["1A"].move_cnt == 0:
                obj.avails.add("1C")
        elif posName == "8E":
            if self.array["8F"] == None and self.array["8G"] == None and self.array["8H"] != None and self.array["8H"].move_cnt == 0:
                obj.avails.add("8G")
            if self.array["1D"] == None and self.array["1C"] == None and self.array["1B"] == None and self.array["1A"] != None and self.array["1A"].move_cnt == 0:
                obj.avails.add("8C")

    def checkAvailable_Pawn(self, obj):
        y_offset = -1
        y_org_pos = "7"
        if( obj.color == "White" ):
            y_offset = 1
            y_org_pos = "2"

        newPosName = obj.pos.getDeltaPosName(0, y_offset)
        #print(f"New PosName {newPosName}")
        if self.isEmpty(newPosName):
            obj.avails.add(newPosName)

            newPosName = obj.pos.getDeltaPosName(0, y_offset * 2)
            #print(f"New PosName {newPosName}")
            if obj.pos.get()[0] == y_org_pos and self.isEmpty(newPosName):
                obj.avails.add(newPosName)

        newPosName = obj.pos.getDeltaPosName(1, y_offset)
        #print(f"New PosName {newPosName}")
        if self.isEnermy(newPosName):
            obj.avails.add(newPosName)

        newPosName = obj.pos.getDeltaPosName(-1, y_offset)
        #print(f"New PosName {newPosName}")
        if self.isEnermy(newPosName):
            obj.avails.add(newPosName)

    def checkAvailable(self, posName):
        obj = self.array[posName]
        objName = obj.name
        if obj.avails == None:
            obj.avails = Available()
        else:
            obj.avails.clear()

        #print(self.turn)
        #print(f"Check available {posName}, objName={objName}, objColor={obj.color}, turn={self.turn.getThisTurnName()}")

        if objName == "King":
            self.checkAvailableByDirList(obj, obj.EveryDirs, 1)
            self.checkCastling(obj)
        elif objName == "Queen":
            self.checkAvailableByDirList(obj, obj.EveryDirs, 7)
        elif objName == "Bishop":
            self.checkAvailableByDirList(obj, obj.DiagonalDirs, 7)
        elif objName == "Rook":
            self.checkAvailableByDirList(obj, obj.RightAngleDirs, 7)
        elif objName == "Knight":
            self.checkAvailableByDirList(obj, obj.KnightDirs, 1)
        elif objName == "Pawn":
            self.checkAvailable_Pawn(obj)

    # Mouse Event
    def selectObject(self, posName):
        obj = self.getObject(posName)
        turn = self.turn.getThisTurnName()
        if obj != None and obj.color == turn:
            self.selector.set(posName)
            self.checkAvailable(posName)
        else:
            print(f"Not Turn : turn={turn}")

    def cancelselected(self):
        self.selector.cancel()
        print(f"Availables Clear")

    def clicked(self, posName):
        if self.turn.gameover == True:
            return

        print(f"")
        print(f"Clicked {posName}")

        self.cursor.set(posName)

        if posName in self.array and self.turn.checkThisTurnObj(self.array[posName]):
            # Cancel previsou selected
            if self.selector.isPos(posName):
                self.cancelselected()
            else:
                self.cancelselected()
                self.selectObject(posName)
            return

        # Move selected
        avails = self.getAvails()
        if avails != None:
            for pt in avails.get():
                if pt == posName:
                    self.moveTo(self.selector.posName, posName)

        # Cancel selected
        self.cancelselected()

    # Actual Movement Functions
    def movement(self, posName, newPosName, subSeq = 0):
        if self.array[posName] == None:
            print(f"Invalid {posName}")
        objName = self.array[posName].getName()
        newObj = self.array[newPosName]
        if newObj != None:
            newObjName = newObj.getName()
        else:
            newObjName = "Empty"

        #print(f"====> Move [{posName}] {objName} => [{newPosName}] {newObjName}")

        # Move Count
        self.array[posName].move_cnt += 1

        # Write History
        if newPosName in self.array:
            objNew = self.array[newPosName]
        else:
            objNew = None
        self.history.append(posName, self.array[posName], newPosName, objNew, subSeq)

        # Check Game Over
        obj = self.array[newPosName]
        if obj is not None and obj.name == "King":
            self.turn.gameover = True
            self.turn.winner = self.turn.getThisTurnName()

        # Make movement
        self.array[newPosName] = self.array[posName]
        self.array[newPosName].pos.set(newPosName)
        self.array[posName] = None

    def pawnUpgrade(self, posName):
        print(f"Pawn Upgrade({posName})")

        # Write History
        self.history.append(posName, self.array[posName], posName, self.array[posName], 2)

        # Change pawn to queen
        self.array[posName].name = "Queen"

    def moveTo(self, posName, newPosName):
        # Castling
        obj = self.array[posName]
        if obj is not None and obj.name == "King" and posName[1] == "E" and newPosName[1] == "G":
            # Kingside castling
            self.movement(posName, newPosName)
            posNameRook = Position(posName).getDeltaPosName(3, 0)
            posNameNewRook = Position(posName).getDeltaPosName(1, 0)
            self.movement(posNameRook, posNameNewRook, 2)
        elif obj is not None and obj.name == "King" and posName[1] == "E" and newPosName[1] == "C":
            # Queenside castling
            self.movement(posName, newPosName)
            posNameRook = Position(posName).getDeltaPosName(-4, 0)
            posNameNewRook = Position(posName).getDeltaPosName(-2, 0)
            self.movement(posNameRook, posNameNewRook, 2)
        else:
            # Make Movement
            self.movement(posName, newPosName)

            # Check Pawn Upgrade
            obj = self.array[newPosName]
            if obj is not None and obj.name == "Pawn" and obj.color == "White" and newPosName[0] == "8":
                self.pawnUpgrade(newPosName)
            elif obj is not None and obj.name == "Pawn" and obj.color == "Black" and newPosName[0] == "1":
                self.pawnUpgrade(newPosName)

        # Next Turn
        if self.turn.gameover != True:
            self.turn.nextTurn()

    def rollback(self):
        mov = self.history.rollback()
        if mov == None:
            print(f"Nothing in history")
            return False

        # Rollback for pawn upgrade
        if mov.posName == mov.newPosName:
            self.array[mov.newPosName].name = "Pawn"
            print(f"Pawn Upgrade Rollback")
            return True
        elif mov.newObj == None:
            #print(f"Set {mov.newPosName} : Empty")
            self.array[mov.newPosName] = None
            newObjName = "Empty"
        else:
            #print(f"Set {mov.newPosName} : {mov.newObj.getFullName()}")
            self.array[mov.newPosName] = mov.newObj
            mov.newObj.pos.set(mov.newPosName)
            newObjName = mov.newObj.name

        #print(f"<==== Rollback [{mov.posName}] {mov.obj.getFullName()} <= [{mov.newPosName}] {newObjName}")
        self.array[mov.posName] = mov.obj
        self.array[mov.posName].move_cnt -= 1
        self.array[mov.posName].pos.set(mov.posName)

        self.turn.setTurnName(mov.obj.getColor())
        self.turn.gameover = False

        if mov.subSeq == 2:
            return True
        
    array_org2 = {
        "4A" : 'BlackPawn',
        "6C" : 'BlackPawn',
        "3H" : 'WhitePawn',
        "3B" : 'WhitePawn',
    }

    array_org = {
        "8A" : 'BlackRook',
        "8B" : 'BlackKnight',
        "8C" : 'BlackBishop',
        "8D" : 'BlackQueen',
        "8E" : 'BlackKing',
        "8F" : 'BlackBishop',
        "8G" : 'BlackKnight',
        "8H" : 'BlackRook',
        "7A" : 'BlackPawn',
        "7B" : 'BlackPawn',
        "7C" : 'BlackPawn',
        "7D" : 'BlackPawn',
        "7E" : 'BlackPawn',
        "7F" : 'BlackPawn',
        "7G" : 'BlackPawn',
        "7H" : 'BlackPawn',
        "2A" : 'WhitePawn',
        "2B" : 'WhitePawn',
        "2C" : 'WhitePawn',
        "2D" : 'WhitePawn',
        "2E" : 'WhitePawn',
        "2F" : 'WhitePawn',
        "2G" : 'WhitePawn',
        "2H" : 'WhitePawn',
        "1A" : 'WhiteRook',
        "1B" : 'WhiteKnight',
        "1C" : 'WhiteBishop',
        "1D" : 'WhiteQueen',
        "1E" : 'WhiteKing',
        "1F" : 'WhiteBishop',
        "1G" : 'WhiteKnight',
        "1H" : 'WhiteRook'
    }

    array = None
    cursor = None
    selector = Selector("")
    turn = None
    history = None

class ChessUser:
    def __init__(self, color, chess):
        self.color = color
        self.chess = chess

    color = ""
    chess = None

#class ChessHuman(ChessUser):

class ChessAI(ChessUser):
    def copyBoard(self, newBoard):
        for posName in self.chess.cursor.getAllPosNames():
            obj = self.chess.getObject(posName)
            if obj == None:
                newBoard.array[posName] = None
                continue
            newBoard.array[posName] = Object(obj.name, obj.color, posName, obj.move_cnt)
            #print(f"New Board {posName} {obj.name}")

        print(f"Set Turn Color : {self.chess.turn.turn} from {self.chess.turn}")
        newBoard.turn.color = self.chess.turn.color
        newBoard.turn.turn = self.chess.turn.turn

    def getSelectable(self, chess):
        #print(f"Get Selectable For {chess.turn.turn}")
        selectable = []
        posNames = chess.cursor.getAllPosNames()
        for posName in posNames:
            obj = chess.array[posName]
            if obj == None:
                continue
            elif obj.color == chess.turn.turn:
                selectable.append(posName)

        return selectable
    
    def getMoveable(self, chess, selectable):
        moveables = []
        #print(f"selectables {selectable}")
        for posName in selectable:
            #print(f"Sel {select}")
            chess.checkAvailable(posName)
            obj = chess.getObject(posName)
            if obj == None:
                continue
            for newPosName in obj.avails.get():
                newObj = chess.getObject(newPosName)
                move = Movement(posName, obj, newPosName, newObj)
                moveables.append(move)

        return moveables

    def getBestMove_Recursive(self, chess, moveArr, cnt):
        if cnt == 0:
            #print(f"Calc {self.calc_cnt} (score : {score})")
            self.arrResult.append(moveArr)
            return
        #print(f"Get Best Move For {color} : Level-{cnt}")

        # Get Selectable
        selectables = self.getSelectable(chess)

        # Get Moveable
        moveables = self.getMoveable(chess, selectables)

        for mov in moveables:
            import copy
            newMove = copy.deepcopy(moveArr)

            newMove.append(mov)
            chess.moveTo(mov.posName, mov.newPosName)
            self.getBestMove_Recursive(chess, newMove, cnt - 1)
            if chess.rollback():
                chess.rollback()

    def getBestMove(self):
        import chess_view

        # Generate New Chess For Calculating
        turn = self.chess.turn.turn
        chess = Chess(turn)
        chess_view = chess_view.ChessView(chess, True, "Chess AI")
        self.copyBoard(chess)

        self.arrResult.clear()

        print(f"Check Move Score")
        self.getBestMove_Recursive(chess, [], 2)

        chess_view.draw()

        max_score = 0
        max_move = None
        weight = 1
        for result in self.arrResult:
            score = 0
            for move in result:
                if move.newObj != None:
                    if move.newObj.color == turn:
                        score -= ( move.newObj.score * weight )
                    else:
                        score += ( move.newObj.score * weight )
                import random

                score += (random.randint(1,10) / 20)
                #weight /= 2
            
            if score >= max_score:
                print(f"Update max score : {score}")
                max_score = score
                max_move = result

        print(f"Best Move (score : {max_score}), {len(self.arrResult)} cases")
        for mov in max_move:
            mov.print()

        return max_move[0]
    
    arrResult = []