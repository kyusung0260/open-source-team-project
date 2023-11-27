import random
import minimax
import math
import pygame
import time
import csv
import pandas as pd
import board_status as bs
pygame.init()

board = [[0]*4 for _ in range(4)]

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 600
background = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
font = pygame.font.SysFont("cambria",20)
pygame.display.set_caption("Rubik's Flip")

# 폰트 종류
# fonts = pygame.font.get_fonts()
# print(fonts)

# colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (128, 128, 128)
yellow = (255, 255, 0)
red = (255, 0, 0)
blue = (0, 0, 255)
green = (0, 255, 0)

color = -1                  # player 가 선택한 color 정보
selected_tray = (-1, -1)    # 선택된 tray
state = 10                  # 현재 step
player = False              # False 가 Player1 True 가 Player2
ai_mode = False
ai_turn = False
record_mode = True
record_list = []

class Tile:
    global red, blue, yellow, white
    def __init__(self,player ):
        self.player = player
    def put_tile(self, tray_type_, color_type):
        if tray_type_ == color_type:
            self.type = 0
            self.player = player
        else:
            self.type = 1
    def get_tile_color(self, tray_type_):
        if tray_type_ == self.type:
            if self.player == 0:
                return 1
            else:
                return 3
        else:
            if self.player == 0:
                return 2
            else:
                return 4

TRAY_SIZE = SCREEN_HEIGHT / 6




def get_board_properties(i, j):
    return (i+j) % 2

# 새로운 타일 생성
player1_tile = []
player2_tile = []

def tile_reset():
    global player1_tile, player2_tile
    player2_tile = []
    player1_tile = []
    for _ in range(8):
        new_obj = Tile(0)
        player1_tile.append(new_obj)
    for _ in range(8):
        new_obj = Tile(1)
        player2_tile.append(new_obj)
tile_reset()


def ai_move(player):
    global board
    if is_opening():
        opening_move()
    else:
        color_board = board_to_cboard(board) #
        if player:
            color_board = ai_only_player1(color_board)

        alpha_value = -math.inf
        beta_value = math.inf

        start_time = time.time()

        #첫 번째 검사
        depth = 3
        best_val, return_board = minimax.alphabeta(color_board,depth,alpha_value,beta_value,False)
        print("depth : ", depth,"evaluation :",best_val)
        depth = 2
        tmp_val, tmp_board = minimax.alphabeta(color_board,depth,alpha_value,beta_value,False)
        print("depth : ", depth,"evaluation :",tmp_val)
        if depth %  2 == 0:
            tmp_val = -tmp_val

        if best_val < tmp_val:
            return_board = tmp_board
            best_val = tmp_val

        end_time = time.time()
        elapsed_time = end_time - start_time
        print("알고리즘 경과 시간 = ", round(elapsed_time, 2))
        print("best val =", best_val)

        if player:
            return_board = ai_only_player1(return_board)
        move_board_from_return(return_board, player)


def turn(board):
    turn = 0
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                turn += 1
    return turn


def is_opening():
    global board
    for i in range(4):
        for j in range(4):
            if board[i][j] != 0:
                return False
    return True

def opening_move():
    global player1_tile, board
    # ###player1 으로 시작할 경우만 가능한 move
    random_num = random.randint(0,3)
    rand_color = random.randint(0,1)
    color_ = (red, blue)
    pos = ((0, 0), (0, 3),(3, 0),(3, 3))
    put_tile_pos = pos[random_num]
    color = color_[rand_color]
    tray_type = get_board_properties(put_tile_pos[0],put_tile_pos[1])
    player1_tile[0].put_tile(tray_type, color)  # 플레이어가 가지고 있는 타일에 속성을 부여
    board[put_tile_pos[0]][put_tile_pos[1]] = player1_tile[0]  # 해당 보드에 타일 놓기
    player1_tile = player1_tile[1:]  # tray에 놓은 타일 제거

