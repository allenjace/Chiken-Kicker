import random
import queue
import os

cwd = os.getcwd()

class Deck():
    def __init__(self, GameWorld):
        self.gameworld = GameWorld
        self.deck = self.create_deck()
        self.infinitedeck = self.deck.copy()
        self.shuffled_deck = []
        self.non_common_cards = []
        self.common_cards = []
        self.combos = self.combo_list()
        
        # identify all common cards
        for card_id, card_data in self.deck.items():
            if card_data[3] == "common":  # Index 3 is rarity in the original format
                self.common_cards.append(card_id)
            else:
                self.non_common_cards.append(card_id)
                
        self.og_shuffledeck = self.non_common_cards.copy()
        self.reset_deck()
        print("Deck created")
        
    def create_deck(self) -> list:
        # dictionary to describe cards
        # format: [id, name, description, card rarity, player movement = (dx,dy, ratio to shrink/expand char), enemy movement = (dx,dy, ratio), range, self dmg, enemy dmg]
        # common cards - total 6
        deck = dict()
        deck = dict()
        deck[len(deck)+1] = [1, "Move Forward", "Move Forward","common",'card images/forwards.png', [300,0,1], [0,0,1], [0,0], 0, 0] # 01
        deck[len(deck)+1] = [2, "Move Backward", "Move Backward","common",'card images/backwards.png', [-300,0,1], [0,0,1], [0,0], 0, 0] # 02
        deck[len(deck)+1] = [3, "Move Up", "Aim upwards","common",'card images/up.png',[0,-200,1], [0,0,1], [0,0], 0, 0] #03
        deck[len(deck)+1] = [4, "Move Down", "Moves down","common",'card images/down.png',[0,200,1], [0,0,1], [0,0], 0, 0] # 04
        deck[len(deck)+1] = [5, "Duck", "Duck down","common",'card images/common_card.png',[0,0,0.5], [0,0,1], [0,0], 0, 0] # 05
        deck[len(deck)+1] = [6, "Kick", "A kick aimed towards the family jewels","common",'card images/common_card.png',[0,0,1],[75,0,1], [0.5,0.5], 0, 10 ]# 06
        
        # rare cards - total 5
        deck[len(deck)+1] = [7, "Back Kick", "Happy de ume tsukushite","rare",'card images/rare_card.png',[0,0,1], [75,0,1], [0.5,0],0,15] # 07, backwards + kick 
        deck[len(deck)+1] = [8, "Roundhouse Kick", "A kick with extra knockback","rare",'card images/rare_card.png',[0,0,1], [150,0,1], [0.5,1],0,10] # 08, up + forwards + kick
        deck[len(deck)+1] = [9, "Axe Kick", "A kick with a chance to stun","rare",'card images/rare_card.png',[0,0,1], [0,0,1], [0.5,1],0,20] # 09, up + down + kick
        deck[len(deck)+1] = [10, "Knee Strike", "A quick knee","rare",'card images/rare_card.png',[0,0,1], [0,0,1], [0.5,1],0,15] # 10, up + kick
        deck[len(deck)+1] = [11, "Spin","You some kind of ballerina?","rare",'card images/rare_card.png',[0,0,1], [0,0,1], [0,0],0,0] # 11, backwards + forwards + back
        deck[len(deck)+1] = [12, "Leap","","rare",'card images/rare_card.png',[300,-100,1], [0,0,1], [0,0],0,0] # 12, up + up


        # epic cards - total 3
        deck[len(deck)+1] = [13, "Spinning Back Kick", "A powerful spinning kick","epic",'card images/epic_card.png',[0,0,1], [0,0,1], [0.5,0],0,25] #13, spin + back kick
        deck[len(deck)+1] = [14, "Flying Knee", "","epic",'card images/epic_card.png',[300,-100,1], [200,0,1], [1,0],0,30] #14, jump + forward + knee
        deck[len(deck)+1] = [15, "Tornado Kick", "Let it rip!","epic",'card images/epic_card.png',[0,0,1], [500,0,1], [1,1],0,40] # spin + roundhouse kick
        deck[len(deck)+1] = [16, "Flying Kick", "Soaring through the air feet first","epic",'card images/epic_card.png',[300,-100,1], [200,0,1], [1,1],0,25] # jump + forward + kick
        # rdm drug


        # legendary careds
        deck[len(deck)+1] = [17, "Roids", "Jump Higher, Run Faster Kick Harder","Legendary",'card images/legendary_card.png',[0,0,1],[0,0,1], [0,0], 0, 0] # add a multiplier to outgoing dmg
        deck[len(deck)+1] = [18, "Lucky Strike", "Deal double damage on your next hit","Legendary",'card images/legendary_card.png',[0,0,1],[0,0,1], [0,0], 0, 0] # add a multiplier to outgoing dmg
        
        # Make copies of non-common cards
        original_length = len(deck)
        base_cards = {k: v for k, v in deck.items() if k > 6}  # Get all non-common cards
        num_copies = 9  # We already have 1 copy, so make 9 more for total of 10
        
        for _ in range(num_copies):
            for card_id, card_data in base_cards.items():
                deck[len(deck)+1] = card_data.copy()  # Add copy with new ID
        return deck
    
    def combo_list(self):
        combos = dict()
        combos["20600"] = ["Back Kick", "Happy de ume tsukushite",1,[0,0,1], [75,0,1], [0.5,0],0,20]
        combos["30106"] = ["Roundhouse Kick", "A kick with extra knockback",1,[0,0,1], [300,0,1], [0.5,1],0,10]
        combos["30406"] = ["Axe Kick", "A kick with a chance to stun",1,[0,0,1], [150,0,1], [0.5,1],0,10]
        combos["30600"] = ["Knee Strike", "A quick knee to the chin",1,[0,0,1], [0,0,1], [0.5,1],0,15]
        combos["20102"] = ["Spin","You some kind of ballerina?",1,[0,0,1], [0,0,1], [0,0],0,0] # change to taunt?
        combos["30300"] = ["Jump","",1,[0,-30,1], [0,0,1], [0,0],0,0] # taunt?
        combos["110700"] = ["Spinning Back Kick", "A powerful spinning kick",2,[0,0,1], [0,0,1], [0.5,0],0,35]
        combos["120110"] = ["Flying Knee", "",2,[300,-100,1], [200,0,1], [1,0],0,30] 
        combos["110800"] = ["Tornado Kick", "Let it rip!",2,[0,0,1], [500,0,1], [2,1],0,40]
        combos["120106"] = ["Flying Kick", "Soaring through the air feet first",[300,-100,1], [200,0,1], [2,1],0,25]

        return combos

    def get_card_name(self, id: int) -> str:
        return self.deck[id][1]

    def get_card_description(self, id: int) -> str:
        return self.deck[id][2]
    
    def get_card_img(self, id: int) -> str:
        return os.path.join(cwd, self.deck[id][4])
    
    def get_card_file_path(self, id:int) -> str:
        return self.deck[id][4]
    
    def get_card_mvmt(self, id:int):
        return self.deck[id][5]
    
    def get_card_knockback(self, id:int):
        return self.deck[id][6]
    
    def get_card_range(self, id:int):
        return self.deck[id][7]
    
    def get_card_self_dmg(self, id:int):
        return self.deck[id][8]

    def get_card_dmg(self,id:int):
        return self.deck[id][9]
    
    def get_combo_mvmt(self, id:int):
        return self.deck[id][3]
    
    def get_combo_knockback(self, id:int):
        return self.deck[id][4]
    
    def get_combo_range(self, id:int):
        return self.deck[id][5]
    
    def get_combo_self_dmg(self, id:int):
        return self.combos[id][6]

    def get_combo_dmg(self,id:int):
        return self.combos[id][7]
        
    def get_next_card(self) -> int:
        if len(self.shuffled_deck) == 0:
            self.reset_deck()
        return self.shuffled_deck.pop(0)
    
    def reset_deck(self):
        self.shuffled_deck = self.non_common_cards.copy()
        random.shuffle(self.shuffled_deck)
        print("Deck reset and reshuffled")

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
