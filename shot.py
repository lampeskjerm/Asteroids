import pygame
from circleshape import CircleShape
from constants import SHOT_RADIUS

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)

    def draw(self, screen):
        line_width = self.radius
        pygame.draw.circle(screen, "black", self.position, self.radius, line_width)
        pygame.draw.circle(screen, (100, 100, 255), self.position, self.radius, 2)

    def update(self, dt):
        self.position += self.velocity * dt