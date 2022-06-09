import pygame
import sys
import math
from button import Button
pygame.init()

WINDOW_SIZE = (900, 550)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Whack The Minions")

# colors
LIGHT_BLUE = "#bae6ff"
WHITE = (255, 255, 255)
LIGHT_YELLOW = "#fcffaf"

# images
menu_bg = pygame.transform.scale(pygame.image.load("Images/menu_bg.png"), WINDOW_SIZE)
menu_title = pygame.image.load("Images/menu_title.png")

empty_hole = pygame.transform.scale(pygame.image.load("Images/empty_hole.png"), (210, 224))
minion_hole = pygame.transform.scale(pygame.image.load("Images/minion_hole.png"), (210, 224))

hammer_img = pygame.transform.scale(pygame.image.load("Images/hammer.png"), (120, 186))


class Hole:
    def __init__(self, surface, x, y, minion_in):
        self.surface = surface
        self.x = x
        self.y = y
        self.minion_in = minion_in

    def draw(self):
        if self.minion_in:
            self.surface.blit(minion_hole, (self.x, self.y))
        else:
            self.surface.blit(empty_hole, (self.x, self.y))


class Hammer:
    def __init__(self, surface, x, y, velocity):
        self.surface = surface
        self.x = x
        self.y = y
        self.velocity = velocity

    def draw(self):
        mx, my = pygame.mouse.get_pos()
        hammer_pos = (self.x, self.y)
        hammer_rect = hammer_img.get_rect(center=hammer_pos)

        dx, dy = mx - hammer_rect.centerx, my - hammer_rect.centery
        angle = math.degrees(math.atan2(-dy, dx)) - 90

        rot_image = pygame.transform.rotate(hammer_img, angle)
        rot_image_rect = rot_image.get_rect(center=hammer_rect.center)
        window.blit(rot_image, rot_image_rect.topleft)


def main():
    holes = []
    x = 90
    y = 100
    for i in range(5):
        holes.append(Hole(window, x, y, False))
        x += 250
        if i == 2:
            x = 220
            y += 170

    clock = pygame.time.Clock()
    hammer_x, hammer_y = window.get_rect().center
    hammer = Hammer(window, hammer_x, hammer_y, 5)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu()

            # if event.type == pygame.MOUSEMOTION:
            #     hammer.x, hammer.y = pygame.mouse.get_pos()

        window.fill(LIGHT_YELLOW)
        clock.tick(60)

        for hole in holes:
            hole.draw()

        hammer.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def menu():
    play_button = Button(window, "PLAY", LIGHT_BLUE, WHITE, 280, 280, 300, 120)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    main()

        window.blit(menu_bg, (0, 0))
        window.blit(menu_title, (100, 20))
        play_button.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()