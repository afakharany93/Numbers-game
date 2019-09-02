import random
print(" Number Discovery Game\n*****************\nThis game is made by : Ahmed Essam El Fakharany\n afakharany93@gmail.com \n*****************\nThe Rules:\n ")
print("The computer will generate a random 5 digit number.\n")
print("Your mission is to guess the number in the least amount of tries.\n")
print("Each try you'll input a 5 digit number as a guess the computer will compare \n")
print("your guess to the number and it will give you an answer in the form of \n")
print("(Number1/Number2).\n")
print("The First number denotes The amount of numbers from your guess \n")
print("that actually exist in the random generated number.\n")
print("The Second Number Denotes the amount of numbers that not only exist in the \n")
print("randomly generated number but also have the correct position in the 5 digit \n")
print("number.\n")
print(" Example:\n")
print("The Computer Generates a random number : 28461\n")
print("your initial guess is 2 6 7 9 8\n")
print("The computer will Reply 3/1 The 3 Denotes that 2 6 and 7 were part of the guess\n")
print("The 1 Denotes that the 2 was not only in the guess but also in the correct \n")
print(" position.\n")
print("Rules The Computer are limited by In generating the random number.\n")
print("1- The number may never start with a 0.\n")
print("2- A single number may never repeat in the random number.\n")
print("The Following are examples of numbers that will never be generated.\n")
print("Ex1: 02314 Can't start with a 0.\n")
print("Ex2: 22314 Can't generate same number twice.\n")
print("Method of input:\n")
print("If you are guessing 12345 you will type 12345 and then you will press enter.\n")
print("If you enter the character: e, the number will be revealed and you lose.\n")

print("Press Enter to start\n ")
print("*******************************************************************************")
input()
class NumGame ():
    def __init__(self):
        self.num = self.generate_number()

    def check_input(self,ip, verbose=False):
        ret_val = True
        mesg_string = None
        #check if the input is of 5 characters
        if len(ip) != 5 :
            mesg_string = 'lnegth of input number isn\'t 5 digits'
            ret_val =  False
        #check if all inputs are numbers
        elif not ip.isdigit():
            mesg_string = 'All vlaues input should be numbers'
            ret_val =  False
            #check if the first isn't 0
        elif int(ip[0]) == 0:
            mesg_string = 'The first value shouldn\'t be zero'
            ret_val =  False
        else:
            #check if there is a duplicate number
            for i in range(len(ip)):
                if ip.count(ip[i]) > 1:
                    mesg_string = 'there shouldn\'t be a number that is occured twice'
                    ret_val =  False

        if mesg_string is not None and verbose:
            print(mesg_string)
        return ret_val

    def get_input(self):
        x = None
        x = input('enter number: ')
        flag = False
        if x != 'e':
            flag = self.check_input(x, verbose = True)
            if not flag:
                x = None
            else:
                x = int(x)
        return flag, x

    def generate_number(self):
        f = True
        while f:
            num = random.randint(10000, 99999)
            print(num)
            f = self.check_input(str(num))
            f = not f
        return num

    def compare(self, ip):
        ref_n = str(self.num)
        ip_s = str(ip)
        count = 0
        place = 0
        for i in range(len(ref_n)):
            val_i = ref_n[i]
            for j in range(len(ip_s)):
                val_j = ip_s[j]
                if val_i == val_j:
                    count += 1
                    if i == j:
                        place += 1
        return count, place
play_again = True
while play_again:
    print("*******************************************************************************")
    play_again = False
    game = NumGame()
    solved = False
    tries = 0
    while not solved:
        flag, x = game.get_input()
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
