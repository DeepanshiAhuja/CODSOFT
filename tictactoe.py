import copy
import sys
import pygame
import random
import numpy as np
from numerials import *
pygame.init()
screen = pygame.display.set_mode( (width, height) )
pygame.display.set_caption('TIC TAC TOE AI')
screen.fill( bgColor )
class Board:

    def __init__(self):
        self.squares = np.zeros( (rows, cols) )
        self.empty_sqrs = self.squares 
        self.marked_sqrs = 0

    def finalState(self, show=False):
       

        for col in range(cols):
            if self.squares[0][col] == self.squares[1][col] == self.squares[2][col] != 0:
                if show:
                    color = circColor if self.squares[0][col] == 2 else crossColor 
                    iPos = (col * SQSIZE + SQSIZE // 2, 20)
                    fPos = (col * SQSIZE + SQSIZE // 2, height - 20)
                    pygame.draw.line(screen, color, iPos, fPos, lineWidth )
                return self.squares[0][col]
        for row in range(rows):
            if self.squares[row][0] == self.squares[row][1] == self.squares[row][2] != 0:
                if show:
                    color =circColor if self.squares[row][0] == 2 else crossColor 
                    iPos = (20, row * SQSIZE + SQSIZE // 2)
                    fPos = (width - 20, row * SQSIZE + SQSIZE // 2)
                    pygame.draw.line(screen, color, iPos, fPos, lineWidth )
                return self.squares[row][0]
        if self.squares[0][0] == self.squares[1][1] == self.squares[2][2] != 0:
            if show:
                color = circColor if self.squares[1][1] == 2 else crossColor 
                iPos = (20, 20)
                fPos = (width - 20, height - 20)
                pygame.draw.line(screen, color, iPos, fPos, crossWidth)
            return self.squares[1][1]
        if self.squares[2][0] == self.squares[1][1] == self.squares[0][2] != 0:
            if show:
                color = circColor if self.squares[1][1] == 2 else crossColor 
                iPos = (20,height - 20)
                fPos = (width - 20, 20)
                pygame.draw.line(screen, color, iPos, fPos, crossWidth)
            return self.squares[1][1]
        return 0
    def mark_sqr(self, row, col, player):
        self.squares[row][col] = player
        self.marked_sqrs += 1

    def empty_sqr(self, row, col):
        return self.squares[row][col] == 0

    def get_empty_sqrs(self):
        empty_sqrs = []
        for row in range(rows):
            for col in range(cols):
                if self.empty_sqr(row, col):
                    empty_sqrs.append( (row, col) )
        
        return empty_sqrs

    def isfull(self):
        return self.marked_sqrs == 9

    def isempty(self):
        return self.marked_sqrs == 0

class AI:

    def __init__(self, level=1, player=2):
        self.level = level
        self.player = player


    def rnd(self, board):
        empty_sqrs = board.get_empty_sqrs()
        idx = random.randrange(0, len(empty_sqrs))

        return empty_sqrs[idx]
  
    def minimax(self, board, maximizing):
        
     
        case = board.finalState()

       
        if case == 1:
            return 1, None 
   
        if case == 2:
            return -1, None

  
        elif board.isfull():
            return 0, None

        if maximizing:
            max_eval = -100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, 1)
                eval = self.minimax(temp_board, False)[0]
                if eval > max_eval:
                    max_eval = eval
                    best_move = (row, col)

            return max_eval, best_move

        elif not maximizing:
            min_eval = 100
            best_move = None
            empty_sqrs = board.get_empty_sqrs()

            for (row, col) in empty_sqrs:
                temp_board = copy.deepcopy(board)
                temp_board.mark_sqr(row, col, self.player)
                eval = self.minimax(temp_board, True)[0]
                if eval < min_eval:
                    min_eval = eval
                    best_move = (row, col)

            return min_eval, best_move



    def eval(self, main_board):
        if self.level == 0:
        
            eval = 'random'
            move = self.rnd(main_board)
        else:
        
            eval, move = self.minimax(main_board, False)

        print(move,eval)

        return move 

class Game:

    def __init__(self):
        self.board = Board()
        self.ai = AI()
        self.player = 1   
        self.gamemode = 'ai' 
        self.running = True
        self.showLines()

  

    def showLines(self):
      
        screen.fill( bgColor )

      
        pygame.draw.line(screen, lineColor, (SQSIZE, 0), (SQSIZE, height), lineWidth )
        pygame.draw.line(screen, lineColor, (width - SQSIZE, 0), (width- SQSIZE, height), lineWidth )

 
        pygame.draw.line(screen, lineColor, (0, SQSIZE), (width, SQSIZE), lineWidth )
        pygame.draw.line(screen, lineColor, (0, height - SQSIZE), (width, height - SQSIZE),lineWidth )

    def drawFig(self, row, col):
        if self.player == 1:
           
            start_desc = (col * SQSIZE + OFFSET, row * SQSIZE + OFFSET)
            end_desc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            pygame.draw.line(screen,crossColor , start_desc, end_desc, crossWidth)
          
            start_asc = (col * SQSIZE + OFFSET, row * SQSIZE + SQSIZE - OFFSET)
            end_asc = (col * SQSIZE + SQSIZE - OFFSET, row * SQSIZE + OFFSET)
            pygame.draw.line(screen, crossColor , start_asc, end_asc,crossWidth)
        
        elif self.player == 2:
       
            center = (col * SQSIZE + SQSIZE // 2, row * SQSIZE + SQSIZE // 2)
            pygame.draw.circle(screen, circColor, center, RADIUS, crossWidth)



    def makeMove(self, row, col):
        self.board.mark_sqr(row, col, self.player)
        self.drawFig(row, col)
        self.nextTurn()

    def nextTurn(self):
        self.player = self.player % 2 + 1

    def changeGamemode(self):
        self.gamemode = 'ai' if self.gamemode == 'pvp' else 'pvp'

    def isover(self):
        return self.board.finalState(show=True) != 0 or self.board.isfull()

    def reset(self):
        self.__init__()

def main():


    game = Game()
    board = game.board
    ai = game.ai


    while True:
        
       
        for event in pygame.event.get():

          
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

         
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_g:
                    game.changeGamemode()

            
                if event.key == pygame.K_r:
                    game.reset()
                    board = game.board
                    ai = game.ai

            
                if event.key == pygame.K_0:
                    ai.level = 0
                
     
                if event.key == pygame.K_1:
                    ai.level = 1

  
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = event.pos
                row = pos[1] // SQSIZE
                col = pos[0] // SQSIZE
                
        
                if board.empty_sqr(row, col) and game.running:
                    game.makeMove(row, col)

                    if game.isover():
                        game.running = False


        if game.gamemode == 'ai' and game.player == ai.player and game.running:

      
            pygame.display.update()

            row, col = ai.eval(board)
            game.makeMove(row, col)

            if game.isover():
                game.running = False
            
        pygame.display.update()

main()