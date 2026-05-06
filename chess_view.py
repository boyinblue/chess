import cv2
from chess import Chess, Position
import time
import os
import numpy as np
from PIL import Image, ImageDraw, ImageFont

# ── PIL font helpers ───────────────────────────────────────────────────────────
_FONT_CACHE = {}

def _get_font(size, bold=False):
    key = (size, bold)
    if key in _FONT_CACHE:
        return _FONT_CACHE[key]
    candidates = [
        "C:/Windows/Fonts/malgun.ttf",       # Malgun Gothic (Korean)
        "C:/Windows/Fonts/malgunbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
    ]
    bold_candidates = [c for c in candidates if 'bd' in c or 'b.' in c]
    regular_candidates = [c for c in candidates if 'bd' not in c and 'b.' not in c]
    search = bold_candidates + regular_candidates if bold else regular_candidates + bold_candidates
    for path in search:
        if os.path.isfile(path):
            font = ImageFont.truetype(path, size)
            _FONT_CACHE[key] = font
            return font
    font = ImageFont.load_default()
    _FONT_CACHE[key] = font
    return font


def _put_text_pil(cv_img, text, x, y, font_size=15, color=(0, 0, 0), bold=False):
    """Draw anti-aliased text onto a BGR OpenCV image using Pillow."""
    rgb = cv2.cvtColor(cv_img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(rgb)
    draw = ImageDraw.Draw(pil_img)
    font = _get_font(font_size, bold)
    # Pillow uses RGB, color param is BGR → convert
    r, g, b = color[2], color[1], color[0]
    draw.text((x, y), text, font=font, fill=(r, g, b))
    result = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
    cv_img[:] = result


def _measure_text_pil(text, font_size=15, bold=False):
    font = _get_font(font_size, bold)
    canvas = Image.new("RGB", (10, 10), (255, 255, 255))
    draw = ImageDraw.Draw(canvas)
    box = draw.textbbox((0, 0), text, font=font)
    return box[2] - box[0], box[3] - box[1]


# ── win32 icon helper ──────────────────────────────────────────────────────────
def _set_window_icon(hwnd, icon_path):
    try:
        import win32gui, win32con, win32api
        icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
        hicon = win32gui.LoadImage(None, icon_path, win32con.IMAGE_ICON, 0, 0, icon_flags)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
        win32gui.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG,  hicon)
    except Exception:
        pass

ICON_PATH = os.path.join(os.path.dirname(__file__), "img", "chess_icon.ico")

