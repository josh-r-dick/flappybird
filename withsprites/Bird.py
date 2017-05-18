

import pygame

class Bird(pygame.sprite.Sprite):
    """
    Represents the Bird flying through the game.
    """

    HEIGHT = WIDTH = 32
    CLIMB_DURATION = 8
    FLAP_DURATION = 5

    def __init__(self, x, y):
        super(Bird, self).__init__()
        # The bird's position
        self.x, self.y = x, y
        self.width, self.height = 32, 32

        # The bird's image.
        self.wing_up_image = pygame.image.load("resources/images/bird_wing_up.png").convert_alpha()
        self.wing_down_image = pygame.image.load("resources/images/bird_wing_down.png").convert_alpha()
        self.wing_up = True
        self.image = self.wing_up_image
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
