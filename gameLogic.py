from constants import *



def placeTile(inventory, tile):
    pass

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


def maximizer(actions, turns, inventory, highScore):
    #global counter
    
    if turns == 0:
        s = score(inventory)
        if s > highScore['score']:
            os.system('cls')
            print inventory
            print s
            highScore['score'] = s
            highScore['inv'] = inventory
        return inventory
    if not inventory['dwarves'][0]:
        inventory['dwarves'][0] = inventory['dwarves'][1]
        inventory['dwarves'][1] = 0
        update(actions, inventory)
        return maximizer(actions, turns-1, inventory, highScore)
    #if not inventory['dwarves'][1]:
        
    
    #counter += 1
    #print turns, inventory
    #raw_input()
    
    
    results = []
    random.shuffle(actions)
    for i in range(len(actions)):
        if not actions[i].inUse:
            newInv, newActions = copy.deepcopy(inventory), copy.deepcopy(actions)
            
            newActions[i].use(newInv)
            results.append(maximizer(newActions, turns, newInv, highScore))
    
    res = sorted(results, key=lambda x: score(x))
    return res[-1] 