# Author: Karan Shah
# Date:2/16/2022
# University: University at Buffalo, The State University of New York
# Rubik's Race Colour Detection

#import pacakges
import black
import cv2
from cv2 import inRange
import numpy as np
import time
import pygame
import sys
import random
from pygame.locals import *

hsv = []
color_tile9 = []
color_tile25 = []
color_state = []

tile_25 = {
    'tile': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white'],
}

tile_9 = {
    'tile': ['white', 'white', 'white', 'white', 'white', 'white', 'white', 'white', 'white'],
}

color = {
    'white': (255, 255, 255),
    'blue': (255, 0, 0),
    'green': (0, 255, 0),
    'yellow': (0, 255, 255),
    'red': (0, 0, 255),
    'orange': (0, 165, 255),
    'black': (0, 0, 0),
}

stickers = {
    # 'tile_9': [
    #     [140, 130], [240, 130], [340, 130],
    #     [140, 230], [240, 230], [340, 230],
    #     [140, 330], [240, 330], [340, 330]
    # ],
    'tile_9': [
        [370, 210], [460, 210], [550, 210],
        [370, 290], [460, 290], [550, 290],
        [370, 380], [460, 380], [550, 380]
    ],
    'prev_9': [
        [10, 10], [30, 10], [50, 10],
        [10, 30], [30, 30], [50, 30],
        [10, 50], [30, 50], [50, 50]
    ],
    # 'tile_25': [
    #     [200, 80], [280, 80], [360, 80], [440, 80], [520, 80],
    #     [200, 155], [280, 155], [360, 155], [440, 155], [520, 155],
    #     [200, 230], [280, 230], [360, 230], [440, 230], [520, 230],
    #     [200, 305], [280, 305], [360, 305], [440, 305], [520, 305],
    #     [200, 380], [280, 380], [360, 380], [440, 380], [520, 380],
    # ],
    'tile_25': [
        [130, 80], [270, 80], [395, 80], [500, 80], [620, 80],
        [130, 180], [270, 180], [395, 180], [500, 180], [620, 180],
        [130, 290], [270, 290], [395, 290], [500, 290], [620, 290],
        [130, 410], [270, 410], [395, 410], [500, 410], [620, 410],
        [130, 530], [270, 530], [395, 530], [500, 530], [620, 530],
    ],
    'prev_25': [
        [20, 10], [40, 10], [60, 10], [80, 10], [100, 10],
        [20, 30], [40, 30], [60, 30], [80, 30], [100, 30],
        [20, 50], [40, 50], [60, 50], [80, 50], [100, 50],
        [20, 70], [40, 70], [60, 70], [80, 70], [100, 70],
        [20, 90], [40, 90], [60, 90], [80, 90], [100, 90]
    ],
}


def colour_detection(h, s, v):
    # color_dict_HSV = {'black': [[180, 255, 30], [0, 0, 0]],
    # 'white': [[180, 18, 255], [0, 0, 231]],
    # 'red1': [[180, 255, 255], [159, 50, 70]],
    # 'red2': [[9, 255, 255], [0, 50, 70]],
    # 'green': [[89, 255, 255], [36, 50, 70]],
    # 'blue': [[128, 255, 255], [90, 50, 70]],
    # 'yellow': [[35, 255, 255], [25, 50, 70]],
    # 'purple': [[158, 255, 255], [129, 50, 70]],
    # 'orange': [[24, 255, 255], [10, 50, 70]],
    # 'gray': [[180, 18, 230], [0, 0, 40]]}
    #print([h, s, v])
    if(h >= 0 and h < 9) and (s >= 50 and s <= 255) and (v >= 70 and v <= 255):
        return 'orange'
    elif(h >= 9 and h <= 20) and (s >= 50 and s <= 255) and (v >= 70 and v <= 255):
        return 'orange'
    # elif(h>=0 and h <=180) and (s>=0 and s<=18) and (v>=170 and v<=255):
    elif(h >= 0 and h <= 180) and (s >= 0 and s <= 35) and (v >= 140 and v <= 255):
        return 'white'
    elif(h > 20 and h <= 35) and (s >= 50 and s <= 255):
        return 'yellow'
    elif(h >= 39 and h <= 89) and (s >= 50 and s <= 255):
        return 'green'
    elif(h >= 90 and h <= 128) and (s >= 50 and s <= 255) and (v >= 70 and v <= 255):
        return 'blue'
    elif(h >= 159 and h <= 180) and (s >= 50 and s <= 255):
        return 'red'
    else:
        return 'black'


