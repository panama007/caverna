import random, copy, time, os, numpy as np

totalRounds = 11

buildingItems = ['rock', 'ore', 'wood', 'ruby', 'food', 'gold']
plants = ['wheat', 'vegetable']
farmAnimals = ['sheep', 'donkey', 'pig', 'cow']]
animals = ['dog'] + farmAnimals
items = buildingItems + plants + animals

def cls():
    os.system('cls' if os.name=='nt' else 'clear')
