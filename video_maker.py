import pygame
import os
import json

adr = "C://USERS/USER/desktop/01-01.json"  #  адрес файла json
with open (adr) as file:
    y = json.load(file)

adress = "C://USERS/USER/desktop/01-01/"  # адрес папки, в которой хранятся фото
photo_list = os.listdir(adress)  # список, где находятся все файлы

pygame.init()
sc = pygame.display.set_mode((640, 520)) # размеры окна вывода

clock = pygame.time.Clock()
FPS = 24 #тут находится FPS
j = 0
z = 0

fon_surf = pygame.image.load("black_fon.png")
fon_rect = fon_surf.get_rect()

text_format = pygame.font.SysFont("Arial", 20) # шрифт и размер текста

play = True
while play == True:  # основной цикл программы
    if z%2 == 1:
        sc.blit(fon_surf, fon_rect) # крч, я еще добавил фон, чтобы текст не накладывался, у меня это черная картинка
        # и я ее закинул в папку с программой для сборки фото в видео
        new_ad = adress + photo_list[j]
        img_surf = pygame.image.load(new_ad)
        img_rect = img_surf.get_rect()
        sc.blit(img_surf, img_rect)
        text = text_format.render(str(y["/FullPackage"][j]['Value']['pulseRate']), 0, (255,0,0))
        sc.blit(text, (310,490))
        j += 1

    clock.tick(FPS)

    pygame.display.update()

    for i in pygame.event.get():
        if i.type == pygame.QUIT:  # код выхода
            play = False
        elif i.type == pygame.KEYDOWN:
            if i.key == pygame.K_SPACE:  # чтобы нажатие на пробел запускает все действие и паузит его
                z += 1

    if j == len(photo_list)-1:
        play = False