def draw(image, sticker_name):
    for x, y in stickers[sticker_name]:
        cv2.rectangle(image, (x, y), (x + 10, y + 10), (255, 255, 0), 2)


def draw_tile(tile, image, sticker_name):
    for i in range(tile):
        hsv.append(image[stickers[sticker_name][i][1] + 10]
                   [stickers[sticker_name][i][0] + 10])


def draw_prev(image, sticker_name):
    a = 0
    for x, y in stickers[sticker_name]:
        colour = colour_detection(hsv[a][0], hsv[a][1], hsv[a][2])
        cv2.rectangle(image, (x, y), (x + 10, y + 10), color[colour], -1)
        a += 1
        if(sticker_name == 'prev_9'):
            color_tile9.append(colour)
        elif(sticker_name == 'prev_25'):
            color_tile25.append(colour)

###########################################################


# Create the constants (go ahead and experiment with different values)
BOARDWIDTH = 5  # number of columns in the board
BOARDHEIGHT = 5  # number of rows in the board
TILESIZE = 80
WINDOWWIDTH = 640
WINDOWHEIGHT = 480
FPS = 30
BLANK = None

#                 R    G    B
BLACK = (0,   0,   0)
WHITE = (255, 0, 255)
BRIGHTBLUE = (0,  50, 255)
DARKTURQUOISE = (3,  54,  73)
#DARKTURQUOISE = (  0,   0,   0)
GREEN = (0, 204,   0)

BGCOLOR = DARKTURQUOISE
TILECOLOR = GREEN
TEXTCOLOR = WHITE
BORDERCOLOR = BRIGHTBLUE
BASICFONTSIZE = 20

