import random, pickle
from tkinter import *
try:
    import pyglet
    try:
        from PIL import Image, ImageTk
    except ImportError:
        import ImageTk
        import Image
except ModuleNotFoundError:
    import sys, subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pillow"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyglet"])
    del sys
    del subprocess
    import pyglet
    try:
        from PIL import Image, ImageTk
    except ImportError:
        import ImageTk
        import Image



# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# |||                                           ||||| #
# |||                  FUNCTIONS                ||||| #
# |||                                           ||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
class Timer:
    def __init__(self, label):
        self.label = label
        self.seconds = 0
        self.isRunning = False

    def counter_label(self):
        def count():
            if self.isRunning:
                self.label['text'] = self.seconds
                self.label.after(1000, count)
                self.seconds += 1
        count()

    def start(self):
        self.isRunning = True
        self.counter_label()

    def reset(self):
        self.isRunning = False
        self.seconds = 0


def menuMaker():
    mnu = Menu(root)
    root.config(menu = mnu)

    file_menu = Menu(mnu, tearoff = False)
    mnu.add_cascade(label = "File", menu = file_menu)

    file_menu.add_command(label = "New Game (F2)", command = restart)
    file_menu.add_separator()
    file_menu.add_command(label = "Options      (F5)", command = firstScreen)
    file_menu.add_separator()
    file_menu.add_command(label = "Exit", command = root.quit)


def minesAdder(x_dim, y_dim, count):
    global main_list, mines
    for i in range(count):
        while True:
            x_geese = random.randint(0, (x_dim - 1))
            y_geese = random.randint(0, y_dim - 1)
            if (x_geese, y_geese) not in mines:
                break
        main_list[x_geese][y_geese] = 9
        mines.append((x_geese, y_geese))


def show(x_coord, y_coord, event):
    global main_list, printable_list, revealPerTurn, revealed, timer

    if not timer.isRunning: timer.start()
    if ((x_coord, y_coord) not in marked) and ((x_coord, y_coord) not in revealed):
        buttonUpdater(event.widget, main_list[x_coord][y_coord])
        revealPerTurn.append((x_coord, y_coord))
        if main_list[x_coord][y_coord] == 0:
            zeroReveal(x_coord, y_coord)
        revealPerTurn = [(x, y) for x, y in revealPerTurn if (x, y) not in marked]
        for x, y in revealPerTurn:
            normalReveal(x, y)
        revealed.extend(revealPerTurn)
        revealed = list(set(revealed))
        revealPerTurn = []
        markAll()
    winCondition()


def normalReveal(x_coord, y_coord):
    global main_list, printable_list, revealPerTurn
    buttonUpdater(tiles[x_coord][y_coord], main_list[x_coord][y_coord])


def zeroReveal(x_coord, y_coord):
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
        buttonUpdater(event.widget, -1)
        marked.append((x, y))
        markAll()
    elif ((x, y) in marked) and ((x, y) not in revealed):
        buttonUpdater(event.widget, -2)
        marked.remove((x, y))
        printable_list[x][y] = '*'
    mine_label["text"] = count - len(marked)
    winCondition()


def markAll():
    global marked, printable_list
    for x, y in marked:
        printable_list[x][y] = 'M'


def tileList():
    global tiles
    tiles = [x for x in game.winfo_children()]
    tiles = list(tiles[i:i + y_dim] for i in range(0, len(tiles), y_dim))


def restart():
    global root
    root.destroy()
    main()


def neighborCalc(x_coord, y_coord):
    global x_dim, y_dim, main_list

    if (x_coord, y_coord) == (0, 0):
        return [(0, 1), (1, 0), (1, 1)]

    elif (x_coord, y_coord) == (x_dim - 1, y_dim - 1):
        return [(x_dim - 1, y_dim - 2), (x_dim - 2, y_dim - 1), (x_dim - 2, y_dim - 2)]

    elif (x_coord, y_coord) == (0, y_dim - 1):
        return [(0, y_dim - 2), (1, y_dim - 1), (1, y_dim - 2)]

    elif (x_coord, y_coord) == (x_dim - 1, 0):
        return [(x_dim - 1, 1), (x_dim - 2, 0), (x_dim - 2, 1)]

    elif x_coord == 0:
        return [(0, y_coord - 1), (0, y_coord + 1), (1, y_coord - 1), (1, y_coord + 1), (1, y_coord)]

    elif x_coord == (x_dim - 1):
        return ([(x_dim - 1, y_coord - 1), (x_dim - 1, y_coord + 1), (x_dim - 2, y_coord - 1), (x_dim - 2, y_coord + 1),
                 (x_dim - 2, y_coord)])

    elif y_coord == 0:
        return [(x_coord - 1, 0), (x_coord + 1, 0), (x_coord - 1, 1), (x_coord + 1, 1), (x_coord, 1)]

    elif y_coord == (y_dim - 1):
        return ([(x_coord, y_dim - 2), (x_coord - 1, y_dim - 2), (x_coord + 1, y_dim - 2), (x_coord - 1, y_dim - 1),
                 (x_coord + 1, y_dim - 1)])
    else:
        return [(x, y) for x in range(x_coord - 1, x_coord + 2) for y in range(y_coord - 1, y_coord + 2)]


