from constants import *
from Actions import *
from gameLogic import *
from Tiles import *

'''
import psyco ; psyco.jit() 
from psyco.classes import *
'''
#global counter
#counter = 0
highScore = {'score':-1000}

dwarves = {'home':['unarmed']*2,'working':[]}

history = [[]]

board = {'forest':[[[]]*4]*3, 'cave':[[[]]*4]*3, 'tiles':[StarterDwelling()]}
board['cave'][0][0] = ['starter dwelling']
board['cave'][0][1] = ['cavern']
board['cave'][1][0] = ['food']
board['cave'][2][3] = ['food']*2
board['forest'][1][0] = ['food']
board['forest'][2][3] = ['pig']
board['forest'][0][1] = ['pig']

inv = {}
for item in items: inv[item] = 0
inv.update({'food':2, })


def UCT(node, n):
    #print node['scores'], n
    return np.mean(node['scores']) + np.sqrt(2 * np.log(n)/len(node['scores']))
 
def getNewNode(tree):
    fringe = [node for node in tree if not node['fullyExplored']]
    n = sum([len(node['scores']) for node in fringe])
    #for node in tree: print node['scores'], node['gamestate']['inventory']['history']
    newNode = max(fringe, key=lambda node, n=n: UCT(node, n))
    return newNode
    
def explore(node, tree):
    if not node['fullyExplored']:
        gamestates = getOptions(node['gamestate'])
        for gamestate in gamestates:
            score = randomPlayout(gamestate, highScore)
            nodeToAdd = {'gamestate':gamestate,'scores':[score],'fullyExplored':0}
            node['scores'].append(score)
            tree.append(nodeToAdd)
    node['fullyExplored'] = 1
    

gamestate = {'actions':{a.name:[a,0,[]] for a in Actions}, 'inventory':inv, 'turn':0, 'dwarves':dwarves, 'board':board, 'history':history}
root = {'gamestate':gamestate,'scores':[],'fullyExplored':0} 
tree = [root]

#m = maximizer(11, gamestate, highScore)
#print randomPlayout(gamestate, highScore)
node = root
for t in range(1000000):
    explore(node,tree)
    node = getNewNode(tree)
        
        
        
        
        
        
        
        
        
        

