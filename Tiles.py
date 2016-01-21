

class Tile:
    def __init__(self, name, dwarves):
        self.name = name

    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return [newGamestate]
