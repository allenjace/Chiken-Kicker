import random
import queue

class deck():
    def __init__(self) -> None:
        self.deck = self.create_deck()
        self.sections = []
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
        
        # common cards - total 6
        deck = dict()
        deck[len(deck)+1] = ["Move Left", "Moves Left"]
        deck[len(deck)+1] = ["Move Right", "Moves right"]
        deck[len(deck)+1] = ["Move Up", "Moves up"]
        deck[len(deck)+1] = ["Move Down", "Moves down"]
        deck[len(deck)+1] = ["Duck", "Duck down"]
        deck[len(deck)+1] = ["Kick", "A kick aimed towards the family jewels"]
        
        # rare cards - total 5
        deck[len(deck)+1] = ["Back Kick", "Happy de ume tsukushite"] # direction opposite orientation + kick
        deck[len(deck)+1] = ["Flying Kick", "Soaring through the air feet first"] # up + direction + kick 
        deck[len(deck)+1] = ["Roundhouse Kick", "A kick with extra knockback"] # left + right + kick or right + left + kick
        deck[len(deck)+1] = ["Axe Kick", "A kick with a chance to stun"] # up + down + kick
        deck[len(deck)+1] = ["Knee Strike", "A quick knee to the chin"] # up + kick
        deck[len(deck)+1] = ["Spin","You some kind of ballerina?"] # left + right + left
        deck[len(deck)+1] = ["Leap","Its like jumping twice"] # up + up + up


        # epic cards - total 3
        deck[len(deck)+1] = ["Spinning Back Kick", "A powerful spinning kick"] # spin + back kick
        deck[len(deck)+1] = ["Flying Knee", ""] # direction + direction + knee strike
        deck[len(deck)+1] = ["Tornado Kick", "Let it rip!"] # spin + roundhouse kick
        deck[len(deck)+1] = ["Sky Drop",""]



        # legendary careds
        deck[len(deck)+1] = ["Roids", "Jump Higher, Run Faster Kick Harder"]

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
