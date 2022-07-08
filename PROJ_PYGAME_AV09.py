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
    
def testLevel(coord):
    x,y = coord[0],coord[1]
    matrix = []
    for i in range(x):
        matrix.append([])
        for j in range(y):
            matrix[i].append(randint(0,9))
    return matrix

def generateQuads(x,y):
    tile_groups = []
    for h in range(3):
        tile_quads = []
        for i in range(x):
            for j in range(y): 
                tile_quads.append((i * tile_size , j * tile_size + h*group_size, tile_size, tile_size))
        tile_groups.append(tile_quads)
    return tile_groups

def loadMap(lines,n):
    levels = []
    for h in range(n):
        with open("level"+str(h+1)+".txt","r") as level1:
            text_matrix = level1.readlines()
            level_matrix = []
            for i in range(lines):
                level_matrix.append([])
                for j in text_matrix[i]:
                    level_matrix[i].append(j)
            levels.append(level_matrix)
    return levels

tile_size = 64
group_size = tile_size * 4
level = 0
screen_tiles = [15,10]
width = tile_size * screen_tiles[0]
height = tile_size * screen_tiles[1]

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)
skull = pygame.image.load('skull.png')

try:
    with open("save.txt","r") as save:
        save_values = save.readlines()
        high_score = int(save_values[0])
except FileNotFoundError:
    high_score = 0

display = pygame.display.set_mode((width,height))
tilesheet = pygame.image.load("tilesheet.png")
tile_pattern = ["0","1","2","3","4","5","6","7","8","9","A","B"]

levels = loadMap(screen_tiles[1],4)
tile_groups = generateQuads(3,4)

coin_rect = pygame.Rect(100,100,90,90)
coin_speed = generateSpeed(-1,1)
count = 0

font = pygame.font.Font('freesansbold.ttf', 32)
img = pygame.image.load('coin_asset.png')
img = pygame.transform.scale(img, (90, 90))
coin_pickup = pygame.mixer.Sound('snd_coin.wav')
hurt = pygame.mixer.Sound('hurt.wav')
bg = pygame.image.load('bg_01.jpeg')
clock = pygame.time.Clock()


vidas = 3
player_w = 128
player_h = 64
player_speed = 0.5
facing_right = False
hand_anim = []
for i in range(8):
    sprite = pygame.image.load('sprites/tile00'+str(i)+'.png')
    hand_anim.append(pygame.transform.scale(sprite, (player_w, player_h)))
player = {"rect":pygame.Rect(50,50,player_w,player_h),"speed":0,"anim":hand_anim,"frame":0}


enemy_width = 62
enemy_height = 74
skull = pygame.transform.scale(skull,(enemy_width+20,enemy_height+40))

inimigos = []
while len(inimigos) < level+1:
    i = geraInimigos(enemy_width,enemy_height)
    if distanceBetween((i["rect"].x,i["rect"].y),(player["rect"].x,player["rect"].y)) > 300:
        inimigos.append(i)

while True:
    clock.tick(60)
    dt = clock.get_time()
    
    
    for event in pygame.event.get():
        if event.type == QUIT:
            if count > high_score:
                high_score = count
            with open("save.txt","w") as save:
                save.write(str(high_score))
            pygame.quit()
            exit()   
    
    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        player["rect"].x += player_speed * dt
        facing_right = True
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        player["rect"].x += -1*player_speed * dt
        facing_right = False
    if keys[pygame.K_DOWN] or keys[pygame.K_s]:
        player["rect"].y += player_speed * dt
    if keys[pygame.K_UP] or keys[pygame.K_w]:
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
            hurt.play()
            #vidas += -1
    while len(inimigos) < level+1:
        j = geraInimigos(enemy_width,enemy_height)
        if distanceBetween((j["rect"].x,j["rect"].y),(player["rect"].x,player["rect"].y)) > 300:
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
        valid = False
        coin_pickup.play()
        count += 1
        while not valid:
            coin_rect.x = randint(40,display.get_width()-90)
            coin_rect.y = randint(100,display.get_height()-90)
            coin_speed = generateSpeed(-1,1)
            if distanceBetween((coin_rect.x,coin_rect.y),(player["rect"].x,player["rect"].y)) > 300:
                valid = True
    if vidas <= 0:
        if count > high_score:
            high_score = count
        with open("save.txt","w") as save:
            save.write(str(high_score))
        pygame.quit()
        exit()
    
    player["frame"] += 0.25
    if player["frame"] >= len(player["anim"]):
            player["frame"] = 0
    
    frame = player["anim"][int(player["frame"])]
    if facing_right:
        frame = pygame.transform.flip(frame,True,False)

    level = count//10
    if level >= 4:
        level = 3

    #display.blit(bg,(0,0))
    for i in range(screen_tiles[1]):
        for j in range(screen_tiles[0]):
            tile_name = levels[level][i][j]
            if tile_name in tile_pattern:
                tile = tile_pattern.index(tile_name)
                display.blit(tilesheet,((j* tile_size),(i* tile_size)),tile_groups[level][tile])


    for i in inimigos:
        display.blit(skull,(i["rect"].x,i["rect"].y))
    display.blit(img,(coin_rect.x,coin_rect.y))
    display.blit(frame,(player["rect"].x,player["rect"].y))
    text_score = font.render("Score: "+str(count),True,green,(0,0,0))
    display.blit(text_score,(0,0))
    text_vidas = font.render("Vidas: "+str(vidas),True,green,(0,0,0))
    display.blit(text_vidas,(200,0))
    text_hs = font.render("High Score: "+str(high_score),True,green,(0,0,0))
    display.blit(text_hs,(600,0))
    pygame.display.update()