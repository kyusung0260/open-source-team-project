def cant_move(node, player):
    if player == False: # 플레이어1
        oc1, oc2 = 3,4 # player-color // opposite - color
    else:
        oc1, oc2 = 1,2
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우
    cant_move = 0
    for i in range(4):
        for j in range(4):
            if node[i][j] == oc1 or node[i][j] == oc2:
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 4 and 0 <= nj < 4 and node[ni][nj] == 0:
                        cant_move += 1
    if cant_move == 0:
        return True
    else:
        return False