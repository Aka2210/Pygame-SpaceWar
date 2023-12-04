import pygame #最主要的函式庫
import random #機率物品設定
import os #載入圖片時方便指定路徑的函式
#sprite 用來表示遊戲上的物件

#數值設定
pow_drop_rate = 0.85# 機率為(1 - 0.85)
lives_numbers = 3
init_health = 100
attack_delay = 600
invincible_time = 1000
hidden_time = 1000
gunup_time = 5000
burst_time = 1500
FPS = 144
WHITE = (255,255,255)
GREEN = (0,255,0)
BLACK = (0, 0, 0)
WIDTH = 500
HEIGHT = 600

#遊戲初始化
pygame.init()
pygame.mixer.init#初始化音效模組
running = True
 #創建視窗，寬度高度
screen = pygame.display.set_mode((WIDTH,HEIGHT))
#載入圖片 記得先初始化遊戲 否則會錯誤
background_img = pygame.image.load(os.path.join("img", "background.png")).convert()#前者為最左方pygame內的資料夾 後者為資料夾內的檔案 convert將圖片轉換成pygame較易讀取的格式
player_img = pygame.image.load(os.path.join("img", "player.png")).convert()
start_img = pygame.image.load(os.path.join("img", "start.png"))
start_img = pygame.transform.scale(start_img, (200, 100))
exit_img = pygame.image.load(os.path.join("img", "exit.png"))
exit_img = pygame.transform.scale(exit_img, (150, 75))
ui_img = pygame.image.load(os.path.join("img", "ui.png"))
ui_img.set_colorkey(WHITE)

# rock_img = pygame.image.load(os.path.join("img", "rock.png")).convert()
bullet_img = pygame.image.load(os.path.join("img", "bullet.png")).convert()
player_mini_img = pygame.transform.scale(player_img, (25, 19))
player_mini_img.set_colorkey(BLACK)
rock_imgs = []#建立列表放置不同石頭圖片
expl_anim = {}#爆炸圖片字典
expl_anim['lg'] = []
expl_anim['sm'] = []
expl_anim['player'] = []
power_img = {}
power_img['health'] =  pygame.image.load(os.path.join("img", "health.png")).convert()#引入圖片
power_img['lightning'] =  pygame.image.load(os.path.join("img", "lightning.png")).convert()#引入圖片
power_img['burst'] = pygame.image.load(os.path.join("img", "burst.png")).convert()
power_img['burst'] = pygame.transform.scale(power_img['burst'], (100, 50))

for i in range(7):
    rock_imgs.append(pygame.image.load(os.path.join("img", f"rock{i}.png")).convert())#在""前加f就可以在裡面使用變數了 將不同圖片載入列表裡
for i in range(9) :
    expl_img =  pygame.image.load(os.path.join("img", f"expl{i}.png")).convert()#引入九種圖片方便做成動畫
    expl_img.set_colorkey(BLACK)#去除黑色背景
    expl_anim['lg'].append(pygame.transform.scale(expl_img, (75, 75)))
    expl_anim['sm'].append(pygame.transform.scale(expl_img, (30, 30)))
    player_expl_img =  pygame.image.load(os.path.join("img", f"player_expl{i}.png")).convert()#引入九種圖片方便做成動畫
    player_expl_img.set_colorkey(BLACK)#去除黑色背景
    expl_anim['player'].append(player_expl_img)

#載入音樂
shoot_sound = pygame.mixer.Sound(os.path.join("sound", "shoot.wav"))#前者為最左方pygame內的資料夾 後者為要引入的檔案
gun_sound = pygame.mixer.Sound(os.path.join("sound", "pow1.wav"))#前者為最左方pygame內的資料夾 後者為要引入的檔案
shield_sound = pygame.mixer.Sound(os.path.join("sound", "pow0.wav"))#前者為最左方pygame內的資料夾 後者為要引入的檔案
die_sound = pygame.mixer.Sound(os.path.join("sound", "rumble.ogg"))#前者為最左方pygame內的資料夾 後者為要引入的檔案
expl_sounds = [pygame.mixer.Sound(os.path.join("sound", "expl0.wav")), pygame.mixer.Sound(os.path.join("sound", "expl1.wav"))]#建立列表存入兩種不同音效 撥放音效時隨機撥放
pygame.mixer.music.load(os.path.join("sound", "background.ogg"))#因為要持續撥放所以與上面兩種引入方式不同
pygame.mixer.music.set_volume(0.1)#調整背景音效大小
power_img['health'] = pygame.transform.scale(power_img['health'], (30, 30))
#引入字體
font_name = os.path.join("font.ttf") 

