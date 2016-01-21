from constants import *

def canNewDwarf(gamestate):
    n = sum(len(d) for d in gamestate['dwarves'].values())
    if n < 5:
        return 1
    
def strength(dwarf):
    if dwarf == 'unarmed':
        return 0
    else: 
        return int(dwarf)

def expedition(gamestate, n):
    return [copy.deepcopy(gamestate)]

def update(gamestate):
    l = list(gamestate['dwarves']['working'])
    l = ['unarmed' if elem == 'baby' else elem for elem in l]
    l.sort(key=strength)
    gamestate['dwarves']['home'] = l
    gamestate['dwarves']['working'] = []
    for action in gamestate['actions'].values():
        action[1] = 0
        n = len(action[2])
        if n >= 6: action[2] = []
        elif n: action[2] += action[0].accumulate[1]
        else: action[2] += action[0].accumulate[0]
    gamestate['turn'] += 1
    gamestate['history'].append([])

def score(gamestate):
    res = 0
    for animal in animals:
        if gamestate['inventory'][animal] == 0:
            res -= 2
        else:
            res += gamestate['inventory'][animal]
    res += gamestate['inventory']['vegetable']
    res += (gamestate['inventory']['wheat']+1)/2
    #print gamestate['dwarves']
    res += sum([len(l) for l in gamestate['dwarves'].values()])
    res += gamestate['inventory']['ruby']
    res += gamestate['inventory']['gold']
    for tile in gamestate['board']['tiles']:
        res += tile.points(gamestate)
    
    return res

def getOptions(gamestate):
    if gamestate['turn'] == totalRounds:
        return []
    if not gamestate['dwarves']['home']:
        update(gamestate)
        return getOptions(gamestate)
    options = []
    for [action,inUse,items] in gamestate['actions'].values():
        if not inUse:
            newGamestate = copy.deepcopy(gamestate)
            newGamestates = action.use(newGamestate)
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
            cls()
            print 'New Highscore : %i\n\n'%s
            print gamestate['history'], '\n\n'
            print gamestate['dwarves']
            highscore['score'] = s
            highscore['gamestate'] = gamestate
        return s
