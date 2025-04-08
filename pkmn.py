import math
import json
import random

with open("mons_db.json") as f:
    db = json.load(f)[0]

db_1 = db["wiki_garchomp_1"]
db_2 = db["lando_t"]

with open("type_chart.json") as f:
    tchart = json.load(f)[0]

class Species:
    def __init__(self,name,hp=5,atk=5,de=5,spa=5,spd=5,spe=5,types=None,abilities=None):
        self.name = name
        self.bhp = hp
        self.batk = atk
        self.bde = de
        self.bspa = spa
        self.bspd = spd
        self.bspe = spe
        self.btypes = types

    def __str__(self):
        return(f"{self.name}\n{self.btypes}\nHP: {self.bhp}\nAtk: {self.batk}\nDef: {self.bde}\nSpa: {self.bspa}\nSpd: {self.bspd}\nSpe: {self.bspe}")

def getFactors(target,user,move,crit=False):
    type_factor = 1
    crit_factor = 1
    stab_factor = 1
    for t in target.types:
        #print(t)
        if move.types.lower() in tchart:
            if t.lower() in tchart[move.types.lower()]:
                type_factor *= tchart[move.types.lower()][t.lower()]
                
    if type_factor > 1:
        print("It's super effective!")
    elif type_factor < 1 and type_factor > 0:
        print("It's not very effective...")
    elif type_factor == 0:
        print(f"It doesn't affect {target.name}...")
    if crit:
        print("A critical hit!")
        crit_factor = 1.5
    utypes = []
    for t in user.types: utypes.append(t.lower())
    if move.types.lower() in utypes:
        stab_factor = 1.5
        #print(1)
    if  user.is_tera:
        #print(user.tera.lower(),move.types.lower())
        if user.tera.lower() == move.types.lower():
            #print(2)
            stab_factor += 0.5
    factors = [
            random.randint(85,100)/100,
            type_factor,
            crit_factor,
            stab_factor
        ]
    
    print(factors)
    return(factors)

def importMon(dbd={}):
    iname = "MissingNo"
    ilvl = 100
    itypes = []
    ibss = (5,5,5,5,5,5)
    ievs = (0,0,0,0,0,0)
    iivs = (0,0,0,0,0,0)
    inature = (0,0)
    iability = ""
    iitem = ""
    
    if "name" in dbd:
        iname = dbd["name"]
    if "lvl" in dbd:
        ilvl = dbd["lvl"]
    if "types" in dbd:
        itypes = dbd["types"]
    if "bss" in dbd:
        ibss = dbd["bss"]
    if "evs" in dbd:
        ievs = dbd["evs"]
    if "ivs" in dbd:
        iivs = dbd["ivs"]
    if "nature" in dbd:
        inature = dbd["nature"]
    if "ability" in dbd:
        iability = dbd["ability"]
    if "item" in dbd:
        iitem = dbd["item"]

    return(Mon(name=iname,lvl=ilvl,types=itypes,bss=ibss,evs=ievs,ivs=iivs,nature=inature,ability=iability,item=iitem))

def statCalc(stat=0,base=0,ev=0,iv=0,lvl=100,nature=(0,0)):
    ostat = float(base)
    if stat == 0:
        ## HP has a different calculation
        ostat *= 2
        ostat += iv
        ostat += abs(math.floor(ev/4))
        ostat *= lvl
        ostat = math.floor(ostat/100)
        ostat = abs(ostat) + lvl + 10
    else:
        ostat *= 2
        ostat += iv
        ostat += abs(math.floor(ev/4))
        ostat *= lvl
        ostat /= 100
        ostat = abs(math.floor(ostat)) + 5
        if nature[0] == stat:
            ## First index is the stat ID that gets boosted
            ostat = math.floor(ostat*1.1)
        if nature[1] == stat:
            ## Second index is the stat ID that gets nerfed
            ostat = ostat*90
            ostat = math.floor(ostat/100)
    return(abs(int(math.floor(ostat))))
        
#print(statCalc(0,108,74,24,78,(1,3)))
#print(statCalc(1,130,190,12,78,(1,3)))
#print(statCalc(2,95,91,30,78,(1,3)))
#print(statCalc(3,80,48,16,78,(1,3)))

