import pyxel, random

goalstate = list(range(1,9)) + [0]

# A*探索のスコア計算(ゴールまでの距離+終了までのステップ数)
def evalstat(path):
    gval = len(path)
    stat = path[-1]
    # 理想の位置にないパネルの総数
    # hval = sum(1 for i in range(3*3) if stat[i] and stat[i] != i+1)
    # マンハッタン距離の総和
    hval = sum(mdist(i, stat[i]-1) if stat[i] else 0 for i in range(3*3))
    return gval + hval

def sort_openL(openL):
    newL = []
    for path in openL:
        ans = evalstat(path)
        newL.append((ans, path))
    newL.sort(key=lambda x:x[0])
    return [hist for (_, hist) in newL]

def nextmoves(stat):
    zeropos = stat.index(0)
    nextstatL = []
    for panel in range(9):
        if mdist(panel, zeropos) == 1:
            nextstat = stat.copy()
            nextstat[zeropos] = nextstat[panel]
            nextstat[panel] = 0
            nextstatL.append(nextstat)
    return nextstatL

def solver(board):
    print("Auto-solving...")
    openL = [ [board] ]
    doneL = [ ]
    for i in range(10000):
        if not openL: break
        openL = sort_openL(openL)
        path = openL.pop(0)
        stat = path[-1]
        if stat == goalstate:
            print(f"Solution found({i}, ol:{len(openL)}, dl:{len(doneL)}){len(path)-1} steps!")
            # print(path)
            return [list(s) for s in path[1:]]
        doneL.append(stat)
        newstatL = nextmoves(stat)
        for newstat in newstatL:
            if newstat not in doneL:
                openL.append(path + [newstat])

    print("No solution found.")
    return None

def mdist(pos1, pos2):
        x1, y1 = pos1 % 3, pos1 // 3
        x2, y2 = pos2 % 3, pos2 // 3
        return abs(x1-x2) + abs(y1-y2)

def invnum(board):
        return sum(1 for i in range(9) for j in range(i)
                   if board[j] > board[i])

class App:
    def __init__(self):
        pyxel.init(60, 70, "8 Puzzle")
        self.new_game()
        self.gridsize = 3
        self.tilesize = 20
        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def new_game(self):
        for _ in range(10):
            self.board = list(range(9))
            random.shuffle(self.board)
            # lower = list(range(3,9)) + [0]
            # random.shuffle(lower)
            # self.board = list(range(1,3)) + lower
            self.board = [1,2,8,3,0,7,6,4,5]
            inum = invnum(self.board)
            print(inum, inum%2, self.board)
            if inum % 2 == 0:
                break
        self.steps = 0
        print(f"New game: {self.board}")

    def update(self):
        if pyxel.btnp(pyxel.KEY_S):
            self.solution = solver(self.board)
        if pyxel.btnp(pyxel.KEY_SPACE):
            self.show_step()
        if pyxel.btnp(pyxel.KEY_N):
            self.new_game()
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            mx, my = pyxel.mouse_x, pyxel.mouse_y
            cx, cy = mx // self.tilesize, my // self.tilesize
            cpos = cy * self.gridsize + cx

            if 0 <= cpos <= 8:
                print(mx, my, cx, cy, cpos)
                self.movetile(cpos)
    
    def movetile(self, cpos):
        zeropos = self.board.index(0)
        # print(f"zeropos: {zeropos}, mdist: {mdist}")
        if mdist(cpos, zeropos) == 1:
            self.board[zeropos] = self.board[cpos]
            self.board[cpos] = 0
            self.steps += 1
            print(invnum(self.board), self.board)

    def show_step(self):
        if self.solution:
            self.board = self.solution.pop(0)
            self.steps += 1
            print(f"{self.steps}: {invnum(self.board)}, {self.board}")

    def draw(self):
        pyxel.cls(0)
        for i,v in enumerate(self.board):
            x = i % self.gridsize * self.tilesize
            y = i // self.gridsize * self.tilesize
            if v:
                pyxel.rect(x, y, self.tilesize-1, self.tilesize-1, 6)
                pyxel.text(x+8, y+8, str(v), 1)
        if self.board == goalstate:
            pyxel.text(5, 60, f"CLEAR! {self.steps} steps", 14)
        else:
            pyxel.text(5, 60, f"{self.steps} steps", 11)
App()