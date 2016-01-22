

class Tile:
    def __init__(self, name, points, cost, dwarves=0, animals={}, num=1):
        self.name = name
        self.dwarves = dwarves
        self.pts = points
        self.cost = cost
        self.num = num
        self.animals = animals
        
    def points(self, gamestate):
        return self.pts


class StarterDwelling(Tile):
    def __init__(self):
        Tile.__init__(self, 'Starter dwelling', 0, [], dwarves=2, animals={'num':2,'type':farmAnimals})
        
class Dwelling(Tile):
    def __init__(self):
        Tile.__init__(self, 'Dwelling', 3, ['wood']*4+['rock']*3, dwarves=1, num=17)

class SimpleDwelling1(Tile):
    def __init__(self):
        Tile.__init__(self, 'Simple dwelling', 0, ['wood']*4+['rock']*2, dwarves=1)
        
class SimpleDwelling2(Tile):
    def __init__(self):
        Tile.__init__(self, 'Simple dwelling', 0, ['wood']*3+['rock']*3, dwarves=1)
        
class MixedDwelling(Tile):
    def __init__(self):
        Tile.__init__(self, 'Mixed dwelling', 4, ['wood']*5+['rock']*4, animals={'num':2,'type':farmAnimals}, dwarves=1)

class CoupleDwelling(Tile):
    def __init__(self):
        Tile.__init__(self, 'Couple dwelling', 5, ['wood']*8+['rock']*6, dwarves=2)
        
# TODO Additional dwelling

class Carpenter(Tile):
    def __init__(self):
        Tile.__init__(self, 'Carpenter', 0, ['rock'])
    # TODO

class StoneCarver(Tile):
    def __init__(self):
        Tile.__init__(self, 'Stone carver', 1, ['wood'])
    # TODO
    
class Blacksmith(Tile):
    def __init__(self):
        Tile.__init__(self, 'Blacksmith', 3, ['wood']+['rock']*2)
    # TODO   

class Miner(Tile):
    def __init__(self):
        Tile.__init__(self, 'Miner', 3, ['wood']+['rock'])
    # TODO
    
class Builder(Tile):
    def __init__(self):
        Tile.__init__(self, 'Builder', 2, ['rock'])
    # TODO
    
class Trader(Tile):
    def __init__(self):
        Tile.__init__(self, 'Trader', 2, ['wood'])
    # TODO
    
class CuddleRoom(Tile):
    def __init__(self):
        Tile.__init__(self, 'Cuddle room', 2, ['wood'])
    # TODO
    
class BreakfastRoom(Tile):
    def __init__(self):
        Tile.__init__(self, 'Breakfast room', 0, ['wood'])
    # TODO
  
class StubbleRoom(Tile):
    def __init__(self):
        Tile.__init__(self, 'Studdle room', 1, ['wood']+['ore'])
    # TODO 

class WorkRoom(Tile):
    def __init__(self):
        Tile.__init__(self, 'Work room', 2, ['rock'])
    # TODO    
    
class GuestRoom(Tile):
    def __init__(self):
        Tile.__init__(self, 'Guest room', 0, ['wood']+['rock'])
    # TODO    



Dwellings = [Dwelling(), SimpleDwelling1(), SimpleDwelling2(), MixedDwelling(), CoupleDwelling()]
Others = [Carpenter(), StoneCarver(), Blacksmith(), Miner(), Builder(), Trader(), CuddleRoom(), BreakfastRoom(),
          StubbleRoom(), WorkRoom(), GuestRoom()]

Tiles = Dwellings + Others
      
