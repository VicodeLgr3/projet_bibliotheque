import tkinter as tk
import tkinter.scrolledtext as tkscroll
from tkinter import messagebox
import datetime
import sqlite3
import random
import string


def convert_date(x):
    month = {
        1: "Janvier",
        2: "Février",
        3: "Mars",
        4: "Avril",
        5: "Mai",
        6: "Juin",
        7: "Juillet",
        8: "Août",
        9: "Septembre",
        10: "Octobre",
        11: "Novembre",
        12: "Décembre"
    }
    return month[x]


def date():
    date_today = datetime.datetime.now()
    day = date_today.day
    month = date_today.month
    year = date_today.year
    return f"{day} {convert_date(month)} {year}"


def center_window(fen, width: int = 600, height: int = 400):
    x_coordinate = int((fen.winfo_screenwidth() / 2) - (width / 2))
    y_coordinate = int((fen.winfo_screenheight() / 2) - (height / 2) - 30)
    return f"{width}x{height}+{x_coordinate}+{y_coordinate}"


class App:
    def __init__(self):
        self.db_conn = sqlite3.connect('bibliotheque.db')
        self.db_cursor = self.db_conn.cursor()

        self.fen = tk.Tk()
        self.fen.geometry(center_window(self.fen, 805, 500))
        self.fen.resizable(False, False)
        self.fen.title(f'Bibliothèques - {date()}')
        self.fen.iconbitmap('icone.ico')
        self.couleur = "#2E64FE"
        self.fen.config(bg=self.couleur)

        # Titre principal
        titre_principale = tk.Label(self.fen, text="Gestionnaire d'une bibliothèque", bg=self.couleur,
                                    font=("Courrier", 30))
        titre_principale.grid(row=0, column=0, columnspan=2)

        # Frame qui va gérer la section rechercher dans la base
        frame_rechercher = tk.LabelFrame(self.fen, text="Rechercher dans la base", bg=self.couleur,
                                         font=("Courrier", 22))
        frame_rechercher.grid(row=1, column=0, pady=15, padx=15)

        rechercher_livres_empruntes = tk.Button(frame_rechercher,
                                                text="Rechercher les livres empruntés par une personne ", width=40,
                                                height=2, font=("Courrier", 11),
                                                command=self.recherche_livres_empruntes_graphique)
        rechercher_livres_empruntes.pack(pady=2)
        rechercher_livre_emprunte_isbn = tk.Button(frame_rechercher, text="Rechercher un livre emprunté par ISBN",
                                                   width=40, height=2, font=("Courrier", 11),
                                                   command=self.recherche_livre_isbn_graphique)
        rechercher_livre_emprunte_isbn.pack(pady=2)
        affiche_personnes_retard = tk.Button(frame_rechercher, text="Afficher les personnes en retard", width=40,
                                             height=2, font=("Courrier", 11), command=self.retardataires_graphique)
        affiche_personnes_retard.pack(pady=2)
        rechercher_livre_mot_cle = tk.Button(frame_rechercher, text="Rechercher un livre par mot clé", width=40,
                                             height=2, font=("Courrier", 11),
                                             command=self.recherche_isbn_mot_cle_graphique)
        rechercher_livre_mot_cle.pack(pady=2)

        # Frame qui va gérer la section insertion dans la base
        frame_inserer = tk.LabelFrame(self.fen, text="Insérer dans la base", bg=self.couleur, font=("Courrier", 22))
        frame_inserer.grid(row=1, column=1, pady=11, padx=15)

        inserer_usager = tk.Button(frame_inserer, text="Insérer un usager", width=40, height=2, font=("Courrier", 11),
                                   command=self.inserer_usager_graphique)
        inserer_usager.pack(pady=2)
        inserer_livre = tk.Button(frame_inserer, text="Insérer un livre", width=40, height=2, font=("Courrier", 11),
                                  command=self.inserer_livre_graphique)
        inserer_livre.pack(pady=2)
        inserer_emprunt = tk.Button(frame_inserer, text="Insérer un emprunt", width=40, height=2, font=("Courrier", 11),
                                    command=self.inserer_emprunt_graphique)
        inserer_emprunt.pack(pady=2)

        # Frame qui va gérer la section mise à jour de la base
        frame_mise_a_jour = tk.LabelFrame(self.fen, text="Mettre à jour la base", bg=self.couleur,
                                          font=("Courrier", 22))
        frame_mise_a_jour.grid(row=2, column=0, pady=11, padx=15)

        changer_date_retour_livre = tk.Button(frame_mise_a_jour, text="Changer la date de retour d'un livre", width=40,
                                              height=2, font=("Courrier", 11))
        changer_date_retour_livre.pack(pady=2)
        changer_donnee_usager = tk.Button(frame_mise_a_jour, text="Changer une donnée d'un usager", width=40, height=2,
                                          font=("Courrier", 11))
        changer_donnee_usager.pack(pady=2)

        # Frame qui va gérer la section supprimer dans la base
        frame_supprimer = tk.LabelFrame(self.fen, text="Supprimer dans la base", bg=self.couleur, font=("Courrier", 22))
        frame_supprimer.grid(row=2, column=1, pady=15, padx=15)

        supprimer_livre = tk.Button(frame_supprimer, text="Supprimer un livre de la base", width=40, height=2,
                                    font=("Courrier", 11))
        supprimer_livre.pack(pady=2)
        supprimer_emprunt = tk.Button(frame_supprimer, text="Supprimer un emprunt", width=40, height=2,
                                      font=("Courrier", 11))
        supprimer_emprunt.pack(pady=2)

        self.fen.mainloop()

    def recherche_livres_empruntes_graphique(self):

        def rechercher_livres_empruntes_fonction():
            scrolledtext_livres_empruntes.delete("1.0", tk.END)
            code_barre = entry_code_barre.get()
            if len(code_barre) != 0 and len(code_barre) == 15:
                self.db_cursor.execute('SELECT * FROM LIVRE JOIN EMPRUNT ON LIVRE.isbn = EMPRUNT.isbn '
                                       'WHERE code_barre = ?', [code_barre, ])
                livres_empruntes = self.db_cursor.fetchall()
                if len(livres_empruntes) != 0:
                    for i in range(0, len(livres_empruntes)):
                        scrolledtext_livres_empruntes.insert(tk.END,
                                                             f"Livre n°{i + 1}\nTitre : {livres_empruntes[i][0]}\n"
                                                             f"Editeur : {livres_empruntes[i][1]}\n"
                                                             f"Année : {livres_empruntes[i][2]}\n"
                                                             f"Isbn : {livres_empruntes[i][3]}\n\n")
                else:
                    scrolledtext_livres_empruntes.insert(tk.END, "Aucun livre emprunté !")
            entry_code_barre.delete(0, tk.END)

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"500x400+{self.fen.winfo_x() + 150}+{self.fen.winfo_y() + 50}")
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.Frame(fen)
        frame.pack(expand=tk.YES)

        label_code_barre = tk.Label(frame, text="Code barre : ", font=("Courrier", 14))
        label_code_barre.grid(row=0, column=0, sticky="e")
        entry_code_barre = tk.Entry(frame, font=("Courrier", 13), width=20)
        entry_code_barre.grid(row=0, column=1, sticky="w")
        button_valider = tk.Button(frame, text="Valider", font=("Courrier", 12),
                                   command=rechercher_livres_empruntes_fonction)
        button_valider.grid(row=0, column=2, sticky="")

        scrolledtext_livres_empruntes = tkscroll.ScrolledText(frame, width=40, height=18, font=("Courrier", 12))
        scrolledtext_livres_empruntes.grid(row=1, column=0, columnspan=3)

        entry_code_barre.bind("<Return>", lambda event: rechercher_livres_empruntes_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def recherche_livre_isbn_graphique(self):

        def rechercher_livre_isbn_fonction():
            scrolledtext_emprunteur.delete("1.0", tk.END)
            isbn = entry_isbn.get()
            if len(isbn) != 0 and len(isbn) == 14:
                self.db_cursor.execute('SELECT * FROM USAGER JOIN EMPRUNT ON USAGER.code_barre = EMPRUNT.code_barre '
                                       'WHERE EMPRUNT.isbn = ?', [isbn, ])
                emprunteur = self.db_cursor.fetchall()
                if len(emprunteur) != 0:
                    scrolledtext_emprunteur.insert(tk.END, f"Nom : {emprunteur[0][0]}\nPrénom : {emprunteur[0][1]}\n"
                                                           f"Adresse : {emprunteur[0][2]}\n"
                                                           f"Code postal : {emprunteur[0][3]}\n "
                                                           f"Ville : {emprunteur[0][4]}\nEmail : {emprunteur[0][5]}\n"
                                                           f"Code barre : {emprunteur[0][6]}")
                else:
                    scrolledtext_emprunteur.insert(tk.END, "Personne n'a emprunté ce livre !")
            entry_isbn.delete(0, tk.END)

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x250+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 100}")
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.Frame(fen)
        frame.pack(expand=tk.YES)

        label_isbn = tk.Label(frame, text="ISBN : ", font=("Courrier", 14))
        label_isbn.grid(row=0, column=0, sticky="e")
        entry_isbn = tk.Entry(frame, font=("Courrier", 13), width=24)
        entry_isbn.grid(row=0, column=1, sticky="w")
        button_valider = tk.Button(frame, text="Valider", font=("Courrier", 12),
                                   command=rechercher_livre_isbn_fonction)
        button_valider.grid(row=0, column=2, sticky="")

        scrolledtext_emprunteur = tkscroll.ScrolledText(frame, width=40, height=10, font=("Courrier", 12))
        scrolledtext_emprunteur.grid(row=1, column=0, columnspan=3)

        entry_isbn.bind("<Return>", lambda event: rechercher_livre_isbn_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def retardataires_graphique(self):

        def retardataires_fonction():
            date_du_jour = str(datetime.datetime.now()).split(" ")[0]
            self.db_cursor.execute('SELECT DISTINCT USAGER.nom, USAGER.prenom, USAGER.adresse, USAGER.cp, '
                                   'USAGER.ville, USAGER.email, USAGER.code_barre FROM USAGER JOIN EMPRUNT ON '
                                   'EMPRUNT.code_barre = USAGER.code_barre WHERE EMPRUNT.retour < ?', [date_du_jour, ])
            personnes = self.db_cursor.fetchall()
            self.db_cursor.execute('SELECT * FROM EMPRUNT WHERE retour < ?', [date_du_jour, ])
            retards = self.db_cursor.fetchall()
            if len(retards) != 0:
                for i in range(0, len(personnes)):
                    scrolledtext_retardataires.insert(tk.END, f"Nom : {personnes[i][0]}\nPrénom : {personnes[i][1]}\n"
                                                              f"Adresse : {personnes[i][2]}\n"
                                                              f"Code postal : {personnes[i][3]}\n"
                                                              f"Ville : {personnes[i][4]}\n"
                                                              f"Email : {personnes[i][5]}\n"
                                                              f"Code barre : {personnes[i][6]}\n")
                    for r in range(0, len(retards)):
                        if personnes[i][6] == retards[r][0]:
                            scrolledtext_retardataires.insert(tk.END, f"Isbn : {retards[r][1]}\n")
                    scrolledtext_retardataires.insert(tk.END, "\n")

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"500x300+{self.fen.winfo_x() + 150}+{self.fen.winfo_y() + 100}")
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        scrolledtext_retardataires = tkscroll.ScrolledText(fen, font=("Courrier", 12))
        scrolledtext_retardataires.pack(expand=tk.YES)

        fen.after(0, lambda: retardataires_fonction())
        fen.mainloop()

    def recherche_isbn_mot_cle_graphique(self):

        def recherche_isbn_mot_cle_fonction():
            scrolledtext_livres.delete("1.0", tk.END)
            mot_cle = entry_mot_cle.get()
            if len(mot_cle) != 0:
                self.db_cursor.execute('SELECT * FROM LIVRE WHERE titre LIKE ?', [f"%{mot_cle}%", ])
                livres = self.db_cursor.fetchall()
                if len(livres) != 0:
                    for i in range(0, len(livres)):
                        scrolledtext_livres.insert(tk.END, f"Livre n°{i+1}\nTitre : {livres[i][0]}\n"
                                                           f"Editeur : {livres[i][1]}\nAnnée : {livres[i][2]}\n"
                                                           f"Isbn : {livres[i][3]}\n\n")
                else:
                    scrolledtext_livres.insert(tk.END, "Aucun livre trouvé !")

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"500x400+{self.fen.winfo_x() + 150}+{self.fen.winfo_y() + 50}")
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.Frame(fen)
        frame.pack(expand=tk.YES)

        label_mot_cle = tk.Label(frame, text="Mot clé : ", font=("Courrier", 14))
        label_mot_cle.grid(row=0, column=0, sticky="e")
        entry_mot_cle = tk.Entry(frame, font=("Courrier", 13), width=20)
        entry_mot_cle.grid(row=0, column=1, sticky="w")
        button_valider = tk.Button(frame, text="Valider", font=("Courrier", 12),
                                   command=recherche_isbn_mot_cle_fonction)
        button_valider.grid(row=0, column=2, sticky="")

        scrolledtext_livres = tkscroll.ScrolledText(frame, width=40, height=18, font=("Courrier", 12))
        scrolledtext_livres.grid(row=1, column=0, columnspan=3)

        entry_mot_cle.bind("<KeyRelease>", lambda event: recherche_isbn_mot_cle_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def inserer_usager_graphique(self):

        def genere_code_barre():
            code_barre = "".join(random.choice(string.digits) for _ in range(random.randint(15, 15)))
            self.db_cursor.execute('SELECT * FROM USAGER WHERE code_barre = ?', [code_barre, ])
            data = self.db_cursor.fetchall()
            while len(data) != 0:
                code_barre = "".join(random.choice(string.digits) for _ in range(random.randint(15, 15)))
                self.db_cursor.execute('SELECT * FROM USAGER WHERE code_barre = ?', [code_barre, ])
                data = self.db_cursor.fetchall()
            return code_barre

        def inserer_usager_fonction():
            nom = entry_nom.get()
            prenom = entry_prenom.get()
            adresse = entry_adresse.get()
            cp = entry_cp.get()
            ville = entry_ville.get()
            email = entry_ville.get()
            code_barre = genere_code_barre()
            if len(nom) != 0 and len(prenom) != 0 and len(adresse) != 0 and len(cp) != 0 and len(ville) != 0 \
                    and len(email) != 0:
                data_usager = [nom, prenom, adresse, cp, ville, email, code_barre]
                self.db_cursor.execute('INSERT INTO USAGER VALUES (?,?,?,?,?,?,?)', data_usager)
                self.db_conn.commit()

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x300+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 100}")
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.LabelFrame(fen, text="Renseignez les informations sur la personne", font=("Courrier", 12))
        frame.pack(expand=tk.YES)

        label_nom = tk.Label(frame, text="Nom : ", font=("Courrier", 12))
        label_nom.grid(row=0, column=0, sticky="ne", pady=5)
        entry_nom = tk.Entry(frame, font=("Courrier", 11))
        entry_nom.grid(row=0, column=1)

        label_prenom = tk.Label(frame, text="Prénom : ", font=("Courrier", 12))
        label_prenom.grid(row=1, column=0, sticky="ne", pady=5)
        entry_prenom = tk.Entry(frame, font=("Courrier", 11))
        entry_prenom.grid(row=1, column=1)

        label_adresse = tk.Label(frame, text="Adresse : ", font=("Courrier", 12))
        label_adresse.grid(row=2, column=0, sticky="ne", pady=5)
        entry_adresse = tk.Entry(frame, font=("Courrier", 11))
        entry_adresse.grid(row=2, column=1)

        label_cp = tk.Label(frame, text="Code postal : ", font=("Courrier", 12))
        label_cp.grid(row=3, column=0, sticky="ne", pady=5)
        entry_cp = tk.Entry(frame, font=("Courrier", 11))
        entry_cp.grid(row=3, column=1)

        label_ville = tk.Label(frame, text="Ville : ", font=("Courrier", 12))
        label_ville.grid(row=4, column=0, sticky="ne", pady=5)
        entry_ville = tk.Entry(frame, font=("Courrier", 11))
        entry_ville.grid(row=4, column=1)

        label_email = tk.Label(frame, text="Adresse mail : ", font=("Courrier", 12))
        label_email.grid(row=5, column=0, sticky="ne", pady=5)
        entry_email = tk.Entry(frame, font=("Courrier", 11))
        entry_email.grid(row=5, column=1)

        button_validate = tk.Button(fen, text="Ajouter", font=("Courrier", 12), command=inserer_usager_fonction)
        button_validate.pack(pady=10)

        fen.bind("<Return>", lambda event: inserer_usager_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def inserer_livre_graphique(self):

        def inserer_livre_fonction():
            titre = entry_titre.get()
            editeur = entry_editeur.get()
            annee = entry_annee.get()
            isbn = entry_isbn.get()
            if len(titre) != 0 and len(editeur) != 0 and len(annee) != 0 and len(isbn) != 0:
                data_livre = [titre, editeur, annee, isbn]
                self.db_cursor.execute('INSERT INTO LIVRE VALUES(?,?,?,?)', data_livre)
                self.db_conn.commit()

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x250+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 120}")
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.LabelFrame(fen, text="Renseignez les informations sur le livre", font=("Courrier", 12))
        frame.pack(expand=tk.YES)

        label_titre = tk.Label(frame, text="Titre : ", font=("Courrier", 12))
        label_titre.grid(row=0, column=0, sticky="ne", pady=5)
        entry_titre = tk.Entry(frame, font=("Courrier", 11))
        entry_titre.grid(row=0, column=1)

        label_editeur = tk.Label(frame, text="Editeur : ", font=("Courrier", 12))
        label_editeur.grid(row=1, column=0, sticky="ne", pady=5)
        entry_editeur = tk.Entry(frame, font=("Courrier", 11))
        entry_editeur.grid(row=1, column=1)

        label_annee = tk.Label(frame, text="Année : ", font=("Courrier", 12))
        label_annee.grid(row=2, column=0, sticky="ne", pady=5)
        entry_annee = tk.Entry(frame, font=("Courrier", 11))
        entry_annee.grid(row=2, column=1)

        label_isbn = tk.Label(frame, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=3, column=0, sticky="ne", pady=5)
        entry_isbn = tk.Entry(frame, font=("Courrier", 11))
        entry_isbn.grid(row=3, column=1)

        button_validate = tk.Button(fen, text="Ajouter", font=("Courrier", 12), command=inserer_livre_fonction)
        button_validate.pack(pady=10)

        fen.bind("<Return>", lambda event: inserer_livre_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def inserer_emprunt_graphique(self):
        def inserer_emprunt_fonction():
            code_barre = entry_code_barre.get()
            isbn = entry_isbn.get()
            retour = entry_retour.get()
            if len(code_barre) != 0 and len(isbn) != 0 and len(retour) != 0:
                self.db_cursor.execute('SELECT * FROM USAGER WHERE code_barre = ?', [code_barre, ])
                if len(self.db_cursor.fetchall()) != 0:
                    self.db_cursor.execute('SELECT * FROM LIVRE WHERE isbn = ?', [isbn, ])
                    if len(self.db_cursor.fetchall()) != 0:
                        try:
                            self.db_cursor.execute('INSERT INTO EMPRUNT VALUES(?,?,?)', [code_barre, isbn, retour])
                        except sqlite3.IntegrityError:
                            messagebox.showerror("Emprunt existant", f"{code_barre} emprunte déjà le livre", parent=fen)
                        else:
                            messagebox.showinfo("Livre insérer", "Le livre a été insérer", parent=fen)
                        self.db_conn.commit()
                    else:
                        messagebox.showerror("Isbn invalide", "L'isbn ne correspond à aucun livre", parent=fen)
                else:
                    messagebox.showerror("Code barre invalide", "Le code barre ne correspond à personne", parent=fen)

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x200+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 150}")
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.LabelFrame(fen, text="Renseignez les informations sur l'emprunt", font=("Courrier", 12))
        frame.pack(expand=tk.YES)

        label_code_barre = tk.Label(frame, text="Code barre : ", font=("Courrier", 12))
        label_code_barre.grid(row=0, column=0, sticky="ne", pady=5)
        entry_code_barre = tk.Entry(frame, font=("Courrier", 11))
        entry_code_barre.grid(row=0, column=1)

        label_isbn = tk.Label(frame, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=1, column=0, sticky="ne", pady=5)
        entry_isbn = tk.Entry(frame, font=("Courrier", 11))
        entry_isbn.grid(row=1, column=1)

        label_retour = tk.Label(frame, text="Date de retour : ", font=("Courrier", 12))
        label_retour.grid(row=2, column=0, sticky="ne", pady=5)
        entry_retour = tk.Entry(frame, font=("Courrier", 11))
        entry_retour.grid(row=2, column=1)

        button_validate = tk.Button(fen, text="Ajouter", font=("Courrier", 12), command=inserer_emprunt_fonction)
        button_validate.pack(pady=10)

        fen.bind("<Return>", lambda event: inserer_emprunt_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()


if __name__ == '__main__':
    app = App()
