import pygame
import sys
import random
import time
pygame.init()       ##Khởi tạo tất cả các module cho PyGame
width = 700
height = 750
SCREEN = pygame.display.set_mode((width, height))    #Khởi chạy 1 cửa sổ có độ dài = width và độ rộng = height
pygame.display.set_caption("TETRIS")
icon_img = pygame.image.load("resources/images/icon.png")
pause_img = pygame.image.load("resources/images/pause.png")
background_img = pygame.image.load("resources/images/background_img.jpg")
level_img = pygame.image.load("images/level.png")
pause_img =pygame.transform.scale(pause_img, (50, 50))
pygame.display.set_icon(icon_img)
clock = pygame.time.Clock()  #Khởi tạo đối tượng thời gian
currentBar_height =75  # Thanh thể hiện thông số điểm ,thời gian ,nút pause
playBox_x =50                    # Tọa độ x của khung chơi = 50
playBox_y =currentBar_height +10   # Tọa đ y của khung chơi = với thanh thông số + 10
playBox_w=330 # Chiều dài của khung chơi
playBox_h=660 # Chiều rộng của khung chơi
playBox_square=33 # Chiều dài rộng Ô vuông trong khung chơi
fps=60


background_menu=pygame.image.load("images/background_menu.png")
huongdan_img=pygame.image.load("images/huong_dan_img.png")
SCREEN.blit(background_menu, (0,0))




best_sc=0
longest_time=0


# Khởi tạo màu cần thiết
blue =(0,0,255)
org = (249,87,0 )
white = (255,255,255)
black = (0,0,0)
gray = (95,95,96)
purple=(128,0,128)
yellow=(255,255,0)
red= (255,0,0)
pink =(255,0,127)
green = (0, 255, 0)
flower_blue=(100, 149, 237)
steel_blue=(70, 130, 180)
light_green=(152, 251, 152)
pale_green=(144, 238, 144)
medium_green=(60, 179, 113)
gouache=(176, 224, 230)
light=(173, 216, 230)

currentBar_color = (0,51,102)    # Màu nền của thanh thông số
playBox_color=(204,255,255)
background_color =(0,204,204)

block_colors = (blue,pink,purple,yellow,green)
shapes = ("i","l","j","o","s","t","z")
directions = ("v","^",">","<")


class Button:
    def __init__(self, button_color, button_hover_over_color, x, y, width, height, text_size=None, text_color=None, text_hover_over_color=None, text_str="", picture=""):
        self.button_color=button_color
        self.button_hover_over_color=button_hover_over_color
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.text_size=text_size
        self.text_color=text_color
        self.text_str=text_str
        if text_hover_over_color:
            self.text_hover_over_color=text_hover_over_color
        else:
            self.text_hover_over_color=text_color
        self.picture=picture
        self.condition=False

    #===== BUTTON CHƯA ĐƯỢC TRỎ CHUỘT VÀO =====
    def blit(self, SCREEN, outline_color=None): #Tạo nút
        if self.picture == "":
            pygame.draw.rect(SCREEN, outline_color,(self.x + 3, self.y + 3, self.width + 3, self.height + 3))
            pygame.draw.rect(SCREEN, self.button_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.circle(SCREEN, outline_color,(self.x + self.width / 2 + 3, self.y + self.width / 2 + 3),(self.width / 2 + 3))
            pygame.draw.circle(SCREEN, self.button_color,(self.x + self.width / 2, self.y + self.width / 2), (self.width / 2))
            button_img = pygame.image.load(self.picture)
            button_img_fix = pygame.transform.scale(button_img, (self.width, self.width))
            SCREEN.blit(button_img_fix,(self.x, self.y))
        if self.text_str!="":
            font=pygame.font.SysFont("consolas", self.text_size)
            text=font.render(self.text_str, True, self.text_color)
            # Canh giữa chữ trong nút
            text_position=(self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height/2 - text.get_height()/2))
            SCREEN.blit(text, text_position) # vẽ surface lên 1 surface khác và tọa độ đặt surface đó


    #===== PHẦN GIỚI HẠN CỦA BUTTON KHI TRỎ CHUỘT VÀO ( PHẠM VI ẢNH HƯỞNG ĐỂ THAY ĐỔI KIỂU NÚT ) =====
    def hovered_over(self, mouse_position): #Điều kiện chuột trỏ vào nút
        if self.picture == "": #Nút không có hình
            if self.x<mouse_position[0]<self.x+self.width and self.y<mouse_position[1]<self.y+self.height:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return True
        else:
            if self.x<mouse_position[0]<self.x+self.width and self.y<mouse_position[1]<self.y+self.width:
                pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                return True
        return False


    #===== BUTTON ĐÃ ĐƯỢC TRỎ CHUỘT VÀO =====
    def blit_hovered_over(self, SCREEN, outline_hover_color=None): #Nút khi trỏ chuột vào
        if self.picture == "":
            pygame.draw.rect(SCREEN, outline_hover_color,(self.x + 3, self.y + 3, self.width + 3, self.height + 3))
            pygame.draw.rect(SCREEN, self.button_hover_over_color, (self.x, self.y, self.width, self.height))
        else:
            pygame.draw.circle(SCREEN, outline_hover_color,(self.x + self.width / 2 + 3, self.y + self.width / 2 + 3),(self.width / 2 + 3))
            pygame.draw.circle(SCREEN, self.button_hover_over_color, (self.x + self.width / 2, self.y + self.width / 2),(self.width / 2))
            button_hover_img = pygame.image.load(self.picture)
            button_hover_img_fix = pygame.transform.scale(button_hover_img, (self.width, self.width))
            SCREEN.blit(button_hover_img_fix,(self.x, self.y))
        if self.text_str!="" :
            font=pygame.font.SysFont("consolas", self.text_size)
            text=font.render(self.text_str, True, self.text_hover_over_color)
            text_position=(self.x+(self.width/2-text.get_width()/2), self.y+(self.height/2-text.get_height()/2))
            SCREEN.blit(text, text_position)

    def change_pic(self, picture):
        self.picture=picture

    def get_condition(self):
        return self.condition

    #===== LẤY SỰ KIỆN KHI NHẤN CHUỘT VÀO BUTTON =====
    def clicked(self, mouse_position, event, condition=False):
        if self.hovered_over(mouse_position):
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.condition = condition
                    return True
        return False


