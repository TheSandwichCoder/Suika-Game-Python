import math
import random

from vector import Vec2
import pygame

class smallSmokeParticle():
    def __init__(self, pos, mag):
        self.size = random.randint(3,7)*mag
        self.pos = Vec2(pos)
        self.angle = random.randint(0,360)
        self.speed = random.randint(1,3) * ((8-self.size)/(7*mag))
        radian = self.angle*math.pi/180

        self.vec = Vec2((math.sin(radian)*2*self.speed, math.cos(radian)*2*self.speed))


    def update(self):
        self.pos += self.vec
        self.size /= 1.05

    def draw(self, screen):
        pygame.draw.circle(screen, (232, 232, 232), self.pos.position, self.size/2)

class smokeParticle():
    def __init__(self, pos, size):
        self.pos = pos
        self.delete = False
        self.subSmokeParticles = [smallSmokeParticle(self.pos.position, size) for i in range(7)]

    def update(self):
        num = 0
        for particle in self.subSmokeParticles:
            particle.update()

            if particle.size < 1:
                num += 1

        if num == len(self.subSmokeParticles):
            self.delete = True

    def draw(self, screen):
        for particle in self.subSmokeParticles:
            particle.draw(screen)