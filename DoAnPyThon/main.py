from util import *
volume_button = Button(gouache, light_green, 650, 3, 40, 40, picture="images/volume.png")
playSound = pygame.mixer.Sound("sound/PS.mp3")
playSound.play(-1)
play=1
def time_format(time):
    minute =int(time/1000/60)
    second = int(time / 1000) - minute*60
    return str(minute) + ":" +str(second)

def next_block_modal(next_block):
    surface = pygame.Surface((6* playBox_square+10,6* playBox_square+10))
    surface.fill((0, 51, 102))
    font = pygame.font.SysFont("consolas", 50)
    render_next_block = font.render("Next", True, white)
    render_next_block_line = font.render("Next", True, (0, 51, 102))
    pygame.draw.rect(surface,playBox_color,(5,5,6* playBox_square,6* playBox_square))
    SCREEN.blit(render_next_block_line, (507, 322))
    SCREEN.blit(render_next_block, (504, 319))
    SCREEN.blit(surface,(playBox_x+playBox_w + playBox_square*2.25,height/2))

    display_nextblock = Block(next_block.shape,next_block.color)
    #Sửa lại vị trí ô Square[0]
    display_nextblock.squares = [Square(playBox_x+playBox_w + playBox_square * 5,height / 2 + playBox_square*4,next_block.color),Square(0, 0, next_block.color),Square(0, 0, next_block.color),Square(0, 0, next_block.color)]
    display_nextblock.complete_block()   # gọi lại hàm khởi tạo hình dạng block để các Square còn lại kết hợp với Square[0] ở trên

    for sq in display_nextblock.squares:   #Vẽ block lên màn hình
        sq.draw_square()

def next_block_screen(next_block):
    surface = pygame.Surface((6 * playBox_square + 10, 6 * playBox_square + 10))
    surface.fill((0, 51, 102))
    font = pygame.font.SysFont("consolas", 50)
    render_next_block = font.render("Next", True, white)
    render_next_block_line = font.render("Next", True, (0, 51, 102))
    pygame.draw.rect(surface, playBox_color, (5, 5, 6 * playBox_square, 6 * playBox_square))
    SCREEN.blit(render_next_block_line, (507, 322))
    SCREEN.blit(render_next_block, (504, 319))
    SCREEN.blit(surface, (playBox_x + playBox_w + playBox_square * 2.25, height / 2))

def is_game_over(playBox, player):
    y = playBox_y
    for i in range(20):
        for sq in playBox.sq["row" + str(i + 1)][y]:
            if not sq.empty and sq.y <= playBox_y:
                temp_y = playBox_y
                for j in range(20):
                    for sq in playBox.sq["row" + str(j + 1)][temp_y]:
                        sq.draw_square()
                    temp_y += playBox_square

                font = pygame.font.SysFont("consolas", 50)
                rendered_text = font.render("GAME OVER", 1, black)
                SCREEN.blit(rendered_text, (playBox_x + playBox_w/2 - rendered_text.get_width()/2, playBox_h / 2 - rendered_text.get_height()/2))
                pygame.display.update()

                time.sleep(2)
                score(player)
                break

        y += playBox_square

