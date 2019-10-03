import random
from collections import defaultdict


class Arena:
    """
    Class to configure an arena. An arena can accommodate x number of Bowling lanes
    """
    n_lanes = 5  # Keeping it default for now

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
        self.score = 0

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
        Game.__init__(self, n_players)
        self.frame_number = 1
        self.players = []
        self.rolls = defaultdict(list)
        self.scores = defaultdict(list)  # Keeping a track of individual scores for each roll as well
        for i in range(n_players):
            player = input(f"Enter player {i + 1} name: ")
            self.players.append(Player(player))
        Arena.join_arena()

    def get_scoreboard(self):
        """
        Prints the scoreboard at a given point of game.
        :return:
        """
        # print(self.scores, self.rolls)
        for _player in self.players:
            player_name = _player.get_name()
            print(f"{player_name}")
            print(f"Rolls: {self.rolls.get(player_name)}")
            print(f"Scores: {self.scores.get(player_name)}")

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
        Gets the winner of this game
        :return:
        """
        user_score_map = {i: i.get_score() for i in self.players}
        max_score = max(user_score_map.values())
        return list(filter(lambda i: user_score_map[i] == max_score, list(user_score_map.keys())))

    def calculate_set_score(self, _set):
        """
        Calculates score of a set
        :param _set:
        :return:
        """
        if self.is_strike(_set):
            return sum(_set) + 10
        elif self.is_spare(_set):
            return sum(_set) + 5
        else:
            return sum(_set)

    def start_game(self):
        """
        Initiating the game with random rolls
        :return:
        """
        if Arena.n_lanes_available() <= 0:
            print("Lanes are not available.")
            return
        for i in range(1, 11):
            self.frame_number = i
            for _player in self.players:
                _set = []
                first_strike = random.randint(0, 10)
                _set.append(first_strike)
                if BowlingGame.is_strike(_set) and i != 11:
                    self.rolls[_player.get_name()].append(_set)
                    _player.score += 20
                    self.scores[_player.get_name()].append(_player.get_score())
                    continue
                else:
                    second_strike = random.randint(0, 10 - first_strike)
                    _set.append(second_strike)
                    self.rolls[_player.get_name()].append(_set)
                    if BowlingGame.is_spare(_set):
                        _player.score += 15
                    else:
                        _player.score += sum(_set)
                    self.scores[_player.get_name()].append(_player.get_score())
        Arena.leave_arena()
        self.get_scoreboard()

    def start_game_v2(self):
        """

        :return:
        """
        if Arena.n_lanes_available() <= 0:
            print("No lanes available")
            return
        while self.frame_number <= 10:
            for _player in self.players:
                _set = []
                first_strike = random.randint(0, 10)
                _set.append(first_strike)
                second_strike = random.randint(0, 10 - first_strike) if not self.is_strike(_set) else None
                if second_strike is not None:
                    _set.append(second_strike)
                if self.frame_number == 10 and (self.is_strike(_set) or self.is_spare(_set)):
                    third_strike = random.randint(0, 10)
                    _set.append(third_strike)
                self.rolls[_player.get_name()].append(_set)
                _player.score = _player.score + self.calculate_set_score(_set)
                self.scores[_player.get_name()].append(_player.score)
            self.frame_number += 1
        Arena.leave_arena()
        self.get_scoreboard()


if __name__ == "__main__":
    g = BowlingGame(2)
    g.start_game_v2()
