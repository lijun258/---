import pygame,sys
import random,time,os


screen_size= W,H = 288,512
FPS = 30#设置游戏速度，是游戏刷新即帧数

pygame.init()  #初始化
SCREEN = pygame.display.set_mode((W,H))   #初始化游戏窗口
pygame.display.set_caption('像素鸟')
CLOCK = pygame.time.Clock() #引入时间模块帮助控制游戏的帧率

IMAGES = {}  #引用字典，被用来存储图像数据。通过将图像文件加载到字典中的相应键中，以便在程序中使用这些图像
for image in os.listdir('assets/sprites'):
    name, extension = os.path.splitext(image)  #文件名和后缀分开检索，函数，splitext()用于将文件路径拆分为文件名和扩展名。
    #文件名  扩展名。os.path 是 Python 中用于处理文件路径的模块。
    path = os.path.join('assets/sprites',image)#join() 是 os.path 模块中的一个函数，用于将多个路径组合成一个完整的路径。path 变量就表示了bird.png' 文件的完整路径
    IMAGES[name]  = pygame.image.load(path)  #引用方法及贴入。图像文件对象存储到 IMAGES 字典



floor_Y = H - IMAGES['floor'].get_height()#屏幕高度H减去字典图像的高度，得到floor_Y的值

AUDIO = {}                                #音频文件设置和调用
for audio in os.listdir('assets/audio'):#for是遍历这些文件
    name, extension = os.path.splitext(audio)
    path = os.path.join('assets/audio',audio)
    AUDIO[name] = pygame.mixer.Sound(path)#与前面image功能相同，它则是将文件夹中的音频调用。调用音频并不是开始播放音频，而是将音频文件加载到内存中

#通过调用 play() 方法来播放该声音对象
def main():
    while True:
        AUDIO['1'].play()
        AUDIO['start'].play()  #开始播放音乐
        IMAGES['bgpic'] = IMAGES['day']  #场景固定为白天
        color = 'red'#小鸟颜色固定为红色
        IMAGES['birds'] = [IMAGES[color +'-up'],IMAGES[color+'-mid'],IMAGES[color+'-down']]
        pipe = IMAGES['green-pipe']    #选取绿色水管
        IMAGES['pipes'] = [pipe, pygame.transform.flip(pipe,False,True)] #贴上方的水管，第二个是左右互换，第三个是上下互换方向
        menu_window() #显示游戏菜单界面
        result = game_window()  #开始游戏，并返回游戏结果（例如本游戏得分）
        end_window(result)   #显示游戏结算窗口，通常包括游戏得分、排行榜、重新开始和退出游戏

def menu_window():
#W在这里就是一开始说明的宽
    floor_gap = IMAGES['floor'].get_width() - W #获取地板贴图和屏幕之间宽的差值
    floor_x = 0#水平位置高度为0

    guide_x = (W - IMAGES['guide'].get_width())/2
    guide_y = (floor_Y - IMAGES['guide'].get_height())/2

    bird_x = W*0.2
    bird_y =(H - IMAGES['birds'][0].get_height())/2
    bird_y_move =1   #小鸟运动速度
    bird_y_range = [bird_y - 8,bird_y + 8]  #小鸟运动范围
    idx = 0
    repeat = 5  #控制小鸟飞行画面流畅度
    frames = [0] * repeat + [1] * repeat +[2] * repeat + [1] * repeat

    mck_image = pygame.transform.scale(IMAGES['mck'], (300, 100))  # 音乐按钮
    mck_rect = mck_image.get_rect()
    mck_rect.center = (30, 25)

    start_image = pygame.transform.scale(IMAGES['kai'], (300, 100))  # 开始按钮
    start_rect = start_image.get_rect()
    start_rect.center = (guide_x + 40, guide_y + 270)

    exit_image = pygame.transform.scale(IMAGES['tuichu'], (100, 67))  # 退出按钮，调整图片尺寸
    exit_rect = exit_image.get_rect()
    exit_rect.center = (W - 60, H - 60)


    while True:
        for event in pygame.event.get():  # 获取当前事件
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.MOUSEBUTTONUP:
                if mck_rect.collidepoint(event.pos):
                       AUDIO['1'].stop()
                if start_rect.collidepoint(event.pos):  # 点击开始按钮后的切换
                    return
                if exit_rect.collidepoint(event.pos):  # 点击退出按钮后的程序结束
                    pygame.display.quit()
                    sys.exit()



        floor_x -= 4   #地板每次移动四个像素
        if floor_x <=- floor_gap:   #判断位置并重置地板位置
             floor_x = 0
        bird_y += bird_y_move  #控制小鸟运动
        if bird_y < bird_y_range[0] or bird_y > bird_y_range[1]: #判断小鸟飞出范围即反方向运动
            bird_y_move *= -1


        idx += 1
        idx %= len(frames) #限制idx避免无限增加，多于frames即重置
        SCREEN.blit(IMAGES['bgpic'], (0,0))
        SCREEN.blit(IMAGES['floor'], (floor_x,floor_Y))
        SCREEN.blit(IMAGES['guide'], (guide_x,guide_y))
        SCREEN.blit(IMAGES['birds'][frames[idx]], (bird_x,bird_y))
        SCREEN.blit(IMAGES['tuichu'], (W - 60, H - 60))
        SCREEN.blit(IMAGES['mck'], (30, 25))
        # SCREEN.blit(IMAGES['mcg'],(30,25))
        SCREEN.blit(IMAGES['kai'], (guide_x + 40, guide_y + 270))
        pygame.display.update()  # 刷新窗口
        CLOCK.tick(FPS)


