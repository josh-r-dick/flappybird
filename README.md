# flappybird

A flappy bird clone written for the Code Enrichment program at NMS. It is a work in progress.

Controls:
* ```space```, ```p``` to pause, ```r``` to reset.

## November 2, 2016

The Bird now crashes in to the pipes. Added rectangles to Bird and Pipes to track their positions on screen, this made
it possible to do collision detection. Also added a full reset to the game, pushing ```r``` now clears the pipes and
resets the bird's position.

Things to do in ```flappybird.py```:
- Get the Bird and Pipe rectangles.
- Check for collisions between them.
- Reset the game.

## October 27, 2016

Pipes have been added. Pipes class added to hold two Pipe(s), top and bottom. The main game maintains a list of pipes
representing each top and bottom pipe pair, a new pipe is added based on a counter, old pipes are removed once they
move off screen.

Things to do:
- Draw the pies off the right side of the screen.
- Move the pipes.
- Game freezes when the bird crashes, add a key command to reset the game.
