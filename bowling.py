import random
import time
from collections import defaultdict
from constants import ARENA_CONSTANTS as arena_constants
from constants import BOWLING_GAME_CONSTANTS as bowling_constants
from constants import PLAYER_CONSTANTS as player_constants


class Arena:
    """
    Class to configure an arena. An arena can accommodate x number of Bowling lanes
    """
    n_lanes = arena_constants.TOTAL_LANES  # Keeping it default for now

    def __init__(self):
        pass

    @classmethod
    def n_lanes_available(cls) -> int:
        """
        Gives the number of lanes available at any point of time
        :return: number of free lanes
        """
        return cls.n_lanes

    @classmethod
    def join_arena(cls):
        """
        Decreasing the number of lanes available once a game is started
        :return:
        """
        if cls.n_lanes <= 0:
            raise Exception("Lanes not available. Try after some time.")
        cls.n_lanes -= 1

    @classmethod
    def leave_arena(cls):
        """
        Increasing the number of lanes available once game is ended
        :return:
        """
        cls.n_lanes += 1


class Game:
    """
    Game Class -> used as a base class to be inherited by different games(We only have Bowling Game for now).
    """

    def __init__(self, n_players: int):
        self.number_of_players = n_players


class Player:
    """
    Player Class with player attributes
    """

    def __init__(self, name: str):
        self._name = name
        self.score = player_constants.INITIAL_SCORE

    def get_name(self) -> str:
        """
        Gets name of user
        :return: Player name
        """
        return self._name

    def get_score(self) -> int:
        """
        Gets Score of user
        :return: score of player at any point
        """
        return self.score


class BowlingGame(Game):
    """
    class with all Bowling Game attributes
    """

    def __init__(self, n_players: int):
        try:
            Arena.join_arena()
        except Exception as ex:
            raise Exception(f'{ex}')
        Game.__init__(self, n_players)
        self.frame_number = bowling_constants.INITIAL_FRAME_NUMBER
        self.players = []
        self.rolls = defaultdict(list)
        self.scores = defaultdict(list)  # Keeping a track of individual scores for each roll as well
        for i in range(n_players):
            player = input(f"Enter player {i + 1} name: ")
            self.players.append(Player(player))
        print('Joined arena!')

    def __repr__(self):
        return " vs ".join([i.get_name() for i in self.players])

    def get_scoreboard(self):
        """
        Prints the scoreboard at a given point of game.
        :return:
        """
        for _player in self.players:
            player_name = _player.get_name()
            print(f"{player_name} \n-------------------")
            print(f"Rolls: {self.rolls.get(player_name)}")
            print(f"Scores: {self.scores.get(player_name)} \n-------------------")
        winners_list = self.game_master()
        res = ","
        if len(winners_list) > 1:
            print(
                f"It's a tie between {res.join([i.get_name() for i in winners_list])} with a score of {winners_list[0].get_score()}.!")
        else:
            print(f"Winner of the game is: {winners_list[0].get_name()} with a score of {winners_list[0].get_score()}")

    @staticmethod
    def is_spare(_set: list) -> bool:
        """
        Checks if a given roll set is spare
        :param _set:
        :return:
        """
        return _set[0] != 10 and sum((_set[0], _set[1])) == 10

    @staticmethod
    def is_strike(_set: list) -> bool:
        """
        Checks if a given roll set is strike
        :param _set:
        :return:
        """
        return _set[0] == 10

    def game_master(self) -> list:
        """
        Gets a list of winners for this game
        :return:
        """
        user_score_map = {i: i.get_score() for i in self.players}
        max_score = max(user_score_map.values())
        return list(filter(lambda i: user_score_map[i] == max_score, list(user_score_map.keys())))

    def calculate_set_score(self, _set: list) -> int:
        """
        Calculates score of a set
        :param _set:
        :return:
        """
        if self.is_strike(_set):
            return sum(_set) + bowling_constants.STRIKE_BONUS
        elif self.is_spare(_set):
            return sum(_set) + bowling_constants.SPARE_BONUS
        else:
            return sum(_set)

    def start_game(self):
        """
        Starts the game
        :return:
        """
        while self.frame_number <= bowling_constants.TOTAL_FRAMES:
            print(f"FRAME:{self.frame_number}")
            for _player in self.players:
                _set = []
                first_strike = random.randint(0, 10)
                _set.append(first_strike)
                if not self.is_strike(_set):
                    second_strike = random.randint(0, 10 - first_strike)
                elif self.is_strike(_set) and self.frame_number == 10:
                    second_strike = random.randint(0, 10)
                else:
                    second_strike = None
                if second_strike is not None:
                    _set.append(second_strike)
                third_strike = None
                if self.frame_number == 10 and (self.is_strike(_set) or self.is_spare(_set)):
                    if self.is_spare(_set):
                        third_strike = random.randint(0, 10)
                    else:
                        third_strike = random.randint(0, 10 - second_strike)
                    _set.append(third_strike)
                self.rolls[_player.get_name()].append(_set)
                _player.score = _player.score + self.calculate_set_score(_set)
                display_msg = f"{_player.get_name()} rolls {first_strike} in his first strike"
                if second_strike is not None:
                    display_msg += f", {second_strike} in his second strike"
                if third_strike is not None:
                    display_msg += f" and {third_strike} rolls in his third turn"
                score_msg = f"- His score till now = {_player.score}"
                print(display_msg + score_msg)
                self.scores[_player.get_name()].append(_player.score)
                time.sleep(1)  # Added for cleaner simulation purpose
            self.frame_number += 1
        print("Game ended! Here's the score card:\n-------------------")
        Arena.leave_arena()
        self.get_scoreboard()


def simulate_game():
    """
    Test simulator to test the game
    :return:
    """
    games = {}
    i = 0
    while True:
        query = int(
            input(
                "Enter 1 to show the existing games in arena, 2 to create a new game, 3 to start a game, any other to exit: "))
        if query == 1:
            print(games)
        elif query == 2:
            n_players = int(input("Enter the number of players in the game: "))
            try:
                game = BowlingGame(n_players)
            except Exception as ex:
                print(ex)
                continue
            games[i] = game
            query = int(input("Start the game? 1/0 "))
            if query == 1:
                game.start_game()
                games.pop(i)
                i += 1
            else:
                continue
        elif query == 3:
            game_number = int(input(f"Enter the game number from {games}: "))
            if games.get(game_number):
                games[game_number].start_game()
                games.pop(game_number)
            else:
                print("No such game number available!")
        else:
            exit(1)


if __name__ == "__main__":
    simulate_game()
