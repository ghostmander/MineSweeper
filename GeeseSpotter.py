import random
import tkinter as tk
try:
    from PIL import Image, ImageTk
except ImportError:
    import ImageTk
    import Image


print('Welcome to GeeseSpotter!')

x_dim = 5  # int(input('Please enter the x dimension: '))
y_dim = 5  # int(input('Please enter the y dimension: '))
count = 1  # int(input('Please enter the number of geese: '))


root = tk.Tk()
root.title("Geese Spotter")
root.geometry("684x700")
root.configure(bg='#a1a1a1')

main_list = [[0 for y in range(y_dim)] for x in range(x_dim)]
printable_list = [["*" for y in range(y_dim)] for x in range(x_dim)]
geese, zeroes, revealPerTurn, marked, revealed = [], [], [], [], []
isRunning = False  # True

game = tk.Frame(root, bg='#000', height=572, width=572)
game.pack(pady=20)


# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# |||                                           ||||| #
# |||                  FUNCTIONS                ||||| #
# |||                                           ||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
def gooseAdder(x_dim, y_dim, count):
    global main_list, geese
    for i in range(count):
        while True:
            x_geese = random.randint(0, (x_dim - 1))
            y_geese = random.randint(0, y_dim - 1)
            if (x_geese, y_geese) not in geese:
                break
        main_list[x_geese][y_geese] = 9
        geese.append((x_geese, y_geese))


def show(x_coord, y_coord, event):
    global main_list, printable_list, revealPerTurn, revealed
    buttonUpdater(event.widget, main_list[x_coord][y_coord])

    if ((x_coord, y_coord) not in marked) and ((x_coord, y_coord) not in revealed):
        revealPerTurn.append((x_coord, y_coord))
        if main_list[x_coord][y_coord] == 0:
            zeroReveal(x_coord, y_coord)
        for x, y in revealPerTurn:
            normalReveal(x, y)
        revealed.extend(revealPerTurn)
        revealed = list(set(revealed))
        revealPerTurn = []
        markAll()
    boardPrinter()
    # winCondition()


def normalReveal(x_coord, y_coord, ):
    global main_list, printable_list, revealPerTurn
    printable_list[x_coord][y_coord] = str(main_list[x_coord][y_coord])


def zeroReveal(x_coord, y_coord, ):
    global zeroes, revealPerTurn
    neighbors = neighborCalc(x_coord, y_coord)
    for x, y in neighbors:
        if (x, y) not in zeroes:
            revealPerTurn.append((x, y))
            if main_list[x][y] == 0:
                zeroes.append((x, y))
                zeroReveal(x, y)


def mark(x, y, event):
    global printable_list, marked
    if ((x, y) not in marked) and ((x, y) not in revealed):
        marked.append((x, y))
        markAll()
    elif ((x, y) in marked) and ((x, y) not in revealed):
        marked.remove((x, y))
        printable_list[x][y] = '*'
    boardPrinter()


def markAll():
    global marked, printable_list
    for x, y in marked:
        printable_list[x][y] = 'M'


def restart():
    global main_list, printable_list, geese, zeroes, revealPerTurn, marked, revealed
    main_list = [[0 for y in range(y_dim)] for x in range(x_dim)]
    printable_list = [["*" for y in range(y_dim)] for x in range(x_dim)]
    geese, zeroes, revealPerTurn, marked, revealed = [], [], [], [], []
    gooseAdder(x_dim, y_dim, count)
    countAdd()
    for i in range(x_dim):
        for j in range(y_dim):
            buttonFunc(i, j)


def quit():
    global isRunning
    isRunning = False


def actionTaken():
    ch = input("Please enter the action ([S]how; [M]ark; [R]estart; [Q]uit): ")
    if ch.upper() == "S":
        x = int(input("Please enter the x location: "))
        y = int(input("Please enter the y location: "))
        show(x, y)
    elif ch.upper() == "M":
        x = int(input("Please enter the x location: "))
        y = int(input("Please enter the y location: "))
        mark(x, y)
    elif ch.upper() == "R":
        restart()
    elif ch.upper() == "Q":
        quit()