def draw_text(surf, text, size, x, y):#把文字寫入畫面 surf代表寫在什麼平面上 text是要寫的文字
    font = pygame.font.Font(font_name, size)#傳入字體與大小
    text_surface = font.render(text, True, (255, 255, 255))#text代表要渲染的文字 True代表是否使用反鋸齒(讓字體看起來更平順) 最後是顏色
    text_rect = text_surface.get_rect()#取得平面的x、y
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)#在傳入的平面上對應位置畫出文字

def produce_new_rock():#重新產生石頭
    rock = Rock()
    all_sprites.add(rock)
    rocks.add(rock)

def draw_health(surf, hp, x, y):#畫出生命條
    if hp < 0 :
        hp = 0
    BAR_LENGTH = 100#設定生命條長度、高度
    BAR_HIGHT = 10
    fill = (hp / init_health) * BAR_LENGTH
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HIGHT)#給予矩形長度、高度、位置
    fill_rect = pygame.Rect(x, y, fill, BAR_HIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)#fill_rect代表以什麼方式畫出來 這裡是填滿 下面是外框
    pygame.draw.rect(surf, WHITE, outline_rect, 2)#2代表外框有幾象素

def draw_lives(surf, lives, img, x, y):
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = 470 - 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def draw_init():
    screen.blit(background_img, (0, 0))
    draw_text(screen, '打隕石', 64, WIDTH / 2, HEIGHT / 4)
    draw_text(screen, '<- ->移動飛船 空白鍵發射子彈 ESC暫停', 22, WIDTH / 2, HEIGHT / 2)
    screen.blit(start_img, (WIDTH/3 - 20, HEIGHT/3 * 2 - 70))
    screen.blit(exit_img, (WIDTH/3 + 5, HEIGHT/3 * 2 + 10))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x > 174 and mouse_x < 319 and mouse_y > 368 and mouse_y < 390:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    return False
        elif mouse_x > 185 and mouse_x < 302 and mouse_y > 437 and mouse_y < 466:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.quit()
                    return True

        for event in pygame.event.get() :#後者回傳現在發生的所有事件，包括滑鼠位置、按鍵輸入等(回傳型別為列表)
            if event.type == pygame.QUIT:
                pygame.quit()
                return True
    
def draw_wait():
    screen.blit(background_img, (0, 0))
    screen.blit(ui_img, (-130, 100))
    pygame.display.update()
    waiting = True
    while waiting:
        clock.tick(FPS)
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if mouse_x > 206 and mouse_x < 323 and mouse_y > 280 and mouse_y < 322:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    waiting = False
                    return False
        elif mouse_x > 188 and mouse_x < 333 and mouse_y > 349 and mouse_y < 411:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    pygame.quit()
                    return True
        elif mouse_x > 204 and mouse_x < 321 and mouse_y > 197 and mouse_y < 241:
            for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP:
                    return 3
        for event in pygame.event.get() :#後者回傳現在發生的所有事件，包括滑鼠位置、按鍵輸入等(回傳型別為列表)
            if event.type == pygame.QUIT:
                pygame.quit()
                return True

