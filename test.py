# Rendre l'application responsive


import tkinter as tk

fen = tk.Tk()

fen.minsize(862, 490)

# Titre principal
titre_principale = tk.Label(fen, text="Gestionnaire d'une bibliothèque", font=("Courrier", 30))
titre_principale.grid(row=0, column=0, columnspan=2, sticky="nwse")
fen.rowconfigure(0, weight=1)
fen.columnconfigure(0, weight=1)


# Frame qui va gérer la section rechercher dans la base
frame_rechercher = tk.LabelFrame(fen, text="Rechercher dans la base", font=("Courrier", 22))
frame_rechercher.grid(row=1, column=0, pady=15, padx=15, sticky="nwse")
fen.rowconfigure(1, weight=1)
fen.columnconfigure(0, weight=1)

rechercher_livres_empruntes = tk.Button(frame_rechercher, text="Rechercher les livres empruntés par une personne ",
                                        width=40, height=2, font=("Courrier", 11))
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


def test():
    print(fen.winfo_width(), fen.winfo_height())


rechercher_livres_empruntes.bind("<Visibility>", lambda event: test())


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