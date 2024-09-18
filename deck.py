import random

class deck():
    def __init__(self) -> None:
        self.deck = self.create_deck()
        print("deck created")
        
    def create_deck(self) -> list:
        # dictionary to describe cards
        # [n, pos, atk, d, img]
        #  n -> Name of the card
        #  pos -> describes change in position for character, None if no change in position
        #    - [x,y] given position of the characer (0,0), the character would be moved to (x,y) after the card is played
        #  atk -> describes the attack of the card, left None if no attack is made
        #    - [dmg, k, x1, x2, y1, y2]
        #    - dmg -> dmg done to opponent if opponent is within the aoe (x1,x2,y1,y2)
        #    - k -> knockback done to the opponent if hit
        #        - [x, y, prone] pos vector denoting change in movement and if action knocks the opponent down 
        #    - aoe ranges from x1 - x2, y1 - y2
        #  d -> short description of the card
        #  img -> image to be displayed on the player hand and queue
        
        # common cards
        common_deck = dict()
        common_deck[len(common_deck)+1] = ["Move Left", [-1,0], None, "Moves Left", "some/file/path.png"]
        common_deck[len(common_deck)+1] = ["Move Right", [1,0], None, "Moves right", "some/file/path.png"]
        common_deck[len(common_deck)+1] = ["Move Up", [0,1], None, "Moves up", "some/file/path.png"]
        common_deck[len(common_deck)+1] = ["Move Down", [0,-1], None, "Moves down", "some/file/path.png"]
        common_deck[len(common_deck)+1] = ["flying kick", [2,1], [1,[0,5,-1,1]],"A kick whilst flying","some/file/s.png"]
        common_deck[len(common_deck)+1] = ["Kick", None, [1,[1,0,False],[(1,1)]], "A kick aimed towards the family jewels", "some/file/path.png"]
        
        # rare cards
        rare_deck = dict()
        rare_deck[len(rare_deck)+1] = ["flying kick", [2,1], [1,[2,0,False],[-1,1,1,1]],"A kick whilst flying","some/file/s.png"]
        rare_deck[len(rare_deck)+1] = ["Roundhouse Kick", None, [1,[0,5,-1,1]],"flying kick","some/file/s.png"]
        
        # epic cards
        epic_deck = dict()
        epic_deck[len(epic_deck)+1] = ["epic placeholder", [2,1], [1,[2,0,False],[-1,1,1,1]],"A kick whilst flying","some/file/s.png"]

        # legendary careds
        leg_deck = dict()


        return [common_deck,rare_deck, epic_deck, leg_deck]

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
            if time > 210:
                if bucket_choice < 61:
                    cards_drawn.append(self.draw_card(0))
                elif bucket_choice < 96:
                    cards_drawn.append(self.draw_card(1))
                else:
                    cards_drawn.append(self.draw_card(2))
            # between 2:00 and 3:30 chances for C/R/E/L -> 45/40/10/1
            elif time > 120:
                if bucket_choice < 41:
                    cards_drawn.append(self.draw_card(0))
                elif bucket_choice < 71:
                    cards_drawn.append(self.draw_card(1))
                elif bucket_choice < 91:
                    cards_drawn.append(self.draw_card(2))
                else:
                    cards_drawn.append(self.draw_card(3))
            # between 2:00 and 3:30 chances for C/R/E/L -> 30/40/25/5
            elif time > 60:
                if bucket_choice < 31:
                    cards_drawn.append(self.draw_card(0))
                elif bucket_choice < 71:
                    cards_drawn.append(self.draw_card(1))
                elif bucket_choice < 96:
                    cards_drawn.append(self.draw_card(2))
                else:
                    cards_drawn.append(self.draw_card(3))
            # between 2:00 and 3:30 chances for C/R/E/L -> 15/30/45/10
            else:
                if bucket_choice < 16:
                    cards_drawn.append(self.draw_card(0))
                elif bucket_choice < 46:
                    cards_drawn.append(self.draw_card(1))
                elif bucket_choice < 91:
                    cards_drawn.append(self.draw_card(2))
                else:
                    cards_drawn.append(self.draw_card(3))
                
        return cards_drawn

    def draw_card(self, bucket:int) -> int:
        return self.deck[bucket][random.randint(1,len(self.deck[bucket]))]
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

myq = queue.Queue()
myq.put(12)
myq.put(34)
myq.put(56)
print(check_combo_q(myq))

myl = list()
myl.append(12)
myl.append(34)
myl.append(56)
print(check_combo_l(myl))
