''' Minesweeper '''

from random import choice
import os

try:
    from bext import fg, bg

except ModuleNotFoundError:
    # If bext is not installed, create blank functions
    def fg(_):
        pass
    def bg(_):
        pass

MESSAGE = r'''                                                                                    
  _    _    __                                                                                  
 / \  / \  /  \  __  _     _____    ______  _    _    _____     _____    _____    _____    _ __
|   \/   | \__/ |  |/ \   /  __ \  /  ___/ | |  | |  /  __ \   /  __ \  |  _  \  /  __ \  | |  \
|  /\/\  | |  | |      | |   ____| \___  \ | \/\/ | |   ____| |   ____| |   __/ |   ____| |  /\_|
|_/    \_| |__| |__/\__|  \______| /_____/  \_/\_/   \______|  \______| |  |     \______| |_|
                                                                        |__|                    '''
OPTIONS = {'1': 'Easy', '2': 'Medium', '3': 'Hard', '4': 'Random'}
NUMCOLORS = {1: 'white', 2: 'cyan', 3: 'magenta', 4: 'green', 5: 'blue', 6: 'red', 7: 'black', 8: 'white'}
DIFF_DATA = {
    'Easy': (10, 30),
    'Medium': (10, 40),
    'Hard': (10, 50)
}

def avg_len(iterable):
    ''' Returns the average length of the items in the argument '''
    lens = []
    for i in iterable:
        lens.append(len(i))
    return sum(lens) // len(lens)

def print_matrix(matrix):
    ''' Print matrix '''
    for y in matrix:
        for x in y:
            print(x, end='')
        print()
    # Reset font colors
    bg('reset')
    fg('reset')

def won():
    ''' Check if all cells have been cleared except for the mines '''
    for y in matrix:
        for x in y:
            if (not x.dug) and (not x.mine):
                return False
    return True

class Cell:
    ''' Class for holding cell attributes '''
    
    def __init__(self, x, y):
        ''' Create cell instance '''
        self.index = (x, y)
        self.mine = self.dug = self.lost = self.flagged = False

    def init_touching(self):
        ''' Find neighboring cells '''
        x, y = self.index
        self.neighbors = []

        for plusy in range(-1, 2):
            for plusx in range(-1, 2):
                if plusx or plusy:
                    try:
                        newx, newy = x + plusx, y + plusy
                        if newx >= 0 and newy >= 0:
                            self.neighbors.append(matrix[newy][newx])
                    except IndexError:
                        pass

    def dig(self):
        ''' Dig cell '''
        self.dug = True
        if self.mine:
            os.system(command)
            print('You hit a mine!')
            for y in matrix:
                for x in y:
                    x.lost = True
            print_matrix(matrix)
            while True:
                pass

        for n in self.neighbors:
            if (not n.dug) and (not n.mine):
                n.dig()

    def __str__(self):
        ''' Return what the cell would look like on the screen '''
        if self.dug:
            bg('yellow')
            mines = 0
            for n in self.neighbors:
                if n.mine:
                    mines += 1
        else:
            bg('green')
            mines = 0

        if not mines:
            mines = ' '
        else:
            fg(NUMCOLORS[mines])
        
        if self.mine and self.lost:
            bg('green')
            fg('red')
            mines = '!'
        if self.flagged:
            bg('red')
            fg('black')
            mines = 'P'

        return str(mines) + ' '

print(MESSAGE)

colors = ('green', 'yellow', 'red', 'cyan')
length = avg_len(MESSAGE.split('\n'))
prompt = 'Enter difficulty: '

# Draw options
print('Select difficulty level'.center(length))
for c, o in zip(colors, OPTIONS.items()):
    fg(c)
    text = f'{o[0]}. {o[1]}'
    print(text.center(length))
    fg('reset')

while True:
    try:
        pre = (length / 1.8).__floor__()
        level = input(prompt.rjust(pre))
        level = OPTIONS[level]
    except (KeyboardInterrupt, EOFError, KeyError):
        prompt = ''
        continue
    break

if level == 'Random':
    level = choice(list(DIFF_DATA.keys()))

edge, mines = DIFF_DATA[level]

matrix = list([0] * edge for _ in range(edge))
for y in range(edge):
    for x in range(edge):
        matrix[y][x] = Cell(x, y)

for _ in range(mines):
    while True:
        y = choice(range(0, edge))
        x = choice(range(0, edge))
        if not matrix[y][x].mine:
            matrix[y][x].mine = True
            break
for y in matrix:
    for x in y:
        x.init_touching()

if os.name == 'nt':
    command = 'cls'
else:
    command = 'clear'

while True:
    os.system(command)
    print_matrix(matrix)
    if won():
        print('You won!')
        while True:
            pass

    while True:
        try:
            move = input('Enter move in form XXYYF: ')
            if len(move) < 4:
                raise IndexError
            # Read move
            x = int(move[:2]) - 1
            y = int(move[2:4]) - 1
            flag = len(move) > 4
            matrix[y][x] # Check if index exists
        except (KeyboardInterrupt, EOFError, IndexError) as e:
            continue
        break
    if flag:
        matrix[y][x].flagged = True
    else:
        matrix[y][x].dig()
