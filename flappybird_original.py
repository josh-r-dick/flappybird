
"""
November 16, 2016 Update:

    - Pipes start moving after the bird has progressed further in to the game.
    - Backgrounds change based on how long the game has been played.

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
    """
    Represents the Bird flying through the game.
    """

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
        self.surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)

        self.flap_count = 0
        self.climbingcount = 0

        self.score = Score()

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
        self.score.draw(gamescreen)
        self.surface.blit(self.image, (0, 0))
        gamescreen.blit(self.surface, (self.x, self.y))

    def crashed(self, p_list):
        """
        Check if the bird crashed in to the ground or a pipe in the pipes_list

        :return: True if the bird crashed in to the ground.
        """
        if self.y >= (SCREENHEIGHT - self.height):
            return True

        for p in p_list:
            if p.collide(self):
                return True

        return False

    def get_rect(self):
        """
        Get the bounding rectangle.

        :return: The bounding rectangle.
        """
        return self.surface.get_bounding_rect().move(self.x, self.y)

    def scored(self, p_list):
        """
        Has the bird scored on the pipe list.

        :param p_list: List of pipes to check if the bird has passed.
        :return: True if the bird scored.
        """
        for pipes in p_list:
            if pipes.passed(self) and not pipes.score_counted:
                pipes.score_counted = True
                self.score.score()
                return True

        return False

    def reset(self):
        self.y = SCREENHEIGHT / 2
        self.score.score_count = 0

class Pipe:
    """
    Represents a single pipe, top or bottom.
    """

    # Flags indicating position and drawing direction.
    TOP = 0
    BOTTOM = 1

    # Height of a pipe piece.
    PIECE_HEIGHT = 32
    # Width of a pipe.
    WIDTH = 80

    # Pipe Images
    BODY_IMAGE = pygame.image.load("resources/images/pipe_body.png")
    END_IMAGE = pygame.image.load("resources/images/pipe_end.png")

    # How many extra pieces to draw to accommodate for up/down movement
    EXTRA_PIECES = 10

    def __init__(self, x, pieces, position):
        self.x = x
        self.y = 0
        # Offset to have the pipes move up and down.
        self.y_offset = 0

        self.position = position
        self.pieces = pieces
        self.height = Pipe.PIECE_HEIGHT * (self.pieces + 1 + Pipe.EXTRA_PIECES)
        self.startPosition = self.calculates_start_position()

        self.surface = pygame.Surface((Pipe.WIDTH, self.height), pygame.SRCALPHA)

        # If we're a bottom pipe, draw the end at y=0, otherwise use the calculation.
        if position == Pipe.BOTTOM:
            self.end_position = 0
        else:
            self.end_position = 1

    def draw(self, gamescreen):
        """
        Draw the Pipe.
        """
        for i in range(0, self.pieces + Pipe.EXTRA_PIECES):
            self.surface.blit(Pipe.BODY_IMAGE, (0, i * Pipe.PIECE_HEIGHT))

        # Keep track of the pipe's y screen position.
        self.y = self.startPosition + self.y_offset
        self.surface.blit(Pipe.END_IMAGE, (0, i * Pipe.PIECE_HEIGHT * self.end_position))
        # Draw the pipe's surface.
        gamescreen.blit(self.surface, (self.x, self.y))

    def calculates_start_position(self):
        """
        Calculate the pipe draw start position based on whether or not it's a top pipe or a bottom pipe.
        :return:  0 if this is a top pipe, or (SCREENHEIGHT - Pipe.PIECE_HEIGHT) to start drawing from
        """
        # start_pos = (SCREENHEIGHT - Pipe.PIECE_HEIGHT) * self.position
        start_pos = (SCREENHEIGHT - self.height) * self.position
        if self.position == Pipe.TOP:
            start_pos -= Pipe.PIECE_HEIGHT * Pipe.EXTRA_PIECES
        else:
            start_pos += Pipe.PIECE_HEIGHT * Pipe.EXTRA_PIECES

        return start_pos

    def update(self, x, y_offset):
        """
        Update the pipe.
        :param x: New X value.
        """
        self.x = x
        self.y_offset = y_offset

    def get_rect(self):
        """
        Get the screen rectangle around the Pipe.
        :return: Rectangle with game screen position.
        """
        return self.surface.get_bounding_rect().move(self.x, self.y)

    def collide(self, b):
        """
        Check if the given bird collides with the pipe's rectangle.
        :param b: The bird.
        :return: True if the bird has collided with this pipe.
        """
        return self.get_rect().colliderect(b.get_rect())


class Pipes:
    """
    Represents a pair of pipes that generate with a random gap between them and move from
    right to left.
    """

    # Frames between adding a pipe.
    ADD_INTERVAL = 200

    # Pixel per frame speed at which the pipe moves from right to left.
    PIPE_SPEED = 2

    # Can only have a maximum number of pipe pieces to allow the bird through and to draw the pipe top on each pipe
    MAX_PIPE_PIECES = (SCREENHEIGHT - 3 * Bird.HEIGHT - 3 * Pipe.PIECE_HEIGHT) / Pipe.PIECE_HEIGHT

    # Min and max number of frames the pipes can move up or down.
    MIN_PIPE_Y_MOVEMENT = 0
    MAX_PIPE_Y_MOVEMENT = 50
    MOVE_UP = 0
    MOVE_DOWN = 1

    # Start moving in the Y direction after this many pipes
    START_MOVING_Y_COUNT = 2

    def __init__(self, gamescreen, number_of_pipes):
        """
        Initialize the pipes.

        :param gamescreen: The game screen.
        :param number_of_pipes: The number of this pipe.
        """
        self.score_counted = False
        self.x = SCREENWIDTH
        self.y = 0

        # Randomly generate the number of pipes for the top.
        self.top_pieces = randint(1, Pipes.MAX_PIPE_PIECES)
        # The opposite number is how many bottom pieces we have.
        self.bottom_pieces = Pipes.MAX_PIPE_PIECES - self.top_pieces
        # Create the pipes.
        self.top_pipe = Pipe(self.x, self.top_pieces, Pipe.TOP)
        self.bottom_pipe = Pipe(self.x, self.bottom_pieces, Pipe.BOTTOM)

        self.y_movement_duration = randint(Pipes.MIN_PIPE_Y_MOVEMENT, Pipes.MAX_PIPE_Y_MOVEMENT)
        self.y_movement_direction = randint(Pipes.MOVE_UP, Pipes.MOVE_DOWN)
        self.y_movement_count = 0
        # This is the next pipe.
        self.number = number_of_pipes + 1

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

        # If we are still moving, move up or down accordingly
        if self.number < Pipes.START_MOVING_Y_COUNT:
            self.y = 0
        elif self.y_movement_count < self.y_movement_duration:
            self.y_movement_count += 1
            if self.y_movement_direction == Pipes.MOVE_DOWN:
                self.y += 1
            elif self.y_movement_direction == Pipes.MOVE_UP:
                self.y -= 1
        # Otherwise reset the movement for the next time around
        else:
            self.y_movement_duration = randint(Pipes.MIN_PIPE_Y_MOVEMENT, Pipes.MAX_PIPE_Y_MOVEMENT)
            self.y_movement_direction = randint(Pipes.MOVE_UP, Pipes.MOVE_DOWN)
            self.y_movement_count = 0

        self.x -= 1
        self.top_pipe.update(self.x, self.y)
        self.bottom_pipe.update(self.x, self.y)

    def is_visible(self):
        """
        Is the pipe pair still visible.
        :return: True if the pipes has moved past 0, i.e. off screen
        """
        return self.x + Pipe.WIDTH > 0

    def collide(self, b):
        """
        Check if the bird collided with the pipes.
        :param b: The bird.
        :return: True if the bird collided with the top or bottom pipe.
        """
        return self.top_pipe.collide(b) or self.bottom_pipe.collide(b)

    def passed(self, bird):
        if self.x + Pipe.WIDTH < bird.x:
            return True
        else:
            return False


class Score:
    """
    Maintains and renders the score.
    """

    # The number images.
    NUMBERS = (
        pygame.image.load('resources/images/numbers/0.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/1.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/2.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/3.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/4.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/5.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/6.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/7.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/8.png').convert_alpha(),
        pygame.image.load('resources/images/numbers/9.png').convert_alpha()
    )

    # The width of a number, plus some padding.
    NUMBER_WIDTH = 24 + 1
    # Number height
    NUMBER_HEIGHT = 36
    # Total number of digits.
    DIGITS = 3

    def __init__(self):
        # Area to render the score on.
        self.surface = pygame.Surface((Score.DIGITS * Score.NUMBER_WIDTH, Score.NUMBER_HEIGHT), pygame.SRCALPHA)
        # The score.
        self.score_count = 0

    def draw(self, gamescreen):
        """
        Draw the current score on the game screen.

        :param gamescreen: The game screen to draw on.
        """
        score_string = str(self.score_count)
        self.surface.fill(0)

        # Draw each digit.
        digit_count = 0
        for d in score_string:
            self.surface.blit(Score.NUMBERS[int(d)], (digit_count * Score.NUMBER_WIDTH, 0))
            digit_count += 1

        gamescreen.blit(self.surface, (SCREENWIDTH - self.surface.get_width(), 5))

    def score(self):
        """
        Increment the score.

        :return: The updated score.
        """
        self.score_count += 1
        return self.score_count


class Background:
    """
    Keeps track of the background image and switches them accordingly.
    """

    # Length of  a day or night in frames
    DAY_NIGHT_LENGTH = 120

    # Dawn/dusk transition frames, for a smooth transition this should be a multiple of 255 (or close to it)
    # for a smooth transition.
    TRANSITION_TIME = 51

    def __init__(self):

        self.day_background = pygame.image.load("resources/images/background.png").convert()
        self.night_background = pygame.image.load("resources/images/night_background.png").convert()

        self.count = 0
        self.day = True
        self.day_alpha = 255
        self.night_alpha = 0

    def update(self):
        """
        Update the background.
        """
        # transition form day to night, or vice versa.
        if self.count == Background.DAY_NIGHT_LENGTH:
            self.day = not self.day
            self.count = 0
        # Else check for if we are in a transition
        else:
            # If we are in a transition smoothly change the alpha accordingly.
            if (Background.DAY_NIGHT_LENGTH - Background.TRANSITION_TIME) <= self.count <= Background.DAY_NIGHT_LENGTH:
                if self.day:
                    self.day_alpha -= 255 / Background.TRANSITION_TIME
                    self.night_alpha = 255
                else:
                    self.night_alpha -= 255 / Background.TRANSITION_TIME
                    self.day_alpha = 255

        # Increment the time and update the alphas accordingly.
        self.count += 1
        self.day_background.set_alpha(self.day_alpha)
        self.night_background.set_alpha(self.night_alpha)

    def draw(self, gamescreen):
        """
        Draw the backgrounds on the gamescreen.

        If it is during the day, draw the day on top, then during transition it will fade out. The opposite happens
        at night.
        :param gamescreen:
        """
        if self.day:
            gamescreen.blit(self.night_background, (0, 0))
            gamescreen.blit(self.day_background, (0, 0))
        else:
            gamescreen.blit(self.day_background, (0, 0))
            gamescreen.blit(self.night_background, (0, 0))

"""
Game Control

