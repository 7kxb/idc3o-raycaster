##########
# Filename: index.py
# Description: A 3D game through using its own raycasting engine
# Author: Kevin X.
# Date: 2022 - 09 - 28
##########

import sys
# imports the sys class
import pygame
# imports the pygame class
from pygame.locals import *
# imports all functions from the pygame.locals class
import os
# imports the os class
from math import radians, sin,cos,tan,atan,pi,hypot
# imports the math class
import random
# imports the random class
pygame.font.init()
pygame.mixer.init()
pygame.init()
# initializes pygame

fps = 120
# sets fps cap to 120
fpsClock = pygame.time.Clock()
# defines variable fpsClock as pygame.time.Clock()
width, height = 1280,720
# sets width and height to 1280 by 720
screen = pygame.display.set_mode((width, height))
# initializes the screen

class player():
# player object
  x, y = float(width-width/16*4+width/20), float(height/20)
  # position of the player
  rotation = 0
  # angle the player is pointing
  if sys.platform == 'linux' or sys.platform == 'linux2':
    image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('raycaster','contents','player.png')).convert_alpha(),(width/4/64,height/3/64)),rotation)
  if sys.platform == 'win32':
    image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load('./contents/player.png').convert_alpha(),(int(width/4/64),int(height/3/64))),int(rotation))
  # player icon on the minimap
  w, h = image.get_size()
  # width and height of the player icon on the minimap
  fov = 90
  # field of view
  res = 16
  # resolution (pixel width per line)
  fog = 32
  # fog
  collected = -3
  # collected
  time = 0
  # time
  def print(win, image, pos, origin, angle):
  # draws the image when called
    image_rect = image.get_rect(topleft = (pos[0] - origin[0], pos[1]-origin[1]))
    offset_center_to_pivot = pygame.math.Vector2(pos) - image_rect.center
    # offset from pivot to center
    rotated_offset = offset_center_to_pivot.rotate(-angle)
    # rotated offset from pivot to center
    rotated_image_center = (pos[0] - rotated_offset.x, pos[1] - rotated_offset.y)
    # rotated image center
    rotated_image = pygame.transform.rotate(image, angle)
    # get a rotated image
    rotated_image_rect = rotated_image.get_rect(center = rotated_image_center)
    # rotate and blit the image
    pygame.draw.rect(screen,(255,0,0),pygame.Rect(player.x-player.w/2,player.y-player.w/2,player.w,player.w))
    win.blit(rotated_image, rotated_image_rect)
    # done
  def try_move(dx,dy):
  # tries moving and checks for wall segments
    player.x += dx
    player.y -= dy
    # move player's x position and y position by dx and dy
    tl = screen.get_at((round(player.x-player.w/2),round(player.y-player.w/2)))
    tr = screen.get_at((round(player.x+player.w/2),round(player.y-player.w/2)))
    bl = screen.get_at((round(player.x-player.w/2),round(player.y+player.w/2)))
    br = screen.get_at((round(player.x+player.w/2),round(player.y+player.w/2)))
    # get the colour of the pixel at each 4 corner of the hitbox
    if tl == (255,255,255) or tr == (255,255,255) or bl == (255,255,255) or br == (255,255,255):
    # if there's a colision, move the player back
      player.x -= dx
      player.y += dy
  def handle_movement(delta):
  # handles player movement
    keys_pressed = pygame.key.get_pressed()
    # handles controls
    vel = level.s/1280 * delta
    if keys_pressed[pygame.K_LSHIFT]:
      vel = level.s/640 * delta
    # velocity
    dx = vel*cos(player.rotation*pi/180)
    # sin and cos functions require the argument angle
    dy = vel*sin(player.rotation*pi/180)
    # to be in radians (360 degrees = 2*pi radians)
    toggle = 1
    # fixes directional controls for player movement
    if keys_pressed[pygame.K_s]:
    # if s is pressed go backwards
      player.try_move(dx*-1,0*-1)
      player.try_move(0*-1,dy*-1)
    if keys_pressed[pygame.K_w]:
    # if w is pressed go forwards
      player.try_move(dx,0)
      player.try_move(0,dy)
    if keys_pressed[pygame.K_d]:
    # turn right
      player.rotation -= vel * toggle * 4
    if keys_pressed[pygame.K_a]:
    # turn left
      player.rotation += vel * toggle * 4
    if keys_pressed[pygame.K_o] and player.res > 1:
      player.res -= 0.5
    if keys_pressed[pygame.K_p] and player.res < (width-width/16*4)/10:
      player.res += 0.5
    if keys_pressed[pygame.K_l] and player.fov > 10:
      player.fov -= 5
    if keys_pressed[pygame.K_SEMICOLON] and player.fov < 350:
      player.fov += 5
    
