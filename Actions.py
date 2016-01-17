from constants import *



class ActionSpace:
    def __init__(self, name, accumulate=[[],[]], pickup=[]):
        self.name = name
        self.accumulate = accumulate
        self.pickup = pickup
        self.inUse = 0
        
        self.itemDic = {}
        for item in items: self.itemDic[item] = 0
        
    def _update(self):
        self.inUse = 0
    
        n = sum(self.itemDic.values())
        if n > 6:
            for key in self.itemDic.keys(): self.itemDic[key] = 0
        elif n == 0:
            for key in self.accumulate[0]: self.itemDic[key] += 1
        else:
            for key in self.accumulate[1]: self.itemDic[key] += 1
    
    def _use(self, gamestate):
        gamestate['inventory']['dwarves']['home'] -= 1
        gamestate['inventory']['dwarves']['working'] += 1
        self.inUse = 1
        for key in self.itemDic.keys():
            gamestate['inventory'][key] += self.itemDic[key]
            self.itemDic[key] = 0
        for item in self.pickup:
            gamestate['inventory'][item] += 1 
        gamestate['inventory']['history'][-1].append(self.name)

    def use(self, gamestate):
        self._use(gamestate)
        return [gamestate]

class TilePlacementAction(ActionSpace):
    def __init__(self, name, accumulate=[[],[]], pickup=[], tile=[]):
        self.tile = tile
        ActionSpace.__init__(self, name, accumulate=[[],[]], pickup=[])
    def use(self, gamestate):
        self._use(gamestate)
        self.placeTile(gamestate)
        return [gamestate]
    def placeTile(self, gamestate):
        pass
    
NormalActions = [ActionSpace(name, acc, pickup) for (name, acc, pickup) in 
            [('Logging', [['wood']*3,['wood']], []),
             ('Wood gathering', [['wood']]*2, []), 
             ('Ore mining', [['ore']*2,['ore']], []), 
             ('Ruby mining', [['ruby']]*2, []), 
             ('Blacksmithing', [[],[]], []),
             ('Sheep Farming', [['sheep']]*2, []), 
             ('Wish for children', [[],[]], []),
             ('Donkey farming', [['donkey']]*2, []), 
             ('Ore delivery', [['ore','rock']]*2, []), 
             ('Family life', [[],[]], []), 
             ('Ore trading', [[],[]], []), 
             ('Adventure', [[],[]], []), 
             ('Ruby delivery', [['ruby']*2,['ruby']], [])]]
TileActions = [TilePlacementAction(name, acc, pickup, tile) for (name, acc, pickup, tile) in
            [('Excavation',[['rock']]*2,[],['cave','tunnel','cavern']), 
             ('Sustenance', [['food']]*2, ['wheat'],['forest','field','farm']),
             ('Housework', [[],[]], ['dog'],['cave','furnish']), 
             ('Slash-and-burn', [[],[]], [],['forest','field','farm']), 
             ('Ore mine construction', [[],[]], [],['cave','deep tunnel','ore mine']),           
             ('Ruby mine construction', [[],[]], [],['cave','ruby mine'])]]
Actions = NormalActions + TileActions
for act in Actions: locals()[act.name]=act

#Excavation.use = 