def display_screen(block,next_block,playBox,pause_button,mouse_position, level):
    SCREEN.blit(background_img, (0, 0))
    font = pygame.font.SysFont("consolas", 25)
    render_time_play = font.render("Time : ", True, white)
    pygame.draw.rect(SCREEN, currentBar_color, [0, 0, width, currentBar_height])
    SCREEN.blit(render_time_play, (20, 25))

    render_score_play = font.render("Score : ", True, white)
    SCREEN.blit(render_score_play, (450, 25))

    surface_contain_playBox = pygame.Surface((playBox_w + 10, playBox_h + 10))  # Surface bao quanh playBox
    surface_contain_playBox.fill((0, 51, 102))
    pygame.draw.rect(surface_contain_playBox, playBox_color, [5, 5, playBox_w, playBox_h])  ##Khung để chơi

    SCREEN.blit(surface_contain_playBox, (playBox_x - 5, playBox_y - 5))
    font_level = pygame.font.SysFont("consolas", 70)
    if level == 1:
        str_level = "Easy"
    elif level == 2:
        str_level = "Medium"
    elif level == 3:
        str_level = "Hard"
    render_level = font_level.render("" + str_level, True, flower_blue)
    render_level_line = font_level.render("" + str_level, True, (0, 51, 102))
    # render_level_1 = font_level.render("", True, flower_blue)
    # render_level_1_line = font_level.render("" + str_level, True, (0, 51, 102))
    SCREEN.blit(render_level_line,
                (540 - render_level_line.get_width() / 2 + 3, 180 - render_level_line.get_height() / 2 + 3))
    SCREEN.blit(render_level, (540 - render_level_line.get_width() / 2, 180 - render_level_line.get_height() / 2))
    # SCREEN.blit(render_level_1_line,(552, 142))
    # SCREEN.blit(render_level_1, (549, 139))

    if pause_button.hovered_over(mouse_position):
        pause_button.blit_hovered_over(SCREEN, medium_green)
    else:
        pause_button.blit(SCREEN, light)

    next_block_screen(next_block)
    column_lines = playBox_x  # Cột đầu tiên bắt đầu từ viền chiều dài bên trái khung chơi
    raw_lines = playBox_y  # Hàng đầu tiên bắt đầu từ viền chiều rộng trên cùng khung chơi
    column_lines = playBox_x  # Cột đầu tiên bắt đầu từ viền chiều dài bên trái khung chơi
    raw_lines = playBox_y  # Hàng đầu tiên bắt đầu từ viền chiều rộng trên cùng khung chơi
    for i in range(19):  ## Vẽ các viền của các dòng
        raw_lines += 33
        pygame.draw.line(SCREEN, black, (playBox_x, raw_lines), (playBox_w + playBox_x - 2, raw_lines))
    for i in range(9):  ## Vẽ các viền của các cột
        column_lines += 33
        pygame.draw.line(SCREEN, black, (column_lines, playBox_y), (column_lines, playBox_y + playBox_h - 2))
    pygame.display.update()

def update_display(block,next_block,playBox,player,pause_button,mouse_position, level):
    SCREEN.blit(background_img,(0,0))
    font = pygame.font.SysFont("consolas",25)
    player.time_since_start = pygame.time.get_ticks() - player.start_time
    render_time_play=font.render("Time : " +time_format(player.time_since_start),True,white)
    pygame.draw.rect(SCREEN,currentBar_color,[0,0,width,currentBar_height])
    SCREEN.blit(render_time_play,(20,25))

    render_score_play =font.render("Score : " + str(player.score), True, white)
    SCREEN.blit(render_score_play,(450,25))

    surface_contain_playBox = pygame.Surface((playBox_w + 10, playBox_h + 10))  # Surface bao quanh playBox
    surface_contain_playBox.fill((0, 51, 102))
    pygame.draw.rect(surface_contain_playBox,playBox_color,[5,5,playBox_w,playBox_h])    ##Khung để chơi

    SCREEN.blit(surface_contain_playBox,(playBox_x - 5,playBox_y -5))
    font_level = pygame.font.SysFont("consolas", 70)
    if level == 1:
        str_level="Easy"
    elif level == 2:
        str_level="Medium"
    elif level == 3:
        str_level="Hard"
    render_level = font_level.render(""+str_level, True, flower_blue)
    render_level_line = font_level.render(""+str_level, True, (0, 51, 102))
    # render_level_1 = font_level.render("", True, flower_blue)
    # render_level_1_line = font_level.render("" + str_level, True, (0, 51, 102))
    SCREEN.blit(render_level_line, (540 - render_level_line.get_width()/2 +3 , 180 - render_level_line.get_height()/2 + 3))
    SCREEN.blit(render_level, (540 - render_level_line.get_width()/2, 180 - render_level_line.get_height()/2))
    # SCREEN.blit(render_level_1_line,(552, 142))
    # SCREEN.blit(render_level_1, (549, 139))

    if pause_button.hovered_over(mouse_position):
        pause_button.blit_hovered_over(SCREEN, medium_green)
    else:
        pause_button.blit(SCREEN, light)

    next_block_modal(next_block)


    y = playBox_y
    for i in range(20):
        for sq in playBox.sq["row" + str(i + 1)][y]:
            sq.draw_square()         ### vẽ các ô đã được khởi tạo
        y += playBox_square

    # Vẽ ra các Block rơi

    for sq in block.squares:
        if sq.y + playBox_square / 3 + 1  > playBox_y:
            sq.draw_square()

    column_lines = playBox_x  # Cột đầu tiên bắt đầu từ viền chiều dài bên trái khung chơi
    raw_lines = playBox_y  # Hàng đầu tiên bắt đầu từ viền chiều rộng trên cùng khung chơi
    for i in range(19):  ## Vẽ các viền của các dòng
        raw_lines += 33
        pygame.draw.line(SCREEN, black, (playBox_x, raw_lines), (playBox_w + playBox_x - 2, raw_lines))
    for i in range(9):        ## Vẽ các viền của các cột
        column_lines += 33
        pygame.draw.line(SCREEN, black, (column_lines, playBox_y), (column_lines, playBox_y + playBox_h - 2))
    pygame.display.update()


