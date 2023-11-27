import math
import evaluate
import random
import time
def is_terminal_node(node):
    for i in range(4):
        for j in range(4):
            if node[i][j] == 0:
                return False
    return True


def generate_children(node,player):
    children = []
    if player == False: # 플레이어1
        pc1, pc2, oc1, oc2 = 1,2,3,4 # player-color // opposite - color
    else:
        pc1, pc2, oc1, oc2 = 3,4,1,2

    def add_child(new_node):
        for x in range(4):
            for y in range(4):
                if new_node[x][y] == 0:
                    new_node3 = [row[:] for row in new_node]
                    new_node3[x][y] = pc1
                    children.append(new_node3)
                    new_node4 = [row[:] for row in new_node]
                    new_node4[x][y] = pc2
                    children.append(new_node4)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상, 하, 좌, 우
    cant_move = 0
    for i in range(4):
        for j in range(4):
            if node[i][j] == oc1 or node[i][j] == oc2:
                for di, dj in directions:
                    ni, nj = i + di, j + dj
                    if 0 <= ni < 4 and 0 <= nj < 4 and node[ni][nj] == 0:
                        new_node = [row[:] for row in node]
                        if node[i][j] == oc1: #1은 2로
                            new_node[ni][nj] = oc2
                        else: #2는 1로
                            new_node[ni][nj] = oc1
                        new_node[i][j] = 0
                        add_child(new_node)
                        cant_move += 1
    if cant_move == 0:
        add_child(node)

    return tuple(children) #tuple 리턴

total_time = 1

def alphabeta(node, depth, alpha, beta, maximizing_player, first_depth = 1):

    if first_depth > 0:
        return_lst = []

    if depth == 0 or is_terminal_node(node):  # max depth 이거나 마지막 노드(게임 over) 이면 값 반환
        score = evaluate.evaluate(node)
        return score, []

    if not maximizing_player:
        bestVal = -math.inf
        bestPos = 0
        for child in generate_children(node, False):

            # print("\n#################\ndepth = ", depth)
            # print_cboard(child)

            if evaluate.win_check(child):
                if evaluate.get_p1_score() == evaluate.get_win_val() + 1:
                    return evaluate.get_win_val() + 1, child
            value, _ = alphabeta(child, depth - 1, alpha, beta, True, first_depth-1)
            # print("depth =", depth)
            #     print_cboard(child)
            #     print("value = ", value, "beta =", beta, "alpha =", alpha)

            if first_depth > 0:
                if bestVal == value:
                    bestVal = value
                    return_lst.append(child)
                elif bestVal < value:
                    bestVal = value
                    return_lst = [child]
            else:
                if bestVal <= value:
                    bestVal = value
                    bestPos = child
            alpha = max(alpha, bestVal)
            if beta < alpha:
                break  # β cut-off

            # print("bestVal = ", bestVal)

        if first_depth > 0:
            return bestVal, random.choice(return_lst)
        return bestVal, bestPos

    else:
        bestVal = math.inf
        bestPos = 0
        # print("노드의 개수 :", len(generate_children(node, True)))
        for child in generate_children(node, True):
            if evaluate.win_check(child):
                if evaluate.get_p2_score() == evaluate.get_win_val():
                    return -evaluate.get_win_val(), child
            value, _ = alphabeta(child, depth - 1, alpha, beta, False, first_depth-1)

            # print("depth =", depth)
            # print_cboard(child)
            # print("value = ", value, "beta =", beta, "alpha =", alpha)

            if bestVal >= value:
                bestVal = value
                bestPos = child
            beta = min(beta, bestVal)
            if beta < alpha:
                break  # α cut-off

            # print("bestVal = ", bestVal)

        return bestVal, bestPos

def print_cboard(cbaord):
    for line in cbaord:
        print(line)
    print()

# b = [[0,0,1,4],[0,0,2,3],[0,0,2,4],[0,0,1,3]
# print(generate_children(b, False))
# b1 = [[1, 1, 0, 3],
#       [4, 3, 1, 3],
#       [0, 0, 1, 0],
#       [0, 0, 0, 0]]
#
# b2 = [[4, 1, 1, 3],
# [2, 2, 3, 2],
# [1, 4, 2, 4],
# [3, 1, 4, 3]]
# # print(len(generate_children(b2, True)))
# print(type(generate_children(b2, True)))

# val, node = alphabeta(b2, 3, -10000000000, 1000000000000, False)
# print("val =", val)
# print_cboard(node)\

