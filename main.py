import pygame
from game import Game

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 576

def main():
    #инициализировать все импортированные модули pygame
    pygame.init()
    #создание иконки
    icon_image = pygame.image.load("icon.png")
    pygame.display.set_icon(icon_image)
    #установка ширины и высоты экрана
    screen = pygame.display.set_mode((SCREEN_WIDTH,SCREEN_HEIGHT))
    #заголовок текущего окна
    pygame.display.set_caption("PACMAN")
    done = False
    #управление скоростью обновления экрана
    clock = pygame.time.Clock()
    #создание игрового объекта
    game = Game()
    restart = False
    #основной цикл программы
    while not done:
        if restart:  #перезапуск игры
            game = Game()
            restart = False
        #cобытия процесса
        done = game.process_events()
        #логика игры
        game.run_logic()
        #текущий кадр
        game.display_frame(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                pass
        #задаем 30 FPS 
        clock.tick(30)
        
    pygame.quit()

if __name__ == '__main__':
    main()
