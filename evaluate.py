# 점수 지정
TWO_TILE_VAL = 100
THREE_TILE_VAL = 111
BLANK_VAL = -10
EDGE_SCORE = 95
WIN_VAL = 3000
player1_score = 0
player2_score = 0

def print_cboard(cbaord):
    for line in cbaord:
        print(line)
    print()
def rotate_90(matrix):
    return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]) - 1, -1, -1)]

def get_win_val():
    return WIN_VAL

def get_p1_score():
    return player1_score

def get_p2_score():
    return player2_score

def evaluate(board):
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0

    # 승리 조건 check
    if win_check(board):
        return player1_score - player2_score
    # 가로 평가
    line_score(board, True)
    
    # 세로 평가
    board = list(map(list,zip(*board)))
    line_score(board, True)

    # 대각 평가
    line_score(board, False)
    board = [row[::-1] for row in board]

    # 대각 대칭 평가
    line_score(board, False)

    for _ in range(4):
        edge_score(board)
        board = rotate_90(board)
    return player1_score - player2_score


def win_check(board):
    global player1_score, player2_score
    player1_score = 0
    player2_score = 0
    game_over = False
    if line_win_check(board):
        game_over = True
    board = list(map(list,zip(*board)))
    if line_win_check(board):
        game_over = True
    if dialog_win_check(board):
        game_over = True
    board = [row[::-1] for row in board]
    if dialog_win_check(board):
        game_over = True
    if game_over:
        if player1_score == player2_score:
            player1_score = 1
            player2_score = 0
        elif player1_score > player2_score:
            player1_score = 3001
            player2_score = 0
        elif player1_score < player2_score:
            player1_score = 0
            player2_score = 3000
    return game_over

def line_win_check(board):
    global player1_score, player2_score
    around = [(0, -1), (-1, 0), (-1, 1), (-1, 2), (1, 0), (1, 1), (1, 2), (0, 3)]
    for i in range(4):
        for j in range(2):
            if board[i][j] != 0 and board[i][j] == board[i][j+1] == board[i][j+2]:
                win_color = board[i][j]
                win = True
                for bi, bj in around:
                    if 0 <= i + bi < 4 and 0 <= j + bj < 4:
                        if board[i+bi][j+bj] == 0:
                            win = False
                            break
                if win:
                    if win_color == 1 or win_color == 2:
                        player1_score += WIN_VAL + 1
                        return True
                    else:
                        player2_score += WIN_VAL
                        return True
    return False

def dialog_win_check(board):
    global player1_score, player2_score
    around = [(0, -1), (-1, 0), (0, 1), (1, 0), (1, 2), (2, 1), (2, 3), (3, 2)]
    start_points = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for start_i, start_j in start_points:
        if board[start_i][start_j] != 0 and board[start_i][start_j] == board[start_i+1][start_j+1] == board[start_i+2][start_j+2] :
            win_color = board[start_i][start_j]
            win = True
            for bi, bj in around:
                if 0 <= start_i+bi < 4 and 0 <= start_j+bj < 4:
                    if board[start_i+bi][start_j+bj] == 0:
                        win = False
                        break
            if win:
                if win_color == 1 or win_color == 2:
                    player1_score += WIN_VAL + 1
                    return True
                else:
                    player2_score += WIN_VAL
                    return True
    return False
