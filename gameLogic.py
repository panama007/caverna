from constants import *


def update(gamestate):
    gamestate['inventory']['dwarves']['home'] = gamestate['inventory']['dwarves']['working']
    gamestate['inventory']['dwarves']['working'] = 0
    for action in gamestate['actions']:
        action._update()	      
    gamestate['turn'] += 1
    gamestate['inventory']['history'].append([])

def score(gamestate):
    res = 0
    for animal in animals:
        if gamestate['inventory'][animal] == 0:
            res -= 2
        else:
            res += gamestate['inventory'][animal]
    res += gamestate['inventory']['vegetable']
    res += (gamestate['inventory']['wheat']+1)/2
    res += sum(gamestate['inventory']['dwarves'].values())
    res += gamestate['inventory']['ruby']
    
    return res

def getOptions(gamestate):
    if gamestate['turn'] == totalRounds:
        return []
    if not gamestate['inventory']['dwarves']['home']:
        update(gamestate)
        return getOptions(gamestate)
    options = []
    for i in range(len(gamestate['actions'])):
        if not gamestate['actions'][i].inUse:
            newGamestate = copy.deepcopy(gamestate)
            newGamestates = newGamestate['actions'][i].use(newGamestate)
            options += newGamestates
    return options

# score
def randomPlayout(gamestate, highscore):
    gamestates = getOptions(gamestate)
    if gamestates:
        return randomPlayout(random.choice(gamestates), highscore)
    else:
        s = score(gamestate)
        if s > highscore['score']:
            print 'New Highscore : %i'%s
            print gamestate['inventory']['history']
            highscore['score'] = s
            highscore['gamestate'] = gamestate
        return s
    
    
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
    if not inventory['dwarves']['home']:
        inventory['dwarves']['home'] = inventory['dwarves']['working']
        inventory['dwarves']['working'] = 0
        update(actions, inventory)
        return maximizer(actions, turns-1, inventory, highScore)
    #if not inventory['dwarves']['working']:
        
    
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