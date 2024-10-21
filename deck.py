import random
import queue

class Deck():
    def __init__(self) -> None:
        self.deck = self.create_deck()
        self.sections = []
        print("deck created")
        
    def create_deck(self) -> list:
        # dictionary to describe cards
        # format: [name, description, card rarity, player movement = (dx,dy, ratio to shrink/expand char), enemy movement = (dx,dy, ratio), range, self dmg, enemy dmg]
        # deck[len(deck)+1] = ["", "", (0,0,1), (0,0,1), 0, 0]
        # common cards - total 6
        deck = dict()
        deck[len(deck)+1] = ["Forward", "Moves Left",0, [5,0,1], [0,0,1], [0,0], 0, 0]
        deck[len(deck)+1] = ["Backward", "Moves right",0, [-5,0,1], [0,0,1], [0,0], 0, 0]
        deck[len(deck)+1] = ["Jump", "Jump",0,[0,-15,1], [0,0,1], [0,0], 0, 0]
        deck[len(deck)+1] = ["Move Down", "Moves down",0,[0,15,1], [0,0,1], [0,0], 0, 0]
        deck[len(deck)+1] = ["Duck", "Duck down",0,[0,0,0.5], [0,0,1], [0,0], 0, 0]
        deck[len(deck)+1] = ["Kick", "A kick aimed towards the family jewels",0,[0,0,1],[5,0,1], [0.5,0.5], 0, 5]
        
        # rare cards - total 5
        deck[len(deck)+1] = ["Back Kick", "Happy de ume tsukushite",1,[0,0,1], [0,0,1], [0.5,0.5]] # direction opposite orientation + kick
        deck[len(deck)+1] = ["Flying Kick", "Soaring through the air feet first",[-5,-15,1], [0,0,1], [0.5,0.5]] # up + direction + kick 
        deck[len(deck)+1] = ["Roundhouse Kick", "A kick with extra knockback",1,[0,0,1], [0,0,1], [0.5,1]] # left + right + kick or right + left + kick
        deck[len(deck)+1] = ["Axe Kick", "A kick with a chance to stun",1,[0,0,1], [0,0,1], [0.5,1]] # up + down + kick
        deck[len(deck)+1] = ["Knee Strike", "A quick knee to the chin",1,[0,0,1], [0,0,1], [0.5,0.5]] # up + kick
        deck[len(deck)+1] = ["Spin","You some kind of ballerina?",1,[0,0,1], [0,0,1], [0,0]] # left + right + left
        deck[len(deck)+1] = ["Leap","Its like jumping twice",1,[0,-30,1], [0,0,1], [0,0]] # up + up + up


        # epic cards - total 3
        deck[len(deck)+1] = ["Spinning Back Kick", "A powerful spinning kick",2,[0,0,1], [0,0,1], [0.5,0]] # spin + back kick
        deck[len(deck)+1] = ["Flying Knee", "",2,[10,15,1], [0,0,1], [0.5,0.5]] # direction + direction + knee strike
        deck[len(deck)+1] = ["Tornado Kick", "Let it rip!",2,[0,0,1], [0,0,1], [0.5,1]] # spin + roundhouse kick
        deck[len(deck)+1] = ["Sky Drop","",2,[0,-15,1], [0,0,1], [0.5,1.5]]
        # rdm drug


        # legendary careds
        deck[len(deck)+1] = ["Roids", "Jump Higher, Run Faster Kick Harder",3] # add a multiplier to outgoing dmg
        

        return deck

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
def check_combo_q(q:queue):
    multiplier = 10000
    combo_id = 0
    while not q.empty():
        combo_id += q.get() * multiplier
        multiplier /= 100
    return combo_id
def check_combo_l(l:list):
    multiplier = 10000
    combo_id = 0
    for i in l:
        combo_id += i*multiplier
        multiplier /= 100
    return combo_id
