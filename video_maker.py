import pygame
import os

adress = "C://USERS/USER/desktop/01-01/"  # адрес папки, в которой хранятся фото

photo_list = os.listdir(adress)  # список, где находятся все файлы
print(photo_list)

pygame.init()
sc = pygame.display.set_mode((640, 480)) # размеры окна вывода

clock = pygame.time.Clock()
FPS = 2 #тут находится FPS
j = 0
z = 0

play = True
while play == True:  # основной цикл программы
    if z%2 == 1:
        new_ad = adress + photo_list[j]
        img_surf = pygame.image.load(new_ad)
        img_rect = img_surf.get_rect()
        sc.blit(img_surf, img_rect)
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