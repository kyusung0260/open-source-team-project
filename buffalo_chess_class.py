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
        for x in range(height_cel):
            row = []
            for y in range(width_cells):
                row.append(EMPTY)
            self.board.append(row)
    
    def erase_board(self):
        for x in range(height_cel):
            for y in range(width_cells):
                self.board[x][y]=EMPTY
    
    def check_valid_pos(self,pos):
        x,y=pos[0],pos[1]
        if (x >= 0 and x <= 6) and (x >= 0 and y <= 10):
            return True
        return False