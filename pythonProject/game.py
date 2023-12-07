import pygame
from pygame import mixer
import math
import random

#pygame setup
pygame.init()
screen = pygame.display.set_mode((400,600))
clock = pygame.time.Clock()
running = True
dt = 0
speed = 30

bGimage = pygame.image.load("assets1/background.png").convert()
background_image = pygame.transform.scale(bGimage, (screen.get_width()*2,screen.get_height()*2))
bgimage2 = pygame.image.load("assets1/background.png").convert()
background_image2 = pygame.transform.scale(bgimage2, (screen.get_width()*2,screen.get_height()*2))

scroll = 0
tiles = math.ceil(600/bGimage.get_height()) +1
i = 0
h = 400
w = 600
bgx = 0
bgy = 0
alpha = 0

#top surface fix
background_y = 0
white_area_height = 50
top_surface = pygame.Surface((screen.get_width(),white_area_height))
top_surface.fill((255,255,255))
screen.blit(top_surface , (0,0))
screen.blit(background_image, (0,background_y))

#more pygame setup
car_pos = pygame.Vector2(screen.get_width()/2 , screen.get_height()/2)
previous_car_pos = car_pos.copy()

mixer.init()
mixer.music.load('assets1/stylish-rock-beat-trailer-116346.mp3')
mixer.music.set_volume(0.2)
mixer.music.play()

hit_sound = mixer.Sound('assets1/crash.mp3')
hit_sound.set_volume(0.4)


class Car(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.image.load("assets1/car.png")
        self.rect = self.image.get_rect()

        self.x = 159
        self.y = 350
    #update cars position
    def update(self):
        self.x +=0
        self.y +=0
    # draw car to screen
    def draw(self, screen):
        screen.blit(self.image , (self.x,self.y))


#sprite group
sprites = pygame.sprite.Group()
#car object
car = Car()
#add car to sprite group
sprites.add(car)
sprites.draw(screen)

#create ground and sides
ground_rect = pygame.Rect(-10 ,0, 10, screen.get_height())
crash = False
update = False
totTime = 0
#while loop
while running:
    if totTime>2:
        totTime-=2
        update = True
    #scrolling background
    screen.blit(bGimage,(0, bgy))
    if bgy < 0:
        screen.blit(bGimage,(0,bgy+400))
        pygame.display.flip()
    if bgy < screen.get_height():
        screen.blit(bGimage, (0,bgy - 400))
    if bgy >= bGimage.get_height():
        alpha += .01
        background_image.set_alpha(alpha)
        screen.blit(background_image, (0,bgy))
        pygame.display.flip()
        if alpha >= 1:
            bgy = 0
            alpha = 0

    if bgy >= bGimage.get_height():
        bgy = 0


    #crash loops
    if car.rect.colliderect(ground_rect):
        car.vy = (159,350)
        car.update()
        if not crash:
            hit_sound.play()
            crash = True
    else:
        car.update()
        crash = False


    #poll for events
    #pygame.QUIT event when the user clicks x to close the window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        car.y -= 300 *dt *.01
        bgy+= 400*dt
        if bgy < screen.get_height():
            bgy+=2
    if keys[pygame.K_s]:
        car.y+= 300 *dt *.01
        bgy-=400*dt
        if bgy < screen.get_height():
            bgy -=2
    if keys[pygame.K_d]:
        if car.x < screen.get_width()-car.image.get_width():
            car.x += 300 * dt
    if keys[pygame.K_a]:
        if car.x > 0:
            car.x -= 300 * dt
    car.draw(screen)


    #flip() the display to put it on your screen
    pygame.display.flip()


   #limit fps to 60
    dt = clock.tick(60)/1000

pygame.quit()