class Mon:
    def __init__(self,types=[],bss=(5,5,5,5,5,5),ability="",item="",nature=(0,0),lvl=100,evs=(0,0,0,0,0,0),name="MissingNo",ivs=(31,31,31,31,31,31)):
        self.name = name

        self.lvl = lvl
        self.evs = evs
        self.ivs = ivs
        self.nature = nature
        self.item = item
        self.ability = ability

        ## Move:PP
        self.moves = {}

        ## HP-Atk-Def-SpA-SpD-Acc-Eva-Crit (HP does nothing)
        self.sm = [1,1,1,1,1,1,1,1]

        ## Base Stat Spread -- Unmarked in attributes but 0 is HP, 1 is Atk, 2 is Def, 3 is SpA, 4 is SpD, 5 is Spe
        self.bss = bss
        ## final Stat Spread
        self.ss = list(bss)
        self.hp = self.ss[0]
        ind = 0
        for s in self.bss:
            #print(ind,s)
            self.ss[ind] = statCalc(ind,s,self.evs[ind],self.ivs[ind],self.lvl,self.nature)
            ind += 1
        self.types = types
        if type(types) == str:
            self.types = [types]

        ## What Tera Type mon has
        self.tera = "Normal"
        self.is_tera = False

    def use_move(self,move,target):
        if self.moves[move] > 0:
            self.moves[move] -= 1
            move.calc(self,target)
        else:
            print(f"{move.name} is out of PP!")
        
    def add_move(self,move):
        self.moves[move] = move.pp
        
    def __str__(self):
        if len(self.types) == 1:
            typestr = self.types[0]
        else:
            typestr = f"{self.types[0]}/{self.types[1]}"
        if self.item:
             itemstr = f" @ {self.item}"
        else:
            itemstr = ""
        return(f"{self.name}{itemstr}\n{typestr}\nHP: {self.ss[0]}\nAtk: {self.ss[1]}\nDef: {self.ss[2]}\nSpA: {self.ss[3]}\nSpD: {self.ss[4]}\nSpe: {self.ss[5]}")

class Move:
    def __init__(self,types="Normal",power=0,acc=100,pp=5,cat=1,name="Splash",tdef=None):
        self.types = types
        self.power = power
        self.acc = acc
        self.pp = pp
        self.name = name
        ## Category: 1 for physical, 2 for body press, 3 for special
        self.cat = cat
        self.tdef = 2
        if self.cat == 3:
            self.tdef = 4
        ## Defensive stat that target uses
        if tdef:
            self.tdef = tdef

    def __str__(self):
        return(self.name)

    def calc(self,user,target):
        ## sm is Stat Mods, indexed HP-Atk-Def-SpA-SpD-Spe-Acc-Eva-Crit (HP does nothing)
        ## NOTE: add crit chance modifiers vvv
        print(f"{user.name} used {self.name}!")
        if target.hp > 0:
            crit = random.randint(1,24) == 1
            factors = getFactors(target,user,self,crit)
            uatk = user.ss[self.cat] * user.sm[self.cat]
            udef = target.ss[self.tdef]
        #print(udef)
            if random.randint(1,100) <= self.acc*user.sm[6]:
                dmg = 2*user.lvl/5
                dmg += 2
                dmg *= self.power
            ## NOTE: add that if either of these are >255, divde by four and round down to both
                dmg *= uatk/udef
                dmg /= 50
                dmg += 2
                dmg = round(dmg)
                for f in factors:
                    dmg = round(dmg*f)
                target.hp -= dmg
                if target.hp < 0:
                    dmg += target.hp
                    target.hp = 0
                print(f"{target.name} lost {round(dmg/target.ss[0]*100,1)}% of its health!")
            else:
                print(f"{target.name} avoided the attack!")
        else:
            print("But it failed!")
                
mon_1= Mon(name="Pecharunt",types=["ghost","Fire"],bss=(88,88,160,88,88,88),ivs=(31,0,31,31,31,31),evs=(252,0,4,0,0,252),lvl=100,nature=(5,1))
mon_2 = Mon(name="the cooler Pecharunt",types=["Poison","Ghost"],bss=(88,88,160,88,88,88),ivs=(31,0,31,31,31,31),evs=(252,0,4,0,0,252),lvl=100,nature=(5,1))

#mon_1 = importMon(db_1)
print(mon_1)
#mon_1.hp = 10
print()
print(mon_2)

TACKLE = Move(types="Water",power=80,cat=3,name="the cooler Tackle",acc=90)
#print(TACKLE)

mon_2.add_move(TACKLE)
#mon_2.add_move(Move(types="Ghost",power=40,cat=3,name="the cooler Tackle",acc=90))

mon_2.is_tera = False

mon_2.tera = "GHOST"
mon_2.use_move(TACKLE,mon_1)

#TACKLE.calc(mon_2,mon_1)


