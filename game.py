# 棋盘构造：
# 9*9格子
# 2人每方10块板子，3人每方6块板子，4人每方5块板子
# 格子大小（内围）：50*50像素，黑线宽5像素，板子5*105像素
# 选择棋子时只要点到格子中即可，选择板子和放置板子容错i和j都为+-20
# 黄方板子位置 (i, 605~710) i ∈ (85~625)（105, 105+55*9+5=605）

import pygame
from pygame import Vector2
import time
import copy


# 环境配置
WIDTH = 710
HEIGHT = 710
FPS = 60
Menu_xborder=[210, 500]
Menu_yborder=[[250, 320, 390], [280, 350, 420]]

# 初始化
pygame.font.init()
# pygame.mixer.init()
clock = pygame.time.Clock()
gameScreen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("步步围营")
TITLE_FONT = pygame.font.SysFont('simhei', 50)
MENU_FONT = pygame.font.SysFont('simhei', 30)

# 导入图片
BACKGROUND = pygame.image.load("images/background.png")
PINK = pygame.image.load("images/pink.png")
GREEN = pygame.image.load("images/green.png")
BLUE = pygame.image.load("images/blue.png")
YELLOW = pygame.image.load("images/yellow.png")
PINKBACK = pygame.image.load("images/pinkback.png")
GREENBACK = pygame.image.load("images/greenback.png")
BLUEBACK = pygame.image.load("images/blueback.png")
YELLOWBACK = pygame.image.load("images/yellowback.png")
PIECE = [YELLOW, PINK, BLUE, GREEN, YELLOWBACK, PINKBACK, BLUEBACK, GREENBACK]
BOARD_ = pygame.image.load("images/board_.png")        #横
BOARDl= pygame.image.load("images/boardl.png")         #竖
BOARD_BACK = pygame.image.load("images/board_back.png")
BOARDlBACK = pygame.image.load("images/boardlback.png")
BOARD = [BOARD_, BOARDl, BOARD_BACK, BOARDlBACK]


class Stack:
    def __init__(self):
        self.items = []

    def is_empty(self):
        return self.items == []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self.items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self.items[-1]

    def size(self):
        return len(self.items)
    
    def print_stack(self):
        for i in range(len(self.items)):
            print(self.items[i])


