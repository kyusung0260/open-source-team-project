import sys
import math
import copy
import pygame
import time


def direction(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    elif x == 0:
        return 0
    else:
        return x


class buffalo_chess:
    teams={}
    def __init__(self):
        self.running=True
        self.score={}
        self.score['player1']={BUFFALO:0,HUNTER:0}
        self.score['player2']={BUFFALO:0,HUNTER:0}
        self.board=[]
        self.player1=BUFFALO
        self.turn=BUFFALO
        self.teams={}
        self.teams[BUFFALO]=Team(BUFFALO)
        self.teams[HUNTER]=Team(HUNTER)
        self.display=Display()
        self.clear_board()
        self.fill_board()
    
    def getting_p1(self):
        return self.player1
    
    def change_player(self):
        if self.player1==BUFFALO:
            self.player1=HUNTER
        else:
            self.player1=BUFFALO
    
    def getting_buffalo_score(self,player):
        return self.score[player][BUFFALO]

    def getting_hunter_score(self,player):
        return self.score[player][HUNTER]
    
    def add_buffalo_score(self,player):
        self.score[player][BUFFALO]+=1
    
    def add_hunter_score(self,player):
        self.score[player][HUNTER]+=1
        
    
    def resetting_board(self):
        self.teams[BUFFALO]=Team(BUFFALO)
        self.teams[HUNTER]=Team(HUNTER)
        self.clear_board()
        self.fill_board()
        self.setting_turn(BUFFALO)
        
    def gettingRunning(self):
        return self.running
    
    def setRunning(self, running):
        self.running = running
    
    def gettingBoard(self):
        return self.board
    
    def gettingDisplay(self):
        return self.display
    
    def getting_team(self, teamStr):
        return self.teams[teamStr]
   
    def clear_board(self):
        self.board = []
        for x in range(height_cells):
            row = []
            for y in range(width_cells):
                row.append(EMPTY)
            self.board.append(row)
    
    def erase_board(self):
        for x in range(height_cells):
            for y in range(width_cells):
                self.board[x][y]=EMPTY
    
    def check_valid_pos(self,pos):
        x,y=pos[0],pos[1]
        if (x >= 0 and x <= 6) and (x >= 0 and y <= 10):
            return True
        return False
    
    def pixel_to_pos(self, sx, sy, px, py, stride):
        pad = 0.1
        x = (py - sy) / stride 
        y = (px - sx) / stride
        if x < 0 or x >=height_cells  \
            or y < 0 or y >= width_cells:
                return False, -1, -1
        x_upper = math.floor(x)
        y_left = math.floor(y) 
        x_lower = math.ceil(x) 
        y_right = math.ceil(y) 
        if x >= x_upper + pad and x <= x_lower - pad:
            if y >= y_left + pad and y <= y_right - pad:
                return True, x_upper, y_left
        
        return False, x_upper, y_left   
    
    def getting_piece_num_from_board(self, team, pos):
        if team == BUFFALO:
            pieces = self.getting_team(BUFFALO).getting_all_pieces()
        else:
            pieces = self.getting_team(HUNTER).getting_all_pieces()
        for index,piece in enumerate(pieces):
            if piece.getting_alive():
                pos_i, pos_j = piece.getting_pos()
                if pos_i == pos[0] and pos_j == pos[1]:
                    return index
        return -1
    

    
    def getting_cell_from_board(self,pos):
        return self.board[pos[0]][pos[1]]
    
    def setting_cell_into_board(self,teamStr,typeStr,pos):
        self.board[pos[0]][pos[1]]=teamStr+typeStr
    
    def fill_board(self):
        pieces = self.getting_team(BUFFALO).getting_all_pieces()
        for piece in pieces:
            if piece.getting_alive():
                self.setting_cell_into_board(piece.getting_team(), piece.getting_type(), piece.getting_pos())
        pieces = self.getting_team(HUNTER).getting_all_pieces()
        for piece in pieces:
            if piece.getting_alive():
                self.setting_cell_into_board(piece.getting_team(), piece.getting_type(), piece.getting_pos())

    
    def getting_current_turn(self):
        return self.turn

    def setting_turn(self,turn):
        self.turn=turn

    def update_board(self):
        self.clear_board()
        self.fill_board()

    def getting_next_turn(self):
        if self.getting_current_turn()==BUFFALO:
            return HUNTER
        else:
            return BUFFALO
    
    def is_leftright_clear(self,pos_from,pos_to):
        x_from,y_from=pos_from[0],pos_from[1]
        x_to,y_to=pos_to[0],pos_to[1]
        diff_y=y_to-y_from
        for di in range(1,abs(diff_y)+1):
            if self.getting_cell_from_board((x_from,y_from+direction(diff_y)*di))!=EMPTY:
                return False
        return True

    def is_updown_clear(self,pos_from,pos_to):
        x_from,y_from=pos_from[0],pos_from[1]
        x_to,y_to=pos_to[0],pos_to[1]
        diff_x=x_to-x_from
        for di in range(1,abs(diff_x)+1):
            if self.getting_cell_from_board((x_from+direction(diff_x)*di,y_from))!=EMPTY:
                return False
        return True

    def is_diagonal_clear(self, pos_from, pos_to):
        x_from, y_from = pos_from
        x_to, y_to = pos_to
        diff_x = x_to - x_from 
        diff_y = y_to - y_from 
        if abs(diff_x) != abs(diff_y):
            return False
        direction_x = direction(diff_x)
        direction_y = direction(diff_y) 
        for di in range(1, abs(diff_x) + 1):
            if self.getting_cell_from_board((x_from + direction_x * di, y_from + direction_y * di)) != EMPTY:
                return False  
        return True

    def is_same_pos(self, pos1, pos2):
        if pos1[0] == pos2[0] and pos1[1] == pos2[1]:
            return False
    
    def get_all_possible_move(self,pos_from):
        if not self.check_valid_pos(pos_from):
            return False
        possible_pos=[]
        test_pos=[]
        for x in range(height_cells):
            for y in range(width_cells):
                if x!=pos_from[0] or y!=pos_from[1]:
                    test_pos.append([x,y])

        src_cell=self.getting_cell_from_board(pos_from)
        src_cell_team=src_cell[0]
        original_piece_num=self.getting_piece_num_from_board(src_cell_team,pos_from)


        for pos_to in test_pos:
            target_cell=self.getting_cell_from_board(pos_to)

            target_cell_team=target_cell[0]
            target_piece_num=self.getting_piece_num_from_board(target_cell_team,pos_to)
            is_not_my_turn=src_cell_team!=self.getting_current_turn()
            is_not_valid_teams=src_cell_team==target_cell_team
            if is_not_my_turn or is_not_valid_teams:
                continue
            
            moved=False
            iskilled=False

            if self.move(original_piece_num,pos_to):
                moved=True
                self.getting_team(src_cell_team).getting_piece(original_piece_num).setting_pos(pos_to)
                self.update_board()
            
            elif self.attack(original_piece_num,target_piece_num,pos_to):
                self.getting_team(src_cell_team).getting_piece(original_piece_num).setting_pos(pos_to)
                self.getting_team(self.getting_next_turn()).getting_piece(target_piece_num).setting_alive(False)
                self.update_board()
                iskilled=True

            
            else:
                continue

            if moved or iskilled:
                self.getting_team(src_cell_team).getting_piece(original_piece_num).setting_pos(pos_from)
                if iskilled:
                    self.getting_team(self.getting_next_turn()).getting_piece(target_piece_num).setting_alive(True)
                
                self.update_board()
                possible_pos.append(pos_to)
        return possible_pos
    
    def put(self, pos_from, pos_to):
        print('put')
        is_two_pos_same = self.is_same_pos(pos_from, pos_to)
        is_not_valid_pos_from = not self.check_valid_pos(pos_from)
        is_not_valid_pos_to = not self.check_valid_pos(pos_to)
        
        if is_two_pos_same or is_not_valid_pos_from or is_not_valid_pos_to:
            return False
        
        src_cell = self.getting_cell_from_board(pos_from)
        src_cell_team = src_cell[0]
        original_piece_num = self.getting_piece_num_from_board(src_cell_team, pos_from)
        
        target_cell = self.getting_cell_from_board(pos_to)
        target_cell_team = target_cell[0]
        target_piece_num = self.getting_piece_num_from_board(target_cell_team, pos_to)
        is_not_my_turn = src_cell_team != self.getting_current_turn()
        is_not_valid_teams = src_cell_team == target_cell_team
        if is_not_my_turn or is_not_valid_teams:
            return False
        
        isMoved = False
        isKilled = False
        if self.move(original_piece_num, pos_to):
            isMoved = True
            self.getting_team(src_cell_team).getting_piece(original_piece_num).setting_pos(pos_to)
            self.update_board()
        elif self.attack(original_piece_num, target_piece_num, pos_to):
            print("타켓넘버",target_piece_num)
            isKilled = True
            self.getting_team(src_cell_team).getting_piece(original_piece_num).setting_pos(pos_to)
            self.getting_team(self.getting_next_turn()).getting_piece(target_piece_num).setting_alive(False)
            
            self.update_board()
        else:
            return False
        return True

    def move(self, original_piece_num, pos_to):
        is_target_filled = self.getting_cell_from_board(pos_to) !=  EMPTY 
        if is_target_filled:
            return False
        src_team = self.getting_current_turn()
        original_piece = self.getting_team(src_team).getting_piece(original_piece_num)
        if self.piece_move(original_piece, pos_to):
            return True
        return False
 

    def piece_move(self,original_piece, pos_to):
        original_piece_team = original_piece.getting_team()
        original_piece_type = original_piece.getting_type()
        original_piece_moved = original_piece.getting_moved()
        src_pos = original_piece.getting_pos()
        if original_piece_type == BUFFALO:
             if self.buffalo_move(original_piece,pos_to):
                return True
        elif original_piece_type == HUNTER:
            if self.hunter_move(original_piece, pos_to):
                return True
        elif original_piece_type==DOG:
            if self.dog_move(original_piece, pos_to):
                return True
    
    def buffalo_move(self,original_piece,pos_to):
        src_team=original_piece.getting_team()
        pos_from=original_piece.getting_pos()
        x_from,y_from=pos_from[0],pos_from[1]
        x_to,y_to=pos_to[0],pos_to[1]
        isnotxpos=(x_from-1!=x_to)
        isnotypos=(y_from!=y_to)
        if isnotxpos or isnotypos:
            return False
        return True
    
    def dog_move(self,original_piece,pos_to):
        if pos_to[0]==0 or pos_to[0]==6:
            return False
        pos_from = original_piece.getting_pos()
        x_from, y_from = pos_from[0],pos_from[1]
        x_to, y_to = pos_to[0],pos_to[1]
        isleftright = x_from == x_to and y_from != y_to
        isupdown = x_from != x_to and y_from == y_to
        if isleftright:
            if self.is_leftright_clear(pos_from, pos_to):
                return True
        elif isupdown:
            if self.is_updown_clear(pos_from, pos_to):
                return True

        diff_x = x_to - x_from 
        diff_y = y_to - y_from
        is_not_diag_move = abs(diff_x) != abs(diff_y)
        if is_not_diag_move:
            return False
        if self.is_diagonal_clear(pos_from, pos_to):
            return True
        return False
    
    def hunter_move(self,original_piece,pos_to):
        if pos_to[0]==0 or pos_to[0]==6:
            return False
        pos_from = original_piece.getting_pos()
        x_from, y_from = pos_from[0],pos_from[1]
        x_to, y_to = pos_to[0],pos_to[1]
        diff_x = x_to - x_from 
        diff_y = y_to - y_from
        num_steps = (abs(diff_x) + abs(diff_y))
        isOneStep = num_steps == 1
        isTwoDiagStep = (abs(diff_x) == abs(diff_y)) and num_steps == 2
        if isOneStep or isTwoDiagStep:
            return True
        return False       

    def attack(self, original_piece_num, target_piece_num, pos_to):
        src_team = self.getting_current_turn()
        original_piece = self.getting_team(src_team).getting_piece(original_piece_num)
        pos_from = original_piece.getting_pos()
        target_team = self.getting_next_turn()
        target_piece = self.getting_team(target_team).getting_piece(target_piece_num)
        if target_piece == -1:
            target_cell = self.getting_cell_from_board([pos_from[0], pos_to[1]])
            target_cell_team = target_cell[0]
            if target_cell ==  EMPTY:
                return False
            return False
                
        is_target_empty = target_piece.getting_type() ==  EMPTY 
        if is_target_empty:
            return False
        
        if self.piece_attack(original_piece, target_piece, pos_to):
            return True
        return False    

    def piece_attack(self, original_piece, target_piece, pos_to):
        original_piece_type = original_piece.getting_type()
        if original_piece_type == HUNTER:
            if self.hunter_attack(original_piece, target_piece):
            
                return True     
        return False
    
    def hunter_attack(self,original_piece,target_piece):
        pos_from = original_piece.getting_pos()
        pos_to = target_piece.getting_pos()
        if pos_to[0]==0 or pos_to[0]==6:
            return False
        x_from, y_from = pos_from[0],pos_from[1]
        x_to, y_to = pos_to[0],pos_to[1]
        diff_x = x_to - x_from 
        diff_y = y_to - y_from
        num_steps = (abs(diff_x) + abs(diff_y))
        isOneStep = num_steps == 1
        isTwoDiagStep = (abs(diff_x) == abs(diff_y)) and num_steps == 2
        if isOneStep or isTwoDiagStep:
            return True
        return False
    


def buffalo_ai():
        board=game.gettingBoard()
        possible_board=[]
        cnt=-10000
        ans=0
        pos_from,pos_to=0,0
        for x in range(7):
            for y in range(11):
                if board[x][y]=='bb' and board[x-1][y]==EMPTY:
                    made_board,made_pos=make_buffalo_board(board,(x,y))
                    evaluate=evaluate_buffalo_board(made_board)
                    if evaluate[0]>cnt:
                        cnt=evaluate[0]
                        print(cnt)
                        ans=evaluate[1]
                        pos_from=(x,y)
                        pos_to=(x-1,y)
        print(pos_from,pos_to)
        print(board)
        game.put(pos_from,pos_to)
        print('score:',cnt)
                
def make_buffalo_board(Board,pos):
    board=copy.deepcopy(Board)
    x,y=pos
    board[x][y]=EMPTY
    board[x-1][y]='bb'
    return (board,(x-1,y))

def evaluate_buffalo_board(board):
    x_direc=[1,0,-1,1,0,-1]
    y_direc=[1,1,1,-1,-1,-1]
    right_side,left_side=0,0
    buffalo_pos=[]
    hunter_pos=0
    dog_pos=[]
    score=0
    for x in range(7):
        for y in range(11):
            if board[x][y]=='bb':
                buffalo_pos.append((x,y))
            elif board[x][y]=='hh':
                hunter_pos=[x,y]
            elif board[x][y]=='hd':
                dog_pos.append((x,y))
    for x in range(7):
        for y in range(11):
            if board[x][y]=='bb':
                if x<6 and max(abs(x-hunter_pos[0]),abs(y-hunter_pos[1]))<8:
                    for direc in range(6):
                        x_pos=x+x_direc[direc]
                        y_pos=y+y_direc[direc]
                        if 0<=x_pos<6 and 0<=y_pos<=10:
                            if board[x+x_direc[direc]][y+y_direc[direc]]=='bb':
                                score-=1
    for x,y in buffalo_pos:
        if x==0 or (x==1 and max(abs(x-hunter_pos[0]),abs(y-hunter_pos[1]))>1):
            return (100000,board)
        if x<6:
            if y<5:
                left_side+=(6-x)
            elif y>5:
                right_side+=(6-x)
            
        blocked=False
        for i in range(0,x):
            if board[i][y]!=EMPTY:
                blocked=True
                break
        if not blocked:
            if not can_catch(hunter_pos,[x,y],board,HUNTER):
            
                score+=6*(6-x)*(abs(hunter_pos[1]-y)+(abs(hunter_pos[0]-x)+(hunter_pos[0]-x))/2)
            else:
                score+=(6-x)*(abs(hunter_pos[1]-y)+(abs(hunter_pos[0]-x)+(hunter_pos[0]-x))/2)
    if hunter_pos[1]==5:
        score-=abs(left_side-right_side)
            
        
    return (score,board)







def direction_check(direction,pos_from,board,type):
    x_direc=[-1,0,1,-1,0,1,-1,1]
    y_direc=[-1,-1,-1,1,1,1,0,0]
    x,y=pos_from
    pos_to=(x+x_direc[direction],y+y_direc[direction])
    if (0<pos_to[0]<6) and (0<=pos_to[1]<11):
        if board[pos_to[0]][pos_to[1]]==EMPTY:
            return True
        elif type=="hh" and board[pos_to[0]][pos_to[1]]=="bb":
            return True
    return False

def can_catch(Hunter_pos,Buffalo_pos,board,turn):
    hunter_pos=copy.deepcopy(Hunter_pos)
    buffalo_pos=copy.deepcopy(Buffalo_pos)
    x_direc=[-1,0,1,-1,0,1]
    y_direc=[-1,-1,-1,1,1,1]

    if hunter_pos[0]>buffalo_pos[0]:
        return False
    
    if hunter_pos[1]<buffalo_pos[1]:
        direction=3
    

    elif hunter_pos[1]>buffalo_pos[1]:
        direction=0
    else:
        print('error')
        return False
    if turn==HUNTER:
        if buffalo_pos[0]<6:
            buffalo_pos[0]+=1

    
    while True:
        
        buffalo_pos[0]-=1
        if buffalo_pos[0]==0:
            return False
        if direction_check(direction,hunter_pos,board,'hh'):
            hunter_pos[0]+=x_direc[direction]
            hunter_pos[1]+=y_direc[direction]
        elif direction_check(direction+1,hunter_pos,board,'hh'):
            hunter_pos[0]+=x_direc[direction+1]
            hunter_pos[1]+=y_direc[direction+1]
        elif direction_check(direction+2,hunter_pos,board,'hh'):
            hunter_pos[0]+=x_direc[direction+2]
            hunter_pos[1]+=y_direc[direction+2]
        else:
            return False
        if hunter_pos[1]==buffalo_pos[1] and hunter_pos[0]<=buffalo_pos[0]:
            return True

def check_buffalo(buffalo_pos,board):
    x,y=buffalo_pos
    x_direc=[-1,0,1,-1,0,1]
    y_direc=[-1,-1,-1,1,1,1]
    near=0
    for direction in range(6):
        x_pos=x+x_direc[direction]
        y_pos=y+y_direc[direction]
        if 0<=x_pos<6 and 0<=y_pos<11 and board[x_pos][y_pos]=='bb':
            near+=1
    return near

def make_hunter_board(pos_from,pos_to,Board,type):
    board=copy.deepcopy(Board)
    board[pos_from[0]][pos_from[1]]=EMPTY
    board[pos_to[0]][pos_to[1]]=type
    return (board,pos_from,pos_to)

def evaluate_hunter_board(board):
    buffalo_pos=[]
    hunter_pos=0
    dog_pos=[]
    score=0
    for x in range(7):
        for y in range(11):
            if board[x][y]=='bb':
                buffalo_pos.append((x,y))
            elif board[x][y]=='hh':
                hunter_pos=[x,y]
            elif board[x][y]=='hd':
                dog_pos.append((x,y))
    buffalo_list=[i[1] for i in buffalo_pos]
    
    for x,y in buffalo_pos:
        score-=50*(6-x)

    score+=hunter_pos[0]/10
    score-=abs(hunter_pos[1]-5)/10
    row1,row2=0,0
    for x,y in dog_pos:
        if x==1:
            row1+=1
        elif x==2:
            row2+=1
    if row1==3 and row2==1:
        score+=20
    
    
 
    for x,y in buffalo_pos:
        if x==0 or (x==1 and max(abs(x-hunter_pos[0]),abs(y-hunter_pos[1]))>=1):
            return -100000
        if x in (2,3) and y==8 and board[2][7]=='hd' and board[3][7]=='bb':
            result=list(filter(lambda x:x>8,buffalo_list))
            if len(result)==2:
                if board[1][9]!='hd' or board[1][10]!='hd':
                    score-=300   

        if x in (2,3)and y==7 and board[2][8]=='hd' and board[3][8]=='bb':
            result=list(filter(lambda x:x>8,buffalo_list))
            if len(result)==2:
                if board[1][9]!='hd' or board[1][10]!='hd':
                    score-=300      
        
        if  x in (2,3) and y==2 and board[2][3]=='hd' and board[3][3]=='bb':
            result=list(filter(lambda x:x<2,buffalo_list))
            if len(result)==2:
                if board[1][0]!='hd' or board[1][1]!='hd':
                    score-=300   

        if  x in (2,3) and y==3 and board[2][2]=='hd' and board[3][2]=='bb':
            result=list(filter(lambda x:x<2,buffalo_list))
            if len(result)==2:
                if board[1][0]!='hd' or board[1][1]!='hd':
                    score-=300
        
        if  x in (2,3) and y==1:
            result=list(filter(lambda x:x<1,buffalo_list))
            if len(result)==1:
                if board[1][0]!='hd':
                    score-=300

        if  x in (2,3) and y==9:
            result=list(filter(lambda x:x>9,buffalo_list))
            if len(result)==1:
                if board[1][10]!='hd':
                    score-=300

        if x<=2:
            if not can_catch(hunter_pos,[x,y],board,BUFFALO):
                score-=20
             
        if x<6 and 0<=y<11:
            
            score+=(6-x)*10*(check_buffalo((x,y),board)+1)/(max(abs(x-hunter_pos[0]),abs(y-hunter_pos[1]))**(1/5))
            score-=(abs(hunter_pos[0]-x)+hunter_pos[0]-x)/2
        if x==3 and y in (2,3,7,8):
            if not can_catch(hunter_pos,[x,y],board,BUFFALO):
                if board[2][y]!='hd':
                    score-=50
        if x==4 and y in (2,3,7,8):
            if hunter_pos[0]==2:
                score-=2
        blocked=False
        for i in range(0,x):
            if board[i][y]!=EMPTY:
                blocked=True                
                break
        if not blocked:
            if not can_catch(hunter_pos,[x,y],board,BUFFALO):
                if x<=2:
                    return -100000
            #     score-=(6-x)
            # if can_catch(hunter_pos,[x,y],board):
            #     score-=(6-x)*max(abs(x-hunter_pos[0]),abs(y-hunter_pos[1]))/6
                
            

    return score



def hunter_ai():
    x_direc=[-1,0,1,-1,0,1,-1,1]
    y_direc=[-1,-1,-1,1,1,1,0,0]

    score=-10000000
    
    board=game.gettingBoard()
    all_board_info=[]
    for x in range(1,6):
        for y in range(11):
            if board[x][y]=="hh":
                type="hh"
                for direction in range(8):
                    x_pos=x
                    y_pos=y
                    if direction_check(direction,(x_pos,y_pos),board,"hh"):
                        x_pos+=x_direc[direction]
                        y_pos+=y_direc[direction]   

                        all_board_info.append(make_hunter_board((x,y),(x_pos,y_pos),board,type))

            elif board[x][y]=="hd":
                type="hd"
                for direction in range(8):
                    x_pos=x
                    y_pos=y
                    while direction_check(direction,(x_pos,y_pos),board,"hd"):
                        x_pos+=x_direc[direction]
                        y_pos+=y_direc[direction]

                        all_board_info.append(make_hunter_board((x,y),(x_pos,y_pos),board,type))

    for board_info in all_board_info:
        board=board_info[0]
        current_score=evaluate_hunter_board(board)
        print()
        print()
        print(current_score)
        for i in board:
            print(i)
            
        if current_score>score:
            score=current_score
            pos_from=board_info[1]
            pos_to=board_info[2]
    
    game.put(pos_from,pos_to)
    
            
            

        
        
        


    

def draw_alpha(disp, color, rect):
    rect_shape = pygame.Surface(pygame.Rect(rect).size, pygame.SRCALPHA)
    pygame.draw.rect(rect_shape, color, rect_shape.get_rect())
    disp.blit(rect_shape, rect)
        

mouse_pressed = False
mouse_clicked = False
is_src_set = False
is_target_set = False
game = buffalo_chess()
game_disp = game.gettingDisplay().gettingdisp()
pygame.display.set_caption("buffalo chess")
pygame.init()
while game.gettingRunning():
    for activation in pygame.event.get():
        if activation.type == pygame.QUIT:
            game.setRunning(False)
            break
        elif activation.type == pygame.MOUSEBUTTONDOWN:
            mouse_presses = pygame.mouse.get_pressed()
            if mouse_presses[0]:
                mouse_pressed = True
        elif activation.type == pygame.MOUSEBUTTONUP:
            if mouse_pressed:
                mouse_clicked = True
                mouse_pressed = False
                mx, my = pygame.mouse.get_pos()
            else:
                mouse_clicked = False
    if game.getting_current_turn()==BUFFALO and game.getting_p1()==BUFFALO:
        buffalo_ai()
        print('moved')
        game.setting_turn(game.getting_next_turn())

    elif game.getting_current_turn()==HUNTER and game.getting_p1()==HUNTER:
        hunter_ai()
        print('moved')
        game.setting_turn(game.getting_next_turn())
        
    else:
        if mouse_clicked:
            isValid, mi, mj = game.pixel_to_pos(board_space, board_space, mx, my, cell_pixels)
            mouse_clicked = False
            if not isValid:
                is_src_set = False
                is_target_set = False
                mouse_pressed = False
                continue
            else:
                if not is_src_set:
                    src_pos = (mi, mj)
                    src_rect = (mj * cell_pixels + board_space, \
                mi * cell_pixels + board_space, \
                    cell_pixels, cell_pixels)
                    
                    original_piece_type = game.getting_cell_from_board(src_pos)
                    is_src_set = True
                else:
                    target_pos = (mi, mj)
                    target_rect = (mj * cell_pixels + board_space,mi * cell_pixels + board_space, cell_pixels, cell_pixels)
                    target_piece_type = game.getting_cell_from_board(target_pos)
                    is_target_set = True
            if is_src_set and not is_target_set:
                possible_pos = game.get_all_possible_move(src_pos)
            if is_src_set and is_target_set:
                if game.put(src_pos, target_pos):
                    game.setting_turn(game.getting_next_turn())
                is_src_set = False
                is_target_set = False



    #drawing the board
    for i in range(height_cells):
        for j in range(width_cells):
            rect = (j * cell_pixels + board_space, i * cell_pixels + board_space, cell_pixels, cell_pixels)
            if (i + j) % 2 == 0:
                if i==0 or i==6:
                    pygame.draw.rect(game_disp, (0, 144,255), rect, 0)
                else:
                    pygame.draw.rect(game_disp, (240, 217,183), rect, 0)
            else:
                if i==0 or i==6:
                    pygame.draw.rect(game_disp, (0, 0,255), rect, 0)
                else:
                    pygame.draw.rect(game_disp, (180, 136, 102), rect, 0)

    if is_target_set:
        pygame.draw.rect(game_disp, targeted_color, target_rect, 0)
    elif is_src_set:
        draw_alpha(game_disp, piece_src_color, src_rect)
        for i, j in possible_pos:
            possible_rect = (j * cell_pixels + board_space,i * cell_pixels + board_space,cell_pixels, cell_pixels)
            draw_alpha(game_disp, piece_guide_color, possible_rect)
            pygame.draw.rect(game_disp, piece_guide_color, possible_rect, 0)

    for x in range(height_cells):
        for y in range(width_cells):
            cell_team = game.getting_cell_from_board((x,y))[0]
            cell_type = game.getting_cell_from_board((x,y))[1]
            sprite_num = -1
            if cell_type == BUFFALO:
                game_disp.blit(game.gettingDisplay().gettingBUFFALO(),\
                    (y * cell_pixels + board_space, x * cell_pixels + board_space))


            if cell_type == HUNTER:
                game_disp.blit(game.gettingDisplay().gettingHUNTER(),\
                    (y * cell_pixels + board_space, x * cell_pixels + board_space))
            elif cell_type==DOG:
                game_disp.blit(game.gettingDisplay().gettingDOG(), \
                    (y * cell_pixels + board_space, x * cell_pixels + board_space))           
    #draw score
    font=pygame.font.SysFont(None,50)
    score1=font.render('ai> buffalo:'+str(game.getting_buffalo_score('player1'))+'  hunter:'+str(game.getting_hunter_score('player1')),True,(0,0,0))
    score2=font.render('player2> buffalo:'+str(game.getting_buffalo_score('player2'))+'  hunter:'+str(game.getting_hunter_score('player2')),True,(0,0,0))
    game_disp.blit(score1,(0,0))
    game_disp.blit(score2,(game_board_height-board_space*2,0))

    #draw player position
    player1_buffalo_pos=font.render('ai',True,(139,69,19))
    player1_hunter_pos=font.render('ai',True,(0,127,255))
    player2_buffalo_pos=font.render('player2',True,(139,69,19))
    player2_hunter_pos=font.render('player2',True,(0,127,255))
    if game.getting_p1()==BUFFALO:
        game_disp.blit(player1_buffalo_pos,(500,640))
        game_disp.blit(player2_hunter_pos,(460,40))
    else:
        game_disp.blit(player2_buffalo_pos,(460,640))
        game_disp.blit(player1_hunter_pos,(500,40))
    
    #draw current turn
    turn=font.render('TURN',True,(0,255,0))
    if game.getting_current_turn()==BUFFALO:
        game_disp.blit(turn,(620,640))
    else:
        game_disp.blit(turn,(620,40))

    #end condition   

    #buffalo win
    for y in range(11):
        if game.getting_cell_from_board((0,y))[1]==BUFFALO:

            if game.getting_p1()==BUFFALO:
                game.add_buffalo_score('player1')
            else:
                game.add_buffalo_score('player2')
            game.change_player()
            game.resetting_board()
                
    
    #hunter win
    cnt=0
    live_buffalos=list(filter(lambda x:x.getting_alive()==True,game.getting_team(BUFFALO).getting_all_pieces()))
    for b in live_buffalos:
        for h in game.getting_team(HUNTER).getting_all_pieces():
            if b.getting_pos()[1]==h.getting_pos()[1] and b.getting_pos()[0]>h.getting_pos()[0]:
                cnt+=1
                continue
    if cnt==len(live_buffalos):
        if game.getting_p1()==BUFFALO:
            game.add_hunter_score('player2')
        else:
            game.add_hunter_score('player1')
        game.change_player()
        game.resetting_board()
    
    pygame.display.update()
    game_disp.fill((100,100,100))
                          

pygame.quit()
sys.exit()
