# flappybird

A flappy bird clone written for the Code Enrichment program at NMS. It is a work in progress.

Controls:
* ```space```, ```p``` to pause, ```r``` to reset, ```z``` to fire!

## November 23, 2016

Added Enemies and fireballs to shoot them with. Now has a simple start screen too.

Things to add:
- Enemies that move in more than along the x axis at a fixed speed.
- Alternate between pipes and enemies.

## November 16, 2016

Pipes now start moving up and down after a certain point in the game. Default is 2 pipes, but that can be changed.

Also added transition between day and night backgrounds.

Things to add:
- Some good looking start, end and pause screens.
- Bird death animation.

## November 9, 2016

You can score. The score is incremented every time the bird passes a pipe. The pipe x positions are checked against the
bird's x position to add a point.

Also added movement to the pipes to make the game harder. The pipes move up or down randomly for 0 to 100 frames. This
makes the game a lot harder right off  the bat.

Things to add:
- How can we turn on the pipe up/down movemnt after a certain score?
- Change the backgrounds as time goes on?
- How to add a good looking start screen and end screen?

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