class Player(pygame.sprite.Sprite):#創建類別繼承內建的sprite類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite的初始函式
        self.image = player_img#image表示要顯示的圖
        self.image = pygame.transform.scale(player_img, (50, 38))#改變圖片大小
        self.image.set_colorkey(BLACK)#將圖片內的某個顏色透明化
        #self.image.fill((0,255,0))#改變圖片顏色
        self.rect = self.image.get_rect()#rect用來定位圖片
        self.radius = 20#給予碰撞箱半徑
        #pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)#畫在哪一個圖片上，顏色，中心點位置，半徑 此指令將碰撞箱畫出來，方便判斷碰撞箱是否太大或太小
        self.rect.x = 200#設定x座標
        self.rect.y = 200#設定y座標(左上角為(0, 0))
        self.rect.centerx = WIDTH/2#將遊戲物件中心x座標定位
        self.rect.bottom = HEIGHT - 10#將遊戲物件底部y座標定位
        self.health = init_health#給予飛船血條
        self.lives = lives_numbers
        self.hidden = True
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
        self.shoot_time = -500
        self.invincibility = True
        self.flashing_detect = 0
        self.past_center = self.rect.center
        self.reset_flashing_center = False
        self.invincibility_time = 0
        self.speed = 2
        self.burst_time = 0
        self.attack_delay = 600

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.burst_time > burst_time:
            self.attack_delay = 600

        if self.gun > 1 and now - self.gun_time > gunup_time:
            self.gun = 1
            self.gun_time = now

        if self.hidden and now - self.hide_time > hidden_time:
            self.hidden = False
            self.rect.centerx = WIDTH / 2
            self.rect.bottom = HEIGHT - 10
            self.invincibility = True
            self.invincibility_time = pygame.time.get_ticks()

        key_pressed = pygame.key.get_pressed()#判斷按鍵是否被按,若有回傳true

        if key_pressed[pygame.K_RIGHT]:#判斷右鍵是否被按
            self.rect.x += self.speed

        if key_pressed[pygame.K_LEFT]:#判斷左鍵是否被按
            self.rect.x -= self.speed

        if self.rect.left > WIDTH:#若物件左邊座標大於寬度則將右邊座標重設為0
            self.rect.right = 0

        if self.rect.right < 0:
            self.rect.left = WIDTH

        if now - self.invincibility_time > invincible_time :
            self.invincibility = False

        if self.invincibility and self.flashing_detect == 0:
            self.past_center = self.rect.center
            self.rect.center = (WIDTH / 2, HEIGHT + 500)
            self.flashing_detect = 1

        elif self.flashing_detect == 1:
            self.rect.center = self.past_center
            self.flashing_detect = 0

    def shoot(self):
        self.now = pygame.time.get_ticks()
        if  self.now - self.shoot_time > self.attack_delay:
            self.shoot_time = self.now
            if not(self.hidden):#不在隱藏狀態才可發射子彈
                if self.gun == 1:
                    bullet = Bullet(self.rect.centerx, self.rect.top)
                    all_sprites.add(bullet)
                    bullets.add(bullet)#將子彈加入碰撞判斷需要用到的群組
                    shoot_sound.play()
                elif self.gun == 2:
                    bullet1 = Bullet(self.rect.left, self.rect.centery)
                    bullet2 = Bullet(self.rect.right, self.rect.centery)
                    all_sprites.add(bullet1)
                    all_sprites.add(bullet2)
                    bullets.add(bullet1)#將子彈加入碰撞判斷需要用到的群組
                    bullets.add(bullet2)
                    shoot_sound.play()

    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (WIDTH / 2, HEIGHT + 500)

    def gunup(self):
        self.gun = 2
        self.gun_time = pygame.time.get_ticks()

    def burst(self):
        self.attack_delay = 100
        self.burst_time = pygame.time.get_ticks()
       
class Rock(pygame.sprite.Sprite):#創建類別繼承內建的sprite類別
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite的初始函式
        self.image_ori = random.choice(rock_imgs)#訂一個原始未失真的圖片 圖片由石頭列表中隨機選擇
        self.image = self.image_ori.copy()#image表示要顯示的圖, 訂一個會失真的圖片
        #self.image.fill((255,0,0))#改變圖片顏色
        self.image_ori.set_colorkey(BLACK)#將圖片內的某個顏色透明化
        self.rect = self.image.get_rect()#rect用來定位圖片
        self.radius = self.rect.width * 0.85 / 2#給予碰撞箱半徑
        #pygame.draw.circle(self.image, (255, 0, 0), self.rect.center, self.radius)#畫在哪一個圖片上，顏色，中心點位置，半徑 此指令將碰撞箱畫出來，方便判斷碰撞箱是否太大或太小
        self.rect.x = random.randrange(0, WIDTH - self.rect.width)#設定x座標
        self.rect.y = random.randrange(-180, -100)#設定y座標(左上角為(0, 0))
        self.speedy = random.randrange(2, 5)#垂直速度
        self.speedx = random.randrange(-3, 3)#水平速度
        self.rot_degree = random.randrange(-3, 3)
        self.total_degree = 0

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360#需要用原始圖片去轉動的原因是如果連續轉動，每次轉動造成的失真疊加起來會產生錯誤，因此只轉動一次然後讓角度疊加，可以最小化失真
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree) #將圖片轉動某個角度
        center = self.rect.center#儲存原本的中心點 以下三個指令避免石頭旋轉時中心點改變造成的抽動
        self.rect = self.image.get_rect()#重新訂為中心點
        self.rect.center = center#將中心點設為原本的中心點  

    def update(self):
        self.rotate()
        self.rect.y += self.speedy   
        self.rect.x += self.speedx
        if self.rect.top > HEIGHT or self.rect.left > WIDTH or self.rect.right < 0:
            self.rect.x = random.randrange(0, WIDTH - self.rect.width)#設定x座標
            self.rect.y = random.randrange(-100, -40)#設定y座標(左上角為(0, 0))
            self.speedy = random.randrange(2, 7)#垂直速度
            self.speedx = random.randrange(-3, 3)#水平速度

