from game_engine import NumGame
from help_string import help_string
help_string2 = help_string + """Method of input:\n
If you are guessing 12345 you will type 12345 and then you will press enter.\n
If you enter the character: e, the number will be revealed and you lose.\n

Press Enter to start\n
*******************************************************************************
"""
print(help_string2)
input()

play_again = True
while play_again:
    print("*******************************************************************************")
    play_again = False
    game = NumGame()
    solved = False
    tries = 0
    while not solved:
        x = None
        x = input('enter number: ')
        flag, x, mesg_string = game.get_input(x)
        if x == 'e':
            print('the solution was {}'.format(game.num))
            print('quit game')
            break
        if flag:
            tries += 1
            count, place = game.compare(x)
            print( '{}) reply for {} is {}/{}'.format(tries,x, count, place))
            if count == place == 5:
                print('you won !')
                print('your score is {}/100'.format(100-tries+1))
                solved = True
                y = input('play again? \n if yes type: y \n if no press any key excpet: y \n')
                if y.lower() == 'y':
                    play_again = True
        else:
            print(mesg_string)
