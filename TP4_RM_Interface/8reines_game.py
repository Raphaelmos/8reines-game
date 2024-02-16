from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import pygame

pygame.mixer.init()

#Classe qui représente le jeu
class Jeu(Tk):
    def __init__(self,):
        super().__init__()
        #Créer les différents widgets de la fenêtre
        #Boutons et plateau

        self.plateau = Plateau(self, 300, 550)
        self.resizable(TRUE,TRUE)
        self.columnconfigure(0,weight=1)
        self.rowconfigure(0,weight=1)
        self.plateau.grid(row = 0, column = 0)

        frame_btn = Frame(self,width = 300, height = 550, bg= 'ivory')
        frame_btn.grid(row = 0, column = 1)

        self.btn_verification = Button(frame_btn,text = "Vérifier", fg = 'black', command=self.validation, width= 10, highlightbackground='ivory')
        self.btn_verification.place(x = 50 , y=100)
        #
        self.btn_indice = Button(frame_btn,text = "Indice", command=self.indice, width= 10, highlightbackground='red')
        self.btn_indice.place(x = 50, y=150)
        #
        self.btn_reset = Button(frame_btn,text = "Réinitialiser", command=self.resetAll, width= 10, highlightbackground ='red')
        self.btn_reset.place(x = 50, y=200)
        self.btn_image=PhotoImage(file="soncoupe.png")
        self.music_btn = Button(frame_btn, text= "Jouer/stop musique", command =self.play_sound, image=self.btn_image )
        self.music_btn.place(x = 50, y = 250)

        self.label=Label(frame_btn, text="1 pour Stop/jouer le son", font=("Adventure", 10), bg="ivory")
        self.label.place (x=50, y=305)
        self.label=Label(frame_btn, text="2 pour valider", font=("Adventure", 10),bg="ivory")
        self.label.place (x=50, y=330)
        self.label=Label(frame_btn, text="3 pour indice", font=("Adventure", 10), bg="ivory")
        self.label.place (x=50, y=360)
        self.label=Label(frame_btn, text="4 pour reset", font=("Adventure", 10),bg="ivory")
        self.label.place (x=50, y=390)

        frame_texte = Frame(self,width = 500, height = 500, bg= 'ivory')
        frame_texte.grid(row = 1, column = 0)
        self.texte_moves= Text(frame_texte,height=5, width=50,highlightbackground= "ivory")
        self.scrollbar_zmoves=Scrollbar(frame_texte)
        self.scrollbar_zmoves.pack(side=RIGHT, fill=Y)
        self.scrollbar_zmoves.config(command=self.texte_moves.yview, width=8)
        self.texte_moves.config(yscrollcommand = self.scrollbar_zmoves.set)
        self.texte_moves.pack()

        self.my_sizegrip = ttk.Sizegrip(self)
        self.my_sizegrip.grid(row=1,sticky=SE)

        self.boutons()

    def boutons(self):
        self.bind('1', lambda event: self.play_sound())
        self.bind('2', lambda event: self.validation())
        self.bind('3', lambda event: self.indice())
        self.bind('4', lambda event: self.resetAll())


    def play(self):
        pygame.mixer.music.load("Swingmusic50s.mp3")
        pygame.mixer.music.play(loops=-1)
        pygame.mixer.music.set_volume(0.01)

    def play_sound(self):
        self.sound_on=PhotoImage(file="sonactif.png")
        self.sound_off=PhotoImage(file="soncoupe.png")
        if self.music_btn ["text"] == "Play musique":
            self.music_btn.config(image=self.sound_on)
            self.music_btn ["text"] = "Pause musique"
            self.music_btn["bg"] = "gray"
            pygame.mixer.music.load("Swingmusic50s.mp3")
            pygame.mixer.music.play(loops= -1)
            pygame.mixer.music.set_volume(0.1)

        else:
            self.music_btn.config(image=self.sound_off)
            self.music_btn["text"] = "Play musique"
            self.music_btn["bg"] = "wheat"
            pygame.mixer.music.pause()

    def validation(self):
        if self.plateau.verifieConfiguration():
            self.btn_verification['fg'] = 'gray'
        else:
            self.btn_verification['fg'] = 'wheat'

    def indice(self):
        indice= self.plateau.solution()
        if indice[0]:
            self.btn_indice['fg'] = 'gray'
            case = self.plateau.getCase(indice[1], indice[2])
            case['text'] = 'X'
            case['fg'] = 'wheat'
            case.after(1000,case.reset)
        else:
            self.btn_indice['fg'] = 'wheat'

    def resetAll(self):
        self.message = messagebox.askquestion("Nouvelle partie", "Confirmer pour reset la partie")
        if self.message == "yes":
            self.plateau.reset()
        else:
            pass

