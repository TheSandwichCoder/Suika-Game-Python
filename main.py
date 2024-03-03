import pygame
from ball import Ball
from vector import Vec2
from random import randint
from Chunk import Chunks
from particles import smokeParticle
import settings
import time


pygame.init()

pygame.font.init()
pygame.font.get_init()

screenSize = (480, 630)
pygame.display.set_caption("Suika Game")

grapeImage = pygame.image.load("assets/suikaGameFruits/grape.png")
appleImage = pygame.image.load("assets/suikaGameFruits/apple.png")
orangeImage = pygame.image.load("assets/suikaGameFruits/orange.png")
watermelonImage = pygame.image.load("assets/suikaGameFruits/watermelon.png")
strawberryImage = pygame.image.load("assets/suikaGameFruits/Strawberry.png")
pineappleImage = pygame.image.load("assets/suikaGameFruits/pineapple.png")
durianImage = pygame.image.load("assets/suikaGameFruits/durian.png")
pearImage = pygame.image.load("assets/suikaGameFruits/pear.png")
peachImage = pygame.image.load("assets/suikaGameFruits/peach.png")
rambutanImage = pygame.image.load("assets/suikaGameFruits/rambutan.png")
cherryImage = pygame.image.load("assets/suikaGameFruits/cherry.png")

fruitTypeImageArray = (cherryImage, grapeImage, strawberryImage, rambutanImage, pearImage, appleImage, orangeImage, peachImage, durianImage, pineappleImage, watermelonImage)
smokeParticleArray = []
background = pygame.Surface(screenSize)

for i in range(40):
    if i%2 == 0:
        color = (239,207,127)
    else:
        color = (253, 231, 157)
        # color = (241, 205, 129)

    pygame.draw.line(background,color , *((i*20,0),(i*20,screenSize[1])), 20)

for i in range(0,100,2):
    pygame.draw.line(background,(255,255,255) , *((i*10,70),(i*10+10,70)),5)


pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode(screenSize)

font = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 45)
font2 = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 15)
font3 = pygame.font.Font("assets/Roboto/Roboto-Regular.ttf", 30)
f = open('ball_positions.txt', 'a')

ballArray = []
chunks = Chunks()

generalDelta = 0.06
delta = 0.1
intervals = 50
see_chunks = False
paused = False

spawnedBall = False
selectedBall = None

def clamp(min, max, n):
    if n > max:
        return max
    elif n < min:
        return min
    return n

def keyinputs(ballArray):
    global spawnedBall
    global selectedBall

    if pygame.mouse.get_pressed()[0]:
        mousePos = pygame.mouse.get_pos()
        # ballArray.append(Ball((mousePos[0], 30), (0, 0), randint(0, 4)))

        if not spawnedBall:
            if selectedBall == None:

                selectedBall = Ball((mousePos[0], 30), (0,0), randint(0,4))


                spawnedBall = True
    else:
        if spawnedBall:
            ballArray.append(selectedBall)
            # selectedBall = None
        spawnedBall = False


def delta_stuff():
    global paused
    global delta
    global generalDelta
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        paused = True
    else:
        paused = False



    if keys[pygame.K_LEFT]:
        if generalDelta > 0.001:
            generalDelta -= 0.001
    elif keys[pygame.K_RIGHT]:
        if generalDelta < 10:
            generalDelta += 0.001

    elif keys[pygame.K_DOWN]:
        generalDelta = 0.1

    delta = generalDelta


def chunking(ballArray):
    chunks.clear()
    for ball in ballArray:
        ball.containerCollisionPhysics(delta)

    chunks.addBalls(ballArray)
    if see_chunks:
        chunks.draw(screen)
        for ball in ballArray:
            chunks.draw_surroundingObjects(ball.pos, screen)
        chunks.seeOccupiedChunks(screen)

        chunks.highlightChunk((255, 0, 0), chunks.get_chunkIndex(Vec2(pygame.mouse.get_pos())), screen)
    # for ball in ballArray:
        # chunks.get_surroundingObjects(ball.pos, screen)






score = 0
def ballEnlargementThing(ballArray):
    global score
    for ball in ballArray:
        if ball.fruitType == 10:
            continue
        if ball.pos.y-ball.radius < 0:
            continue


        surroundingBalls = chunks.get_surroundingObjects(ball.pos)
        for ball2 in surroundingBalls:
            if ball == ball2:
                continue

            elif ball.is_ballCollision(ball2):
                if ball.radius == ball2.radius:
                    try:
                        ballArray.remove(ball2)
                    except:
                        pass

                    ball.fruitType += 1
                    ball.size = settings.fruitSizeArray[ball.fruitType]
                    ball.image = pygame.transform.scale(fruitTypeImageArray[ball.fruitType], (ball.size, ball.size))
                    ball.radius = ball.size / 2
                    ball.angularMomentum = 0
                    smokeParticleArray.append(smokeParticle(Vec2(ball.pos.position), ball.size/10))
                    score += int((ball.fruitType**2)*10)
                    break