class level():
# level object
  if sys.platform == 'linux' or sys.platform == 'linux2':
    image = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('raycaster','contents','level.png')).convert_alpha(),(width/4/64,height/3/64)),0)
  if sys.platform == 'win32':
    image = pygame.transform.scale(pygame.image.load('./contents/level.png').convert_alpha(),(int(width/4/64),int(height/3/64)))
  # image of the level
  s = image.get_size()[0]
  # size of the image
  def print():
  # draws the image when called
    screen.blit(level.image,(width-width/16*4,0))

class raycaster():
# raycaster object
  rays = []
  # vector
  cameraDir = radians(player.rotation)
  dv = (width-width/16*4)/tan(radians(player.fov)/2)
  temp3 = False
  def raycast():
  # will raycast when called
    x = 0
    # width
    angle = player.rotation + player.fov/2
    # raycast angle
    scanLines = (width-width/16*4)/player.res
    # amount of lines being scanned
    raycaster.cameraDir = radians(player.rotation)
    # original heading of the player
    raycaster.temp3 = True
    for i in range(round(scanLines)):
    # for each scanline
      vel = level.s/160
      # set velocity to an eightyth of the total size of the minimap
      dx = vel*cos(angle*pi/180)
      dy = vel*sin(angle*pi/180)
      # value to change x and y by
      ray = [pygame.Rect(player.x,player.y,1,1),player.x,player.y]
      # ray object
      raycaster.rays.append(ray)
      # appending ray to vector
      for ray in raycaster.rays:
      # for each ray in vector
        temp1a = False
        temp1b = False
        temp1c = False
        while screen.get_at(((ray[0].x),(ray[0].y))) != (255,255,255):
        # until the ray does collide with a white pixel
          pygame.draw.rect(screen,(0,127,255),ray[0])
          # draw the ray on the minimap
          ray[1] += dx
          ray[2] -= dy
          # move ray's x and y by dx and dy
          ray[0].x = ray[1]
          ray[0].y = ray[2]
          if screen.get_at(((ray[0].x),(ray[0].y))) == (10,255,10) and not temp1a:
            temp1a = True
            while screen.get_at(((ray[0].x),(ray[0].y))) == (10,255,10):
              ray[1] -= dx/2
              ray[2] += dy/2
              ray[0].x = ray[1]
              ray[0].y = ray[2]
            temp2a = [ray,angle,x]
            entities.print1(temp2a[0],temp2a[1],temp2a[2])
          if screen.get_at(((ray[0].x),(ray[0].y))) == (20,255,20) and not temp1b:
            temp1b = True
            while screen.get_at(((ray[0].x),(ray[0].y))) == (20,255,20):
              ray[1] -= dx/2
              ray[2] += dy/2
              ray[0].x = ray[1]
              ray[0].y = ray[2]
            temp2b = [ray,angle,x]
            entities.print2(temp2b[0],temp2b[1],temp2b[2])
          if screen.get_at(((ray[0].x),(ray[0].y))) == (30,255,30) and not temp1c:
            temp1c = True
            while screen.get_at(((ray[0].x),(ray[0].y))) == (30,255,30):
              ray[1] -= dx/2
              ray[2] += dy/2
              ray[0].x = ray[1]
              ray[0].y = ray[2]
            temp2c = [ray,angle,x]
            entities.print3(temp2c[0],temp2c[1],temp2c[2])
        while screen.get_at(((ray[0].x),(ray[0].y))) == (255,255,255):
        # until the ray does not collide with a white pixel
          ray[1] -= dx/2
          ray[2] += dy/2
          # move the ray back out of the wall segment to get abs pos
          ray[0].x = ray[1]
          ray[0].y = ray[2]
        pygame.draw.rect(screen,(0,127,255),ray[0])
        # draw the ray on the minimap
        dist1 = hypot(abs(player.x-ray[1]), abs(player.y-ray[2]))
        dist2 = dist1 * cos(radians(angle)-raycaster.cameraDir)
        dist = (dist1+dist2)/2
        # distance between player and wall segment, also remove fisheye lens effect
        if dist != 0:
          h = 10*raycaster.dv/dist
        else:
          h = 10*raycaster.dv/1
        # height of wall segment
        r = pygame.Rect(x,height/2-h/2,player.res,h)
        # wall segment
        sv = max(1,dist/(level.s/player.fog))
        # saturation value of wall segment
        pygame.draw.rect(screen,(0,int(127/sv),int(255/sv)),r)
        # draw a line from the scan
        if temp1a:
          entities.print1(temp2a[0],temp2a[1],temp2a[2])
        if temp1b:
          entities.print2(temp2b[0],temp2b[1],temp2b[2])
        if temp1c:
          entities.print3(temp2c[0],temp2c[1],temp2c[2])
        raycaster.rays.remove(ray)
        # remove the ray from vector
      angle -= player.fov/scanLines
      x += player.res
      # move the scanner to next line