class ChessView:
    def __init__(self, chess, invert, viewName):
        self.scale = 1.5
        self.chess = chess
        self.invert = invert
        self.viewName = viewName
        self.windowName = f"{self.viewName} {self.chess.turn.color}"
        self._icon_set = False
        self.hideCursor = False

    def getMenuHeight(self):
        return int(30 * self.scale)

    def drawMenu(self):
        menu_h = self.getMenuHeight()
        cv2.rectangle(self.image, (0, 0), (self.image.shape[1], menu_h), (235, 236, 242), -1)
        cv2.line(self.image, (0, menu_h), (self.image.shape[1], menu_h), (178, 182, 194), 1)

        items = [
            ("새 게임", "Reset"),
            ("무르기", "Rollback"),
            ("저장", "SaveRecord"),
            ("재생", "ReplayRecord"),
            ("종료", "Exit"),
        ]

        self.menuCoordinator.clear()
        x = int(10 * self.scale)
        y = int(4 * self.scale)
        fs = max(11, int(10.5 * self.scale))

        for label, ev in items:
            tw, th = _measure_text_pil(label, fs, bold=True)
            pad_x = int(10 * self.scale)
            pad_y = int(4 * self.scale)
            bx1 = x
            by1 = y
            bx2 = x + tw + pad_x * 2
            by2 = y + th + pad_y * 2

            # Shadow + button body
            cv2.rectangle(self.image, (bx1 + 1, by1 + 1), (bx2 + 1, by2 + 1), (186, 190, 202), -1)
            cv2.rectangle(self.image, (bx1, by1), (bx2, by2), (248, 249, 252), -1)
            cv2.rectangle(self.image, (bx1, by1), (bx2, by2), (165, 170, 184), 1)

            _put_text_pil(self.image, label, bx1 + pad_x, by1 + pad_y, fs, (48, 52, 64), bold=True)
            self.menuCoordinator.append([bx1, by1, bx2, by2, ev])
            x = bx2 + int(10 * self.scale)

    def loadObjImages(self):
        for obj in self.objs:
            img = cv2.imread(f"img/{obj}.png")
            self.objImages[obj] = cv2.resize(img, (int(img.shape[1] * self.scale), int(img.shape[0] * self.scale)))
            self.objImages_small[obj] = cv2.resize(img, (int(img.shape[0] * self.scale / 2), int(img.shape[1] * self.scale / 2)))
            self.obj_width = self.objImages[obj].shape[1]
            self.obj_height = self.objImages[obj].shape[0]

        #print(f"Object Size : {obj_width} x {obj_height}")

    def getObjectCoordinate(self, x, y, width):
        top = self.getMenuHeight()
        ptX = ( x + 1 ) * self.obj_width + width
        ptY = top + ( y + 1 ) * self.obj_height + width
        ptX2 = ( x + 2 ) * self.obj_width - width
        ptY2 = top + ( y + 2 ) * self.obj_height - width
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
        top = self.getMenuHeight()
        for i in range(8):
            if self.invert == True:
                Idx = 7 - i
            else:
                Idx = i

            textPos = [ int(self.obj_width / 2), int(top + ( i + 1 ) * self.obj_height + self.obj_height / 2) ]
            cv2.putText(self.image, f"{Position.Id2Row[Idx]}", textPos, 1, 1, (0, 0, 0), 2)
            textPos = [ int( ( i + 1 ) * self.obj_width + self.obj_width / 2), int(top + self.obj_height / 2) ]
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
        
        if self.hideCursor or posName != self.chess.cursor.posName:
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
        top = self.getMenuHeight()
        pX = int(500 * self.scale + x * self.obj_width / 2 + 1)
        # Keep captured pieces below the info text area.
        pY = top + int(305 * self.scale + y * self.obj_height / 2 + 1)
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
        top = self.getMenuHeight()
        pt1 = ( int(500 * self.scale), top )
        pt2 = ( int(800 * self.scale), top + int(400 * self.scale) )
        cv2.rectangle(self.image, pt1, pt2, (255,255,255), -1)

    def draw_info(self):
        self.delete_info_background()

        turn = self.chess.turn.getThisTurnName()
        posName = self.chess.cursor.posName
        obj = self.chess.getObject(posName)
        objName = "Empty" if obj is None else obj.getFullName()

        ix = int(500 * self.scale) + 8
        top = self.getMenuHeight()
        FS  = 15   # regular font size
        FSB = 16   # bold / highlight font size
        LH  = 26   # line height
        y = top + 14

        _put_text_pil(self.image, f"♟  {self.chess.turn.comm_type.upper()}",
                      ix, y, FSB, (40, 40, 40), bold=True);              y += LH + 6
        _put_text_pil(self.image, f"My Color : {self.chess.turn.color}",
                      ix, y, FS, (60, 60, 60));                          y += LH
        _put_text_pil(self.image, f"Turn      : {turn}",
                      ix, y, FS, (0, 120, 0) if turn == "White" else (160, 0, 0)); y += LH
        _put_text_pil(self.image, f"Cursor  : {posName}",
                      ix, y, FS, (60, 60, 60));                          y += LH
        _put_text_pil(self.image, f"Object  : {objName}",
                      ix, y, FS, (60, 60, 60));                          y += LH + 8

        # Key hints
        hints = [
            ("ESC / Q", "종료"),
            ("R",       "리셋"),
            ("b",       "무르기"),
            ("s",       "기보 저장"),
            ("p",       "기보 재생"),
        ]
        for key, label in hints:
            _put_text_pil(self.image, f"[{key}]  {label}",
                          ix, y, FS - 1, (100, 100, 100));               y += LH - 4

        # Game-over banner
        if self.chess.turn.gameover:
            if self.chess.turn.winner == "Draw":
                msg = "DRAW  –  무승부"
                color = (0, 140, 140)
            else:
                msg = f"{self.chess.turn.winner}  승리! 🏆"
                color = (0, 0, 200)
            y += 8
            _put_text_pil(self.image, msg, ix, y, FSB + 2, color, bold=True); y += LH + 4

        # Captured pieces label
        cap_y = top + int(300 * self.scale)
        _put_text_pil(self.image, "Captured", ix, cap_y, FS, (80, 80, 80), bold=True)

        i = 0
        for killedObj in self.chess.history.arrKilled:
            if killedObj == None:
                break
            self.drawKilledObject(int(i % 4), int(i / 4), killedObj.getFullName())
            i = i + 1

    def draw(self):
        image_org = cv2.imread('img/background.png')
        self.image = cv2.resize(image_org, (int(image_org.shape[1] * self.scale), int(image_org.shape[0] * self.scale)))
        cv2.imshow(self.windowName, self.image)
        cv2.setMouseCallback(self.windowName, self.mouse_event, self.image)
        # Set window icon once after first imshow
        if not self._icon_set and os.path.isfile(ICON_PATH):
            cv2.waitKey(1)
            try:
                import win32gui
                hwnd = win32gui.FindWindow(None, self.windowName)
                if hwnd:
                    _set_window_icon(hwnd, ICON_PATH)
                    self._icon_set = True
            except Exception:
                self._icon_set = True
        self.loadObjImages()

        self.drawMenu()

        self.drawPosName()

        self.posCoordinator.clear()
        posNames = self.chess.cursor.getAllPosNames()
        #print(f"Pos Names for drawing : {posNames}")
        for posName in posNames:
            self.draw_object(posName)

        #self.draw_availables()
        #self.draw_selected()
        self.draw_info()

        cv2.imshow(self.windowName, self.image)

    def animateMovement(self, posName, newPosName, objName, duration=0.20, steps=10):
        if posName == newPosName:
            return

        moved_obj = self.chess.array.get(newPosName)
        if moved_obj is None:
            return

        window_name = self.windowName

        # Draw a base frame with destination square empty, then overlay moving piece.
        self.chess.array[newPosName] = None
        self.draw()
        base = self.image.copy()
        self.chess.array[newPosName] = moved_obj

        sx, sy = self.getXY(posName, self.invert)
        ex, ey = self.getXY(newPosName, self.invert)
        sptX, sptY, _, _ = self.getObjectCoordinate(sx, sy, 0)
        eptX, eptY, _, _ = self.getObjectCoordinate(ex, ey, 0)

        if objName not in self.objImages:
            self.draw()
            return

        obj_img = self.objImages[objName]
        obj_h, obj_w = obj_img.shape[:2]
        delay_ms = max(1, int((duration / steps) * 1000))

        for i in range(1, steps + 1):
            t = i / steps
            cur_x = int(sptX + (eptX - sptX) * t)
            cur_y = int(sptY + (eptY - sptY) * t)

            frame = base.copy()
            frame[cur_y:cur_y + obj_h, cur_x:cur_x + obj_w] = obj_img
            cv2.imshow(window_name, frame)
            cv2.waitKeyEx(delay_ms)

        self.draw()

    def animateMoves(self, moves):
        for mov in moves:
            if mov.posName == mov.newPosName:
                continue
            obj = self.chess.getObject(mov.newPosName)
            if obj is None:
                continue
            self.animateMovement(mov.posName, mov.newPosName, obj.getFullName())

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

            for menu in self.menuCoordinator:
                if x > menu[0] and x < menu[2] and y > menu[1] and y < menu[3]:
                    self.msg.append([menu[4]])
                    return

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
        if k == 27 or k == ord('q') or k == ord('Q'):
            cv2.destroyAllWindows()
            msg = [ "Exit" ]
            return msg
        elif k == ord('R'):
            return [ "Reset" ]
        elif k == ord('r'):
            return [ "Reset" ]
        elif k == ord('b'):
            return [ "Rollback" ]
        elif k == ord('s') or k == ord('S'):
            return [ "SaveRecord" ]
        elif k == ord('p') or k == ord('P'):
            return [ "ReplayRecord" ]
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
    menuCoordinator = []

    chess = None

    objs = [
        'BlackRook',  'BlackKnight',  'BlackBishop',  'BlackQueen',   'BlackKing',    'BlackPawn',
        'WhiteRook',  'WhiteKnight',  'WhiteBishop',  'WhiteQueen',   'WhiteKing',    'WhitePawn',
        'Empty'
    ]