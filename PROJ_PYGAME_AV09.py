# Programa feito por:

# Antonio Brych (Matrícula 2211884) 
# Rodrigo Rocha (Matrícula 2210814)

# Para a disciplina INF1031.

"""
   ,___                       ______                      ,___               
  /   /                   /  (  /     /        /) _/_    /   /    o          
 /  __  _   __,  _ _   __/     /     /_  _    //  /     /      __,  _ _   (  
(___/  / (_(_/(_/ / /_(_/_   _/     / /_(/_  //_ (__   (___/  (_)(_/ / /_/_)_
                                            /)                               
                                           (/                                
"""

import pygame

from pygame.locals import *

from math import sqrt

from random import randint, uniform

from sys import exit

pygame.init()
pygame.mixer.init()
pygame.display.set_caption('Grand Theft Coins')

def distanceBetween(coord1,coord2):
    return sqrt((coord2[0]-coord1[0])**2 + (coord2[1]-coord1[1])**2)
def generateSpeed(val1,val2):
    return [uniform(val1,val2),uniform(val1,val2)]
def geraInimigos(w,h):
    random_x = randint(w,display.get_width()-w)
    random_y = randint(h,display.get_height()-h)
    inimigo = {"rect":pygame.Rect(random_x,random_y,w,h),"posList":[random_x,random_y],"speed":generateSpeed(-1,1)}
    return inimigo


width = 850
height = 567

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

try:
    with open("save.txt","r") as save:
        save_values = save.readlines()
        high_score = int(save_values[0])
        fase = int(save_values[1])
except FileNotFoundError:
    high_score = 0
    fase = 0


coin_rect = pygame.Rect(100,100,90,90)
coin_speed = generateSpeed(-1,1)
count = 0


display = pygame.display.set_mode((width,height))


font = pygame.font.Font('freesansbold.ttf', 32)
img = pygame.image.load('coin_asset.png')
img = pygame.transform.scale(img, (90, 90))
coin_pickup = pygame.mixer.Sound('snd_coin.wav')
bg = pygame.image.load('bg_01.jpeg')
clock = pygame.time.Clock()


vidas = 3
player_w = 60
player_h = 60
player_speed = 0.5
player = {"rect":pygame.Rect(50,50,player_w,player_h),"speed":0}

n = 3
enemy_width = 60
enemy_height = 60

inimigos = []
while len(inimigos) < n:
    i = geraInimigos(enemy_width,enemy_height)
    if distanceBetween((i["rect"].x,i["rect"].y),(player["rect"].x,player["rect"].y)) > 100:
        inimigos.append(i)
# Precisa adicionar um check se o inimigo nasce muito perto do player


while True:
    clock.tick(60)
    dt = clock.get_time()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()   
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player["rect"].x += player_speed * dt
    if keys[pygame.K_LEFT]:
        player["rect"].x += -1*player_speed * dt
    if keys[pygame.K_DOWN]:
        player["rect"].y += player_speed * dt
    if keys[pygame.K_UP]:
        player["rect"].y += -1*player_speed * dt
    
    if player["rect"].right >= display.get_width():
        player["rect"].right = display.get_width()
    elif player["rect"].left <= 0:
        player["rect"].left = 0
    if player["rect"].bottom >= display.get_height():
        player["rect"].bottom = display.get_height()
    elif player["rect"].top <= 0:
        player["rect"].top = 0

    coin_rect.x += coin_speed[0]/1.5 * dt
    coin_rect.y += coin_speed[1]/1.5 * dt

    rects_inimigos = []

    # Atualizar posições de inimigos e verificar colisão
    for i in inimigos:
        i["rect"].x += i["speed"][0]/2 * dt
        i["rect"].y += i["speed"][1]/2 * dt
        if i["rect"].right >= display.get_width():
            i["speed"][0] = i["speed"][0] * -1
            i["rect"].right = display.get_width()
        elif i["rect"].left <= 0:
            i["speed"][0] = i["speed"][0] * -1
            i["rect"].left = 0
        if i["rect"].bottom >= display.get_height():
            i["speed"][1] = i["speed"][1] * -1
            i["rect"].bottom = display.get_height()
        elif i["rect"].top <= 0:
            i["speed"][1] = i["speed"][1] * -1
            i["rect"].top = 0
        if pygame.Rect.colliderect(player["rect"],i["rect"]):
            inimigos.remove(i)
            vidas += -1
            while len(inimigos) < n:
                j = geraInimigos(enemy_width,enemy_height)
                if distanceBetween((j["rect"].x,j["rect"].y),(player["rect"].x,player["rect"].y)) > 100:
                    inimigos.append(j)

    if coin_rect.right >= display.get_width():
        coin_speed[0] = coin_speed[0] * -1
        coin_rect.right = display.get_width()
    elif coin_rect.left <= 0:
        coin_speed[0] = coin_speed[0] * -1
        coin_rect.left = 0
    if coin_rect.bottom >= display.get_height():
        coin_speed[1] = coin_speed[1] * -1
        coin_rect.bottom = display.get_height()
    elif coin_rect.top <= 0:
        coin_speed[1] = coin_speed[1] * -1
        coin_rect.top = 0
    
    # Verifica colisão entre Player e Moeda, e aumenta a pontuação se sim
    if pygame.Rect.colliderect(player["rect"],coin_rect):
        coin_pickup.play()
        count += 1
        coin_rect.x = randint(40,display.get_width()-90)
        coin_rect.y = randint(100,display.get_height()-90)
        coin_speed = generateSpeed(-1,1)
    
    if vidas <= 0:
        if count > high_score:
            high_score = count
        with open("save.txt","w") as save:
            save.write(str(high_score)+"\n"+str(fase))
        pygame.quit()
        exit()

    display.blit(bg,(0,0))
    for i in inimigos:
        pygame.draw.rect(display,green,i["rect"])
    display.blit(img,(coin_rect.x,coin_rect.y))
    pygame.draw.rect(display,blue,player["rect"])
    text_score = font.render("Score: "+str(count),True,green,(0,0,0))
    display.blit(text_score,(0,0))
    text_vidas = font.render("Vidas: "+str(vidas),True,green,(0,0,0))
    display.blit(text_vidas,(200,0))

    pygame.display.update()
    

    

        
        
