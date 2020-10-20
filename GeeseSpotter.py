import random


print('Welcome to GeeseSpotter!')

x_dim = 3  # int(input('Please enter the x dimension: '))
y_dim = 5  # int(input('Please enter the y dimension: '))
count = 5  # int(input('Please enter the number of geese: '))

isRunning = True

main_list = [[0 for y in range(y_dim)] for x in range(x_dim)]
printable_list = [["*" for y in range(y_dim)] for x in range(x_dim)]
geese = []


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


def show():
    pass


def mark():
    pass


def restart():
    global main_list, printable_list, geese
    main_list = [[0 for x in range(x_dim)] for y in range(y_dim)]
    printable_list = [["*" for x in range(x_dim)] for y in range(y_dim)]
    geese = []


def quit():
    global isRunning
    isRunning = False


def actionTaken():
    ch = input("Please enter the action ([S]how; [M]ark; [R]estart; [Q]uit): ")
    if ch.upper() == "S":
        show()
    elif ch.upper() == "M":
        mark()
    elif ch.upper() == "R":
        restart()
    elif ch.upper() == "Q":
        quit()


def neighborCalc(x_coord, y_coord):
    global x_dim, y_dim, main_list

    if (x_coord, y_coord) == (0, 0):
        return ([(0, 1), (1, 0), (1, 1)])

    elif (x_coord, y_coord) == (x_dim - 1, y_dim - 1):
        return ([(-1, -2), (-2, -1), (-2, -2)])

    elif (x_coord, y_coord) == (0, y_dim - 1):
        return ([(0, -2), (1, -1), (1, -2)])

    elif (x_coord, y_coord) == (x_dim - 1, 0):
        return ([(-1, 1), (-2, 0), (-2, -1)])

    elif x_coord == 0:
        return ([(0, y_coord-1), (0, y_coord+1), (1, y_coord-1), (1, y_coord+1), (1, y_coord)])

    elif x_coord == (x_dim-1):
        return ([(-1, y_coord-1), (-1, y_coord+1), (-2, y_coord-1), (-2, y_coord+1), (-2, y_coord)])

    elif y_coord == 0:
        return ([(x_coord-1, 0), (x_coord+1, 0), (x_coord-1, 1), (x_coord+1, 1), (x_coord, 1)])

    elif y_coord == (y_dim-1):
        return ([(x_coord-1, -1), (x_coord+1, -1), (x_coord-1, -2), (x_coord+1, -2), (x_coord, -2)])
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


def boardUpdater():
    global main_list, printable_list
    for i in range(x_dim):
        for j in range(y_dim):
            if main_list[i][j] != 0:
                printable_list[i][j] = str(main_list[i][j])
    boardPrinter()
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #


gooseAdder(x_dim, y_dim, count)
countAdd()
boardUpdater()