class entities():
  x1 = player.x
  y1 = player.y
  x2 = player.x
  y2 = player.y
  x3 = player.x
  y3 = player.y
  def summon():
    a1 = pygame.Rect(entities.x1,entities.y1,4,4)
    a2 = pygame.Rect(entities.x2,entities.y2,4,4)
    a3 = pygame.Rect(entities.x3,entities.y3,4,4)
    pygame.draw.rect(screen,(10,255,10),a1)
    pygame.draw.rect(screen,(20,255,20),a2)
    pygame.draw.rect(screen,(30,255,30),a3)
  def print1(ray,angle,x):
    dist1 = hypot(abs(player.x-ray[1]), abs(player.y-ray[2]))
    dist2 = dist1 * cos(radians(angle)-raycaster.cameraDir)
    dist = (dist1+dist2)/2
    # distance between player and wall segment, also remove fisheye lens effect
    if dist >= 4:
      h = 10*raycaster.dv/dist
    else:
      h = 10*raycaster.dv/1
      entities.x1 = random.randint(int(max(width-width/16*4,player.x-width/16)),int(min(width-1,player.x+width/16)))
      entities.y1 = random.randint(int(max(1,player.y-height/9)),int(min(height/9*4,player.y+height/9)))
      while screen.get_at((entities.x1,entities.y1)) == (255,255,255):
        entities.x1 = random.randint(width-width/16*4,width-1)
        entities.y1 = random.randint(1,height/9*4)
      if raycaster.temp3:
        player.collected += 1
        raycaster.temp3 = False
        if sys.platform == 'linux' or sys.platform == 'linux2':
          sfx = pygame.mixer.Sound(os.path.join('raycaster','contents','yippee.mp3'))
          sfx.play()
        if sys.platform == 'win32':
          sfx = pygame.mixer.Sound('./contents/yippee.mp3')
          sfx.play()
    # height of wall segment
    r = pygame.Rect(x,height/2-h/2,player.res,h)
    # wall segment
    sv = max(1,dist/(level.s/player.fog))
    # saturation value of wall segment
    pygame.draw.rect(screen,(255,int(127/sv),int(255/sv)),r)
    # draw a line from the scan
  def print2(ray,angle,x):
    dist1 = hypot(abs(player.x-ray[1]), abs(player.y-ray[2]))
    dist2 = dist1 * cos(radians(angle)-raycaster.cameraDir)
    dist = (dist1+dist2)/2
    # distance between player and wall segment, also remove fisheye lens effect
    if dist >= 4:
      h = 10*raycaster.dv/dist
    else:
      h = 10*raycaster.dv/1
      entities.x2 = random.randint(int(max(width-width/16*4,player.x-width/16)),int(min(width-1,player.x+width/16)))
      entities.y2 = random.randint(int(max(1,player.y-height/9)),int(min(height/9*4,player.y+height/9)))
      while screen.get_at((entities.x2,entities.y2)) == (255,255,255):
        entities.x2 = random.randint(width-width/16*4,width-1)
        entities.y2 = random.randint(1,height/9*4)
      if raycaster.temp3:
        player.collected += 1
        raycaster.temp3 = False
        if sys.platform == 'linux' or sys.platform == 'linux2':
          sfx = pygame.mixer.Sound(os.path.join('raycaster','contents','yippee.mp3'))
          sfx.play()
        if sys.platform == 'win32':
          sfx = pygame.mixer.Sound('./contents/yippee.mp3')
          sfx.play()
    # height of wall segment
    r = pygame.Rect(x,height/2-h/2,player.res,h)
    # wall segment
    sv = max(1,dist/(level.s/player.fog))
    # saturation value of wall segment
    pygame.draw.rect(screen,(255,int(127/sv),int(255/sv)),r)
    # draw a line from the scan
  def print3(ray,angle,x):
    dist1 = hypot(abs(player.x-ray[1]), abs(player.y-ray[2]))
    dist2 = dist1 * cos(radians(angle)-raycaster.cameraDir)
    dist = (dist1+dist2)/2
    # distance between player and wall segment, also remove fisheye lens effect
    if dist >= 4:
      h = 10*raycaster.dv/dist
    else:
      h = 10*raycaster.dv/1
      entities.x3 = random.randint(int(max(width-width/16*4,player.x-width/16)),int(min(width-1,player.x+width/16)))
      entities.y3 = random.randint(int(max(1,player.y-height/9)),int(min(height/9*4,player.y+height/9)))
      while screen.get_at((entities.x3,entities.y3)) == (255,255,255):
        entities.x3 = random.randint(width-width/16*4,width-1)
        entities.y3 = random.randint(1,height/9*4)
      if raycaster.temp3:
        player.collected += 1
        raycaster.temp3 = False
        if sys.platform == 'linux' or sys.platform == 'linux2':
          sfx = pygame.mixer.Sound(os.path.join('raycaster','contents','yippee.mp3'))
          sfx.play()
        if sys.platform == 'win32':
          sfx = pygame.mixer.Sound('./contents/yippee.mp3')
          sfx.play()
    # height of wall segment
    r = pygame.Rect(x,height/2-h/2,player.res,h)
    # wall segment
    sv = max(1,dist/(level.s/player.fog))
    # saturation value of wall segment
    pygame.draw.rect(screen,(255,int(127/sv),int(255/sv)),r)
    # draw a line from the scan
    
