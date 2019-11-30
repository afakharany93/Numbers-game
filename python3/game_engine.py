import random
class NumGame ():
    def __init__(self):
        self.num = self.generate_number()

    def check_input(self,ip):
        ret_val = True
        mesg_string = None
        #check if the input is of 5 characters
        mesg_string = ''
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

        # if mesg_string is not None and verbose:
        #     print(mesg_string)
        return ret_val, mesg_string

    def get_input(self, x):
        flag = False
        mesg_string = ''
        if x != 'e':
            flag, mesg_string = self.check_input(x)
            if not flag:
                x = None
            else:
                x = int(x)
        return flag, x, mesg_string

    def generate_number(self):
        f = True
        while f:
            num = random.randint(10000, 99999)
            # print(num)
            f, mesg_string = self.check_input(str(num))
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