class BoardGame:
    def __init__(self):
        self.piece = []
        self.piece_state = []
        self.board = []
        self.board_moved = []
        self.board_state = []
        self.puzzle_state = []
        self.dirs=[(1,0), (-1,0), (0,1), (0,-1)]       #当前位置四个方向的偏移量
        self.mode = 4


    def init_game(self):
        '''
        初始化一局游戏
        '''
        # 四方棋子[所处格子(i, j）, ctrl]
        # ctrl=0：未点击，ctrl=1：被点击
        self.piece = [[0, 4, 0], [8, 4, 0], [4, 0, 0], [4, 8, 0]]

        # 记录每个棋子在全局的哪个位置
        self.piece_state = [[0 for i in range(9)] for j in range(9)]
        # 记录每方板子状态
        # 一方：[[一个板所处格点(i, j), ctrl]x10块板子]，默认上下2方，板子初始化都为竖(ctrl=1)；(i, j)∈(11*11)；ctrl=0：横；ctrl=1：竖；ctrl=2：横被点；ctrl=3：竖被点
        self.board = [[[Vector2(105+i*55, 0), 1] for i in range(10)], [[Vector2(105+i*55, 605), 1] for i in range(10)]]
        # 记录每个板子是否被移动，每个板子只能移动一次，ctrl=0：未移动；ctrl=1：已移动
        self.board_moved = [[0 for i in range(10)] for j in range(2)]
        # 81个格子，每个格子的上下左右，无板=0，有板=1
        self.board_state = [[[0, 0, 0, 0] for i in range(9)] for j in range(9)]    
        self.puzzle_state = [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3, 0, 3], 
            [3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3], 
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
        ]               # 0:未探索，1:已探索，2: 有板子，3: 边缘或空隙（初始已知的不可达位置）


        for i in range(self.mode):
            self.piece_state[self.piece[i][0]][self.piece[i][1]] = i+1

        if self.mode == 3:
            # 每方6块板子
            self.board[0] = self.board[0][:6]
            self.board[1] = self.board[1][:6]
            self.board.append([[Vector2(0, 105+i*55), 0] for i in range(6)])
            self.board_moved[0] = self.board_moved[0][:6]
            self.board_moved[1] = self.board_moved[1][:6]
            self.board_moved.append([0 for i in range(6)])
        elif self.mode == 4:
            # 每方5块板子
            self.board[0] = self.board[0][:5]
            self.board[1] = self.board[1][:5]
            self.board.append([[Vector2(0, 105+i*55), 0] for i in range(5)])
            self.board.append([[Vector2(605, 105+i*55), 0] for i in range(5)])
            self.board_moved[0] = self.board_moved[0][:5]
            self.board_moved[1] = self.board_moved[1][:5]
            self.board_moved.append([0 for i in range(5)])
            self.board_moved.append([0 for i in range(5)])


    def piece_grid2pos(self, ij):        #给在(i, j)个格子上，求棋子左上角应处的坐标（ij[0]=i，ij[j]=j）
        pos_x = ij[1] * 55 + 110
        pos_y = ij[0] * 55 + 110
        return Vector2(pos_x, pos_y)
    

    def mouse_pos2grid(self, xy):        #给鼠标坐标xy[0]=x，xy[1]=y，求鼠标在(i, j)个格子上
        i = int((xy[1] - 108) / 55)
        j = int((xy[0] - 108) / 55)
        ij = [i, j]
        return ij


    def change_turn(self, turn_flag):
        #轮换逻辑
        if turn_flag == 0:
            turn_flag = 1
        elif turn_flag == 1:
            if self.mode == 2:
                turn_flag =  0
            else:
                turn_flag = 2
        elif turn_flag == 2:
            if self.mode == 3:
                turn_flag = 0
            elif self.mode == 4:
                turn_flag = 3
        elif turn_flag == 3:
            if self.mode == 4:
                turn_flag = 0
        return turn_flag
    

    def maze_solver(self, start, end, start_ctrl):    # start_ctrl=0/1，控制start的列/行和end比，如黄棋(0)的ctrl是0，列到达end=8即可
        stack = Stack()
        start_puzzle_pose = 2*start[0]+1, 2*start[1]+1          # 2n+1
        puzzle_plate = copy.deepcopy(self.puzzle_state)
        puzzle_plate[start_puzzle_pose[0]][start_puzzle_pose[1]] = 1
        stack.push((start_puzzle_pose, 0))             #入口和方向0的序对入栈
        while not stack.is_empty():      #走不通时回退
            pos, nxt = stack.pop()           #取栈顶及其检查方向
            for i in range(nxt, 4):     #依次检查未检查方向，算出下一位置
                nextp_board = pos[0] + self.dirs[i][0], pos[1] + self.dirs[i][1]
                nextp_piece = pos[0] + 2*self.dirs[i][0], pos[1] + 2*self.dirs[i][1]
                if nextp_piece[start_ctrl] == 2*end+1:
                    print("next.  ", nextp_piece)
                    return True
                if puzzle_plate[nextp_board[0]][nextp_board[1]] == 0:    #遇到未探索的新位置
                    stack.push((pos, i+1))      #原位置和下一方向入栈
                    puzzle_plate[nextp_piece[0]][nextp_piece[1]] = 1
                    puzzle_plate[nextp_board[0]][nextp_board[1]] = 1
                    # print(self.puzzle_state)
                    stack.push((nextp_piece, 0))      #新位置入栈
                    break                   #退出内层循环，下次迭代将以新栈顶作为当前位置继续
        return False
            
    
    def update_piece_state(self, id, ori_ij, new_ij):
        self.piece_state[ori_ij[0]][ori_ij[1]] = 0
        self.piece_state[new_ij[0]][new_ij[1]] = id+1


    def drawGame(self, win):
        gameScreen.blit(BACKGROUND, (0,0))
        if win >= 0:
            if win == 0:
                winner = "黄"
            elif win == 1:
                winner = "粉"
            elif win == 2:
                winner = "蓝"
            elif win == 3:
                winner = "绿"
            gameScreen.blit(TITLE_FONT.render(winner + "方获胜！" , -1, (255,0,0)), (170,230))
            pygame.display.update()
            time.sleep(3)
            return -1
        else:        
            # 画棋子
            for m in range(self.mode):
                if self.piece[m][2] == 0:
                    gameScreen.blit(PIECE[m], self.piece_grid2pos(self.piece[m]))
                elif self.piece[m][2] == 1:
                    gameScreen.blit(PIECE[m+4], self.piece_grid2pos(self.piece[m]))
            # 画板子
            if self.mode == 2:
                for i in range(10):
                    gameScreen.blit(BOARD[self.board[0][i][1]], self.board[0][i][0])
                    gameScreen.blit(BOARD[self.board[1][i][1]], self.board[1][i][0])
            elif self.mode == 3:
                for i in range(6):
                    gameScreen.blit(BOARD[self.board[0][i][1]], self.board[0][i][0])
                    gameScreen.blit(BOARD[self.board[1][i][1]], self.board[1][i][0])
                    gameScreen.blit(BOARD[self.board[2][i][1]], self.board[2][i][0])
            elif self.mode == 4:
                for i in range(5):
                    gameScreen.blit(BOARD[self.board[0][i][1]], self.board[0][i][0])
                    gameScreen.blit(BOARD[self.board[1][i][1]], self.board[1][i][0])
                    gameScreen.blit(BOARD[self.board[2][i][1]], self.board[2][i][0])
                    gameScreen.blit(BOARD[self.board[3][i][1]], self.board[3][i][0])
            pygame.display.update()
            return 1

    
    def ShowMenu(self):
        gameScreen.fill((255,255,255))
        gameScreen.blit(TITLE_FONT.render("步步围营", -1, (0,0,0)), (100,100))
        gameScreen.blit(MENU_FONT.render("双人", -1, (0,0,0)), (210, Menu_yborder[0][0]))
        gameScreen.blit(MENU_FONT.render("三人", -1, (0,0,0)), (210, Menu_yborder[0][1]))
        gameScreen.blit(MENU_FONT.render("四人", -1, (0,0,0)), (210, Menu_yborder[0][2]))
        pygame.display.update()


    def gameloop(self):
        selected_board_ind = 100
        turn_flag = 0           # =0：该黄，=1该粉，=2该蓝，=3该绿
        piece_board = -1        # =0为棋子被点击，=1为板被点击
        win = -1                # =0：黄胜，=1：粉胜，=2：蓝胜，=3：绿胜
        run = -1                # 游戏状态，=-1：菜单，=1：游戏
        while True:
            piece_alive_flag = 1    # 棋子是否被堵死
            #print(win)
            if run == -1:
                win = -1
                turn_flag = 0

                # 菜单
                self.ShowMenu()
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        m_pos = pygame.mouse.get_pos()
                        if(m_pos[0] >= Menu_xborder[0] and m_pos[0] <= Menu_xborder[1]):
                            if(m_pos[1] >= Menu_yborder[0][0] and m_pos[1] <= Menu_yborder[1][0]):      # 双人
                                self.mode = 2
                                run = 1
                                self.init_game()
                            elif(m_pos[1] >= Menu_yborder[0][1] and m_pos[1] <= Menu_yborder[1][1]):      # 三人
                                self.mode = 3
                                run = 1
                                self.init_game()
                            elif(m_pos[1] >= Menu_yborder[0][2] and m_pos[1] <= Menu_yborder[1][2]):      # 四人
                                self.mode = 4
                                run = 1
                                self.init_game()
            elif run == 1:
                run = self.drawGame(win)
                m_pos = pygame.mouse.get_pos()
                m_ij = self.mouse_pos2grid(m_pos)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if piece_board == -1:       # 没有棋子/板子被选中
                            # 选中棋子
                            if m_ij[0] == self.piece[turn_flag][0] and m_ij[1] == self.piece[turn_flag][1]:
                                self.piece[turn_flag][2] = 1                 #棋子状态改为被点击
                                piece_board = 0
                            # 选到哪块（ind）板（黄）
                            elif turn_flag == 0 and m_pos[0] >= 85 and m_pos[1] >= 0 and m_pos[1] < 105:
                                if (self.mode == 2 and m_pos[0] < 625) or (self.mode == 3 and m_pos[0] < 405) or (self.mode == 4 and m_pos[0] < 350):
                                    selected_board_ind = int((m_pos[0] - 85) / 55)
                                    if self.board_moved[turn_flag][selected_board_ind] == 0:
                                        self.board[turn_flag][selected_board_ind][1] = 3   # 竖被点
                                        piece_board = 1
                            # 选到哪块板（粉）
                            elif turn_flag == 1 and m_pos[0] >= 85 and m_pos[1] >= 605 and m_pos[1] < 710:
                                if (self.mode == 2 and m_pos[0] < 625) or (self.mode == 3 and m_pos[0] < 405) or (self.mode == 4 and m_pos[0] < 350):
                                    selected_board_ind = int((m_pos[0] - 85) / 55)
                                    if self.board_moved[turn_flag][selected_board_ind] == 0:
                                        self.board[turn_flag][selected_board_ind][1] = 3   # 竖被点
                                        piece_board = 1
                            # 选到哪块板（蓝）
                            elif turn_flag == 2 and m_pos[0] >= 0 and m_pos[0] < 105 and m_pos[1] >= 85:
                                if (self.mode == 2 and m_pos[1] < 625) or (self.mode == 3 and m_pos[1] < 405) or (self.mode == 4 and m_pos[1] < 350):
                                    selected_board_ind = int((m_pos[1] - 85) / 55)
                                    if self.board_moved[turn_flag][selected_board_ind] == 0:
                                        self.board[turn_flag][selected_board_ind][1] = 2   # 横被点
                                        piece_board = 1
                            # 选到哪块板（绿）
                            elif turn_flag == 3 and m_pos[0] >= 605 and m_pos[0] < 710 and m_pos[1] >= 85:
                                if (self.mode == 2 and m_pos[1] < 625) or (self.mode == 3 and m_pos[1] < 450) or (self.mode == 4 and m_pos[1] < 350):
                                    selected_board_ind = int((m_pos[1] - 85) / 55)
                                    if self.board_moved[turn_flag][selected_board_ind] == 0:
                                        self.board[turn_flag][selected_board_ind][1] = 2   # 横被点
                                        piece_board = 1
                            else:
                                continue

                        elif piece_board == 0:      # 已选中棋子并点击放置
                            # 点前/后/左/右格子 -> 判断是否可走 -> 走 -> 转state1
                            if m_ij[0] == self.piece[turn_flag][0]-1 and m_ij[1] == self.piece[turn_flag][1]:     #上
                                if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]][0] == 0 and self.piece[turn_flag][0] != 0 and self.piece_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]] == 0:           #（piece[turn_flag][0]，piece[turn_flag][1]）格上没板 + 棋子不在棋盘最上方 + 棋子上方格子没棋子
                                    #放下棋子
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][0] -= 1
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]-2 and m_ij[1] == self.piece[turn_flag][1]:              # 上2格
                                if self.piece_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]] != 0 and self.piece[turn_flag][0]-1 != 0 and self.board_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]][0] == 0:     # 上方有棋+上一格不是0+上格的上方没板 -> 跳过去
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][0] -= 2
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]-1 and m_ij[1] == self.piece[turn_flag][1]-1:              # 点到上左
                                if self.piece_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]] != 0:     # 上方有棋
                                    if self.board_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]][0] != 0 and self.board_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]][2] == 0:           # 上格的上方有板但左边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] -= 1
                                        self.piece[turn_flag][1] -= 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                                elif self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1] != 0:     # 左方有棋
                                    if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1][2] != 0 and self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1][0] == 0:           # 左格的左边有板但上边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] -= 1
                                        self.piece[turn_flag][1] -= 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]-1 and m_ij[1] == self.piece[turn_flag][1]+1:              # 点到上右
                                if self.piece_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]] != 0:     # 上方有棋
                                    if self.board_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]][0] != 0 and self.board_state[self.piece[turn_flag][0]-1][self.piece[turn_flag][1]][3] == 0:           # 上格的上方有板但右边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] -= 1
                                        self.piece[turn_flag][1] += 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                                elif self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1] != 0:     # 右方有棋
                                    if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1][3] != 0 and self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1][0] == 0:           # 右格的右边有板但上边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] -= 1
                                        self.piece[turn_flag][1] += 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]+1 and m_ij[1] == self.piece[turn_flag][1]:     #下
                                if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]][1] == 0 and self.piece[turn_flag][0] != 8 and self.piece_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]] == 0:           #（piece[turn_flag][0]，piece[turn_flag][1]）格下没板，且棋子不在棋盘最下方，且棋子下方格子没棋子
                                    #放下棋子
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][0] += 1
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]+2 and m_ij[1] == self.piece[turn_flag][1]:              # 下2格
                                if self.piece_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]] != 0 and self.piece[turn_flag][0]+1 != 8 and self.board_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]][1] == 0:     # 下方有棋+下一格不是8+下格的下方没板 -> 跳过去
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][0] += 2
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]+1 and m_ij[1] == self.piece[turn_flag][1]-1:              # 点到下左
                                if self.piece_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]] != 0:     # 下方有棋
                                    if self.board_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]][1] != 0 and self.board_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]][2] == 0:           # 下格的下方有板但左边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] += 1
                                        self.piece[turn_flag][1] -= 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                                elif self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1] != 0:     # 左方有棋
                                    if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1][2] != 0 and self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1][1] == 0:           # 左格的左边有板但下边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] -= 1
                                        self.piece[turn_flag][1] += 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0]+1 and m_ij[1] == self.piece[turn_flag][1]+1:              # 点到下右
                                if self.piece_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]] != 0:     # 下方有棋
                                    if self.board_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]][1] != 0 and self.board_state[self.piece[turn_flag][0]+1][self.piece[turn_flag][1]][3] == 0:           # 下格的下方有板但右边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] += 1
                                        self.piece[turn_flag][1] += 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                                elif self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1] != 0:     # 右方有棋
                                    if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1][3] != 0 and self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1][1] == 0:           # 右格的右边有板但下边没板
                                        ori_ij = self.piece[turn_flag][:2].copy()
                                        self.piece[turn_flag][0] += 1
                                        self.piece[turn_flag][1] += 1
                                        self.piece[turn_flag][2] = 0
                                        self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                        turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                        piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0] and m_ij[1] == self.piece[turn_flag][1]-1:     #左
                                if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]][2] == 0 and self.piece[turn_flag][1] != 0 and self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1] == 0:           #（piece[turn_flag][0]，piece[turn_flag][1]）格左没板，且棋子不在棋盘最左边，且棋子左边格子没棋子
                                    #放下棋子
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][1] -= 1
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0] and m_ij[1] == self.piece[turn_flag][1]-2:     # 左2格
                                if self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1] != 0 and self.piece[turn_flag][1]-1 != 0 and self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]-1][2] == 0:     # 左边有棋+左边一格不是0+左边格的左边没板 -> 跳过去
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][1] -= 2
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1

                            elif m_ij[0] == self.piece[turn_flag][0] and m_ij[1] == self.piece[turn_flag][1]+1:     #右
                                if self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]][3] == 0  and self.piece[turn_flag][1] != 8 and self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1] == 0:               #（piece[turn_flag][0]，piece[turn_flag][1]）格右没板，且棋子不在棋盘最右边，且棋子右边格子没棋子
                                    #放下棋子
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][1] += 1
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                            elif m_ij[0] == self.piece[turn_flag][0] and m_ij[1] == self.piece[turn_flag][1]+2:     # 右2格
                                if self.piece_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1] != 0 and self.piece[turn_flag][1]+1 != 8 and self.board_state[self.piece[turn_flag][0]][self.piece[turn_flag][1]+1][3] == 0:     # 右边有棋+右边一格不是8+右边格的右边没板 -> 跳过去
                                    ori_ij = self.piece[turn_flag][:2].copy()
                                    self.piece[turn_flag][1] += 2
                                    self.piece[turn_flag][2] = 0
                                    self.update_piece_state(turn_flag, ori_ij, self.piece[turn_flag])
                                    turn_flag = self.change_turn(turn_flag)       # 换下一方turn_flag
                                    piece_board = -1
                                    
                            else:                   #点到别处，取消选中（不改变turn）
                                self.piece[turn_flag][2] = 0
                                piece_board = -1
                
                        elif piece_board == 1:      # 已选中板子并点击放置
                            j_ind = int((m_pos[0] - 80) / 55)
                            i_ind = int((m_pos[1] - 80) / 55)                #距离m_pos最近的十字交叉点坐标
                            
                            if m_pos[0] > 160-25 and m_pos[0] < 550+25 and m_pos[1] > 105-25 and m_pos[1] < 605+25 and self.board[turn_flag][selected_board_ind][1] == 2:                    #横
                                # 假设能在这里放
                                self.puzzle_state[2*i_ind][2*j_ind-1] = 2       # 都是2n-1+1，i为[2*i_ind-1] j为[2*j_ind-1+-1]再统一+1
                                self.puzzle_state[2*i_ind][2*j_ind+1] = 2
                                for piece_idx in range(self.mode):          # 判断放置这块板子会不会把某方的棋子堵死
                                    piece_place = self.piece[piece_idx][:2]
                                    print("piece id: ", piece_idx, "piece place: ", piece_place)
                                    if self.maze_solver(piece_place, 8-8*(piece_idx%2), piece_idx//2) == False:     # 会堵死
                                        piece_alive_flag = 0
                                        # 还原puzzle_state
                                        self.puzzle_state[2*i_ind][2*j_ind-1] = 0
                                        self.puzzle_state[2*i_ind][2*j_ind+1] = 0
                                        break

                                # 更新board_state（1,2 -> 01下 02下 11上 12上）
                                if i_ind == 0 or i_ind == 9 or piece_alive_flag == 0:      # 板子不能放在边框，不能堵死任意一方棋子
                                    continue
                                else:
                                    if self.board_state[i_ind][j_ind-1][0] == 1 or self.board_state[i_ind][j_ind][0] == 1 or (self.board_state[i_ind-1][j_ind-1][3] == 1 and self.board_state[i_ind][j_ind-1][3] == 1):         #板子不能重叠，不能交叉
                                        continue
                                    else:
                                        self.board_state[i_ind-1][j_ind-1][1] = 1
                                        self.board_state[i_ind-1][j_ind][1] = 1
                                        self.board_state[i_ind][j_ind-1][0] = 1
                                        self.board_state[i_ind][j_ind][0] = 1

                                        self.puzzle_state[2*i_ind][2*j_ind-1] = 2       # 都是2n-1+1，i为[2*i_ind-1] j为[2*j_ind-1+-1]再统一+1
                                        self.puzzle_state[2*i_ind][2*j_ind+1] = 2
                                #放下板
                                self.board[turn_flag][selected_board_ind][0] = Vector2(j_ind*55+55, i_ind*55+105)
                                self.board[turn_flag][selected_board_ind][1] = 0     
                                #更新状态
                                piece_board = -1
                                self.board_moved[turn_flag][selected_board_ind] = 1
                                turn_flag = self.change_turn(turn_flag)
                            elif m_pos[0] > 105-25 and m_pos[0] < 605+25 and m_pos[1] > 160-25 and m_pos[1] < 550+25 and self.board[turn_flag][selected_board_ind][1] == 3 :                  #竖
                                #更新board_state（1,2 -> 01下 02下 11上 12上）
                                if j_ind == 0 or j_ind == 9:# or piece_alive_flag == 0:
                                    continue
                                else:
                                    if self.board_state[i_ind-1][j_ind][2] == 1 or self.board_state[i_ind][j_ind][2] == 1 or (self.board_state[i_ind-1][j_ind-1][1] == 1 and self.board_state[i_ind-1][j_ind][1] == 1):         #板子不能重叠，不能交叉
                                        continue
                                    else:
                                        self.board_state[i_ind-1][j_ind-1][3] = 1
                                        self.board_state[i_ind-1][j_ind][2] = 1
                                        self.board_state[i_ind][j_ind-1][3] = 1
                                        self.board_state[i_ind][j_ind][2] = 1
                                        
                                        self.puzzle_state[2*i_ind-1][2*j_ind] = 2
                                        self.puzzle_state[2*i_ind+1][2*j_ind] = 2
                                #放下板
                                self.board[turn_flag][selected_board_ind][0] = Vector2(j_ind*55+105, i_ind*55+55)
                                self.board[turn_flag][selected_board_ind][1] = 1
                                #更新状态
                                piece_board = -1
                                self.board_moved[turn_flag][selected_board_ind] = 1
                                turn_flag = self.change_turn(turn_flag)
                            else:                               # 点到不在能放置板子的范围内：板子归还原处
                                if turn_flag == 0:
                                    self.board[turn_flag][selected_board_ind][0] = Vector2(selected_board_ind*55+105, 0)
                                    self.board[turn_flag][selected_board_ind][1] = 1
                                elif turn_flag == 1:
                                    self.board[turn_flag][selected_board_ind][0] = Vector2(selected_board_ind*55+105, 605)
                                    self.board[turn_flag][selected_board_ind][1] = 1
                                elif turn_flag == 2:
                                    self.board[turn_flag][selected_board_ind][0] = Vector2(0, selected_board_ind*55+105)
                                    self.board[turn_flag][selected_board_ind][1] = 0
                                elif turn_flag == 3:
                                    self.board[turn_flag][selected_board_ind][0] = Vector2(605, selected_board_ind*55+105)
                                    self.board[turn_flag][selected_board_ind][1] = 0

                                piece_board = -1
                                piece_alive_flag = 1
                                

                    #键盘控制：鼠标选中板时，按空格键切换横/竖
                    if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                        if piece_board == 1:
                            if self.board[turn_flag][selected_board_ind][1] == 2:
                                self.board[turn_flag][selected_board_ind][1] = 3
                            elif self.board[turn_flag][selected_board_ind][1] == 3:
                                self.board[turn_flag][selected_board_ind][1] = 2
                        
                
                #board单独用：跟随鼠标
                if piece_board == 1:
                    if self.board[turn_flag][selected_board_ind][1] == 2:
                        self.board[turn_flag][selected_board_ind][0] = Vector2(m_pos[0]-52, m_pos[1]-2)
                    elif self.board[turn_flag][selected_board_ind][1] == 3:
                        self.board[turn_flag][selected_board_ind][0] = Vector2(m_pos[0]-2, m_pos[1]-52)
                

                #获胜条件
                if self.piece[0][0] == 8:
                    win = 0
                elif self.piece[1][0] == 0:
                    win = 1
                elif self.piece[2][1] == 8:
                    win = 2
                elif self.piece[3][1] == 0:
                    win = 3

            clock.tick(FPS)


if __name__ == "__main__":
    game = BoardGame()
    game.gameloop()
