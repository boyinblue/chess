import cv2
import chess

class ChessView:
    def __init__(self, chess):
        self.scale = 1.5
        self.chess = chess

    def loadObjImages(self):
        for obj in self.objs:
            img = cv2.imread(f"img/{obj}.png")
            self.objImages[obj] = cv2.resize(img, (int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)))
            self.objImages_small[obj] = cv2.resize(img, (int(img.shape[0] * self.scale / 2), int(img.shape[1] * self.scale / 2)))
            self.obj_width = self.objImages[obj].shape[1]
            self.obj_height = self.objImages[obj].shape[0]

        #print(f"Object Size : {obj_width} x {obj_height}")

    def draw_border(self, x, y, color, width):
        pt1 = ( x * self.obj_width + width, y * self.obj_height + width )
        pt2 = ( x * self.obj_width + self.obj_width - width, y * self.obj_height + self.obj_height - width )
        cv2.rectangle(self.image, pt1, pt2, color, width)

    def draw_object(self, x, y):
        obj = self.chess.array[y][x]
        if obj == None:
            objName = "Empty"
        else:
            objName = obj.getFullName()

        # Draw Object
        pX = x * self.obj_width + 1
        pY = y * self.obj_height + 1
        self.image[pY:pY+self.obj_height, pX:pX+self.obj_width] = self.objImages[objName]

        # Draw Border
        posName = self.chess.getPosName(self.chess, x, y)
        if x != self.chess.cursor[0] or y != self.chess.cursor[1]:
            self.draw_border(x, y, (0, 0, 0), 1)
        elif self.chess.availables.isAvaiable(posName):
            self.draw_border(x, y, (255, 0, 0), 3)
        elif self.chess.array[y][x] != None and self.chess.array[y][x].getColor() == self.chess.turn.getThisTurnName():
            self.draw_border(x, y, (255, 0, 0), 3)
        else:
            self.draw_border(x, y, (0, 0, 255), 3)

    def drawKilledObject(self, x, y, objName):
        print(f"Draw Killed Obj x={x}, y={y}")

        # Draw Object
        pX = int(500 * self.scale + x * self.obj_width / 2 + 1)
        pY = int(50 * self.scale + y * self.obj_height / 2 + 1)
        self.image[pY:int(pY + self.obj_height / 2), pX:int(pX + self.obj_width / 2)] = self.objImages_small[objName]

    def draw_selected(self):
        # Draw selected
        selected = self.chess.selected
        if selected[0] >= 8 or selected[1] >= 8:
            return
        print(f"Draw selected")
        cv2.circle(self.image, (int(selected[0] * self.obj_width + self.obj_width / 2), int(selected[1] * self.obj_height + self.obj_height / 2)), int(self.obj_width / 3), (255,255,0), 2)

    def draw_availables(self):
        for pos in self.chess.availables.get():
            print(f"Draw Availables {pos}")
            x, y = self.chess.getXY(self.chess, pos)
            cv2.circle(self.image, (int(x * self.obj_width + self.obj_width / 2), int(y * self.obj_height + self.obj_height / 2)), int(self.obj_width / 3), (0,0,255), 2)

    def delete_info_background(self):
        pt1 = ( int(400 * self.scale), 0 )
        pt2 = ( int(800 * self.scale), int(400 * self.scale) )
        cv2.rectangle(self.image, pt1, pt2, (255,255,255), -1)

    def draw_info(self):
        self.delete_info_background()

        turn = self.chess.turn.getThisTurnName()
        if turn == "White":
            textPos = [ int(400 * self.scale), int(375 * self.scale) ]
        else:
            textPos = [ int(400 * self.scale), int(25 * self.scale) ]
        cv2.putText(self.image, f"< {turn}", textPos, 1, 1, (0, 0, 0), 2)

        cv2.putText(self.image, "ESC : Exit", [ int(500 * self.scale), 25 ], 1, 1, (255, 255, 0), 2)
        cv2.putText(self.image, "R : Reset", [ int(500 * self.scale), 50 ], 1, 1, (255, 255, 0), 2)

        if self.chess.turn.gameover:
            cv2.putText(self.image, "GAME OVER!", [ int(400 * self.scale), int(50 * self.scale) ], 1, 1, (0, 0, 255), 2)

        i = 0
        for killedObj in self.chess.history.arrKilled:
            if killedObj == None:
                break
            self.drawKilledObject(int(i % 4), int(1 + i / 4), killedObj.getFullName())
            i = i + 1

    def draw(self):
        image_org = cv2.imread('img/background.png')
        self.image = cv2.resize(image_org, (int(image_org.shape[1] * self.scale), int(image_org.shape[0] * self.scale)))
        cv2.imshow('Chess', self.image)
        cv2.setMouseCallback("Chess", self.mouse_event, self.image)
        #print(f"Image Size({image.shape[1]} x {image.shape[0]} x {image.shape[2]})")
        self.loadObjImages()

        for x in range(8):
            for y in range(8):
                self.draw_object(x, y)

        self.draw_selected()
        self.draw_availables()
        self.draw_info()

        cv2.imshow('Chess', self.image)

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
            msg = [ "Clicked", int(x / self.obj_width), int(y / self.obj_height) ]
            self.msg.append(msg)

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
        elif k == ord('R'):
            self.chess.reset(self.chess, True)
            self.draw()
        elif k == ord('r'):
            self.chess.reset(self.chess)
            self.draw()
        elif k == ord('b'):
            self.chess.cancelselected(self.chess)
            if self.chess.rollback(self.chess):
                # Castling rollback takes 2 actions.
                self.chess.rollback(self.chess)
            self.draw()
        # Arrow Keys (8BitDo Gamepad)
        elif k == ord('e') or k == 0x250000:
            self.chess.cursor[0] = (self.chess.cursor[0] + 7) % 8
            self.draw()
        elif k == ord('f') or k == 0x270000:
            self.chess.cursor[0] = (self.chess.cursor[0] + 1) % 8
            self.draw()
        elif k == ord('c') or k == 0x260000:
            self.chess.cursor[1] = (self.chess.cursor[1] + 7) % 8
            self.draw()
        elif k == ord('d') or k == 0x280000:
            self.chess.cursor[1] = (self.chess.cursor[1] + 1) % 8
            self.draw()
        elif k == ord('g') or k == ord(' '):
            self.chess.clicked(self.chess, self.chess.cursor[0], self.chess.cursor[1])
            self.draw()

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

    msg = []

    chess = None

    objs = [
        'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackPawn',
        'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhitePawn',
        'Empty'
    ]