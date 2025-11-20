from tkinter import *
import os
from random import *
from tkinter import messagebox

print(os.getcwd())

tour = 0
plateau = ["n", "n", "n", "n", "n", "n", "n", "n", "n"]

lignes = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8)
    ]

colonnes = [
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8)
    ]

diagonales = [
        (0, 4, 8),
        (2, 4, 6)
    ]

def ia(board, signe):

    if signe == "X" :
        adversaire = "O"
    else :
        adversaire = "X"
    

    #liste des listes de combinaisons gagnante
    lignes_total = lignes + colonnes + diagonales

    print(lignes_total)

    #Cherche un coup gagnant
    for a, b, c in lignes_total:                            #Parcourt du plateau en fonction des combinaisons gagnantes
        trio = (board[a], board[b], board[c])               #En fonction des indices gagnants, on initialise le trio avec ce qu'il y dans le plateau
        if trio.count(signe) == 2 and trio.count("n") == 1: #Si le signe de l'IA apparaît 2 fois dans une combinaison gagnante et que la dernière case n'est pas encore jouée
            coup = [a, b, c][trio.index("n")]               #Le coup de l'IA sera la case qui n'est pas jouée
            placer(coup)
            return

    #Cherche à bloquer l'adversaire
    for a, b, c in lignes_total:
        trio = (board[a], board[b], board[c])
        if trio.count(adversaire) == 2 and trio.count("n") == 1:    #Si le signe du joueur apparaît 2 fois dans une combinaison gagnante et que la dernière case n'est pas encore jouée
            coup = [a, b, c][trio.index("n")]                       #Le coup de l'IA sera la case qui n'est pas joué
            placer(coup)
            return

    #Prendre le centre si disponible --> centre avantageux dans ce jeu
    if board[4] == "n":
        placer(4)
        return

    #Prendre un coin si disponible --> coins avantageux dans ce jeu
    for coin in [0, 2, 6, 8]:
        if board[coin] == "n":
            placer(coin)
            return

    #Sinon jouer aléatoire
    i = randint(0, 8)
    while board[i] != "n" :
        i = randint(0, 8)
    placer(i)


def placer(n) :
    global tour, img_croix, img_rond, board, lst_boutons
        
    if tour%2 == 0 :
        plateau[n] = "X"
        lst_boutons[n].configure(state="disabled", image = img_croix, height = 150, width = 150)

    else :
        plateau[n] = "O"
        lst_boutons[n].configure(state="disabled", image = img_rond, height = 150, width = 150)
    
    tour += 1

    resultat = fin_de_partie()
    if resultat :
        messagebox.showinfo("Fin de partie", resultat)
        print(resultat)

        for btn in lst_boutons :
            btn.configure(state = "disabled")

        fen_jeu.destroy()
        
        return

    if var_joueur.get() == 1 and tour < 9 :
        if var_signe.get() == "X" and tour%2 == 1 :
            fen_jeu.after(200, lambda : ia(plateau, "O"))
        if var_signe.get() == "O" and tour%2 == 0 :
            fen_jeu.after(200, lambda : ia(plateau, "X"))

def fin_de_partie() :
    global tour, plateau

    for a, b, c in lignes :
        if plateau[a] == plateau[b] == plateau[c] != "n" :
            return f"Gagnant par ligne ({plateau[a]})"
        
    for a, b, c in colonnes :
        if plateau[a] == plateau[b] == plateau[c] != "n" :
            return f"Gagnant par colonne ({plateau[a]})"
        
    for a, b, c in diagonales :
        if plateau[a] == plateau[b] == plateau[c] != "n" :
            return f"Gagnant par diagonale ({plateau[a]})"
        
    if tour >= 9 :
        return "Match nul !"
    
    return None

def recommencer() :
    if fen_jeu.winfo_exists() :
        fen_jeu.destroy()
        jeu()

