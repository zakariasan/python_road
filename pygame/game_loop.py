import pygame

WIDTH, HEIGHT = 1280, 720


def run():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Fly-in")

    running = True
    while running:
        screen.fill((30, 30, 30))  # background color

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.draw.circle(screen, (200, 200, 255), (400, 300), 10)

        pygame.display.flip()

    pygame.quit()

run()
