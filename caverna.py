import random, copy, time
'''
import psyco ; psyco.jit() 
from psyco.classes import *
'''
counter = 0

building_items = ['rock', 'ore', 'wood', 'ruby', 'food']
plants = ['wheat', 'vegetable']
animals = ['dog', 'sheep', 'donkey', 'pig', 'cow']
items = building_items + plants + animals

inv = {'dwarves':[2,0], 'food':1, 'history' :[]}

for item in items: inv[item] = 0

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
    
    def _use(self, inventory):
        inventory['dwarves'][0] -= 1
        inventory['dwarves'][1] += 1
        self.inUse = 1
        for key in self.itemDic.keys():
            inventory[key] += self.itemDic[key]
            self.itemDic[key] = 0
        for item in self.pickup:
            inventory[item] += 1 
        inventory['history'].append(self.name)

Actions = [ActionSpace(name, acc, pickup) for (name, acc, pickup) in 
            [('Excavation',[['rock']]*2,[]), 
             ('Logging', [['wood']*3,['wood']], []),
             ('Wood gathering', [['wood']]*2, []), 
             ('Ore mining', [['ore']*2,['ore']], []), 
             ('Sustenance', [['food']]*2, ['wheat']),
             ('Ruby mining', [['ruby']]*2, []), 
             ('Housework', [[],[]], ['dog']), 
             ('Slash-and-burn', [[],[]], []), 
             ('Blacksmithing', [[],[]], []),
             ('Sheep Farming', [['sheep']]*2, []),
             ('Ore mine construction', [[],[]], []), 
             ('Wish for children', [[],[]], []),             
             ('Donkey farming', [['donkey']]*2, []), 
             ('Ruby mine construction', [[],[]], []), 
             ('Ore delivery', [['ore','rock']]*2, []), 
             ('Family life', [[],[]], []), 
             ('Ore trading', [[],[]], []), 
             ('Adventure', [[],[]], []), 
             ('Ruby delivery', [['ruby']*2,['ruby']], [])]]



def update(actions, inventory):
    for action in actions:
        action._update()	      

def score(inventory):
    res = 0
    for animal in animals:
        if inventory[animal] == 0:
            res -= 2
        else:
            res += inventory[animal]
    res += inventory['vegetable']
    res += (inventory['wheat']+1)/2
    res += sum(inventory['dwarves'])
    res += inventory['ruby']
    
    return res


def maximizer(actions, turns, inventory):
    global counter
    
    if turns == 0:
        return inventory
    if not inventory['dwarves'][0]:
        inventory['dwarves'][0] = inventory['dwarves'][1]
        inventory['dwarves'][1] = 0
        return maximizer(actions, turns-1, inventory)
    if not inventory['dwarves'][1]:
        update(actions, inventory)
    
    counter += 1
    #print turns, inventory
    #raw_input()
    
    
    results = []
    for i in range(len(actions)):
        if not actions[i].inUse:
            newInv, newActions = copy.deepcopy(inventory), copy.deepcopy(actions)
            
            newActions[i]._use(newInv)
            results.append(maximizer(newActions, turns, newInv))
    
    res = sorted(results, key=lambda x: score(x))
    return res[-1] 
    
'''
for i in range(3):
    update(Actions)
    [Actions[i]._use(inv) for i in [random.randint(0,4) for j in range(2)]]
'''
#print inv, score(inv)
   
#print 'test'
for j in range(2,len(Actions)):  
    for i in range(4):
        counter = 0
        newActions = copy.deepcopy(Actions)
        newInv = copy.deepcopy(inv)
        t0 = time.time()
        m = maximizer(newActions[:j], i+1, newInv)
        t1 = time.time()
        print "%i action tiles\t%i turns\t%i calls \t%i pts\t%0.05f seconds"%(j,i+1, counter, score(m), t1-t0)   

#print Actions[2].itemDic
        
        
        
        
        
        
        
        
        
        

