from matplotlib import pyplot as plt

array = [[0 for col in range(8)] for row in range(8)]

array[0][0] = 'L'
array[0][1] = 'K'
array[0][1] = 'V'

def print_rectangle(plt, x, y, obj):
    lA = [ x * 10 + 1, x * 10 + 9, x * 10 + 9, x * 10 + 1 ]
    lB = [ y * 10 + 1, y * 10 + 1, y * 10 + 9, y * 10 + 9 ]
    plt.fill(lA, lB)
    plt.text( x * 10 + 1, y * 10 + 1, obj)

print(f"Draw Rectangle")

for x in range(8):
    for y in range(8):
        print_rectangle(plt, x, y, array[x][y])
#print_rectangle(plt, 0, 0)
plt.show()
