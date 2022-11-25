# Rendre l'application responsive


import tkinter as tk
import platform


def center_window(win, width: int = 600, height: int = 400):
    x_coordinate = int((win.winfo_screenwidth() / 2) - (width / 2))
    y_coordinate = int((win.winfo_screenheight() / 2) - (height / 2) - 30)
    return f"{width}x{height}+{x_coordinate}+{y_coordinate}"


def place_toplevel(win, toplevel, width: int, height: int):
    win_width = win.winfo_width()
    win_height = win.winfo_height()
    win_x = win.winfo_x()
    win_y = win.winfo_y()
    win_screenwidth = win.winfo_screenwidth()
    x_coordinate = int((win_width / 2) - (width / 2) + win_x)
    y_coordinate = int((win_height / 2) - (height / 2) + win_y)
    espace_restant = win_screenwidth - (win_x + win_width)
    if platform.system() == "Linux":
        toplevel.geometry(f"{width}x{height}+{win_x}+{win_y - 35}")
    elif platform.system() == "Windows":
        # Permet d'afficher la fenêtre de façon à tout le temps la voir sur l'écran
        if win_x + win_width + width < win_screenwidth:
            toplevel.geometry(f"{width}x{height}+{win_x + win_width}+{win_y}")  # À droite de l'écran
        elif win_screenwidth  - win_width - width - espace_restant >= 0:
            toplevel.geometry(f"{width}x{height}+{win_x - width}+{win_y}")  # À gauche de l'écran
        else:
            toplevel.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")  # Au centre de l'écran


fen = tk.Tk()

fen_width, fen_height = 844, 490
fen.geometry(center_window(fen, fen_width, fen_height))
fen.minsize(844, 490)

# Titre principal
titre_principale = tk.Label(fen, text="Gestionnaire d'une bibliothèque", font=("Courrier", 30))
titre_principale.grid(row=0, column=0, columnspan=2, sticky="nwse")
fen.rowconfigure(0, weight=1)
fen.columnconfigure(0, weight=1)


# Frame qui va gérer la section rechercher dans la base
frame_rechercher = tk.LabelFrame(fen, text="Rechercher dans la base", font=("Courrier", 22))
frame_rechercher.grid(row=1, column=0, pady=15, padx=15, sticky="nwse")
fen.rowconfigure(1, weight=1)
# fen.columnconfigure(0, weight=1)


def test():
    win = tk.Toplevel()
    width = 400
    height = 300
    place_toplevel(fen, win, width, height)
    # x_coordinate = int((fen.winfo_width() / 2) - (width / 2) + fen.winfo_x())
    # y_coordinate = int((fen.winfo_height() / 2) - (height / 2) + fen.winfo_y())
    # espace_restant = fen.winfo_screenwidth() - (fen.winfo_x() + fen.winfo_width())
    # if platform.system() == "Linux":
    #     win.geometry(f"{width}x{height}+{fen.winfo_x()}+{fen.winfo_y() - 35}")
    # elif platform.system() == "Windows":
    #     # Permet d'afficher la fenêtre de façon à tout le temps la voir sur l'écran
    #     if fen.winfo_x() + fen.winfo_width() + width < fen.winfo_screenwidth():
    #         win.geometry(f"{width}x{height}+{fen.winfo_x() + fen.winfo_width()}+{fen.winfo_y()}")  # À droite de l'écran
    #     elif fen.winfo_screenwidth() - fen.winfo_width() - width - espace_restant >= 0:
    #         win.geometry(f"{width}x{height}+{fen.winfo_x() - width}+{fen.winfo_y()}")  # À gauche de l'écran
    #     else:
    #         win.geometry(f"{width}x{height}+{x_coordinate}+{y_coordinate}")  # Au centre de l'écran
    win.mainloop()


rechercher_livres_empruntes = tk.Button(frame_rechercher, text="Rechercher les livres empruntés par une personne ",
                                        width=40, height=2, font=("Courrier", 11), command=test)
rechercher_livres_empruntes.grid(row=0, column=0, sticky="nwse")
frame_rechercher.rowconfigure(0, weight=1)
frame_rechercher.columnconfigure(0, weight=1)

rechercher_livre_emprunte_isbn = tk.Button(frame_rechercher, text="Rechercher un livre emprunté par ISBN",
                                                   width=40, height=2, font=("Courrier", 11))
