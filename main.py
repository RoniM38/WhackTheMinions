import pygame
import sys
import random
from button import Button
pygame.init()

WINDOW_SIZE = (900, 550)
window = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Whack The Minions")

# colors
LIGHT_BLUE = "#bae6ff"
WHITE = (255, 255, 255)
LIGHT_YELLOW = "#fcffaf"
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# images
menu_bg = pygame.transform.scale(pygame.image.load("Images/menu_bg.png"), WINDOW_SIZE)
menu_title = pygame.image.load("Images/menu_title.png")

empty_hole = pygame.transform.scale(pygame.image.load("Images/empty_hole.png"), (210, 224))
minion_hole = pygame.transform.scale(pygame.image.load("Images/minion_hole.png"), (210, 224))

hammer_img = pygame.transform.scale(pygame.image.load("Images/hammer.png"), (120, 186))

laughing_img1 = pygame.transform.scale(pygame.image.load("Images/minions_laughing1.png"), WINDOW_SIZE)
laughing_img2 = pygame.transform.scale(pygame.image.load("Images/minions_laughing2.png"), WINDOW_SIZE)
cheering_img = pygame.transform.scale(pygame.image.load("Images/minions_cheering.png"), (518, 388))

heart_img = pygame.image.load("Images/heart.png")

# sounds
laugh_sound = pygame.mixer.Sound("Sounds/minions_laughing.wav")
hammer_sound = pygame.mixer.Sound("Sounds/hammer_sound.wav")
menu_music = pygame.mixer.Sound("Sounds/menu_music.wav")
losepoint_sound = pygame.mixer.Sound("Sounds/lose_point.wav")


class Hole:
    def __init__(self, surface, x, y, minion_in):
        self.surface = surface
        self.x = x
        self.y = y
        self.minion_in = minion_in

        w, h = minion_hole.get_size()
        self.rect = pygame.Rect(self.x, self.y, w, h)

    def draw(self):
        if self.minion_in:
            self.surface.blit(minion_hole, (self.x, self.y))
        else:
            self.surface.blit(empty_hole, (self.x, self.y))
        # code for testing the hitboxes
        # pygame.draw.rect(self.surface, RED, self.rect, 3)


class Hammer:
    def __init__(self, surface, x, y):
        self.surface = surface
        self.x = x
        self.y = y

    def draw(self, hammer_hit):
        if hammer_hit:
            hammer_pos = (self.x, self.y)
            hammer_rect = hammer_img.get_rect(center=hammer_pos)

            rot_image = pygame.transform.rotate(hammer_img, 90)
            rot_image_rect = rot_image.get_rect(center=hammer_rect.center)
            self.surface.blit(rot_image, rot_image_rect.topleft)
        else:
            self.surface.blit(hammer_img, pygame.mouse.get_pos())


def choose_hole(holes):
    i = random.randrange(len(holes) - 1)
    holes.append(holes.pop(i))
    return holes[-1]


