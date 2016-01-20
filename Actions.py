from constants import *
from gameLogic import *



class ActionSpace:
    def __init__(self, name, accumulate=[[],[]], pickup=[]):
        self.name = name
        self.accumulate = accumulate
        self.pickup = pickup

    def _use(self, gamestate):
        d = gamestate['dwarves']['home'].pop(0)
        gamestate['dwarves']['working'].append(d)
        gamestate['actions'][self.name][1] = 1
        for item in gamestate['actions'][self.name][2]:
            gamestate['inventory'][item] += 1
        gamestate['actions'][self.name][2] = []
        for item in self.pickup:
            gamestate['inventory'][item] += 1 
        gamestate['history'][-1].append(self.name)

    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return [newGamestate]

# TODO make sure all Actions are making new copies of gamestates before acting on them
class Logging(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Logging', [['wood']*3,['wood']])
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return expedition(newGamestate,1)
        
class WoodGathering(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Wood gathering', [['wood']]*2)
        
class OreMining(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore mining', [['ore']*2,['ore']])
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        newGamestate['inventory']['ore'] += 2 * sum(row.count('ore mine') for row in newGamestate['board']['cave'])
        return [newGamestate]

class RubyMining(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ruby mining', [['ruby']]*2)
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        if sum(row.count('ruby mine') for row in newGamestate['board']['cave']): newGamestate['inventory']['ruby'] += 1 
        return [newGamestate]
        
class Blacksmithing(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Blacksmithing')
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        states = []
        for i in range(newGamestate['inventory']['ore']):
            otherNewGamestate = copy.deepcopy(newGamestate)
            otherNewGamestate['inventory']['ore'] -= i+1
            otherNewGamestate['dwarves']['working'][-1] = str(i+1)
            states.append(otherNewGamestate)
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
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        states = []
        if canNewDwarf(newGamestate):
            otherNewGamestate = copy.deepcopy(newGamestate)
            otherNewGamestate['dwarves']['working'].append('baby')
            #print newGamestate['inventory']['dwarves']['working']
            states.append(otherNewGamestate)
        states += self.placeDwelling(newGamestate)
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
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        newGamestate['inventory']['ore'] += 2 * sum(row.count('ore mine') for row in newGamestate['board']['cave'])
        return [newGamestate]

class FamilyLife(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Family life')

class OreTrading(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore trading')
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        states = []
        for i in range(max(newGamestate['inventory']['ore']/2, 3)):
            otherNewGamestate = copy.deepcopy(newGamestate)
            otherNewGamestate['inventory']['ore'] -= 2*(i+1)
            otherNewGamestate['inventory']['gold'] += 2*(i+1)
            otherNewGamestate['inventory']['food'] += (i+1)
            states.append(otherNewGamestate)
        return states
        
class Adventure(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Adventure')

class RubyDelivery(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ruby delivery', [['ruby']*2,['ruby']])
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        if sum(row.count('ruby mine') for row in newGamestate['board']['cave'])/2: newGamestate['inventory']['ruby'] += 1 
        return [newGamestate]

class Excavation(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Excavation',[['rock']]*2)
    def placeCaveTwin(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return self.placeCaveTwin(newGamestate)
        
class Sustenance(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Sustenance', [['food']]*2, ['wheat'])
    def placeForestTwin(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return self.placeForestTwin(newGamestate)
        
class Housework(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Housework', [[],[]], ['dog'])
    def placeFurnishing(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return self.placeFurnishing(newGamestate)
        
class SlashAndBurn(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Slash-and-burn')
    def plantCrops(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return self.plantCrops(newGamestate)
        
class OreMineConstruction(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ore mine construction')
    def placeOreMine(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return self.placeOreMine(newGamestate)        
        
class RubyMineConstruction(ActionSpace):
    def __init__(self):
        ActionSpace.__init__(self, 'Ruby mine construction')
    def placeRubyMine(self, gamestate):
        return [copy.deepcopy(gamestate)]
    def use(self, gamestate):
        newGamestate = copy.deepcopy(gamestate)
        self._use(newGamestate)
        return self.placeRubyMine(newGamestate)        

Actions = [Logging(), WoodGathering(), OreMining(), RubyMining(), Blacksmithing(), SheepFarming(),
           WishForChildren(), DonkeyFarming(), OreDelivery(), FamilyLife(), OreTrading(), Adventure(),
           RubyDelivery(), Excavation(), Sustenance(), Housework(), SlashAndBurn(), 
           OreMineConstruction(), RubyMineConstruction()] 

