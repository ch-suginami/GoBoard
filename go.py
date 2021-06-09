'''
MIT License

Copyright (c) 2021 Masanori Hirata(ch-suginami)

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

from PIL import Image, ImageDraw, ImageFont
import sys, os

BOARD_COORDS = 9
BOARD_SIZE = BOARD_COORDS
FIG_SIZE = 750
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
FRAME_LEFT = 70
FRAME_TOP = 70
BETWEEN = 80
LINE_WIDTH = 2
DOTS  = 5
STONE = 33
ALPHABET_U = [chr(ord('A') + i) for i in range(26)]
ALPHABET_L = [chr(ord('a') + i) for i in range(26)]
DIREC = [[-1, 0], [0, 1], [1, 0], [0, -1]]

# font setting
font_coords = ImageFont.truetype('SourceHanSans-Normal.otf', 36)
font_num = ImageFont.truetype('SourceHanSans-Normal.otf', 46)

class board:
    # initializing
    def __init__(self):
        self.board = [[' ' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.check_board = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

    # clearing
    def clear_check(self):
        self.check_board = [[False for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        return self.check_board

    # checking dame at that position
    def check_dame(self, x, y, color):
        #already checked
        if self.check_board[x][y]:
            return True

        # marking
        self.check_board[x][y] = True

        # empty position
        if self.board[x][y] == ' ':
            return False

        for dx, dy in DIREC:
            ddx = dx + x
            ddy = dy + y
            if 0 <= ddx < BOARD_SIZE and 0 <= ddy < BOARD_SIZE:
                if self.board[ddx][ddy] != color:
                    stone = self.check_dame(ddx, ddy, color)
                    if stone == False:
                        return False

        return True

    # remove stones action
    def remove_act(self, x, y, color):
        if self.check_board[x][y]:
            self.board[x][y] = ' '

            for dx, dy in DIREC:
                ddx = x + dx
                ddy = y + dy
                if 0 <= ddx < BOARD_SIZE and 0 <= ddy < BOARD_SIZE:
                    self.board = self.remove_act(ddx, ddy, color)

        return self.board

    # remove stones
    def remove_stone(self, x, y, color):
        # same stone color
        if self.board[x][y] == color:
            return self.board

        # empty
        if self.board[x][y] == ' ':
            return self.board

        self.check_board = self.clear_check()

        # different color
        if self.check_dame(x, y, color):
            self.board = self.remove_act(x, y, color)

        return self.board

    def put_stone(self, pos_x, pos_y, color):
        # put black
        if color == 'B':
            self.board[pos_x][pos_y] = 'b'
            for x, y in DIREC:
                dx = pos_x + x
                dy = pos_y + y
                if 0 <= dx < BOARD_SIZE and 0 <= dy < BOARD_SIZE:
                    self.board = self.remove_stone(dx, dy, 'b')
        # put white
        else:
            self.board[pos_x][pos_y] = 'w'
            for x, y in DIREC:
                dx = pos_x + x
                dy = pos_y + y
                if 0 <= dx < BOARD_SIZE and 0 <= dy < BOARD_SIZE:
                    self.board = self.remove_stone(dx, dy, 'w')
        return self.board

# drawing lines
def draw_pos(drawing):
    for i in range(BOARD_COORDS):
        if i == 0 or i == 8:
            drawing.line((FRAME_LEFT + i*BETWEEN, FRAME_TOP - LINE_WIDTH, FRAME_LEFT + i*BETWEEN, FRAME_TOP + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH), fill = BLACK, width = 5)
            drawing.line((FRAME_LEFT - LINE_WIDTH, FRAME_TOP + i*BETWEEN, FRAME_LEFT + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH, FRAME_TOP + i*BETWEEN), fill = BLACK, width = 5)
        else:
            drawing.line((FRAME_LEFT + i*BETWEEN, FRAME_TOP, FRAME_LEFT + i*BETWEEN, FRAME_TOP + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH), fill = BLACK, width = 1)
            drawing.line((FRAME_LEFT, FRAME_TOP + i*BETWEEN, FRAME_LEFT + (BOARD_COORDS-1)*BETWEEN + LINE_WIDTH, FRAME_TOP + i*BETWEEN), fill = BLACK, width = 1)
    # drawing dots
    drawing.ellipse((FRAME_LEFT + 2*BETWEEN - DOTS, FRAME_TOP + 2*BETWEEN - DOTS, FRAME_LEFT + 2*BETWEEN + DOTS, FRAME_TOP + 2*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 2*BETWEEN - DOTS, FRAME_TOP + 6*BETWEEN - DOTS, FRAME_LEFT + 2*BETWEEN + DOTS, FRAME_TOP + 6*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 6*BETWEEN - DOTS, FRAME_TOP + 2*BETWEEN - DOTS, FRAME_LEFT + 6*BETWEEN + DOTS, FRAME_TOP + 2*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 6*BETWEEN - DOTS, FRAME_TOP + 6*BETWEEN - DOTS, FRAME_LEFT + 6*BETWEEN + DOTS, FRAME_TOP + 6*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    drawing.ellipse((FRAME_LEFT + 4*BETWEEN - DOTS, FRAME_TOP + 4*BETWEEN - DOTS, FRAME_LEFT + 4*BETWEEN + DOTS, FRAME_TOP + 4*BETWEEN + DOTS), fill = BLACK, outline = BLACK)
    return drawing

# drawing letters of coordinates
def draw_letters(drawing):
    for i in range(1, BOARD_COORDS + 1):
        drawing.text((15, (BOARD_COORDS - i)*BETWEEN + 41), str(i), font = font_coords, fill = BLACK)
        drawing.text((i*BETWEEN - 20, -10), ALPHABET_U[i-1], font = font_coords, fill = BLACK)
    return drawing

# convert alphabet to number
def conv2num(letter):
    if letter.islower():
        return ALPHABET_L.index(letter)
    else:
        return ALPHABET_U.index(letter)

# drawing stones
def draw_stones(drawing, board, last_pos, num = None, flag = True):
    DIFF = 8
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            last = False
            if last_pos[0] == i and last_pos[1] == j:
                last = True
            if board[i][j] == 'b':
                drawing.ellipse((FRAME_LEFT + j*BETWEEN - STONE, FRAME_TOP + i*BETWEEN - STONE, FRAME_LEFT + j*BETWEEN + STONE, FRAME_TOP + i*BETWEEN + STONE), fill = BLACK, outline = BLACK)
                if last and num is not None:
                    if num >= 10:
                        drawing.text((FRAME_LEFT + j*BETWEEN - STONE//2, FRAME_TOP + i*BETWEEN - STONE), str(num), font = font_num, fill = WHITE)
                    elif 0 < num < 10:
                        drawing.text((FRAME_LEFT + j*BETWEEN - STONE//3, FRAME_TOP + i*BETWEEN - STONE), str(num), font = font_num, fill = WHITE)
                if last and flag:
                    drawing.ellipse((FRAME_LEFT + j*BETWEEN - int(DOTS*0.7), FRAME_TOP + i*BETWEEN - STONE//2 - int(DOTS*0.7) - DIFF, FRAME_LEFT + j*BETWEEN + int(DOTS*0.7), FRAME_TOP + i*BETWEEN - STONE//2 + int(DOTS*0.7) - DIFF), fill = WHITE, outline = BLACK)
            elif board[i][j] == 'w':
                drawing.ellipse((FRAME_LEFT + j*BETWEEN - STONE, FRAME_TOP + i*BETWEEN - STONE, FRAME_LEFT + j*BETWEEN + STONE, FRAME_TOP + i*BETWEEN + STONE), fill = WHITE, outline = BLACK)
                if last and num is not None:
                    if num >= 10:
                        drawing.text((FRAME_LEFT + j*BETWEEN - STONE//2, FRAME_TOP + i*BETWEEN - STONE), str(num), font = font_num, fill = BLACK)
                    elif 0 < num < 10:
                        drawing.text((FRAME_LEFT + j*BETWEEN - STONE//3, FRAME_TOP + i*BETWEEN - STONE), str(num), font = font_num, fill = BLACK)
                if last and flag:
                    drawing.ellipse((FRAME_LEFT + j*BETWEEN - int(DOTS*0.7), FRAME_TOP + i*BETWEEN - STONE//2 - int(DOTS*0.7) - DIFF, FRAME_LEFT + j*BETWEEN + int(DOTS*0.7), FRAME_TOP + i*BETWEEN - STONE//2 + int(DOTS*0.7) - DIFF), fill = BLACK, outline = BLACK)
    return drawing

# drawing stones
def draw_num_stones(drawing, board, pos_i):
    # no number
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == 'b':
                drawing.ellipse((FRAME_LEFT + j*BETWEEN - STONE, FRAME_TOP + i*BETWEEN - STONE, FRAME_LEFT + j*BETWEEN + STONE, FRAME_TOP + i*BETWEEN + STONE), fill = BLACK, outline = BLACK)
            elif board[i][j] == 'w':
                drawing.ellipse((FRAME_LEFT + j*BETWEEN - STONE, FRAME_TOP + i*BETWEEN - STONE, FRAME_LEFT + j*BETWEEN + STONE, FRAME_TOP + i*BETWEEN + STONE), fill = WHITE, outline = BLACK)

    # write number
    for i in range(len(pos_i)):
        num = pos_i[i][0]
        x = pos_i[i][1]
        y = pos_i[i][2]
        DIFFX = -1
        DIFFY = -4
        if board[x][y] == 'b':
            if int(num) >= 10:
                drawing.text((FRAME_LEFT + y*BETWEEN - STONE//2 + DIFFX*8, FRAME_TOP + x*BETWEEN - STONE + DIFFY), num, font = font_num, fill = WHITE)
            elif 0 < int(num) < 10:
                drawing.text((FRAME_LEFT + y*BETWEEN - STONE//3 + DIFFX, FRAME_TOP + x*BETWEEN - STONE + DIFFY), num, font = font_num, fill = WHITE)
        elif board[x][y] == 'w':
            if int(num) >= 10:
                drawing.text((FRAME_LEFT + y*BETWEEN - STONE//2 + DIFFX*8, FRAME_TOP + x*BETWEEN - STONE + DIFFY), num, font = font_num, fill = BLACK)
            elif 0 < int(num) < 10:
                drawing.text((FRAME_LEFT + y*BETWEEN - STONE//3 + DIFFX, FRAME_TOP + x*BETWEEN - STONE + DIFFY), num, font = font_num, fill = BLACK)

    return drawing

# draw letters for explanations
def draw_tree(drawing, pos_x, pos_y, letter):
    BOX = 25
    DIFFX = 5
    DIFFY = 12
    drawing.rectangle((FRAME_LEFT + pos_x*BETWEEN - BOX, FRAME_TOP + pos_y*BETWEEN - BOX, FRAME_LEFT + pos_x*BETWEEN + BOX, FRAME_TOP + pos_y*BETWEEN + BOX), fill = WHITE)
    drawing.text((FRAME_LEFT + pos_x*BETWEEN - STONE//4 - DIFFX, FRAME_TOP + pos_y*BETWEEN - STONE*3//4 - DIFFY), letter, font = font_num, fill = BLACK)
    return drawing

# draw letters for explanations
def draw_marks(drawing, board, pos_x, pos_y, letter):
    BOX = 21
    # draw square
    if letter == 'S':
        if board[pos_y][pos_x] == 'b':
            drawing.rectangle((FRAME_LEFT + pos_x*BETWEEN - BOX, FRAME_TOP + pos_y*BETWEEN - BOX, FRAME_LEFT + pos_x*BETWEEN + BOX, FRAME_TOP + pos_y*BETWEEN + BOX), fill = BLACK, outline = WHITE, width = 3)
        elif board[pos_y][pos_x] == 'w':
            drawing.rectangle((FRAME_LEFT + pos_x*BETWEEN - BOX, FRAME_TOP + pos_y*BETWEEN - BOX, FRAME_LEFT + pos_x*BETWEEN + BOX, FRAME_TOP + pos_y*BETWEEN + BOX), fill = WHITE, outline = BLACK, width = 3)
    # draw triangle
    if letter == 'T':
        DIFFX = 2
        DIFFY = 6
        if board[pos_y][pos_x] == 'b':
            drawing.line((FRAME_LEFT + pos_x*BETWEEN, FRAME_TOP + pos_y*BETWEEN - BOX - DIFFY, FRAME_LEFT + pos_x*BETWEEN - BOX - DIFFX, FRAME_TOP + pos_y*BETWEEN + BOX - DIFFY//2, FRAME_LEFT + pos_x*BETWEEN + BOX + DIFFX, FRAME_TOP + pos_y*BETWEEN + BOX - DIFFY//2, FRAME_LEFT + pos_x*BETWEEN, FRAME_TOP + pos_y*BETWEEN - BOX - DIFFY), fill = WHITE, width = 3)
        elif board[pos_y][pos_x] == 'w':
            drawing.line((FRAME_LEFT + pos_x*BETWEEN, FRAME_TOP + pos_y*BETWEEN - BOX - DIFFY, FRAME_LEFT + pos_x*BETWEEN - BOX - DIFFX, FRAME_TOP + pos_y*BETWEEN + BOX - DIFFY//2, FRAME_LEFT + pos_x*BETWEEN + BOX + DIFFX, FRAME_TOP + pos_y*BETWEEN + BOX - DIFFY//2, FRAME_LEFT + pos_x*BETWEEN, FRAME_TOP + pos_y*BETWEEN - BOX - DIFFY), fill = BLACK, width = 3)
    return drawing

# splitting notation
def split_notation(file_in):
    notation = []
    ans = []
    with open(file_in, 'r') as f:
        # read dummy data
        for _ in range(3):
            data = f.readline()
        data = f.readline().split(';')
        for i in range(1, len(data)):
            if len(data[i]) == 3:
                continue
            else:
                notation.append([i-1, data[i][0], data[i][2:4]])
        num = int(f.readline())
        tree = int(f.readline())
        for i in range(tree):
            data = f.readline().split(',')
            data[-1] = data[-1].replace('\n', '')
            wr_data = []
            for j in range(len(data)):
                n_data = data[j].split('[')
                wr_data.append([n_data[0], n_data[1][:-1]])
            ans.append(wr_data)
    return [num, notation, ans]

#main part
def main():
    args = sys.argv
    if len(args) != 2:
        print('Wrong Input!')
        sys.exit()

    go = board()
    notation = split_notation(args[1])

    if notation[0] > len(notation[1]):
        notation[0] = len(notation[1])

    for i in range(notation[0]):
        pos_x = conv2num(notation[1][i][2][0].upper())
        pos_y = conv2num(notation[1][i][2][1].upper())
        color = notation[1][i][1]
        go.board = go.put_stone(pos_y, pos_x, color)
        pos = [pos_y, pos_x]

    im_q = Image.new('RGB', (FIG_SIZE, FIG_SIZE), WHITE)
    im_a = Image.new('RGB', (FIG_SIZE, FIG_SIZE), WHITE)
    draw_q = ImageDraw.Draw(im_q)
    draw_a = ImageDraw.Draw(im_a)
    draw_q = draw_pos(draw_q)
    draw_a = draw_pos(draw_a)
    draw_q = draw_letters(draw_q)
    draw_a = draw_letters(draw_a)

    # drawing board
    draw_q = draw_stones(draw_q, go.board, pos)
    draw_a = draw_num_stones(draw_a, go.board, [])

    fq_out = "Q" + os.path.splitext(os.path.basename(args[1]))[0] + '.png'
    im_q.save(fq_out)

    # drawing answer part
    for i in range(len(notation[2])):
        fa_out = "A" + os.path.splitext(os.path.basename(args[1]))[0]+ '_' + str(i+1) + '.png'
        im_ai = im_a.copy()
        go_a = go
        draw_ai = ImageDraw.Draw(im_ai)
        pos_i = []
        for j in range(len(notation[2][i])):
            letter = notation[2][i][j][0]
            if letter.isdecimal():
                pos_x = conv2num(notation[2][i][j][1][1].upper())
                pos_y = BOARD_COORDS - int(notation[2][i][j][1][2:])
                color = notation[2][i][j][1][0].upper()
                pos_i.append([letter, pos_y, pos_x])
                go_a.board = go_a.put_stone(pos_y, pos_x, color)
                draw_ai = draw_num_stones(draw_ai, go_a.board, pos_i)
            elif letter.upper() == 'S':
                pos_x = conv2num(notation[2][i][j][1][0].upper())
                pos_y = BOARD_COORDS - int(notation[2][i][j][1][1:])
                draw_ai = draw_marks(draw_ai, go_a.board, pos_x, pos_y, letter)
            elif letter.upper() == 'T':
                pos_x = conv2num(notation[2][i][j][1][0].upper())
                pos_y = BOARD_COORDS - int(notation[2][i][j][1][1:])
                draw_ai = draw_marks(draw_ai, go_a.board, pos_x, pos_y, letter)
            else:
                pos_x = conv2num(notation[2][i][j][1][0].upper())
                pos_y = BOARD_COORDS - int(notation[2][i][j][1][1:])
                draw_ai = draw_tree(draw_ai, pos_x, pos_y, letter)
        im_ai.save(fa_out)

if __name__ == '__main__':
    main()