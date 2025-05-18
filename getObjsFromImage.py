import cv2

objs_data = [
    [ 0, 0, "BlackRook" ],
    [ 0, 1, "BlackKnight" ],
    [ 0, 2, "BlackBishop"],
    [ 0, 3, "BlackQueen"],
    [ 0, 4, "BlackKing"],
    [ 1, 0, "BlackPawn"],

    [ 2, 0, "Empty"],

    [ 6, 0, "WhitePawn"],
    [ 7, 0, "WhiteRook" ],
    [ 7, 1, "WhiteKnight" ],
    [ 7, 2, "WhiteBishop"],
    [ 7, 3, "WhiteQueen"],
    [ 7, 4, "WhiteKing"],
]

#img = cv2.imread("objects.png")
img = cv2.imread("objects_transparency.png")

height, width, color = img.shape

for obj in objs_data:
    print(f"Get Obj Image {obj[0]}, {obj[1]}, {obj[2]}.png")
    x = obj[1] * 49 + 1
    y = obj[0] * 49 + 1
    obj_img = img[y:y+49, x:x+49]
    #print(obj_img)
    cv2.imshow(obj[2], obj_img)
    cv2.imwrite(f"img/{obj[2]}.png", obj_img)

cv2.waitKey()
cv2.destroyAllWindows()