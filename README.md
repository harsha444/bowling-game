# BOWLING GAME
To run the code, use the following steps

```
git clone https://github.com/harsha444/bowling-game.git

cd bowling-game/

python3 bowling.py
```
You will be asked a set of questions. Follow accordingly to simulate the game.

## Documentation

`Arena`
- Arena is basically where we have bowling lanes.
- An arena may have multiple bowling lanes
- At any point of time the maximum number of games that can be played is equal to the number of lanes available. Right now, it is set to 5. Configurable in constants.py

`Game`
- Just a base class for any game.
- In case we have any other kinds of games, this class becomes a base to be inherited by such various games and generic attributes and methods of a game will be specified here.

`Player`
- Player related info such as name and score.
- Can be extended to other player attributes.

`BowlingGame`
- Inherits from the base class Game.
- Contains all the bowling game attributes (like scoreboard, is_strike, players in game etc..)
- Core logic of the bowling game is also present in this.

> Also, a simulator logic is present which simulates the game.

All the constants are in constants.py and are configurable.