BUTTONCOLOR = WHITE
BUTTONTEXTCOLOR = BLACK
MESSAGECOLOR = WHITE

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int(
    (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'

flag_status = 0


def main():
    global FPSCLOCK, DISPLAYSURF, BASICFONT, RESET_SURF, RESET_RECT, NEW_SURF, NEW_RECT, SOLVE_SURF, SOLVE_RECT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    # Store the option buttons and their rectangles in OPTIONS.
    RESET_SURF, RESET_RECT = makeText(
        'Reset',    TEXTCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 90)
    NEW_SURF,   NEW_RECT = makeText(
        'New Game', TEXTCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 60)
    SOLVE_SURF, SOLVE_RECT = makeText(
        'Solve',    TEXTCOLOR, WINDOWWIDTH - 120, WINDOWHEIGHT - 30)

    mainBoard, solutionSeq = generateNewPuzzle(1)
    # a solved board is the same as the board in a start state.
    SOLVEDBOARD = getSolvedBoard()
    allMoves = []  # list of moves made from the solved configuration
    print('mainBoard', mainBoard)
    print('solvedBoard', SOLVEDBOARD)

    # while True: # main game loop
    #     slideTo = None # the direction, if any, a tile should slide
    #     msg = 'Click tile or press arrow keys to slide.' # contains the message to show in the upper left corner.
    #     if mainBoard == SOLVEDBOARD:
    #         msg = 'Solved!'

    #     drawBoard(mainBoard, msg)

    #     checkForQuit()
    #     for event in pygame.event.get(): # event handling loop
    #         if event.type == MOUSEBUTTONUP:
    #             spotx, spoty = getSpotClicked(mainBoard, event.pos[0], event.pos[1])

    #             if (spotx, spoty) == (None, None):
    #                 # check if the user clicked on an option button
    #                 if RESET_RECT.collidepoint(event.pos):
    #                     #resetAnimation(mainBoard, allMoves) # clicked on Reset button
    #                     allMoves = []
    #                 elif NEW_RECT.collidepoint(event.pos):
    #                     mainBoard, solutionSeq = generateNewPuzzle(80) # clicked on New Game button
    #                     allMoves = []
    #                 elif SOLVE_RECT.collidepoint(event.pos):
    #                     #resetAnimation(mainBoard, solutionSeq + allMoves) # clicked on Solve button
    #                     allMoves = []
    #             else:
    #                 # check if the clicked tile was next to the blank spot

    #                 blankx, blanky = getBlankPosition(mainBoard)
    #                 if spotx == blankx + 1 and spoty == blanky:
    #                     slideTo = LEFT
    #                 elif spotx == blankx - 1 and spoty == blanky:
    #                     slideTo = RIGHT
    #                 elif spotx == blankx and spoty == blanky + 1:
    #                     slideTo = UP
    #                 elif spotx == blankx and spoty == blanky - 1:
    #                     slideTo = DOWN

    #         elif event.type == KEYUP:
    #             # check if the user pressed a key to slide a tile
    #             if event.key in (K_LEFT, K_a) and isValidMove(mainBoard, LEFT):
    #                 slideTo = LEFT
    #             elif event.key in (K_RIGHT, K_d) and isValidMove(mainBoard, RIGHT):
    #                 slideTo = RIGHT
    #             elif event.key in (K_UP, K_w) and isValidMove(mainBoard, UP):
    #                 slideTo = UP
    #             elif event.key in (K_DOWN, K_s) and isValidMove(mainBoard, DOWN):
    #                 slideTo = DOWN

    #     if slideTo:
    #         slideAnimation(mainBoard, slideTo, 'Click tile or press arrow keys to slide.', 8) # show slide on screen
    #         makeMove(mainBoard, slideTo)
    #         allMoves.append(slideTo) # record the slide
    #     pygame.display.update()
    #     FPSCLOCK.tick(FPS)


def terminate():
    pygame.quit()
    sys.exit()


def checkForQuit():
    for event in pygame.event.get(QUIT):  # get all the QUIT events
        terminate()  # terminate if any QUIT events are present
    for event in pygame.event.get(KEYUP):  # get all the KEYUP events
        if event.key == K_ESCAPE:
            terminate()  # terminate if the KEYUP event was for the Esc key
        pygame.event.post(event)  # put the other KEYUP event objects back


def getStartingBoard():
    # Return a board data structure with tiles in the solved state.
    # For example, if BOARDWIDTH and BOARDHEIGHT are both 3, this function
    # returns [[1, 4, 7], [2, 5, 8], [3, 6, BLANK]]
    board = []
    column = []
    counter = 1
    for i in range(1, (BOARDHEIGHT * BOARDWIDTH) + 1):
        if(color_tile25[i-1] == 'black'):
            column.append(BLANK)
        else:
            column.append(counter)
            counter += 1
        if(i % 5 == 0):
            board.append(column)
            column = []
    return board


def getSolvedBoard():
    solvedBoard = []
    solvedColumn = []
    solvedcounter = 1
    for i in range(1, (BOARDHEIGHT * BOARDWIDTH) + 1):
        solvedColumn.append(solvedcounter)
        solvedcounter += 1
        if(i % 5 == 0):
            solvedBoard.append(solvedColumn)
            solvedColumn = []
    solvedBoard[BOARDHEIGHT - 1][BOARDWIDTH - 1] = BLANK
    return solvedBoard


def getBlankPosition(board):
    # Return the x and y of board coordinates of the blank space.
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    # This function does not check if the move is valid.
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx -
                                     1][blanky] = board[blankx - 1][blanky], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx +
                                     1][blanky] = board[blankx + 1][blanky], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx][blanky -
                                             1] = board[blankx][blanky - 1], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx][blanky +
                                             1] = board[blankx][blanky + 1], board[blankx][blanky]
    print(board)


def isValidMove(board, move):
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


# def getRandomMove():
#     return