rechercher_livre_emprunte_isbn.grid(row=1, column=0, sticky="nwse")
frame_rechercher.rowconfigure(1, weight=1)
frame_rechercher.columnconfigure(0, weight=1)
affiche_personnes_retard = tk.Button(frame_rechercher, text="Afficher les personnes en retard", width=40,
                                             height=2, font=("Courrier", 11))
affiche_personnes_retard.grid(row=2, column=0, sticky="nwse")
frame_rechercher.rowconfigure(2, weight=1)
frame_rechercher.columnconfigure(0, weight=1)
rechercher_livre_mot_cle = tk.Button(frame_rechercher, text="Rechercher un livre par mot clé", width=40,
                                             height=2, font=("Courrier", 11))
rechercher_livre_mot_cle.grid(row=3, column=0, sticky="nwse")
frame_rechercher.rowconfigure(3, weight=1)
frame_rechercher.columnconfigure(0, weight=1)


# Frame qui va gérer la section insertion dans la base
frame_inserer = tk.LabelFrame(fen, text="Insérer dans la base", font=("Courrier", 22))
frame_inserer.grid(row=1, column=1, pady=15, padx=15, sticky="nwse")
fen.rowconfigure(1, weight=1)
fen.columnconfigure(1, weight=1)

inserer_usager = tk.Button(frame_inserer, text="Insérer un usager", width=40, height=2, font=("Courrier", 11))
inserer_usager.grid(row=0, column=0, sticky="nwse")
frame_inserer.rowconfigure(0, weight=1)
frame_inserer.columnconfigure(0, weight=1)
inserer_livre = tk.Button(frame_inserer, text="Insérer un livre", width=40, height=2, font=("Courrier", 11))
inserer_livre.grid(row=1, column=0, sticky="nwse")
frame_inserer.rowconfigure(1, weight=1)
frame_inserer.columnconfigure(0, weight=1)
inserer_emprunt = tk.Button(frame_inserer, text="Insérer un emprunt", width=40, height=2, font=("Courrier", 11))
inserer_emprunt.grid(row=2, column=0, sticky="nwse")
frame_inserer.rowconfigure(2, weight=1)
frame_inserer.columnconfigure(0, weight=1)


# Frame qui va gérer la section mise à jour de la base
frame_mise_a_jour = tk.LabelFrame(fen, text="Mettre à jour la base", font=("Courrier", 22))
frame_mise_a_jour.grid(row=2, column=0, pady=15, padx=15, sticky="nwse")
fen.rowconfigure(2, weight=1)
fen.columnconfigure(0, weight=1)

changer_date_retour_livre = tk.Button(frame_mise_a_jour, text="Changer la date de retour d'un livre", width=40,
                                              height=2, font=("Courrier", 11))
changer_date_retour_livre.grid(row=0, column=0, sticky="nwse")
frame_mise_a_jour.rowconfigure(0, weight=1)
frame_mise_a_jour.columnconfigure(0, weight=1)
changer_donnee_usager = tk.Button(frame_mise_a_jour, text="Changer une donnée d'un usager", width=40, height=2,
                                          font=("Courrier", 11))
changer_donnee_usager.grid(row=1, column=0, sticky="nwse")
frame_mise_a_jour.rowconfigure(1, weight=1)
frame_mise_a_jour.columnconfigure(0, weight=1)


# Frame qui va gérer la section supprimer dans la base
frame_supprimer = tk.LabelFrame(fen, text="Supprimer dans la base", font=("Courrier", 22))
frame_supprimer.grid(row=2, column=1, pady=15, padx=15, sticky="nwse")
fen.rowconfigure(2, weight=1)
fen.columnconfigure(1, weight=1)

supprimer_livre = tk.Button(frame_supprimer, text="Supprimer un livre de la base", width=40, height=2,
                                    font=("Courrier", 11))
supprimer_livre.grid(row=0, column=0, sticky="nwse")
frame_supprimer.rowconfigure(0, weight=1)
frame_supprimer.columnconfigure(0, weight=1)
supprimer_emprunt = tk.Button(frame_supprimer, text="Supprimer un emprunt", width=40, height=2,
                                      font=("Courrier", 11))
supprimer_emprunt.grid(row=1, column=0, sticky="nwse")
frame_supprimer.rowconfigure(1, weight=1)
frame_supprimer.columnconfigure(0, weight=1)

fen.mainloop()