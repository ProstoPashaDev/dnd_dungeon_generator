from abc import ABC, abstractmethod


class Dungeon(ABC):

    @abstractmethod
    def fitness_function(self, state):
        pass
