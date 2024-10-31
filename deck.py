import random
import queue

class Deck():
    def __init__(self) -> None:
        self.deck = self.create_deck()
        self.combos = self.combo_list()
        self.sections = []
        print("deck created")
        
    def create_deck(self) -> list:
        # dictionary to describe cards
        # format: [id, name, description, card rarity, player movement = (dx,dy, ratio to shrink/expand char), enemy movement = (dx,dy, ratio), range, self dmg, enemy dmg]
        # common cards - total 6
        deck = dict()
        deck[len(deck)+1] = [1, "Forward", "Move Forwards",0, [30,0,1], [0,0,1], [0,0], 0, 0] # 01
        deck[len(deck)+1] = [2, "Backward", "Move Backwards",0, [-30,0,1], [0,0,1], [0,0], 0, 0] # 02
        deck[len(deck)+1] = [3, "Up", "Aim upwards",0,[0,-30,1], [0,0,1], [0,0], 0, 0] #03
        deck[len(deck)+1] = [4, "Move Down", "Moves down",0,[0,30,1], [0,0,1], [0,0], 0, 0] # 04
        deck[len(deck)+1] = [5, "Duck", "Duck down",0,[0,0,0.5], [0,0,1], [0,0], 0, 0] # 05
        deck[len(deck)+1] = [6, "Kick", "A kick aimed towards the family jewels",0,[0,0,1],[10,0,1], [0.5,0.5], 0, 5] # 06
        
        # rare cards - total 5
        deck[len(deck)+1] = [7, "Back Kick", "Happy de ume tsukushite",1,[0,0,1], [0,0,1], [0.5,0.5],0,10] # 07, backwards + kick 
        deck[len(deck)+1] = [8, "Roundhouse Kick", "A kick with extra knockback",1,[0,0,1], [0,0,1], [0.5,1],0,10] # 08, up + forwards + kick
        deck[len(deck)+1] = [9, "Axe Kick", "A kick with a chance to stun",1,[0,0,1], [0,0,1], [0.5,1],0,10] # 09, up + down + kick
        deck[len(deck)+1] = [10, "Knee Strike", "A quick knee to the chin",1,[0,0,1], [0,0,1], [0.5,1],0,10] # 10, up + kick
        deck[len(deck)+1] = [11, "Spin","You some kind of ballerina?",1,[0,0,1], [0,0,1], [0,0],0,0] # 11, backwards + forwards + back
        deck[len(deck)+1] = [12, "Jump","",1,[0,-30,1], [0,0,1], [0,0],0,0] # 12, up + up


        # epic cards - total 3
        deck[len(deck)+1] = [13, "Spinning Back Kick", "A powerful spinning kick",2,[0,0,1], [0,0,1], [0.5,0],0,20] #13, spin + back kick
        deck[len(deck)+1] = [14, "Flying Knee", "",2,[20,15,1], [0,0,1], [0.5,0.5],0,20] #14, jump + forward + knee
        deck[len(deck)+1] = [15, "Tornado Kick", "Let it rip!",2,[0,0,1], [0,0,1], [0.5,1],0,20] # spin + roundhouse kick
        deck[len(deck)+1] = [16, "Flying Kick", "Soaring through the air feet first",[-20,-15,1], [0,0,1], [0.5,0.5],0,10] # jump + forward + kick
        # rdm drug


        # legendary careds
        deck[len(deck)+1] = [17, "Roids", "Jump Higher, Run Faster Kick Harder",3] # add a multiplier to outgoing dmg
        

        return deck
    
    def combo_list(self):
        combos = dict()
        combos["20600"] = [7,"Back Kick", "Happy de ume tsukushite",1,[0,0,1], [0,0,1], [0.5,0.5],0,15]
        combos["30106"] = [8,"Roundhouse Kick", "A kick with extra knockback",1,[0,0,1], [0,0,1], [0.5,1],0,15]
        combos["30406"] = [9,"Axe Kick", "A kick with a chance to stun",1,[0,0,1], [0,0,1], [0.5,1],0,15]
        combos["30600"] = [10,"Knee Strike", "A quick knee to the chin",1,[0,0,1], [0,0,1], [0.5,1],0,15]
        combos["20102"] = [11,"Spin","You some kind of ballerina?",1,[0,0,1], [0,0,1], [0,0],0,0] # change to taunt?
        combos["30300"] = [12,"Jump","",1,[0,-30,1], [0,0,1], [0,0],0,0] # taunt?
        combos["110700"] = [13,"Spinning Back Kick", "A powerful spinning kick",2,[0,0,1], [0,0,1], [0.5,0],0,25]
        combos["120110"] = [14,"Flying Knee", "",2,[20,15,1], [0,0,1], [0.5,0.5],0,25]
        combos["110800"] = [15,"Tornado Kick", "Let it rip!",2,[0,0,1], [0,0,1], [0.5,1],0,25]
        combos["120106"] = [16,"Flying Kick", "Soaring through the air feet first",[-20,-15,1], [0,0,1], [0.5,0.5],0,25]
        

        return combos

    def get_card_name(self, id: int) -> str:
        return self.deck[id][0]
    
    def get_card_movement(self, id:int) -> list:
        return self.deck[id][1]
    
    def get_card_attack(self, id:int) -> list:
        return self.deck[id][2]
    
    def get_card_description(self, id:int) -> str:
        return self.deck[id][3]
    
    def get_card_img(self, id:int) -> str:
        return self.deck[id][4]

    # takes in n number of cards to draw and time left in game, will return n sized list
    def fill_hand(self, n:int, time:int) -> list:
        cards_drawn = []
        for i in range(n):
            bucket_choice = random.randrange(1,100)
            # before 3:30, chances for C/R/E/L -> 60/35/5/0
            if time > 120:
                if bucket_choice < 70:
                    cards_drawn.append(self.draw_card(7,12))
                elif bucket_choice < 95:
                    cards_drawn.append(self.draw_card(13,16))
                else:
                    cards_drawn.append(self.draw_card(17,17))
            # between 2:00 and 3:30 chances for C/R/E/L -> 45/40/10/1
            elif time > 60:
                if bucket_choice < 55:
                    cards_drawn.append(self.draw_card(7,12))
                elif bucket_choice < 90:
                    cards_drawn.append(self.draw_card(13,16))
                else:
                    cards_drawn.append(self.draw_card(17,17))
            # between 2:00 and 3:30 chances for C/R/E/L -> 30/40/25/5
            else:
                if bucket_choice < 40:
                    cards_drawn.append(self.draw_card(7,12))
                elif bucket_choice < 85:
                    cards_drawn.append(self.draw_card(13,16))
                else:
                    cards_drawn.append(self.draw_card(17,17))
        return cards_drawn

    def draw_card(self, lower:int, upper:int) -> int:
        return self.deck[random.randint(lower, upper)]
    
# checks combo if game queue is in the form of a FIFO queue
    def check_combo(self, pqueue):
        multiplier = 10000
        combo_id = 0
        temp = []
        while not(pqueue.empty()):
            i = pqueue.get()
            combo_id += i[0] * multiplier
            multiplier = multiplier / 100
            temp.append(i)
        combo_id = str(int(combo_id))
        print(combo_id)
        if combo_id in self.combos.keys():
            print("Combo made")
            return [self.combos[combo_id]]
        return temp

def check_combo_l(l:list):
    multiplier = 10000
    combo_id = 0
    for i in l:
        combo_id += i*multiplier
        multiplier /= 100
    return combo_id