def victory(score):
    title_font = pygame.font.SysFont("Berlin Sans FB Demi", 100, "bold")
    subtitle_font = pygame.font.SysFont("Arial", 30, "bold")
    subtitle_label = subtitle_font.render("Congrats! You've completed all 5 levels!", True, BLACK)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    menu()

        window.fill(WHITE)
        window.blit(cheering_img, (190, 170))

        window.blit(title_font.render("VICTORY", True, BLACK), (240, 10))
        window.blit(subtitle_label, (180, 110))
        window.blit(subtitle_font.render(f"SCORE:{score};", True, BLACK), (230, 150))
        window.blit(subtitle_font.render("press p to play again", True, BLACK), (420, 147))

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def game_over():
    laughing_imgs = [laughing_img1, laughing_img2]
    img_index = 0
    start_time = pygame.time.get_ticks()
    title_font = pygame.font.SysFont("segoeuiblack", 100)
    subtitle_font = pygame.font.SysFont("Arial", 40, "bold")
    subtitle_label = subtitle_font.render("press p to play again", True, BLACK)
    laugh_sound.play(-1)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    laugh_sound.stop()
                    menu()

        window.fill(BLACK)
        window.blit(laughing_imgs[img_index], (0, 0))
        window.blit(title_font.render("GAME OVER", True, BLACK), (155, 0))
        window.blit(subtitle_label, (265, 100))

        now = pygame.time.get_ticks()
        if now - start_time >= 500:
            if img_index + 1 < len(laughing_imgs):
                img_index += 1
            else:
                img_index = 0
            start_time = pygame.time.get_ticks()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


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
    score = 0
    score_font = pygame.font.SysFont("Arial", 30, "bold")
    lives = 3

    scorechange_font = pygame.font.SysFont("Arial", 50, "bold")
    scorechange_start = None
    scorechange_pos = None
    increase_score = None

    hammer_x, hammer_y = window.get_rect().center
    hammer = Hammer(window, hammer_x, hammer_y)
    hammer_hit = False
    hit_start = None

    # time (in ms) waited after a minion pops up
    pop_wait = 1500
    pop_start = pygame.time.get_ticks()
    chosen_hole = choose_hole(holes)

    level_font = pygame.font.SysFont("Arial", 80, "bold")
    level = 1
    minion_count = 0
    minions_hit = 0
    minion_count_font = pygame.font.SysFont("comicsans", 30)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    menu()

            if event.type == pygame.MOUSEBUTTONDOWN:
                hammer_hit = True
                hit_start = pygame.time.get_ticks()

                for h in holes:
                    if h.rect.collidepoint(event.pos) and h.minion_in:
                        h.minion_in = False
                        scorechange_pos = h.rect.center
                        scorechange_start = pygame.time.get_ticks()
                        increase_score = True
                        score += 5
                        hammer_sound.play()
                        minions_hit += 1
                        break

            if event.type == pygame.MOUSEMOTION:
                if not hammer_hit:
                    hammer.x, hammer.y = pygame.mouse.get_pos()

        window.fill(LIGHT_YELLOW)
        clock.tick(60)

        window.blit(score_font.render(f"SCORE:{score}", True, BLACK), (10, 10))
        window.blit(level_font.render(f"LEVEL {level}", True, BLACK), (300, 15))
        hits_label = minion_count_font.render(f"Hit {15 - minions_hit} more minions to level up!",
                                              True, BLACK)
        window.blit(hits_label, (10, WINDOW_SIZE[1] - 50))

        for hole in holes:
            hole.draw()

        x = 840
        for i in range(lives):
            window.blit(heart_img, (x, 5))
            x -= 50

        if lives == 0:
            game_over()

        if pop_start is not None:
            now = pygame.time.get_ticks()
            if now - pop_start >= pop_wait:
                if chosen_hole.minion_in:
                    scorechange_pos = chosen_hole.rect.center
                    scorechange_start = pygame.time.get_ticks()
                    increase_score = False

                    lives -= 1

                chosen_hole.minion_in = False
                chosen_hole = choose_hole(holes)
                chosen_hole.minion_in = True
                minion_count += 1

                pop_start = pygame.time.get_ticks()

        hammer.draw(hammer_hit)

        if hit_start is not None:
            now = pygame.time.get_ticks()
            if now - hit_start >= 300:
                hammer_hit = False

        if scorechange_start is not None:
            now = pygame.time.get_ticks()
            if now - scorechange_start < 350:
                if increase_score:
                    window.blit(scorechange_font.render("+5", True, GREEN), scorechange_pos)
                else:
                    window.blit(scorechange_font.render("-", True, RED), scorechange_pos)
                    heart_img2 = pygame.transform.scale(heart_img, (40, 40))
                    window.blit(heart_img2, (scorechange_pos[0]+20, scorechange_pos[1]+15))

                    if losepoint_sound.get_num_channels() == 0:
                        losepoint_sound.play()

        if level <= 5 and minion_count == 15:
            level += 1
            minion_count = 0
            minions_hit = 0
            pop_wait -= 200
        elif level == 6:
            victory(score)

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


def menu():
    play_button = Button(window, "PLAY", LIGHT_BLUE, WHITE, 280, 280, 300, 120)
    menu_music.play(-1)

    run = True
    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_button.rect.collidepoint(event.pos):
                    menu_music.stop()
                    main()

        window.blit(menu_bg, (0, 0))
        window.blit(menu_title, (100, 20))
        play_button.draw()

        pygame.display.update()

    pygame.quit()
    sys.exit(0)


if __name__ == "__main__":
    menu()
