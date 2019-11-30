from tkinter import *
import tkinter.ttk as ttk
import tkinter.scrolledtext as scrolledtext
from game_engine import NumGame
from help_string import help_string
class Window(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.game = NumGame()
        self.init_window()

    def init_window(self):
        self.master.title("GUI")
        self.pack(fill=BOTH, expand=1)
        # quitButton = Button(self, text='quit', command=self.client_exit)
        # quitButton.place(x=0, y=0)
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        file.add_command(label="New thinking area", command=self.thinking_area)
        menu.add_cascade(label="File", menu=file)

        t = Label(self.master, text="Enter your guess here")
        t.place(x=450, y=0)
        self.e1 = Entry(self.master)
        self.e1.place(x=450, y=20)
        self.e1.bind("<Return>", self.eval)
        # e1.pack()
        self.tex = scrolledtext.ScrolledText(master=self.master, wrap="word", width=50)
        self.tex.place(x=0, y=0)
        self.callback(help_string)
        self.thinking_area()
        # self.add_checkbuttons()
        # self.add_matrix()
    def thinking_area(self):
        root2 = Tk()
        root2.geometry('800x600')
        app2 =Window2(root2)
        # root2.mainloop()

    def add_matrix(self):
        d = 50
        for i in range(5):
            for j in range(5):
                OPTIONS = ["","F", "T"] #etc
                variable = StringVar(self.master)
                variable.set(OPTIONS[0]) # default value
                w = OptionMenu(self.master, variable, *OPTIONS)
                w.place(x=500+j*d, y=100+i*d)
                e1 = Entry(self.master,width=2)
                e1.place(x=470, y=105+i*d)


    def add_checkbuttons(self):
        for i in range(10):
            ch0 = Checkbutton(self.master, text=str(i))
            ch0.place(x=10+int(i)*70,y=500)
            OPTIONS = ["","F", "T"] #etc
            variable = StringVar(self.master)
            variable.set(OPTIONS[0]) # default value
            w = OptionMenu(self.master, variable, *OPTIONS)
            w.place(x=int(i)*70,y=530)

    def callback(self,s,end='\n'):
        # s = 'At {} f is {}\n'.format(id, id**id/0.987)
        self.tex.insert(END, s+end)
        self.tex.see(END)
    def eval(self,event):
        flag, x, mesg_string = self.game.get_input(self.e1.get())
        if x == 'e':
            self.callback('the solution was {}'.format(self.game.num))
            self.callback('quit game')
        if flag:

            count, place = self.game.compare(x)
            self.callback( 'reply for {} is {}/{}'.format(x, count, place))
            if count == place == 5:
                self.callback('you won !')
                # self.callback('your score is {}/100'.format(100-tries+1))
        else:
            self.callback(mesg_string)
        # self.callback(s)
        self.e1.delete(0, 'end')

    def client_exit(self):
        exit()

class Window2(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.init_window()

    def init_window(self):
        self.master.title("Thinking area")
        self.pack(fill=BOTH, expand=1)
        # quitButton = Button(self, text='quit', command=self.client_exit)
        # quitButton.place(x=0, y=0)
        menu = Menu(self.master)
        self.master.config(menu=menu)

        file = Menu(menu)
        file.add_command(label="Exit", command=self.client_exit)
        menu.add_cascade(label="File", menu=file)
        self.add_checkbuttons()
        self.add_matrix()


    def add_matrix(self):
        d = 50
        for i in range(5):
            for j in range(5):
                OPTIONS = ["","F", "T"] #etc
                variable = StringVar(self.master)
                variable.set(OPTIONS[0]) # default value
                w = OptionMenu(self.master, variable, *OPTIONS)
                w.place(x=60+j*d, y=0+i*d)
                e1 = Entry(self.master,width=2)
                e1.place(x=30, y=5+i*d)


    def add_checkbuttons(self):
        for i in range(10):
            ch0 = Checkbutton(self.master, text=str(i))
            ch0.place(x=10+int(i)*70,y=300)
            OPTIONS = ["","F", "T"] #etc
            variable = StringVar(self.master)
            variable.set(OPTIONS[0]) # default value
            w = OptionMenu(self.master, variable, *OPTIONS)
            w.place(x=int(i)*70,y=330)

    def client_exit(self):
        exit()
if __name__ =="__main__":

    root = Tk()
    root.geometry('800x600')
    app = Window(root)
    root.mainloop()
