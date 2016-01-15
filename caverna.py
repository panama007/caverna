from constants import *
from Actions import *
from gameLogic import *

'''
import psyco ; psyco.jit() 
from psyco.classes import *
'''
global counter
counter = 0



inv = {}
for item in items: inv[item] = 0
inv.update({'dwarves':[2,0], 'food':1, 'history' :[], 'forest':[[[]]*4]*3, 'cave':[[[]]*4]*3, 'tiles':[]})
inv['cave'][0][0] = ['dwelling']
inv['cave'][0][1] = ['cavern']
inv['cave'][1][0] = ['food']
inv['cave'][2][3] = ['food']*2
inv['cave'][1][0] = ['food']
inv['cave'][2][3] = ['pig']
inv['cave'][0][1] = ['pig']

    
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
        
        
        
        
        
        
        
        
        
        

