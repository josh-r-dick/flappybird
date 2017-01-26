import pygame

"""
The enemies in a much harder version of flappy bird.

"""


class Enemy:
    """
    Represents a single enemy.
    """
    IMAGE = pygame.image.load("resources/images/ghost.png").convert_alpha()
    WIDTH = 32
    HEIGHT = 32
    SPEED = 2

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.surface = pygame.Surface((Enemy.WIDTH, Enemy.HEIGHT), pygame.SRCALPHA)
        self.dead = False

    def update(self):
        self.x -= Enemy.SPEED

    def draw(self, gamescreen):
        self.surface.fill(0)
        self.surface.blit(Enemy.IMAGE, (0, 0))
        gamescreen.blit(self.surface, (self.x, self.y))

    def is_visible(self):
        return self.x > 0

    def get_rect(self):
        """
        Get the screen rectangle around the enemy.
        :return: Rectangle with game screen position.
        """
        return self.surface.get_bounding_rect().move(self.x, self.y)

    def collide(self, rect):
        """
        check if the given rectangle collides with this enemy.
        :param rect: To check against
        :return: True if there was a collision.
        """
        return self.get_rect().colliderect(rect)


class Enemies:
    """
    Maintains a list of all the enemies in the game. Also controls the adding of a new enemey at the
    specified add interval.
    """
    # Frames between an enemy.
    ADD_INTERVAL = 150

    def __init__(self, gamescreen):
        self.enemies_list = []
        self.gamescreen = gamescreen
        self.add_count = 0

    def add(self, x, y):
        """
        Add a new enemy at the given x, y location
        :param x: X coordinate.
        :param y: Y coordiante
        """
        self.enemies_list.append(Enemy(x, y))
        self.add_count = 0

    def update(self):
        for en in self.enemies_list:
            en.update()
            if not en.is_visible():
                self.enemies_list.remove(en)

        self.add_count += 1

        if self.add_count > Enemies.ADD_INTERVAL:
            self.add(self.gamescreen.get_height()/2, self.gamescreen.get_width())

    def draw(self):
        for en in self.enemies_list:
            en.draw(self.gamescreen)

    def collide(self, rect):
        """
        Check if any of the enemies have collided with the given rectangle.
        :param rect: Rectangle ot check collisions with.
        :return: True if an enemy has collided, false if not.
        """
        for en in self.enemies_list:
            if en.collide(rect):
                return True

        return False

    def killed(self, fireball_rect):
        """
        Check if an enmy has been killed by the fireball contained in the given rectangle.
        :param fireball_rect: To check for collisions with
        :return: True if the fireball killed an enemy.
        """
        enemy_has_been_killed = False;
        for en in self.enemies_list:
            if en.collide(fireball_rect):
                self.enemies_list.remove(en)
                enemy_has_been_killed = True
        return enemy_has_been_killed

    def reset(self):
        """
        Reset.
        """
        self.add_count = 0
        self.enemies_list = []

