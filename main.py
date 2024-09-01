from game import Game

runGame = Game()

while runGame.running:
    runGame.curr_menu.display_menu()
    runGame.game_loop()
