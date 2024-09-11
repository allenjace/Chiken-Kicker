class deck():
    def __init__(self) -> None:
        self.deck = self.create_deck()
        print("deck created")
        
    def create_deck(self) -> dict:
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
        card_deck = dict()
        # common cards
        card_deck[len(card_deck)+1] = ["Move Left", [-1,0], None, "Moves Left", "some/file/path.png"]
        card_deck[len(card_deck)+1] = ["Move Right", [1,0], None, "Moves right", "some/file/path.png"]
        card_deck[len(card_deck)+1] = ["Move Up", [0,1], None, "Moves up", "some/file/path.png"]
        card_deck[len(card_deck)+1] = ["Move Down", [0,-1], None, "Moves down", "some/file/path.png"]
        card_deck[len(card_deck)+1] = ["flying kick", [2,1], [1,[0,5,-1,1]],"A kick whilst flying","some/file/s.png"]
        card_deck[len(card_deck)+1] = ["Kick", None, [1,[1,0,False],[(1,1)]], "A kick aimed towards the family jewels", "some/file/path.png"]
        
        # rare cards
        card_deck[len(card_deck)+1] = ["flying kick", [2,1], [1,[2,0,False],[-1,1,1,1]],"A kick whilst flying","some/file/s.png"]
        card_deck[len(card_deck)+1] = ["Roundhouse Kick", None, [1,[0,5,-1,1]],"flying kick","some/file/s.png"]
        # epic cards

        # legendary careds

        return card_deck

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

