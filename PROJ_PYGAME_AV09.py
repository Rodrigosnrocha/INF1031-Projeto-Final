#Programa feito por:

# Antonio Brych(Matrícula 2211884) 

#Rodrigo Rocha (Matrícula 2210814)

#Para a disciplina INF1031.

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

pygame.display.set_caption('Grand Theft Coins')

width = 850
height = 567

white = (255, 255, 255)
green = (0, 255, 0)
blue = (0, 0, 128)

pressed = False

posList = []
speed = []
count = 0

pygame.init()

display = pygame.display.set_mode((width,height))

def distanceBetween(coord1,coord2):
    return sqrt((coord2[0]-coord1[0])**2 + (coord2[1]-coord1[1])**2)
def generateSpeed(val1,val2):
    return [uniform(val1,val2),uniform(val1,val2)]
    
font = pygame.font.Font('freesansbold.ttf', 32)

img = pygame.image.load('coin_asset.png')
img = pygame.transform.scale(img, (90, 90))
bg = pygame.image.load('bg_asset.jpeg')
clock = pygame.time.Clock()



while True:
    clock.tick(60)
    dt = clock.get_time()
    mouse_coord = pygame.mouse.get_pos()
    time = pygame.time.get_ticks()
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()    
    
    if len(posList) == 0:
        display.blit(img,(100,100))
        posList.append(100)
        posList.append(100)
        speed = generateSpeed(-1,1)

    posList[0] += speed[0]/1.45 * dt
    posList[1] += speed[1]/1.45 * dt

    if posList[0]+90 >= display.get_width():
        speed[0] = speed[0] * -1
        posList[0] = display.get_width()-90
    elif posList[0] <= 0:
        speed[0] = speed[0] * -1
        posList[0] = 0
    if posList[1]+90 >= display.get_height():
        speed[1] = speed[1] * -1
        posList[1] = display.get_height()-90
    elif posList[1] <= 0:
        speed[1] = speed[1] * -1
        posList[1] = 0
    

    if distanceBetween(mouse_coord,(posList[0]+45,posList[1]+45)) <=45 and (not pressed):
        if True in pygame.mouse.get_pressed():
            random_x = randint(40,display.get_width()-90)
            random_y = randint(100,display.get_height()-90)

            posList = [random_x,random_y]
            speed = generateSpeed(-1,1)
            display.blit(bg,(0,0))
            display.blit(img,(posList[0],posList[1]))
            count += 1
            pressed = True
    if not(True in pygame.mouse.get_pressed()):
        pressed = False

    
    display.blit(bg,(0,0))
    text = font.render("Score: "+str(count),True,green,(0,0,0))
    display.blit(text,(0,0))
    display.blit(img,(posList[0],posList[1]))

    pygame.display.update()
    

    

        
        