class Player:
    def __init__(self, start_time):
        self.start_time = start_time
        self.time_since_start = 0
        self.score = 0


class Square:
    def __init__(self,x,y,color=playBox_color):
        self.x= x
        self.y= y
        self.color=color
        self.empty = True

    def draw_square(self):
        pygame.draw.rect(SCREEN,self.color,(self.x,self.y,playBox_square,playBox_square))


class PlayBox():
    def __init__(self):
        self.sq = {
            "row1": {85: []},               ###  1 dictionary của các dòng
            "row2": {118: []},                 ### Value của các dòng là dictionary khác với key là giá trị là tọa độ y của dòng đó, value là 1 list rỗng để add cái ô
            "row3": {151: []},
            "row4": {184: []},
            "row5": {217: []},
            "row6": {250: []},
            "row7": {283: []},
            "row8": {316: []},
            "row9": {349: []},
            "row10": {382: []},
            "row11": {415: []},
            "row12": {448: []},
            "row13": {481: []},
            "row14": {514: []},
            "row15": {547: []},
            "row16": {580: []},
            "row17": {613: []},
            "row18": {646: []},
            "row19": {679: []},
            "row20": {712: []},
        }
        self.__init_field()            ### add cái ô

    def __init_field(self):
        y = playBox_y
        for i in range(20):  # dòng
            x = playBox_x
            for j in range(10):  # cột
                sq_add = Square(x, y)
                self.sq["row" + str(i + 1)][y].append(sq_add)  ### add các ô vào dòng
                x += playBox_square
            y += playBox_square

    def destroy_full_row(self,player):
        times=0
        y = playBox_y
        for i in range(20):
            for sq in self.sq["row" + str(i + 1)][y]:
                if sq.empty:        # Chỉ cần có 1 ô trống là out
                    break
                elif sq.x == playBox_x + playBox_w - playBox_square:
                    times+=1
                    for j in range(800):
                        if j % 2 == 0:
                            pygame.draw.rect(SCREEN,black,(self.sq["row" + str(i+1)][y][0].x,self.sq["row"+ str(i+1)][y][0].y,playBox_w,playBox_square))
                        else:
                            for sq2 in self.sq["row" + str(i+1)][y]:
                                pygame.draw.rect(SCREEN, sq2.color, (sq2.x, sq2.y, playBox_square, playBox_square))
                        pygame.display.update()
                    self.destroy_and_replace(i + 1, y)
                    player.score += 50 * times

            y += playBox_square

    def destroy_and_replace(self, row_number, row_y):
        for i in range(row_number, 1, -1):
            prev_row_number = i - 1
            prev_y = row_y - playBox_square

            self.sq["row" + str(i)][row_y].clear()  # current_row.clear()
            temp_x = playBox_x
            for j in range(10):
                empty_tile = Square(temp_x, row_y)
                temp_x += playBox_square
                self.sq["row" + str(i)][row_y].append(empty_tile)
            if prev_y < 80:
                break

            for j in range(10):
                old_tile = self.sq["row" + str(i)][row_y][j]
                new_tile = self.sq["row" + str(prev_row_number)][prev_y][j]
                old_tile.x = new_tile.x
                old_tile.color = new_tile.color
                old_tile.empty = new_tile.empty

            row_y -= playBox_square


