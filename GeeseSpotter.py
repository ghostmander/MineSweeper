import random


print('Welcome to GeeseSpotter!')

x_dim = int(input('Please enter the x dimension: '))
y_dim = int(input('Please enter the y dimension: '))
count = int(input('Please enter the number of geese: '))

isRunning = True


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


def show(x_coord, y_coord):
    global main_list, printable_list, revealPerTurn
    if ((x_coord, y_coord) not in marked) and ((x_coord, y_coord) not in revealed):
        revealPerTurn.append((x_coord, y_coord))
        if main_list[x_coord][y_coord] == 0:
            zeroReveal(x_coord, y_coord)
        for x, y in revealPerTurn:
            normalReveal(x, y)
        revealed.extend(revealPerTurn)
        revealPerTurn = []
        markAll()
    boardPrinter()


def normalReveal(x_coord, y_coord):
    global main_list, printable_list, revealPerTurn
    printable_list[x_coord][y_coord] = str(main_list[x_coord][y_coord])


def zeroReveal(x_coord, y_coord):
    global zeroes, revealPerTurn
    neighbors = neighborCalc(x_coord, y_coord)
    for x, y in neighbors:
        if (x, y) not in zeroes:
            revealPerTurn.append((x, y))
            if main_list[x][y] == 0:
                zeroes.append((x, y))
                zeroReveal(x, y)


def mark(x, y):
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
    return 1


def test():
    global main_list, printable_list
    for i in range(x_dim):
        for j in range(y_dim):
            printable_list[i][j] = str(main_list[i][j])
    boardPrinter()
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #


restart()

for print_object in main_list:
    for i in print_object:
        print(str(i), end='')
    print()

boardPrinter()
# test()
while isRunning:
    actionTaken()
    winVar = isGameWon()
    if winVar == 2:
        print("Congratulations! You Win! Press any Key to Restart or Press \'q\' to Exit.")
        ch = input().lower().strip()
        if ch == 'q':
            print('Thanks For Playing! Have a Good Day.')
            break
        restart()
    elif winVar == 0:
        print("You Lost! Press any Key to Restart or Press \'q\' to Exit.")
        ch = input().lower().strip()
        if ch == 'q':
            print('Thanks For Playing! Have a Good Day.')
            break
        restart()
