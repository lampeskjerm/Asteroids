import pygame
import sys
from constants import *
from logger import log_state, log_event
from player import Player
from asteroid import Asteroid
from asteroidfield import AsteroidField
from shot import Shot
from menu import Menu

def load_high_score(filename="highscore.txt"):
    try:
        with open(filename, "r") as f:
            high_score = int(f.read())
    except (IOError, ValueError):
        high_score = 0
    return high_score

def save_high_score(high_score, filename="highscore.txt"):
        try:
            with open(filename, "w") as f:
                f.write(str(high_score))
        except IOError:
            print("Error saving high score.")

def main():
    print(f"Starting Asteroids!")
    print(f"Screen width: {SCREEN_WIDTH}")
    print(f"Screen height: {SCREEN_HEIGHT}")
    
    highscore = load_high_score()

    pygame.init()
    
    clock = pygame.time.Clock()
    dt = 0
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

    is_game_over = False
    kills = 0
    font = pygame.font.Font(None, 36)
    big_font = pygame.font.Font(None, 72)

    updatable = pygame.sprite.Group()
    drawable = pygame.sprite.Group()
    asteroids = pygame.sprite.Group()
    shots = pygame.sprite.Group()

    Asteroid.containers = (asteroids, updatable, drawable)
    AsteroidField.containers = (updatable)
    Player.containers = (updatable, drawable)
    Shot.containers = (shots, updatable, drawable)

    player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
    menu = Menu()
    asteroidfield = AsteroidField()

    while True:
        log_state()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return
        
        screen.fill((30, 35, 40))
        
        updatable.update(dt)

        for asteroid in asteroids:
            for shot in shots:
                if asteroid.collides_with(shot) == True:
                    log_event("asteroid_shot")
                    asteroid.shrink()
                    shot.kill()
                    if asteroid.radius == ASTEROID_MIN_RADIUS:
                        kills += 1

        for asteroid in asteroids:
            if asteroid.collides_with(player) == True:
                log_event("player_hit")
                player.kill()
                player.death()
                is_game_over = True
                if kills > highscore:
                    highscore = kills
                save_high_score(highscore)
        
        for asteroid in asteroids:
            other_asteroids = asteroids.copy()
            other_asteroids.remove(asteroid)
            for other_asteroid in other_asteroids:
                if asteroid.collides_with(other_asteroid) == True:
                    asteroid.merge(other_asteroid)

        asteroids2 = asteroids.copy()
        other_asteroids = asteroids.copy()
        for asteroid in asteroids2:
            other_asteroids.remove(asteroid)
            for other_asteroid in other_asteroids:
                if asteroid.collides_with(other_asteroid) == True:
                    asteroid.bounce(other_asteroid)
                    other_asteroids.remove(other_asteroid)
                    asteroids2.remove(asteroid)
                    asteroids2.remove(other_asteroid)

        for object in drawable:
            object.draw(screen)
        
        if is_game_over == False:
            kills_text = font.render(f"Kills: {kills}", True, (255, 0, 0))
            kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH/2, 25))
            screen.blit(kills_text, kills_rect)
        
        else:
        # Display game over screen / menu
            for asteroid in asteroids:
                asteroid.death()
            menu.update(screen, kills, highscore)
            if menu.update(screen, kills, highscore) == "new game":
                for shot in shots:
                    shot.kill()
                is_game_over = False
                kills = 0
                player = Player(x=SCREEN_WIDTH/2, y=SCREEN_HEIGHT/2)
            
        
        pygame.display.flip()
        
        dt = clock.tick(60) / 1000

if __name__ == "__main__":
    main()