def countAdd():
    global main_list, printable_list, mines
    for i, j in mines:
        neighbors = neighborCalc(i, j)
        for x, y in neighbors:
            main_list[x][y] += 1

    for i, j in mines:
        main_list[i][j] = 9


def isGameWon():
    for i in mines:
        if i in revealed:
            return 0
    if count + len(revealed) == x_dim * y_dim:
        return 2
    return 1


def winCondition():
    global timer
    winVar = isGameWon()
    if winVar in (0, 2):
        timer.reset()
        window = Toplevel()
        window.grab_set()
        window.configure(bg = '#515151')
        window.geometry("330x250")
        window.iconbitmap('assets/Sprites/logo.ico')
        stats = Frame(window, bg = '#515151')
        stats.grid(row = 0, column = 0, columnspan = 2, padx = 20, pady = 20)
        tot, win, perc = statChanger(winVar)
        Label(stats, text = f"Games Played: {tot}", bg = '#515151', fg = '#fff', font = ('Calibri 12')).grid(row = 1,
                                                                                                             column = 0,
                                                                                                             padx = 5,
                                                                                                             pady = 5)
        Label(stats, text = f"Games Won: {win}", bg = '#515151', fg = '#fff', font = ('Calibri 12')).grid(row = 2,
                                                                                                          column = 0,
                                                                                                          padx = 5,
                                                                                                          pady = 5)
        Label(stats, text = f"Percentage: {perc}", bg = '#515151', fg = '#fff', font = ('Calibri 12')).grid(row = 1,
                                                                                                            column = 1,
                                                                                                            padx = 5,
                                                                                                            pady = 5)

        exitBtn = Label(window, text = "   Exit   ", font = ('Calibri 26 bold'), borderwidth = 3, relief = 'raised',
                        bg = '#A10000', fg = '#fff')
        exitBtn.grid(row = 1, column = 0, padx = 7, pady = 7)
        exitBtn.bind('<Button-1>', lambda x: root.destroy())

        restBtn = Label(window, text = "Play Again", font = ('Calibri 26 bold'), borderwidth = 3, relief = 'raised',
                        bg = '#A10000', fg = '#fff')
        restBtn.grid(row = 1, column = 1, padx = 7, pady = 7)
        restBtn.bind('<Button-1>', lambda x: restart())
        if winVar == 2:
            window.title("You Win!")
            Label(stats, text = "Congratulations! You Won the Game!!", bg = '#515151', fg = '#fff',
                  font = ('Calibri 12 bold')).grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)
        elif winVar == 0:
            window.title("You Lose!")
            Label(stats, text = "Sorry you Lost, Better Luck Next Time!", bg = '#515151', fg = '#fff',
                  font = ('Calibri 12 bold')).grid(row = 0, column = 0, columnspan = 2, padx = 10, pady = 10)


