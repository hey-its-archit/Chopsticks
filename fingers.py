import pygame

pygame.init()
size = (1000, 2000)
scaling_factor = 8
fingers = []
for _ in range(0,5):
    fingers.append(pygame.image.load('fingers/finger_'+str(_)+'.png'))

for i in range(0, 5):
    fingers[i] = pygame.transform.scale(fingers[i], (int(size[0] / scaling_factor), int(size[1] / scaling_factor)))