def neighborCalc(x_coord, y_coord):
    global x_dim, y_dim, main_list

    if (x_coord, y_coord) == (0, 0):
        return ([(0, 1), (1, 0), (1, 1)])

    elif (x_coord, y_coord) == (x_dim - 1, y_dim - 1):
        return ([(x_dim-1, y_dim-2), (x_dim-2, y_dim-1), (x_dim-2, y_dim-2)])

    elif (x_coord, y_coord) == (0, y_dim - 1):
        return ([(0, y_dim-2), (1, y_dim-1), (1, y_dim-2)])

    elif (x_coord, y_coord) == (x_dim - 1, 0):
        return ([(x_dim-1, 1), (x_dim-2, 0), (x_dim-2, 1)])

    elif x_coord == 0:
        return ([(0, y_coord-1), (0, y_coord+1), (1, y_coord-1), (1, y_coord+1), (1, y_coord)])

    elif x_coord == (x_dim-1):
        return ([(x_dim-1, y_coord-1), (x_dim-1, y_coord+1), (x_dim-2, y_coord-1), (x_dim-2, y_coord+1), (x_dim-2, y_coord)])

    elif y_coord == 0:
        return ([(x_coord-1, 0), (x_coord+1, 0), (x_coord-1, 1), (x_coord+1, 1), (x_coord, 1)])

    elif y_coord == (y_dim-1):
        return ([(x_coord, y_dim-2), (x_coord - 1, y_dim-2), (x_coord + 1, y_dim-2), (x_coord - 1, y_dim-1), (x_coord + 1, y_dim-1)])
    else:
        return [(x, y) for x in range(x_coord-1, x_coord+2) for y in range(y_coord-1, y_coord+2)]


def countAdd():
    global main_list, printable_list, geese
    for i, j in geese:
        neighbors = neighborCalc(i, j)
        for x, y in neighbors:
            main_list[x][y] += 1

    for i, j in geese:
        main_list[i][j] = 9


def boardPrinter():
    for print_object in printable_list:
        print(''.join(print_object))


def isGameWon():
    if [i for i in geese if i not in marked] == []:
        return 2
    for i in geese:
        if i in revealed:
            return 0
    if (count + len(revealed) == x_dim*y_dim):
        return 2
    print(len(revealed))
    return 1


def winCondition():
    winVar = isGameWon()
    if winVar == 2:
        print("Congratulations! You Win! Press any Key to Restart or Press \'q\' to Exit.")
        ch = input().lower().strip()
        if ch == 'q':
            print('Thanks For Playing! Have a Good Day.')
            return None
        restart()
        boardPrinter()
    elif winVar == 0:
        print("You Lost! Press any Key to Restart or Press \'q\' to Exit.")
        ch = input().lower().strip()
        if ch == 'q':
            print('Thanks For Playing! Have a Good Day.')
            return None
        restart()
        boardPrinter()


def buttonFunc(i, j):
    height, width = (572//x_dim), (572//y_dim)
    image = ImageTk.PhotoImage(Image.open(
        'assets/unrevealed_tile.png').resize((height, width)))
    lbl = tk.Label(game, image=image)
    lbl.image = image
    lbl.grid(row=i, column=j, padx=0.5, pady=0.5)
    lbl.bind("<Button-1>", lambda x: show(i, j, x))
    lbl.bind("<Button-2>", lambda x: mark(i, j, x))
    lbl.bind("<Button-3>", lambda x: mark(i, j, x))


def buttonUpdater(lbl, number):
    if number == 0:
        image = ImageTk.PhotoImage(Image.open(
            'assets/zero.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 1:
        image = ImageTk.PhotoImage(Image.open(
            'assets/one.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 2:
        image = ImageTk.PhotoImage(Image.open(
            'assets/two.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 3:
        image = ImageTk.PhotoImage(Image.open(
            'assets/three.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 4:
        image = ImageTk.PhotoImage(Image.open(
            'assets/four.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 5:
        image = ImageTk.PhotoImage(Image.open(
            'assets/five.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 6:
        image = ImageTk.PhotoImage(Image.open(
            'assets/six.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 7:
        image = ImageTk.PhotoImage(Image.open(
            'assets/seven.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 8:
        image = ImageTk.PhotoImage(Image.open(
            'assets/eight.png').resize(((572//x_dim), (572//y_dim))))
    elif number == 9:
        image = ImageTk.PhotoImage(Image.open(
            'assets/bomb.png').resize(((572//x_dim), (572//y_dim))))
    elif number == -1:
        image = ImageTk.PhotoImage(Image.open(
            'assets/mark.png').resize(((572//x_dim), (572//y_dim))))
    lbl['image'] = image
    lbl.image = image
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #


gooseAdder(x_dim, y_dim, count)
countAdd()


for i in range(x_dim):
    for j in range(y_dim):
        buttonFunc(i, j)


boardPrinter()

tk.mainloop()