def buttonFunc(i, j):
    height, width = (572 // y_dim), (572 // x_dim)
    image = ImageTk.PhotoImage(Image.open(
        'assets/Sprites/unrevealed_tile.png').resize((height, width)))
    lbl = Label(game, image = image)
    lbl.image = image
    lbl.grid(row = i, column = j, padx = 0.5, pady = 0.5)
    lbl.bind("<Button-1>", lambda x: show(i, j, x))
    lbl.bind("<Button-2>", lambda x: mark(i, j, x))
    lbl.bind("<Button-3>", lambda x: mark(i, j, x))


def buttonUpdater(lbl, number):
    if number == 0:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/zero.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 1:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/one.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 2:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/two.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 3:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/three.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 4:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/four.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 5:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/five.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 6:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/six.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 7:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/seven.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 8:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/eight.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == 9:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/bomb.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == -1:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/flag.png').resize(((572 // y_dim), (572 // x_dim))))
    elif number == -2:
        image = ImageTk.PhotoImage(Image.open(
            'assets/Sprites/unrevealed_tile.png').resize(((572 // y_dim), (572 // x_dim))))
    lbl['image'] = image
    lbl.image = image


def statChanger(x):
    with open('assets/data', 'rb') as f:
        data = pickle.load(f)

        tot, win, perc = data['Stats']['Total'], data['Stats']['Win'], data['Stats']['Percentage']

        if x: 
            win += 1; 
            perc = f"{(win * 100) // tot}%"

        data['Stats']['Total'], data['Stats']['Win'], data['Stats']['Percentage'] = tot, win, perc

    with open('assets/data', 'wb') as f:
        writeObject = pickle.dump(data, f)
    
    return tot, win, perc


def dimSet(height, width, mines, diff):
    global x_dim, y_dim, count
    value = diff.get()
    toRestart = False

    if value == 1:
        x_dim = 9
        y_dim = 9
        count = 10
        toRestart = True
    elif value == 2:
        x_dim = 16
        y_dim = 16
        count = 40
        toRestart = True
    elif value == 3:
        x_dim = 24
        y_dim = 24
        count = 99
        toRestart = True

    elif value == 0:
        x_dim = height.get()
        y_dim = width.get()
        count = mines.get()

        x_dim = int(x_dim)
        y_dim = int(y_dim)
        count = int(count)

        if (x_dim >= 9) and (y_dim >= 9) and (10 <= count <= x_dim * y_dim):
            toRestart = True
        else:
            print('\a')

    if toRestart:
        with open('assets/data', 'rb') as f:
            data = pickle.load(f)
            data['Dimensions']['xdim'], data['Dimensions']['ydim'], data['Dimensions']['mines'] = x_dim, y_dim, count

        with open('assets/data', 'wb') as f:
            pickle.dump(data, f)

        restart()


def firstScreen():
    config = Toplevel()
    config.grab_set()
    config.iconbitmap('assets/Sprites/logo.ico')
    difficulty = LabelFrame(config, text = 'Difficulty')
    difficulty.pack(padx = 20, pady = 20)

    Button(config, text = "OK", command = lambda: dimSet(height, width, mines, diff)).pack()

    firstThreeDifficulty = Frame(difficulty)
    firstThreeDifficulty.grid(column = 0, row = 0, padx = 10)

    customDifficulty = Frame(difficulty)
    customDifficulty.grid(column = 1, row = 0, padx = 10)
    customDifficultyButton = Frame(customDifficulty)
    customDifficultyButton.grid(row = 0, column = 0, columnspan = 2)

    diff = IntVar()
    diff.set(1)

    bbtn = Radiobutton(firstThreeDifficulty, text = "Beginner    \n10 Mines\n9x9 Grid  ", variable = diff, value = 1)
    bbtn.pack(anchor = W)
    ibtn = Radiobutton(firstThreeDifficulty, text = "Intermediate\n40 Mines\n16x16 Grid", variable = diff, value = 2)
    ibtn.pack(anchor = W)
    abtn = Radiobutton(firstThreeDifficulty, text = "Advanced    \n99 Mines\n24x24 Grid", variable = diff, value = 3)
    abtn.pack(anchor = W)
    customBtn = Radiobutton(customDifficultyButton, text = "Custom", variable = diff, value = 0)
    customBtn.pack(anchor = W)

    def validate_entry(text, min, max, widget):
        if text == "":
            return True
        try:
            value = int(text)
        except ValueError:  # oops, couldn't convert to int
            print('\a')
            return False
        if 0 <= value <= max:
            return True
        else:
            print('\a')
            widget.delete(0, END)
            widget.insert(0, max)
            height.config(validate = "key", validatecommand = hcmd)
            width.config(validate = "key", validatecommand = wcmd)
            mines.config(validate = "key", validatecommand = mcmd)
            return False

    hcmd = (root.register(lambda x: validate_entry(x, 9, 24, height)), "%P")
    wcmd = (root.register(lambda x: validate_entry(x, 9, 24, width)), "%P")
    mcmd = (root.register(lambda x: validate_entry(x, 10, min(int(height.get()) * int(width.get()), 400), mines)), "%P")

    hlbl = Label(customDifficulty, state = DISABLED, text = "Height (9-24)")
    hlbl.grid(row = 1, column = 0)
    height = Entry(customDifficulty, state = DISABLED)
    height.grid(row = 1, column = 1)

    wlbl = Label(customDifficulty, state = DISABLED, text = "Width (9-24)")
    wlbl.grid(row = 2, column = 0)
    width = Entry(customDifficulty, state = DISABLED)
    width.grid(row = 2, column = 1)

    mlbl = Label(customDifficulty, state = DISABLED, text = "Mines (10-400)")
    mlbl.grid(row = 3, column = 0)
    mines = Entry(customDifficulty, state = DISABLED)
    mines.grid(row = 3, column = 1)

    def enabler(event):
        hlbl['state'] = NORMAL
        height['state'] = NORMAL
        height.config(validate = "key", validatecommand = hcmd)

        wlbl['state'] = NORMAL
        width['state'] = NORMAL
        width.config(validate = "key", validatecommand = wcmd)

        mlbl['state'] = NORMAL
        mines['state'] = NORMAL
        mines.config(validate = "key", validatecommand = mcmd)

    def disabler(event):
        hlbl['state'] = DISABLED
        height['state'] = DISABLED

        wlbl['state'] = DISABLED
        width['state'] = DISABLED

        mlbl['state'] = DISABLED
        mines['state'] = DISABLED

    bbtn.bind("<Button-1>", lambda x: disabler(x))
    ibtn.bind("<Button-1>", lambda x: disabler(x))
    abtn.bind("<Button-1>", lambda x: disabler(x))
    customBtn.bind("<Button-1>", lambda x: enabler(x))


# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #
# ||||||||||||||||||||||||||||||||||||||||||||||||||| #

def main():
    global x_dim, y_dim, count, F, root, main_list, printable_list, mines, zeroes, revealPerTurn, marked, revealed, game, L, x_var, y_var, tiles, timer, timer_label, stuff, mine_label
    try:
        with open('assets/data', 'rb') as f:
            data = pickle.load(f)
            x_dim, y_dim, count = data['Dimensions']['xdim'], data['Dimensions']['ydim'], data['Dimensions']['mines']

        root = Tk()
        root.title("Minesweeper")
        root.minsize(684, 700)
        root.configure(bg = '#a1a1a1')
        root.iconbitmap('assets/Sprites/logo.ico')

        main_list = [[0 for y in range(y_dim)] for x in range(x_dim)]
        printable_list = [["*" for y in range(y_dim)] for x in range(x_dim)]
        mines, zeroes, revealPerTurn, marked, revealed = [], [], [], [], []

        game = Frame(root, bg = '#000', height = 572, width = 572)
        game.pack(pady = 5)

        stuff = Frame(root, bg = '#a1a1a1', width = 572)
        stuff.pack()

        pyglet.font.add_file("assets/Font/DS-DIGI.TTF")

        timer_label = Label(stuff, text = "0", fg = "white", bg = "#515151", font = "DS-Digital 40", width = 5)
        timer_label.grid(row = 0, column = 0, padx = 30)

        timer = Timer(timer_label)

        mine_label = Label(stuff, text = count, fg = "white", bg = "#515151", font = "DS-Digital 40", width = 5)
        mine_label.grid(row = 0, column = 1, padx = 30)

        with open('assets/data', 'rb') as f:
            data = pickle.load(f)

            data['Stats']['Total'] += 1
            data['Stats']['Percentage'] = f"{(data['Stats']['Win'] * 100) // data['Stats']['Total']}%"
        with open('assets/data', 'wb') as f: pickle.dump(data, f)


        menuMaker()
        minesAdder(x_dim, y_dim, count)
        countAdd()

        for x_var in range(x_dim):
            for y_var in range(y_dim):
                buttonFunc(x_var, y_var)
        tiles = [x for x in game.winfo_children()]
        tiles = list(tiles[i:i + y_dim] for i in range(0, len(tiles), y_dim))

        if [x_dim, y_dim, count] == [5, 5, 0]:
            firstScreen()

        root.bind("<F5>", lambda x: firstScreen())
        root.bind("<F2>", lambda x: restart())
        root.mainloop()
    except (FileExistsError, FileNotFoundError):
        with open("assets/data", "wb") as f:
            data = {
                "Dimensions": { "xdim" : 5, "ydim" : 5, "mines": 0 },
                "Stats"     : { "Total": 0, "Percentage": "0%", "Win": 0 }
            }
            pickle.dump(data, f)
        main()
        
    except ModuleNotFoundError:
        root.destroy()
        main()

if __name__ == '__main__':
    main()