#L'interface se met à jour en fonction des choix de l'utilisateur
def afficher_signe() :
    global var_signe

    if var_joueur.get() == 1 :
        fen_menu.geometry("500x270")
        frame_signe_txt.pack(pady = 5)
        frame_signe_btn.pack(pady = 5)
        if var_signe.get() != "None" :
            btn_Jouer.pack(side = "left", padx = 10, anchor = "se")
            btn_quitter.pack(side = "left", anchor = "sw")
    else :
        var_signe = "None"
        fen_menu.geometry("500x200")
        frame_signe_txt.pack_forget()
        frame_signe_btn.pack_forget()
        btn_Jouer.pack(side = "left", padx = 10, anchor = "se")
        btn_quitter.pack(side = "left", anchor = "sw")
        

#Fonction appelée lors du lancement d'un jeu --> fait apparaître l'interface et appelle les fonctions nécessaires lorsqu'un coup est joué par le joueur 
def jeu() :
    global plateau, tour
    plateau = ["n", "n", "n", "n", "n", "n", "n", "n", "n"]
    tour = 0

    if var_joueur.get() == 0 :
        return messagebox.showerror("Erreur", "Erreur, le nombre de joueur n'a pas été sélectionné !")
    if var_joueur.get() == 1 and var_signe.get() == "None" :
        return messagebox.showerror("Erreur", "Erreur, le signe du joueur n'a pas été sélectionné !")

    #Création de la fenêtre de jeu
    global fen_jeu
    fen_jeu = Toplevel(fen_menu)
    fen_jeu.geometry("479x560+570+150")
    fen_jeu.title("TicTacToe")
    fen_jeu.configure(bg = "#2c2f33")

    STYLE_CASE = {
        "bg" : "#99aab5",
        "activebackground": "#7289da",
        "relief": "flat",
        "cursor" : "hand2",
        "width": 160,
        "height": 160

    }

    global img_croix
    img_croix = PhotoImage(file="C:/Users/guigu/Documents/LAPLATEFORME/PYTHON/projet tictactoe/images/croix.png")
    global img_rond 
    img_rond= PhotoImage(file="C:/Users/guigu/Documents/LAPLATEFORME/PYTHON/projet tictactoe/images/rond.png")
        
    btn_1 = Button(fen_jeu, command = lambda : placer(0),  bg = "white", height = 10, width = 20)
    btn_2 = Button(fen_jeu, command = lambda : placer(1), bg = "white", height = 10, width = 20)
    btn_3 = Button(fen_jeu, command = lambda : placer(2), bg = "white", height = 10, width = 20)
    btn_4 = Button(fen_jeu, command = lambda : placer(3), bg = "white", height = 10, width = 20)
    btn_5 = Button(fen_jeu, command = lambda : placer(4), bg = "white", height = 10, width = 20)
    btn_6 = Button(fen_jeu, command = lambda : placer(5), bg = "white", height = 10, width = 20)
    btn_7 = Button(fen_jeu, command = lambda : placer(6), bg = "white", height = 10, width = 20)
    btn_8 = Button(fen_jeu, command = lambda : placer(7), bg = "white", height = 10, width = 20)
    btn_9 = Button(fen_jeu, command = lambda : placer(8), bg = "white", height = 10, width = 20)

    global lst_boutons
    lst_boutons = [btn_1, btn_2, btn_3, btn_4, btn_5, btn_6, btn_7, btn_8, btn_9]

    btn_1.grid(row = 0, column = 0, padx = 5, pady = 5)
    btn_2.grid(row = 0, column = 1, padx = 5, pady = 5)
    btn_3.grid(row = 0, column = 2, padx = 5, pady = 5)
    btn_4.grid(row = 1, column = 0, padx = 5, pady = 5)
    btn_5.grid(row = 1, column = 1, padx = 5, pady = 5)
    btn_6.grid(row = 1, column = 2, padx = 5, pady = 5)
    btn_7.grid(row = 2, column = 0, padx = 5, pady = 5)
    btn_8.grid(row = 2, column = 1, padx = 5, pady = 5)
    btn_9.grid(row = 2, column = 2, padx = 5, pady = 5)


    btn_recommencer = Button(fen_jeu, text = "Recommencer la partie", command = recommencer, bg = "#7289da", fg = "white", font = ("Calibri", 13, "bold"),  relief = "flat", cursor = "hand2", width = 15)
    btn_recommencer.grid(row = 3, column = 0, pady = 15)

    btn_menu = Button(fen_jeu, text = "Menu", command = fen_jeu.destroy, bg = "#f04747", fg = "white", font = ("Calibri", 13, "bold"), relief = "flat", cursor = "hand2", width = 10)
    btn_menu.grid(row = 3, column = 2, ipadx = 40, pady = 20)


    if var_signe.get() == "O" :
        ia(plateau, "X")