class Block:
    def __init__(self, shape: str, color=black):
        self.shape = shape
        self.color = color

        self.direction = directions[0]
        self.squares = [Square(playBox_x + playBox_w / 2 - playBox_square, playBox_y, self.color), Square(0, 0, color),
                      Square(0, 0, color), Square(0, 0, color)]

        self.__init_shape()
        for square in self.squares:
            square.empty = False

    def __init_shape(self):
        if self.shape == "i":
            self.squares[1] = Square(self.squares[0].x, self.squares[0].y - playBox_square, self.color)
            self.squares[2] = Square(self.squares[0].x, self.squares[1].y - playBox_square, self.color)
            self.squares[3] = Square(self.squares[0].x, self.squares[2].y - playBox_square, self.color)
        elif self.shape == "l":
            self.squares[1] = Square(self.squares[0].x + playBox_square, self.squares[0].y, self.color)
            self.squares[2] = Square(self.squares[0].x - playBox_square, self.squares[0].y, self.color)
            self.squares[3] = Square(self.squares[2].x, self.squares[2].y - playBox_square, self.color)
        elif self.shape == "j":
            self.squares[1] = Square(self.squares[0].x + playBox_square, self.squares[0].y, self.color)
            self.squares[2] = Square(self.squares[0].x - playBox_square, self.squares[0].y, self.color)
            self.squares[3] = Square(self.squares[1].x, self.squares[1].y - playBox_square, self.color)
        elif self.shape == "o":
            self.squares[1] = Square(self.squares[0].x + playBox_square, self.squares[0].y, self.color)
            self.squares[2] = Square(self.squares[0].x, self.squares[0].y - playBox_square, self.color)
            self.squares[3] = Square(self.squares[1].x, self.squares[1].y - playBox_square, self.color)
        elif self.shape == "s":
            self.squares[1] = Square(self.squares[0].x - playBox_square, self.squares[0].y, self.color)
            self.squares[2] = Square(self.squares[0].x, self.squares[0].y - playBox_square, self.color)
            self.squares[3] = Square(self.squares[2].x + playBox_square, self.squares[2].y, self.color)
        elif self.shape == "t":
            self.squares[1] = Square(self.squares[0].x + playBox_square, self.squares[0].y, self.color)
            self.squares[2] = Square(self.squares[0].x - playBox_square, self.squares[0].y, self.color)
            self.squares[3] = Square(self.squares[0].x, self.squares[0].y - playBox_square, self.color)
        elif self.shape == "z":
            self.squares[1] = Square(self.squares[0].x + playBox_square, self.squares[0].y, self.color)
            self.squares[2] = Square(self.squares[0].x, self.squares[0].y - playBox_square, self.color)
            self.squares[3] = Square(self.squares[2].x - playBox_square, self.squares[2].y, self.color)
        else:
            print("Lỗi: Block không tồn tại.")
            pygame.quit()
            sys.exit()

    def complete_block(self):          ### Đóng khuôn lại block s
        self.__init_shape()

    def can_fall(self, next_block, playBox, player,pause_button,mouse_position, level):    ### xem coi nó có rơi được không
        from main import manage_events
        manage_events(self, next_block, playBox, player,pause_button,mouse_position, level)
        # Kiểm tra xem có đụng đáy không
        for block_sq in self.squares:
            if block_sq.y >= playBox_h + playBox_y - playBox_square:
                return False

                # Kiểm tra xem có có block nào có sẵn không
        for block_sq in self.squares:
            y = playBox_y
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_sq.y + playBox_square == sq.y and block_sq.x == sq.x:
                        return False
                y += playBox_square

        return True

    def block_is_falling(self, next_block, playBox, player,pause_button,mouse_position,level,faster=None):
        from main import manage_events,update_display,manage_key_getpress
        manage_events(self, next_block, playBox,player,pause_button,mouse_position, level)

        if self.can_fall(next_block, playBox, player,pause_button,mouse_position, level):
            for i in range(0,3):
                for sq in self.squares:
                    sq.y += playBox_square / 3
                if level == 1 :
                    if faster == None:
                        clock.tick(15)
                    else:
                        clock.tick(30)
                if level == 2:
                    if faster == None:
                        clock.tick(25)
                    else:
                        clock.tick(40)
                if level == 3 :
                    if faster == None:
                        clock.tick(35)
                    else:
                        clock.tick(50)
                manage_events(self, next_block, playBox, player,pause_button,mouse_position, level)
                update_display(self, next_block, playBox, player,pause_button,mouse_position, level)
            manage_key_getpress(self, next_block, playBox,player,pause_button,mouse_position,level)
            update_display(self, next_block, playBox, player,pause_button,mouse_position, level)

    def get_new_block(self, next_block, playBox, player,pause_button,mouse_position, level):
        if self.can_fall(next_block, playBox, player,pause_button,mouse_position, level):             ### Nếu còn rơi được nữa thì rơi típ
            return self, next_block

        for block_sq in self.squares:           # Nếu rơi không được nữa (nghĩa là đã xong )
            found = False
            y = playBox_y
            for i in range(20):                     # Thực hiện tìm các khối vừa rơi thành công để
                if not found:
                    for j in range(10):
                        if block_sq.x == playBox.sq["row" + str(i + 1)][y][j].x and block_sq.y == playBox.sq["row" + str(i + 1)][y][j].y:
                            playBox.sq["row" + str(i + 1)][y][j].color = block_sq.color
                            playBox.sq["row" + str(i + 1)][y][j].empty = False
                            found = True
                            break
                    y += playBox_square
                else:
                    break

        new_block = next_block
        next_rand =random.randint(0, 6)
        next_rand_index2 = random.randint(0, 4)
        new_next_block = Block(shapes[next_rand], block_colors[next_rand_index2])
        clock.tick(20)
        return new_block, new_next_block

    def move_left(self,playBox):
        if self.can_move_left(playBox):
            for sq in self.squares:
                sq.x -= playBox_square

    def move_right(self, playBox):
        if self.can_move_right(playBox):
            for sq in self.squares:
                sq.x += playBox_square

    def can_move_left(self, playBox):
        for sq in self.squares:
            if sq.x <= playBox_x:
                return False
        for block_sq in self.squares:
            y = playBox_y
            t = (block_sq.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_sq.x - playBox_square == sq.x:
                        if t == 0 and block_sq.y == sq.y:
                            return False
                        if t == playBox_square / 3 and (block_sq.y + (2 *playBox_square) / 3   == sq.y or block_sq.y - t == sq.y):
                            return False
                        if t == (2*playBox_square) / 3 and (block_sq.y + playBox_square / 3   == sq.y or block_sq.y - t == sq.y):
                            return False

                y += playBox_square
        return True

    def can_move_right(self, playBox):
        for sq in self.squares:
            if sq.x + playBox_x >= playBox_x + playBox_w:
                return False
        for block_sq in self.squares:
            y = playBox_y
            t = (block_sq.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_sq.x + playBox_square == sq.x :
                        if t == 0 and block_sq.y == sq.y:
                            return False
                        if t == playBox_square / 3 and (
                                block_sq.y + (2 * playBox_square) / 3 == sq.y or block_sq.y - t == sq.y):
                            return False
                        if t == (2 * playBox_square) / 3 and (
                                block_sq.y + playBox_square / 3 == sq.y or block_sq.y - t == sq.y):
                            return False
                y += playBox_square
        return True

    def rotate_i(self, playBox):
            i=Block("i", self.color)
            i.squares=self.squares.copy()

            if self.direction == directions[0] or self.direction==directions[1]:
                i.squares[0]=Square(i.squares[1].x, i.squares[0].y, i.color)
                i.squares[1]=Square(i.squares[0].x - playBox_square, i.squares[0].y, i.color)
                i.squares[2]=Square(i.squares[0].x + playBox_square, i.squares[0].y, i.color)
                i.squares[3]=Square(i.squares[2].x + playBox_square, i.squares[0].y, i.color)
                i.direction=directions[2]

            elif self.direction==directions[2] or self.direction==directions[3]:
                i.squares[1] = Square(i.squares[0].x, i.squares[0].y - playBox_square, i.color)
                i.squares[2] = Square(i.squares[1].x, i.squares[1].y - playBox_square, i.color)
                i.squares[3] = Square(i.squares[2].x, i.squares[2].y - playBox_square, i.color)
                i.direction = directions[0]

            for block_square in i.squares:
                if block_square.x <= playBox_x or block_square.x >= playBox_w:
                    return
                y=playBox_y
                t = (block_square.y - y) % 33
                for j in range(20):
                    for sq in playBox.sq["row" + str(j + 1)][y]:
                        if not sq.empty and block_square.x == sq.x:
                            if t == 0 and block_square.y == sq.y:
                                return False
                            if t == playBox_square / 3 and (
                                    block_square.y + (2 * playBox_square) / 3 == sq.y or block_square.y - t == sq.y):
                                return False
                            if t == (2 * playBox_square) / 3 and (
                                    block_square.y + playBox_square / 3 == sq.y or block_square.y - t == sq.y):
                                return False
                    y += playBox_square
            self.direction=i.direction
            self.squares=i.squares

    def rotate_l(self, playBox):
        l = Block("l", self.color)
        l.squares = self.squares.copy()

        if self.direction == directions[0]:
            l.squares[0] = Square(l.squares[0].x, l.squares[0].y, l.color)
            l.squares[1] = Square(l.squares[0].x, l.squares[0].y - playBox_square, l.color)
            l.squares[2] = Square(l.squares[1].x, l.squares[1].y - playBox_square, l.color)
            l.squares[3] = Square(l.squares[2].x + playBox_square, l.squares[2].y, l.color)
            l.direction = directions[1]
        elif self.direction == directions[1]:
            l.squares[0] = Square(l.squares[3].x, l.squares[0].y, l.color)
            l.squares[1] = Square(l.squares[0].x, l.squares[0].y - playBox_square, l.color)
            l.squares[2] = Square(l.squares[1].x - playBox_square, l.squares[1].y, l.color)
            l.squares[3] = Square(l.squares[2].x - playBox_square, l.squares[2].y, l.color)
            l.direction = directions[2]
        elif self.direction == directions[2]:
            l.squares[0] = Square(l.squares[3].x, l.squares[0].y, l.color)
            l.squares[1] = Square(l.squares[0].x + playBox_square, l.squares[0].y, l.color)
            l.squares[2] = Square(l.squares[1].x, l.squares[1].y - playBox_square, l.color)
            l.squares[3] = Square(l.squares[2].x, l.squares[2].y - playBox_square, l.color)
            l.direction = directions[3]
        elif self.direction == directions[3]:
            l.squares[0] = Square(l.squares[1].x, l.squares[0].y, l.color)
            l.squares[1] = Square(l.squares[0].x + playBox_square, l.squares[0].y, l.color)
            l.squares[2] = Square(l.squares[0].x - playBox_square, l.squares[1].y, l.color)
            l.squares[3] = Square(l.squares[2].x, l.squares[2].y - playBox_square, l.color)
            l.direction = directions[0]

        for block_square in l.squares:
            if block_square.x <= playBox_x or block_square.x >= playBox_w:
                return
            y = playBox_y
            t = (block_square.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_square.x == sq.x:
                        if t == 0 and block_square.y == sq.y:
                            return False
                        if t == playBox_square / 3 and (
                                block_square.y + (2 * playBox_square) / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                        if t == (2 * playBox_square) / 3 and (
                                block_square.y + playBox_square / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                y += playBox_square

        self.direction = l.direction
        self.squares = l.squares

    def rotate_j(self, playBox):
        j=Block("j", self.color)
        j.squares=self.squares.copy()

        if self.direction == directions[0]:
            j.squares[0]=Square(j.squares[1].x, j.squares[0].y, j.color)
            j.squares[1]=Square(j.squares[0].x - playBox_square, j.squares[0].y, j.color)
            j.squares[2]=Square(j.squares[1].x, j.squares[1].y - playBox_square, j.color)
            j.squares[3]=Square(j.squares[2].x, j.squares[2].y - playBox_square, j.color)
            j.direction=directions[1]
        elif self.direction == directions[1]:
            j.squares[0]=Square(j.squares[1].x - playBox_square, j.squares[0].y ,j.color)
            j.squares[1]=Square(j.squares[0].x, j.squares[0].y - playBox_square, j.color)
            j.squares[2]=Square(j.squares[1].x + playBox_square, j.squares[1].y, j.color)
            j.squares[3]=Square(j.squares[2].x + playBox_square, j.squares[2].y, j.color)
            j.direction=directions[2]
        elif self.direction == directions[2]:
            j.squares[0]=Square(j.squares[2].x, j.squares[0].y, j.color)
            j.squares[1]=Square(j.squares[0].x, j.squares[0].y - playBox_square, j.color)
            j.squares[2]=Square(j.squares[1].x, j.squares[1].y - playBox_square, j.color)
            j.squares[3]=Square(j.squares[2].x - playBox_square, j.squares[2].y, j.color)
            j.direction=directions[3]
        elif self.direction == directions[3]:
            j.squares[0]=Square(j.squares[0].x, j.squares[0].y, j.color)
            j.squares[1]=Square(j.squares[0].x + playBox_square, j.squares[0].y, j.color)
            j.squares[2]=Square(j.squares[0].x - playBox_square, j.squares[0].y, j.color)
            j.squares[3]=Square(j.squares[1].x, j.squares[1].y - playBox_square, j.color)
            j.direction=directions[0]

        for block_square in j.squares:
            if block_square.x <= playBox_x or block_square.x >= playBox_w:
                return
            y=playBox_y
            t = (block_square.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_square.x  == sq.x:
                        if t == 0 and block_square.y == sq.y:
                            return False
                        if t == playBox_square / 3 and (
                                block_square.y + (2 * playBox_square) / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                        if t == (2 * playBox_square) / 3 and (
                                block_square.y + playBox_square / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                y += playBox_square

        self.direction=j.direction
        self.squares=j.squares
    def rotate_s(self, playBox):
        s=Block("s", self.color)
        s.squares=self.squares.copy()

        if self.direction == directions[0] or self.direction == directions[1]:
            s.squares[0]=Square(s.squares[3].x, s.squares[0].y, s.color)
            s.squares[1]=Square(s.squares[0].x, s.squares[0].y - playBox_square, s.color)
            s.squares[2]=Square(s.squares[1].x - playBox_square, s.squares[1].y, s.color)
            s.squares[3]=Square(s.squares[2].x, s.squares[2].y - playBox_square, s.color)
            s.direction=directions[2]
        elif self.direction == directions[2] or self.direction == directions[3]:
            s.squares[0]=Square(s.squares[2].x, s.squares[0].y, s.color)
            s.squares[1]=Square(s.squares[0].x - playBox_square, s.squares[0].y, s.color)
            s.squares[2]=Square(s.squares[0].x, s.squares[0].y - playBox_square, s.color)
            s.squares[3]=Square(s.squares[2].x + playBox_square, s.squares[2].y, s.color)
            s.direction=directions[0]

        for block_square in s.squares:
            if block_square.x <= playBox_x or block_square.x >= playBox_w:
                return
            y=playBox_y
            t = (block_square.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_square.x == sq.x:
                        if t == 0 and block_square.y == sq.y:
                            return False
                        if t == playBox_square / 3 and (
                                block_square.y + (2 * playBox_square) / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                        if t == (2 * playBox_square) / 3 and (
                                block_square.y + playBox_square / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                y += playBox_square
        self.direction = s.direction
        self.squares = s.squares

    def rotate_t(self, playBox):
        t=Block("t", self.color)
        t.squares=self.squares.copy()
        if self.direction == directions[0]:
            t.squares[0]=Square(t.squares[0].x, t.squares[0].y, t.color)
            t.squares[1]=Square(t.squares[0].x, t.squares[0].y - playBox_square, t.color)
            t.squares[2]=Square(t.squares[1].x, t.squares[1].y - playBox_square, t.color)
            t.squares[3]=Square(t.squares[1].x + playBox_square, t.squares[1].y, t.color)
            t.direction=directions[1]
        elif self.direction == directions[1]:
            t.squares[0] = Square(t.squares[0].x, t.squares[0].y, t.color)
            t.squares[1] = Square(t.squares[0].x, t.squares[0].y - playBox_square, t.color)
            t.squares[2] = Square(t.squares[1].x - playBox_square, t.squares[1].y, t.color)
            t.squares[3] = Square(t.squares[1].x + playBox_square, t.squares[2].y, t.color)
            t.direction = directions[2]
        elif self.direction == directions[2]:
            t.squares[0] = Square(t.squares[0].x, t.squares[0].y, t.color)
            t.squares[1] = Square(t.squares[0].x, t.squares[0].y - playBox_square, t.color)
            t.squares[2] = Square(t.squares[1].x, t.squares[1].y - playBox_square, t.color)
            t.squares[3] = Square(t.squares[1].x - playBox_square, t.squares[1].y, t.color)
            t.direction = directions[3]
        elif self.direction == directions[3]:
            t.squares[0] = Square(t.squares[0].x, t.squares[0].y, t.color)
            t.squares[1] = Square(t.squares[0].x + playBox_square, t.squares[0].y, t.color)
            t.squares[2] = Square(t.squares[0].x - playBox_square, t.squares[0].y, t.color)
            t.squares[3] = Square(t.squares[0].x, t.squares[0].y - playBox_square, t.color)
            t.direction = directions[0]

        for block_square in t.squares:
            if block_square.x <= playBox_x or block_square.x >= playBox_w:
                return
            y=playBox_y
            k = (block_square.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_square.x == sq.x:
                        if k == 0 and block_square.y == sq.y:
                            return False
                        if k == playBox_square / 3 and (
                                block_square.y + (2 * playBox_square) / 3 == sq.y or block_square.y - k == sq.y):
                            return False
                        if k == (2 * playBox_square) / 3 and (
                                block_square.y + playBox_square / 3 == sq.y or block_square.y - k == sq.y):
                            return False
                y += playBox_square
        self.direction = t.direction
        self.squares = t.squares

    def rotate_z(self, playBox):
        z = Block("z", self.color)
        z.squares = self.squares.copy()

        if self.direction == directions[0] or self.direction == directions[1]:
            z.squares[0] = Square(z.squares[3].x, z.squares[0].y, z.color)
            z.squares[1] = Square(z.squares[0].x, z.squares[0].y - playBox_square, z.color)
            z.squares[2] = Square(z.squares[1].x + playBox_square, z.squares[1].y, z.color)
            z.squares[3] = Square(z.squares[2].x, z.squares[2].y - playBox_square, z.color)
            z.direction = directions[2]
        elif self.direction == directions[2] or self.direction == directions[3]:
            z.squares[0] = Square(z.squares[3].x, z.squares[0].y, z.color)
            z.squares[1] = Square(z.squares[0].x + playBox_square, z.squares[0].y, z.color)
            z.squares[2] = Square(z.squares[0].x, z.squares[0].y - playBox_square, z.color)
            z.squares[3] = Square(z.squares[2].x - playBox_square, z.squares[2].y, z.color)
            z.direction = directions[0]

        for block_square in z.squares:
            if block_square.x <= playBox_x or block_square.x >= playBox_w:
                return
            y = playBox_y
            t = (block_square.y - y) % 33
            for i in range(20):
                for sq in playBox.sq["row" + str(i + 1)][y]:
                    if not sq.empty and block_square.x == sq.x:
                        if t == 0 and block_square.y == sq.y:
                            return False
                        if t == playBox_square / 3 and (
                                block_square.y + (2 * playBox_square) / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                        if t == (2 * playBox_square) / 3 and (
                                block_square.y + playBox_square / 3 == sq.y or block_square.y - t == sq.y):
                            return False
                y += playBox_square
        self.direction = z.direction
        self.squares = z.squares

    def rotate(self, next_block, playBox, player,pause_button,mouse_position, level):
        from main import manage_events, update_display
        manage_events(self, next_block, playBox, player,pause_button,mouse_position, level)

        if self.shape == "i":
            self.rotate_i(playBox)
        elif self.shape == "l":
            self.rotate_l(playBox)
        elif self.shape == "j":
            self.rotate_j(playBox)
        elif self.shape == "o":
            return
        elif self.shape == "s":
            self.rotate_s(playBox)
        elif self.shape == "t":
            self.rotate_t(playBox)
        elif self.shape == "z":
            self.rotate_z(playBox)
        else:
            print("Lỗi tên block")
            pygame.quit()
            sys.exit()
        manage_events(self, next_block, playBox, player,pause_button,mouse_position, level)
        update_display(self, next_block, playBox, player,pause_button,mouse_position, level)
from main import *