#Classe qui représente l'échiquier
class Plateau(Frame):

    cases = []
    #Constructeur
    def __init__(self,fenetre : Tk, width, height):
        super().__init__(fenetre, width= width, height =height, bg='ivory')
        #Créer les cases
        for x in range(0, 8):
            for y in range(0, 8):
                self.cases.append(Case(self, x, y))

    def getCase(self, x, y):#obtenir la position
        for c in self.cases:
            if c.x == x and c.y == y:
                return c

    def solution(self):
        if self.verifieConfiguration():
            for i in range(0,8):
                if self.compteLigne(i) == 0:
                    for j in range(0, 8):
                        c= self.getCase(i,j)
                        c['text'] = 'X'
                        c.occupee = True
                        if self.verifieConfiguration():
                            c.reset()
                            return (True, i, j)
                        else:
                            c.reset()
        return (False, -1, -1)

    def compteDiagonale(self, k):
        nb = 0
        min = 0
        max = 0
        if k < 0:
            min = -k
            max = 8
        else:
            min = 0
            max = 8 - k

        for i in range(min ,max):
            for c in self.cases:
                if c.x == i and c.y == i+k and c.estOccupee():
                    nb +=1
        return nb
    def compteAntidiagonale(self, k):
        nb = 0
        min = 0
        max = 0
        if k < 0:
            min = -k
            max = 8
        else:
            min = 0
            max = 8 - k
        for i in range(min ,max):
            for c in self.cases:
                if c.x == 7-i and c.y == i+k and c.estOccupee():
                    nb +=1
        return nb
    def compteLigne(self, k):
        nb = 0
        for c in self.cases:
            if c.x == k and c.estOccupee():
                nb +=1
        return nb
    def compteColonne(self, k):
        nb = 0
        for c in self.cases:
            if c.y == k and c.estOccupee():
                nb +=1
        return nb
    def verifieDiagonales(self):
        for i in range(-6, 7):
            if self.compteDiagonale(i)>1:
                return False
        return True
    def verifieAntidiagonales(self):
        for i in range(-6, 7):
            if self.compteAntidiagonale(i)>1:
                return False
        return True
    def verifieLignes(self):
        for i in range(0,8):
            if self.compteLigne(i)>1:
                return False
        return True
    def verifieColonnes(self):
        for i in range(0,8):
            if self.compteColonne(i)>1:
                return False
        return True
    def verifieConfiguration(self):
        return self.verifieDiagonales() and self.verifieAntidiagonales()\
            and self.verifieLignes() and self.verifieColonnes()

    def reset(self):
        for c in self.cases:
            c.reset()

#Classe qui représente une case de l'échiquier
class Case(Button):
    def __init__(self,plateau:Frame, x , y):
        super().__init__(plateau, text="", width=3, height=3, command=self.clicGauche, highlightbackground='ivory', bg="dark orange")
        self.x = x
        self.y = y
        self.occupee = False
        self.grid(row=x, column=y)

    def estOccupee(self):
        return self.occupee

    def click (self):
        return self.isclicked

    def clicGauche(self):
        if self.estOccupee() :
            self.configure(text="")
            self.occupee = False
            pygame.mixer.init()
            self.sound02= pygame.mixer.Sound("sons.wav")
            pygame.mixer.find_channel(True).play(self.sound02)

        else:
            self.configure(text="X" , fg='black')
            self.occupee = True
            pygame.mixer.init()
            self.sound= pygame.mixer.Sound("sons.wav")
            pygame.mixer.find_channel(True).play(self.sound)

    def reset(self):
        self['text'] = ""
        self['fg'] = "black"
        self.occupee = False
        pygame.mixer.init()
        self.sound02= pygame.mixer.Sound("sons.wav")
        pygame.mixer.find_channel(True).play(self.sound02)

    def get_coord(self):
        return self.x, self.y

mon_jeu = Jeu()
mon_jeu.play()
mon_jeu.mainloop()