if sys.platform == 'linux' or sys.platform == 'linux2':
  music = pygame.mixer.Sound(os.path.join('raycaster','contents','bosa-nova.mp3'))
  music.play(-1)
if sys.platform == 'win32':
  music = pygame.mixer.Sound('./contents/bosa-nova.mp3')
  music.play(-1)
# play music
temp4 = True
while True:
# main game loop
  screen.fill((0, 0, 0))
  # fill the screen with black
  for event in pygame.event.get():
  # handles events
    if event.type == QUIT:
    # if user quits the game
      pygame.quit()
      # quit the game
      sys.exit()
      # exit the program
  if sys.platform == 'linux' or sys.platform == 'linux2':
    bg = pygame.transform.scale(pygame.image.load(os.path.join('raycaster','contents','background.png')).convert(),((width-width/16*4),(height)))
  if sys.platform == 'win32':
    bg = pygame.transform.scale(pygame.image.load('./contents/background.png').convert(),(int(width-width/16*4),int(height)))
  screen.blit(bg,(0,0))
  # background
  pygame.draw.rect(screen,(127,127,127),pygame.Rect(width-width/16*4,height/9*4,width/16*4,height-height/9*4))
  # ui
  level.print()
  # draws the level image
  fps2 = fpsClock.get_fps()
  delta = fps/max(fps2,1)
  player.handle_movement(delta)
  # handles player movement
  player.print(screen,player.image,(player.x,player.y),(player.w/2,player.h/2),player.rotation)
  # draws the player image
  entities.summon()
  # summon entities
  raycaster.raycast()
  # raycast
  player.time += 1 * delta
  if player.time/120 > 30 and temp4:
    if sys.platform == 'linux' or sys.platform == 'linux2':
      sfx2 = pygame.mixer.Sound(os.path.join('raycaster','contents','gordon.mp3'))
      sfx2.play()
    if sys.platform == 'win32':
      sfx2 = pygame.mixer.Sound('./raycaster/contents/gordon.mp3')
      sfx2.play()
    temp4 = False
  FONT = pygame.font.SysFont('comicsans',width//32)
  FONT3 = pygame.font.SysFont('comicsans',width//64)
  fps_text = FONT.render('fps: '+str(round(fps2,1)),1,(0,0,0))
  collected_text = FONT.render('collected: '+str(round(player.collected,1)),1,(0,0,0))
  time_text = FONT.render('time: '+str(round(player.time/120,1))+' / 120.0',1,(0,0,0))
  info_text1 = FONT3.render('wasd to move',1,(0,0,0))
  info_text2 = FONT3.render('lshift to run',1,(0,0,0))
  info_text3 = FONT3.render('o/p to change resolution',1,(0,0,0))
  info_text4 = FONT3.render('l/; to change fov',1,(0,0,0))
  screen.blit(fps_text,(width-width/16*4+width//32,height//2))
  screen.blit(collected_text,(width-width/16*4+width//32,height//2+height//32))
  screen.blit(time_text,(width-width/16*4+width//32,height//2+height//16))
  screen.blit(info_text1,(width-width/16*4+width//32,height//2+height//6))
  screen.blit(info_text2,(width-width/16*4+width//32,height//2+height//5))
  screen.blit(info_text3,(width-width/16*4+width//32,height//2+height//4.5))
  screen.blit(info_text4,(width-width/16*4+width//32,height//2+height//4))
  # counter
  if player.time/120 < 20:
    image0 = pygame.transform.scale(pygame.image.load(os.path.join('raycaster','contents','intro.png')).convert_alpha(),(width-width/16*4,height))
    intro_text1 = FONT.render('After an intense battle protecting their portals from the ball...',1,(255,255,255))
    intro_text2 = FONT.render('One ship ended up defeated...',1,(255,255,255))
    intro_text3 = FONT.render('However, they have been zapped into the 3rd dimension!',1,(255,255,255))
    intro_text4 = FONT.render('You must help go around the maze collecting materials...',1,(255,255,255))
    screen.blit(image0,(0,0))
    screen.blit(intro_text1,(width/16,height/5))
    screen.blit(intro_text2,(width/16,height/4))
    screen.blit(intro_text3,(width/16,height/3))
    screen.blit(intro_text4,(width/16,height/2))
  if player.time/120 > 120:
    FONT2 = pygame.font.SysFont('comicsans',width//8)
    over_text = FONT2.render('TIMES UP!',1,(255,255,255))
    screen.blit(over_text,(width//4,height//4))
    pygame.time.delay(1000)
  # check
  pygame.display.update()
  # update the display
  fpsClock.tick(fps)
  # aligns the clock so that all the methods above
  # are syncronised to be completed in 1 tick
  # (1 tick = 1/fps seconds)