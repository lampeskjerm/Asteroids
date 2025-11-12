import pygame
import random
from logger import log_event
from circleshape import CircleShape
from constants import *
from shot import Shot

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        line_width = self.radius
        pygame.draw.circle(screen, (50, 0, 0), self.position, self.radius, line_width)
        pygame.draw.circle(screen, (200, 200, 200), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt

    def shrink(self):
        if self.radius <= ASTEROID_MIN_RADIUS:
            self.death()
            return
        else:
            self.kill()
            log_event("asteroid_split")
            angle = random.uniform(20, 50)
            new_velocity = self.velocity.rotate(angle)
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            new_asteroid = Asteroid(self.position, self.position, new_radius)
            new_asteroid.velocity = new_velocity * random.uniform(1.25, 1.75)


    def merge(self, other):
        if self.radius >= other.radius and self.radius <= ASTEROID_MAX_RADIUS * 2:
            log_event("asteroid_merge")
            self.kill()
            other.kill()
            new_velocity = self.velocity
            new_radius = self.radius + other.radius
            if new_radius <= ASTEROID_MAX_RADIUS * 2:
                new_asteroid = Asteroid(self.position, other.position, new_radius)
            else:
                new_asteroid = Asteroid(self.position, other.position, ASTEROID_MAX_RADIUS * 2)
            new_asteroid.velocity = new_velocity * random.uniform(0.75, 1)
        else:
            self.bounce(other)
        

    def bounce(self, other):
        angle_to_other = self.position.angle_to(other.position)
        angle_to_self = other.position.angle_to(self.position)
        self.velocity = self.velocity.rotate(angle_to_other - 180)
        other.velocity = other.velocity.rotate(angle_to_self - 180)

    def death(self):
        for i in range(int(random.uniform(2, 9))):
            new_velocity = self.velocity.rotate(random.uniform(40, 180) * i)
            new_shot = Shot(self.position, self.position)
            new_shot.velocity = new_velocity * random.uniform(4, 6)
        self.kill()