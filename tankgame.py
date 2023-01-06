from pickle import NONE
from time import time
from turtle import speed
import pygame
from pygame.locals import *
import random

_dp=pygame.display
BGCOLOR=pygame.Color(0,0,0)
TXTCOLOR=pygame.Color(0,255,0)

class MainGame():
    window=None
    SCREEN_WIDTH=800
    SCREEN_HEIGHT=600
    MYTANK=None
    ENEMIES=[]
    ENEMY_COUNT = 5
    BULLETS=[]
    ENEMY_BULLETS=[]
    EXPLODES=[]
    WALLS=[]

    def __init__(self):
        pass
    def start_game(self):
        _dp.init()
        MainGame.window = _dp.set_mode((MainGame.SCREEN_WIDTH, MainGame.SCREEN_HEIGHT))
        self.create_me()
        #MainGame.MYTANK = Tank(300,200)
        self.create_enemy()
        self.create_wall()
        _dp.set_caption("Tank War")
        while True:
            MainGame.window.fill(BGCOLOR)
            self.get_event()
            MainGame.window.blit(self.get_text('Enemies left: '+str(len(MainGame.ENEMIES))),(5,5))
            self.blit_wall()
            if MainGame.MYTANK and MainGame.MYTANK.exist:
                MainGame.MYTANK.displayTank()
            else:
                del MainGame.MYTANK
                MainGame.MYTANK=None
            self.blit_enemy()
            if MainGame.MYTANK and not MainGame.MYTANK.stop:
                MainGame.MYTANK.move()
                MainGame.MYTANK.hit_wall()
                MainGame.MYTANK.hit_enemy()
            self.blit_bullet()
            self.blit_enemy_bullet()
            self.show_explosion()
            _dp.update()

    def create_enemy(self):
        num_list = [1,2,3,4,5,6,7]
        left = random.sample(num_list, MainGame.ENEMY_COUNT)
        top = 100
        for i in left:
            speed = random.randint(2,5)
            eTank=Enemy(i*100,top,speed)
            MainGame.ENEMIES.append(eTank)
    
    def create_me(self):
        MainGame.MYTANK = Me(300, 290)

    def create_wall(self):
        for i in range(0,7):
            wall = Wall(180*i,200)
            MainGame.WALLS.append(wall)
            wall = Wall(180*i,370)
            MainGame.WALLS.append(wall)
    
    def blit_wall(self):
        for w in MainGame.WALLS:
            if w.exist:
                w.displayWall()
            else:
                MainGame.WALLS.remove(w)

    def blit_enemy(self):
        for e in MainGame.ENEMIES:
            if e.exist:
                num = random.randint(1,60)
                e.displayTank()
                e.rnd_moves()
                e.hit_wall()
                if MainGame.MYTANK and MainGame.MYTANK.exist:
                    e.hit_mytank()
                if num==1:
                    e_bullet = e.shoot()
                    MainGame.ENEMY_BULLETS.append(e_bullet)
            else:
                MainGame.ENEMIES.remove(e)

    def blit_bullet(self):
        for b in MainGame.BULLETS:
            if b.exist:
                b.displayBullet()
                b.bullet_move()
                b.hit_enemy()
                b.hit_wall()
            else:
                MainGame.BULLETS.remove(b)

    def blit_enemy_bullet(self):
        for e in MainGame.ENEMY_BULLETS:
            if e.exist:
                e.displayBullet()
                e.bullet_move()
                e.hit_wall()
                if MainGame.MYTANK and MainGame.MYTANK.exist:
                    e.hit_me()
            else:
                MainGame.ENEMY_BULLETS.remove(e)

    def show_explosion(self):
        for exp in MainGame.EXPLODES:
            if exp.exist:
                exp.displayExplode()
            else:
                MainGame.EXPLODES.remove(exp)

    def get_event(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.end_game()
            if event.type == KEYDOWN:
                if MainGame.MYTANK and MainGame.MYTANK.exist:
                    if event.key == K_LEFT:
                        print('Moving left')
                        MainGame.MYTANK.dir='L'
                        MainGame.MYTANK.stop=False
                    if event.key == K_RIGHT:
                        print('Moving right')
                        MainGame.MYTANK.dir='R'
                        MainGame.MYTANK.stop=False
                    if event.key == K_UP:
                        print('Moving upward')
                        MainGame.MYTANK.dir='U'
                        MainGame.MYTANK.stop=False
                    if event.key == K_DOWN:
                        print('Moving downward')
                        MainGame.MYTANK.dir='D'
                        MainGame.MYTANK.stop=False
                    if event.key == K_SPACE:
                        print('Fire')
                        if len(MainGame.BULLETS)<3:
                            b=Bullet(MainGame.MYTANK)
                            MainGame.BULLETS.append(b)
                        else:
                            print('Bullet outage')
                
                if not MainGame.MYTANK:
                    if event.key == K_ESCAPE:
                        self.create_me()

            if event.type == KEYUP:
                if event.key == K_DOWN or event.key == K_LEFT or event.key == K_RIGHT or event.key == K_UP:
                    if MainGame.MYTANK and MainGame.MYTANK.exist:
                        MainGame.MYTANK.stop=True
    
    def get_text(self, text):
        pygame.font.init()
        font = pygame.font.SysFont('arial black', 20)
        surface = font.render(text, True, TXTCOLOR)
        return surface

    def end_game(self):
        print('Thanks for playing')
        exit()

class Bases(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite().__init__(self)


class Tank(Bases):
    def __init__(self,left,top):
        self.img={
            'U':pygame.image.load('img/tank-up.png'),
            'L':pygame.image.load('img/tank-left.png'),
            'D':pygame.image.load('img/tank-down.png'),
            'R':pygame.image.load('img/tank-right.png')
        }
        self.dir='U'
        self.current=self.img[self.dir]
        self.rect=self.current.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.speed=3
        self.stop=True
        self.exist=True
        self.oldL=self.rect.left
        self.oldT=self.rect.top

    def move(self):
        self.oldL=self.rect.left
        self.oldT=self.rect.top
        if self.dir=='L':
            if self.rect.left>0:
                self.rect.left-=self.speed
        if self.dir=='R':
            if self.rect.left+self.rect.height<MainGame.SCREEN_WIDTH:
                self.rect.left+=self.speed
        if self.dir=='U':
            if self.rect.top>0:
                self.rect.top-=self.speed
        if self.dir=='D':
            if self.rect.top+self.rect.height<MainGame.SCREEN_HEIGHT:
                self.rect.top+=self.speed

    def stay(self):
        self.rect.left=self.oldL
        self.rect.top=self.oldT

    def hit_wall(self):
        for w in MainGame.WALLS:
            if pygame.sprite.collide_rect(w, self):
                self.stay()

    def shoot(self):
        return Bullet(self)

    def displayTank(self):
        self.current=self.img[self.dir]
        MainGame.window.blit(self.current,self.rect)

class Me(Tank):
    def __init__(self,left,top):
        super(Me,self).__init__(left,top)

    def hit_enemy(self):
        for e in MainGame.ENEMIES:
            if pygame.sprite.collide_rect(e, self):
                self.stay()

class Enemy(Tank):
    def __init__(self,left,top,speed):
        super(Enemy,self).__init__(left,top)
        self.img={
            'U':pygame.image.load('img/enemy-up.png'),
            'L':pygame.image.load('img/enemy-left.png'),
            'D':pygame.image.load('img/enemy-down.png'),
            'R':pygame.image.load('img/enemy-right.png')
        }
        self.dir=self.rnd_direction()
        self.current=self.img[self.dir]
        self.rect=self.current.get_rect()
        self.rect.left=left
        self.rect.top=top
        self.speed=speed
        self.stop=True
        self.step=40
        self.oldL=self.rect.left
        self.oldT=self.rect.top
    
    def rnd_direction(self):
        num=random.randint(1,4)
        if num==1:
            return 'U'
        if num==2:
            return 'D'
        if num==3:
            return 'L'
        if num==4:
            return 'R'

    def move(self):
        self.oldL=self.rect.left
        self.oldT=self.rect.top
        if self.dir=='L':
            if self.rect.left>0:
                self.rect.left-=self.speed
        if self.dir=='R':
            if self.rect.left+self.rect.height<MainGame.SCREEN_WIDTH:
                self.rect.left+=self.speed
        if self.dir=='U':
            if self.rect.top>0:
                self.rect.top-=self.speed
        if self.dir=='D':
            if self.rect.top+self.rect.height<MainGame.SCREEN_HEIGHT:
                self.rect.top+=self.speed

    def stay(self):
        self.rect.left=self.oldL
        self.rect.top=self.oldT

    def hit_mytank(self):
        if pygame.sprite.collide_rect(self, MainGame.MYTANK):
            self.stay()

    def hit_wall(self):
        for w in MainGame.WALLS:
            if pygame.sprite.collide_rect(w, self):
                self.stay()
    
    def rnd_moves(self):
        if self.step<=0:
            self.dir=self.rnd_direction()
            self.step=40
        else:
            self.move()
            self.step-=1

    def shoot(self):
        return Bullet(self)

    def displayTank(self):
        self.current=self.img[self.dir]
        MainGame.window.blit(self.current,self.rect)

class Bullet(Bases):
    def __init__(self,tank):
        self.img=pygame.image.load('img/bullet.png')
        self.speed = 6
        self.dir=tank.dir
        self.rect=self.img.get_rect()
        if self.dir=='L':
            self.rect.left=tank.rect.left-self.rect.width
            self.rect.top=tank.rect.top+tank.rect.width/2-self.rect.width/2
        elif self.dir=='R':
            self.rect.left=tank.rect.left+tank.rect.width
            self.rect.top=tank.rect.top+tank.rect.width/2-self.rect.width/2
        elif self.dir=='U':
            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top-self.rect.height
        elif self.dir=='D':
            self.rect.left=tank.rect.left+tank.rect.width/2-self.rect.width/2
            self.rect.top=tank.rect.top+tank.rect.height
        self.exist=True
            
    def bullet_move(self):
        if self.dir=='L':
            if self.rect.left>0:
                self.rect.left-=self.speed
            else:
                self.exist=False
        elif self.dir=='R':
            if self.rect.left<MainGame.SCREEN_WIDTH-self.rect.height:
                self.rect.left+=self.speed
            else:
                self.exist=False
        elif self.dir=='U':
            if self.rect.top>0:
                self.rect.top-=self.speed
            else:
                self.exist=False
        elif self.dir=='D':
            if self.rect.top<MainGame.SCREEN_HEIGHT-self.rect.width:
                self.rect.top+=self.speed
            else:
                self.exist=False

    def displayBullet(self):
        MainGame.window.blit(self.img, self.rect)

    def hit_enemy(self):
        for e in MainGame.ENEMIES:
            if pygame.sprite.collide_rect(e, self):
                explode=Explode(e)
                MainGame.EXPLODES.append(explode)
                self.exist=False
                e.exist=False
    
    def hit_me(self):
        if pygame.sprite.collide_rect(self,MainGame.MYTANK):
            explode=Explode(MainGame.MYTANK)
            MainGame.EXPLODES.append(explode)
            self.exist=False
            MainGame.MYTANK.exist=False
    
    def hit_wall(self):
        for w in MainGame.WALLS:
            if pygame.sprite.collide_rect(w, self):
                self.exist=False
                w.hp-=1
                if w.hp<=0:
                    w.exist = False

class Explode():
    def __init__(self,tank):
        self.rect = tank.rect
        self.step = 0
        self.img = [pygame.image.load('img/explosion0.png'),
                    pygame.image.load('img/explosion1.png'),
                    pygame.image.load('img/explosion2.png'),
                    pygame.image.load('img/explosion3.png'),
                    pygame.image.load('img/explosion4.png')]
        self.effect = self.img[self.step]
        self.exist=True

    def displayExplode(self):
        if self.step<len(self.img):
            MainGame.window.blit(self.effect, self.rect)
            self.effect = self.img[self.step]
            self.step+=1
        else:
            self.exist=False
            self.step=0

class Wall():
    def __init__(self,left,top):
        self.img=pygame.image.load('img/brick.png')
        self.rect=self.img.get_rect()
        self.rect.left = left
        self.rect.top = top
        self.exist = True
        self.hp=3

    def displayWall(self):
        MainGame.window.blit(self.img, self.rect)

class BGM():
    def __init__(self):
        pass
    def play(self):
        pass

MainGame().start_game()
