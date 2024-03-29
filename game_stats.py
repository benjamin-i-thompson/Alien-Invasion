#Ben Thompson

class GameStats: #creating a new file and class to track stats for the game
    """Track stats for Alien Invasion"""

    def __init__(self, ai_game):
        """Initialize stats"""
        self.settings = ai_game.settings
        self.reset_stats()


        # Start game in an inactive state
        self.game_active = False

        #High score should never be reset
        self.high_score = 0 # initialize here so it doesnt get reset in reset_stats()

    def reset_stats(self):
        """Initialize stats that can change during the game"""
        self.ships_left = self.settings.ship_limit
        self.score = 0
        self.level = 1