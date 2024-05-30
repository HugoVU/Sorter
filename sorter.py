import pandas as pd 
import numpy as np

df = pd.read_csv('gegevens.csv', delimiter=';')
df = df[['Voor- en achternaam', 'Welke kantoren hebben jouw voorkeur voor de workshops? (maximaal 5 kantoren mogelijk)']] 
df.columns = ['name', 'choices']

df.to_csv('testa.csv', index=False)
df = pd.read_csv('testa.csv')

preferences = df['choices'].str.split(',', expand=True).apply(lambda x: x.str.strip())

# 5 rounds in total
slots = {
    1: {
        "Linklaters": [],
        "PwC": [],
        "BDO": [],
        "Meijburg & Co": [],
        "Belastingdienst": [],
    },
    2: {
        "Stibbe": [],
        "PwC": [],
        "Baker McKenzie": [],
        "Meijburg & Co": [],
        "Pereria": [],
    },
    3: {
        "Mazars": [],
        "Deloitte": [],
        "Bird & Bird": [],
        "Grant Thornton": [],
        "DLA Piper": [],
    },
    4: {
        "Van Doorne": [],
        "EY": [],
        "AKD": [],
        "Baker Tilly": [],
        "CROP": [],
    },
    5: {
        "Loyens & Loeff": [],
        "Houthoff": [],
        "PKF Wallast": [],
        "Dentons": [],
        "RSM": [],
    },
}

# If no priority is given, these slots will be filled first
priorities = {
    1: ['Linklaters', 'BDO'],
    2: ['Pereira'],
    3: ['Grant Thornton'],
    4: ['CROP', 'Baker Tilly'],
    5: ['RSM', 'PKF']
}

import pprint 

# Overlapping locations, students cannot be in the same location in consecutive slots
overlap = ['PwC', 'Meijburg & Co']

for slot in slots: 
    for student, choices in df.iterrows():
        assigned = False
        priorityAssigned = False
        for i in range(len(preferences.columns)):
            if preferences[i][student] in slots[slot]:
                if preferences[i][student] in overlap and slot > 1:
                    if df['name'][student] in slots[slot-1][preferences[i][student]]:
                        print(f"{df['name'][student]} is already assigned to {preferences[i][student]} in slot {slot-1}")
                        continue
                    
                if preferences[i][student] in priorities[slot] and not priorityAssigned:
                    if len(slots[slot][preferences[i][student]]) < 18:
                        
                        slots[slot][preferences[i][student]].append(df['name'][student])
                        priorityAssigned = True
                        break
                
                if len(slots[slot][preferences[i][student]]) < 18 and not assigned and not priorityAssigned:
                    slots[slot][preferences[i][student]].append(df['name'][student])
                    assigned = True
                    break

        if not assigned and not priorityAssigned and not pd.isnull(df['name'][student]):
            min_occupied = min(slots[slot], key=lambda x: len(slots[slot][x]))
            while(min_occupied in overlap and slot > 1):
                if df['name'][student] in slots[slot-1][min_occupied]:
                    min_occupied = min(slots[slot], key=lambda x: len(slots[slot][x]) if x != min_occupied else np.inf)
                else:
                    break
                    
            if len(slots[slot][min_occupied]) < 18:
                slots[slot][min_occupied].append(df['name'][student])            
                assinged = True
            
                
pprint.pprint(slots)

for slot in slots:
    print(f"\nSlot {slot}")
    for location in slots[slot]:
        print(f"{location}: {slots[slot][location]}")

with open('assignments.csv', 'w') as f:
    for slot in slots:
        f.write(f"\nSlot {slot}\n")
        for location in slots[slot]:
            f.write(f"{location}: {slots[slot][location]}\n")