def move_board_from_return(return_board, player):
    global player1_tile, player2_tile, board
    print_cboard(return_board)
    cboard = board_to_cboard(board)
    moved = False
    for i in range(4):
        for j in range(4):
            if return_board[i][j] != cboard[i][j]:
                if not player:
                    #print("서로 다른 위치의 i =",i,"j =",j)
                    if cboard[i][j] == 3 or cboard[i][j] == 4: # False 일 때 움직인 3,4의 원래 위치
                        move_before_pos = (i,j)
                        moved = True
                    if return_board[i][j] == 3 or return_board[i][j] == 4:
                        move_after_pos = (i,j)
                    if return_board[i][j] == 1 or return_board[i][j] == 2:  # 1,2의 차례인데 바뀐 곳 중 1,2
                        put_after_pos = (i, j, return_board[i][j]-1)
                else:
                    if cboard[i][j] == 1 or cboard[i][j] == 2: # False 일 때 움직인 1,2의 원래 위치
                        move_before_pos = (i,j)
                        moved = True
                    if return_board[i][j] == 1 or return_board[i][j] == 2:
                        move_after_pos = (i,j)
                    if return_board[i][j] == 3 or return_board[i][j] == 4:  # 3,4의 차례인데 바뀐 곳 중 3,4
                        put_after_pos = (i, j, return_board[i][j]-3)
    if moved:
        board[move_after_pos[0]][move_after_pos[1]] = board[move_before_pos[0]][move_before_pos[1]]
        board[move_before_pos[0]][move_before_pos[1]] = 0
    #color 는 0과 1로 부여
    tray_type = get_board_properties(put_after_pos[0], put_after_pos[1])
    draw_board()
    pygame.display.update()
    pygame.time.delay(500)
    if not player:  # player1 일  때
        player1_tile[0].put_tile(tray_type, put_after_pos[2])  # 플레이어가 가지고 있는 타일에 속성을 부여
        board[put_after_pos[0]][put_after_pos[1]] = player1_tile[0]  # 해당 보드에 타일 놓기
        player1_tile = player1_tile[1:]  # tray에 놓은 타일 제거
    else:
        player2_tile[0].put_tile(tray_type, put_after_pos[2])  # 플레이어가 가지고 있는 타일에 속성을 부여
        board[put_after_pos[0]][put_after_pos[1]] = player2_tile[0]  # 해당 보드에 타일 놓기
        player2_tile = player2_tile[1:]  # tray에 놓은 타일 제거



def draw_check(board):
    for i in range(4):
        for j in range(4):
            if board[i][j] == 0:
                return False
    return True

def game_over_check(board):
    if win_check(board):
        return True
    if draw_check(board):
        return True


def find_color(i, j):
    if (i,j) == selected_tray:
        return green
    elif board[i][j] == 0:
        return gray
    else:
        tray_type = get_board_properties(i, j)
        color = board[i][j].get_tile_color(tray_type)
        if color == 1:
            return red
        elif color == 2:
            return blue
        elif color == 3:
            return yellow
        elif color == 4:
            return white

def select_opposite_tile(pos):
    tmp_tray = find_tray(pos)
    if on_board_button(pos) and board[tmp_tray[0]][tmp_tray[1]] != 0 and board[tmp_tray[0]][tmp_tray[1]].player != player:
        return True
    return False

def move_opposite_tile(pos,s_tray):
    tmp_tile = find_tray(pos) # 선택된 곳의 타일 index  s_tray는 이동 하려하는 타일의 tray index
    all_index = (s_tray[0]-1,s_tray[1]),(s_tray[0]+1,s_tray[1]),(s_tray[0],s_tray[1]-1),(s_tray[0],s_tray[1]+1)
    for index in all_index:
        if 0 <= index[0] < 4 and 0 <= index[1] < 4 and tmp_tile == index:
            return True
    return False

MESSAGE_HEIGHT = 40
def info_message(_msg):
    if _msg is not None:
        # 배경 덧칠 하기
        rect = pygame.Rect( (TRAY_SIZE * 5.5, TRAY_SIZE * 2.5), (TRAY_SIZE * 3, TRAY_SIZE) )
        pygame.draw.rect(background, black, rect)

        # display message text
        text = font.render(_msg, True, white)
        background.blit(text, (550, 285))
        pygame.display.update()