class Bullet(pygame.sprite.Sprite):#創建類別繼承內建的sprite類別
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite的初始函式
        self.image = bullet_img#image表示要顯示的圖
        self.image.set_colorkey(BLACK)#將圖片內的某個顏色透明化
        #self.image.fill((255,255,0))#改變圖片顏色
        self.rect = self.image.get_rect()#rect用來定位圖片
        self.rect.centerx = x#設定x座標
        self.rect.bottom = y#設定y座標(左上角為(0, 0))
        self.speedy = -10#垂直速度
    
    def update(self):
        self.rect.y += self.speedy   
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):#創建類別繼承內建的sprite類別
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite的初始函式
        self.size = size
        self.image = expl_anim[self.size][0]#image表示要顯示的圖
        self.rect = self.image.get_rect()#rect用來定位圖片
        self.rect.center = center#設定x座標
        self.frame = 0
        self.last_update = pygame.time.get_ticks()#=後面回傳開始到現在經過的毫秒數
        self.frame_rate = 70#幾毫秒更新圖片 越高則動畫速度越慢
    
    def update(self):
        if player.lives == 0:
            self.frame_rate = 200
            player.kill()
            
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(expl_anim[self.size]) :
                self.kill()#已經跑完動畫 刪除圖片
            else:#更新圖片
                self.image = expl_anim[self.size][self.frame]
                center = self.rect.center#重新定位
                self.rect = self.image.get_rect()
                self.rect.center = center

class Power(pygame.sprite.Sprite):#創建類別繼承內建的sprite類別
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)#呼叫內建sprite的初始函式
        self.type = random.choice(['health', 'lightning', 'burst'])#image表示要顯示的圖
        self.image = power_img[self.type]
        self.image.set_colorkey(BLACK)#將圖片內的某個顏色透明化
        self.rect = self.image.get_rect()#rect用來定位圖片
        self.rect.center = center#設定x座標
        self.speedy = 3
    
    def update(self):
        self.rect.y += self.speedy   
        if self.rect.top > HEIGHT:
            self.kill()

pygame.mixer.music.play(-1)#撥放音樂 數字代表重複撥放幾次 -1代表無限

pygame.display.set_caption("小遊戲")#更改左上角名稱
pygame.display.set_icon(player_mini_img)#更改左上角圖片
clock = pygame.time.Clock()

#遊戲迴圈
show_init = True
running = True
time_out_detect = False

