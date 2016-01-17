from constants import *
from gameLogic import *



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

# TODO make sure all Actions are making new copies of gamestates before acting on them
class Logging(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Logging', [['wood']*3,['wood']])
    def use(self, gamestate):
        self._use(gamestate)
        return expedition(gamestate,1)
        
class WoodGathering(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Wood gathering', [['wood']]*2)
        
class OreMining(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore mining', [['ore']*2,['ore']])
    def use(self, gamestate):
        self._use(gamestate)
        #add 2 ore to inv for each mine
        gamestate['inventory']['ore'] += 2 * sum(row.count('ore mine') for row in gamestate['inventory']['cave'])
        return [gamestate]

class RubyMining(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ruby mining', [['ruby']]*2)
    def use(self, gamestate):
        self._use(gamestate)
        if sum(row.count('ruby mine') for row in gamestate['inventory']['cave']): gamestate['inventory']['ruby'] += 1 
        return [gamestate]
        
class Blacksmithing(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Blacksmithing')
    def use(self, gamestate):
        self._use(gamestate)
        states = []
        for i in range(gamestate['inventory']['ore']):
            newGamestate = copy.deepcopy(gamestate)
            newGamestate['inventory']['ore'] -= i+1
            # TODO upgrade the dwarf to i+1
            states.append(newGamestate)
        return states
        
class SheepFarming(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Sheep farming', [['sheep']]*2)
    def placeSingleFence(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def placeDoubleFence(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def getStable(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        states = []
        wood = gamestate['inventory']['wood']
        for i in range(2**3):
            if i%2 and wood >= 2:
                states += self.placeSingleFence(gamestate)
            if i/2%2 and wood >= 4:
                states += self.placeDoubleFence(gamestate) 
            if i/4%2 and gamestate['inventory']['rock']:
                states += self.getStable(gamestate)
        for state in states: self._use(state)
        return states
        
class WishForChildren(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Wish for children')
    def placeDwelling(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        states = []
        if canNewDwarf(gamestate):
            newGamestate = copy.deepcopy(gamestate)
            #add baby dwarf
            states.append(newGamestate)
        states += self.placeDwelling(gamestate)
        return states

class DonkeyFarming(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Donkey farming', [['donkey']]*2)
    def placeSingleFence(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def placeDoubleFence(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def getStable(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        states = []
        wood = gamestate['inventory']['wood']
        for i in range(2**3):
            if i%2 and wood >= 2:
                states += self.placeSingleFence(gamestate)
            if i/2%2 and wood >= 4:
                states += self.placeDoubleFence(gamestate) 
            if i/4%2 and gamestate['inventory']['rock']:
                states += self.getStable(gamestate)
        for state in states: self._use(state)
        return states
        
class OreDelivery(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore delivery', [['ore','rock']]*2)
    def use(self, gamestate):
        self._use(gamestate)
        #add 2 ore to inv for each mine
        gamestate['inventory']['ore'] += 2 * sum(row.count('ore mine') for row in gamestate['inventory']['cave'])
        return [gamestate]

class FamilyLife(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Family life')

class OreTrading(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore trading')
    def use(self, gamestate):
        self._use(gamestate)
        states = []
        for i in range(max(gamestate['inventory']['ore']/2, 3)):
            newGamestate = copy.deepcopy(gamestate)
            newGamestate['inventory']['ore'] -= 2*(i+1)
            newGamestate['inventory']['gold'] += 2*(i+1)
            newGamestate['inventory']['food'] += (i+1)
            states.append(newGamestate)
        return states
        
class Adventure(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Adventure')

class RubyDelivery(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ruby delivery', [['ruby']*2,['ruby']])
    def use(self, gamestate):
        self._use(gamestate)
        if sum(row.count('ruby mine') for row in gamestate['inventory']['cave'])/2: gamestate['inventory']['ruby'] += 1 
        return [gamestate]

class Excavation(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Excavation',[['rock']]*2)
    def placeCaveTwin(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        return self.placeCaveTwin(gamestate)
        
class Sustenance(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Sustenance', [['food']]*2, ['wheat'])
    def placeForestTwin(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        return self.placeForestTwin(gamestate)
        
class Housework(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Housework', [[],[]], ['dog'])
    def placeFurnishing(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        return self.placeFurnishing(gamestate)
        
class SlashAndBurn(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Slash-and-burn')
    def plantCrops(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        return self.plantCrops(gamestate)
        
class OreMineConstruction(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore mine construction')
    def placeOreMine(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        return self.placeOreMine(gamestate)        
        
class RubyMineConstruction(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ruby mine construction')
    def placeRubyMine(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        self._use(gamestate)
        return self.placeRubyMine(gamestate)        

Actions = [Logging(), WoodGathering(), OreMining(), RubyMining(), Blacksmithing(), SheepFarming(),
           WishForChildren(), DonkeyFarming(), OreDelivery(), FamilyLife(), OreTrading(), Adventure(),
           RubyDelivery(), Excavation(), Sustenance(), Housework(), SlashAndBurn(), 
           OreMineConstruction(), RubyMineConstruction()] 

