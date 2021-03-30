from tkinter import *
from navigateur import *
from requete_mail_devoirs import *
from fernet import Fernet

class Work(Frame):
    def __init__(self, titre, contenu, data_id, master=None):
        super().__init__(master, relief=GROOVE, bd=2)
        self.pack(fill=BOTH, padx=10, pady=10)
        self.titre = titre.strip()
        lettre_precedente = ""
        liste_lettre = []
        for lettre in contenu:
            if lettre == " " and lettre_precedente == " ":
                pass
            else:
                liste_lettre.append(lettre)
            lettre_precedente = lettre
        self.contenu = "".join(liste_lettre)
        del liste_lettre, lettre, lettre_precedente
        self.contenu = self.contenu.strip()
        self.data_id = data_id
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=3)
        self.columnconfigure(0, weight=50)
        self.columnconfigure(1, weight=1)
        global fenetre
        self.editing_window = Editing_work(self, master=fenetre)
        self.create()
    
    def create(self):
        self.espace_texte = Frame(self)
        self.espace_texte.grid(row=0, rowspan=2, column=0, sticky="nsew")
        self.label_titre = Label(self.espace_texte, text=self.titre, anchor='w')
        self.label_titre.grid(row=0, sticky="nsew")
        self.label_contenu = Label(self.espace_texte, text=self.contenu, anchor='w', wraplength=650, justify=LEFT)
        self.label_contenu.grid(row=1, sticky="nsew")
        self.boutton_lien = Button(self, text='OUVRIR', cursor='hand1', command=self.ouvrir)
        self.boutton_lien.grid(row=0, column=1, sticky="nsew")
        self.boutton_edit = Button(self, text='EDITER', cursor='hand1', command=self.editing_window.open)
        self.boutton_edit.grid(row=1, column=1, sticky="nsew")
    
    def ouvrir(self):
        global web
        web.ouvrir_devoir(self.data_id)

class Editing_work(Frame):
    def __init__(self, work, master=None):
        super().__init__(master)
        self.work = work
    
    def open(self):
        global fenetre_actu
        fenetre_actu.pack_forget()
        self.pack(fill=BOTH)
        self.label_titre = Label(self, text=self.work.titre, anchor='w')
        self.label_titre.pack()
        self.label_contenu = Label(self, text=self.work.contenu, anchor='w', wraplength=650, justify=LEFT)
        self.label_contenu.pack()
        self.boutton_retour = Button(self, text='RETOUR', cursor='hand1', command=fenetre_actu.open)
        self.boutton_retour.pack()
        fenetre_actu = self
        
class MainPage(Canvas):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack(fill=BOTH)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.columnconfigure(0, weight=1, minsize=200)
        self.columnconfigure(1, weight=3)

        global web, http

        mbn = Button(self, text='MON BUREAU\nNUMERIQUE', cursor='hand1', command=web.ouvrir_mbn)
        mbn.grid(row=0, column=0, sticky="nsew")

        gestion_fichiers = Button(self, text='GESTION\nDES FICHIERS', cursor='hand1')
        gestion_fichiers.grid(row=1, column=0, sticky="nsew")

        espace_news = Canvas(self)
        espace_news.grid(row=0, rowspan=2, column=1, sticky="nsew")
        i = 0
        news=[]
        for devoir in http.get_taf():
            titre = devoir['matiere']
            contenu = devoir['contenu']
            data_id = str(devoir['id_devoir'])
            news.append(Work(titre, contenu, data_id, master=espace_news))
            news[i].create()
            i += 1
    def open(self):
        global fenetre_actu
        fenetre_actu.pack_forget()
        self.pack(fill=BOTH)
        fenetre_actu = self


try:
    file_key = open('key.key', 'rb')
    key = file_key.read()
    file_key.close()
    file_password = open('password.txt', 'rb')
    password_encrypted = file_password.read()
    file_password.close()
    assert password_encrypted != ""
    f = Fernet(key)
    password = f.decrypt(password_encrypted)
    password = password.decode()
except:
    key = Fernet.generate_key()
    f = Fernet(key)
    password = input('Quel est le mot de passe')
    password_encrypted = password.encode()
    password_encrypted = f.encrypt(password_encrypted)
    file_key = open('key.key', 'wb')
    file_key.write(key)
    file_key.close()
    file_password = open('password.txt', 'wb')
    file_password.write(password_encrypted)
    file_password.close()

web = ChromeMbn('f.henrotterobe', password)
http = SessionMonBureauNumerique('f.henrotterobe', password)

fenetre = Tk()

fenetre.geometry("1000x400")
fenetre_principale = MainPage(master=fenetre)
fenetre_actu = fenetre_principale

fenetre.mainloop()