def draw_button(center_pos, button_color, BUTTON_WIDTH = 99,BUTTON_HEIGHT = 99,button_text = "", width = 0):
    # draw button
    rect = pygame.Rect((0, 0, BUTTON_WIDTH, BUTTON_HEIGHT))
    rect.center = center_pos
    pygame.draw.rect(background, button_color, rect, width)

    # button text
    text = font.render(button_text, True, black)
    text_rect = text.get_rect()
    text_rect.center = rect.center
    background.blit(text, text_rect)




def draw_main_button():
    main_center = [SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3 - 10]
    btn_texts = ("P v P", "P v AI", "EXIT")
    for btn in range(3):
        draw_button(tuple(main_center), gray, SCREEN_WIDTH/3 , SCREEN_HEIGHT/6,btn_texts[btn] )
        main_center[1] += SCREEN_HEIGHT / 6 + 10

def on_pvp_button(pos):
    main_center = [SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 3 - 10]
    if (pos[0] - main_center[0] <= SCREEN_WIDTH/6) and (pos[1] - main_center[1] <= SCREEN_HEIGHT/12):
        return True


def on_pvai_button(pos):
    pvai_center = [SCREEN_WIDTH / 2 , SCREEN_HEIGHT / 2]
    if (pos[0] - pvai_center[0] <= SCREEN_WIDTH/6) and (pos[1] - pvai_center[1] <= SCREEN_HEIGHT/12):
        return True

def on_exit_button(pos):
    exit_center = [SCREEN_WIDTH / 2 , 2 * SCREEN_HEIGHT / 3 + 10]
    if (pos[0] - exit_center[0] <= SCREEN_WIDTH/6) and (pos[1] - exit_center[1] <= SCREEN_HEIGHT/12):
        return True

draw_return_to_main_button_size = (TRAY_SIZE,SCREEN_HEIGHT/12)
draw_return_to_main_button_center = (TRAY_SIZE * 6.5, TRAY_SIZE * 0.5)

def draw_return_to_main_button():
    draw_button(draw_return_to_main_button_center, gray, draw_return_to_main_button_size[0]-1, draw_return_to_main_button_size[1]-1, "MAIN")

