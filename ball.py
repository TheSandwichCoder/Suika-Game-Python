import math

import pygame.draw
from random import randint
from vector import Vec2
import settings


ScreenSize = (1280, 720)

CollisionBoundary = (0, 0, 480, 630)

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


class Ball:
    def __init__(self,pos, vec, fruitType):
        self.pos = Vec2(pos)
        self.vec = Vec2(vec)
        self.fruitType = fruitType
        self.size = settings.fruitSizeArray[fruitType]
        self.image = pygame.transform.scale(fruitTypeImageArray[fruitType], (self.size, self.size))
        self.radius = self.size/2
        self.elasticity = 0.3
        self.maincolor = (255, 0, 0)
        self.color = self.maincolor
        self.gravityVec = Vec2((0,50))#Vec2((0,9.807))
        self.pressure = 0
        self.angularMomentum = 0
        self.angle = 0
        self.collided = False
        self.aboveHeightTimer = 0

    def is_containerCollision(self):
        n1 = False
        n2 = False
        n3 = False
        n4 = False

        if self.pos.x - self.radius < CollisionBoundary[0]:
            n1 = True
            self.collided = True

        if self.pos.x + self.radius > CollisionBoundary[2]:
            n2 = True
            self.collided = True

        if self.pos.y - self.radius < CollisionBoundary[1]:
            n3 = True
            self.collided = True

        if self.pos.y + self.radius > CollisionBoundary[3]:
            n4 = True
            self.collided = True

        return (n1,n2,n3,n4)

    def containerCollisionPhysics(self, delta):
        collisionBool = self.is_containerCollision()
        if collisionBool[3]:
            self.pos = Vec2((self.pos.x, CollisionBoundary[3]-self.radius))
            self.vec = Vec2((self.vec.x, -abs(self.vec.y)*self.elasticity))

            self.angularMomentum -= self.vec.x / math.pi * 180 * delta * 0.01

        elif collisionBool[2]:
            self.pos = Vec2((self.pos.x, CollisionBoundary[1] + self.radius))
            self.vec = Vec2((self.vec.x, abs(self.vec.y)*self.elasticity))

        elif collisionBool[0]:
            self.pos = Vec2((CollisionBoundary[0]+self.radius, self.pos.y))
            self.vec = Vec2((abs(self.vec.x)*self.elasticity, self.vec.y))

        elif collisionBool[1]:
            self.pos = Vec2((CollisionBoundary[2]-self.radius, self.pos.y))
            self.vec = Vec2((-abs(self.vec.x)*self.elasticity, self.vec.y))


    def is_ballCollision(self, ball):
        dis = self.pos- ball.pos

        if dis.mag < (self.radius+ball.radius):
            return True
        return False

    def ballCollisionPhysics(self, ball):
        if self.is_ballCollision(ball):
            self.collided = True
            ball.collided = True

            dis = self.pos - ball.pos
            perpendicularDis = dis.perpendicular_norm()

            self.angularMomentum /= 1.07
            ball.angularMomentum /= 1.07

            ratio = self.size**2 / (ball.size**2 + self.size**2)


            dif = self.radius+ball.radius-dis.mag

            dis.normalise_self()
            ave_elasticity = ((self.elasticity+ball.elasticity)/2)
            d1 = dis * (dif/2)
            d2 = dis * dif * ave_elasticity * 10

            self.pos.increment(d1 * (1-ratio))
            ball.pos.increment(-d1 * ratio)
            self.containerCollisionPhysics(0.1)
            ball.containerCollisionPhysics(0.1)

            self.vec.increment(d2 * (1-ratio))
            ball.vec.increment(-d2 * ratio)

            self.pressure += d2.mag

            thing = (ball.vec-self.vec).overlap(perpendicularDis)
            thing2 = (thing/self.radius)*180/math.pi
            thing3 = (thing/ball.radius)*180/math.pi
            self.angularMomentum -= thing2
            ball.angularMomentum += thing3

            return True
        return False

    # def compiledBallCollisionPhysics(self, ball):
    #     if self.is_ballCollision(ball):
    #         values = collision(self.pos.position, self.vec.position, self.radius, self.elasticity, ball.pos.position, ball.vec.position, ball.radius, ball.elasticity)
    #         self.pos = Vec2(values[0])
    #         self.vec = Vec2(values[1])
    #         ball.pos = Vec2(values[2])
    #         ball.vec = Vec2(values[3])
    #         self.pressure += 1
    #         return True
    #     return False




    def gravity(self, delta):
        self.vec.increment(self.gravityVec*delta)

    def update(self, delta):
        self.pressure = 0
        self.gravity(delta)
        self.containerCollisionPhysics(delta)
        self.pos.increment(self.vec*delta)
        self.angle += (self.angularMomentum)*delta
        self.angle %= 360
        self.angularMomentum /= 1.01


    def draw(self, screen):
        # pygame.draw.circle(screen, self.color, self.pos.position, self.radius)
        # angleRadian = self.angle*math.pi/180
        # pygame.draw.line(screen, (0,0,0), *(self.pos.position, (self.pos+Vec2((math.sin(angleRadian), math.cos(angleRadian)))*self.radius).position))
        #
        # self.color = self.maincolor

        imageRot = pygame.transform.rotate(self.image, self.angle)
        size = Vec2(imageRot.get_size())
        screen.blit(imageRot, (self.pos-size*0.5).position)

    def drawVector(self, screen):
        pygame.draw.line(screen, self.maincolor, *(self.pos.position,(self.pos+self.vec.normalise()*25).position))
