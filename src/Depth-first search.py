# 深さ優先探索
import pyxel, random

goalstate = list(range(1,9)) + [0]

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
    for i in range(1000):
        path = openL.pop() # 深さ優先探索では、リストの末尾から取り出す
        stat = path[-1]
        if stat == goalstate:
            print(f"Solution found({i}) in {len(path)-1} steps!")
            print(path)
            return path[1:]
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
            # self.board = list(range(9))
            # random.shuffle(self.board)
            lower = list(range(4,9)) + [0]
            random.shuffle(lower)
            self.board = [1,2,3] + lower
            # self.board = [1,2,3,4,5,6,0,7,8]
            inum = invnum(self.board)
            # print(inum, inum%2, self.board)
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
            mx, my = pyxel.mouse_x, pyxel.mouse_y # クリックされた時点のマウス座標を取得
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