def on_return_to_main_button(pos):
    return (abs(pos[0] - draw_return_to_main_button_center[0]) <= draw_return_to_main_button_size[0]//2) and \
        (abs(pos[1] - draw_return_to_main_button_center[1]) <= draw_return_to_main_button_size[1]//2)

draw_record_button_size = (TRAY_SIZE,SCREEN_HEIGHT/12)
draw_record_button_center = (TRAY_SIZE * 7.5, TRAY_SIZE * 0.5)

def draw_record_button():
    global record_mode
    if record_mode:
        draw_button(draw_record_button_center, green, draw_record_button_size[0]-1, draw_record_button_size[1]-1, "Record ON")
    else:
        draw_button(draw_record_button_center, gray, draw_record_button_size[0]-1, draw_record_button_size[1]-1, "Record OFF")

def on_draw_record_button(pos):
        return (abs(pos[0] - draw_record_button_center[0]) <= draw_record_button_size[0]//2) and \
            (abs(pos[1] - draw_record_button_center[1]) <= draw_record_button_size[1]//2)
def draw_board():
    for i in range(4):
        for j in range(4):
            # print("i =",i,"j =",j,"find_color(i,j) =",find_color(i,j))
            draw_button((j*TRAY_SIZE+TRAY_SIZE*1.5,
                         i*TRAY_SIZE+TRAY_SIZE* 1.5),find_color(i,j))

def on_board_button(pos):
    return (pos[0] - TRAY_SIZE <= TRAY_SIZE * 4 - 1) \
        and (pos[1] - TRAY_SIZE <= TRAY_SIZE * 4 - 1)

# 색깔 버튼 위치 선정
select_button_first_left = (TRAY_SIZE*6.5, TRAY_SIZE*1.5)
select_button_first_right = (TRAY_SIZE*7.5, TRAY_SIZE*1.5)

select_button_second_left = (TRAY_SIZE*6.5, TRAY_SIZE*4.5)
select_button_second_right = (TRAY_SIZE*7.5, TRAY_SIZE*4.5)

def on_empty_tray(pos):
    tmp_tray = find_tray(pos)
    return on_board_button(pos) and board[tmp_tray[0]][tmp_tray[1]] == 0

# 색깔 버튼 생성
def draw_color_button():
    draw_button(select_button_first_left,red)
    draw_button(select_button_first_right,blue)
    draw_button(select_button_second_left,yellow)
    draw_button(select_button_second_right,white)

def on_color_button(pos):
    global color
    if player:
        if (abs(pos[0] - select_button_second_left[0]) <= TRAY_SIZE/2) \
                and (abs(pos[1] - select_button_second_left[1]) <= TRAY_SIZE/2) :
            color = 0
            return True
        elif (abs(pos[0] - select_button_second_right[0]) <= TRAY_SIZE/2) \
                and (abs(pos[1] - select_button_second_right[1]) <= TRAY_SIZE/2):
            color = 1
            return True
    else:
        if (abs(pos[0] - select_button_first_left[0]) <= TRAY_SIZE/2) \
                and (abs(pos[1] - select_button_first_left[1]) <= TRAY_SIZE/2) :
            color = 0
            return True
        elif  (abs(pos[0] - select_button_first_right[0]) <= TRAY_SIZE/2) \
                and (abs(pos[1] - select_button_first_right[1]) <= TRAY_SIZE/2) :
            color = 1
            return True

# 리셋 버튼 설정
reset_button_size = (TRAY_SIZE,SCREEN_HEIGHT/12)
reset_button_center = (TRAY_SIZE * 6.5, TRAY_SIZE * 5.5)
def draw_gameReset_button():
    draw_button(reset_button_center, gray, reset_button_size[0]-1, reset_button_size[1]-1, "RESET")

def on_game_reset(pos):
    return (abs(pos[0] - reset_button_center[0]) <= reset_button_size[0]//2) and \
        (abs(pos[1] - reset_button_center[1]) <= reset_button_size[1]//2)

manual_ai_button_size = (TRAY_SIZE,SCREEN_HEIGHT/12)
manual_ai_button_center = (TRAY_SIZE * 7.5, TRAY_SIZE * 5.5)
def draw_manual_ai_button():
    draw_button(manual_ai_button_center, gray, manual_ai_button_size[0]-1, manual_ai_button_size[1]-1, "AI MOVE")

def on_manual_ai_button(pos):
    return (abs(pos[0] - manual_ai_button_center[0]) <= manual_ai_button_size[0]//2) and \
        (abs(pos[1] - manual_ai_button_center[1]) <= manual_ai_button_size[1]//2)

def find_tray(pos):
    return (int((pos[1]-TRAY_SIZE) // TRAY_SIZE),
            int((pos[0]-TRAY_SIZE) // TRAY_SIZE))

draw_record_confirm_button_size = (TRAY_SIZE * 0.8,TRAY_SIZE * 0.8)
draw_record_confirm_center = (TRAY_SIZE * 4 , TRAY_SIZE * 3)

def draw_record_confirm_button():
    draw_button(draw_record_confirm_center, gray, draw_record_confirm_button_size[0], draw_record_confirm_button_size[1], "Yes")

def on_record_button(pos):
    return (abs(pos[0] - draw_record_confirm_center[0]) <= draw_record_confirm_button_size[0]//2) and \
        (abs(pos[1] - draw_record_confirm_center[1]) <= draw_record_confirm_button_size[1]//2)


record_cancel_button_size = (TRAY_SIZE * 0.8,TRAY_SIZE * 0.8)
record_cancel_button_center = (TRAY_SIZE * 5 , TRAY_SIZE * 3)

def draw_record_cancel_button():
    draw_button(record_cancel_button_center, gray, record_cancel_button_size[0], record_cancel_button_size[1], "No")

def on_record_cancel_button(pos):
    return (abs(pos[0] - record_cancel_button_center[0]) <= record_cancel_button_size[0]//2) and \
        (abs(pos[1] - record_cancel_button_center[1]) <= record_cancel_button_size[1]//2)


draw_record_background_size = (TRAY_SIZE * 2,TRAY_SIZE * 1.2)
draw_record_background_center = (TRAY_SIZE * 4.5 , TRAY_SIZE * 3)
def draw_record_background():
    draw_button(draw_record_background_center, black, draw_record_background_size[0], draw_record_background_size[1])

def recording():
    global record_list
    try:
        rdf = pd.read_csv('board_record.csv')
    except pd.errors.EmptyDataError: # 파일이 비어있는 경우 빈 DataFrame 으로 초기화
        rdf = pd.DataFrame()
    df = pd.DataFrame()
    for board in record_list:
        board.append([-1,-1,-1,-1])
        board = pd.DataFrame(board)
        df = pd.concat([df, board], axis = 0, ignore_index=True)
    df['NewColumn'] = -1
    df = df[['NewColumn'] + [col for col in df.columns if col != 'NewColumn']]
    rdf = pd.concat([rdf, df], axis=1, ignore_index=True)
    rdf.to_csv("board_record.csv", index=False)

def plyer_select(p):
    if not p:
        return "player1"
    else:
        return "player2"

def player_first_serve():
    return random.randint(0,1) == 0

def board_to_cboard(board): # 객체가 담겨있는 보드를 1,2,3,4 숫자로만 이루어진 보드로 변환
    cboard = [[] for i in range(4)]
    for i in range(4):
        for j in range(4):
            #           print(i, j ,board)
            if board[i][j] == 0:
                cboard[i].append(0)
            elif isinstance(board[i][j], Tile):
                cboard[i].append(board[i][j].get_tile_color(get_board_properties(i, j)))
    return cboard


def ai_only_player1(cb):
    for i in range(4):
        for j in range(4):
            if cb[i][j] == 1:
                cb[i][j] = 3
            elif cb[i][j] == 2:
                cb[i][j] = 4
            elif cb[i][j] == 3:
                cb[i][j] = 1
            elif cb[i][j] == 4:
                cb[i][j] = 2
    return cb
def print_cboard(cbaord):
    for line in cbaord:
        print(line)
    print()

def pt(b,i,j):
    if b[i][j].get_tile_color(get_board_properties(i, j))==1 or b[i][j].get_tile_color(get_board_properties(i, j))==2:
        return True
    else:
        return False
def three_check(b):
    temp1 = []
    temp2 = []
    for i in range(4):
        for j in range(2):
            if (b[i][j] != 0) and (b[i][j+1] != 0) and (b[i][j+2] != 0):
                if b[i][j].get_tile_color(get_board_properties(i, j)) \
                        == b[i][j+1].get_tile_color(get_board_properties(i, j + 1)) \
                        == b[i][j+2].get_tile_color(get_board_properties(i, j + 2)):
                    if pt(b, i, j):
                        temp1.append([i, j])
                    else:
                        temp2.append([i, j])
    return len(temp1) != 0, temp1, len(temp2) != 0, temp2

def diagonal_check(b):
    temp1 = []
    temp2 = []
    for i in range(2):
        for j in range(2):
            if (b[i][j] != 0) and (b[i + 1][j + 1] != 0) and (b[i + 2][j + 2] != 0):
                if b[i][j].get_tile_color(get_board_properties(i, j)) \
                        == b[i + 1][j + 1].get_tile_color(get_board_properties(i, j)) \
                        == b[i + 2][j + 2].get_tile_color(get_board_properties(i, j)):
                    if pt(b, i, j):
                        temp1.append([i, j])
                    else:
                        temp2.append([i, j])
    return len(temp1) != 0, temp1, len(temp2) != 0, temp2

def around_check(b,index):
    for i,j in index:
        if i == 0:
            if 0 in b[i + 1][j:j + 3]:
                continue
        elif i == 1 or i == 2:
            if (0 in b[i - 1][j:j + 3]) or (0 in b[i + 1][j:j + 3]):
                continue
        elif i == 3:
            if 0 in b[i - 1][j:j + 3]:
                continue
        if j == 0:
            if b[i][3] == 0:
                continue
            else:
                return True
        else:
            if b[i][0] == 0:
                continue
            else:
                return True
    return False

def diagonal_around_check(b,index):
    for i,j in index:
        if i + j == 1:
            if i == 0:
                if 0 in [b[0][2], b[1][3]]:
                    continue
            else:
                if 0 in [b[2][0], b[3][1]]:
                    continue
            if 0 in [b[0][0], b[1][1], b[2][2], b[3][3]]:
                continue
            else:
                return True
            # return 0 not in [b[0][0], b[1][1], b[2][2], b[3][3]]
        else:  # 0,0  1,1
            if (0 in [b[0][1], b[1][2], b[2][3]]) or (0 in [b[1][0], b[2][1], b[3][2]]):
                continue
            else:
                return True
    return False
    # return (0 not in [b[0][1], b[1][2], b[2][3]]) and (0 not in [b[1][0], b[2][1], b[3][2]])

def win_check(board):
    boardr = []
    board1 = list(map(list, zip(*board)))
    for i in board:
        boardr.append(i[::-1])
    three1, index1, three2, index2 = three_check(board)
    three1r, index1r, three2r, index2r = three_check(board1)
    dia1, index1d, dia2, index2d = diagonal_check(board)
    dia1r, index1dr, dia2r, index2dr = diagonal_check(boardr)
    game_over = False
    if three1:
        if around_check(board,index1):
            print('player1 승리')
            game_over = True
    if three2:
        if around_check(board,index2):
            print('player2 승리')
            game_over = True
    if three1r:
        if around_check(board1,index1r):
            print('player1 승리')
            game_over = True
    if three2r:
        if around_check(board1,index2r):
            print('player2 승리')
            game_over = True
    if dia1:
        if diagonal_around_check(board,index1d):
            print('player1 승리')
            game_over = True
    if dia2:
        if diagonal_around_check(board,index2d):
            print('player2 승리')
            game_over = True
    if dia1r:
        if diagonal_around_check(boardr,index1dr):
            print('player1 승리')
            game_over = True
    if dia2r:
        if diagonal_around_check(boardr,index2dr):
            print('player2 승리')
            game_over = True
    return game_over

def reset_game():
    global player, selected_tray, color, board, record_list
    color = -1                  # player 가 선택한 color 정보
    selected_tray = (-1, -1)    # 선택된 tray
    player = False              # False 가 Player1 True 가 Player2
    tile_reset()
    board = [[0]*4 for _ in range(4)]
    record_list = []


def draw_items(state):
    if state == 11:
        draw_record_confirm_button()
        draw_record_cancel_button()
    elif state != 10:
        draw_board()
        draw_color_button()
        draw_gameReset_button()
        draw_manual_ai_button()
        draw_record_button()
        draw_return_to_main_button()
    else:
        draw_main_button()
        draw_record_button()
    pygame.display.flip()

# ai_mode
# False : PvP
# True : PvAI

# state
# -1 : 게임 reset
# 0 : 공수 교대
# 1 : 상대 타일 선택 대기
# 2 : 상대 타일 선택
# 3 : 상대 타일 이동 선택 대기
# 4 : 상대 타일 이동
# 5 :
# 6 : 트레이 선택 대기
# 7 : 트레이 선택
# 8 : 타일 색깔 선택 대기
# 9 : 타일 두기

# 10 : 메뉴
# 11 : 레코드 여부 확인 대기

# 15 : ai 선공 정하기
# 16 : ai 턴

def update_state():
    global state, player, selected_tray, color, player1_tile, player2_tile, board, ai_mode, ai_turn
    if state == -1:
        reset_game()
        if ai_mode:
            state = 15
        else:
            state = 6

    elif state == 0:
        player = not player
        if ai_mode:
            if not ai_turn:
                state = 1
                if bs.cant_move(board_to_cboard(board), player):
                    state = 6
                ai_turn = True
            else:
                state = 16
        else:
            state = 1
            if bs.cant_move(board_to_cboard(board), player):
                state = 6
    elif state == 1:
        info_message(plyer_select(player) + " select opposite tile")
    elif state == 2:
        # 소리나 효과 추가
        state = 3
    elif state == 3:
        info_message(plyer_select(player) + " select tray to move tile")
    elif state == 4:
        selected_tray = (-1, -1)  # 선택된 tray 초기화
        state = 6
    elif state == 6:
        info_message(plyer_select(player) + " select tray")
    elif state == 7:
        # 소리나 효과 추가
        state = 8
    elif state == 8:
        info_message(plyer_select(player) + " select color")
    elif state == 9:
        tray_type = get_board_properties(selected_tray[0], selected_tray[1])
        if not player:  # player1 일  때
            player1_tile[0].put_tile(tray_type, color)  # 플레이어가 가지고 있는 타일에 속성을 부여
            board[selected_tray[0]][selected_tray[1]] = player1_tile[0]  # 해당 보드에 타일 놓기
            player1_tile = player1_tile[1:]  # tray에 놓은 타일 제거
        else:
            player2_tile[0].put_tile(tray_type, color)  # 플레이어가 가지고 있는 타일에 속성을 부여
            board[selected_tray[0]][selected_tray[1]] = player2_tile[0]  # 해당 보드에 타일 놓기
            player2_tile = player2_tile[1:]  # tray에 놓은 타일 제거
        record_list.append(board_to_cboard(board))
        selected_tray = (-1, -1)  # 선택된 tray 초기화
        state = 0

    elif state == 15:
        if player_first_serve():
            ai_turn = True
            state = 6
        else:
            state = 16
    elif state == 16:
        info_message("AI Processing...")
        ai_move(player)
        record_list.append(board_to_cboard(board))
        state = 0
        ai_turn = False
    draw_items(state)

# process
play = True

while play:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            click_pos = pygame.mouse.get_pos()
            if event.type == pygame.MOUSEBUTTONDOWN:
                print("######################마우스 클릭 됨#######################")

            if state == 1:
                if on_manual_ai_button(click_pos):
                    ai_move(player)
                    state = 0
                elif select_opposite_tile(click_pos):
                    selected_tray = find_tray(click_pos)
                    state = 2

            elif state == 3 and select_opposite_tile(click_pos):
                selected_tray = find_tray(click_pos)
            elif state == 3 and move_opposite_tile(click_pos,selected_tray):
                tmp_tray = find_tray(click_pos)
                if board[tmp_tray[0]][tmp_tray[1]] == 0:
                    board[tmp_tray[0]][tmp_tray[1]] = board[selected_tray[0]][selected_tray[1]]
                    board[selected_tray[0]][selected_tray[1]] = 0
                    state = 4

            elif state == 6 and on_empty_tray(click_pos):
                selected_tray = find_tray(click_pos)
                state = 7
            elif state == 8 and on_empty_tray(click_pos):
                selected_tray = find_tray(click_pos)
            elif state == 8 and on_color_button(click_pos):
                state = 9

            elif state == 10 and on_pvp_button(click_pos):
                ai_mode = False
                state = 6
                background.fill(black)
            elif state == 10 and on_pvai_button(click_pos):
                ai_mode = True
                state = 15
                background.fill(black)
            elif state == 10 and on_exit_button(click_pos):
                play = False
            elif state == 10 and on_draw_record_button(click_pos):
                record_mode = not record_mode
            elif state == 11:
                if on_record_button(click_pos):
                    recording()
                    background.fill(black)
                    state = -1
                elif on_record_cancel_button(click_pos):
                    background.fill(black)
                    state = -1
            if on_return_to_main_button(click_pos):
                reset_game()
                state = 10
                background.fill(black)

            if on_game_reset(click_pos):
                state = -1

            if event.type == pygame.MOUSEBUTTONDOWN:  # 상태 확인용

                # color_board = board_to_cboard(board)
                # print_cboard(color_board)
                # print("######################마우스 클릭 됨#######################")
                # print("selected_tray = ",selected_tray, "state =", state, "   player =", player)
                # print("click_pos =", click_pos)
                # print("(게임모드 -- False : PvP True : PvAI)=== mode:",ai_mode)
                pass

    if state != 11 and state != -1 and game_over_check(board):
        time.sleep(2)
        if record_mode:
            draw_record_background()
            pygame.display.update()
            state = 11
        else:
            state = -1
    update_state()
    pygame.display.update()
    pygame.time.delay(40)
pygame.quit()



# 해야 할 것
# 움직일 곳이 없을 때 수를 두기만 하는 것도 추가
# 구석에 두는 수에 차등을 둠 (상대의 타일로 막혀있으면 추가 점수를 줌)
second push test
