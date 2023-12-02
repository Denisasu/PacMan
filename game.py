#!/usr/bin/env python
# -*- coding: utf-8 -*-
#скрипт должен быть запущен с помощью Python. 
#объявление кодировки utf-8

import pygame
from player import Player
from enemies import *
import tkinter
from tkinter import messagebox
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

#Определим некоторые цвета
BLACK = (0,0,0)
WHITE = (255,255,255)
BLUE = (0,0,255)
RED = (255,0,0)


class Game(object):
    def __init__(self): # Инициализация игры
        self.font = pygame.font.Font(None,40) #шрифт для текста
        self.about = False
        self.game_over = True
        self.game_over_image = pygame.image.load("game_over.png").convert()
         # Масштабирование изображения
        self.game_over_image = pygame.transform.scale(self.game_over_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.win_image = pygame.image.load("win.jpg").convert()
        self.win_image = pygame.transform.scale(self.win_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

        
        self.score = 0 #счёт игры
        self.font = pygame.font.Font(None,35) #шрифт для счёта игры
        self.menu = Menu(("Start","About","Exit"),font_color = WHITE,font_size=60) #создание меню
        self.player = Player(32,128,"player.png") #создание игрока
        #стены
        self.horizontal_blocks = pygame.sprite.Group()
        self.vertical_blocks = pygame.sprite.Group()
        #точки
        self.dots_group = pygame.sprite.Group()
       #Размещение стен
        for i,row in enumerate(enviroment()):
            for j,item in enumerate(row):
                if item == 1:
                    self.horizontal_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
                elif item == 2:
                    self.vertical_blocks.add(Block(j*32+8,i*32+8,BLACK,16,16))
        #создание врагов
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Slime(288,96,0,2))
        self.enemies.add(Slime(288,320,0,-2))
        self.enemies.add(Ghost(544,128,0,2))
        self.enemies.add(Ghost(32,224,0,2))
        self.enemies.add(Specter(160,64,2,0))
        self.enemies.add(Specter(448,64,-2,0))
        self.enemies.add(Phantom(640,448,2,0))
        self.enemies.add(Phantom(448,320,2,0))
        
        #добавление точек
        for i, row in enumerate(enviroment()):
            for j, item in enumerate(row):
                if item != 0:
                    self.dots_group.add(Ellipse(j*32+12,i*32+12,WHITE,8,8))

        #звуковые эффекты
        self.pacman_sound = pygame.mixer.Sound("pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("game_over_sound.ogg")
        
 #перезапуск игры
    def restart(self): 
        self.__init__()
 #обработка событий
    def process_events(self):
        #перезапуск игры, если нажата клавиша R
        for event in pygame.event.get(): 
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_r:
                    self.restart()
            self.menu.event_handler(event)

            #обработка событий в меню
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            #начать игру
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            #открыть about
                            self.about = True
                        elif self.menu.state == 2:
                            #закрыть игру
                            return True
                #управление
                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()
                
                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False
            #управление игроком
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    self.player.stop_move_right()
                elif event.key == pygame.K_LEFT:
                    self.player.stop_move_left()
                elif event.key == pygame.K_UP:
                    self.player.stop_move_up()
                elif event.key == pygame.K_DOWN:
                    self.player.stop_move_down()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.player.explosion = True
                    
        return False

   #логика игры
    def run_logic(self):
        if not self.game_over:
            #обновляем положение игрока на основе стен
            self.player.update(self.horizontal_blocks,self.vertical_blocks)
            #проверяем столкновение игрока с точками
            block_hit_list = pygame.sprite.spritecollide(self.player,self.dots_group,True) 
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += 1 #увеличиваем счетчик очков
            enemy_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            # Если произошло столкновение
            if len(enemy_hit_list) > 0:
                self.player.explosion = True
                self.player.lives -= 1  # Уменьшаем количество жизней игрока при столкновении с врагом
                if self.player.lives > 0:
                    # Если остались жизни, перемещаем игрока в начальную позицию
                    self.player.rect.topleft = (32, 128)
                    self.player.explosion = False
                else:
                    self.game_over = True  # Если жизни закончились, завершаем игру
                    #воспроизведение звука Game Over при окончании жизней
                    pygame.mixer.music.load("game_over_sound.ogg")
                    pygame.mixer.music.play()
            #обновляем положение противников на основе стен
            self.enemies.update(self.horizontal_blocks, self.vertical_blocks)

    def display_frame(self,screen):
        screen.fill(BLACK)
        if self.game_over:
            if self.about:
                self.display_message(screen,
                                     "Задача игрока — управляя Пакманом, съесть все точки\n"
                                              "в лабиринте, избегая встречи с привидениями, \n"
                                                 "которые гоняются за героем.\n"
                                              "Если привидение дотронется до Пакмана, \n"
                                              "то его жизнь теряется, призраки и Пакман возвращаются\n"
                                     "на исходную позицию,\n"
                                     "но при этом прогресс собранных точек сохраняется.\n"
                                     "Если при столкновении с призраком ,\n"
                                     "у Пакмана не осталось дополнительных жизней,\n"
                                     "то игра заканчивается.После съедения всех точек\n"
                                     "начинается новый уровень в том же лабиринте.")
                                
            else:
                self.menu.display_frame(screen)
        else:
            #дизайн игры
            self.horizontal_blocks.draw(screen)
            self.vertical_blocks.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image,self.player.rect)
            #text=self.font.render("Score: "+(str)(self.score), 1,self.RED)
            #screen.blit(text, (30, 650))
            #отображение текущего количества жизней игрока
            lives_text = self.font.render("Lives: " + str(self.player.lives), True, WHITE)
            screen.blit(lives_text, (10, 10))  #размещаем текст о жизнях в левом верхнем углу экрана
            #текст для очков
            score_text = self.font.render("Score: " + str(self.score), True, WHITE)
            screen.blit(score_text, (10, 30))
            if len(self.dots_group) == 0:
                screen.blit(self.win_image, (0, 0))
                self.display_text(screen, "Press R to restart the game", (255, 0, 0), 35)
                self.game_over = False
            #размещаем текст о счете на уровне с текстом о жизнях
             #если игра окончена и закончились жизни, показываем изображение Game Over
        if self.game_over and self.player.lives <= 0:
            screen.blit(self.game_over_image, (0, 0))
            self.display_text(screen, "Press R to restart the game!", (0, 255, 0), 35)
            #отображение текущего счета поверх экрана "Game Over"
            score_text = self.font.render(f"Score: {self.score}", True, WHITE)
            score_rect = score_text.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 41))
            screen.blit(score_text, score_rect)
        
        pygame.display.flip()
    def display_text(self, screen, text, color, font_size):
        
        font = pygame.font.Font(None, font_size)
        label = font.render(text, True, (255, 255, 255))
        text_rect = label.get_rect(midbottom=(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 20))
        screen.blit(label, text_rect)

    def display_message(self, screen, message, color=(255, 0, 0)):
        lines = message.split('\n')
        font_size = 20 #уменьшаем размер шрифта
        pygame.font.init()  #инициализация шрифтов в Pygame
        font = pygame.font.SysFont(pygame.font.get_default_font(), font_size)
        text_height = len(lines) * (font_size + 5)
        
        posY = (SCREEN_HEIGHT - text_height) / 2  #вычисление начальной позиции по высоте
        for line in lines:
            label = self.font.render(line, True, color)
            width = label.get_width()
            posX = (SCREEN_WIDTH - width) / 2  #вычисление позиции по горизонтали
            screen.blit(label, (posX, posY))
            posY += font_size + 5  #изменение позиции по высоте для следующей строки




class Menu(object):
    state = 0
    def __init__(self,items,font_color=(0,0,0),select_color=(255,0,0),ttf_font=None,font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font,font_size)
        self.background_image = pygame.image.load("menu.jpg").convert()

    def display_frame(self,screen):
        screen.blit(self.background_image, (0, 0))
        text_height = self.font.get_height()  #получаем высоту текста
        vertical_offset = 50  #новое расстояние между пунктами меню
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item,True,self.select_color)
            else:
                label = self.font.render(item,True,self.font_color)
            
            width = label.get_width()
            height = label.get_height()
            
            posX = (SCREEN_WIDTH /2) - (width /2)
            #общая высота текстового блока
            t_h = len(self.items) * height
            posY = (SCREEN_HEIGHT /2) - (t_h /2) + (index * height) + vertical_offset
            
            screen.blit(label,(posX,posY))
    #обработка событий    
    def event_handler(self,event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) -1:
                    self.state += 1


pygame.quit()