#Création de la fenêtre menu
fen_menu = Tk()
fen_menu.geometry("500x200+650+300")
fen_menu.title("TicTacToe")
fen_menu.configure(bg="#2c2f33")

#style commun texte et bouton
STYLE_TEXTE = {"bg": "#2c2f33", "fg": "white", "font": ("Calibri", 13)}
STYLE_TEXTE_TITRE = {"bg": "#2c2f33", "fg": "white", "font": ("Calibri", 16, "bold")}

STYLE_BUTTON = {
    "bg": "#7289da", "fg": "white",
    "font": ("Calibri", 12, "bold"),
    "activebackground": "#5b6eae",
    "relief": "flat",
    "cursor": "hand2",
    "width": 18
}

#Texte de présentation
txt_Bienvenue = Label(fen_menu, text = "Bonjour et bienvenue dans notre jeu de TicTacToe !", **STYLE_TEXTE_TITRE)
txt_Bienvenue.pack()

#Texte de séléction du nombre de joueur
txt_Joueur = Label(fen_menu, text = "Selectionnez le nombre de joueur :", **STYLE_TEXTE)
txt_Joueur.pack()

txt_Info = Label(fen_menu, text = "(X commence en 1er !)", **STYLE_TEXTE)
txt_Info.pack()

#Bouton pour séléctionner le nombre de joueurs
var_joueur = IntVar(value = 0)
var_signe = StringVar(value = "None")

frame_joueur = Frame(fen_menu, bg="#2c2f33")
frame_joueur.pack()

btn_Joueur_1 = Radiobutton(frame_joueur, text = "1 joueur", variable = var_joueur, value = 1, command = afficher_signe, bg = "#2c2f33", fg = "white", selectcolor = "#23272a",  font = ("Calibri", 12))
btn_Joueur_2 = Radiobutton(frame_joueur, text = "2 joueurs", variable = var_joueur, value = 2, command = afficher_signe, bg = "#2c2f33", fg = "white", selectcolor = "#23272a",  font = ("Calibri", 12))
btn_Joueur_1.pack(side = "left", padx = 30, anchor = "n")
btn_Joueur_2.pack(side = "left", padx = 30, anchor = "n")

frame_signe_txt = Frame(fen_menu, bg="#2c2f33")
frame_signe_btn = Frame(fen_menu, bg="#2c2f33")

txt_Signe = Label(frame_signe_txt, text = "Choisissez votre signe :", **STYLE_TEXTE)
txt_Signe.pack(side = "left", padx = 30)

btn_croix = Radiobutton(frame_signe_btn, text = "X", variable = var_signe, value = "X", bg = "#2c2f33", fg = "white", selectcolor = "#23272a", font = ("Calibri", 12))
btn_rond = Radiobutton(frame_signe_btn, text = "O", variable = var_signe, value = "O", bg = "#2c2f33", fg = "white", selectcolor = "#23272a", font = ("Calibri", 12))
btn_croix.pack(side = "left", padx = 30)
btn_rond.pack(side = "left", padx = 30)

frame_action = Frame(fen_menu, bg="#2c2f33")
frame_action.pack(pady = 15)

btn_quitter = Button(frame_action, text = "Quitter", command = fen_menu.destroy, bg = "#f04747", activebackground = "#c23a3a", fg = "white", font = ("Calibri", 12, "bold"), relief = "flat", cursor = "hand2", width = 12)
btn_Jouer = Button(frame_action, text = "Lancer la partie !", command = jeu, **STYLE_BUTTON)


if var_joueur.get() == 1 :
    btn_croix.pack_forget()
    btn_rond.pack_forget()

fen_menu.mainloop()