def getLeftTopOfTile(tileX, tileY):
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    # from the x & y pixel coordinates, get the x & y board coordinates
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    # draw a tile at board coordinates tilex and tiley, optionally a few
    # pixels over (determined by adjx and adjy)
    left, top = getLeftTopOfTile(tilex, tiley)
    if flag_status == 0:
        pygame.draw.rect(
            DISPLAYSURF, color_tile25[number - 1], (left + adjx, top + adjy, TILESIZE, TILESIZE))
    elif flag_status == 1:
        pygame.draw.rect(
            DISPLAYSURF, color_tile25[number], (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + \
        adjx, top + int(TILESIZE / 2) + adjy
    DISPLAYSURF.blit(textSurf, textRect)


def makeText(text, color, top, left):
    # create the Surface and Rect objects for some text.
    textSurf = BASICFONT.render(text, True, color)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    global flag_status
    DISPLAYSURF.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, 5, 5)
        DISPLAYSURF.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if(board[tilex][tiley]):
                if(color_tile25[board[tilex][tiley] - 1] == 'black'):
                    flag_status = 1
                drawTile(tilex, tiley, board[tiley][tilex])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(DISPLAYSURF, BORDERCOLOR, (left - 5,
                     top - 5, width + 11, height + 11), 4)

    DISPLAYSURF.blit(RESET_SURF, RESET_RECT)
    DISPLAYSURF.blit(NEW_SURF, NEW_RECT)
    DISPLAYSURF.blit(SOLVE_SURF, SOLVE_RECT)


def slideAnimation(board, direction, message, animationSpeed):
    # Note: This function does not check if the move is valid.

    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # prepare the base surface
    drawBoard(board, message)
    baseSurf = DISPLAYSURF.copy()
    # draw a blank space over the moving tile on the baseSurf Surface.
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft,
                     moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # animate the tile sliding over
        checkForQuit()
        DISPLAYSURF.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


def generateNewPuzzle(numSlides):
    # From a starting configuration, make numSlides number of moves (and
    # animate these moves).
    sequence = []
    board = getStartingBoard()
    print(board)
    drawBoard(board, '')
    pygame.display.update()
    pygame.time.wait(500)  # pause 500 milliseconds for effect
    # Get Randomizer here
    # Randomizer() func
    return board, sequence


def resetAnimation(board, allMoves):
    # make all of the moves in allMoves in reverse.
    revAllMoves = allMoves[:]  # gets a copy of the list
    print(revAllMoves)
    revAllMoves.reverse()

    for move in revAllMoves:
        if move == UP:
            oppositeMove = DOWN
        elif move == DOWN:
            oppositeMove = UP
        elif move == RIGHT:
            oppositeMove = LEFT
        elif move == LEFT:
            oppositeMove = RIGHT
        slideAnimation(board, oppositeMove, '',
                       animationSpeed=int(TILESIZE / 2))
        makeMove(board, oppositeMove)

##########################################################


if __name__ == '__main__':
    img9 = cv2.imread("Images/9_tile_2.png")
    img25 = cv2.imread("Images/25_tile_3.png")
    tile_9image = cv2.cvtColor(img9, cv2.COLOR_BGR2HSV)
    tile_25image = cv2.cvtColor(img25, cv2.COLOR_BGR2HSV)

    draw(img9, 'tile_9')
    draw(img9, 'prev_9')
    draw(img25, 'tile_25')
    draw(img25, 'prev_25')

    draw_tile(9, tile_9image, 'tile_9')
    draw_prev(img9, 'prev_9')
    hsv = []
    draw_tile(25, tile_25image, 'tile_25')
    draw_prev(img25, 'prev_25')

    cv2.imshow("Goal State Image", img9[0:900, 0:900])
    cv2.imshow("Pattern Image", img25[0:900, 0:900])

    print("Tile_9", color_tile9)
    print("Tile_25", color_tile25)

    main()

    if cv2.waitKey(0) & 0xFF == 27:
        cv2.destroyAllWindows()


###########################################################################
