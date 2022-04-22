import pygame
import sys
from pygame.locals import *
import numpy as np


class Board:
    def __init__(self) -> None:
        self.BGCOLOR = (3,  54,  73)
        self.X_margin = int((640 - (80 * 5 + (5 - 1))) / 2)
        self.Y_margin = int(
            (480 - (80 * 5 + (5 - 1))) / 2)

        self.color = {
            "R": (255, 0, 0),
            "B": (0, 0, 255),
            "X": (0, 0, 0),
            "Y": (255, 255, 0),
            "G": (0, 255, 0),
            "W": (255, 255, 255),
            "O": (255, 165, 0)
        }
        self.border_color = (0, 0, 0)
        self.message_color = (255, 255, 255)

    def getLeftTopOfTile(self, row, column):
        top = self.Y_margin + ((row % 5) * 80)
        left = self.X_margin + ((column % 5) * 80)
        left = self.X_margin + ((column % 5) * 80)
        return (left, top)

    def start(self, boardColor, mainBoard, moves):
        pygame.init()
        self.fps_clock = pygame.time.Clock()
        self.display_surface = pygame.display.set_mode((640, 480))
        self.font_display = pygame.font.Font('freesansbold.ttf', 20)

        pygame.display.set_caption('Slide Puzzle')

        self.boardColor = boardColor
        self.mainBoard = mainBoard
        while True:
            self.drawBoard(self.mainBoard,
                           "Rubrix Race Board - Initial")
            self.checkForQuit()
            pygame.display.update()
            self.fps_clock.tick(30)

            for i in moves:
                if (i[0] < i[1] and abs(i[0] - i[1]) == 1):
                    MOVE = 'r'
                elif (i[0] > i[1] and abs(i[0] - i[1]) == 1):
                    MOVE = 'l'
                elif i[0] < i[1]:
                    MOVE = 'd'
                else:
                    MOVE = 'u'
                data = np.array(self.mainBoard.copy()).flatten()
                data2 = np.array(self.boardColor.copy()).flatten()
                self.slideAnimation(self.mainBoard, MOVE,
                                    'Click tile or press arrow keys to slide.', 8)
                data[i[0] - 1], data[i[1] - 1] = data[i[1] - 1], data[i[0] - 1]
                data2[i[0] - 1], data2[i[1] -
                                       1] = data2[i[1] - 1], data2[i[0] - 1]

                data = data.reshape(5, 5)
                data2 = data2.reshape(5, 5)
                self.mainBoard = data.tolist()
                self.boardColor = data2.tolist()
                pygame.display.update()
                self.fps_clock.tick(80)
            break

    def terminate(self):
        pygame.quit()
        sys.exit()

    def checkForQuit(self):
        for event in pygame.event.get(QUIT):
            self.terminate()
        for event in pygame.event.get(KEYUP):
            if event.key == K_ESCAPE:
                self.terminate()
            pygame.event.post(event)

    def getBlankPosition(self, board):
        for x in range(5):
            for y in range(5):
                if board[x][y] == 0:
                    return (x, y)

    def drawTile(self, color, tilex, tiley, number, adjx=0, adjy=0):
        left, top = self.getLeftTopOfTile(tilex, tiley)
        pygame.draw.rect(self.display_surface, color,
                         (left + adjx, top + adjy, 80, 80))
        textSurf = self.font_display.render(str(number), True, (0, 0, 0))
        textRect = textSurf.get_rect()
        textRect.center = left + int(80 / 2) + \
            adjx, top + int(80 / 2) + adjy
        self.display_surface.blit(textSurf, textRect)

    def makeText(self, text, color, bgcolor1, top, left):
        textSurf = self.font_display.render(text, True, color, bgcolor1)
        textRect = textSurf.get_rect()
        textRect.topleft = (top, left)
        return (textSurf, textRect)

    def drawBoard(self, board, message):
        self.display_surface.fill(self.BGCOLOR)
        if message:
            textSurf, textRect = self.makeText(
                message, self.message_color, self.BGCOLOR, 5, 5)
            self.display_surface.blit(textSurf, textRect)
        for tilex in range(len(board)):
            for tiley in range(len(board[0])):
                if board[tilex][tiley]:
                    self.drawTile(
                        self.color[self.boardColor[tilex][tiley]], tilex, tiley, board[tilex][tiley])

        left, top = self.getLeftTopOfTile(0, 0)
        width = 5 * 80
        height = 5 * 80
        pygame.draw.rect(self.display_surface, self.border_color, (left - 5,
                                                                   top - 5, width + 11, height + 11), 4)

    def slideAnimation(self, board, direction, message, animationSpeed):
        blankx, blanky = self.getBlankPosition(board)
        if direction == 'u':
            movex = blankx - 1
            movey = blanky
        elif direction == 'd':
            movex = blankx + 1
            movey = blanky
        elif direction == 'l':
            movey = blanky - 1
            movex = blankx
        elif direction == 'r':
            movey = blanky + 1
            movex = blankx
        self.drawBoard(board,  message)
        baseSurf = self.display_surface.copy()
        moveLeft, moveTop = self.getLeftTopOfTile(movex, movey)
        pygame.draw.rect(baseSurf, self.BGCOLOR, (moveLeft,
                                                  moveTop, 80, 80))

        for i in range(0, 80, animationSpeed):
            self.checkForQuit()
            self.display_surface.blit(baseSurf, (0, 0))
            if direction == 'u':
                self.drawTile(self.color[self.boardColor[movex][movey]], movex, movey,
                              board[movex][movey], 0, i)
            if direction == 'd':
                self.drawTile(self.color[self.boardColor[movex][movey]], movex, movey,
                              board[movex][movey], 0, -i)
            if direction == 'l':
                self.drawTile(self.color[self.boardColor[movex][movey]], movex, movey,
                              board[movex][movey], i, 0)
            if direction == 'r':
                self.drawTile(self.color[self.boardColor[movex][movey]], movex, movey,
                              board[movex][movey], -i, 0)
            pygame.display.update()
            self.fps_clock.tick(100)


