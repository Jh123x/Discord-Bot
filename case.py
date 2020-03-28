import random
class Collection:
    def __init__(self, name, items):
        self.name = name
        self.items = items #Dictionary of {rarity: [items]}

    def open(self):
        decimal = random.randint(0,1000)
        if(decimal < 7992 and ('dblue' in self.items)):
            weapon = random.choice(self.items['dblue'])
        elif(decimal < 9590 and ('purple' in self.items)):
            weapon = random.choice(self.items['purple'])
        elif(decimal < 9910 and ('pink' in self.items)):
            weapon = random.choice(self.items['pink'])
        elif(decimal < 9974 and ('red' in self.items)):
            weapon = random.choice(self.items['red'])
        elif(('yellow' in self.items)):
            weapon = random.choice(self.items['yellow'])
        else:
            return "There are no items in this case yet"

        st = random.randint(0,9)
        if(st < 1):
            return "Stattrack " + weapon
        else:
            return weapon

    def get_name(self):
        return self.name

class Simulator():
    def __init__(self):
        self.load()

    def load_weapons(self):
        txts = ['blue', 'dblue', 'pink', 'purple', 'red']
        d = {}
        for color in txts:
            with open('csgo/'+color+'.txt', 'r') as file:
                try:
                    data = file.readlines()
                except:
                    continue
                names = list(map(lambda x: x.strip(),data[::3]))
                collections = list(map(lambda x: x.strip(),data[2::3]))
                for i in range(len(names)):
                    name = names[i].strip()
                    collection = collections[i].strip()
                    if(collection not in d):
                        d[collection] = {}
                    if(color not in d[collection]):
                        d[collection][color] = []

                    d[collection][color].append(name)
        return d

    def load(self):
        '''Main function for the case simulator'''
        cases = "Operation Bravo Case • Operation Phoenix Weapon Case • Operation Breakout Weapon Case • Operation Vanguard Weapon Case • Falchion Case • Operation Wildfire Case • Operation Hydra Case • Shattered Web Case Winter • Huntsman Weapon Case • Chroma Case • Chroma 2 Case • Shadow Case • Revolver Case • Chroma 3 Case • Gamma Case • Gamma 2 Case • Glove Case • Spectrum Case • Spectrum 2 Case • Clutch Case • Horizon Case • Danger Zone Case • Prisma Case • CS20 Case" .split("•")
        cases = list(map(lambda x: x.strip(),cases))
        d = self.load_weapons()
        c = {}

        for k,l in d.items():
            for case in cases:
                case = case.split(' ')
                if(case[0] == 'Operation'):
                    case = case[1]
                else:
                    case = case[0]
                
                if(case in k):
                    c[case.lower()] = (Collection(k,l))
                    break
        self.collection = c

    def collections(self):
        return list(self.collection.keys())

    def get(self):
        return self.collection
        

def main():
    sim = Simulator()
    c = sim.get()
    case = input('What case will you like to open: ')
    print(c[case.lower()].open())

if(__name__ == '__main__'):
    main()