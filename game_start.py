from main import Game
game = Game()
while not game.game_over:
    game.curr_menu.display_menu()
    game.run()