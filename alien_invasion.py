#Ben Thompson

import sys
from time import sleep

import pygame

from settings import Settings
from ship import Ship #importing the ship from the ship file
from game_stats import GameStats #importing the stats from the game stats file
from bullet import Bullet          #Importing the bullets from the bullet file
from alien import Alien# Importing Alien class from alien file
from button import Button # Importing Button class
from scoreboard import Scoreboard #Importing the scoreboard

class AlienInvasion:
    """Overalll class to manage game assets and behavior"""
    def __init__(self):
        """Initialize the game, and create game resources"""
        pygame.init()

        self.settings = Settings()

        #self.screen = pygame.display.set_mode(0,0), pygame.FULLSCREEN)
        #self.setting.screen_width = self.settings.get_rect().width
        #self.settings.screen_height = self.settings.get_rect().height
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height)) #taking the screen settings from the settings file
        pygame.display.set_caption("Alien Invasion")

        #Create an instance to store game stats and create scoreboard
        #Create an instance to store game stats
        self.stats = GameStats(self)
        self.sb = Scoreboard(self)

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()

        self._create_fleet()

        # Make the play button.
        self.play_button = Button(self, "Play")

    def run_game(self):
        """Start the main loop for the game"""
        while True:
            #Watch for keyboard and mouse events.
            self._check_events()                                        #Newly added 2/16

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()           #Updating the bullets with each pass of the loop
                self._update_aliens()

            self._update_screen()

            #Get rid of bullets that have disappeared.
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
                print(len(self.bullets))

    def _check_events(self):                                    #Just added 2/16
        """Respond to keypresses and mouse movements."""
        for event in pygame.event.get():#                       moving this to the new def
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:# adding movement keys using keyup and keydown to make it continuous
               self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """Start a new game when the player clicks play"""
        button_clicked = self.play_button.rect.collidepoint(mouse_pos)
        if button_clicked and not self.stats.game_active:
            #reset game settings
            self.settings.initialize_dynamic_settings()

            #reset game stats
            self.stats.reset_stats()
            self.stats.game_active = True
            self.sb.prep_score()
            self.sb.prep_level()
            self.sb.prep_ships()

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleet and center the ship
            self._create_fleet()
            self.ship.center_ship()

            # Hide mouse button
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self,event):
        """Respond to keypresses."""
        if event.key == pygame.K_RIGHT:
            # move ship right
            self.ship.moving_right = True  # adding keypress for left and right continuous motion 2/18
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_q:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()


    def _check_keyup_events(self,event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False

    def _fire_bullet(self):
        """Create a new bullet and add it to the bullets group."""
        if len(self.bullets) < self.settings.bullets_allowed:
            new_bullet = Bullet(self)
            self.bullets.add(new_bullet)

    def _update_bullets(self):
        """Update position of bullets and get rid of old bullets."""
        # Update bullet positions.
        self.bullets.update()

        # Get rid of old bullets
        for bullet in self.bullets.copy():# adding a loop to delete old bullets
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)


        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """Respond to bullet-alien collisions."""
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)

        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
            self.sb.prep_score()
            self.sb.check_high_score()

        # Remove any bullets and aliens that have collided.
        if not self.aliens:
            # Destroy existing bullets and create new fleet.
            self.bullets.empty()
            self._create_fleet()
            self.settings.increase_speed()

            # Increase level
            self.stats.level += 1
            self.sb.prep_level()

    def _create_fleet(self): # Creating a new def for the fleet to put all the requirements in
        """Create the fleet of aliens."""
        # Make an alien.
        # Create an alien and find the number of aliens in a row
        # Spacing between each alien is equal to one alien width
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - (2*alien_width)
        number_aliens_x = available_space_x // (2*alien_width)

        # Determine the number of rows of aliensthat fit on the screen.
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height - (3*alien_height) - ship_height)# Calculating the available space for the aliens
        number_rows = available_space_y // (2*alien_height)

        # Create the full fleet of aliens.
        for row_number in range(number_rows):
            for alien_number in range(number_aliens_x):
                self._create_alien(alien_number,row_number)

    def _create_alien(self,alien_number,row_number):
        """Create an alien and place it in the row."""
        alien = Alien(self)
        alien_width,alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien_height + 2*alien.rect.height*row_number
        self.aliens.add(alien)

    def _update_aliens(self):
        """Check if the fleet is an edge, then update the position of all aliens in the fleet."""
        self._check_fleet_edges()
        self.aliens.update() #updating all aliens

        # Look for alien-ship collision
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # Look for aliens hitting the bottom of screen
        self._check_aliens_bottom()

    def _check_fleet_edges(self):
        """Respond appropriately if any aliens have reached an edge."""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                self._change_fleet_direction()
                break

    def _check_aliens_bottom(self):
        """Check if any aliens reach the bottom of the screen"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _change_fleet_direction(self):
        """Drop the entire fleet and change the fleet's direction."""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed# Returning true if the fleet hits an edge
        self.settings.fleet_direction *= -1

    def _ship_hit(self):
        """Respond to the ship being hit by an alien"""
        if self.stats.ships_left > 0: #Checking to see how many ships are left
            #Decrement ships_left, update screen
            self.stats.ships_left -= 1
            self.sb.prep_ships() # calling prep_ships to decrease the remaining ships on scoreboard

            # Get rid of any remaining aliens and bullets
            self.aliens.empty()
            self.bullets.empty()

            #Create a new fleed and center the ship
            self._create_fleet()
            self.ship.center_ship

            # Ship
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _update_screen(self):
        """Update images on the screen, and flip to the new screen."""
        self.screen.fill(self.settings.bg_color)  # pulling more settings from the settings file instead of doing all in one file
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self.aliens.draw(self.screen) # 3/9, added the update to show the alien on update screen

        # draw the score info
        self.sb.show_score()

        #draw the play button if the game is inactive
        if not self.stats.game_active:
            self.play_button.draw_button()

        # make the most revently drawn screen visible.
        pygame.display.flip()

if __name__ == '__main__':
    #make a game instance, and run the game
    ai = AlienInvasion()
    ai.run_game()