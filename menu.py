import pygame
import sys
from player import Player
from constants import SCREEN_WIDTH, SCREEN_HEIGHT


class Menu:

    def update(self, screen, kills, highscore):

        big_font = pygame.font.Font(None, 72)
        menu_font = pygame.font.Font(None, 48)
        small_menu_font = pygame.font.Font(None, 32)

        # Game Over
        game_over_text = big_font.render("Game over!", True, "white")
        rect = game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/13 * 4))
        screen.blit(game_over_text, rect)
        
        # Kills
        kills_text = menu_font.render(f"Kills: {kills}", True, (255, 0, 0))
        kills_rect = kills_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/13 * 5))
        screen.blit(kills_text, kills_rect)

        # New Game
        new_game_text = small_menu_font.render("enter - new game", True, "white")
        new_game_rect = new_game_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/13 * 9))
        screen.blit(new_game_text, new_game_rect)
        
        # Quit Game
        quit_game_text = small_menu_font.render("esc - quit game", True, "white")
        quit_game_rect = quit_game_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/13 * 10))
        screen.blit(quit_game_text, quit_game_rect)

        # High Score title
        high_score_title = menu_font.render("High Score", True, "white")
        high_score_rect = high_score_title.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/13 * 6))
        screen.blit(high_score_title, high_score_rect)

        # High Score
        high_score_1_text = small_menu_font.render(f"Kills: {highscore}", True, "white")
        high_score_1_rect = high_score_1_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/13 * 7))
        screen.blit(high_score_1_text, high_score_1_rect)

        keys = pygame.key.get_pressed()

        if keys[pygame.K_ESCAPE]:
            sys.exit()
        if keys[pygame.K_RETURN]:
            return "new game"