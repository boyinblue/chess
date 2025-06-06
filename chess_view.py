import cv2
from chess import Chess, Position

class ChessView:
    def __init__(self, chess, invert, viewName):
        self.scale = 1.5
        self.chess = chess
        self.invert = invert
        self.viewName = viewName

    def loadObjImages(self):
        for obj in self.objs:
            img = cv2.imread(f"img/{obj}.png")
            self.objImages[obj] = cv2.resize(img, (int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)))
            self.objImages_small[obj] = cv2.resize(img, (int(img.shape[0] * self.scale / 2), int(img.shape[1] * self.scale / 2)))
            self.obj_width = self.objImages[obj].shape[1]
            self.obj_height = self.objImages[obj].shape[0]

        #print(f"Object Size : {obj_width} x {obj_height}")

    def getObjectCoordinate(self, x, y, width):
        ptX = ( x + 1 ) * self.obj_width + width
        ptY = ( y + 1 ) * self.obj_height + width
        ptX2 = ( x + 2 ) * self.obj_width - width
        ptY2 = ( y + 2 ) * self.obj_height - width
        return ptX, ptY, ptX2, ptY2
    
    # Basic I/O functions
    def getPosName(self, x, y, invert=False):
        if invert == True:
            posName = f"{y+1}{Position.Id2Col[7-x]}"
        else:
            posName = f"{8-y}{Position.Id2Col[x]}"

        return posName
    
    def getXY(self, posName, invert = False):
        if invert == True:
            y = ord(posName[0]) - ord('1')
            x = 7 - ord(posName[1]) + ord('A')
        else:
            y = 7 - ord(posName[0]) + ord('1')
            x = ord(posName[1])-ord('A')
        return x, y
    
    def drawPosName(self):
        for i in range(8):
            if self.invert == True:
                Idx = 7 - i
            else:
                Idx = i

            textPos = [ int(self.obj_width / 2), int( ( i + 1 ) * self.obj_height + self.obj_height / 2) ]
            cv2.putText(self.image, f"{Position.Id2Row[Idx]}", textPos, 1, 1, (0, 0, 0), 2)
            textPos = [ int( ( i + 1 ) * self.obj_width + self.obj_width / 2), int(self.obj_height/2) ]
            cv2.putText(self.image, f"{Position.Id2Col[Idx]}", textPos, 1, 1, (0, 0, 0), 2)

    def draw_border(self, x, y, color, width):
        ptX, ptY, ptX2, ptY2 = self.getObjectCoordinate(x, y, width)
        cv2.rectangle(self.image, (ptX, ptY), (ptX2, ptY2), color, width)

    def draw_object(self, posName):
        if self.chess.array[posName] == None:
            obj = None
            objName = "Empty"
        else:
            obj = self.chess.array[posName]
            if obj.pos.get() != posName:
                print(f"Pos Name Invalid!!! {posName} != {obj.pos.get()}")
            objName = obj.getFullName()

        #print(f"{self.image.shape}")

        # Draw Object
        x, y = self.getXY(posName, self.invert)
        ptX, ptY, ptX2, ptY2 = self.getObjectCoordinate(x, y, 0)
        #print(f"Draw {posName} {x} {y} : {ptX} {ptY} {ptX2} {ptY2}")
        self.image[ptY:ptY2, ptX:ptX2] = self.objImages[objName]

        # Draw Border
        posName = self.getPosName(x, y, self.invert)
        self.posCoordinator.append([ptX, ptY, ptX2, ptY2, posName])

        # Selected
        avails = self.chess.getAvails()
        if avails != None:
            if avails.isAvaiable(posName):
                self.draw_border(x, y, (0, 255, 0), 6)
            # Draw Selector As Thick Black
            elif self.chess.selector.posName == posName:
                self.draw_border(x, y, (0, 0, 0), 6)
        
        if posName != self.chess.cursor.posName:
            self.draw_border(x, y, (0, 0, 0), 1)
        elif avails != None and avails.isAvaiable(posName):
            self.draw_border(x, y, (255, 0, 0), 3)
        elif obj != None and obj.getColor() == self.chess.turn.getThisTurnName():
            self.draw_border(x, y, (255, 0, 0), 3)
        else:
            self.draw_border(x, y, (0, 0, 255), 3)

    def drawKilledObject(self, x, y, objName):
        #print(f"Draw Killed Obj x={x}, y={y}")

        # Draw Object
        pX = int(500 * self.scale + x * self.obj_width / 2 + 1)
        pY = int(50 * self.scale + y * self.obj_height / 2 + 1)
        self.image[pY:int(pY + self.obj_height / 2), pX:int(pX + self.obj_width / 2)] = self.objImages_small[objName]

    def draw_selected(self):
        # Draw selected
        x, y = self.chess.selector.get()
        if x >= 8 or y >= 8:
            return
        print(f"Draw selected")
        ptX, ptY, ptX2, ptY2 = self.getObjectCoordinate(x, y, 6)
        cv2.rectangle(self.image, (ptX, ptY), (ptX2, ptY2), (0, 0, 0), 6)

    def draw_availables(self):
        for pos in self.chess.availables.get():
            print(f"Draw Availables {pos}")
            x, y = self.chess.getXY(pos, self.invert)
            ptX, ptY, ptX2, ptY2 = self.getObjectCoordinate(x, y, 4)
            cv2.rectangle(self.image, (ptX, ptY), (ptX2, ptY2), (0, 255, 0), 4)

    def delete_info_background(self):
        pt1 = ( int(500 * self.scale), 0 )
        pt2 = ( int(800 * self.scale), int(400 * self.scale) )
        cv2.rectangle(self.image, pt1, pt2, (255,255,255), -1)

    def draw_info(self):
        self.delete_info_background()

        turn = self.chess.turn.getThisTurnName()
        posName = self.chess.cursor.posName
        obj = self.chess.getObject(posName)
        if obj == None:
            objName = "Empty"
        else:
            objName = obj.getFullName()

        cv2.putText(self.image, self.chess.turn.comm_type, [ int(500 * self.scale), 25 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, f"My Color : {self.chess.turn.color}", [ int(500 * self.scale), 50 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, f"Turn : {turn}", [ int(500 * self.scale), 75 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, f"Cursor : {posName}", [ int(500 * self.scale), 100 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, f"Object : {objName}", [ int(500 * self.scale), 120 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, "ESC : Exit", [ int(500 * self.scale), 150 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, "R : Reset", [ int(500 * self.scale), 175 ], 1, 1, (0, 0, 0), 2)
        cv2.putText(self.image, "b : Rollback", [ int(500 * self.scale), 200 ], 1, 1, (0, 0, 0), 2)
        #for his in self.chess.history.arrHistory:
        #    print(f"History : {his}")
        #    his.print()

        if self.chess.turn.gameover:
            cv2.putText(self.image, "GAME OVER!", [ int(500 * self.scale), 225 ], 1, 1, (0, 0, 255), 2)

        i = 0
        for killedObj in self.chess.history.arrKilled:
            if killedObj == None:
                break
            self.drawKilledObject(int(i % 4), int(1 + i / 4), killedObj.getFullName())
            i = i + 1

    def draw(self):
        image_org = cv2.imread('img/background.png')
        self.image = cv2.resize(image_org, (int(image_org.shape[1] * self.scale), int(image_org.shape[0] * self.scale)))
        cv2.imshow(f"{self.viewName} {self.chess.turn.color}", self.image)
        cv2.setMouseCallback(f"{self.viewName} {self.chess.turn.color}", self.mouse_event, self.image)
        #print(f"Image Size({image.shape[1]} x {image.shape[0]} x {image.shape[2]})")
        self.loadObjImages()

        self.drawPosName()

        self.posCoordinator.clear()
        posNames = self.chess.cursor.getAllPosNames()
        #print(f"Pos Names for drawing : {posNames}")
        for posName in posNames:
            self.draw_object(posName)

        #self.draw_availables()
        #self.draw_selected()
        self.draw_info()

        cv2.imshow(f"{self.viewName} {self.chess.turn.color}", self.image)

    def scale_up(self):
        self.scale += 0.1
        self.draw()

    def scale_down(self):
        self.scale -= 0.1
        self.draw()

    ##################################################
    # Mouse Event
    ##################################################
    def mouse_event(self, event, x, y, flags, param):
        if event == cv2.EVENT_FLAG_LBUTTON:
            print(f"Clicked {x},{y}")
            for coord in self.posCoordinator:
                #print(f"Check {x} {y}, {coord[0]} {coord[1]} {coord[2]} {coord[3]}")
                if x > coord[0] and x < coord[2] and y > coord[1] and y < coord[3]:
                    msg = [ "Clicked", coord[4] ]
                    self.msg.append(msg)
                    break

    def getEvent(self):
        if len(self.msg):
            msg = self.msg.pop()
            return msg
        
        k = cv2.waitKeyEx(100)
        if k == -1:
            return None

        print(f"{k} key pressed")
        if k == 27:
            cv2.destroyAllWindows()
            msg = [ "Exit" ]
            return msg
        elif k == ord('R'):
            self.chess.reset(True)
            self.draw()
        elif k == ord('r'):
            self.chess.reset()
            self.draw()
        elif k == ord('b'):
            self.chess.cancelselected()
            if self.chess.rollback():
                # Castling rollback takes 2 actions.
                self.chess.rollback()
            self.draw()
        # Arrow Keys (8BitDo Gamepad)
        elif k == ord('e') or k == 0x250000:    # Left Key
            if self.invert == True:
                return [ "Right"]
            else:
                return [ "Left" ]
        elif k == ord('f') or k == 0x270000:    # Right Key
            if self.invert == True:
                return [ "Left" ]
            else:
                return [ "Right" ]
        elif k == ord('c') or k == 0x260000:    # Up Key
            if self.invert == True:
                return [ "Down" ]
            else:
                return [ "Up" ]
        elif k == ord('d') or k == 0x280000:
            if self.invert == True:
                return [ "Up" ]
            else:
                return [ "Down" ]
        elif k == ord('g') or k == ord(' '):
            return [ "Select" ]

        elif k == ord('+'):
            self.scale_up()
        elif k == ord('-'):
            self.scale_down()

    image = None
    objImages = {}
    objImages_small = {}
    obj_width = 0
    obj_height = 0
    scale = 1
    invert = False
    viewName = "Chess"

    msg = []
    posCoordinator = []

    chess = None

    objs = [
        'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackPawn',
        'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhitePawn',
        'Empty'
    ]