def ballCollision(ballArray):
    for ball in ballArray:
        if ball.pos.y-ball.radius < 0:
            continue


        surroundingBalls = chunks.get_surroundingObjects(ball.pos)
        n = 1
        for i in range(n):
            breakout = True
            for ball2 in surroundingBalls:
                if ball == ball2:
                    continue
                elif ball.ballCollisionPhysics(ball2):
                    breakout = False
            if breakout:
                break





    # for ball1 in ballArray:
    #     for ball2 in ballArray:
    #         if ball1 == ball2:
    #             continue
    #
    #         ball1.ballCollisionPhysics(ball2)



gamestate = "N"
loseText = "Imagine Losing lol"
loseTextRendered = font.render(loseText, 1, (0,0,0))
loseTextRenderedSize = Vec2(loseTextRendered.get_size())

scoreText = f"SCORE: {score}"
scoreTextRendered = font.render(scoreText, 1, (0,0,0))


while True:


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            f.close()
    screen.fill((30, 30, 30))
    screen.blit(background, (0,0))

    delta_stuff()

    if gamestate != "L":
        keyinputs(ballArray)





    keys = pygame.key.get_pressed()

    chunking(ballArray)


    for ball in ballArray:
        ball.update(delta)
        if ball.pos.y < 70 and ball.vec.mag < 5:
            # print("asdasd")
            ball.aboveHeightTimer += 1
        else:
            ball.aboveHeightTimer = 0

        # print(ball.aboveHeightTimer)

        if ball.aboveHeightTimer >= 180:
            gamestate = "L"







    st = time.time()
    ballEnlargementThing(ballArray)
    ballCollision(ballArray)
    et = time.time()

    if selectedBall != None:
        if pygame.mouse.get_pressed()[0] and spawnedBall:
            selectedBall.pos.update(pygame.mouse.get_pos()[0], 30)
        selectedBall.draw(screen)

        if selectedBall.collided:

            selectedBall = None

    for particle in smokeParticleArray:
        particle.update()
        if particle.delete:
            smokeParticleArray.remove(particle)


    for ball in ballArray:
        ball.draw(screen)

    for particle in smokeParticleArray:
        particle.draw(screen)

    if gamestate == "L":
        scoreText = f"SCORE: {score}"
        scoreTextRendered = font2.render(scoreText, 1, (0, 0, 0))
        scoreTextRenderedSize = Vec2(scoreTextRendered.get_size())

        blitPos = ((Vec2(screenSize) - loseTextRenderedSize) * 0.5 - Vec2((0, 25))).position
        blitPos2 = ((Vec2(screenSize) - scoreTextRenderedSize) * 0.5 + Vec2((0, 25))).position

        screen.blit(loseTextRendered, blitPos)
        screen.blit(scoreTextRendered, blitPos2)
        screen.blit(font2.render("press [SPACE] to play again", 1, (0, 0, 0)), (Vec2(blitPos2)+Vec2((-20, 25))).position)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            ballArray.clear()
            gamestate = "N"
            score = 0

    else:
        scoreText = f"SCORE: {score}"
        scoreTextRendered = font3.render(scoreText, 1, (0, 0, 0))
        screen.blit(scoreTextRendered, (0,0))

    balls_onscreen = 0
    total_energy = 0


    array = []
    for ball in ballArray:
        if ball.pos.y > 0:
            balls_onscreen += 1
            total_energy += ball.vec.mag
        array.append(ball.pos.position)

    # f.write(str(array)+",")

    # screen.blit(font.render("FPS:" + str(round(clock.get_fps())), 1, (255, 255, 255)), (0, 0))
    # screen.blit(font.render("Balls:" + str(len(ballArray))+"  "+str(balls_onscreen), 1, (255, 255, 255)), (0, 15))
    # screen.blit(font.render("General Delta:" + str(round(generalDelta,100)), 1, (255, 255, 255)), (0, 30))
    # screen.blit(font.render("Coll Time:" + str(round((et-st)*1000))+"ms", 1, (255, 255, 255)), (0, 45))
    # screen.blit(font.render("Total Energy:" + str(round(total_energy)), 1, (255, 255, 255)), (0, 60))

    clock.tick(60)


    pygame.display.flip()

