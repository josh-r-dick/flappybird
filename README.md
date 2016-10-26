# flappybird

A flappy bird clone written for the Code Enrichment program at NMS. It is a work in progress.

Controls:
* ```space```, ```p``` to pause, ```r``` to reset.

## October 27, 2016

Pipes have been added. Pipes class added to hold two Pipe(s), top and bottom. The main game maintains a list of pipes representing each top and bottom pipe pair, a new pipe is added based on a counter, old pipes are removed once they move off screen.

Things to do:
- Draw the pies off the right side of the screen.
- Move the pipes.
- Game freezes when the bird crashes, add a key command to reset the game.