def line_score(board, mode):
    global player1_score, player2_score
    around_pos = ((-1, 0), (1, 0), (0, -1), (0, 1))
    if mode:
        for i in range(4):
            recent_tile = 0
            for j in range(4):
                if board[i][j] == 0:
                    recent_tile = 0
                else: #현재 탐색하는 위치가 0이 아니면 = 빈 칸이 아니면
                    # 몇개가 이어져 있는가?
                    if recent_tile == board[i][j]: # 최근 타일과 현재 타일이 같으면
                        num_of_tile += 1           # 하나 추가
                    else:
                        tmp_val = 0
                        num_of_tile = 1
                        blank = set()          # 빈 칸의 위치 i,j 집합 저장
                        recent_tile = board[i][j]
                    # 현재의 타일의 주변 빈칸 좌표
                    for dir in around_pos:
                        i_pos = i+dir[0]
                        j_pos = j+dir[1]

                        if 0 <= i_pos < 4 and 0 <= j_pos < 4 and board[i_pos][j_pos] == 0:
                            blank.add((i_pos, j_pos))
                    if num_of_tile == 2:
                        if recent_tile == 1 or recent_tile == 2:
                            tmp_val = TWO_TILE_VAL + len(blank) * BLANK_VAL
                            player1_score += tmp_val
                        else:
                            tmp_val = TWO_TILE_VAL + len(blank) * BLANK_VAL
                            player2_score += tmp_val

                    elif num_of_tile == 3:
                        if recent_tile == 1 or recent_tile == 2:
                            player1_score -= tmp_val
                            tmp_val = THREE_TILE_VAL + len(blank) * BLANK_VAL
                            player1_score += tmp_val
                        else:
                            player2_score -= tmp_val
                            tmp_val = THREE_TILE_VAL + len(blank) * BLANK_VAL
                            player2_score += tmp_val

                    elif num_of_tile == 4:
                        if recent_tile == 1 or recent_tile == 2:
                            player1_score -= tmp_val
                            player1_score += THREE_TILE_VAL + len(blank) * BLANK_VAL
                        else:
                            player2_score -= tmp_val
                            player2_score += THREE_TILE_VAL + len(blank) * BLANK_VAL

    else:
        dialog = [(0, 1), (0 , 0) , (1, 0)]
        for i, j in dialog:
            recent_tile = 0
            for _ in range(4):
                if i > 3 or j > 3:
                    break
                if board[i][j] == 0:
                    recent_tile = 0
                else : #현재 탐색하는 위치가 0이 아니면 = 빈 칸이 아니면
                    # 몇개가 이어져 있는가?
                    if recent_tile == board[i][j]: # 최근 타일과 현재 타일이 같으면
                        num_of_tile += 1           # 하나 추가
                    else:
                        tmp_val = 0
                        num_of_tile = 1
                        blank = set()          # 빈 칸의 위치 i,j 집합 저장
                        recent_tile = board[i][j]
                    # 현재의 타일의 주변 빈칸 좌표
                    for dir in around_pos:
                        i_pos = i+dir[0]
                        j_pos = j+dir[1]

                        if 0 <= i_pos < 4 and 0 <= j_pos < 4 and board[i_pos][j_pos] == 0:
                            blank.add((i_pos, j_pos))
                    if num_of_tile == 2:
                        if recent_tile == 1 or recent_tile == 2:
                            tmp_val = TWO_TILE_VAL + len(blank) * BLANK_VAL
                            player1_score += tmp_val
                        else:
                            tmp_val = TWO_TILE_VAL + len(blank) * BLANK_VAL
                            player2_score += tmp_val

                    elif num_of_tile == 3:
                        if recent_tile == 1 or recent_tile == 2:
                            player1_score -= tmp_val
                            tmp_val = THREE_TILE_VAL + len(blank) * BLANK_VAL
                            player1_score += tmp_val
                        else:
                            player2_score -= tmp_val
                            tmp_val = THREE_TILE_VAL + len(blank) * BLANK_VAL
                            player2_score += tmp_val

                    elif num_of_tile == 4:
                        if recent_tile == 1 or recent_tile == 2:
                            player1_score -= tmp_val
                            player1_score += THREE_TILE_VAL + len(blank) * BLANK_VAL
                        else:
                            player2_score -= tmp_val
                            player2_score += THREE_TILE_VAL + len(blank) * BLANK_VAL

                i += 1
                j += 1

def edge_score(board):
    global player1_score, player2_score
    player1_tile = (1 ,2)
    player2_tile = (3, 4)
    if board[0][1] != 0 and board[1][0] != 0:
        if board[0][0] in player1_tile:
            player1_score += EDGE_SCORE
        elif board[0][0] in player2_tile:
            player2_score += EDGE_SCORE
