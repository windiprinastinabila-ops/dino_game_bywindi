import pygame
import random
import asyncio

pygame.init()
pygame.mixer.init()

# ==================================
# SCREEN
# ==================================
WIDTH = 1000
HEIGHT = 500

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pixel Dino")

clock = pygame.time.Clock()

# ==================================
# LOAD ASSETS
# ==================================
background = pygame.image.load(
    "assets/background.png"
).convert()

dino_img = pygame.image.load(
    "assets/dino.png"
).convert_alpha()

cactus_img = pygame.image.load(
    "assets/cactus.png"
).convert_alpha()

cactus2_img = pygame.image.load(
    "assets/cactus2.png"
).convert_alpha()

bird_img = pygame.image.load(
    "assets/bird.png"
).convert_alpha()

cloud_img = pygame.image.load(
    "assets/cloud.png"
).convert_alpha()

# ==================================
# SOUNDS
# ==================================
jump_sound = pygame.mixer.Sound(
    "assets/jump.ogg"
)

dead_sound = pygame.mixer.Sound(
    "assets/dead.ogg"
)

jump_sound.set_volume(0.7)
dead_sound.set_volume(0.8)

# ==================================
# SCALE PIXEL ART
# ==================================
dino_img = pygame.transform.scale(dino_img, (70, 70))
cactus_img = pygame.transform.scale(cactus_img, (50, 80))
cactus2_img = pygame.transform.scale(cactus2_img, (70, 100))
bird_img = pygame.transform.scale(bird_img, (60, 50))
cloud_img = pygame.transform.scale(cloud_img,(120, 60))
# ==================================
# COLORS
# ==================================
WHITE = (255,255,255)
BLACK = (0,0,0)

font = pygame.font.SysFont(None, 40)

GROUND_Y = 380

# ==================================
# DINO
# ==================================
dino = pygame.Rect(
    100,
    GROUND_Y - 70,
    70,
    70
)

jumping = False
velocity_y = 0
gravity = 1

# ==================================
# GAME DATA
# ==================================
game_over = False
score = 0

speed = 8

# ==================================
# CLOUDS
# ==================================
clouds = []

for i in range(3):
    clouds.append([
        random.randint(0, WIDTH),
        random.randint(50, 180)
    ])

# ==================================
# OBSTACLES
# ==================================
cactus = pygame.Rect(
    WIDTH + 300,
    GROUND_Y - 80,
    50,
    80
)

cactus2 = pygame.Rect(
    WIDTH + 900,   # jarak tetap 600 pixel dari cactus1
    GROUND_Y - 89,
    50,
    80
)

bird = pygame.Rect(
    WIDTH + 500,
    220,
    60,
    50
)

# ==================================
# RESET
# ==================================
def reset_level():
    global speed

    dino.x = 100
    dino.y = GROUND_Y - 70

    cactus.x = WIDTH + 300
    cactus2.x = WIDTH + 900

    bird.x = WIDTH + 500
    bird.y = 220

    speed = 8

# ==================================
# MAIN LOOP
# ==================================
async def main():

    global jumping
    global velocity_y
    global score
    global speed
    global game_over

    running = True

    while running:

        # ==========================
        # EVENTS
        # ==========================
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:

                    if not jumping:
                        jumping = True
                        velocity_y = -18
                        jump_sound.play()

                if event.key == pygame.K_r and game_over:

                    score = 0
                    game_over = False
                    reset_level()

        # ==========================
        # GAME
        # ==========================
        if not game_over:

            score += 1

            speed += 0.001


            # DINO JUMP
            velocity_y += gravity
            dino.y += velocity_y

            if dino.y >= GROUND_Y - 70:
                dino.y = GROUND_Y - 70
                velocity_y = 0
                jumping = False

            # CACTUS
            cactus.x -= speed
            
            if cactus.right < 0:
                cactus.x = WIDTH + random.randint(300, 800)

            # CACTUS 2
            cactus2.x -= speed

            if cactus2.right < 0:
                cactus2.x = WIDTH + random.randint(300, 800)


            # BIRD MOVE (ikut scroll seperti kaktus)
            bird.x -= speed

            if bird.right < 0:
                bird.x = WIDTH + random.randint(400, 1200)
                bird.y = random.randint(180, 260)  # sedikit variasi tinggi

            # COLLISION
            if dino.colliderect(cactus):
                game_over = True
                dead_sound.play()

            if dino.colliderect(cactus2):
                game_over = True
                dead_sound.play()

            if dino.colliderect(bird):
                game_over = True
                dead_sound.play()

            # GERAKKAN AWAN
            for cloud in clouds:

                cloud[0] -= 1

                if cloud[0] < -120:
                    cloud[0] = WIDTH

        # ==========================
        # DRAW
        # ==========================
        screen.blit(background, (0,0))

        # CLOUDS
        for cloud in clouds:
            screen.blit(
                cloud_img,
                (cloud[0], cloud[1])
            )

        pygame.draw.line(
            screen,
            BLACK,
            (0, GROUND_Y),
            (WIDTH, GROUND_Y),
            3
        )

        screen.blit(
            dino_img,
            (dino.x, dino.y)
        )

        screen.blit(
            cactus_img,
            (cactus.x, cactus.y + 8)
        )

        screen.blit(
            cactus2_img,
            (cactus2.x, cactus2.y + 8)
        )

        screen.blit(
            bird_img,
            (bird.x, bird.y)
        )

        # SCORE
        text = font.render(
            f"Score : {score}",
            True,
            BLACK
        )

        screen.blit(text, (750,20))

        # GAME OVER
        if game_over:

            over = font.render(
                "GAME OVER - Press R",
                True,
                BLACK
            )

            screen.blit(
                over,
                (320,200)
            )

        pygame.display.flip()
        clock.tick(60)

        await asyncio.sleep(0)

    pygame.quit()

asyncio.run(main())