def manage_events(block, next_block, playBox, player,pause_button,mouse_position, level):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pause_button.clicked(mouse_position, event):
                while True:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                    i = 0
                    for event2 in pygame.event.get():
                        if event2.type == pygame.MOUSEBUTTONDOWN:
                            if pause_button.clicked(mouse_position, event2):
                                pause()
                    if pause() == 1:
                        break
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                block.move_left(playBox)
            elif event.key == pygame.K_RIGHT:
                block.move_right(playBox)
            elif event.key == pygame.K_UP:
                block.rotate(next_block, playBox, player,pause_button,mouse_position, level)
    update_display(block, next_block, playBox, player,pause_button,mouse_position, level)


def manage_key_getpress(block,next_block,playBox,player, pause_button, mouse_position,level):
    if pygame.key.get_pressed()[pygame.K_DOWN]:
        while True:
            if block.can_fall(next_block, playBox, player,pause_button,mouse_position,level)==False:
                break
            block.block_is_falling(next_block, playBox, player,pause_button,mouse_position,level,True)
            if pygame.key.get_pressed()[pygame.K_DOWN] == False:
                break


def start(level=None):
    global best_sc
    global longest_time
    pause_button = Button(gouache, light_green, 640, 690, 50, 50, picture="images/pause.png")

    rand_index = random.randint(0, 6)
    rand_color = random.randint(0, 4)
    block = Block(shapes[rand_index], block_colors[rand_color])  # Khởi tạo Block
    rand_index2 = random.randint(0, 6)
    rand_color2 = random.randint(0, 4)
    next_block = Block(shapes[rand_index2], block_colors[rand_color2])  # Khởi tạo block tiếp theo
    playBox = PlayBox()
    size_font= 150
    i=3
    while True :
        if str(i) == "0" : break
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        display_screen(block,next_block,playBox,pause_button,mouse_position, level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        font = pygame.font.SysFont("consolas", size_font)
        render_count = font.render(""+str(i), True, black)
        i -= 1
        SCREEN.blit(render_count,(playBox_x + playBox_w/2 - render_count.get_width()/2, playBox_h / 2 - render_count.get_height()/2))
        pygame.display.update()
        time.sleep(1)
        
    start_time=pygame.time.get_ticks()
    player = Player(start_time)
    while True:
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        update_display(block,next_block,playBox,player,pause_button,mouse_position, level)
        (block, next_block) = block.get_new_block(next_block, playBox, player,pause_button,mouse_position, level)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        if pause_button.hovered_over(mouse_position):
            pause_button.blit_hovered_over(SCREEN, medium_green)
        else:
            pause_button.blit(SCREEN, light)
        manage_events(block, next_block, playBox, player,pause_button,mouse_position, level)
        manage_key_getpress(block, next_block, playBox, player,pause_button,mouse_position,level)
        update_display(block, next_block, playBox, player, pause_button, mouse_position, level)
        block.block_is_falling(next_block, playBox, player,pause_button,mouse_position,level)
        update_display(block,next_block,playBox,player,pause_button,mouse_position, level)
        playBox.destroy_full_row(player)
        update_display(block,next_block,playBox,player,pause_button,mouse_position, level)

        if player.score > best_sc:
            best_sc = player.score
        if player.time_since_start > longest_time:
            longest_time = player.time_since_start

        is_game_over(playBox,player)
        update_display(block, next_block, playBox, player, pause_button, mouse_position, level)

        pygame.display.update()
        clock.tick(60)         #FPS= 60

def level():
    global play
    global playSound
    easy_button=Button(flower_blue, light_green, width-500, height-320, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Easy")
    medium_button = Button(flower_blue, light_green, width - 500, height - 230, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Medium")
    hard_button = Button(flower_blue, light_green, width - 500, height - 140, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Hard")
    back_button = Button(flower_blue, light_green, 20, height - 100, 150, 80, text_size=35, text_color=white, text_hover_over_color=black, text_str="Back")


    while True:
        SCREEN.blit(level_img, (0, 0))
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN: # LẤY SỰ KIỆN KHI CON CHUỘT CLICK VÀO
                if easy_button.clicked(mouse_position, event):
                    start(1)
                    break
                elif medium_button.clicked(mouse_position, event):
                    start(2)
                    break
                elif hard_button.clicked(mouse_position, event):
                    start(3)
                    break
                elif back_button.clicked(mouse_position, event):
                    menu()
                    break
                if volume_button.clicked(mouse_position, event, not volume_button.condition):
                    if (play == 1):
                        playSound.stop()
                        play = 0
                    else:
                        playSound.play(-1)
                        play = 1

        if easy_button.hovered_over(mouse_position):
            easy_button.blit_hovered_over(SCREEN, medium_green)
        else:
            easy_button.blit(SCREEN, steel_blue)
        if medium_button.hovered_over(mouse_position):
            medium_button.blit_hovered_over(SCREEN, medium_green)
        else:
            medium_button.blit(SCREEN, steel_blue)
        if hard_button.hovered_over(mouse_position):
            hard_button.blit_hovered_over(SCREEN, medium_green)
        else:
            hard_button.blit(SCREEN, steel_blue)
        if back_button.hovered_over(mouse_position):
            back_button.blit_hovered_over(SCREEN, medium_green)
        else:
            back_button.blit(SCREEN, steel_blue)
        if volume_button.get_condition():
            volume_button.change_pic("images/no_volume.png")
        else:
            volume_button.change_pic("images/volume.png")
        if volume_button.hovered_over(mouse_position):
            volume_button.blit_hovered_over(SCREEN, medium_green)
        else:
            volume_button.blit(SCREEN, light)

        clock.tick(fps)
        pygame.display.flip()
        pygame.display.update()


def pause():
    global play
    global playSound
    back_to_game_button=Button(flower_blue, light_green, width-500, height-400, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Back to game")
    menu_button = Button(flower_blue, light_green, width - 500, height - 310, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Menu")
    quit_button = Button(flower_blue, light_green, width - 500, height - 220, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Quit")

    while True:
        pygame.Surface.set_alpha(SCREEN)
        mouse_position = pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN: # LẤY SỰ KIỆN KHI CON CHUỘT CLICK VÀO
                if back_to_game_button.clicked(mouse_position, event):
                    return 1
                elif menu_button.clicked(mouse_position, event):
                    menu()
                    break
                elif quit_button.clicked(mouse_position, event):
                    pygame.quit()
                    sys.exit()
                if volume_button.clicked(mouse_position, event, not volume_button.condition):
                    if (play == 1):
                        playSound.stop()
                        play = 0
                    else:
                        playSound.play(-1)
                        play = 1

        if back_to_game_button.hovered_over(mouse_position):
            back_to_game_button.blit_hovered_over(SCREEN, medium_green)
        else:
            back_to_game_button.blit(SCREEN, steel_blue)
        if menu_button.hovered_over(mouse_position):
            menu_button.blit_hovered_over(SCREEN, medium_green)
        else:
            menu_button.blit(SCREEN, steel_blue)
        if quit_button.hovered_over(mouse_position):
            quit_button.blit_hovered_over(SCREEN, medium_green)
        else:
            quit_button.blit(SCREEN, steel_blue)
        if volume_button.get_condition():
            volume_button.change_pic("images/no_volume.png")
        else:
            volume_button.change_pic("images/volume.png")
        if volume_button.hovered_over(mouse_position):
            volume_button.blit_hovered_over(SCREEN, medium_green)
        else:
            volume_button.blit(SCREEN, light)

        clock.tick(fps)
        pygame.display.flip()
        pygame.display.update()

def score(player=None):
    ok_button = Button(flower_blue, light_green, 250, 410, 200, 50, text_size=30, text_color=white,text_hover_over_color=black, text_str="OK")
    if player:
        font_small = pygame.font.SysFont("consolas", 30)
        rendered_current_score = font_small.render("Current Score: " + str(player.score), 1, black)
        rendered_best_score = font_small.render("Best Score   : " + str(best_sc), 1, black)
        rendered_current_time = font_small.render("Current Time : " + str(time_format(player.time_since_start)), 1, black)
        rendered_longest_time = font_small.render("Longest Time : " + str(time_format(longest_time)), 1, black)

        while True:
            pygame.Surface.set_alpha(SCREEN)
            pygame.draw.rect(SCREEN, black, (140, 215, 410, 270))
            pygame.draw.rect(SCREEN, gouache, (150, 225, 390, 250))
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            mouse_position = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if ok_button.clicked(mouse_position, event):
                        menu(player)
                        break
            if ok_button.hovered_over(mouse_position):
                ok_button.blit_hovered_over(SCREEN, medium_green)
            else:
                ok_button.blit(SCREEN, steel_blue)
            SCREEN.blit(rendered_current_score, (180, 240))
            SCREEN.blit(rendered_best_score, (180, 280))
            SCREEN.blit(rendered_current_time, (180, 320))
            SCREEN.blit(rendered_longest_time, (180, 360))

            pygame.display.update()

def menu(player=None):
    global play
    global playSound

    #===== ADD BUTTON =====
    play_button=Button(flower_blue, light_green, width-500, height-320, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Play")
    instruction_button=Button(flower_blue, light_green, width-500, height-230, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Instruction")
    quit_button=Button(flower_blue, light_green, width-500, height-140, 300, 70, text_size=35, text_color=white, text_hover_over_color=black, text_str="Quit")

    if player:
        font_small = pygame.font.SysFont("consolas", 20)
        rendered_best_score = font_small.render("Best Score: " + str(best_sc), 1, black)
        rendered_longest_time = font_small.render("Longest Time: " + str(time_format(longest_time)), 1, black)

    #===== RUN =====
    while True:
        SCREEN.blit(background_menu,(0,0))
        mouse_position=pygame.mouse.get_pos()
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        if player:
            SCREEN.blit(rendered_best_score, (15, 690))
            SCREEN.blit(rendered_longest_time, (15, 720))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type==pygame.MOUSEBUTTONDOWN: # LẤY SỰ KIỆN KHI CON CHUỘT CLICK VÀO
                if play_button.clicked(mouse_position, event):
                    level()
                    break
                if instruction_button.clicked(mouse_position, event):
                    huong_dan()
                    break
                if quit_button.clicked(mouse_position, event):
                    pygame.quit()
                    sys.exit()
                if volume_button.clicked(mouse_position, event, not volume_button.condition):
                    if (play==1) :
                        playSound.stop()
                        play=0
                    else:
                        playSound.play(-1)
                        play=1

        #===== ĐIỀU KIỆN THAY ĐỔI MÀU SẮC CHO BUTTON TRONG MENU=====
        if play_button.hovered_over(mouse_position):
            play_button.blit_hovered_over(SCREEN, medium_green)
        else:
            play_button.blit(SCREEN, steel_blue)
        if instruction_button.hovered_over(mouse_position):
            instruction_button.blit_hovered_over(SCREEN, medium_green)
        else:
            instruction_button.blit(SCREEN, steel_blue)
        if quit_button.hovered_over(mouse_position):
            quit_button.blit_hovered_over(SCREEN, medium_green)
        else:
            quit_button.blit(SCREEN, steel_blue)
        if volume_button.get_condition():
            volume_button.change_pic("images/no_volume.png")
        else:
            volume_button.change_pic("images/volume.png")
        if volume_button.hovered_over(mouse_position):
            volume_button.blit_hovered_over(SCREEN, medium_green)
        else:
            volume_button.blit(SCREEN, light)


        clock.tick(fps)
        pygame.display.flip()
        pygame.display.update()


def huong_dan():
    global play
    global playSound
    play_button=Button(flower_blue, light_green, width - 180, height - 100, 150, 80, text_size=35, text_color=white, text_hover_over_color=black, text_str="Play")
    back_button=Button(flower_blue, light_green, 20, height - 100, 150, 80, text_size=35, text_color=white, text_hover_over_color=black, text_str="Back")

    while True:
        SCREEN.blit(huongdan_img, (0, 0))
        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
        mouse_position = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type==pygame.MOUSEBUTTONDOWN:
                if back_button.clicked(mouse_position, event):
                    menu()
                    break

                if play_button.clicked(mouse_position, event):
                    level()
                    break
                if volume_button.clicked(mouse_position, event, not volume_button.condition):
                    if (play == 1):
                        playSound.stop()
                        play = 0
                    else:
                        playSound.play(-1)
                        play = 1

        #===== ĐIỀU KIỆN THAY ĐỔI MÀU SẮC BUTTON TRONG INSTRUCTION =====
        if play_button.hovered_over(mouse_position):
            play_button.blit_hovered_over(SCREEN, medium_green)
        else:
            play_button.blit(SCREEN, steel_blue)
        if back_button.hovered_over(mouse_position):
            back_button.blit_hovered_over(SCREEN, medium_green)
        else:
            back_button.blit(SCREEN, steel_blue)
        if volume_button.get_condition():
            volume_button.change_pic("images/no_volume.png")
        else:
            volume_button.change_pic("images/volume.png")
        if volume_button.hovered_over(mouse_position):
            volume_button.blit_hovered_over(SCREEN, medium_green)
        else:
            volume_button.blit(SCREEN, light)

        #===== PHẦN FONT, TEXT HƯỚNG DẪN TRONG INSTRUCTION =====
        huong_dan_font=pygame.font.SysFont("consolas", 40)
        huong_dan_text=huong_dan_font.render("Instructions", True, black)
        SCREEN.blit(huong_dan_text, (150,180))

        dong_1= "Play keys"
        dong_2= "Move right    :"
        dong_3= "Move left     :"
        dong_4= "Drop          :"
        dong_5= "Rotate        :"

        font=pygame.font.SysFont("consolas", 30)
        rendered_dong_1 = font.render(dong_1, True, black)
        rendered_dong_2 = font.render(dong_2, True, black)
        rendered_dong_3 = font.render(dong_3, True, black)
        rendered_dong_4 = font.render(dong_4, True, black)
        rendered_dong_5 = font.render(dong_5, True, black)

        SCREEN.blit(rendered_dong_1, (200, 270))
        SCREEN.blit(rendered_dong_2, (150, 340))
        SCREEN.blit(rendered_dong_3, (150, 410))
        SCREEN.blit(rendered_dong_4, (150, 480))
        SCREEN.blit(rendered_dong_5, (150, 550))

        #=====PHẦN HÌNH ẢNH HƯỚNG DẪN TRONG INSTRUCTION =====
        #===== PLAY KEYS =====
        arrow_key_img=pygame.image.load("images/arrow.png")
        SCREEN.blit(arrow_key_img, (400,235))

        # ===== ARROW KEY =====
        wasd_key_img = pygame.image.load("images/right.png")
        SCREEN.blit(wasd_key_img, (500, 335))
        wasd_key_img = pygame.image.load("images/left.png")
        SCREEN.blit(wasd_key_img, (500, 400))
        wasd_key_img = pygame.image.load("images/down.png")
        SCREEN.blit(wasd_key_img, (500, 470))
        wasd_key_img = pygame.image.load("images/up.png")
        SCREEN.blit(wasd_key_img, (500, 540))
        pygame.display.update()


menu()