while running :#遊戲迴圈避免視窗瞬間消失
    if show_init:
        close = draw_init()#關閉視窗!=結束程式 因此若關閉視窗 回傳True 使下面判斷可離開遊戲迴圈 進而結束程式
        if close:
            break
        show_init = False
        all_sprites = pygame.sprite.Group()#創建遊戲物件群組
        powers = pygame.sprite.Group()
        rocks = pygame.sprite.Group()#建立群組，等等引入函式用來偵測碰撞
        bullets = pygame.sprite.Group()#建立群組，等等引入函式用來偵測碰撞
        player = Player()#生成遊戲物件
        all_sprites.add(player)#將遊戲物件加入遊戲物件群組中
        for x in range(8):
            produce_new_rock()
        score = 0

    clock.tick(FPS)#一秒鐘內最多只能執行FPS次(避免好的電腦跑1萬次差的電腦卻只能跑1千次)

    #取得輸入
    for event in pygame.event.get() :#後者回傳現在發生的所有事件，包括滑鼠位置、按鍵輸入等(回傳型別為列表) 以此方式判斷某按鍵是否被按一下
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_ESCAPE and not time_out_detect:
                time_out_detect = True
            elif event.key == pygame.K_ESCAPE and time_out_detect:
                time_out_detect = False

    key_pressed = pygame.key.get_pressed()#判斷按鍵是否被按,若有回傳true 以此方式判斷某按鍵是否被按住

    if key_pressed[pygame.K_SPACE]:
        player.shoot()
        
    #更新遊戲
    if not time_out_detect:#如果遊戲沒有暫停，所有物件更新移動
        all_sprites.update()#all_sprites內的物件都會執行self.update

    #判斷子彈與石頭相撞
    hits = pygame.sprite.groupcollide(rocks, bullets, True, True)#兩者碰撞後是否要刪掉 True代表要刪掉 並回傳碰撞的石頭和子彈
    for hit in hits:#刪除石頭後要重新產生石頭 並加入碰撞箱
        random.choice(expl_sounds).play()
        expl = Explosion(hit.rect.center, 'lg')
        all_sprites.add(expl)
        score += (60 - (int)(hit.radius)) #分數+= (100 - 石頭半徑)
        if random.random() > pow_drop_rate:#函式回傳0~1之間的隨機值
            pow = Power(hit.rect.center)
            all_sprites.add(pow)
            powers.add(pow)#將物件+入寶物的群組，之後用來判斷寶物與飛船是否相撞
        produce_new_rock()
    #判斷石頭、飛船相撞
    hits = pygame.sprite.spritecollide(player, rocks, True, pygame.sprite.collide_circle)#True、False代表是否要把rocks刪掉 並回傳所有碰撞到player的石頭 最後則是碰撞箱形狀
    for hit in hits:
        produce_new_rock()
        if not player.invincibility:
            player.health -= hit.radius
            if player.health > 0:
                expl = Explosion(hit.rect.center, 'sm')
                all_sprites.add(expl)
            else:
                die = Explosion(player.rect.center, 'player')
                all_sprites.add(die)
                die_sound.play()
                player.lives -= 1
                player.health = init_health
                player.hide()

    #判斷寶物、飛船相撞
    hits = pygame.sprite.spritecollide(player, powers, True)#True、False代表是否要把rocks刪掉 並回傳所有碰撞到player的石頭
    for hit in hits:
        if hit.type == 'health':
            if player.health < init_health and player.health > 0:
                player.health += 20
            if player.health > init_health:
                player.health = init_health
            shield_sound.play()
        elif hit.type == 'lightning':
            player.gunup()
            gun_sound.play()
        elif hit.type == 'burst':
            player.burst()
            gun_sound.play()

    if player.lives == 0 and not(die.alive()) :#die.alive()判斷die物件是否還存在 若不存在 則進入elif 則遊戲結束(用來確保死亡音效、動畫滿完才會結束遊戲)
        show_init = True   
            

    #畫面顯示
    screen.blit(background_img, (0, 0))
    all_sprites.draw(screen)#將物件畫入遊戲中
    draw_text(screen, str(score), 18, WIDTH/2, 10) 
    draw_health(screen, player.health, 5, 15)
    draw_lives(screen, player.lives, player_mini_img, WIDTH - 100, 15) 
    if time_out_detect and time_out_detect != 3:
        time_out_detect = draw_wait()
    if time_out_detect and time_out_detect != 3:
        break
    elif time_out_detect == 3:
        time_out_detect = False
        all_sprites = pygame.sprite.Group()#創建遊戲物件群組
        powers = pygame.sprite.Group()
        rocks = pygame.sprite.Group()#建立群組，等等引入函式用來偵測碰撞
        bullets = pygame.sprite.Group()#建立群組，等等引入函式用來偵測碰撞
        player = Player()#生成遊戲物件
        all_sprites.add(player)#將遊戲物件加入遊戲物件群組中
        for x in range(8):
            produce_new_rock()
        score = 0

    pygame.display.update()#更新畫面
