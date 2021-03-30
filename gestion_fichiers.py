from os import mkdir, listdir
from os import rename as move


def create_files(index, jour, date_donnee, mois):
    jours = ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']
    date = date_donnee
    mois_liste = ['Novembre', 'Decembre']
    index_mois = mois_liste.index(mois)
    i = jours.index(jour)
    is_present = False
    l = index + 1
    if date == 30:
        index_mois += 1
        date = 1
    if i == 4:
        i = 0
        date += 2
    else:
        i += 1
        date += 1
    while l < index + 8:
        if is_present:
            mkdir(str('[' + str(l) + '] ' + jours[i] + ' ' + str(date) + ' ' + mois_liste[index_mois]))
            l += 1
        date += 1
        if i == 4:
            i = 0
            date += 2
        else:
            i += 1
        if date == 30:
            index_mois += 1
            date = 1
        is_present = not(is_present)

def func_file():
    liste = [i for i in listdir()]
    liste_fichiers = [i for i in liste for jour in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi'] if jour in i]
    if liste_fichiers != []:
        dernier_element = liste_fichiers[-1]
        index = int(dernier_element[1])
        for jour in ['Lundi', 'Mardi', 'Mercredi', 'Jeudi', 'Vendredi']:
            if jour in dernier_element:
                jour_elmt = jour
                break
        temp = 5 + len(jour_elmt)
        date = int(dernier_element[temp : temp + 2])
        mois = dernier_element[temp + 2:].strip()
    else:
        index = 0
        jour = 'Jeudi'
        date = 12
        mois = 'Novembre'

    create_files(index, jour, date, mois)


def move_file():
    file_liste = listdir()
    fichiers_liste = [elmt for elmt in file_liste if elmt[-3:] == '.md']
    for i in range(len(fichiers_liste)):
        f = open(fichiers_liste[i], 'r')
        date_trouvee = f.readlines(1)
        f.close()
        date_trouvee = "".join(date_trouvee)
        date_trouvee = date_trouvee.split('/')
        date_trouvee = tuple(date_trouvee)
        jour, mois, annee = date_trouvee
        mois_liste = ['Janvier', 'Fevrier', 'Mars', 'Avril', 'Mai', 'Juin', 'Juillet', 'Août', 'Septembre', 'Octobre', 'Novembre', 'Decembre']
        mois = mois_liste[int(mois) - 1]
        for dossier in file_liste:
            if str(jour + ' ' + mois) in dossier:
                dossier_destination = dossier
        path_destination = dossier_destination + '\ '.strip() + fichiers_liste[i]
        move(fichiers_liste[i], path_destination)