def game_window():
    AUDIO['flap'].play()
    floor_gap = IMAGES['floor'].get_width() - W  # 获取地板贴图和屏幕之剑宽的差值
    floor_x = 0

    bird = Bird(W * 0.2 , H * 0.4)
    score = 0
    n_pairs = 4
    # distance = random.uniform(100,200)    #水管之间的距离
    # pipe_gap = random.uniform(100,130) #表示上下水管间距
    pipe_group = pygame.sprite.Group()



    for i in range(n_pairs):       #水管生成
        distance = random.uniform(155, 180)  # 水管之间的距离
        pipe_gap = random.uniform(100, 120)  # 表示上下水管间距
        pipe_y = random.randint(int(H*0.3),int(H*0.7))   #水管随机生成位置
        pipe_up = Pipe(W + i * distance,pipe_y,True)
        pipe_down = Pipe(W + i * distance,pipe_y - pipe_gap,False)
        pipe_group.add(pipe_up)
        pipe_group.add(pipe_down)

    while True:
        flap =False #默认翅膀不拍动
        for event in pygame.event.get():  # 获取当前事件
            if event.type == pygame.QUIT:
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    flap = True
                    AUDIO['flap'].play()

        floor_x -= 4  # 地板每次移动四个像素
        if floor_x <= - floor_gap:  # 判断位置并重置地板位置
            floor_x = 0

        bird.update(flap)

        first_pipe_up = pipe_group.sprites()[0]  #取得所有水管
        first_pipe_down = pipe_group.sprites()[1]


        if first_pipe_up.rect.right< 0:    #水管移出屏幕就销毁并且新增一个
            pipe_y = random.randint(int(H * 0.3), int(H * 0.7))
            new_pipe_up = Pipe(first_pipe_up.rect.x + n_pairs * distance, pipe_y,True)
            new_pipe_down = Pipe(first_pipe_down.rect.x + n_pairs * distance, pipe_y - pipe_gap,False)
            pipe_group.add(new_pipe_up)
            pipe_group.add(new_pipe_down)
            first_pipe_up.kill()
            first_pipe_down.kill()   #销毁

        pipe_group.update()


                  # 跳转到下一个游戏界面
        if bird.rect.y > floor_Y or bird.rect.y < 0 or pygame.sprite.spritecollide(bird, pipe_group, False,pygame.sprite.collide_mask):  #判断小鸟与地板水管天空的界限碰撞            bird.dying = True
            AUDIO['hit'].play()
            AUDIO['die'].play()
            result = {'bird':bird,'pipe_group':pipe_group,'score':score}   #结果字典，传出游戏结束时小鸟和水管位置
            return result

        if bird.rect.left + first_pipe_up.x_vel <first_pipe_up.rect.centerx <bird.rect.left:   #计算得分  三个判断分别是过中心线前，中心线和中心线后
            AUDIO['score'].play()
            score += 1

        SCREEN.blit(IMAGES['bgpic'], (0, 0))
        pipe_group.draw(SCREEN)
       
        SCREEN.blit(IMAGES['floor'],(floor_x,floor_Y))


        show_score(score)

        SCREEN.blit(bird.image,bird.rect)
        pygame.display.update()  # 刷新窗口
        CLOCK.tick(FPS)