"""
# Create a bird
bird = Bird(SCREENWIDTH/2, SCREENHEIGHT/2)

background = Background()

# Keep track of how often to add pipes.
pipe_counter = 0

# List of pipes
number_of_pipes = 0
pipes_list = [Pipes(screen, number_of_pipes)]

game_counter = 0

score = 0

"""
The game loop.
"""
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
            bird.reset()
            pipe_counter = 0
            number_of_pipes = 0
            pipes_list = [Pipes(screen, number_of_pipes)]
            paused = False
            game_over = False

    # Tick the clock, clear the screen and draw everything.
    clock.tick(FPS)
    screen.fill(0)
    background.draw(screen)

    # Draw all the pipes
    for p in pipes_list:
        p.draw(screen)

    # Bird and score on top.
    bird.draw(screen)

    # Update the bird and pipes if the game is not paused and not game over
    if not paused and not game_over:
        bird.update()
        background.update()

        # Update each pipe, removing ones that are no longer visible.
        for p in pipes_list:
            p.update()
            if not p.is_visible():
                pipes_list.remove(p)

        # Increment the pipe counter and add one if it is time to.
        pipe_counter += 1
        if pipe_counter > Pipes.ADD_INTERVAL:
            pipes_list.append(Pipes(screen, number_of_pipes))
            number_of_pipes += 1
            pipe_counter = 0

        # Update the score.
        bird.scored(pipes_list)

    elif paused:
        screen.blit(paused_image, (60, 200))

    elif game_over:
        screen.blit(game_over_image, (60, 200))

    if bird.crashed(pipes_list):
        game_over = True

    pygame.display.flip()

    game_counter += 1

