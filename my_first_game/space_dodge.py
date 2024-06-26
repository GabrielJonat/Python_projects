# Space Dodge 2.0 by Gabriel Jonathan de Matos
import pygame
import time
import random
import os

pygame.font.init()
WIDTH, HEIGHT = 1000, 740
TELA = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Star Dodge by Gabriel Jonathan")
BG = pygame.image.load("bg.jpg")
pygame.mixer.init()
PLAYER_WIDTH = 40
PLAYER_HEIGHT = 60
PLAYER_VEL = 1.618
PROJECTILE_WIDTH = 10
PROJECTILE_HEIGHT = 20
proj_vel = 3.4
FONT = pygame.font.SysFont("Comicsans", 30)
bestTime = 0
average_time = 0
best_times = []
add_chances = 0
RECORDFILE = 'best_time.txt'
msg = " "
pygame.mixer.music.load("free_song.ogg")
pygame.mixer.music.play(loops=-1)


def set_record(file_name,message):
    with open(file_name, 'w') as file:
        file.write(str(message))

def get_record(file_name):
    with open(file_name, 'r') as file:
        content = file.read()
        return content

bestTime = 0 if os.stat(RECORDFILE).st_size == 0 else int(get_record(RECORDFILE))

def Paused():
    pauseText = FONT.render("Paused", 1, "yellow")
    TELA.blit(pauseText, (WIDTH // 2 - pauseText.get_width() // 2, HEIGHT // 2 - pauseText.get_height() // 2))
    pygame.display.update()


def draw(player, elapsedTime, projectiles, slowees, bestTime, average_time, add_chances, vidas, specials,msg):
    TELA.blit(BG, (0, 0))
    timeText = FONT.render("Time: " + str(round(elapsedTime)) + "s", 1, "yellow")
    bestTimeText = FONT.render("Best time: " + str(round(bestTime)) + "s", 1, "yellow")
    averageTimeText = FONT.render("Average time: " + str(round(average_time)) + "s", 1, "yellow")
    chancesText = FONT.render("Stamina: " + str(add_chances), 1, "yellow")
    special_msg = FONT.render(msg, 1, "yellow")
    TELA.blit(bestTimeText, (750, 5))
    TELA.blit(timeText, (10, 5))
    TELA.blit(averageTimeText, (WIDTH // 2 - averageTimeText.get_width() // 2, 5))
    TELA.blit(chancesText, (842, 570))
    TELA.blit(special_msg, (10, 700))
    pygame.draw.rect(TELA, "red", player)
    for projectile in projectiles:
        pygame.draw.rect(TELA, "white", projectile)
    for slowee in slowees:
        pygame.draw.rect(TELA, "blue", slowee)
    for vida in vidas:
        pygame.draw.rect(TELA, "green", vida)
    for special in specials:
        pygame.draw.rect(TELA, "purple", special)
    pygame.display.update()


def main(bestTime, average_time, best_times, add_chances):
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    elapsedTime = 0
    projectile_add_increment = 1000
    slowees_add_increment = 7000
    slowee_count = 0
    projectile_count = 0
    special_count = 0
    projectiles = []
    slowees = []
    specials = []
    hit = False
    pause = False
    time_slow = False
    special_activate = False
    special_hit = False
    vidas_add_increment = 7000
    special_add_increment = 11500
    vidas_count = 0
    vidas = []
    global msg
    
    while run:
        dt = clock.tick(170)  # Compute delta time (dt)
        if not pause:  # Update time only if not paused
            elapsedTime += dt / 1000  # Convert milliseconds to seconds

        projectile_count += dt
        slowee_count += dt
        vidas_count += dt
        special_count += dt

        if projectile_count > projectile_add_increment:
            for i in range(random.randint(0, 5)):
                proj_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                proj = pygame.Rect(proj_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                projectiles.append(proj)
            minimo = 120 if add_chances >= 2 else 163
            decr = 20 if add_chances <= 2 else 78
            projectile_add_increment = max(minimo, projectile_add_increment - decr)
            projectile_count = 0

        if slowee_count > slowees_add_increment:
            for i in range(random.randint(0, 1)):
                slowee_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                slowee = pygame.Rect(slowee_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                slowees.append(slowee)
            minimo = 1100 if add_chances <= 2 else 2000
            slowees_add_increment = max(minimo, slowees_add_increment - 30)
            slowee_count = 0

        if vidas_count > vidas_add_increment:
            for i in range(random.randint(0, 1)):
                vidas_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                vida = pygame.Rect(vidas_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                vidas.append(vida)
            vidas_add_increment = max(1000, slowees_add_increment - 25)
            vidas_count = 0

        if  special_count > special_add_increment:
            for i in range(random.randint(0, 2)):
                spec_x = random.randint(0, WIDTH - PROJECTILE_WIDTH)
                special = pygame.Rect(spec_x, -PROJECTILE_HEIGHT, PROJECTILE_WIDTH, PROJECTILE_HEIGHT)
                specials.append(special)
            special_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    pause = not pause
                    projectile_add_increment = 675
                    if pause:
                        for _ in range(500):
                            Paused()
                            projectile_add_increment += 2
        if not pause:
            key = pygame.key.get_pressed()
            if key[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if key[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
            if key[pygame.K_a] and player.x - PLAYER_VEL >= 0:
                player.x -= PLAYER_VEL
            if key[pygame.K_d] and player.x + PLAYER_VEL + player.width <= WIDTH:
                player.x += PLAYER_VEL
            if (key[pygame.K_x] or key[pygame.K_m]) and player.x + PLAYER_VEL * 1.618 + player.width <= WIDTH:  
                player.x += PLAYER_VEL * 1.618
            if (key[pygame.K_z] or key[pygame.K_n]) and player.x - PLAYER_VEL * 1.618 > 0:
                player.x -= PLAYER_VEL * 1.618
            if (key[pygame.K_c] or key[pygame.K_j]) and player.x - PLAYER_VEL * 1.618 > 0:
                player.x -= PLAYER_VEL * 1.618 ** 3
            if (key[pygame.K_v] or key[pygame.K_k]) and player.x + PLAYER_VEL * 1.618 + player.width <= WIDTH:
                player.x += PLAYER_VEL * 1.618 ** 3
            if key[pygame.K_SPACE] and special_hit:
                special_activate = True
                special_hit = False
                msg = "Immortality Activated"
                special_begin = 0

            for projectile in projectiles[:]:
                global proj_vel
                projectile.y += proj_vel
                if projectile.y > HEIGHT:
                    projectiles.remove(projectile)
                elif projectile.y + projectile.height >= player.y and projectile.colliderect(player):
                    projectiles.remove(projectile)
                    hit = True
                    break

            for slowee in slowees[:]:
                slowee.y += 3.4
                if slowee.y > HEIGHT:
                    slowees.remove(slowee)
                elif slowee.y + slowee.height >= player.y and slowee.colliderect(player):
                    slowees.remove(slowee)
                    time_slow = True
                    slow_begin = 0
                    break

            for vida in vidas[:]:
                vida.y += 3.4
                if vida.y > HEIGHT:
                    vidas.remove(vida)
                elif vida.y + vida.height >= player.y and vida.colliderect(player):
                    vidas.remove(vida)
                    add_chances += 1 
                    break

            for special in specials[:]:
                special.y += 3.4
                if special.y > HEIGHT:
                    specials.remove(special)
                elif special.y + special.height >= player.y and special.colliderect(player):
                    specials.remove(special)
                    if not special_activate:
                        special_hit = True
                        msg = "Press SPACE to activate the special"
                    break

        if special_activate:
            if special_begin == 0:
                special_begin = time.time()
            if time.time() - special_begin >= 5:
                        special_activate = False
                        msg = " "

        if hit:
            if special_activate:
                hit = False
            elif add_chances > 0:
                hit = False
                add_chances -= 1
            else:
                game_over = FONT.render("VOCÊ FOI DE ARRASTA PRA CIMA! GAME OVER!", 1, "yellow")
                TELA.blit(game_over, (WIDTH // 2 - game_over.get_width() // 2, HEIGHT // 2 - game_over.get_height() // 2))
                if elapsedTime >= bestTime:
                    bestTime = elapsedTime
                    set_record(RECORDFILE,round(bestTime))
                best_times.append(elapsedTime)
                average_time = sum(best_times) / len(best_times)
                pygame.display.update()
                pygame.time.delay(2000)
                if elapsedTime > average_time and len(best_times) > 0:
                    congratulations = FONT.render("VOCÊ É FERA! ABOVE AVERAGE SCORE!",1,"yellow")
                    TELA.blit(BG,(0,0))
                    TELA.blit(congratulations, (WIDTH // 2 - congratulations.get_width() // 2, HEIGHT // 2 - congratulations.get_height() // 2))
                    pygame.display.update()
                    pygame.time.delay(1600)
                proj_vel = 3.4
                if special_hit:
                    special_hit = False
                    msg = " "
                break

        if time_slow:
            proj_vel = 2.1
            projectile_add_increment += 0.8
            if slow_begin == 0:
                slow_begin = time.time()

        if time_slow and time.time() - slow_begin >= 7:  # Compare to current time
            time_slow = False
            projectile_add_increment = 300
            slow_begin = 0  # Reset slow_begin for the next slow down

        if not time_slow:
            proj_vel = 3.4

        draw(player, elapsedTime, projectiles, slowees, bestTime, average_time, add_chances, vidas,specials,msg)

    main(bestTime, average_time, best_times, add_chances)


if __name__ == "__main__":
    main(bestTime, average_time, best_times, add_chances)

