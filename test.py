from tkinter import *
from tkinter import ttk

class Edit():
    def ouvrir(self, command):
        global liste_matiere
        self.edit = Tk()

        self.label_matiere = Label(self.edit, text='MATIERE :')
        self.label_matiere.pack(side=TOP)
        self.champ_matiere = Entry(self.edit)
        self.champ_matiere.pack(side=TOP)
        self.label_rac = Label(self.edit, text='Rac')
        self.label_rac.pack(side=TOP)
        self.champ_rac = Entry(self.edit)
        self.champ_rac.pack(side=TOP)
        self.bouton_confirmer = Button(self.edit)
        self.bouton_confirmer.pack(side=BOTTOM)
        self.label_error = Label(self.edit, text='')
        self.label_error.pack(side=BOTTOM)
        if command == 'add':
            self.bouton_confirmer['text'] = 'AJOUTER'
            self.bouton_confirmer['command'] = self.send_add
        else:
            self.bouton_confirmer['text'] = 'MODIFIER'
            self.bouton_confirmer['command'] = self.send_modif
            value = str(liste_matiere.get(ACTIVE))
            value = value.split(' : ')
            self.champ_matiere.insert(0, value[0])
            self.champ_rac.insert(0, value[1])
            self.index_choisi = int(liste_matiere.curselection()[0])


        self.edit.mainloop()

    def send_add(self):
        matiere = self.champ_matiere.get()
        rac = self.champ_rac.get()
        if (rac and matiere) == "":         
            self.label_error['text'] = 'ERROR'
        else:
            liste_matiere.insert(END, str(matiere + ' : ' + rac))
            self.edit.destroy()

    def send_modif(self):
        matiere = self.champ_matiere.get()
        rac = self.champ_rac.get()
        if (rac and matiere) == "":         
            self.label_error['text'] = 'ERROR'
        else:
            liste_matiere.delete(self.index_choisi)
            liste_matiere.insert(self.index_choisi, str(matiere + ' : ' + rac))
            self.edit.destroy()


def creer_add():
    edit = Edit()
    edit.ouvrir('add')
def creer_modif():
    edit = Edit()
    edit.ouvrir('mod')


fenetre = Tk()
global liste_matiere
liste_matiere = Listbox(fenetre)
liste_matiere.pack(pady=10)

bouton_modifier = Button(fenetre, text='AJOUTER', command=creer_add)
bouton_modifier.pack(side=BOTTOM)
bouton_modifier = Button(fenetre, text='MODIFIER', command=creer_modif)
bouton_modifier.pack(side=BOTTOM)

fenetre.mainloop()


