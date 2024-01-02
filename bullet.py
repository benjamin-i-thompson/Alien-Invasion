#Ben Thompson | 3/3

import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """A class to manage bullets fired from the ship"""

    def __init__(self,ai_game):
        """Create a byllet object at the ship's current position"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color                         #pulling the color settings of the bullet from the settings file

        #Create a bullet rect at (0,0) and then set correct position.
        self.rect = pygame.Rect(0,0, self.settings.bullet_width,self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        #Store the bullet's position as a decimal value.
        self.y = float(self.rect.y)

    def update(self):
        """Move the bullet up the screen."""
        #Update the decimal position of the bullet
        self.y -= self.settings.bullet_speed            #Creating an update loop so it decreases in y value to go up the screen
        #Update the rect position
        self.rect.y = self.y                            #Don't need to create an x update because the bullet will only be moving vertically

    def draw_bullet(self):
        """Draw the bullet to the screen."""
        pygame.draw.rect(self.screen,self.color,self.rect)