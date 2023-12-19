from buffalo_chess_piece import *

class Display:
    def __init__(self):
        self.disp=pygame.display.set_mode((game_board_width,game_board_height),pygame.DOUBLEBUF)
        self.buffalo_img=pygame.image.load(BUFFALO_IMAGE_PATH)
        self.hunter_img=pygame.image.load(HUNTER_IMAGE_PATH)
        self.dog_img=pygame.image.load(DOG_IMAGE_PATH)

    def gettingdisp(self):
        return self.disp
    def gettingBUFFALO(self):
        return self.buffalo_img
    def gettingHUNTER(self):
        return self.hunter_img
    def gettingDOG(self):
        return self.dog_img 
