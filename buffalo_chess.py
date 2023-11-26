import sys
import math
import pygame

BUFFALO='b'
HUNTER='h'
DOG='d'
EMPTY = '00'
BUFFALO_IMAGE_PATH="./buffalo.png"
HUNTER_IMAGE_PATH="./hunter.png"
DOG_IMAGE_PATH="./dog.png"


piece_src_color = (10, 10, 240, 150)
piece_guide_color = (10, 250, 10, 60)
targeted_color = (80, 80, 240)
cell_pixels = 80
width_cells = 11
height_cel= 7
board_space = 80
game_board_height = cell_pixels * height_cel + board_space * 2
game_board_width = cell_pixels * width_cells + board_space * 2


class Piece:
    def __init__(self,TEAM,type,pos):
        self.alive=True
        self.moved=False
        self.team=TEAM
        self.type=type
        self.pos=pos

    def getting_alive(self):
        return self.alive
    
    def setting_alive(self,alive):
        self.alive=alive
   
    def getting_type(self):
        return self.type
    
    def setting_type(self,type):
        self.type=type
    
    def getting_moved(self):
        return self.moved
    
    def setting_moved(self,moved):
        self.moved=moved

    def getting_team(self):
        return self.team 
    
    def getting_pos(self):
        return self.pos
    
    def setting_pos(self,pos):
        self.pos=pos