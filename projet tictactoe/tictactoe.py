from tkinter import *
from random import *
from tkinter import messagebox

#On initialise le tour à 0
tour = 0

#Plateau de jeu vide
plateau = ["n"]*9

#Liste de tuples qui contient les lignes gagnantes
lignes = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8)
    ]

#Liste de tuples qui contient les colonnes gagnantes
colonnes = [
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8)
    ]

#Liste de tuples qui contient les 2 diagonales gagnantes
diagonales = [
        (0, 4, 8),
        (2, 4, 6)
    ]

#Fonction qui introduit une IA si le joueur joue tout seul
def ia(board, signe):

    #Mettre au claire les signes de chaque joueur (adversaire étant le joueur pour l'IA)
    if signe == "X" :
        adversaire = "O"
    else :
        adversaire = "X"
    

    #liste des listes de combinaisons gagnante
    lignes_total = lignes + colonnes + diagonales

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

#Fonction appelée lorsque le joueur ou bien l'IA à joué un coup
def placer(n) :
    global tour, img_croix, img_rond, lst_boutons

    #Le signe est joué en fonction du tour du jeu   
    if tour%2 == 0 :
        plateau[n] = "X"
        lst_boutons[n].configure(state="disabled", image = img_croix, height = 150, width = 150)

    else :
        plateau[n] = "O"
        lst_boutons[n].configure(state="disabled", image = img_rond, height = 150, width = 150)
    
    #Le tour est incrémenté après chaque action
    tour += 1

    #Vérification de fin de partie
    resultat = fin_de_partie()
    if resultat :
        messagebox.showinfo("Fin de partie", resultat)

        for btn in lst_boutons :
            btn.configure(state = "disabled")

        fen_jeu.destroy()
        
        return

    #Conditions à respecter pour demander à l'IA de jouer
    if var_joueur.get() == 1 and tour < 9 :
        if var_signe.get() == "X" and tour%2 == 1 :
            fen_jeu.after(200, lambda : ia(plateau, "O"))
        if var_signe.get() == "O" and tour%2 == 0 :
            fen_jeu.after(200, lambda : ia(plateau, "X"))

#Fonction qui détècte après le coup de l'IA ou du joueur si la partie est terminée
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

#Fonction simple afin de recommencer une partie
def recommencer() :
    if fen_jeu.winfo_exists() :
        fen_jeu.destroy()
        jeu()

#L'interface se met à jour en fonction des choix de l'utilisateur
def afficher_signe():
    if var_joueur.get() == 1:

        #Fenêtre agrandie pour les choix de signe
        fen_menu.geometry("500x220")
        frame_signe_txt.pack(pady=5)
        frame_signe_btn.pack(pady=5)

        #On ne packe les boutons que si un signe est choisi
        if var_signe.get() != "None":
            fen_menu.geometry("500x260")
            frame_action.pack(pady=15)
            btn_quitter.pack(side="left", padx=10)
            btn_Jouer.pack(side="left", padx=10)
            
            
        else:
            frame_action.pack_forget()

    elif var_joueur.get() == 2:
        #Pas de choix de signe nécessaire, boutons visibles immédiatement
        var_signe.set("None")
        fen_menu.geometry("500x200")
        frame_signe_txt.pack_forget()
        frame_signe_btn.pack_forget()

        frame_action.pack(pady=15)
        btn_Jouer.pack(side="left", padx=10)
        btn_quitter.pack(side="left", padx=10)


