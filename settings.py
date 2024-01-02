#Ben Thompson, 2/7

class Settings:
    """A class to store all settings for Alien Invation"""

    def __init__(self):
        """Initialize the game's static settings."""

        #settings screen
        self.screen_width = 1200 #drawing the screen width
        self.screen_height = 600 #drawing the screen height
        self.bg_color = (230, 230, 230) #picking the color for the screen background

        #Ship Settings
        self.ship_speed = 1.5       #adding a new value for the speed so it goes faster
        self.ship_limit = 3

        #Bullet Settings
        self.bullet_speed = 1.5             #setting all of the bullet settings: speed, width, height, and color
        self.bullet_width = 100
        self.bullet_height = 15
        self.bullet_color = (60,60,60)
        self.bullets_allowed = 3

        # Alien Settings
        self.alien_speed = 1.0 # 3/31 setting the alien speed
        self.fleet_drop_speed = 10


        # How quickly the game speeds up
        self.speedup_scale = 1.1

        #How quickly the alien point values increase
        self.score_scale = 1.5

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        """Initialize settings that change throughout the game."""
        self.ship_speed = 1.5
        self.bullet_speed = 1.5
        self.alien_speed = 0.5

        # Fleet direction of 1 represents right; -1 represents left
        self.fleet_direction = 1

        # Scoring
        self.alien_points = 50

    def increase_speed(self):
        """Increase speed settings and alien point values."""
        self.ship_speed *= self.speedup_scale #Speeding up the settings by the scale of 1.1
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)
        print(self.alien_points)