def end_window(result):
    AUDIO['1'].stop()
    floor_gap = IMAGES['floor'].get_width() - W  # 获取地板贴图和屏幕之剑宽的差值
    floor_x = 0
    guide_x = (W - IMAGES['guide'].get_width()) / 2
    guide_y = (floor_Y - IMAGES['guide'].get_height()) / 2

    gameover_x =(W - IMAGES['gameover'].get_width())/2
    gameover_y = (floor_Y - IMAGES['gameover'].get_height())/2

    bird = result['bird']
    pipe_group = result['pipe_group']
    score = result['score']

    start_image = pygame.transform.scale(IMAGES['kai'], (300, 100))  # 开始按钮
    start_rect = start_image.get_rect()
    start_rect.center = (guide_x +40, guide_y + 270)

    exit_image = pygame.transform.scale(IMAGES['tuichu'], (100, 67))  # 退出按钮，调整图片尺寸
    exit_rect = exit_image.get_rect()
    exit_rect.center = (W - 60, H - 60)


    while True:
        if bird.dying:
            bird.go_die()
        else:
            for event in pygame.event.get():  # 获取当前事件
                if event.type == pygame.MOUSEBUTTONUP:
                    if start_rect.collidepoint(event.pos):  # 点击开始按钮后的切换
                        return
                    if exit_rect.collidepoint(event.pos):
                        pygame.display.quit()
                        sys.exit()
        floor_x -= 4  # 地板每次移动四个像素
        if floor_x <= - floor_gap:  # 判断位置并重置地板位置
            floor_x = 0

        SCREEN.blit(IMAGES['day'], (0, 0))
        pipe_group.draw(SCREEN)
        SCREEN.blit(IMAGES['floor'], (0, floor_Y))
        SCREEN.blit(IMAGES['kai'],(guide_x +40 , guide_y + 270))
        SCREEN.blit(IMAGES['tuichu'], (W - 60, H - 60))
        SCREEN.blit(IMAGES['gameover'], (gameover_x, gameover_y))
        show_score(result['score'])
        SCREEN.blit(bird.image,bird.rect)
        pygame.display.update()  # 刷新窗口
        CLOCK.tick(FPS)

def show_score(score):         #计分板位置以及贴图
    score_str = str(score)
    n = len(score_str)
    w = IMAGES['0'].get_width() * 1.1
    x = (W - n * w) / 2
    y = H * 0.1
    for number in score_str:
        SCREEN.blit(IMAGES[number], (x, y))
        x += w

class Bird:
    def __init__(self,x,y):#初始化小鸟坐标
        self.frames = [0]*5 + [1]*5 + [2]*5 + [1]*5
        self.idx = 0
        self.images = IMAGES['birds']
        self.image =IMAGES['birds'][self.frames[self.idx]]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.y_vel = -10   #小鸟初始速度向上
        self.max_y_vel = 10  #y方向上的小鸟能到达的最大速度
        self.gravity = 1  #引入重力加速度模拟物体受到地球引力的影响
        self.rotate = 90 #小鸟初始角度
        self.max_rotate = -20      #小鸟面向角度最大值
        self.rotate_vel = -3    #角度每次改变的值
        self.y_vel_after_flap = -10
        self.rotate_after_flap = 45   #设定震动翅膀后的Y速度的面向角度
        self.dying = False#鸟是否处于死亡状态。初始值为False。

    def update(self,flap = False):

        if flap:
            self.y_vel = self.y_vel_after_flap
            self.rotate = self.rotate_after_flap

        self.y_vel = min(self.y_vel + self.gravity, self.max_y_vel) #更新速度，载入重力加速度，并且使其不超过max_y_vel
        self.rect.y += self.y_vel  #更新小鸟速度
        self.rotate = max(self.rotate +self.rotate_vel,self.max_rotate)  #运动时更新小鸟飞翔角度

        self.idx += 1
        self.idx %= len(self.frames)
        self.image =self.images[self.frames[self.idx]]
        self.image = pygame.transform.rotate(self.image,self.rotate)  #使画面实现角度调整

    def go_die(self):    #小鸟撞到天花板时，垂直下落
        if self.rect.y < floor_Y:
            self.rect.y += self.max_y_vel
            self.rotate = -90
            self.image = self.images[self.frames[self.idx]]
            self.image = pygame.transform.rotate(self.image,self.rotate)
        else:
            self.dying = False

class Pipe(pygame.sprite.Sprite):                  #水管类
    def __init__(self,x,y,upwards = True):   #upwards默认水管开口朝上，所以if写的下方水管，else写的上方水管
        pygame.sprite.Sprite.__init__(self)
        if upwards:
           self.image = IMAGES['pipes'][0]
           self.rect = self.image.get_rect()
           self.rect.x = x
           self.rect.top = y
           self.mask = pygame.mask.from_surface(self.image)
        else:
            self.image = IMAGES['pipes'][1]
            self.rect = self.image.get_rect()
            self.rect.x = x
            self.rect.bottom = y
            self.mask = pygame.mask.from_surface(self.image)
        self.x_vel = -4    #水管X方向速度

    def update(self):
        self.rect.x += self.x_vel



main()

