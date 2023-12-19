from buffalo_chess_piece import *

class Team:
    def __init__(self,TEAM):
        self.team=TEAM
        self.pieces=[]
        self.setting_initial_pos()
    
    def setting_initial_pos(self):
        if self.team==BUFFALO:
            for y in range(11):
                self.pieces.append(Piece(self.team,BUFFALO,[6,y]))
        else:
            for y in [1,2,4,5]:
                self.pieces.append(Piece(self.team,DOG,[1,y+2]))
            self.pieces.append(Piece(self.team,HUNTER,[1,5]))
    
    def getting_all_pieces(self):
        return self.pieces
    
    def getting_piece(self, piece_num):
        if piece_num >= 0:
            return self.pieces[piece_num]
        else:
            return -1
