import pygame,time
import random
from os import path
pygame.init()
screen = pygame.display.set_mode((1200,805))
clock = pygame.time.Clock()
pygame.mixer.init()
shoot_sound = pygame.mixer.Sound('pew.wav')
pygame.mixer.music.load('music1.ogg')
pygame.mixer.music.set_volume(0.4)
background = pygame.image.load('bground.png')
background_rect = background.get_rect(center=(600,400))
player_img = pygame.image.load('ship.png')
meteor_img = pygame.image.load('meteor.png')
meteor_img=pygame.transform.scale(meteor_img, (100,85))
bullet_img = pygame.image.load('bullet1.png')
font_name = pygame.font.match_font('arial')

start = time.time()
# your code

#print("The time of the run:", stop - start)

def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, 'white')
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surf.blit(text_surface, text_rect)
class Player():
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.image=pygame.transform.scale(player_img, (100, 100))
        self.rect = self.image.get_rect()
        self.rect.centerx = 600
        self.rect.bottom = 790
        self.speedx = 2
    def update(self):
        button= pygame.key.get_pressed()
        if button[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if button[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if self.rect.right > 1200:
            self.rect.right = 1200
        if self.rect.left < 0:
            self.rect.left = 0
    def draw(self):
        screen.blit(self.image,self.rect)
class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.transform.scale(bullet_img, (10,50))
        self.rect = self.image.get_rect()
        self.rect.centerx=player.rect.centerx
        self.rect.centery=player.rect.centery-50
        self.speedy =10
    def update(self):
        self.rect.y -= self.speedy
        if self.rect.bottom < 20:
            self.rect.centerx=player.rect.centerx
            self.rect.centery=player.rect.centery
    def draw(self):
        screen.blit(self.image,self.rect)
class Stone(pygame.sprite.Sprite):
    def __init__(self,sc):
        super().__init__()
        self.image = meteor_img
        self.sc=sc
        self.image=pygame.transform.scale(self.image,(sc*5,sc*5))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(1150)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 8)
        self.speedx = random.randrange(-3, 3)
    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > 810 or self.rect.left < -25 or self.rect.right > 1220:
            self.rect.x = random.randrange(1200 - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 8)    
    def draw(self):
        screen.blit(self.image,self.rect)
player = Player()
bullet=Bullet()
stones_group=pygame.sprite.Group()
explosion=[0]*9
for i in range (9):
    f_name='exp'+str(i)+'.png'
    explosion[i]=pygame.image.load(path.join('imgg',f_name))
    explosion[i]=pygame.transform.scale(explosion[i],(70,70))
Q=30
for i in range (Q):
    stone=Stone(random.randint(1,6))
    stone.update()
    stones_group.add(stone)
x,y=2000,2000
k,s,q,q1,q2=0,0,0,0,0
pygame.mixer.music.play(loops=-1)
score = 0
t=-1
while True:
    clock.tick(60)
    t+=1
    t1=round(t/60)
    tt = (time.time())
    print("The time of the run:", round(tt - start))
    screen.blit(background, background_rect)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    player.update()
    player.draw()
    bullet.update()
    bullet.draw()
    stones_group.update()
    stones_group.draw(screen)
    collision= pygame.sprite.spritecollide(bullet,stones_group,True)
    collision1=pygame.sprite.spritecollide(player,stones_group,True)
    #print(collision1)
    if len(stones_group.sprites())==0: 
        draw_text(screen, 'Game over', 45, 700,700)
        q=q+1
        if q==600:
            exit()
    if collision:
        score=score+1
        shoot_sound.play()
        k=1
        x1=bullet.rect.centerx
        y1=bullet.rect.centery
    if k==1:
        s=s+1
        s1=s%9
        screen.blit(explosion[s1],(x1,y1))
        if s1==8:
            k=0
    if collision1:
        q1=q1+1
        shoot_sound.play()
    
    if q1!=0:
        draw_text(screen, 'Penalty=', 38, 100,700)
        draw_text(screen, str(q1), 38, 200,700)
        
        
    draw_text(screen, 'Time in sec  =', 38, 490, 10)
    counter=round(tt - start)
    #draw_text(screen, str(t1), 38, 620, 10)
    draw_text(screen, str(counter), 38, 670, 10)

    draw_text(screen, 'Score  =', 38, 100, 650)
    draw_text(screen, str(score), 38, 200, 650)

    pygame.display.update()