#Fonction appelée lors du lancement d'un jeu --> fait apparaître l'interface et appelle les fonctions nécessaires lorsqu'un coup est joué par le joueur 
def jeu() :
    global plateau, tour
    plateau = ["n"] * 9
    tour = 0

    #Gère les possibles erreurs
    if var_joueur.get() == 0 :
        return messagebox.showerror("Erreur", "Erreur, le nombre de joueur n'a pas été sélectionné !")
    if var_joueur.get() == 1 and var_signe.get() == "None" :
        return messagebox.showerror("Erreur", "Erreur, le signe du joueur n'a pas été sélectionné !")

    #Création de la fenêtre de jeu
    global fen_jeu
    fen_jeu = Toplevel(fen_menu)
    fen_jeu.geometry("500x600+570+150")
    fen_jeu.title("TicTacToe")
    fen_jeu.configure(bg = "#2c2f33")

    #Chargement des images de la croix et du rond
    global img_croix
    img_croix = PhotoImage(file="C:/Users/guigu/Documents/LAPLATEFORME/PYTHON/projet tictactoe/images/croix.png")
    global img_rond 
    img_rond= PhotoImage(file="C:/Users/guigu/Documents/LAPLATEFORME/PYTHON/projet tictactoe/images/rond.png")
    
    #Frame pour le plateau
    frame_plateau = Frame(fen_jeu, bg="#2c2f33")
    frame_plateau.pack(pady=20)

    #On créé tous les boutons qui compose notre grille --> appelle la fonction placer
    global lst_boutons
    lst_boutons = []
    for i in range(9):
        btn = Button(frame_plateau, bg="#99aab5", activebackground="#7289da", relief="flat",
                     cursor="hand2", width=20, height=10, command=lambda n=i: placer(n))
        lst_boutons.append(btn)

    #Placement des boutons en grille 3x3 avec espacement
    for i, btn in enumerate(lst_boutons):
        btn.grid(row=i//3, column=i%3, padx=5, pady=5)

    #Bouton ppour recommencer la partie
    btn_recommencer = Button(frame_plateau, text = "Recommencer la partie", command = recommencer, bg = "#7289da", fg = "white", font = ("Calibri", 11, "bold"),  relief = "flat", cursor = "hand2", width = 18)
    btn_recommencer.grid(row = 3, column = 0, padx = 3, pady = 10)

    #Bouton pour quitter vers le menu
    btn_menu = Button(frame_plateau, text = "Menu", command = fen_jeu.destroy, bg = "#f04747", fg = "white", font = ("Calibri", 13, "bold"), relief = "flat", cursor = "hand2", width = 10)
    btn_menu.grid(row = 3, column = 2, padx = 15, pady = 10)


    #Coup joué par l'IA si le joueur choisit de jouer les ronds
    if var_signe.get() == "O" :
        ia(plateau, "X")


#Création de la fenêtre menu
fen_menu = Tk()
fen_menu.geometry("500x150+650+300")
fen_menu.title("TicTacToe")
fen_menu.configure(bg="#2c2f33")

#Style commun texte et bouton
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
txt_Joueur = Label(fen_menu, text = "Selectionnez le nombre de joueurs :", **STYLE_TEXTE)
txt_Joueur.pack()

#Texte info --> X commence en premier
txt_Info = Label(fen_menu, text = "(X commence en 1er !)", **STYLE_TEXTE)
txt_Info.pack()

#Bouton pour séléctionner le nombre de joueurs
var_joueur = IntVar(value = 0)
var_signe = StringVar(value = "None")

#Frame de fen_menu afin d'afficher les boutons de selection du nombre de joueurs
frame_joueur = Frame(fen_menu, bg="#2c2f33")
frame_joueur.pack()

#Boutons sélection du nombre de joueurs
btn_Joueur_1 = Radiobutton(frame_joueur, text = "1 joueur", variable = var_joueur, value = 1, command = afficher_signe, bg = "#2c2f33", fg = "white", selectcolor = "#23272a",  font = ("Calibri", 12))
btn_Joueur_2 = Radiobutton(frame_joueur, text = "2 joueurs", variable = var_joueur, value = 2, command = afficher_signe, bg = "#2c2f33", fg = "white", selectcolor = "#23272a",  font = ("Calibri", 12))
btn_Joueur_1.pack(side = "left", padx = 30, anchor = "n")
btn_Joueur_2.pack(side = "left", padx = 30, anchor = "n")

#Frame de fen_menu afin d'afficher le texte et les boutons de sélection du signe
frame_signe_txt = Frame(fen_menu, bg="#2c2f33")
frame_signe_btn = Frame(fen_menu, bg="#2c2f33")
frame_action_signe = Frame(fen_menu, bg="#2c2f33")

#Texte pour le choix du signe
txt_Signe = Label(frame_signe_txt, text = "Choisissez votre signe :", **STYLE_TEXTE)
txt_Signe.pack(side = "left", padx = 30)

#Boutons pour le choix du signe
btn_croix = Radiobutton(frame_signe_btn, text = "X", variable = var_signe, value = "X", bg = "#2c2f33", fg = "white", selectcolor = "#23272a", font = ("Calibri", 12), command = afficher_signe)
btn_rond = Radiobutton(frame_signe_btn, text = "O", variable = var_signe, value = "O", bg = "#2c2f33", fg = "white", selectcolor = "#23272a", font = ("Calibri", 12), command = afficher_signe)
btn_croix.pack(side = "left", padx = 30)
btn_rond.pack(side = "left", padx = 30)

#Frame de fen_menu afin d'afficher les boutons pour lancer une partie et quitter le jeu si les conditions sont remplies
frame_action = Frame(fen_menu, bg="#2c2f33")
frame_action.pack(pady = 15)

#Les boutons pour quitter et lancer une partie
btn_quitter = Button(frame_action, text = "Quitter", command = fen_menu.destroy, bg = "#f04747", activebackground = "#c23a3a", fg = "white", font = ("Calibri", 12, "bold"), relief = "flat", cursor = "hand2", width = 12)
btn_Jouer = Button(frame_action, text = "Lancer la partie !", command = jeu, **STYLE_BUTTON)


if var_joueur.get() == 1 :
    btn_croix.pack_forget()
    btn_rond.pack_forget()

fen_menu.mainloop()