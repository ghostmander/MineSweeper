import random


print('Welcome to GeeseSpotter!')

x_dim = 5  # int(input('Please enter the x dimension: '))
y_dim = 5  # int(input('Please enter the y dimension: '))
count = 5  # int(input('Please enter the number of geese: '))


main_list = [[0 for x in range(x_dim)] for y in range(y_dim)]
printable_list = [["*" for x in range(x_dim)] for y in range(y_dim)]
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
        x_geese = random.randint(0, (y_dim - 1))
        y_geese = random.randint(0, x_dim - 1)
        main_list[x_geese][y_geese] = 9
        geese.append((x_geese, y_geese))


def show():
    pass


def mark():
    pass


def restart():
    main_list = [[0 for x in range(x_dim)] for y in range(y_dim)]
    printable_list = [["*" for x in range(x_dim)] for y in range(y_dim)]
    geese = []


def quit():
    pass


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


def boardPrinter():
    for print_object in printable_list:
        print(''.join(print_object))


def boardUpdater():
    global main_list, printable_list
    for i in range(y_dim):
        for j in range(x_dim):
            if main_list[i][j] != 0:
                printable_list[i][j] = str(main_list[i][j])
    boardPrinter()
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #


gooseAdder(x_dim, y_dim, count)
boardUpdater()
