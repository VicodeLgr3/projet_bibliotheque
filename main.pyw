import tkinter as tk
from tkinter import ttk
import tkinter.scrolledtext as tkscroll
from tkinter import messagebox
import tkcalendar as tkcal  # pip install tkcalendar
import pyqrcode  # pip install pyqrcode
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
                                              height=2, font=("Courrier", 11),
                                              command=self.mettre_a_jour_date_retour_livre_graphique)
        changer_date_retour_livre.pack(pady=2)
        changer_donnee_usager = tk.Button(frame_mise_a_jour, text="Changer une donnée d'un usager", width=40, height=2,
                                          font=("Courrier", 11), command=self.mettre_a_jour_donnee_usager_graphique)
        changer_donnee_usager.pack(pady=2)

        # Frame qui va gérer la section supprimer dans la base
        frame_supprimer = tk.LabelFrame(self.fen, text="Supprimer dans la base", bg=self.couleur, font=("Courrier", 22))
        frame_supprimer.grid(row=2, column=1, pady=15, padx=15)

        supprimer_livre = tk.Button(frame_supprimer, text="Supprimer un livre de la base", width=40, height=2,
                                    font=("Courrier", 11), command=self.supprimer_livre_graphique)
        supprimer_livre.pack(pady=2)
        supprimer_emprunt = tk.Button(frame_supprimer, text="Supprimer un emprunt", width=40, height=2,
                                      font=("Courrier", 11), command=self.supprimer_emprunt_graphique)
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
        fen.resizable(False, False)
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
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame = tk.Frame(fen)
        frame.pack(expand=tk.YES)

        label_mot_cle = tk.Label(frame, text="Mot clé : ", font=("Courrier", 14))
        label_mot_cle.grid(row=0, column=0, sticky="e")
        entry_mot_cle = tk.Entry(frame, font=("Courrier", 13), width=20)
        entry_mot_cle.grid(row=0, column=1, sticky="w")

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

            def affiche_code_barre_qrcode():
                fen_qrcode = tk.Toplevel(fen)
                fen_qrcode.geometry(f"300x260+{fen.winfo_x() + 50}+{fen.winfo_y() + 20}")
                fen_qrcode.transient(fen)
                fen_qrcode.grab_set()
                fen_qrcode.focus_set()

                img = tk.BitmapImage(data=pyqrcode.create(code_barre).xbm(scale=8))
                tk.Label(fen_qrcode, image=img).pack(expand=tk.YES)

                tk.Label(fen_qrcode, text=f"Le code barre est {code_barre}", font=("Courrier", 12)).pack(pady=5)

                fen_qrcode.mainloop()

            nom = entry_nom.get().upper()
            prenom = entry_prenom.get().upper()
            adresse = entry_adresse.get()
            cp = entry_cp.get()
            ville = entry_ville.get().title()
            email = entry_ville.get()
            code_barre = genere_code_barre()
            if len(nom) != 0 and len(prenom) != 0 and len(adresse) != 0 and len(cp) != 0 and len(ville) != 0 \
                    and len(email) != 0:
                data_usager = [nom, prenom, adresse, cp, ville, email, code_barre]
                self.db_cursor.execute('INSERT INTO USAGER VALUES (?,?,?,?,?,?,?)', data_usager)
                self.db_conn.commit()
                entry_nom.delete(0, tk.END)
                entry_prenom.delete(0, tk.END)
                entry_adresse.delete(0, tk.END)
                entry_cp.delete(0, tk.END)
                entry_ville.delete(0, tk.END)
                entry_email.delete(0, tk.END)
                affiche_code_barre_qrcode()

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x300+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 100}")
        fen.resizable(False, False)
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
                entry_titre.delete(0, tk.END)
                entry_editeur.delete(0, tk.END)
                entry_annee.delete(0, tk.END)
                entry_isbn.delete(0, tk.END)

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x250+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 120}")
        fen.resizable(False, False)
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
            retour = dateentry_retour.get()
            if len(code_barre) != 0 and len(isbn) != 0 and len(retour) != 0:
                self.db_cursor.execute('SELECT * FROM USAGER WHERE code_barre = ?', [code_barre, ])
                if len(self.db_cursor.fetchall()) != 0:
                    self.db_cursor.execute('SELECT * FROM LIVRE WHERE isbn = ?', [isbn, ])
                    if len(self.db_cursor.fetchall()) != 0:
                        try:
                            self.db_cursor.execute('INSERT INTO EMPRUNT VALUES(?,?,?)', [code_barre, isbn, retour])
                        except sqlite3.IntegrityError:
                            self.db_conn.commit()
                            messagebox.showerror("Emprunt existant", f"{code_barre} emprunte déjà le livre", parent=fen)
                        else:
                            self.db_conn.commit()
                            messagebox.showinfo("Livre insérer", "Le livre a été insérer", parent=fen)
                    else:
                        messagebox.showerror("Isbn invalide", "L'isbn ne correspond à aucun livre", parent=fen)
                else:
                    messagebox.showerror("Code barre invalide", "Le code barre ne correspond à personne", parent=fen)

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x200+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 150}")
        fen.resizable(False, False)
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
        dateentry_retour = tkcal.DateEntry(frame, font=("Courrier", 11), date_pattern="yyyy-mm-dd")
        dateentry_retour.grid(row=2, column=1)

        button_validate = tk.Button(fen, text="Ajouter", font=("Courrier", 12), command=inserer_emprunt_fonction)
        button_validate.pack(pady=10)

        fen.bind("<Return>", lambda event: inserer_emprunt_fonction())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def mettre_a_jour_date_retour_livre_graphique(self):

        def affiche_isbn_avec_code_barre():
            combobox_isbn.set("")
            code_barre = combobox_code_barre.get()
            if len(code_barre) != 0:
                self.db_cursor.execute('SELECT isbn FROM EMPRUNT WHERE code_barre = ?', [code_barre, ])
                isbn = [x for x in self.db_cursor.fetchall()]
                combobox_isbn["values"] = isbn
                combobox_isbn.set(isbn[0])

        def affiche_date_avec_isbn():
            isbn = combobox_isbn.get()
            if len(isbn) != 0:
                self.db_cursor.execute('SELECT retour FROM EMPRUNT WHERE isbn = ?', [isbn, ])
                date_actuelle = self.db_cursor.fetchall()
                label_date_actuelle["text"] = date_actuelle[0]
                label_isbn_view["text"] = isbn
            else:
                messagebox.showinfo("Informations manquantes", "Veuillez renseignez toutes les informations",
                                    parent=fen)

        def mettre_a_jour_date_retour_livre_fonction():
            isbn = label_isbn_view["text"]
            nouvelle_date = dateentry_date_nouvelle.get()
            if len(isbn) != 0:
                self.db_cursor.execute('UPDATE EMPRUNT SET retour = ? WHERE isbn = ?', [nouvelle_date, isbn])
                self.db_conn.commit()
                combobox_code_barre.set("")
                combobox_isbn.set("")
                combobox_isbn["values"] = []
                label_isbn_view["text"] = ""
                label_date_actuelle["text"] = ""
            else:
                messagebox.showinfo("Informations manquantes", "Renseignez les informations manquantes pour continuer")

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"450x250+{self.fen.winfo_x() + 180}+{self.fen.winfo_y() + 120}")
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        label_info = tk.Label(fen, text="Appuyer sur la touche 'Entrée' pour valider vos choix", font=("Courrier", 10))
        label_info.pack()

        frame_rechercher_emprunt = tk.LabelFrame(fen, text="Rechercher l'emprunt", font=("Courrier", 12))
        frame_rechercher_emprunt.pack(expand=tk.YES)

        frame_changer_emprunt = tk.LabelFrame(fen, text="Changer la date de l'emprunt", font=("Courrier", 12))
        frame_changer_emprunt.pack(expand=tk.YES)

        label_code_barre = tk.Label(frame_rechercher_emprunt, text="Code barre : ", font=("Courrier", 12))
        label_code_barre.grid(row=0, column=0, sticky="ne", pady=5)

        self.db_cursor.execute('SELECT DISTINCT code_barre FROM EMPRUNT')
        combobox_code_barre = ttk.Combobox(frame_rechercher_emprunt, values=[x for x in self.db_cursor.fetchall()],
                                           font=("Courrier", 12), state="readonly")
        combobox_code_barre.grid(row=0, column=1)

        label_isbn = tk.Label(frame_rechercher_emprunt, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=1, column=0, sticky="ne", pady=5)

        combobox_isbn = ttk.Combobox(frame_rechercher_emprunt, font=("Courrier", 12), state="readonly")
        combobox_isbn.grid(row=1, column=1)

        label_isbn = tk.Label(frame_changer_emprunt, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=0, column=0, sticky="ne", pady=5)

        label_isbn_view = tk.Label(frame_changer_emprunt, font=("Courrier", 12))
        label_isbn_view.grid(row=0, column=1)

        label_date_actuelle_ = tk.Label(frame_changer_emprunt, text="Date actuelle : ", font=("Courrier", 12))
        label_date_actuelle_.grid(row=1, column=0, sticky="ne", pady=5)

        label_date_actuelle = tk.Label(frame_changer_emprunt, font=("Courrier", 12))
        label_date_actuelle.grid(row=1, column=1)

        label_date_nouvelle = tk.Label(frame_changer_emprunt, text="Nouvelle date : ", font=("Courrier", 12))
        label_date_nouvelle.grid(row=2, column=0, sticky="ne", pady=5)

        dateentry_date_nouvelle = tkcal.DateEntry(frame_changer_emprunt, date_pattern="yyyy-mm-dd")
        dateentry_date_nouvelle.grid(row=2, column=1)

        button_validate = tk.Button(frame_changer_emprunt, text="Changer", font=("Courrier", 12),
                                    command=mettre_a_jour_date_retour_livre_fonction)
        button_validate.grid(row=2, column=2)

        combobox_code_barre.bind("<Return>", lambda event: affiche_isbn_avec_code_barre())
        combobox_isbn.bind("<Return>", lambda event: affiche_date_avec_isbn())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def mettre_a_jour_donnee_usager_graphique(self):

        def affiche_usager_avec_code_barre():
            code_barre = combobox_code_barre.get()
            if len(code_barre) != 0:
                self.db_cursor.execute('SELECT * FROM USAGER WHERE code_barre = ?', [code_barre, ])
                data_usager = self.db_cursor.fetchall()[0]
                label_nom_result["text"] = data_usager[0]
                label_prenom_result["text"] = data_usager[1]
                label_adresse_result["text"] = data_usager[2]
                label_code_postal_result["text"] = data_usager[3]
                label_ville_result["text"] = data_usager[4]
                label_email_result["text"] = data_usager[5]
                label_code_barre_result["text"] = data_usager[6]
            else:
                messagebox.showinfo("Code barre manquant", "Renseignez un code barre pour continuer", parent=fen)

        def changer_nom_graphique():

            def changer_nom_fonction():
                new_nom = entry_nouveau_nom.get().upper()
                if len(new_nom) != 0:
                    self.db_cursor.execute('UPDATE USAGER SET nom = ? WHERE code_barre = ?',
                                           [new_nom, label_code_barre_result["text"]])
                    self.db_conn.commit()
                    entry_nouveau_nom.delete(0, tk.END)
                    label_nom_result["text"] = new_nom
                    fen_nom.destroy()

            if len(label_code_barre_result["text"]) != 0:
                fen_nom = tk.Toplevel(fen)
                if fen.winfo_x() + 600 + 300 < self.fen.winfo_screenwidth():
                    fen_nom.geometry(f"300x150+{fen.winfo_x() + 600}+{fen.winfo_y()}")
                else:
                    fen_nom.geometry(f"300x150+{fen.winfo_x() - 300}+{fen.winfo_y()}")
                fen_nom.resizable(False, False)
                fen_nom.transient(fen)
                fen_nom.grab_set()
                fen_nom.focus_set()

                frame = tk.LabelFrame(fen_nom, text="Changement de nom", font=("Courrier", 12))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Nom actuelle : ", font=("Courrier", 12)).grid(row=0, column=0,
                                                                                    sticky="ne", pady=5)
                tk.Label(frame, text=label_nom_result["text"], font=("Courrier", 12)).grid(row=0, column=1, sticky="w")

                tk.Label(frame, text="Nouveau nom : ", font=("Courrier", 12)).grid(row=1, column=0, sticky="ne", pady=5)

                entry_nouveau_nom = tk.Entry(frame, font=("Courrier", 11))
                entry_nouveau_nom.grid(row=1, column=1, sticky="w")

                tk.Button(fen_nom, text="Valider le changement", font=("Courrier", 12),
                          command=changer_nom_fonction).pack(pady=5)

                fen_nom.mainloop()

        def changer_prenom_graphique():

            def changer_prenom_fonction():
                new_prenom = entry_nouveau_prenom.get().upper()
                if len(new_prenom) != 0:
                    self.db_cursor.execute('UPDATE USAGER SET prenom = ? WHERE code_barre = ?',
                                           [new_prenom, label_code_barre_result["text"]])
                    self.db_conn.commit()
                    entry_nouveau_prenom.delete(0, tk.END)
                    label_prenom_result["text"] = new_prenom
                    fen_prenom.destroy()

            if len(label_code_barre_result["text"]) != 0:
                fen_prenom = tk.Toplevel(fen)
                if fen.winfo_x() + 600 + 310 < self.fen.winfo_screenwidth():
                    fen_prenom.geometry(f"310x150+{fen.winfo_x() + 600}+{fen.winfo_y()}")
                else:
                    fen_prenom.geometry(f"310x150+{fen.winfo_x() - 310}+{fen.winfo_y()}")
                fen_prenom.resizable(False, False)
                fen_prenom.transient(fen)
                fen_prenom.grab_set()
                fen_prenom.focus_set()

                frame = tk.LabelFrame(fen_prenom, text="Changement de prénom", font=("Courrier", 12))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Prénom actuelle : ", font=("Courrier", 12)).grid(row=0, column=0, sticky="ne",
                                                                                       pady=5)

                tk.Label(frame, text=label_prenom_result["text"], font=("Courrier", 12)).grid(row=0, column=1,
                                                                                              sticky="w")

                tk.Label(frame, text="Nouveau prénom : ", font=("Courrier", 12)).grid(row=1, column=0, sticky="ne",
                                                                                      pady=5)

                entry_nouveau_prenom = tk.Entry(frame, font=("Courrier", 11))
                entry_nouveau_prenom.grid(row=1, column=1, sticky="w")

                tk.Button(fen_prenom, text="Valider le changement", font=("Courrier", 12),
                          command=changer_prenom_fonction).pack(pady=5)

                fen_prenom.mainloop()

        def changer_adresse_graphique():

            def changer_adresse_fonction():
                new_adresse = entry_nouvelle_adresse.get()
                if len(new_adresse) != 0:
                    self.db_cursor.execute('UPDATE USAGER SET adresse = ? WHERE code_barre = ?',
                                           [new_adresse, label_code_barre_result["text"]])
                    self.db_conn.commit()
                    entry_nouvelle_adresse.delete(0, tk.END)
                    label_adresse_result["text"] = new_adresse
                    fen_adresse.destroy()

            if len(label_code_barre_result["text"]) != 0:
                fen_adresse = tk.Toplevel()
                if fen.winfo_x() + 600 + 310 < self.fen.winfo_screenwidth():
                    fen_adresse.geometry(f"310x150+{fen.winfo_x() + 600}+{fen.winfo_y()}")
                else:
                    fen_adresse.geometry(f"310x150+{fen.winfo_x() - 310}+{fen.winfo_y()}")
                fen_adresse.resizable(False, False)
                fen_adresse.transient(fen)
                fen_adresse.grab_set()
                fen_adresse.focus_set()

                frame = tk.LabelFrame(fen_adresse, text="Changement d'adresse", font=("Courrier", 12))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Adresse actuelle : ", font=("Courrier", 12)).grid(row=0, column=0,
                                                                                        sticky="ne", pady=5)
                tk.Label(frame, text=label_adresse_result["text"], font=("Courrier", 12)).grid(row=0, column=1,
                                                                                               sticky="w")
                tk.Label(frame, text="Nouvelle adresse : ", font=("Courrier", 12)).grid(row=1, column=0, sticky="ne",
                                                                                        pady=5)
                entry_nouvelle_adresse = tk.Entry(frame, font=("Courrier", 11))
                entry_nouvelle_adresse.grid(row=1, column=1, sticky="w")

                tk.Button(fen_adresse, text="Valider le changement", font=("Courrier", 12),
                          command=changer_adresse_fonction).pack(pady=5)

                fen_adresse.mainloop()

        def changer_code_postal_graphique():

            def changer_code_postal_fonction():
                new_code_postal = entry_nouveau_code_postal.get()
                if len(new_code_postal) != 0:
                    self.db_cursor.execute('UPDATE USAGER SET cp = ? WHERE code_barre = ?',
                                           [new_code_postal, label_code_barre_result["text"]])
                    self.db_conn.commit()
                    entry_nouveau_code_postal.delete(0, tk.END)
                    label_code_postal_result["text"] = new_code_postal
                    fen_code_postal.destroy()

            if len(label_code_barre_result["text"]) != 0:
                fen_code_postal = tk.Toplevel(fen)
                if fen.winfo_x() + 600 + 350 < self.fen.winfo_screenwidth():
                    fen_code_postal.geometry(f"350x150+{fen.winfo_x() + 600}+{fen.winfo_y()}")
                else:
                    fen_code_postal.geometry(f"350x150+{fen.winfo_x() - 350}+{fen.winfo_y()}")
                fen_code_postal.resizable(False, False)
                fen_code_postal.transient(fen)
                fen_code_postal.grab_set()
                fen_code_postal.focus_set()

                frame = tk.LabelFrame(fen_code_postal, text="Changement de code postal", font=("Courrier", 12))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Code postal actuelle : ", font=("Courrier", 12)).grid(row=0, column=0,
                                                                                            sticky="ne", pady=5)
                tk.Label(frame, text=label_code_postal_result["text"], font=("Courrier", 12)).grid(row=0, column=1,
                                                                                                   sticky="w")
                tk.Label(frame, text="Nouveau code postal : ", font=("Courrier", 12)).grid(row=1, column=0,
                                                                                           sticky="ne", pady=5)
                entry_nouveau_code_postal = tk.Entry(frame, font=("Courrier", 11))
                entry_nouveau_code_postal.grid(row=1, column=1, sticky="w")

                tk.Button(fen_code_postal, text="Valider le changement", font=("Courrier", 12),
                          command=changer_code_postal_fonction).pack(pady=5)

                fen.mainloop()

        def changer_ville_graphique():

            def changer_ville_fonction():
                new_ville = entry_nouvelle_ville.get().title()
                if len(new_ville) != 0:
                    self.db_cursor.execute('UPDATE USAGER SET ville = ? WHERE code_barre = ?',
                                           [new_ville, label_code_barre_result["text"]])
                    self.db_conn.commit()
                    entry_nouvelle_ville.delete(0, tk.END)
                    label_ville_result["text"] = new_ville
                    fen_ville.destroy()

            if len(label_code_barre_result["text"]) != 0:
                fen_ville = tk.Toplevel(fen)
                if fen.winfo_x() + 600 + 300 < self.fen.winfo_screenwidth():
                    fen_ville.geometry(f"300x150+{fen.winfo_x() + 600}+{fen.winfo_y()}")
                else:
                    fen_ville.geometry(f"300x150+{fen.winfo_x() - 300}+{fen.winfo_y()}")
                fen_ville.resizable(False, False)
                fen_ville.transient(fen)
                fen_ville.grab_set()
                fen_ville.focus_set()

                frame = tk.LabelFrame(fen_ville, text="Changement de ville", font=("Courrier", 12))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Ville actuelle : ", font=("Courrier", 12)).grid(row=0, column=0, sticky="ne",
                                                                                      pady=5)

                tk.Label(frame, text=label_ville_result["text"], font=("Courrier", 12)).grid(row=0, column=1,
                                                                                             sticky="w")

                tk.Label(frame, text="Nouvelle ville : ", font=("Courrier", 12)).grid(row=1, column=0, sticky="ne",
                                                                                      pady=5)

                entry_nouvelle_ville = tk.Entry(frame, font=("Courrier", 11))
                entry_nouvelle_ville.grid(row=1, column=1, sticky="w")

                tk.Button(fen_ville, text="Valider le changement", font=("Courrier", 12),
                          command=changer_ville_fonction).pack(pady=5)

                fen_ville.mainloop()

        def changer_email_graphique():

            def changer_email_fonction():
                new_email = entry_nouveau_email.get()
                if len(new_email) != 0:
                    self.db_cursor.execute('UPDATE USAGER SET email = ? WHERE code_barre = ?',
                                           [new_email, label_code_barre_result["text"]])
                    self.db_conn.commit()
                    entry_nouveau_email.delete(0, tk.END)
                    label_email_result["text"] = new_email
                    fen_email.destroy()

            if len(label_code_barre_result["text"]) != 0:
                fen_email = tk.Toplevel(fen)
                if fen.winfo_x() + 600 + 320 < self.fen.winfo_screenwidth():
                    fen_email.geometry(f"320x150+{fen.winfo_x() + 600}+{fen.winfo_y()}")
                else:
                    fen_email.geometry(f"320x150+{fen.winfo_x() - 320}+{fen.winfo_y()}")
                fen_email.resizable(False, False)
                fen_email.transient(fen)
                fen_email.grab_set()
                fen_email.focus_set()

                frame = tk.LabelFrame(fen_email, text="Changement d'email", font=("Courrier", 12))
                frame.pack(expand=tk.YES)

                tk.Label(frame, text="Email actuelle : ", font=("Courrier", 12)).grid(row=0, column=0,
                                                                                      sticky="ne", pady=5)
                tk.Label(frame, text=label_email_result["text"], font=("Courrier", 12)).grid(row=0, column=1,
                                                                                             sticky="w")
                tk.Label(frame, text="Nouveau email : ", font=("Courrier", 12)).grid(row=1, column=0,
                                                                                     sticky="ne", pady=5)
                entry_nouveau_email = tk.Entry(frame, font=("Courrier", 12))
                entry_nouveau_email.grid(row=1, column=1, sticky="w")

                tk.Button(fen_email, text="Valider le changement", font=("Courrier", 12),
                          command=changer_email_fonction).pack(pady=5)

                fen_email.mainloop()

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"600x400+{self.fen.winfo_x() + 100}+{self.fen.winfo_y() + 50}")
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame_recherche_usager = tk.LabelFrame(fen, text="Rechercher la personne", font=("Courrier", 12))
        frame_recherche_usager.pack(expand=tk.YES)

        frame_changer_usager = tk.LabelFrame(fen, text="Changer les données d'un usager", font=("Courrier", 12))
        frame_changer_usager.pack(expand=tk.YES)

        label_code_barre = tk.Label(frame_recherche_usager, text="Code barre : ", font=("Courrier", 12))
        label_code_barre.grid(row=0, column=0, sticky="ne", pady=5)

        self.db_cursor.execute('SELECT code_barre FROM USAGER')
        combobox_code_barre = ttk.Combobox(frame_recherche_usager, values=[x for x in self.db_cursor.fetchall()],
                                           font=("Courrier", 11), state="readonly")
        combobox_code_barre.grid(row=0, column=1)

        label_nom = tk.Label(frame_changer_usager, text="Nom : ", font=("Courrier", 12))
        label_nom.grid(row=0, column=0, sticky="ne", pady=5)

        label_nom_result = tk.Label(frame_changer_usager, font=("Courrier", 12))
        label_nom_result.grid(row=0, column=1, sticky="w")

        button_nom = tk.Button(frame_changer_usager, text="Changer", font=("Courrier", 12),
                               command=changer_nom_graphique)
        button_nom.grid(row=0, column=2, sticky="w")

        label_prenom = tk.Label(frame_changer_usager, text="Prénom : ", font=("Courrier", 12))
        label_prenom.grid(row=1, column=0, sticky="ne", pady=5)

        label_prenom_result = tk.Label(frame_changer_usager, font=("Courrier", 12))
        label_prenom_result.grid(row=1, column=1, sticky="w")

        button_prenom = tk.Button(frame_changer_usager, text="Changer", font=("Courrier", 12),
                                  command=changer_prenom_graphique)
        button_prenom.grid(row=1, column=2, sticky="w")

        label_adresse = tk.Label(frame_changer_usager, text="Adresse : ", font=("Courrier", 12))
        label_adresse.grid(row=2, column=0, sticky="ne", pady=5)

        label_adresse_result = tk.Label(frame_changer_usager, font=("Courrier", 12))
        label_adresse_result.grid(row=2, column=1, sticky="w")

        button_adresse = tk.Button(frame_changer_usager, text="Changer", font=("Courrier", 12),
                                   command=changer_adresse_graphique)
        button_adresse.grid(row=2, column=2, sticky="w")

        label_code_postal = tk.Label(frame_changer_usager, text="Code postal : ", font=("Courrier", 12))
        label_code_postal.grid(row=3, column=0, sticky="ne", pady=5)

        label_code_postal_result = tk.Label(frame_changer_usager, font=("Courrier", 12))
        label_code_postal_result.grid(row=3, column=1, sticky="w")

        button_code_postal = tk.Button(frame_changer_usager, text="Changer", font=("Courrier", 12),
                                       command=changer_code_postal_graphique)
        button_code_postal.grid(row=3, column=2, sticky="w")

        label_ville = tk.Label(frame_changer_usager, text="Ville : ", font=("Courrier", 12))
        label_ville.grid(row=4, column=0, sticky="ne", pady=5)

        label_ville_result = tk.Label(frame_changer_usager, font=("Courrier", 12))
        label_ville_result.grid(row=4, column=1, sticky="w")

        button_ville = tk.Button(frame_changer_usager, text="Changer", font=("Courrier", 12),
                                 command=changer_ville_graphique)
        button_ville.grid(row=4, column=2, sticky="w")

        label_email = tk.Label(frame_changer_usager, text="Email : ", font=("Courrier", 12))
        label_email.grid(row=5, column=0, sticky="ne", pady=5)

        label_email_result = tk.Label(frame_changer_usager, font=("Courrier", 12))
        label_email_result.grid(row=5, column=1, sticky="w")

        button_email = tk.Button(frame_changer_usager, text="Changer", font=("Courrier", 12),
                                 command=changer_email_graphique)
        button_email.grid(row=5, column=2, sticky="w")

        label_code_barre = tk.Label(frame_changer_usager, text="Code barre : ", font=("Courrier", 12))
        label_code_barre.grid(row=6, column=0, sticky="ne", pady=5)

        label_code_barre_result = tk.Label(frame_changer_usager, font=("Courrier0", 11))
        label_code_barre_result.grid(row=6, column=1, sticky="w")

        combobox_code_barre.bind("<Return>", lambda event: affiche_usager_avec_code_barre())
        fen.protocol("WM_DELETE_WINDOW", lambda: fen.destroy())
        fen.mainloop()

    def supprimer_livre_graphique(self):

        def affiche_livre_avec_isbn():
            isbn = combobox_isbn.get()
            if len(isbn) != 0:
                self.db_cursor.execute('SELECT * FROM LIVRE WHERE isbn = ?', [isbn, ])
                data_livre = self.db_cursor.fetchall()[0]
                label_titre_result["text"] = data_livre[0]
                label_editeur_result["text"] = data_livre[1]
                label_annee_result["text"] = data_livre[2]
                label_isbn_result["text"] = data_livre[3]

        def supprimer_livre_fonction():
            if len(label_isbn_result["text"]) != 0:
                validation = messagebox.askquestion(f"Confirmation", f"Voulez-vous vraiment supprimer "
                                                                     f"le livre {label_isbn_result['text']} ?",
                                                    parent=fen)
                if validation == "yes":
                    self.db_cursor.execute('DELETE FROM LIVRE WHERE isbn = ?', [label_isbn_result["text"], ])
                    self.db_conn.commit()
                    combobox_isbn.set("")
                    label_titre_result["text"] = ""
                    label_editeur_result["text"] = ""
                    label_annee_result["text"] = ""
                    label_isbn_result["text"] = ""

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"500x280+{self.fen.winfo_x() + 150}+{self.fen.winfo_y() + 110}")
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame_rechercher_livre = tk.LabelFrame(fen, text="Rechercher le livre", font=("Courrier", 12))
        frame_rechercher_livre.pack(expand=tk.YES)

        frame_supprimer_livre = tk.LabelFrame(fen, text="Supprimer le livre", font=("Courrier", 12))
        frame_supprimer_livre.pack(expand=tk.YES)

        label_isbn = tk.Label(frame_rechercher_livre, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=0, column=0, sticky="ne", pady=5)

        self.db_cursor.execute('SELECT LIVRE.isbn FROM LIVRE EXCEPT SELECT EMPRUNT.isbn FROM EMPRUNT')
        combobox_isbn = ttk.Combobox(frame_rechercher_livre, values=[x[0] for x in self.db_cursor.fetchall()],
                                     font=("Courrier", 11), state="readonly")
        combobox_isbn.grid(row=0, column=1, sticky="w")

        label_titre = tk.Label(frame_supprimer_livre, text="Titre : ", font=("Courrier", 12))
        label_titre.grid(row=0, column=0, sticky="ne", pady=5)

        label_titre_result = tk.Label(frame_supprimer_livre, font=("Courrier", 12))
        label_titre_result.grid(row=0, column=1, sticky="w")

        label_editeur = tk.Label(frame_supprimer_livre, text="Editeur : ", font=("Courrier", 12))
        label_editeur.grid(row=1, column=0, sticky="ne", pady=5)

        label_editeur_result = tk.Label(frame_supprimer_livre, font=("Courrier", 12))
        label_editeur_result.grid(row=1, column=1, sticky="w")

        label_annee = tk.Label(frame_supprimer_livre, text="Année : ", font=("Courrier", 12))
        label_annee.grid(row=2, column=0, sticky="ne", pady=5)

        label_annee_result = tk.Label(frame_supprimer_livre, font=("Courrier", 12))
        label_annee_result.grid(row=2, column=1, sticky="w")

        label_isbn = tk.Label(frame_supprimer_livre, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=3, column=0, sticky="ne", pady=5)

        label_isbn_result = tk.Label(frame_supprimer_livre, font=("Courrier", 12))
        label_isbn_result.grid(row=3, column=1, sticky="w")

        button_validate = tk.Button(fen, text="Valider la suppression", font=("Courrier", 12),
                                    command=supprimer_livre_fonction)
        button_validate.pack(pady=5)

        combobox_isbn.bind("<Return>", lambda event: affiche_livre_avec_isbn())
        fen.mainloop()

    def supprimer_emprunt_graphique(self):

        def affiche_emprunt_avec_isbn():
            isbn = combobox_isbn.get()
            if len(isbn) != 0:
                self.db_cursor.execute('SELECT * FROM EMPRUNT WHERE isbn = ?', [isbn, ])
                data_emprunt = self.db_cursor.fetchall()[0]
                label_code_barre_result["text"] = data_emprunt[0]
                label_isbn_result["text"] = data_emprunt[1]
                label_retour_result["text"] = data_emprunt[2]

        def supprimer_emprunt_fonction():
            if len(label_isbn_result["text"]) != 0:
                validation = messagebox.askquestion("Confirmation", f"Voulez-vous supprimer "
                                                                    f"l'emprunt {label_isbn_result['text']} ?",
                                                    parent=fen)
                if validation == "yes":
                    self.db_cursor.execute('DELETE FROM EMPRUNT WHERE isbn = ?', [label_isbn_result["text"], ])
                    self.db_conn.commit()
                    combobox_isbn.set("")
                    label_code_barre_result["text"] = ""
                    label_isbn_result["text"] = ""
                    label_retour_result["text"] = ""

        fen = tk.Toplevel(self.fen)
        fen.geometry(f"400x250+{self.fen.winfo_x() + 200}+{self.fen.winfo_y() + 120}")
        fen.resizable(False, False)
        fen.transient(self.fen)
        fen.grab_set()
        fen.focus_set()

        frame_rechercher_emprunt = tk.LabelFrame(fen, text="Rechercher l'emprunt", font=("Courrier", 12))
        frame_rechercher_emprunt.pack(expand=tk.YES)

        frame_supprimer_emprunt = tk.LabelFrame(fen, text="Supprimer l'emprunt", font=("Courrier", 12))
        frame_supprimer_emprunt.pack(expand=tk.YES)

        label_isbn = tk.Label(frame_rechercher_emprunt, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=0, column=0, sticky="ne", pady=5)

        self.db_cursor.execute('SELECT isbn FROM EMPRUNT')
        combobox_isbn = ttk.Combobox(frame_rechercher_emprunt, values=[x[0] for x in self.db_cursor.fetchall()],
                                     font=("Courrier", 11), state="readonly")
        combobox_isbn.grid(row=0, column=1, sticky="w")

        label_code_barre = tk.Label(frame_supprimer_emprunt, text="Code barre : ", font=("Courrier", 12))
        label_code_barre.grid(row=0, column=0, sticky="ne", pady=5)

        label_code_barre_result = tk.Label(frame_supprimer_emprunt, font=("Courrier", 12))
        label_code_barre_result.grid(row=0, column=1, sticky="w")

        label_isbn = tk.Label(frame_supprimer_emprunt, text="Isbn : ", font=("Courrier", 12))
        label_isbn.grid(row=1, column=0, sticky="ne", pady=5)

        label_isbn_result = tk.Label(frame_supprimer_emprunt, font=("Courrier", 12))
        label_isbn_result.grid(row=1, column=1, sticky="w")

        label_retour = tk.Label(frame_supprimer_emprunt, text="Date de retour : ", font=("Courrier", 12))
        label_retour.grid(row=2, column=0, sticky="ne", pady=5)

        label_retour_result = tk.Label(frame_supprimer_emprunt, font=("Courrier", 12))
        label_retour_result.grid(row=2, column=1, sticky="w")

        button_validate = tk.Button(fen, text="Valider la suppression", font=("Courrier", 12),
                                    command=supprimer_emprunt_fonction)
        button_validate.pack(pady=5)

        combobox_isbn.bind("<Return>", lambda event: affiche_emprunt_avec_isbn())
        fen.mainloop()


if __name__ == '__main__':
    app = App()
