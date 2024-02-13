import pygame

pygame.init()
screen = pygame.display.set_mode((640, 640))
screen.fill((255, 255, 255))

activate = pygame.image.load('./img/activate.png').convert_alpha()
activate = pygame.transform.scale(activate, (50, 60))


acti = activate.get_rect(center = (150, 150))
print(acti)

while True:
    screen.blit(activate, (100, 100))
    pygame.display.flip()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)