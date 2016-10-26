
"""
October 20, 2016:

    - Added a simple background image.
    - Can now.
    - The Bird can crash.
    - Animated the wings.

"""

import pygame
from random import randint

# Static game variables.
FPS = 30
SCREENWIDTH = 284
SCREENHEIGHT = 512

# Initialize the game.
pygame.init()
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT))

# Background image
background_image = pygame.image.load("resources/images/background.png")
# Paused image
paused_image = pygame.image.load("resources/images/paused.png")
# Game over image.
game_over_image = pygame.image.load("resources/images/game_over.png")

# Clock to control the frame rate
clock = pygame.time.Clock()

# Game loop flag
done = False
# Tracking pause and game over
paused = False
game_over = False


class Bird:

    HEIGHT = WIDTH = 32
    CLIMB_DURATION = 8
    FLAP_DURATION = 5

    def __init__(self, x, y):
        # The bird's position
        self.x, self.y = x, y
        self.width, self.height = 32, 32

        # The bird's image.
        self.wing_up_image = pygame.image.load("resources/images/bird_wing_up.png")
        self.wing_down_image = pygame.image.load("resources/images/bird_wing_down.png")
        self.wing_up = True
        self.image = self.wing_up_image

        self.flap_count = 0
        self.climbingcount = 0

    def climb(self):
        """
        Make the bird climb.

        """
        self.climbingcount = Bird.CLIMB_DURATION

    def update(self):
        """
        Update the Bird. This is meant to be called every time through the game loop because the bird is
        always falling.
        """
        if self.climbingcount > 0:
            self.y -= 4
            self.climbingcount -= 1
        else:
            if self.y < (SCREENHEIGHT - self.height):
                self.y += 3

        # Flap the wings
        self.flap()


    def flap(self):
        """
        Alternate the wings every FLAP_DURATION count.
        """
        if self.flap_count < Bird.FLAP_DURATION:
            self.flap_count += 1
        else:
            self.flap_count = 1

            if self.wing_up:
                self.image = self.wing_up_image
            else:
                self.image = self.wing_down_image

            self.wing_up = not self.wing_up

    def draw(self, gamescreen):
        """
        Draw the bird on the given game screen.

        :param gamescreen: The game screen.
        """
        gamescreen.blit(self.image, (self.x, self.y))

    def crashed(self):
        """
        Check if the bird crashed in to the ground.

        :return: True if the bird crashed in to the ground.
        """
        if self.y >= (SCREENHEIGHT - self.height):
            return True
        else:
            return False


class Pipe:
    """
    Represents a single pipe, top or bottom.
    """

    # Flags indicating position and drawing direction.
    TOP = 0
    BOTTOM = 1
    UP = -1
    DOWN = 1

    # Height of a pipe piece.
    PIECE_HEIGHT = 32

    # Pipe Images
    BODY_IMAGE = pygame.image.load("resources/images/pipe_body.png")
    END_IMAGE = pygame.image.load("resources/images/pipe_end.png")

    def __init__(self, x, pieces, position):
        self.x = x
        self.position = position
        self.pieces = pieces
        self.startPosition = self.calculates_start_position()
        if position == Pipe.BOTTOM:
            self.direction = Pipe.UP;
        else:
            self.direction = Pipe.DOWN;

    def draw(self, gamescreen):
        """
        Draw the Pipe.
        """
        for i in range(0, self.pieces):
            gamescreen.blit(Pipe.BODY_IMAGE, (self.x, self.startPosition + self.direction * i * Pipe.PIECE_HEIGHT))
        gamescreen.blit(Pipe.END_IMAGE, (self.x, self.startPosition + self.direction * self.pieces * Pipe.PIECE_HEIGHT))

    def calculates_start_position(self):
        """
        Calculate the pipe draw start position based on whether or not it's a top pipe or a bottom pipe.
        :return:  0 if this is a top pipe, or (SCREENHEIGHT - Pipe.PIECE_HEIGHT) to start drawing from
        """
        return (SCREENHEIGHT - Pipe.PIECE_HEIGHT) * self.position

    def update(self, x):
        """
        Update the pipe.
        :param x: New X value.
        """
        self.x = x


class Pipes:
    """
    Represents a pair of pipes that generate with a random gap between them and move from
    right to left.
    """

    # Width of a pipe.
    WIDTH = 80

    # Frames between adding a pipe.
    ADD_INTERVAL = 200

    # Pixel per frame speed at which the pipe moves from right to left.
    PIPE_SPEED = 2

    # Can only have a maximum number of pipe pieces to allow the bird through and to draw the pipe top on each pipe
    MAX_PIPE_PIECES = (SCREENHEIGHT - 3 * Bird.HEIGHT - 3 * Pipe.PIECE_HEIGHT) / Pipe.PIECE_HEIGHT

    def __init__(self, gamescreen):
        self.x = SCREENWIDTH

        # Randomly generate the number of pipes for the top.
        self.top_pieces = randint(1, Pipes.MAX_PIPE_PIECES)
        # The opposite number is how many bottom pieces we have.
        self.bottom_pieces = Pipes.MAX_PIPE_PIECES - self.top_pieces
        # Create the pipes.
        self.top_pipe = Pipe(self.x, self.top_pieces, Pipe.TOP)
        self.bottom_pipe = Pipe(self.x, self.bottom_pieces, Pipe.BOTTOM)

    def draw(self, gamescreen):
        """
        Draw the pipes on the gamescreen
        :param gamescreen: The game screen.
        """
        self.top_pipe.draw(gamescreen)
        self.bottom_pipe.draw(gamescreen)

    def update(self):
        """
        Update the pipes.
        """
        self.x -= 1
        self.top_pipe.update(self.x)
        self.bottom_pipe.update(self.x)

    def is_visible(self):
        """
        Is the pipe pair still visible.
        :return: True if the pipes has moved past 0, i.e. off screen
        """
        return self.x + Pipes.WIDTH > 0


"""
Game Control

"""
# Create a bird
bird = Bird(SCREENWIDTH/2, SCREENHEIGHT/2)
# List of pipes
pipes_list = [Pipes(screen)]
# Keep track of how often to add pipes.
pipe_counter = 0

# Game loop
while not done:

    # Check for game events.
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            done = True
        # Fly
        elif event.type == pygame.KEYUP and event.key == pygame.K_SPACE:
            bird.climb()
        # Pause
        elif event.type == pygame.KEYUP and event.key == pygame.K_p:
            paused = not paused
        # Reset
        elif event.type == pygame.KEYUP and event.key == pygame.K_r:
            bird.y = SCREENHEIGHT/2
            paused = False
            game_over = False

    # Tick the clock, clear the screen and draw everything.
    clock.tick(FPS)
    screen.fill(0)
    screen.blit(background_image, (0, 0))
    bird.draw(screen)

    # Draw all the pipes
    for p in pipes_list:
        p.draw(screen)

    # Update the bird and pipes if the game is not paused and not game over
    if not paused and not game_over:
        bird.update()

        # Update each pipe, removing ones that are no longer visible.
        for p in pipes_list:
            p.update()
            if not p.is_visible():
                pipes_list.remove(p)

        # Increment the pipe counter and add one if it is time to.
        pipe_counter += 1
        if pipe_counter > Pipes.ADD_INTERVAL:
            pipes_list.append(Pipes(screen))
            pipe_counter = 0
    elif paused:
        screen.blit(paused_image, (60, 200))
    elif game_over:
        screen.blit(game_over_image, (60, 200))

    # Draw the game over screen if the bird crashed, and pause the game
    if bird.crashed():
        game_over = True

    pygame.display.flip()

