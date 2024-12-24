import pygame
import sys
import random
import math


# https://www.gameart2d.com/santa-claus-free-sprites.html
# https://www.pngitem.com/download/iombmmb_christmas-gift-sprite-hd-png-download/


pygame.init()
info = pygame.display.Info()
w, h = info.current_w, info.current_h
screen = pygame.display.set_mode((info.current_w, info.current_h), pygame.RESIZABLE)
pygame.display.set_caption('physics, math, code & fun')

pygame.mixer.init()
beep = pygame.mixer.Sound("beep.mp3")
font = pygame.font.SysFont('Arial', 50)
clock = pygame.time.Clock()


delta_time = 0.0
dt = 0.001
t = 0



class Santa(pygame.sprite.Sprite):
    def __init__(self, pos, santa_id):
        super().__init__()

        self.dead_imgs = []
        self.run_imgs = []
        
        for i in range(1, 18):  
            img = pygame.image.load(f'dead/Dead ({i}).png').convert_alpha()
            img = pygame.transform.scale(img, (280, 192))  
            self.dead_imgs.append(img)
            
        for i in range(1, 12):  
            img = pygame.image.load(f'run/Run ({i}).png').convert_alpha()
            img = pygame.transform.scale(img, (280, 192))  
            self.run_imgs.append(img)
        
        self.rect = self.run_imgs[0].get_rect(center=pos)
        self.collid_rect = pygame.Rect(self.rect.x, self.rect.y, 60, 150)
        
        self.id = 0

        self.dead = False
        self.count = 0
        
        v0 = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
        m = math.sqrt(v0[0]**2 + v0[1]**2)
        self.velocity = [3.0 * v0[0] / m, 3.0 * v0[1] / m]
        
        if self.velocity[0] < 0:
            self.flipX()
            
        self.time_change_pos = 0
        self.gifts_ids = []
        
    def draw(self, screen):
        global gifts
        
        if self.count >= 10:      
            self.id += 1
            self.count = 0
        if not self.dead and self.id >= 11:
            self.id = 0
        if self.dead and self.id >= 17:
            self.id = 16

        #pygame.draw.rect(screen, (255,0,0), self.collid_rect, width=1, border_radius=2)
        
        if self.dead:
            screen.blit(self.dead_imgs[self.id], self.rect)
        else:
            screen.blit(self.run_imgs[self.id], self.rect)
        
        self.count += 1
        
        if not self.dead:                  
            # movement
            last_pos = [self.rect.centerx, self.rect.centery]
            self.rect.centerx += self.velocity[0]
            self.rect.centery += self.velocity[1]
            
            if self.rect.centerx + 70 >= w or self.rect.centerx - 70 <= 0:
                self.rect.centerx = last_pos[0]
                self.velocity[0] = -self.velocity[0]
                self.flipX()
                
            if self.rect.centery + 48 >= h or self.rect.centery - 48 <= 0:
                self.rect.centery = last_pos[1]
                self.velocity[1] = -self.velocity[1]
            
            if self.time_change_pos >= 100:            
                v0 = [random.uniform(-1.0, 1.0), random.uniform(-1.0, 1.0)]
                m = math.sqrt(v0[0]**2 + v0[1]**2)
                new = [3.0 * v0[0] / m, 3.0 * v0[1] / m]
                if new[0] == 0:
                    new[0] = 1.0
                    
                if new[0] / abs(new[0]) != self.velocity[0] / abs(self.velocity[0]):
                    self.velocity = new
                    self.flipX()
                self.time_change_pos = 0
            self.time_change_pos += 1
            self.collid_rect.centerx = self.rect.centerx
            self.collid_rect.centery = self.rect.centery
            # ---
           
            
    def flipX(self):
        if not self.dead:
            for i in range(len(self.run_imgs)):
                self.run_imgs[i] = pygame.transform.flip(self.run_imgs[i], True, False)
        else:
            for i in range(len(self.dead_imgs)):
                self.dead_imgs[i] = pygame.transform.flip(self.dead_imgs[i], True, False)
    def flipY(self):
        if not self.dead:
            for i in range(len(self.run_imgs)):
                self.run_imgs[i] = pygame.transform.flip(self.run_imgs[i], False, True)
        else:
            for i in range(len(self.dead_imgs)):
                self.dead_imgs[i] = pygame.transform.flip(self.dead_imgs[i], False, True)
            

santa = []

for i in range(0, 40):
    santa.append(Santa((random.randint(280, w - 280), random.randint(192, h - 192)), 1))

ball_rect = pygame.Rect(random.randint(60, w - 60), random.randint(60, h - 60), 20, 20)
ball_velocity = [4.0,4.0]

def Update(screen):
    global delta_time
    global dt
    global t
    global h,w
    global santa, gifts
       
    for i in range(len(santa)):
        santa[i].draw(screen)
        if santa[i].collid_rect.colliderect(ball_rect) and not santa[i].dead:
            santa[i].dead = True
            santa[i].id = 0
            if santa[i].velocity[0] / abs(santa[i].velocity[0]) < 0:
                santa[i].flipX()
            beep.play()
            
    pygame.draw.circle(screen, (100, 250, 100), [ball_rect.centerx, ball_rect.centery], 20)
    
    last_pos = [ball_rect.centerx, ball_rect.centery]
    ball_rect.centerx += ball_velocity[0]
    ball_rect.centery += ball_velocity[1]
    
    if ball_rect.centerx  + 50 >= w  or ball_rect.centerx - 50 <= 0:
        ball_rect.centerx = last_pos[0]
        ball_velocity[0] = -ball_velocity[0]
    if ball_rect.centery  + 50 >= h  or ball_rect.centery - 50 <= 0:
        ball_rect.centery = last_pos[1]
        ball_velocity[1] = -ball_velocity[1]
    
    delta_time = clock.tick(60) / 1000
    pygame.display.flip()
    t += 1
    
    
isEnd = False
while not isEnd:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isEnd = True
            
    screen.fill((0,0,0))       
    Update(screen)
    
pygame.quit()
sys.exit()
